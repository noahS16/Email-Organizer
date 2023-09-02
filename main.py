# THIS FILE HANDLES STARTUP AND MANAGING UI
from PyQt5.QtCore import Qt

import inboxWindow
from PyQt5 import QtWidgets
import sys
from view import Setup


if __name__ == "__main__":
    # initializing...
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = inboxWindow.Ui_MainWindow()
    ui.setupUi(MainWindow)
    # Some manual ui setup
    setup = Setup(ui)
    # finishing...

    MainWindow.show()
    sys.exit(app.exec_())


