from PySide2 import QtWidgets, QtCore, QtGui
from ..utilities import cards, funs
from ..graphs import plotting
from decimal import Decimal
from . import debit_page, credit_page

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
            self.setValueGroup = credit_page.SetValue(parentPage)
        else:
            self.setValueGroup = debit_page.SetValue(parentPage)

        ## Customization ==

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.addWidget(self.filterGroup,0,0,1,2)
        self.gridLayout.addWidget(self.setValueGroup,1,0,1,2)

class FilterGroup(QtWidgets.QGroupBox):
    def __init__(self, parentPage):
        super().__init__(parentPage)
        ## Initialization ==
        self.parentPage = parentPage
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
        if self.parentPage.objectName()=="AccPage":
            allAccounts = self.mainWin.DataBase.AllAccounts["debit"][:]
        else:
            allAccounts = self.mainWin.DataBase.AllAccounts["credit"][:]
        allAccounts.insert(0, "Todas")
        self.nameCombo.clear()
        self.yearCombo.clear()
        self.categoryCombo.clear()

        self.nameCombo.addItems(allAccounts)
        self.yearCombo.addItems(years)
        self.categoryCombo.addItems(allCategories)