from PySide2 import QtWidgets, QtCore, QtGui
import math
import Funs
import unidecode
import NewWindows

class Create(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWin = parent
        self.setObjectName("AccPage")
        ## Initialization ==
        ## Creation ==
        self.cardArea = CardArea(self)
        self.filterFrame = FilterFrame(self)
        self.graphicsView = QtWidgets.QGraphicsView(self, objectName="graphicsView")
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 200))
        self.graphicsView.setMaximumSize(QtCore.QSize(16777215, 500))

        ## Customization ==
        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.cardArea, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.filterFrame, 1, 1, 1, 1)

class FilterFrame(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.accPage=parent
        ## Initialization ==
        self.setMinimumSize(QtCore.QSize(421, 0))
        #self.setMaximumSize(QtCore.QSize(421, 16777215))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("FilterFrame")

        ## Creation ==
        self.button_1 = QtWidgets.QPushButton(self, text="Button1", objectName="button1")
        self.button_2 = QtWidgets.QPushButton(self, text="Button2", objectName="button2")
        self.filterGroup = FilterGroup(self)

        ## Customization ==
        self.button_1.clicked.connect(self.accPage.cardArea.HideAllCards)
        self.button_2.clicked.connect(self.accPage.cardArea.ShowAllCards)

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.addWidget(self.filterGroup,0,0,1,2)
        self.gridLayout.addWidget(self.button_1,1,0,1,1)
        self.gridLayout.addWidget(self.button_2,1,1,1,1)

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

class CardArea(QtWidgets.QScrollArea):
    resized = QtCore.Signal()   
    def __init__(self,parent):
        super().__init__(parent)
        self.accPage = parent
        ## Initialization ==
        self.width = 750
        self.cardWidth = 160
        self.setMinimumSize(QtCore.QSize(self.width, 0))
        #self.setMaximumSize(QtCore.QSize(700, 16777215))
        self.setWidgetResizable(True)
        self.setObjectName("cardArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 698, 285))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents, objectName="gridLayout")
        self.nCOl = 4
        self.row = 0
        self.col = 0
        self.setWidget(self.scrollAreaWidgetContents)
        self.card = {}
        transData={}

        ## Creation ==
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        if self.accPage.mainWin.SimulateData == 0:
            if self.accPage.mainWin.allAcc.accountsObjs['Todas'].transactions or self.accPage.mainWin.allAcc.creditCardObjs['Todas'].transactions:
                for iFrame in list(self.accPage.mainWin.allAcc.accountsObjs['Todas'].transactions.keys()):
                    currTransData = self.accPage.mainWin.allAcc.accountsObjs['Todas'].transactions[iFrame]
                    transData["Value"] = currTransData.value
                    transData["Category"] = currTransData.category
                    transData["Account"] = currTransData.bankAccount
                    transData["Comment"] = currTransData.comment
                    transData["Date"] = currTransData.date
                    transData["AccType"] = "bank"
                    self.AddCard(transData, currTransData.transID)
                for iFrame in list(self.accPage.mainWin.allAcc.creditCardObjs['Todas'].transactions.keys()):
                    currTransData = self.accPage.mainWin.allAcc.creditCardObjs['Todas'].transactions[iFrame]
                    transData["Value"] = currTransData.value
                    transData["Category"] = currTransData.category
                    transData["Account"] = currTransData.bankAccount
                    transData["Comment"] = currTransData.comment
                    transData["Date"] = currTransData.date
                    transData["AccType"] = "creditCard"
                    self.AddCard(transData, currTransData.transID)
        else:
            for iFrame in range(60):
                transData = Funs.generateData()
                accData = {
                    'NewAcc':transData['Account'],
                    'InitialValue':transData['InitialValue'],
                    'AccType':transData['AccType'],
                    'DueDay':transData['DueDay'],
                    'LimitValue':transData['LimitValue'],
                    'ClosingDay':transData['ClosingDay']
                    }
                if transData['AccType'] == 'bank':
                    if transData['Account'] not in list(self.accPage.mainWin.allAcc.accountsObjs.keys()):
                        self.accPage.mainWin.allAcc.AddAcc(accData)
                        self.accPage.mainWin.homePage.accGroupBox.comboBox.addItem(transData['Account'])
                else:
                    if transData['Account'] not in list(self.accPage.mainWin.allAcc.creditCardObjs.keys()):
                        self.accPage.mainWin.allAcc.AddAcc(accData)
                        self.accPage.mainWin.homePage.CCGroupBox.comboBox.addItem(transData['Account'])
                transID = self.accPage.mainWin.allAcc.AddTransaction(transData)
                if transData['AccType'] == 'bank':
                    self.accPage.mainWin.homePage.accGroupBox.UpdateValue()
                else:
                    self.accPage.mainWin.homePage.CCGroupBox.UpdateValue()
                self.AddCard(transData, transID)

        ## Customization ==
        ## Layout ==
        self.gridLayout.addItem(spacerItem, self.row+1, 0, 1, 1)

        self.resized.connect(self.Reshape)

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def updatePosition(self):
        self.col = self.col + 1
        if self.col == self.nCOl:
            self.col = 0
            self.row = self.row + 1

    def UpdateCard(self, transData, transID):
        self.card[transID].categoryLbl.setText(transData['Category'])
        self.card[transID].valueLbl.setText(str(transData['Value']))
        self.card[transID].dateLbl.setText(transData['Date'])
        self.card[transID].commLbl.setText(transData['Comment'])
        self.card[transID].accLbl.setText(transData['Account'])
        self.card[transID].setObjectName(unidecode.unidecode(transData['Category']))
        self.card[transID].setStyle(self.card[transID].style())

    def HideCard(self):
        pass

    def RemoveCard(self, transID):
        del self.card[transID]
    
    def HideAllCards(self):
        for iCard in list(self.card.keys()):
            self.card[iCard].hide()
            self.gridLayout.removeWidget(self.card[iCard])
        self.row = 0
        self.col = 0

    def ShowAllCards(self):
        for iCard in list(self.card.keys()):
            self.gridLayout.addWidget(self.card[iCard],self.row, self.col, 1, 1)
            self.card[iCard].show()
            self.updatePosition()
    
    def AddCard(self, transData, transID):
        self.card[transID] = Card(self, transData, transID)
        self.card[transID].setObjectName(unidecode.unidecode(transData['Category']))
        self.gridLayout.addWidget(self.card[transID], self.row, self.col, 1, 1)
        self.updatePosition()
    
    def ShiftCards(self,tow=0,col=0):
        pass

    def Reshape(self):
        # Minimun - 700 (Card - 150 *4 = 600)
        currWidth = self.frameGeometry().width()
        testWidth = math.floor((currWidth-100)/self.cardWidth )
        if testWidth != self.nCOl:
            self.nCOl = testWidth
            self.HideAllCards()
            self.ShowAllCards()

class Card(QtWidgets.QFrame):
    def __init__(self, parent, transData, transID):
        super().__init__(parent)
        self.cardArea = parent
        self.Id = transID
        self.type = transData["AccType"]
        ## Initialization ==
        self.setMinimumSize(QtCore.QSize(parent.cardWidth, 100))
        self.setMaximumSize(QtCore.QSize(parent.cardWidth, 100))
        #self.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        ## Creation ==
        self.categoryLbl = QtWidgets.QLabel(self, text=transData["Category"], objectName="categoryLbl")
        self.valueLbl = QtWidgets.QLabel(self, text=str(transData["Value"]), objectName="valueLbl")
        self.currencyLbl = QtWidgets.QLabel(self, text="R$", objectName="currencyLbl")
        self.dateLbl = QtWidgets.QLabel(self, text=transData["Date"], objectName="dateLbl")
        self.commLbl = QtWidgets.QLabel(self, text=transData["Comment"], objectName="commLbl")
        self.accLbl = QtWidgets.QLabel(self, text=transData["Account"], objectName="accLbl")
        self.editButton = QtWidgets.QPushButton(self, objectName="editButton")

        ## Customization ==
        self.editButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.editButton.setIcon(QtGui.QIcon('Icons/EditTransfer.png'))
        self.editButton.setIconSize(QtCore.QSize(24,24))
        self.editButton.setMinimumSize(QtCore.QSize(24, 24))
        self.editButton.setMaximumSize(QtCore.QSize(24, 24))

        self.currencyLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.accLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)

        self.editButton.clicked.connect(self.Update)
        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.setContentsMargins(9,9,9,9)
        # self.gridLayout.addWidget(self.categoryLbl, 0, 0, 1, 2)
        # self.gridLayout.addWidget(self.dateLbl, 0, 2, 1, 1)
        # self.gridLayout.addWidget(self.currencyLbl, 1, 0, 1, 1)
        # self.gridLayout.addWidget(self.valueLbl, 1, 1, 1, 1)
        # self.gridLayout.addWidget(self.accLbl, 1, 2, 1, 1)
        # self.gridLayout.addWidget(self.commLbl, 2, 0, 1, 2)
        # self.gridLayout.addWidget(self.editButton, 2, 2, 1, 1, alignment = QtCore.Qt.AlignRight)
        # 0 | 1 | 2 | 3 | 4 | 5 | 6
        # CAT       |        Date
        # RS|    00.00  |banco
        # comment               |OK
        self.gridLayout.addWidget(self.categoryLbl, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.dateLbl, 0, 3, 1, 4, alignment = QtCore.Qt.AlignRight)
        self.gridLayout.addWidget(self.currencyLbl, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.valueLbl, 1, 1, 1, 3)
        self.gridLayout.addWidget(self.accLbl, 1, 4, 1, 3)
        self.gridLayout.addWidget(self.commLbl, 2, 0, 1, 6)
        self.gridLayout.addWidget(self.editButton, 2, 6, 1, 1, alignment = QtCore.Qt.AlignRight)

    def Update(self):
        mayProceed = False
        while mayProceed == False:
            accOptions = list(self.cardArea.accPage.mainWin.allAcc.accountsObjs.keys())
            del accOptions[0]
            ccOptions = list(self.cardArea.accPage.mainWin.allAcc.creditCardObjs.keys())
            del ccOptions[0]
            catOptions = list(self.cardArea.accPage.mainWin.allCategories.category.keys())
            transData = {
                'Value': float(self.valueLbl.text()),
                'Comment': self.commLbl.text(),
                'Account': self.accLbl.text(),
                'Category': self.categoryLbl.text(),
                'AccType': self.type
            }
            wind = NewWindows.Transaction(self, accOptions, ccOptions, catOptions, transData)
            if wind.exec_():
                updatedFlag = self.cardArea.accPage.mainWin.allAcc.UpdateTransaction(self.Id, wind.inputs, wind.inputs['Account'], self.accLbl.text(), wind.inputs['AccType'])
                if updatedFlag == 'OK':
                    if wind.inputs['AccType'] == 'bank':
                        self.cardArea.accPage.mainWin.homePage.accGroupBox.UpdateValue()
                    else:
                        self.cardArea.accPage.mainWin.homePage.CCGroupBox.UpdateValue()
                    mayProceed = True
                    self.cardArea.accPage.mainWin.accPage.cardArea.UpdateCard(wind.inputs, self.Id)                    
                else:
                    print('Problema na conta')
            else: 
                mayProceed = True