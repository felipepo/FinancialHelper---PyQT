from PySide2 import QtWidgets
from PySide2 import QtXml
import MainWindow


if __name__ == "__main__":
    financHelper = QtWidgets.QApplication([])

    SimulateData = 2
    app = MainWindow.Create(SimulateData)
    app.show()
    
    financHelper.exec_()

    #pyside2-uic mainwindow.ui > ui_mainwindow.py
    #pyside2-uic transaction.ui > transaction.py
    #pyside2-uic newacc.ui > newacc.py
    #pyside2-uic delacc.ui > delacc.py