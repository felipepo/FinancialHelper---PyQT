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
        self.debitGroupBox = GroupBox(self, "Conta")
        self.creditGroupBox = GroupBox(self, "Cartão de Crédito")
        self.budgetGroupBox = BudgetGroupBox(self, "Orçamento")
        self.graphicsView = QtWidgets.QGraphicsView(self, objectName="graphicsView")

        ## Customization ==
        self.debitGroupBox.setObjectName("debitGroupBox")
        self.creditGroupBox.setObjectName("creditGroupBox")
        self.budgetGroupBox.setObjectName("budgetGroupBox")

        ## Layout ==
        self.gridLayout.addWidget(self.debitGroupBox, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.creditGroupBox, 1, 0, 1, 1)
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
        if self.title() == "Conta":
            options = self.homepage.mainWin.DataBase.AllAccounts["debit"][:]
        else:
            options = self.homepage.mainWin.DataBase.AllAccounts["credit"][:]

        options.insert(0,"Todas")
        self.comboBox.addItems(options)
        self.comboBox.currentIndexChanged.connect(self.UpdateValue)
        self.UpdateValue()

        ## Layout ==
        self.gridLayout.addWidget(self.Label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.valueLbl, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.currencyLbl, 1, 0, 1, 1)

    def UpdateValue(self):
        acc = self.comboBox.currentText()
        if self.title() == "Conta":
            value = self.homepage.mainWin.DataBase.Totals['debit'][acc]
        else:
            value = self.homepage.mainWin.DataBase.Totals['credit'][acc]
        valueStr = "{:.{}f}".format(value, 2)
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