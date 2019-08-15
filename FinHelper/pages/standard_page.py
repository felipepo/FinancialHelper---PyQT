from PySide2 import QtWidgets, QtCore, QtGui
from ..utilities import cards, plotting, funs
from decimal import Decimal

class StandarPage(QtWidgets.QWidget):
    def __init__(self, parent, objName):
        super().__init__(parent)
        self.mainWin = parent
        self.setObjectName(objName)
        ## Initialization ==
        ## Creation ==
        debitOrCredit = 1 if objName == "AccPage" else 2
        self.cardArea = cards.CardArea(self, debitOrCredit)
        self.controlFrame = ControlFrame(self)
        self.bar_chart = plotting.BarChart(self.mainWin.DataBase)
        self.bar_chart.createGraph(self.cardArea.card)

        ## Customization ==

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")

        self.gridLayout.addWidget(self.bar_chart, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.cardArea, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.controlFrame, 1, 1, 1, 1)

    def updateGraph(self):
        self.bar_chart.updateGraph(self.cardArea.card)

class ControlFrame(QtWidgets.QFrame):
    def __init__(self, parentPage):
        super().__init__(parentPage)
        ## Initialization ==
        self.setMinimumSize(QtCore.QSize(421, 0))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("ControlFrame")

        ## Creation ==
        self.filterGroup = FilterGroup(parentPage)
        if parentPage.objectName() == "CreditPage":
            self.setValueGroup = SetValueCredit(parentPage)
        else:
            self.setValueGroup = SetValueDebit(parentPage)

        ## Customization ==

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.addWidget(self.filterGroup,0,0,1,2)
        self.gridLayout.addWidget(self.setValueGroup,1,0,1,2)

class SetValueDebit(QtWidgets.QGroupBox):
    def __init__(self, parentPage):
        ## Initialization ==
        super().__init__(parentPage)
        self.mainWin = parentPage.mainWin
        self.cardArea = parentPage.cardArea
        self.setTitle("Conta")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setObjectName("SetValueGroup")
        self.count_change = 0

        ## Creation ==
        self.accName = QtWidgets.QLabel(self, text="Nome", objectName="NameLbl")
        self.nameDropDown = QtWidgets.QComboBox(self, objectName="nameDropDown")
        self.valLbl = QtWidgets.QLabel(self, text="Definir valor atual", objectName="valLbl")
        self.finalValue = QtWidgets.QLineEdit(self, placeholderText="00.0", alignment=QtCore.Qt.AlignCenter, objectName="finalValue")
        self.applyButton = QtWidgets.QPushButton(self, text="Aplicar", objectName="button2")

        ## Customization ==
        self.applyButton.clicked.connect(self.SetFinalValue)
        options = self.mainWin.DataBase.AllAccounts["debit"][:]
        self.nameDropDown.addItems(options)
        self.nameDropDown.currentIndexChanged.connect(self.UpdateEditBox)
        self.UpdateEditBox()

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.finalValue.setSizePolicy(sizePolicy)
        self.nameDropDown.setSizePolicy(sizePolicy)

        self.finalValue.textChanged.connect(lambda state, targetEdit=self.finalValue: self.numberEntered(targetEdit))

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.addWidget(self.accName,0,0,1,1)
        self.gridLayout.addWidget(self.nameDropDown,0,1,1,1)
        self.gridLayout.addWidget(self.valLbl,1,0,1,1)
        self.gridLayout.addWidget(self.finalValue,1,1,1,1)
        self.gridLayout.addWidget(self.applyButton,2,1,1,1)

    def UpdateEditBox(self):
        currAcc = self.nameDropDown.currentText()
        if currAcc:
            currAccTotal = self.mainWin.DataBase.Totals['debit'][currAcc]
            self.finalValue.setText( str(round(Decimal(currAccTotal), 2)) )

    def SetFinalValue(self):
        accName = self.nameDropDown.currentText()
        Acc_ID = self.mainWin.DataBase.acc_tbl.readByUnique(1, accName)
        Catg_ID = self.mainWin.DataBase.category_tbl.readByName("Outros")
        diffValue = float(self.finalValue.text()) - self.mainWin.DataBase.Totals["debit"][accName]
        if diffValue != 0:
            transData = {
                "Catg_ID": Catg_ID[0],
                "Category": "Outros",
                "AccType": 1,
                "AccName": accName,
                "Acc_ID": Acc_ID[0],
                "Date": QtCore.QDate.currentDate().toString('dd/MM/yyyy'),
                "Value": diffValue,
                "Comment": "Atualização do valor final"
            }
            transID = self.mainWin.DataBase.NewTransaction(transData)
            self.cardArea.AddCard(transData, transID)
            self.mainWin.updateValuePlaces()

    def numberEntered(self, targetEdit):
        self.count_change += 1
        if self.count_change < 2:
            currText = targetEdit.text()
            shiftedText = funs.shift(currText)
            targetEdit.setText(shiftedText)
            if shiftedText == currText:
                self.count_change -= 1
        else:
            self.count_change = 0

class SetValueCredit(QtWidgets.QGroupBox):
    def __init__(self, parentPage):
        ## Initialization ==
        super().__init__(parentPage)
        self.mainWin = parentPage.mainWin
        self.cardArea = parentPage.cardArea
        self.setTitle("Cartão de Crédito")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setObjectName("SetValueGroup")
        self.count_change = 0

        ## Creation ==
        self.accName = QtWidgets.QLabel(self, text="Nome", objectName="NameLbl")
        self.nameDropDown = QtWidgets.QComboBox(self, objectName="nameDropDown")
        self.valLbl = QtWidgets.QLabel(self, text="Definir valor atual", objectName="valLbl")
        self.finalValue = QtWidgets.QLineEdit(self, placeholderText="00.0", alignment=QtCore.Qt.AlignCenter, objectName="finalValue")
        self.limitLbl = QtWidgets.QLabel(self, text="Limite", objectName="limitLbl")
        self.limitValue = QtWidgets.QLineEdit(self, placeholderText="00.0", alignment=QtCore.Qt.AlignCenter, objectName="limitValue")
        self.dueLbl = QtWidgets.QLabel(self, text="Vencimeto", objectName="dueLbl")
        self.DueDay = QtWidgets.QLineEdit(self, placeholderText="00", alignment=QtCore.Qt.AlignCenter, objectName="DueDay")
        self.closingLbl = QtWidgets.QLabel(self, text="Fechamento", objectName="closingLbl")
        self.ClosingDay = QtWidgets.QLineEdit(self, placeholderText="00", alignment=QtCore.Qt.AlignCenter, objectName="ClosingDay")
        self.applyButton = QtWidgets.QPushButton(self, text="Aplicar", objectName="button2")

        ## Customization ==
        self.applyButton.clicked.connect(self.SetFinalValue)
        options = self.mainWin.DataBase.AllAccounts["credit"][:]
        self.nameDropDown.addItems(options)
        self.nameDropDown.currentIndexChanged.connect(self.UpdateEditBox)
        self.UpdateEditBox()

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.finalValue.setSizePolicy(sizePolicy)
        self.nameDropDown.setSizePolicy(sizePolicy)

        self.finalValue.textChanged.connect(lambda state, targetEdit=self.finalValue: self.numberEntered(targetEdit))

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.addWidget(self.accName,0,1,1,1)
        self.gridLayout.addWidget(self.nameDropDown,0,2,1,1)
        self.gridLayout.addWidget(self.valLbl,1,0,1,1)
        self.gridLayout.addWidget(self.finalValue,1,1,1,1)
        self.gridLayout.addWidget(self.limitLbl,1,2,1,1)
        self.gridLayout.addWidget(self.limitValue,1,3,1,1)
        self.gridLayout.addWidget(self.dueLbl,2,0,1,1)
        self.gridLayout.addWidget(self.DueDay,2,1,1,1)
        self.gridLayout.addWidget(self.closingLbl,2,2,1,1)
        self.gridLayout.addWidget(self.ClosingDay,2,3,1,1)
        self.gridLayout.addWidget(self.applyButton,3,3,1,1)

    def UpdateEditBox(self):
        currAcc = self.nameDropDown.currentText()
        if currAcc:
            currAccData = self.mainWin.DataBase.acc_tbl.readByUnique(2,currAcc)
            self.finalValue.setText( str(round(Decimal(currAccData[3]), 2)) )
            self.limitValue.setText( str(round(Decimal(currAccData[4]), 2)) )
            self.DueDay.setText(str(currAccData[5]))
            self.ClosingDay.setText(str(currAccData[6]))

    def SetFinalValue(self):
        accName = self.nameDropDown.currentText()
        Acc_ID = self.mainWin.DataBase.acc_tbl.readByUnique(2, accName)
        Catg_ID = self.mainWin.DataBase.category_tbl.readByName("Outros")
        diffValue = float(self.finalValue.text()) - self.mainWin.DataBase.Totals["credit"][accName]
        accData = {
            'Acc_ID':Acc_ID[0],
            'Type':Acc_ID[1],
            'Name':Acc_ID[2],
            'Total':Acc_ID[3],
            'Limit':float(self.limitValue.text()),
            'DueDay':int(self.DueDay.text()),
            'ClosingDay':int(self.ClosingDay.text())
        }
        self.mainWin.DataBase.acc_tbl.updateById(accData)
        if diffValue != 0:
            transData = {
                "Catg_ID": Catg_ID[0],
                "Category": "Outros",
                "AccType": 1,
                "AccName": accName,
                "Acc_ID": Acc_ID[0],
                "Date": QtCore.QDate.currentDate().toString('dd/MM/yyyy'),
                "Value": diffValue,
                "Comment": "Atualização do valor final"
            }
            transID = self.mainWin.DataBase.NewTransaction(transData)
            self.cardArea.AddCard(transData, transID)
            self.mainWin.updateValuePlaces()

    def numberEntered(self, targetEdit):
        self.count_change += 1
        if self.count_change < 2:
            currText = targetEdit.text()
            shiftedText = funs.shift(currText)
            targetEdit.setText(shiftedText)
            if shiftedText == currText:
                self.count_change -= 1
        else:
            self.count_change = 0

class FilterGroup(QtWidgets.QGroupBox):
    def __init__(self, parentPage):
        super().__init__(parentPage)
        ## Initialization ==
        self.mainWin = parentPage.mainWin
        self.cardArea = parentPage.cardArea
        self.setTitle("Filtros")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setObjectName("FilterGroup")
        self.months = ("Todos", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")

        ## Creation ==
        self.nameLbl = QtWidgets.QLabel(self, text="Nome", objectName="nameLbL")
        self.yearLbl = QtWidgets.QLabel(self, text="Ano", objectName="yearLbl")
        self.monthLbl = QtWidgets.QLabel(self, text="Mês", objectName="monthLbl")
        self.categoryLbl = QtWidgets.QLabel(self, text="Categoria", objectName="categoryLbl")
        self.nameCombo = QtWidgets.QComboBox(self, objectName="ComboBox")
        self.yearCombo = QtWidgets.QComboBox(self, objectName="ComboBox")
        self.monthCombo = QtWidgets.QComboBox(self, objectName="ComboBox")
        self.categoryCombo = QtWidgets.QComboBox(self, objectName="ComboBox")
        self.applyFilter = QtWidgets.QPushButton(self, text="Aplicar", objectName="Button")
        # vertSpacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        ## Customization ==
        self.applyFilter.clicked.connect(self.updateFilters)
        self.getComboValues()
        self.monthCombo.addItems(self.months)

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.addWidget(self.nameLbl, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.nameCombo, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.yearLbl, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.yearCombo, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.monthLbl, 0, 4, 1, 1)
        self.gridLayout.addWidget(self.monthCombo, 0, 5, 1, 1)
        self.gridLayout.addWidget(self.categoryLbl, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.categoryCombo, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.applyFilter, 1, 5, 1, 1)
        # self.gridLayout.addItem(vertSpacerItem, 1, 0, 1, 1)

    def addFilter(self, filterName="", options=[]):
        self.filter[filterName]=options

    def updateFilters(self):
        self.cardArea.filters["Month"] = self.monthCombo.currentText()
        self.cardArea.filters["Year"] = self.yearCombo.currentText()
        self.cardArea.filters["AccName"] = self.nameCombo.currentText()
        self.cardArea.filters["Category"] = self.categoryCombo.currentText()

        self.cardArea.HideAllCards()
        self.cardArea.initializeCards()

    def getComboValues(self):
        catgTable = self.mainWin.DataBase.category_total_tbl.readAll()
        years = ["Todos"]
        for iRow in catgTable:
            currYear = str(iRow[4])
            if currYear not in years:
                years.append(currYear)
        allCategories = list(self.mainWin.DataBase.AllCategories)
        allCategories.insert(0, "Todas")
        allAccounts = self.mainWin.DataBase.AllAccounts["credit"][:]
        allAccounts.insert(0, "Todas")
        self.nameCombo.clear()
        self.yearCombo.clear()
        self.categoryCombo.clear()

        self.nameCombo.addItems(allAccounts)
        self.yearCombo.addItems(years)
        self.categoryCombo.addItems(allCategories)