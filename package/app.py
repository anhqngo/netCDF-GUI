from package.ui.main_window import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


class MyMainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.ui.pushButton.clicked.connect(self.display_message)

    def display_message(self):
        self.ui.pushButton.setText("Hello World")

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = MyMainWindow()
MainWindow.show()
sys.exit(app.exec_())