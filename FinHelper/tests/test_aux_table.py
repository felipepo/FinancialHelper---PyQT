from ..pages import aux_table_page
from PySide2 import QtWidgets

class MyGui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = aux_table_page.ContributionTable()
        self.table2 = aux_table_page.MonthlyProfitTable()
        parent = QtWidgets.QFrame(self)
        self.setCentralWidget(parent)
        self.setGeometry(50,50,1280,920)

        testButton = QtWidgets.QPushButton(text="Apply")
        self.offsetInput = QtWidgets.QLineEdit(placeholderText="Offset")
        self.goaltInput = QtWidgets.QLineEdit(placeholderText="Goal")

        testButton.clicked.connect(self.getValues)

        ver = QtWidgets.QGridLayout(parent)
        ver.addWidget(self.table, 0,0,1,2)
        ver.addWidget(self.table2, 0,3,1,1)
        ver.addWidget(self.offsetInput, 1,0,1,1)
        ver.addWidget(self.goaltInput, 1,1,1,1)
        ver.addWidget(testButton, 2,0,1,2)
        self.show()

    def getValues(self):
        offset = int(self.offsetInput.text())
        goal = int(self.goaltInput.text())
        self.table.fill_table(offset, goal)

def run_test():
    financHelper = QtWidgets.QApplication([])

    mygui = MyGui()
    financHelper.exec_()