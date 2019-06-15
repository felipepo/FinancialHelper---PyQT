from PySide2 import QtWidgets
import MainWindow


if __name__ == "__main__":
    financHelper = QtWidgets.QApplication([])

    app = MainWindow.Create()
    app.show()
    
    financHelper.exec_()

    #pyside2-uic mainwindow.ui > ui_mainwindow.py
    #pyside2-uic transaction.ui > transaction.py
    #pyside2-uic newacc.ui > newacc.py
    #pyside2-uic delacc.ui > delacc.py