# THIS FILE HANDLES STARTUP AND MANAGING UI
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QWidget, QMenu

import inboxWindow
from PyQt5 import QtWidgets
import sys
from ui_manager import UiData
from view import MainUi


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


