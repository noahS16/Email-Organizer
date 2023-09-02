from PyQt5.QtCore import QThread, pyqtSignal
import db
from emails import GmailOp


class ProgressThread(QThread):
    update = pyqtSignal(int, int)
    finished = pyqtSignal()
    cancel = pyqtSignal()

    def __init__(self, ui, username):
        super().__init__()
        self.ui = ui
        self.username = username

    def load_all_senders(self, username):
        user = GmailOp(username)
        messages = user.get_all_messages(username)
        self.ui.progressBar.setMaximum(len(messages))
        count = 0
        all_senders = {}
        for msg in messages:
            msg_id = msg.get('id')
            info = user.get_message_info(msg_id)
            sender = info.get('from')
            if all_senders.get(sender, None):
                all_senders[sender].append({"subject": info.get('subject'), "id": msg.get('id')})
                self.update.emit(len(messages), count)
            else:
                all_senders[sender] = [{"subject": info.get('subject'), "id": msg.get('id')}]
                self.update.emit(len(messages), count)
            count += 1
            # print('ADDED', count)
        print(len(all_senders))
        db.insert_new_account(self.username)
        db.update_account(all_senders, username)
        self.finished.emit()

    def run(self):
        self.load_all_senders(self.username)


class DeleteSendersThread(QThread):
    open_load_screen = pyqtSignal()
    close_load_screen = pyqtSignal()

    def __init__(self, senders, user):
        super().__init__()
        self.senders = senders
        self.user = user

    def run(self):
        self.open_load_screen.emit()
        self.user.delete_senders(self.senders)
        self.close_load_screen.emit()


class TrashSendersThread(QThread):
    open_load_screen = pyqtSignal()
    close_load_screen = pyqtSignal()

    def __init__(self, senders, user):
        super().__init__()
        self.senders = senders
        self.user = user

    def run(self):
        self.open_load_screen.emit()
        self.user.trash_senders(self.senders)
        self.close_load_screen.emit()


class DeleteMessagesThread(QThread):
    open_load_screen = pyqtSignal()
    close_load_screen = pyqtSignal()

    def __init__(self, ids, sender, user):
        super().__init__()
        self.ids = ids
        self.sender = sender
        self.user = user

    def run(self):
        self.open_load_screen.emit()
        self.user.delete_messages(self.ids, self.sender)
        self.close_load_screen.emit()


class TrashMessagesThread(QThread):
    open_load_screen = pyqtSignal()
    close_load_screen = pyqtSignal()

    def __init__(self, ids, sender, user):
        super().__init__()
        self.ids = ids
        self.sender = sender
        self.user = user

    def run(self):
        self.open_load_screen.emit()
        self.user.trash_messages(self.ids, self.sender)
        self.close_load_screen.emit()

