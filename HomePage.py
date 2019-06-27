from PySide2 import QtWidgets, QtCore

class Create(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWin = parent
        self.setObjectName("HomePage")
        ## Initialization ==

        ## Creation ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.payGroupBox = QtWidgets.QGroupBox(self, title = "Pagamentos", objectName="payGroupBox")
        self.accGroupBox = GroupBox(self, "Conta")
        self.CCGroupBox = GroupBox(self, "Cartão de Crédito")
        self.budgetGroupBox = BudgetGroupBox(self, "Orçamento")
        self.graphicsView = QtWidgets.QGraphicsView(self, objectName="graphicsView")

        ## Customization ==
        self.accGroupBox.setObjectName("accGroupBox")
        self.CCGroupBox.setObjectName("CCGroupBox")
        self.budgetGroupBox.setObjectName("budgetGroupBox")

        ## Layout ==
        self.gridLayout.addWidget(self.accGroupBox, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.CCGroupBox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.graphicsView, 0, 1, 2, 5)
        self.gridLayout.addWidget(self.budgetGroupBox, 2, 0, 1, 3)
        self.gridLayout.addWidget(self.payGroupBox, 2, 3, 1, 3)

class GroupBox(QtWidgets.QGroupBox):
    def __init__(self, parent, titleSTR):
        super().__init__(parent)
        self.homepage=parent
        ## Initialization ==
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setTitle(titleSTR)

        ## Creation ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.Label = QtWidgets.QLabel(self, text = "Contas", objectName="Label")
        self.comboBox = QtWidgets.QComboBox(self, objectName="comboBox")
        self.currencyLbl = QtWidgets.QLabel(self, text = "R$", objectName="currencyLbl")
        self.valueLbl = QtWidgets.QLabel(self, objectName="valueLbl")

        ## Customizaion ==
        options = list(self.homepage.mainWin.allAcc.accountsObjs.keys())
        self.comboBox.addItems(options)
        self.comboBox.currentIndexChanged.connect(self.UpdateValue)

        if self.title() == "Conta":
            valueStr = str(self.homepage.mainWin.allAcc.accountsObjs[self.comboBox.currentText()].totalAmount)
        else:
            valueStr = str(self.homepage.mainWin.allAcc.creditCardObjs[self.comboBox.currentText()].totalAmount)
        self.valueLbl.setText(valueStr)

        ## Layout ==
        self.gridLayout.addWidget(self.Label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.valueLbl, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.currencyLbl, 1, 0, 1, 1)

    def UpdateValue(self):
        acc = self.comboBox.currentText()
        if self.title() == "Conta":
            valueStr = str(self.homepage.mainWin.allAcc.accountsObjs[acc].totalAmount)
        else:
            valueStr = str(self.homepage.mainWin.allAcc.creditCardObjs[acc].totalAmount)
        self.valueLbl.setText(valueStr)

class BudgetGroupBox(QtWidgets.QGroupBox):
    def __init__(self, parent, titleSTR):
        super().__init__(parent)
        self.setTitle(titleSTR)

        ## Initialization ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.budgets = {}

        ## Creation ==
        self.progressBar = QtWidgets.QProgressBar(self, objectName="progressBar")
        for irow in [1, 2, 3]:
            for icol in range(3):
                self.budgets[str(irow)+str(icol)] = QtWidgets.QLabel(self,  text=str(irow)+str(icol), objectName=str(irow)+str(icol))
                self.gridLayout.addWidget(self.budgets[str(irow)+str(icol)], irow, icol, 1, 1)

        ## Customization ==
        self.progressBar.setProperty("value", 24)

        ## Layout ==
        self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 3)