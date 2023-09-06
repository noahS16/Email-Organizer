# THIS FILE HANDLES STARTUP AND MANAGING UI
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QWidget, QMenu

import inboxWindow
from PyQt5 import QtWidgets
import sys
from view import Worker, AccountSetup, UiData


class MainUi(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.data = UiData(self.ui)
        self.account_setup = AccountSetup(self.ui, self.data.users)
        self.worker = Worker(self.ui, self.data.users)

        self.ui.accountsList.installEventFilter(self)



    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and (source is self.ui.accountsList or source is self.ui.sendersList):
            menu = QMenu()
            menu.addAction("Delete")
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                self.account.remove_account(item)
            return True
        return super().eventFilter(source, event)




if __name__ == "__main__":
    # initializing...
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = inboxWindow.Ui_MainWindow()
    ui.setupUi(MainWindow)
    # Some manual ui setup
    setup = MainUi(ui)
    # finishing...
    MainWindow.show()
    sys.exit(app.exec_())


