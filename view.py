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
from users import Users
from threads import *


class NoSelectionView:
    def __init__(self, ui):
        self.ui = ui

    def update_view(self):
        pass


class SingleSelectionView:
    pass


class MultiSelectionView:
    pass


class Setup(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.users = Users()
        self.connect_signals()

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and (source is self.ui.accountsList or source is self.ui.sendersList):
            menu = QMenu()
            menu.addAction("Delete")
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                self.remove_account(item)
            return True
        return super().eventFilter(source, event)

    def connect_signals(self):
        self.ui.addAcctButton.clicked.connect(lambda: self.open_info_request())
        self.setup_accounts_list()
        self.ui.accountsList.installEventFilter(self)
        self.ui.accountsList.clicked.connect(lambda: self.process_sender_sort())
        self.ui.sendersList.itemDoubleClicked.connect(lambda: self.process_msg_sort(self.ui.subjectsList))
        self.ui.sendersList.clicked.connect(lambda: self.set_display_label())
        self.ui.sendersList.clicked.connect(lambda: self.update_buttons_sender_screen())
        self.ui.sendersList.clicked.connect(lambda: self.process_msg_sort(self.ui.subjectsList_2))
        self.ui.subjectsList.itemDoubleClicked.connect(lambda: self.open_message_in_browser())
        self.ui.subjectsList.clicked.connect(lambda: self.update_buttons_msgs_screen())
        self.ui.cancelButton.clicked.connect(lambda: self.thread2.cancel.emit())
        self.ui.backButton.clicked.connect(lambda: self.process_sender_sort())
        self.ui.view_msgs_button.clicked.connect(lambda: self.process_msg_sort(self.ui.subjectsList))
        self.ui.delete_all_button.clicked.connect(lambda: self.delete_senders())
        self.ui.trash_all_button.clicked.connect(lambda: self.trash_senders())
        self.ui.refresh_button.clicked.connect(lambda: self.fetch_messages())
        self.ui.delete_message_button.clicked.connect(lambda: self.delete_messages())
        self.ui.trash_message_button.clicked.connect(lambda: self.trash_messages())
        self.ui.unsubscribe_button.clicked.connect(lambda: self.unsubscribe())
        self.ui.sort_option.currentIndexChanged.connect(lambda: self.process_sender_sort())
        self.ui.msg_sort_option.currentIndexChanged.connect(lambda: self.process_msg_sort(self.ui.subjectsList))
        self.ui.set_select_check.stateChanged.connect(lambda: self.update_buttons_sender_screen())
        self.ui.select_msgs_chkbox.stateChanged.connect(lambda: self.update_buttons_msgs_screen())
        self.ui.open_browser_bttn.clicked.connect(lambda: self.open_message_in_browser())

    def update_buttons_sender_screen(self):
        selected_items = self.ui.sendersList.selectedItems()
        if not selected_items:
            self.ui.delete_all_button.setEnabled(False)
            self.ui.trash_all_button.setEnabled(False)
            self.ui.view_msgs_button.setEnabled(False)
            self.ui.unsubscribe_button.setEnabled(False)
        elif len(selected_items) > 1:
            self.ui.unsubscribe_button.setEnabled(False)
            self.ui.view_msgs_button.setEnabled(False)
            self.ui.delete_all_button.setEnabled(True)
            self.ui.trash_all_button.setEnabled(True)
        else:
            self.ui.delete_all_button.setEnabled(True)
            self.ui.trash_all_button.setEnabled(True)
            self.ui.view_msgs_button.setEnabled(True)
            self.ui.unsubscribe_button.setEnabled(True)
        self.set_sender_multiselect_option()

    def update_buttons_msgs_screen(self):
        selected_items = self.ui.subjectsList.selectedItems()
        for msg in selected_items:
            print(msg.get_subject(), msg.get_id())
        if not selected_items:
            self.ui.delete_message_button.setEnabled(False)
            self.ui.trash_message_button.setEnabled(False)
            self.ui.open_browser_bttn.setEnabled(False)
        else:
            self.ui.delete_message_button.setEnabled(True)
            self.ui.trash_message_button.setEnabled(True)
            self.ui.open_browser_bttn.setEnabled(True)
        if len(selected_items) > 1:
            self.ui.open_browser_bttn.setEnabled(False)
        self.set_message_multiselect_option()

    def set_sender_multiselect_option(self):
        selectSendersChecked = self.ui.set_select_check.isChecked()
        if selectSendersChecked:
            self.ui.sendersList.setSelectionMode(QAbstractItemView.MultiSelection)
        else:
            self.ui.sendersList.setSelectionMode(QAbstractItemView.SingleSelection)

    def set_message_multiselect_option(self):
        selectMsgsChecked = self.ui.select_msgs_chkbox.isChecked()
        if selectMsgsChecked:
            self.ui.subjectsList.setSelectionMode(QAbstractItemView.MultiSelection)
        else:
            self.ui.subjectsList.setSelectionMode(QAbstractItemView.SingleSelection)

    def process_sender_sort(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        index = self.ui.sort_option.currentIndex()
        if index == 0:
            self.display_senders()
        elif index == 1:
            self.display_senders(rev=True)
        elif index == 2:
            self.display_senders(sort=True)
        self.update_buttons_sender_screen()

    def process_msg_sort(self, listWidget):
        self.ui.stackedWidget.setCurrentIndex(3)
        index = self.ui.msg_sort_option.currentIndex()
        if index == 0:
            self.display_messages(listWidget)
        elif index == 1:
            self.display_messages(listWidget, rev=True)
        elif index == 2:
            self.display_messages(listWidget, sort=True)
        self.update_buttons_msgs_screen()

    def modify_accounts_list(self, username):
        if username == "":
            return None
        if not self.ui.accountsList.findItems(username, QtCore.Qt.MatchExactly):
            self.ui.accountsList.addItem(username)

    def remove_senders_from_list(self):
        senders = self.ui.sendersList.selectedItems()
        for sender in senders:
            row = self.ui.sendersList.row(sender)
            self.ui.sendersList.takeItem(row)
        self.set_display_label()
        self.set_labels()

    def remove_account(self, item):
        row = self.ui.accountsList.row(item)
        self.ui.accountsList.takeItem(row)
        db.delete_account(item.text())
        self.ui.sendersList.clear()
        self.ui.stackedWidget.setCurrentIndex(2)

    def remove_messages(self):
        messages = self.ui.subjectsList.selectedItems()
        for msg in messages:
            row = self.ui.subjectsList.row(msg)
            self.ui.subjectsList.takeItem(row)
        if self.ui.subjectsList.count() == 0:
            self.ui.stackedWidget.setCurrentIndex(0)
            self.update_buttons_sender_screen()
            self.remove_senders_from_list()
        self.set_labels()
        self.update_buttons_msgs_screen()

    def setup_accounts_list(self):
        accounts = db.get_all_accounts()
        for username in accounts:
            self.ui.accountsList.addItem(username)
            self.users.add_user(username)

    def add_sender_to_list(self, sender):
        self.ui.sendersList.addItem(sender)

    def open_info_request(self):
        self.ui.info_request_window = QtWidgets.QMainWindow()
        self.ui.info_request_ui = Ui_InfoRequestWindow()
        self.ui.info_request_ui.setupUi(self.ui.info_request_window)
        self.ui.info_request_window.setWindowTitle("New Account")
        self.ui.info_request_ui.submit_button.clicked.connect(lambda: self.get_new_username())
        self.ui.info_request_window.show()

    def get_new_username(self):
        username = self.ui.info_request_ui.gmail_username.text()
        if username == "":
            self.emptyFieldPopup()
            return False
        self.ui.info_request_window.close()
        self.fetch_messages(newUser=username)
        return username

    def fetch_messages(self, newUser=""):
        self.ui.accountsList.setEnabled(False)
        self.ui.addAcctButton.setEnabled(False)
        self.ui.total_senders_label.setText("")
        self.ui.total_messages_label.setText("")
        self.ui.action_label.setText("")
        if not newUser:
            newUser = self.ui.accountsList.currentItem().text()
        self.modify_accounts_list(newUser)
        self.ui.sendersList.clear()
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.progressBar.setValue(0)
        self.thread2 = ProgressThread(self.ui, newUser)
        self.thread2.update.connect(self.update_progress_bar)
        self.thread2.finished.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.thread2.finished.connect(lambda: self.users.add_user(newUser))
        self.thread2.finished.connect(lambda: self.users.records[newUser].update_inbox())
        self.thread2.finished.connect(lambda: self.ui.accountsList.setEnabled(True))
        self.thread2.finished.connect(lambda: self.ui.addAcctButton.setEnabled(True))
        self.thread2.cancel.connect(lambda: self.terminate_fetch())
        self.thread2.start()

    def terminate_fetch(self):
        self.ui.accountsList.setEnabled(True)
        self.ui.addAcctButton.setEnabled(True)
        self.thread2.terminate()
        self.ui.progressBar.setValue(0)
        self.ui.count_label.setText("Connecting...")
        self.ui.stackedWidget.setCurrentIndex(2)
        self.set_labels()

    def display_messages(self, listWidget, rev=False, sort=False):
        self.ui.total_senders_label.setText("")
        self.ui.total_messages_label.setText("")
        username = self.ui.accountsList.currentItem().text()
        sender = self.ui.sendersList.currentItem().text()
        user = self.users.records[username]
        self.ui.subjectsList.clear()
        self.set_display_label()
        messages = user.get_messages_from(sender, sort=sort, rev=rev)
        for msg in messages:
            listWidget.addItem(msg)


    def set_ui_disabled(self):
        self.ui.stackedWidget.setEnabled(False)
        self.ui.accountsList.setEnabled(False)
        self.ui.addAcctButton.setEnabled(False)

    def set_ui_enabled(self):
        self.ui.stackedWidget.setEnabled(True)
        self.ui.accountsList.setEnabled(True)
        self.ui.addAcctButton.setEnabled(True)
        self.set_display_label()

    def delete_senders(self):
        self.set_ui_disabled()
        username = self.ui.accountsList.currentItem().text()
        selected_senders = self.ui.sendersList.selectedItems()
        user = self.users.records[username]
        all_senders = []
        for sender in selected_senders:
            all_senders.append(sender.text())
        self.delete_senders_thread = DeleteSendersThread(all_senders, user)
        self.delete_senders_thread.open_load_screen.connect(self.open_loading_screen)
        self.delete_senders_thread.close_load_screen.connect(lambda: self.ui.loading_window.close())
        self.delete_senders_thread.close_load_screen.connect(lambda: self.set_ui_enabled())
        self.delete_senders_thread.close_load_screen.connect(lambda: self.set_labels())
        self.delete_senders_thread.start()
        self.remove_senders_from_list()
        self.update_buttons_sender_screen()

    def trash_senders(self):
        self.set_ui_disabled()
        username = self.ui.accountsList.currentItem().text()
        senders = self.ui.sendersList.selectedItems()
        user = self.users.records[username]
        all_senders = []
        for sender in senders:
            all_senders.append(sender.text())
        self.trash_senders_thread = TrashSendersThread(all_senders, user)
        self.trash_senders_thread.open_load_screen.connect(self.open_loading_screen)
        self.trash_senders_thread.close_load_screen.connect(lambda: self.ui.loading_window.close())
        self.trash_senders_thread.close_load_screen.connect(lambda: self.set_ui_enabled())
        self.trash_senders_thread.close_load_screen.connect(lambda: self.set_labels())
        self.trash_senders_thread.start()
        self.remove_senders_from_list()
        self.update_buttons_sender_screen()

    def delete_messages(self):
        self.set_ui_disabled()
        username = self.ui.accountsList.currentItem().text()
        to_delete = self.ui.subjectsList.selectedItems()
        user = self.users.records[username]
        sender = self.ui.sendersList.currentItem().text()
        messages = []
        for msg in to_delete:
            messages.append(msg.get_id())
        self.delete_messages_thread = DeleteMessagesThread(messages, sender, user)
        self.delete_messages_thread.open_load_screen.connect(self.open_loading_screen)
        self.delete_messages_thread.close_load_screen.connect(lambda: self.ui.loading_window.close())
        self.delete_messages_thread.close_load_screen.connect(lambda: self.set_ui_enabled())
        self.delete_messages_thread.close_load_screen.connect(lambda: self.set_labels())
        self.delete_messages_thread.start()
        self.remove_messages()
        self.update_buttons_msgs_screen()

    def trash_messages(self):
        self.set_ui_disabled()
        username = self.ui.accountsList.currentItem().text()
        to_delete = [msg.msg_id for msg in self.ui.subjectsList.selectedItems()]
        user = self.users.records[username]
        sender = self.ui.sendersList.currentItem().text()

        self.trash_messages_thread = TrashMessagesThread(to_delete, sender, user)
        self.trash_messages_thread.open_load_screen.connect(self.open_loading_screen)
        self.trash_messages_thread.close_load_screen.connect(lambda: self.ui.loading_window.close())
        self.trash_messages_thread.close_load_screen.connect(lambda: self.set_ui_enabled())
        self.trash_messages_thread.close_load_screen.connect(lambda: self.set_labels())
        self.trash_messages_thread.start()
        self.remove_messages()
        self.update_buttons_msgs_screen()

    def open_loading_screen(self):
        self.ui.loading_window = QtWidgets.QMainWindow()
        self.ui.loading_window.setParent(self.ui.centralwidget)
        self.ui.loading_window.setWindowFlag(Qt.FramelessWindowHint)
        self.ui.loading_window.setFixedSize(200, 200)
        self.ui.loading_ui = Ui_LoadWindow()
        self.ui.loading_ui.setupUi(self.ui.loading_window)
        movie = QMovie('icons/ezgif.com-resize.gif')
        self.ui.loading_ui.load_anim.setMovie(movie)
        movie.start()
        print(self.ui.centralwidget.pos())
        self.ui.loading_window.show()
        self.ui.loading_window.move(self.ui.loading_window.parent().geometry().center())

    def unsubscribe(self):
        username = self.ui.accountsList.currentItem().text()
        sender = self.ui.sendersList.currentItem().text()
        link = GmailOp(username).get_unsubscribe_link(sender)
        if not link:
            self.no_link_popup()
            return
        webbrowser.open(link)

    def open_message_in_browser(self):
        username = self.ui.accountsList.currentItem().text()
        message = self.ui.subjectsList.currentItem().text()
        sender = self.ui.sendersList.currentItem().text()
        file_made = GmailOp(username).get_html_message(sender, message=message)
        print(file_made)
        if not file_made:
            self.no_html_data_popup()
            return
        url = 'file:///'+os.getcwd()+ '/sites/message.html'
        webbrowser.open(url, new=2)

    def set_labels(self):
        username = self.ui.accountsList.currentItem().text()
        user = self.users.records[username]
        total_messages = user.get_total_num_messages()
        total_senders = user.get_total_num_senders()
        self.ui.total_senders_label.setText(f"Senders: {total_senders}")
        self.ui.total_messages_label.setText(f"Messages: {total_messages}")

    def set_display_label(self):
        if not self.ui.sendersList.currentItem():
            self.ui.action_label.setText("")
        else:
            current_sender = self.ui.sendersList.currentItem().text()
            username = self.ui.accountsList.currentItem().text()
            user = self.users.records[username]
            num_messages = user.get_num_messages_from(current_sender)
            grammar = "Messages." if num_messages > 1 else "Message."
            text = f"{current_sender} | {num_messages} {grammar}"
            self.ui.action_label.setText(text)

    def display_senders(self, rev=False, sort=False):
        username = self.ui.accountsList.currentItem().text()
        self.set_sender_multiselect_option()
        self.ui.sendersList.clear()
        user = self.users.records[username]
        senders = user.get_all_senders(sort=sort, rev=rev)
        self.ui.sendersList.addItems(senders)
        self.set_labels()
        self.set_display_label()

    def update_progress_bar(self, total_emails, count):
        self.ui.count_label.setText(
            "Processing " + str(self.ui.progressBar.value()) + " of " + str(total_emails) + " emails")
        self.ui.progressBar.setValue(count)

    def emptyFieldPopup(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Empty Fields")
        msg.setText("Fields must not be empty")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()

    def no_html_data_popup(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Failed to Open in Browser")
        msg.setText("Could not parse message")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()

    def no_link_popup(self):
        sender = self.ui.sendersList.currentItem().text()
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("No Unsubscribe Link Found")
        msg.setIcon(QMessageBox.Question)
        msg.setText(f"No unsubscribe link was found.\nWould you like to open a message from \"{sender}\" in your "
                    f"browser?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.process_popup)
        msg.exec_()

    def process_popup(self, button):
        username = self.ui.accountsList.currentItem().text()
        sender = self.ui.sendersList.currentItem().text()
        if button.text() == "&Yes":
            GmailOp(username).get_html_message(sender)
            url = 'file:///' + os.getcwd() + '/sites/message.html'
            webbrowser.open(url)
