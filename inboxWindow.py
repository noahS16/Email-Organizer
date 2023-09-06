# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/inboxWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 637)
        MainWindow.setMinimumSize(QtCore.QSize(520, 0))
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color: rgb(11, 1, 55);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.groupBox.setFont(font)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 5, 1, 1)
        self.total_messages_label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(15)
        self.total_messages_label.setFont(font)
        self.total_messages_label.setStyleSheet("color: white;")
        self.total_messages_label.setObjectName("total_messages_label")
        self.gridLayout_2.addWidget(self.total_messages_label, 2, 8, 1, 1, QtCore.Qt.AlignRight)
        self.stackedWidget = QtWidgets.QStackedWidget(self.groupBox)
        self.stackedWidget.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.stackedWidget.setFont(font)
        self.stackedWidget.setStyleSheet("QStackedWidget{\n"
"    background-color: rrgb(48, 33, 86);\n"
"    border-top: 1px solid grey;\n"
"}")
        self.stackedWidget.setObjectName("stackedWidget")
        self.all_senders_screen = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.all_senders_screen.setFont(font)
        self.all_senders_screen.setObjectName("all_senders_screen")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.all_senders_screen)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_5 = QtWidgets.QGroupBox(self.all_senders_screen)
        self.groupBox_5.setMaximumSize(QtCore.QSize(16777215, 60))
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.msg_sort_option = QtWidgets.QComboBox(self.groupBox_5)
        self.msg_sort_option.setObjectName("msg_sort_option")
        self.msg_sort_option.addItem("")
        self.msg_sort_option.addItem("")
        self.msg_sort_option.addItem("")
        self.horizontalLayout_2.addWidget(self.msg_sort_option, 0, QtCore.Qt.AlignLeft)
        self.select_msgs_chkbox = QtWidgets.QCheckBox(self.groupBox_5)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(15)
        self.select_msgs_chkbox.setFont(font)
        self.select_msgs_chkbox.setObjectName("select_msgs_chkbox")
        self.horizontalLayout_2.addWidget(self.select_msgs_chkbox)
        self.delete_message_button = QtWidgets.QPushButton(self.groupBox_5)
        self.delete_message_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.delete_message_button.setStyleSheet("QPushButton {\n"
"    width: 30px;\n"
"    height: 25px;\n"
"    color: black;\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"    background-color: rgb(255, 101, 118);\n"
"    border: 2px solid black;\n"
"}\n"
"QPushButton::hover {\n"
"    background-color:  rgb(245, 85, 96);\n"
"    border: 0px;\n"
"}\n"
"QPushButton::pressed {\n"
"    \n"
"}\n"
"QPushButton:disabled{\n"
"    background-color:  rgb(123, 124, 125);\n"
"    border: 2px solid black;\n"
"}")
        self.delete_message_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/../icons/delete_btn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_message_button.setIcon(icon)
        self.delete_message_button.setObjectName("delete_message_button")
        self.horizontalLayout_2.addWidget(self.delete_message_button, 0, QtCore.Qt.AlignLeft)
        self.trash_message_button = QtWidgets.QPushButton(self.groupBox_5)
        self.trash_message_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.trash_message_button.setStyleSheet("QPushButton {\n"
"    width: 30px;\n"
"    height: 25px;\n"
"    color: black;\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"    background-color: rgb(255, 101, 118);\n"
"    border: 2px solid black;\n"
"}\n"
"QPushButton::hover {\n"
"    background-color:  rgb(245, 85, 96);\n"
"    border: 0px;\n"
"}\n"
"QPushButton::pressed {\n"
"    \n"
"}\n"
"QPushButton:disabled{\n"
"    background-color:  rgb(123, 124, 125);\n"
"    border: 2px solid black;\n"
"}")
        self.trash_message_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ui/../icons/trash_bin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.trash_message_button.setIcon(icon1)
        self.trash_message_button.setObjectName("trash_message_button")
        self.horizontalLayout_2.addWidget(self.trash_message_button, 0, QtCore.Qt.AlignLeft)
        self.open_browser_bttn = QtWidgets.QPushButton(self.groupBox_5)
        self.open_browser_bttn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.open_browser_bttn.setStyleSheet("QPushButton {\n"
"    width: 30px;\n"
"    height: 25px;\n"
"    color: black;\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"    background-color: rgba(30, 165, 255, 186);\n"
"    border: 2px solid black;\n"
"}\n"
"QPushButton::hover {\n"
"    background-color:  rgb(32, 96, 207);\n"
"    border: 0px;\n"
"}\n"
"QPushButton::pressed {\n"
"    \n"
"}\n"
"QPushButton:disabled{\n"
"    background-color:  rgb(123, 124, 125);\n"
"    border: 2px solid black;\n"
"}")
        self.open_browser_bttn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ui/../icons/open_web.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.open_browser_bttn.setIcon(icon2)
        self.open_browser_bttn.setObjectName("open_browser_bttn")
        self.horizontalLayout_2.addWidget(self.open_browser_bttn, 0, QtCore.Qt.AlignLeft)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout_3.addWidget(self.groupBox_5, 0, 3, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.all_senders_screen)
        self.groupBox_4.setMaximumSize(QtCore.QSize(16777215, 60))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sort_option = QtWidgets.QComboBox(self.groupBox_4)
        self.sort_option.setObjectName("sort_option")
        self.sort_option.addItem("")
        self.sort_option.addItem("")
        self.sort_option.addItem("")
        self.horizontalLayout.addWidget(self.sort_option, 0, QtCore.Qt.AlignLeft)
        self.set_select_check = QtWidgets.QCheckBox(self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(15)
        self.set_select_check.setFont(font)
        self.set_select_check.setStyleSheet("color: white;")
        self.set_select_check.setObjectName("set_select_check")
        self.horizontalLayout.addWidget(self.set_select_check)
        self.delete_all_button = QtWidgets.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(15)
        self.delete_all_button.setFont(font)
        self.delete_all_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.delete_all_button.setStyleSheet("QPushButton {\n"
"    width: 30px;\n"
"    height: 25px;\n"
"    color: black;\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"    background-color: rgb(255, 101, 118);\n"
"    border: 2px solid black;\n"
"}\n"
"QPushButton::hover {\n"
"    background-color:  rgb(245, 85, 96);\n"
"    border: 0px;\n"
"}\n"
"QPushButton::pressed {\n"
"    \n"
"}\n"
"QPushButton:disabled{\n"
"    background-color:  rgb(123, 124, 125);\n"
"    border: 2px solid black;\n"
"}")
        self.delete_all_button.setText("")
        self.delete_all_button.setIcon(icon)
        self.delete_all_button.setIconSize(QtCore.QSize(18, 18))
        self.delete_all_button.setObjectName("delete_all_button")
        self.horizontalLayout.addWidget(self.delete_all_button, 0, QtCore.Qt.AlignLeft)
        self.trash_all_button = QtWidgets.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(15)
        self.trash_all_button.setFont(font)
        self.trash_all_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.trash_all_button.setStyleSheet("QPushButton {\n"
"    width: 30px;\n"
"    height: 25px;\n"
"    color: black;\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"    background-color: rgb(255, 101, 118);\n"
"    border: 2px solid black;\n"
"}\n"
"QPushButton::hover {\n"
"    background-color:  rgb(245, 85, 96);\n"
"    border: 0px;\n"
"}\n"
"QPushButton::pressed {\n"
"    \n"
"}\n"
"QPushButton:disabled{\n"
"    background-color:  rgb(123, 124, 125);\n"
"    border: 2px solid black;\n"
"}")
        self.trash_all_button.setText("")
        self.trash_all_button.setIcon(icon1)
        self.trash_all_button.setIconSize(QtCore.QSize(18, 18))
        self.trash_all_button.setObjectName("trash_all_button")
        self.horizontalLayout.addWidget(self.trash_all_button, 0, QtCore.Qt.AlignLeft)
        self.unsubscribe_button = QtWidgets.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(15)
        self.unsubscribe_button.setFont(font)
        self.unsubscribe_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.unsubscribe_button.setStyleSheet("QPushButton {\n"
"    border: 2px solid black;\n"
"    width: 30;\n"
"    height: 25px;\n"
"    color: black;\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"    background-color: rgb(203, 203, 203)\n"
"}\n"
"QPushButton::hover {\n"
"    background-color:  rgb(123, 124, 125);\n"
"    border: 0px;\n"
"}\n"
"QPushButton::pressed {\n"
"    \n"
"}\n"
"QPushButton:disabled{\n"
"    background-color:  rgb(123, 124, 125);\n"
"}")
        self.unsubscribe_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ui/../icons/unsubscribe.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.unsubscribe_button.setIcon(icon3)
        self.unsubscribe_button.setObjectName("unsubscribe_button")
        self.horizontalLayout.addWidget(self.unsubscribe_button, 0, QtCore.Qt.AlignLeft)
        self.refresh_button = QtWidgets.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(15)
        self.refresh_button.setFont(font)
        self.refresh_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.refresh_button.setStyleSheet("QPushButton {\n"
"    border: 2px solid black;\n"
"    width: 30px;\n"
"    height: 25px;\n"
"    color: black;\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"    background-color: rgb(157, 198, 150);\n"
"}\n"
"QPushButton::hover {\n"
"    background-color:  rgb(140, 169, 131);\n"
"    border: 0px;\n"
"}\n"
"QPushButton::pressed {\n"
"    \n"
"}\n"
"")
        self.refresh_button.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("ui/../icons/refresh_btn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refresh_button.setIcon(icon4)
        self.refresh_button.setObjectName("refresh_button")
        self.horizontalLayout.addWidget(self.refresh_button, 0, QtCore.Qt.AlignLeft)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout_3.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.sendersList = QtWidgets.QListWidget(self.all_senders_screen)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(15)
        self.sendersList.setFont(font)
        self.sendersList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sendersList.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.sendersList.setStyleSheet("QListWidget{\n"
"background-color: transparent;\n"
"}\n"
"QListView::item:selected\n"
"{\n"
"background-color: rgb(173, 173, 173);\n"
"}\n"
"\n"
"QListView::item:hover\n"
"{\n"
"border: 3px solid white;\n"
"}\n"
"QListView::item{\n"
"margin-top: 3px;\n"
"margin-bottom: 2px;\n"
"margin-left: 5px;\n"
"margin-right: 5px;\n"
"spacing: 10px;\n"
"border-radius: 10px;\n"
"color: rgb(9, 1, 63);\n"
"text-align: center;\n"
"background-color: rgb(215, 215, 215);\n"
"height: 45;\n"
"\n"
"}\n"
"")
        self.sendersList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sendersList.setFrameShadow(QtWidgets.QFrame.Plain)
        self.sendersList.setLineWidth(1)
        self.sendersList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.sendersList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.sendersList.setViewMode(QtWidgets.QListView.ListMode)
        self.sendersList.setObjectName("sendersList")
        self.gridLayout_3.addWidget(self.sendersList, 1, 0, 4, 1)
        self.subjectsList = QtWidgets.QListWidget(self.all_senders_screen)
        self.subjectsList.setStyleSheet("QListWidget{\n"
"background-color: transparent;\n"
"}\n"
"QListView::item:selected\n"
"{\n"
"background-color: rgb(173, 173, 173);\n"
"}\n"
"\n"
"QListView::item:hover\n"
"{\n"
"border: 3px solid white;\n"
"}\n"
"QListView::item{\n"
"margin-top: 3px;\n"
"margin-bottom: 2px;\n"
"margin-left: 5px;\n"
"margin-right: 5px;\n"
"spacing: 10px;\n"
"border-radius: 10px;\n"
"color: rgb(9, 1, 63);\n"
"text-align: center;\n"
"background-color: rgb(215, 215, 215);\n"
"height: 45;\n"
"\n"
"}\n"
"")
        self.subjectsList.setObjectName("subjectsList")
        self.gridLayout_3.addWidget(self.subjectsList, 1, 3, 4, 1)
        self.line = QtWidgets.QFrame(self.all_senders_screen)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 0, 2, 5, 1)
        self.stackedWidget.addWidget(self.all_senders_screen)
        self.loading_screen = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.loading_screen.setFont(font)
        self.loading_screen.setStyleSheet("color: white;")
        self.loading_screen.setObjectName("loading_screen")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.loading_screen)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.cancelButton = QtWidgets.QPushButton(self.loading_screen)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(16)
        self.cancelButton.setFont(font)
        self.cancelButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelButton.setStyleSheet("QPushButton {\n"
"    width: 90px;\n"
"    height: 40px;\n"
"    color: black;\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"    background-color: rgb(255, 101, 118);\n"
"    border: 2px solid black;\n"
"}\n"
"QPushButton::hover {\n"
"    background-color:  rgb(245, 85, 96);\n"
"    border: 0px;\n"
"}\n"
"QPushButton::pressed {\n"
"    \n"
"}\n"
"QPushButton:disabled{\n"
"    background-color:  rgb(123, 124, 125);\n"
"    border: 2px solid black;\n"
"}\n"
"")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("ui/../icons/cancel_btn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelButton.setIcon(icon5)
        self.cancelButton.setIconSize(QtCore.QSize(18, 18))
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout_4.addWidget(self.cancelButton, 10, 0, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem3, 4, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.loading_screen)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(16)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar{\n"
"    border-radius: 10px;\n"
"    height: 25px;\n"
"}\n"
"QProgressBar::chunk{\n"
"    border-radius: 10px;\n"
"    background: QLinearGradient( x1: 0, y1: 0,\n"
"                             x2: 1, y2: 0, \n"
"                          stop: 0 #614385, \n"
"                          stop: 1 #516395 );\n"
"    \n"
"}")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_4.addWidget(self.progressBar, 8, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.loading_screen)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 5, 0, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem4, 9, 0, 1, 1)
        self.count_label = QtWidgets.QLabel(self.loading_screen)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(15)
        self.count_label.setFont(font)
        self.count_label.setStyleSheet("padding: 10px;\n"
"padding-bottom: 20px;")
        self.count_label.setObjectName("count_label")
        self.gridLayout_4.addWidget(self.count_label, 7, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.stackedWidget.addWidget(self.loading_screen)
        self.default_page = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.default_page.setFont(font)
        self.default_page.setObjectName("default_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.default_page)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.default_page)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(26)
        font.setBold(False)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: white;")
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4, 0, QtCore.Qt.AlignHCenter)
        self.stackedWidget.addWidget(self.default_page)
        self.gridLayout_2.addWidget(self.stackedWidget, 4, 1, 3, 9)
        self.total_senders_label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(15)
        self.total_senders_label.setFont(font)
        self.total_senders_label.setStyleSheet("color: white;")
        self.total_senders_label.setObjectName("total_senders_label")
        self.gridLayout_2.addWidget(self.total_senders_label, 2, 7, 1, 1, QtCore.Qt.AlignRight)
        self.accountsList = QtWidgets.QListWidget(self.groupBox)
        self.accountsList.setMinimumSize(QtCore.QSize(0, 0))
        self.accountsList.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(13)
        font.setBold(False)
        self.accountsList.setFont(font)
        self.accountsList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.accountsList.setStyleSheet("QListView{\n"
"background-color: transparent;\n"
"border-left: 0.5px solid grey;\n"
"}\n"
"QListView::item:selected\n"
"{\n"
"background-color: rgb(173, 173, 173);\n"
"border: 2px solid white;\n"
"}\n"
"\n"
"QListView::item:hover\n"
"{\n"
"border: 3px solid white;\n"
"}\n"
"QListView::item{\n"
"margin-top: 7px;\n"
"margin-bottom: 2px;\n"
"margin-left: 5px;\n"
"margin-right: 5px;\n"
"spacing: 10px;\n"
"border-radius: 10px;\n"
"color: rgb(9, 1, 63);\n"
"text-align: center;\n"
"background-color: rgb(215, 215, 215);\n"
"height: 2;\n"
"\n"
"}\n"
"")
        self.accountsList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.accountsList.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.accountsList.setFlow(QtWidgets.QListView.LeftToRight)
        self.accountsList.setResizeMode(QtWidgets.QListView.Fixed)
        self.accountsList.setViewMode(QtWidgets.QListView.ListMode)
        self.accountsList.setObjectName("accountsList")
        self.gridLayout_2.addWidget(self.accountsList, 2, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.addAcctButton = QtWidgets.QPushButton(self.groupBox)
        self.addAcctButton.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(15)
        self.addAcctButton.setFont(font)
        self.addAcctButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addAcctButton.setStyleSheet("QPushButton {\n"
"    border: 2px solid black;\n"
"    width: 30px;\n"
"    height: 35px;\n"
"    color: black;\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"    background-color: rgb(203, 203, 203)\n"
"}\n"
"QPushButton::hover {\n"
"    background-color:  rgb(123, 124, 125);\n"
"    border: 0px;\n"
"}\n"
"QPushButton::pressed {\n"
"    \n"
"}\n"
"QPushButton:disabled{\n"
"    background-color:  rgb(123, 124, 125);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.addAcctButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("ui/../icons/add_btn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addAcctButton.setIcon(icon6)
        self.addAcctButton.setIconSize(QtCore.QSize(22, 22))
        self.addAcctButton.setObjectName("addAcctButton")
        self.gridLayout_2.addWidget(self.addAcctButton, 2, 2, 1, 1)
        self.action_label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(19)
        font.setBold(True)
        self.action_label.setFont(font)
        self.action_label.setStyleSheet("color: white;")
        self.action_label.setObjectName("action_label")
        self.gridLayout_2.addWidget(self.action_label, 2, 4, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 2, 3, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem6, 2, 6, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 5, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mail"))
        self.total_messages_label.setText(_translate("MainWindow", "Messages: "))
        self.msg_sort_option.setItemText(0, _translate("MainWindow", "Newest"))
        self.msg_sort_option.setItemText(1, _translate("MainWindow", "Oldest"))
        self.msg_sort_option.setItemText(2, _translate("MainWindow", "Alphabetical"))
        self.select_msgs_chkbox.setText(_translate("MainWindow", "Select"))
        self.delete_message_button.setToolTip(_translate("MainWindow", "Delete this message"))
        self.trash_message_button.setToolTip(_translate("MainWindow", "Trash this message."))
        self.open_browser_bttn.setToolTip(_translate("MainWindow", "Open message in browser."))
        self.sort_option.setItemText(0, _translate("MainWindow", "Newest"))
        self.sort_option.setItemText(1, _translate("MainWindow", "Oldest"))
        self.sort_option.setItemText(2, _translate("MainWindow", "Alphabetical"))
        self.set_select_check.setText(_translate("MainWindow", "Select"))
        self.delete_all_button.setToolTip(_translate("MainWindow", "Delete all messages from this sender."))
        self.trash_all_button.setToolTip(_translate("MainWindow", "Trash all messages from this sender"))
        self.unsubscribe_button.setToolTip(_translate("MainWindow", "Unsubscribe from this sender."))
        self.refresh_button.setToolTip(_translate("MainWindow", "Fetch new messages."))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
        self.label_3.setText(_translate("MainWindow", "Please Do Not Close The Application"))
        self.count_label.setText(_translate("MainWindow", "Waiting..."))
        self.label_4.setText(_translate("MainWindow", "Select or Add Account to Continue"))
        self.total_senders_label.setText(_translate("MainWindow", "Senders: "))
        self.addAcctButton.setToolTip(_translate("MainWindow", "Add account."))
        self.action_label.setText(_translate("MainWindow", "Messages"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
