from PySide2 import QtWidgets, QtXml
from base import base_window


if __name__ == "__main__":
    financHelper = QtWidgets.QApplication([])

    SimulateData = 2
    app = base_window.Create(SimulateData)
    app.show()

    financHelper.exec_()

    #pyside2-uic mainwindow.ui > ui_mainwindow.py
    #pyside2-uic transaction.ui > transaction.py
    #pyside2-uic newacc.ui > newacc.py
    #pyside2-uic delacc.ui > delacc.py