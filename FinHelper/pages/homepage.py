from PySide2 import QtWidgets, QtCore
from ..dialogwin import transaction_window
from ..utilities import dict_from_list
from ..graphs import plotting
from decimal import Decimal

class Create(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWin = parent
        self.setObjectName("HomePage")
        ## Initialization ==

        ## Creation ==
        self.payGroupBox = QtWidgets.QGroupBox(self, title = "Pagamentos", objectName="payGroupBox")
        self.debitGroupBox = GroupBox(self, "Débito")
        self.creditGroupBox = GroupBox(self, "Cartão de Crédito")
        self.budgetGroupBox = BudgetGroupBox(self, "Orçamento")
        self.bar_chart = plotting.BarChart(self.mainWin.DataBase)
        self.bar_chart.createGraph()

        ## Customization ==
        self.debitGroupBox.setObjectName("debitGroupBox")
        self.creditGroupBox.setObjectName("creditGroupBox")
        self.budgetGroupBox.setObjectName("budgetGroupBox")

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.addWidget(self.debitGroupBox, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.creditGroupBox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.bar_chart, 0, 1, 2, 5)
        self.gridLayout.addWidget(self.budgetGroupBox, 2, 0, 1, 3)
        self.gridLayout.addWidget(self.payGroupBox, 2, 3, 1, 3)

    def updateGraph(self):
        self.bar_chart.updateGraph()

class GroupBox(QtWidgets.QGroupBox):
    def __init__(self, parent, titleSTR):
        super().__init__(parent)
        self.homepage=parent
        self.mainWin = self.homepage.mainWin
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
        if self.title() == "Débito":
            options = self.mainWin.DataBase.AllAccounts["debit"][:]
        else:
            options = self.mainWin.DataBase.AllAccounts["credit"][:]
            self.payBill = QtWidgets.QPushButton(self,objectName="Button", text="Pagar Fatura")
            self.payBill.clicked.connect(self.payCurrentBill)
            self.gridLayout.addWidget(self.payBill, 3,1,1,1)

        options.insert(0,"Todas")
        self.comboBox.addItems(options)
        self.comboBox.currentIndexChanged.connect(self.UpdateValue)
        self.UpdateValue()

        ## Layout ==
        self.gridLayout.addWidget(self.Label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.valueLbl, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.currencyLbl, 1, 0, 1, 1)

    def payCurrentBill(self):
        mayProceed = False
        targetCredit = self.mainWin.DataBase.acc_tbl.readByUnique(2, self.comboBox.currentText())
        prevTransData = {
            'Value': float(self.valueLbl.text()),
            'Comment': "Pagamento Cartão {}".format(self.comboBox.currentText()),
            'Category': "Outros",
            'AccType': 1,
            'Date': QtCore.QDate.currentDate().toString('dd/MM/yyyy')
        }
        while mayProceed == False:
            debitOptions = self.mainWin.DataBase.AllAccounts["debit"]
            creditOptions = self.mainWin.DataBase.AllAccounts["credit"]
            catgOptions = self.mainWin.DataBase.AllCategories
            wind = transaction_window.Create(self, debitOptions, creditOptions, catgOptions, prevTransData)
            if wind.exec_():
                if "AppendData" in wind.inputs:
                    self.mainWin.newCategory(wind.inputs)
                instalments = wind.inputs['Instalments']
                targetCatg = self.mainWin.DataBase.category_tbl.readByName(wind.inputs["Category"])
                targetDebit = self.mainWin.DataBase.acc_tbl.readByUnique(wind.inputs["AccType"], wind.inputs["AccName"])
                accData = dict_from_list.account(targetCredit)
                accData["Total"] = accData["Total"] - wind.inputs["Value"]
                self.mainWin.DataBase.acc_tbl.updateById(accData)
                wind.inputs["Value"] = wind.inputs["Value"]/instalments
                transInfo = {"Catg_ID":targetCatg[0], "Acc_ID":targetDebit[0], "Comment":wind.inputs["Comment"], "Value":wind.inputs["Value"], "Date":wind.inputs["Date"]}
                if targetDebit[1] == 2:
                    for iMonth in range(instalments):
                        instalmentInfo = transInfo.copy()
                        cardData = wind.inputs.copy()
                        if instalments > 1:
                            instalmentInfo["Comment"] = '({}/{}) {}'.format(iMonth+1, instalments, instalmentInfo["Comment"])
                            instalmentInfo["Date"] = QtCore.QDate.fromString(instalmentInfo["Date"], 'dd/MM/yyyy').addDays((iMonth)*30).toString('dd/MM/yyyy')
                        transID = self.mainWin.DataBase.NewTransaction(instalmentInfo)
                        cardData["Comment"] = instalmentInfo["Comment"]
                        cardData["Date"] = instalmentInfo["Date"]
                        self.mainWin.creditCardPage.cardArea.AddCard(cardData, transID)
                else:
                    transID = self.mainWin.DataBase.NewTransaction(transInfo)
                    self.mainWin.accPage.cardArea.AddCard(wind.inputs, transID)
                self.mainWin.updateInteface()
                mayProceed = True
            else:
                mayProceed = True

    def UpdateValue(self):
        acc = self.comboBox.currentText()
        if self.title() == "Débito":
            value = round(Decimal(self.mainWin.DataBase.Totals['debit'][acc]), 2)
        else:
            value = round(Decimal(self.mainWin.DataBase.Totals['credit'][acc]), 2)
        self.valueLbl.setText(str(value))

class BudgetGroupBox(QtWidgets.QGroupBox):
    def __init__(self, parent, titleSTR):
        super().__init__(parent)
        self.setTitle(titleSTR)

        ## Initialization ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.budgets = {}

        ## Creation ==
        self.bar_chart = plotting.HorBarChart()
        self.bar_chart.createGraph()
        for irow in [1, 2, 3]:
            for icol in range(3):
                self.budgets[str(irow)+str(icol)] = QtWidgets.QLabel(self,  text=str(irow)+str(icol), objectName=str(irow)+str(icol))
                self.gridLayout.addWidget(self.budgets[str(irow)+str(icol)], irow, icol, 1, 1)

        ## Customization ==

        ## Layout ==
        self.gridLayout.addWidget(self.bar_chart, 0, 0, 1, 3)