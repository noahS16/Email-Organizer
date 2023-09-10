import os
import webbrowser
from PyQt5.QtGui import QMovie
from PyQt5 import QtWidgets
from emails import GmailOp
from infoRequestWindow import Ui_InfoRequestWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from load_window import Ui_LoadWindow


class UiData:
    def __init__(self, ui):
        self.ui = ui

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
        ids = [x.get_id() for x in messages]
        return ids

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

    def update_progress_bar(self, total_emails, count):
        self.ui.count_label.setText(
            "Processing " + str(self.ui.progressBar.value()) + " of " + str(total_emails) + " emails")
        self.ui.progressBar.setValue(count)


class UiDataDisplay:
    def __init__(self, ui):
        self.ui = ui
        self.states = States(self.ui)
        self.sender_list = self.ui.sendersList
        self.message_list = self.ui.subjectsList
        self.accounts_list = self.ui.accountsList

    def populate_senders(self, senders: list):
        self.states.default_state()
        self.sender_list.clear()
        self.message_list.clear()
        self.sender_list.addItems(senders)

    def populate_messages(self, messages: list):
        self.message_list.clear()
        for msg in messages:
            self.message_list.addItem(msg)
        self.states.update_sender_screen()
        self.states.update_buttons_msgs_screen()

    def delete_senders(self):
        senders = self.sender_list.selectedItems()
        for sender in senders:
            row = self.sender_list.row(sender)
            self.sender_list.takeItem(row)

    def delete_messages(self):
        self.states.update_sender_screen()
        messages = self.message_list.selectedItems()
        for msg in messages:
            row = self.message_list.row(msg)
            self.message_list.takeItem(row)
        if self.message_list.count() == 0:
            self.delete_senders()

    def add_accounts(self, accounts: list):
        self.accounts_list.addItems(accounts)

    def delete_account(self):
        accounts = self.accounts_list.selectedItems()
        row = self.accounts_list.row(accounts[0])
        self.accounts_list.takeItem(row)


class States:
    def __init__(self, ui):
        self.ui = ui

    def default_state(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.groupBox.setEnabled(True)
        self.ui.accountsList.setEnabled(True)
        self.ui.addAcctButton.setEnabled(True)
        self.update_sender_screen()
        self.update_buttons_msgs_screen()

    def loading_state(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.progressBar.setValue(0)
        self.ui.accountsList.setEnabled(False)
        self.ui.addAcctButton.setEnabled(False)
        self.ui.total_senders_label.setText("")
        self.ui.total_messages_label.setText("")
        self.ui.action_label.setText("")

    def update_sender_screen(self):
        selected_items = self.ui.sendersList.selectedItems()
        if not selected_items:
            self.ui.delete_all_button.setEnabled(False)
            self.ui.trash_all_button.setEnabled(False)
            self.ui.unsubscribe_button.setEnabled(False)
            self.ui.subjectsList.clear()
        elif len(selected_items) > 1:
            self.ui.unsubscribe_button.setEnabled(False)
            self.ui.delete_all_button.setEnabled(True)
            self.ui.trash_all_button.setEnabled(True)
        else:
            self.ui.delete_all_button.setEnabled(True)
            self.ui.trash_all_button.setEnabled(True)
            self.ui.unsubscribe_button.setEnabled(True)

    def update_buttons_msgs_screen(self):
        selected_items = self.ui.subjectsList.selectedItems()
        print(selected_items)
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

    def set_ui_disabled(self):
        self.ui.groupBox.setEnabled(False)

    def set_ui_enabled(self):
        self.ui.groupBox.setEnabled(True)

    def update_count_labels(self, num_senders, num_messages):
        self.ui.total_senders_label.setText(f"Senders: {num_senders}")
        self.ui.total_messages_label.setText(f"Messages: {num_messages}")

    def update_header_label(self, num_messages_from):
        if len(self.ui.sendersList.selectedItems()) == 0:
            self.ui.action_label.setText("")
        else:
            sender = self.ui.sendersList.currentItem().text()
            grammar = "Messages." if num_messages_from > 1 else "Message."
            text = f"{sender} | {num_messages_from} {grammar}"
            self.ui.action_label.setText(text)



class WindowsAndPopups:
    def __init__(self, ui):
        self.ui = ui

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
        msg.buttonClicked.connect(self.process_nolink_popup)
        msg.exec_()

    def process_nolink_popup(self, button):
        username = self.ui.accountsList.currentItem().text()
        sender = self.ui.sendersList.currentItem().text()
        if button.text() == "&Yes":
            GmailOp(username).get_html_message(sender)
            url = 'file:///' + os.getcwd() + '/sites/message.html'
            webbrowser.open(url)

    def make_info_request_window(self):
        info_request_window = QtWidgets.QMainWindow()
        info_request_ui = Ui_InfoRequestWindow()
        info_request_ui.setupUi(info_request_window)
        info_request_window.setWindowTitle("New Account")
        return info_request_ui

    def open_waiting_screen(self):
        self.ui.loading_window = QtWidgets.QMainWindow()
        self.ui.loading_window.setParent(self.ui.centralwidget)
        self.ui.loading_window.setWindowFlag(Qt.FramelessWindowHint)
        self.ui.loading_window.setFixedSize(200, 200)
        self.ui.loading_ui = Ui_LoadWindow()
        self.ui.loading_ui.setupUi(self.ui.loading_window)
        movie = QMovie('icons/ezgif.com-resize.gif')
        self.ui.loading_ui.load_anim.setMovie(movie)
        movie.start()
        self.ui.loading_window.show()
        self.ui.loading_window.move(self.ui.loading_window.parent().geometry().center())


