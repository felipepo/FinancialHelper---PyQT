from PySide2 import QtWidgets, QtXml
from FinHelper.base import base_window
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy

def main():
    financHelper = QtWidgets.QApplication([])

    SimulateData = 2
    app = base_window.Create(SimulateData)
    app.show()

    financHelper.exec_()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        input("Press enter to continue...")

    #pyside2-uic mainwindow.ui > ui_mainwindow.py
    #pyside2-uic transaction.ui > transaction.py
    #pyside2-uic newacc.ui > newacc.py
    #pyside2-uic delacc.ui > delacc.py