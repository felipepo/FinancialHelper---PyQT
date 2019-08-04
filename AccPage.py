from PySide2 import QtWidgets, QtCore, QtGui
import Funs
import Card

class Create(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWin = parent
        self.setObjectName("AccPage")
        ## Initialization ==
        ## Creation ==
        self.cardArea = Card.CardArea(self, 1)
        self.controlFrame = ControlFrame(self)
        self.graphicsView = QtWidgets.QGraphicsView(self, objectName="graphicsView")
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 200))
        self.graphicsView.setMaximumSize(QtCore.QSize(16777215, 500))

        ## Customization ==
        
        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.cardArea, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.controlFrame, 1, 1, 1, 1)

class ControlFrame(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.accPage=parent
        ## Initialization ==
        self.setMinimumSize(QtCore.QSize(421, 0))
        #self.setMaximumSize(QtCore.QSize(421, 16777215))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("ControlFrame")

        ## Creation ==
        self.filterGroup = FilterGroup(self)
        self.setValueGroup = SetValueGroup(self)

        ## Customization ==

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.addWidget(self.filterGroup,0,0,1,2)
        self.gridLayout.addWidget(self.setValueGroup,1,0,1,2)

class SetValueGroup(QtWidgets.QGroupBox):
    def __init__(self, parent):
        ## Initialization ==
        super().__init__(parent)
        self.controlFrame=parent
        self.setTitle("Conta")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setObjectName("SetValueGroup")
        
        ## Creation ==
        self.accName = QtWidgets.QLabel(self, text="Nome", objectName="NameLbl")
        self.nameDropDown = QtWidgets.QComboBox(self, objectName="nameDropDown")
        self.valLbl = QtWidgets.QLabel(self, text="Definir valor atual", objectName="valLbl")
        self.finalValue = QtWidgets.QLineEdit(self, placeholderText="00.0", alignment=QtCore.Qt.AlignCenter, objectName="finalValue")
        self.applyButton = QtWidgets.QPushButton(self, text="Aplicar", objectName="button2")
        
        ## Customization ==
        self.applyButton.clicked.connect(self.SetFinalValue)
        options = self.controlFrame.accPage.mainWin.DataBase.AllAccounts["debit"][:]
        self.nameDropDown.addItems(options)
        self.nameDropDown.currentIndexChanged.connect(self.UpdateEditBox)
        self.UpdateEditBox()
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.finalValue.setSizePolicy(sizePolicy)
        self.nameDropDown.setSizePolicy(sizePolicy)

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
            currAccTotal = self.controlFrame.accPage.mainWin.DataBase.Totals['debit'][currAcc]
            self.finalValue.setText(str(currAccTotal))

    def SetFinalValue(self):
        accName = self.nameDropDown.currentText()
        Acc_ID = self.controlFrame.accPage.mainWin.DataBase.AccountTable.readByUnique(1, accName)
        Catg_ID = self.controlFrame.accPage.mainWin.DataBase.CategoryTable.readByName("Outros")
        diffValue = float(self.finalValue.text()) - self.controlFrame.accPage.mainWin.DataBase.Totals["debit"][accName]
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
            transID = self.controlFrame.accPage.mainWin.DataBase.NewTransaction(transData)
            self.controlFrame.accPage.cardArea.AddCard(transData, transID)

class FilterGroup(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        ## Initialization ==
        self.setTitle("Filtros")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setObjectName("FilterGroup")
        self.controlFrame = parent
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
        self.controlFrame.accPage.cardArea.filters["Month"] = self.monthCombo.currentText()
        self.controlFrame.accPage.cardArea.filters["Year"] = self.yearCombo.currentText()
        self.controlFrame.accPage.cardArea.filters["AccName"] = self.nameCombo.currentText()
        self.controlFrame.accPage.cardArea.filters["Category"] = self.categoryCombo.currentText()

        self.controlFrame.accPage.cardArea.HideAllCards()
        self.controlFrame.accPage.cardArea.initializeCards()

    def updatePosition(self):
        self.col = self.col + 2
        if self.col == 4:
            self.col = 0
            self.row = self.row + 1

    def getComboValues(self):
        catgTable = self.controlFrame.accPage.mainWin.DataBase.CategoryTotalTable.readAll()
        years = ["Todos"]
        for iRow in catgTable:
            currYear = str(iRow[4])
            if currYear not in years:
                years.append(currYear)
        allCategories = list(self.controlFrame.accPage.mainWin.DataBase.AllCategories)
        allCategories.insert(0, "Todas")
        allAccounts = self.controlFrame.accPage.mainWin.DataBase.AllAccounts["debit"][:]
        allAccounts.insert(0, "Todas")
        self.nameCombo.clear()
        self.yearCombo.clear()
        self.categoryCombo.clear()

        self.nameCombo.addItems(allAccounts)
        self.yearCombo.addItems(years)
        self.categoryCombo.addItems(allCategories)