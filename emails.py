# THIS FILE HANDLES EMAIL AUTHENTICATION AND FETCHING
# NOAH SAENZ - 01/31/2023
import os
import pickle
import socket
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import db
from base64 import urlsafe_b64decode
from bs4 import BeautifulSoup
import google.auth.exceptions


# Request all access (permission to read/send/receive emails, manage the inbox, and more)
class GmailOp:
    SCOPES = ['https://mail.google.com/']
    socket.setdefaulttimeout(60 * 30)

    def __init__(self, username):
        self.username = username
        self.connection = self.gmail_authenticate(username)

    def gmail_authenticate(self, user):
        # insert_new_account(user)
        creds = None
        path = 'creds/' + user + 'token.pickle'
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists(path):
            with open(path, "rb") as token:
                token.flush()
                creds = pickle.load(token)
        # if there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except google.auth.exceptions.RefreshError:
                    print("ERROR")
                    os.remove(os.path.abspath(path))
                    flow = InstalledAppFlow.from_client_secrets_file('creds/credentials.json', GmailOp.SCOPES)
                    creds = flow.run_local_server(port=0)
            else:
                flow = InstalledAppFlow.from_client_secrets_file('creds/credentials.json', GmailOp.SCOPES)
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open(path, "wb") as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)

    # Return all senders in inbox
    def get_all_senders(self):
        messages = self.get_all_messages()
        count = 0
        all_senders = {}
        for msg in messages:
            msg_id = msg.get('id')
            info = self.get_message_info(msg_id)
            sender = info.get('from').split(' <')[
                0]  # extract sender name only from --> ["Amazon <noreply@amazon.com>"]
            if sender in all_senders:
                all_senders[sender].append(info.get('subject'))
            else:
                all_senders[sender] = [info.get('subject')]
            count += 1
            print('ADDED', count)
        print(len(all_senders))
        return all_senders  # Return all message IDs --> [{id: '', threadId: ''},...]

    def get_all_messages(self, query=""):
        connection = self.connection
        result = connection.users().messages().list(userId='me', q=query, includeSpamTrash=False).execute()
        messages = []
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = connection.users().messages().list(userId='me', includeSpamTrash=False,
                                                        pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        print(len(messages))
        connection.close()
        return messages

    # Return message info given message ID --> {from: '', to: '', subject: '', date: ''}
    def get_message_info(self, message_id):
        connection = self.connection
        msg = connection.users().messages().get(userId='me', id=message_id, format='full').execute()
        # pprint.pprint(msg)
        payload = msg['payload']
        headers = payload.get("headers")
        # pprint.pprint(payload)
        info = {}
        if headers:
            for header in headers:
                name = header.get("name")
                value = header.get("value")
                self.add_header_value(name, value, info)
        connection.close()
        return info

    def get_all_messages_info(self):
        messages = self.get_all_messages()
        data = {}
        count = 0
        for msg in messages:
            info = self.get_message_info(msg.get('id'))
            if info.get('from', None):
                data[info.get('from')].append(data)
            else:
                data[info.get('from')] = [data]
            count += 1
            print(count)
        return data

    def add_header_value(self, name, value, info):
        name = name.lower()
        if name == 'from':
            value = value.split(' <')[0]  # Amazon <amazon@amazon.com>
        if name == 'from' or name == 'subject' or name == 'date':
            info[name] = value

    def get_messages_by_sender(self, sender):
        emails = self.get_all_messages(query=f"from:{sender}")
        subjects = []
        # filter fetched messages to obtain exact sender only, add ids as metadata and write to json
        for msg in emails:
            message_info = self.get_message_info(msg.get('id'))
            sub = message_info['subject']
            if message_info['from'] == sender:
                subjects.append(sub)
        return subjects

    def delete_messages(self, message_ids):
        chunked_ids = self.handle_load(message_ids)
        connection = self.connection
        for chunk in chunked_ids:
            connection.users().messages().batchDelete(userId='me', body={'ids': chunk}).execute()
        connection.close()

    def handle_load(self, message_ids):
        factors = str(len(message_ids) / 1000).split('.')
        thousands = int(factors[0])
        chunks = []
        right = 0
        for i in range(thousands):
            right += 1000
            chunks.append(message_ids[i * 1000:right])
        last_chunk = message_ids[right:]
        if len(last_chunk) > 0:
            chunks.append(message_ids[right:])
        return chunks

    def trash_messages(self, message_ids):
        connection = self.connection
        for msg in message_ids:
            connection.users().messages().trash(userId='me', id=msg).execute()
        connection.close()

    def get_message_parts(self, msg_id):
        connection = self.connection
        msg = connection.users().messages().get(userId='me', id=msg_id, format='full').execute()
        payload = msg.get('payload')
        parts = payload.get('parts')
        if not parts:
            parts = payload.get('body').get('data')
        return parts

    def get_html_message(self, sender, message=""):
        msg_id = db.get_message_id(self.username, sender, subject=message)
        parts = self.get_message_parts(msg_id)
        if type(parts) is dict:
            for part in parts:
                mimeType = part.get('mimeType')
                body = part.get('body')
                data = body.get('data')
                if mimeType == 'text/html':
                    return self.make_html_file(data)
        else:
            data = parts
            return self.make_html_file(data)

    def make_html_file(self, data):
        if type(data) is list:
            for part in data:
                if part.get('mimeType') == 'text/html':
                    data = part.get('body').get('data')
                    break
        if os.path.isfile('message.html'):
            os.remove('message.html')
        with open('sites/message.html', 'wb') as file:
            try:
                file.write(urlsafe_b64decode(data))
            except TypeError:
                return False
        return True

    def get_unsubscribe_link(self, sender):
        self.get_html_message(sender)
        with open("sites/message.html", 'r') as file:
            doc = BeautifulSoup(file, "html.parser")
        a_tags = doc.find_all(["a"], text=["unsubscribe", "Unsubscribe", "Email Preferences", "email preferences",
                                           "opt out", "opt-out", "Opt Out", "optout", "Manage Preferences",
                                           "Manage Your Preferences",
                                           "UNSUBSCRIBE", "UNSUBSCRIBE NOW", "unsubscribe now", "Unsubscribe Now",
                                           "CLICK HERE TO UNSUBSCRIBE", "click here to unsubscribe",
                                           "CLICK HERE NOW TO UNSUBSCRIBE", "click here now to unsubscribe",
                                           "CLICK HERE TO UNSUBSCRIBE NOW", "click here to unsubscribe now",
                                           "unsubscribe here", "Unsubscribe here", "Unsubscribe Here"])

        if len(a_tags) == 0:
            text = doc.find_all(text=["unsubscribe", "Unsubscribe", "Email Preferences", "email preferences",
                                      "opt out", "Opt Out", "optout", "Manage Preferences", "Manage Your Preferences",
                                      "UNSUBSCRIBE", "UNSUBSCRIBE NOW", "unsubscribe now", "Unsubscribe Now",
                                      "CLICK HERE TO UNSUBSCRIBE", "click here to unsubscribe",
                                      "CLICK HERE NOW TO UNSUBSCRIBE", "click here now to unsubscribe",
                                      "CLICK HERE TO UNSUBSCRIBE NOW", "click here to unsubscribe now",
                                      "unsubscribe?", "manage your preferences", "manage your subscription preferences",
                                      "to unsubscribe", "mailing list", "opt-out",
                                      "unsubscribe here", "Unsubscribe here", "Unsubscribe Here"
                                      ])
            if not text:
                return None
            parent = text[0].parent
            link = parent.get('href', None)
            return link
        link = a_tags[0].get('href', None)
        return link

