# THIS FILE UPDATES UI inboxWindow.py
from infoRequestWindow import Ui_InfoRequestWindow
from load_window import Ui_LoadWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import QMovie
import webbrowser
import os
from users import UsersCache
from threads import *
from ui_manager import *


class UiData:
    def __init__(self, ui):
        self.ui = ui
        self.users = UsersCache()
        self.states = States(self.ui)
        self.data_display = UiDataDisplay(self.ui)
        self.window_popups = WindowsAndPopups(self.ui)
        self.connect_signals()

    def connect_signals(self):
        self.ui.sendersList.clicked.connect(lambda: self.update_header_label())
        self.ui.sendersList.clicked.connect(lambda: self.update_count_labels())


    def get_sender_sort_option(self):
        return self.ui.sort_option.currentIndex()

    def get_msg_sort_option(self):
        return self.ui.msg_sort_option.currentIndex()

    def sender_multiselect_checked(self):
        return self.ui.set_select_check.isChecked()

    def msg_multiselect_checked(self):
        return self.ui.select_msgs_chkbox.isChecked()

    def get_current_account(self):
        return self.ui.accountsList.currentItem().text()

    def get_selected_senders(self):
        senders = self.ui.sendersList.selectedItems()
        senders = [x.text() for x in senders]
        return senders

    def get_selected_messages(self):
        messages = self.ui.subjectsList.selectedItems()
        messages = [msg.text() for msg in messages]
        return messages

    def get_selected_msg_ids(self):
        messages = self.ui.subjectsList.selectedItems()
        ids = [x.get_id for x in messages]
        return ids

    def update_count_labels(self):
        user = self.users.records[self.get_current_account()]
        num_senders = user.get_total_num_senders()
        num_messages = user.get_total_num_messages()
        self.ui.total_senders_label.setText(f"Senders: {num_senders}")
        self.ui.total_messages_label.setText(f"Messages: {num_messages}")

    def update_header_label(self):
        if not self.ui.sendersList.currentItem():
            self.ui.action_label.setText("")
        else:
            sender = self.ui.sendersList.currentItem().text()
            user = self.users.records[self.get_current_account()]
            num_messages = user.get_num_messages_from(sender)
            grammar = "Messages." if num_messages > 1 else "Message."
            text = f"{sender} | {num_messages} {grammar}"
            self.ui.action_label.setText(text)

    def update_progress_bar(self, total_emails, count):
        self.ui.count_label.setText(
            "Processing " + str(self.ui.progressBar.value()) + " of " + str(total_emails) + " emails")
        self.ui.progressBar.setValue(count)


class AccountSetup(UiData):
    def __init__(self, ui, users):
        super().__init__(ui)
        self.users = users
        self.connect_signals()
        self.setup_accounts_list()

    def connect_signals(self):
        self.ui.addAcctButton.clicked.connect(lambda: self.add_account())

    def modify_accounts_list(self, username):
        if username == "":
            return None
        if not self.ui.accountsList.findItems(username, QtCore.Qt.MatchExactly):
            self.ui.accountsList.addItem(username)

    def remove_account(self, item):
        row = self.ui.accountsList.row(item)
        self.ui.accountsList.takeItem(row)
        db.delete_account(item.text())
        self.ui.sendersList.clear()
        self.ui.stackedWidget.setCurrentIndex(2)

    def setup_accounts_list(self):
        accounts = db.get_all_accounts()
        for username in accounts:
            self.ui.accountsList.addItem(username)
            self.users.add_user(username)

    def get_new_username(self):
        username = self.ui.info_request_ui.gmail_username.text()
        if username == "":
            self.window_popups.emptyFieldPopup()
            return False
        self.ui.info_request_window.close()
        self.fetch_messages(username)
        return username

    def fetch_messages(self, newUser):
        self.modify_accounts_list(newUser)
        self.thread2 = ProgressThread(self.ui, newUser)
        self.thread2.update.connect(self.update_progress_bar)
        self.thread2.finished.connect(lambda: self.users.add_user(newUser))
        self.thread2.finished.connect(lambda: self.users.records[newUser].update_inbox())
        self.thread2.finished.connect(lambda: self.states.default_state())
        self.ui.cancelButton.clicked.connect(lambda: self.thread2.cancel.emit())
        self.thread2.start()

    def add_account(self):
        self.ui.info_request_window = QtWidgets.QMainWindow()
        self.ui.info_request_ui = Ui_InfoRequestWindow()
        self.ui.info_request_ui.setupUi(self.ui.info_request_window)
        self.ui.info_request_ui.submit_button.clicked.connect(lambda: self.get_new_username())
        self.ui.info_request_window.setWindowTitle("New Account")
        self.ui.info_request_window.show()


class Worker(UiData):
    def __init__(self, ui, users):
        super().__init__(ui)
        self.users = users
        self.connect_signals()

    def connect_signals(self):
        self.ui.accountsList.clicked.connect(lambda: self.process_sender_sort())
        self.ui.sendersList.clicked.connect(lambda: self.process_msg_sort())
        self.ui.subjectsList.itemDoubleClicked.connect(lambda: self.open_message_in_browser())
        self.ui.delete_all_button.clicked.connect(lambda: self.delete_senders())
        self.ui.trash_all_button.clicked.connect(lambda: self.trash_senders())
        self.ui.refresh_button.clicked.connect(lambda: self.refresh_inbox())
        self.ui.delete_message_button.clicked.connect(lambda: self.delete_messages())
        self.ui.trash_message_button.clicked.connect(lambda: self.trash_messages())
        self.ui.unsubscribe_button.clicked.connect(lambda: self.unsubscribe())
        self.ui.sort_option.currentIndexChanged.connect(lambda: self.process_sender_sort())
        self.ui.msg_sort_option.currentIndexChanged.connect(lambda: self.process_msg_sort())
        self.ui.open_browser_bttn.clicked.connect(lambda: self.open_message_in_browser())

    def process_sender_sort(self):
        index = self.get_sender_sort_option()
        if index == 0:
            self.display_senders()
        elif index == 1:
            self.display_senders(rev=True)
        elif index == 2:
            self.display_senders(sort=True)

    def process_msg_sort(self):
        index = self.get_msg_sort_option()
        if index == 0:
            self.display_messages()
        elif index == 1:
            self.display_messages(rev=True)
        elif index == 2:
            self.display_messages(sort=True)

    def display_senders(self, rev=False, sort=False):
        username = self.get_current_account()
        user = self.users.records[username]
        senders = user.get_all_senders(sort=sort, rev=rev)
        self.data_display.populate_senders(senders)

    def display_messages(self, rev=False, sort=False):
        username = self.get_current_account()
        sender = self.get_selected_senders()[-1]
        user = self.users.records[username]
        messages = user.get_messages_from(sender, sort=sort, rev=rev)
        self.data_display.populate_messages(messages)

    def delete_senders(self):
        username = self.get_current_account()
        selected_senders = self.get_selected_senders()
        user = self.users.records[username]
        self.delete_senders_thread = DeleteSendersThread(selected_senders, user)
        self.delete_senders_thread.open_load_screen.connect(self.window_popups.open_waiting_screen())
        self.delete_senders_thread.close_load_screen.connect(lambda: self.ui.loading_window.close())
        self.delete_senders_thread.start()
        self.data_display.delete_senders()

    def trash_senders(self):
        username = self.get_current_account()
        senders = self.get_selected_senders()
        user = self.users.records[username]
        self.trash_senders_thread = TrashSendersThread(senders, user)
        self.trash_senders_thread.open_load_screen.connect(self.window_popups.open_waiting_screen())
        self.trash_senders_thread.close_load_screen.connect(lambda: self.ui.loading_window.close())
        self.trash_senders_thread.start()
        self.data_display.delete_senders()

    def delete_messages(self):
        username = self.get_current_account()
        msg_ids = self.get_selected_msg_ids()
        user = self.users.records[username]
        sender = self.get_selected_senders()[-1]
        self.delete_messages_thread = DeleteMessagesThread(msg_ids, sender, user)
        self.delete_messages_thread.open_load_screen.connect(self.window_popups.open_waiting_screen())
        self.delete_messages_thread.close_load_screen.connect(lambda: self.ui.loading_window.close())
        self.delete_messages_thread.start()
        self.data_display.delete_messages()

    def trash_messages(self):
        username = self.get_current_account()
        msg_ids = self.get_selected_msg_ids()
        user = self.users.records[username]
        sender = self.ui.sendersList.currentItem().text()
        self.trash_messages_thread = TrashMessagesThread(msg_ids, sender, user)
        self.trash_messages_thread.open_load_screen.connect(self.window_popups.open_waiting_screen())
        self.trash_messages_thread.close_load_screen.connect(lambda: self.ui.loading_window.close())
        self.trash_messages_thread.start()
        self.data_display.delete_messages()

    def refresh_inbox(self):
        self.states.loading_state()
        user = self.get_current_account()
        self.refresh_thread = ProgressThread(self.ui, user)
        self.refresh_thread.update.connect(UiData(self.ui).update_progress_bar)
        self.ui.cancelButton.clicked.connect(lambda: self.refresh_thread.cancel.emit())
        self.refresh_thread.start()

    def unsubscribe(self):
        username = self.get_current_account()
        sender = self.get_selected_senders()[-1]
        link = GmailOp(username).get_unsubscribe_link(sender)
        if not link:
            self.window_popups.no_link_popup()
            return
        webbrowser.open(link)

    def open_message_in_browser(self):
        username = self.get_current_account()
        message = self.ui.subjectsList.currentItem().text()
        sender = self.ui.sendersList.currentItem().text()
        file_made = GmailOp(username).get_html_message(sender, message=message)
        print(file_made)
        if not file_made:
            self.window_popups.no_html_data_popup()
            return
        url = 'file:///' + os.getcwd() + '/sites/message.html'
        webbrowser.open(url, new=2)

