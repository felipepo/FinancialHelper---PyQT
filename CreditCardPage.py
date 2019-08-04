from PySide2 import QtWidgets, QtCore, QtGui
import Funs
import Card

class Create(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWin = parent
        self.setObjectName("CreditPage")
        ## Initialization ==
        ## Creation ==
        self.cardArea = Card.CardArea(self, 2)
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
        self.creditPage=parent
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
        self.gridLayout.addWidget(self.setValueGroup,0,0,1,2)
        self.gridLayout.addWidget(self.filterGroup,1,0,1,2)

class SetValueGroup(QtWidgets.QGroupBox):
    def __init__(self, parent):
        ## Initialization ==
        super().__init__(parent)
        self.controlFrame=parent
        self.setTitle("Cartão de Crédito")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setObjectName("SetValueGroup")
        
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
        options = self.controlFrame.creditPage.mainWin.DataBase.AllAccounts["credit"][:]
        self.nameDropDown.addItems(options)
        self.nameDropDown.currentIndexChanged.connect(self.UpdateEditBox)
        self.UpdateEditBox()
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.finalValue.setSizePolicy(sizePolicy)
        self.nameDropDown.setSizePolicy(sizePolicy)

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
            currAccData = self.controlFrame.creditPage.mainWin.DataBase.AccountTable.readByUnique(2,currAcc)
            self.finalValue.setText(str(currAccData[3]))
            self.limitValue.setText(str(currAccData[4]))
            self.DueDay.setText(str(currAccData[5]))
            self.ClosingDay.setText(str(currAccData[6]))

    def SetFinalValue(self):
        accName = self.nameDropDown.currentText()
        Acc_ID = self.controlFrame.creditPage.mainWin.DataBase.AccountTable.readByUnique(2, accName)
        Catg_ID = self.controlFrame.creditPage.mainWin.DataBase.CategoryTable.readByName("Outros")
        diffValue = float(self.finalValue.text()) - self.controlFrame.creditPage.mainWin.DataBase.Totals["credit"][accName]
        accData = {
            'Acc_ID':Acc_ID[0],
            'Type':Acc_ID[1],
            'Name':Acc_ID[2],
            'Total':Acc_ID[3],
            'Limit':int(self.limitValue.text()),
            'DueDay':int(self.DueDay.text()),
            'ClosingDay':int(self.ClosingDay.text())
        }
        self.controlFrame.creditPage.mainWin.DataBase.AccountTable.updateById(accData)
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
            transID = self.controlFrame.creditPage.mainWin.DataBase.NewTransaction(transData)
            self.controlFrame.creditPage.cardArea.AddCard(transData, transID)

class FilterGroup(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        ## Initialization ==
        self.setTitle("Filtros")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setObjectName("FilterGroup")
        self.filterNames = ["Ano", "Mês", "Categoria"]
        self.filter = {}
        self.row=0
        self.col=0
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")

        ## Creation ==
        vertSpacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        for iFilter in self.filterNames:
            self.filter[iFilter] = Filter(self, iFilter)
            self.gridLayout.addWidget(self.filter[iFilter].filterLbl, self.row,self.col,1,1)
            self.gridLayout.addWidget(self.filter[iFilter].chooseCombo, self.row,self.col+1,1,1)
            self.updatePosition()

        ## Customization ==
        ## Layout ==
        self.gridLayout.addItem(vertSpacerItem, self.row+1, 0, 1, 1)
    
    def addFilter(self, filterName="", options=[]):
        self.filter[filterName]=options

    def updateFilter(self):
        pass

    def updatePosition(self):
        self.col = self.col + 2
        if self.col == 4:
            self.col = 0
            self.row = self.row + 1

class Filter():
    def __init__(self, parent, filterName="", options=[]):
        self.filterName = filterName
        self.filterLbl = QtWidgets.QLabel(parent, text=filterName, objectName=filterName)
        self.options = options
        self.chooseCombo = QtWidgets.QComboBox(parent, objectName=filterName+"Combo")