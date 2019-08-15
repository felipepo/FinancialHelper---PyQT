from ..dialogwin import transaction_window
from PySide2 import QtWidgets

def run_test():
    financHelper = QtWidgets.QApplication([])
    parent = QtWidgets.QFrame()
    wind = transaction_window.Create(parent, ["Debit1", "Debit2"], ["Credit1", "Credit2"], ["Cat1", "Catg2"])
    if wind.exec_():
        print(wind.inputs)
    financHelper.exec_()

if __name__ == "__main__":
    run_test()