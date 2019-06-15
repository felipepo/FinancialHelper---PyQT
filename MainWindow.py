from ui_mainwindow import Ui_MainWindow
from PySide2 import QtWidgets

'''class Create():
    def __init__(self):
        pass'''

class Create(QtWidgets.QMainWindow):
    def __init__(self):
        super(Create, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)