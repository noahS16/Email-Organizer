from pymongo import MongoClient
import os
import random
import re

MONGODB_URI = "mongodb://localhost:27017"


def insert_new_account(username):
    if not username:
        return False
    client = MongoClient(MONGODB_URI)
    db = client.cleanup
    users = db.users
    new_account = {"username": username}
    result = users.update_one(new_account, {"$setOnInsert": new_account}, upsert=True)
    print("INSERTED: ", result)
    client.close()


def update_account(data, username):
    client = MongoClient(MONGODB_URI)
    db = client.cleanup
    users = db.users
    users.update_one({"username": username}, {"$set": {"messages": data}})
    client.close()


def get_all_senders(username, sortAlph=False):
    client = MongoClient(MONGODB_URI)
    db = client.cleanup
    users = db.users
    senders = users.find_one({"username": username})
    senders = senders.get("messages").keys()
    result = senders if not sortAlph else sorted(senders, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())
    client.close()
    return list(result)


def get_subjects_by_sender(username, sender, sortAlph=False):
    client = MongoClient(MONGODB_URI)
    db = client.cleanup
    users = db.users
    data = users.find_one({"username": username})
    data = data.get("messages").get(sender)
    subjects = []
    for msg in data:
        subjects.append(msg.get('subject'))
    subjects = subjects if not sortAlph else sorted(subjects, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())
    client.close()
    return subjects


def delete_account(username):
    os.remove(os.path.abspath(f"creds/{username}token.pickle"))
    client = MongoClient(MONGODB_URI)
    db = client.cleanup
    users = db.users
    users.delete_many({"username": username})
    client.close()


def get_all_accounts():
    client = MongoClient(MONGODB_URI)
    db = client.cleanup
    users = db.users
    all_users = []
    for doc in users.find():
        all_users.append(doc['username'])
    client.close()
    return all_users


def get_all_messages(username):
    client = MongoClient(MONGODB_URI)
    db = client.cleanup
    user = db.users
    messages = user.find_one({"username": username})
    result = messages['messages']
    client.close()
    return result


def delete_senders(username, senders):
    client = MongoClient(MONGODB_URI)
    db = client.cleanup
    users = db.users
    data = users.find_one({"username": username})
    messages = data.get("messages")
    client.close()
    to_delete = []
    ids = []
    while senders:
        to_delete.append(messages.pop(senders[0]))
        del messages[senders.pop(0)]
    for msg in to_delete:
        for i in range(len(msg)):
            ids.append(msg[i]['id'])
    update_account(messages, username)
    return ids


def delete_messages(username, sender, subjects):
    messages = get_all_messages(username)
    index = 0
    msg_ids = []
    while subjects:
        if messages[sender][index]['subject'] in subjects:
            msg = messages[sender].pop(index)
            msg_ids.append(msg['id'])
            print("REMOVED::", msg)
            subjects.remove(msg['subject'])
            index -= 1
            if len(messages[sender]) == 0:
                del messages[sender]
                break
        index += 1
    update_account(messages, username)
    return msg_ids


def delete_message(username, sender, message):
    messages = get_all_messages(username)
    for i in range(len(messages[sender])):
        if messages[sender][i]['subject'] == message:
            msg_id = messages[sender][i]['id']
            del messages[sender][i]
            if len(messages[sender]) == 0:
                del messages[sender]
            return msg_id
    update_account(messages, username)


def get_message_id(username, sender, subject):
    messages = get_all_messages(username)
    messages = messages[sender]
    if subject == "":
        msg_id = messages[random.randint(0, len(messages) - 1)]['id']
        return msg_id
    for msg in messages:
        if msg['subject'] == subject:
            msg_id = msg['id']
            return msg_id
    return None


def get_number_of_messages_from(username, sender):
    messages = get_subjects_by_sender(username, sender)
    return len(messages)


def get_total_num_messages(username):
    messages = get_all_messages(username)
    total = 0
    for sender in messages:
        total += len(messages[sender])
    return total


def get_total_num_senders(username):
    messages = get_all_messages(username)
    return len(messages.keys())
