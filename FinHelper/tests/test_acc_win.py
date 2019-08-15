from ..dialogwin import account_window
from PySide2 import QtWidgets

def run_test():
    financHelper = QtWidgets.QApplication([])
    parent = QtWidgets.QFrame()
    wind = account_window.New(parent)
    if wind.exec_():
        print(wind.inputs)
    financHelper.exec_()