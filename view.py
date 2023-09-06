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
from threads import *
from ui_manager import *


class MainUi(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.users = UsersCache()
        self.data = UiData(self.ui)
        self.painter = UiDataDisplay(self.ui)
        self.window_popups = WindowsAndPopups(self.ui)
        self.states = States(self.ui)
        self.ui.accountsList.installEventFilter(self)
        self.setup_accounts_list()
        self.connect_signals()

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and (source is self.ui.accountsList or source is self.ui.sendersList):
            menu = QMenu()
            menu.addAction("Delete")
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                self.worker.remove_account(item)
            return True
        return super().eventFilter(source, event)

    def setup_accounts_list(self):
        accounts = db.get_all_accounts()
        for username in accounts:
            self.ui.accountsList.addItem(username)
            self.users.add_user(username)

    def connect_signals(self):
        self.ui.sendersList.clicked.connect(lambda: self.update_header_label())
        self.ui.sendersList.clicked.connect(lambda: self.update_count_labels())
        self.ui.addAcctButton.clicked.connect(lambda: self.add_account())
        self.ui.subjectsList.clicked.connect(lambda: self.states.update_buttons_msgs_screen())
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
        self.ui.set_select_check.clicked.connect(lambda: self.data.set_sender_multiselect_option())
        self.ui.select_msgs_chkbox.clicked.connect(lambda: self.data.set_message_multiselect_option())

    def update_count_labels(self):
        user = self.users.records[self.data.get_current_account()]
        num_senders = user.get_total_num_senders()
        num_messages = user.get_total_num_messages()
        self.ui.total_senders_label.setText(f"Senders: {num_senders}")
        self.ui.total_messages_label.setText(f"Messages: {num_messages}")

    def update_header_label(self):
        if not self.ui.sendersList.currentItem():
            self.ui.action_label.setText("")
        else:
            sender = self.ui.sendersList.currentItem().text()
            user = self.users.records[self.data.get_current_account()]
            num_messages = user.get_num_messages_from(sender)
            grammar = "Messages." if num_messages > 1 else "Message."
            text = f"{sender} | {num_messages} {grammar}"
            self.ui.action_label.setText(text)

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

    def get_new_username(self):
        username = self.ui.info_request_ui.gmail_username.text()
        if username == "":
            self.window_popups.emptyFieldPopup()
            return False
        self.ui.info_request_window.close()
        self.fetch_messages(username)
        return username

    def fetch_messages(self, newUser):
        self.states.loading_state()
        self.modify_accounts_list(newUser)
        self.thread2 = ProgressThread(self.ui, newUser)
        self.thread2.update.connect(self.update_progress_bar)
        self.thread2.finished.connect(lambda: self.users.add_user(newUser))
        self.thread2.finished.connect(lambda: self.users.records[newUser].update_inbox())
        self.thread2.finished.connect(lambda: self.states.default_state())
        self.ui.cancelButton.clicked.connect(lambda: self.terminate_fetch())
        self.thread2.start()

    def terminate_fetch(self):
        self.thread2.cancel.emit()
        self.states.default_state()

    def add_account(self):
        self.ui.info_request_window = QtWidgets.QMainWindow()
        self.ui.info_request_ui = Ui_InfoRequestWindow()
        self.ui.info_request_ui.setupUi(self.ui.info_request_window)
        self.ui.info_request_ui.submit_button.clicked.connect(lambda: self.get_new_username())
        self.ui.info_request_window.setWindowTitle("New Account")
        self.ui.info_request_window.show()

    def process_sender_sort(self):
        index = self.data.get_sender_sort_option()
        if index == 0:
            self.display_senders()
        elif index == 1:
            self.display_senders(rev=True)
        elif index == 2:
            self.display_senders(sort=True)

    def process_msg_sort(self):
        index = self.data.get_msg_sort_option()
        if index == 0:
            self.display_messages()
        elif index == 1:
            self.display_messages(rev=True)
        elif index == 2:
            self.display_messages(sort=True)

    def display_senders(self, rev=False, sort=False):
        username = self.data.get_current_account()
        user = self.users.records[username]
        senders = user.get_all_senders(sort=sort, rev=rev)
        self.painter.populate_senders(senders)

    def display_messages(self, rev=False, sort=False):
        username = self.data.get_current_account()
        sender = self.data.get_selected_senders()[-1]
        user = self.users.records[username]
        messages = user.get_messages_from(sender, sort=sort, rev=rev)
        self.painter.populate_messages(messages)

    def delete_senders(self):
        username = self.data.get_current_account()
        selected_senders = self.data.get_selected_senders()
        user = self.users.records[username]
        self.delete_senders_thread = DeleteSendersThread(selected_senders, user)
        self.delete_senders_thread.open_load_screen.connect(self.window_popups.open_waiting_screen())
        self.delete_senders_thread.close_load_screen.connect(lambda: self.ui.loading_window.close())
        self.delete_senders_thread.start()
        self.painter.delete_senders()
        self.update_count_labels()
        self.update_header_label()

    def trash_senders(self):
        username = self.data.get_current_account()
        senders = self.data.get_selected_senders()
        user = self.users.records[username]
        self.trash_senders_thread = TrashSendersThread(senders, user)
        self.trash_senders_thread.open_load_screen.connect(lambda: self.window_popups.open_waiting_screen())
        self.trash_senders_thread.close_load_screen.connect(lambda: self.ui.loading_window.close())
        self.trash_senders_thread.start()
        self.painter.delete_senders()
        self.update_count_labels()
        self.update_header_label()

    def delete_messages(self):
        username = self.data.get_current_account()
        msg_ids = self.data.get_selected_msg_ids()
        user = self.users.records[username]
        sender = self.data.get_selected_senders()[-1]
        self.delete_messages_thread = DeleteMessagesThread(msg_ids, sender, user)
        self.delete_messages_thread.open_load_screen.connect(self.window_popups.open_waiting_screen())
        self.delete_messages_thread.close_load_screen.connect(lambda: self.ui.loading_window.close())
        self.delete_messages_thread.start()
        self.data_display.delete_messages()
        self.update_count_labels()
        self.update_header_label()

    def trash_messages(self):
        username = self.data.get_current_account()
        msg_ids = self.data.get_selected_msg_ids()
        user = self.users.records[username]
        sender = self.ui.sendersList.currentItem().text()
        self.trash_messages_thread = TrashMessagesThread(msg_ids, sender, user)
        self.trash_messages_thread.open_load_screen.connect(lambda: self.window_popups.open_waiting_screen())
        self.trash_messages_thread.close_load_screen.connect(lambda: self.ui.loading_window.close())
        self.trash_messages_thread.start()
        self.painter.delete_messages()
        self.update_count_labels()
        self.update_header_label()

    def refresh_inbox(self):
        self.states.loading_state()
        user = self.data.get_current_account()
        self.refresh_thread = ProgressThread(self.ui, user)
        self.refresh_thread.update.connect(self.update_progress_bar)
        self.refresh_thread.finished.connect(lambda: self.users.records[user].update_inbox())
        self.refresh_thread.finished.connect(lambda: self.states.default_state())
        self.ui.cancelButton.clicked.connect(lambda: self.terminate_refresh())
        self.refresh_thread.start()
        self.update_count_labels()
        self.update_header_label()

    def terminate_refresh(self):
        self.refresh_thread.cancel.emit()
        self.states.default_state()

    def unsubscribe(self):
        username = self.data.get_current_account()
        sender = self.data.get_selected_senders()[-1]
        link = GmailOp(username).get_unsubscribe_link(sender)
        if not link:
            self.window_popups.no_link_popup()
            return
        webbrowser.open(link)

    def open_message_in_browser(self):
        username = self.data.get_current_account()
        message = self.ui.subjectsList.currentItem().text()
        sender = self.ui.sendersList.currentItem().text()
        file_made = GmailOp(username).get_html_message(sender, message=message)
        print(file_made)
        if not file_made:
            self.window_popups.no_html_data_popup()
            return
        url = 'file:///' + os.getcwd() + '/sites/message.html'
        webbrowser.open(url, new=2)
