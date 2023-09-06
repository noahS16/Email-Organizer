import db
from emails import GmailOp
import re
from PyQt5.QtWidgets import QListWidgetItem


class Message(QListWidgetItem):
    def __init__(self, subject, msg_id):
        super().__init__()
        self.subject = subject
        self.msg_id = msg_id
        self.setText(subject)

    def get_id(self):
        return self.msg_id

    def get_subject(self):
        return self.text()


class User:
    def __init__(self, username):
        self.username = username
        self.inbox = db.get_all_messages(username)

    def setup_inbox(self):
        all_messages = db.get_all_messages(self.username)
        inbox = {}
        for sender, mssgs in all_messages.items():
            inbox[sender] = []
            for msg in mssgs:
                message = Message(msg['subject'], msg['id'])
                inbox[sender].append(message)
        return inbox

    def get_num_messages_from(self, sender):
        return len(self.inbox[sender])

    def get_total_num_messages(self):
        total = 0
        for sender in self.inbox:
            total += len(self.inbox[sender])
        return total

    def get_total_num_senders(self):
        total = len(self.inbox.keys())
        return total

    def get_all_senders(self, sort=False, rev=False):
        senders = list(self.inbox.keys())
        if sort:
            senders = sorted(senders, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())
        elif rev:
            senders = reversed(senders)
        return senders

    def get_messages_from(self, sender, sort=False, rev=False):
        messages = self.create_message_items(sender)
        if sort:
            messages = sorted(messages, key=lambda x: re.sub('[^A-Za-z]+', '', x.subject).lower())
        elif rev:
            messages = reversed(messages)
        return messages

    def create_message_items(self, sender):
        data = self.inbox[sender]
        messages = []
        for msg in data:
            messages.append(Message(msg['subject'], msg['id']))
        return messages

    def update_inbox(self):
        self.inbox = db.get_all_messages(self.username)

    def delete_senders(self, senders):
        print("SENDERS TO DELETE:", senders)
        gmail_user = GmailOp(self.username)
        ids = []
        for sender in senders:
            for msg in self.inbox[sender]:
                ids.append(msg['id'])
            del self.inbox[sender]
        gmail_user.delete_messages(ids)
        self.update_db()

    def trash_senders(self, senders):
        print("SENDERS TO TRASH:", senders)
        gmail_user = GmailOp(self.username)
        ids = []
        for sender in senders:
            for msg in self.inbox[sender]:
                ids.append(msg['id'])
            del self.inbox[sender]
        gmail_user.trash_messages(ids)
        self.update_db()

    def remove_messages(self, message_ids, sender):
        print("MESSAGES TO DELETE", message_ids, len(message_ids))
        index = 0
        for msg in self.inbox[sender][:]:
            if msg['id'] in message_ids:
                self.inbox[sender].pop(index)
                index -= 1
            index += 1
            if len(self.inbox[sender]) == 0:
                del self.inbox[sender]
                break

    def delete_messages(self, ids, sender):
        gmail_user = GmailOp(self.username)
        self.remove_messages(ids, sender)
        gmail_user.delete_messages(ids)
        self.update_db()

    def trash_messages(self, ids, sender):
        gmail_user = GmailOp(self.username)
        self.remove_messages(ids, sender)
        gmail_user.trash_messages(ids)
        self.update_db()

    def update_db(self):
        db.update_account(self.inbox, self.username)


class UsersCache:
    def __init__(self):
        self.records = {}

    def add_user(self, username):
        newUser = User(username)
        self.records[username] = newUser

    def remove_user(self, username):
        del self.records[username]
        db.delete_account(username)
