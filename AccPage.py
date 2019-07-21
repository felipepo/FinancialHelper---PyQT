from PySide2 import QtWidgets, QtCore, QtGui
import math
import Funs
import unidecode
from DialogWindows import TransactionWindow

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
        allTransaction = self.accPage.mainWin.DataBase.ExtractTable.readAll()
        for iTrans in allTransaction:
            currCatg = self.accPage.mainWin.DataBase.CategoryTable.readById(iTrans[1])
            currAcc = self.accPage.mainWin.DataBase.AccountTable.readById(iTrans[2])
            transData["Category"] = currCatg[1]
            transData["AccName"] = currAcc[2]
            transData["Date"] = iTrans[3]
            transData["Value"] = iTrans[4]
            transData["Comment"] = iTrans[5]
            transData["AccType"] = currAcc[1]
            self.AddCard(transData, iTrans[0])

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
        self.card[transID].Update(transData)

    def UpdateALLCards(self):
        for iCard in self.card:
            currCard = self.accPage.mainWin.DataBase.ExtractTable.readById(self.card[iCard].Id)
            currCard = Funs.trans_dictFromlist(currCard)
            catgName = self.accPage.mainWin.DataBase.CategoryTable.readById(currCard["Catg_ID"])
            accName = self.accPage.mainWin.DataBase.AccountTable.readById(currCard["Acc_ID"])
            transData = {
                "AccType": accName[1],
                "AccName":accName[2],
                "Comment":currCard["Comment"],
                "Value":currCard["Value"],
                "Date":currCard["Date"],
                "Category":catgName[1]
            }
            self.card[currCard["Trans_ID"]].Update(transData)

    def HideCard(self):
        pass

    def RemoveCard(self, transID):
        accType = self.card[transID].type
        accType = self.card[transID].type
        self.accPage.mainWin.allAcc.RemoveTransaction(acc, accType, transID)
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
        self.acc = transData["AccName"]
        self.comment = transData["Comment"]
        self.value = transData["Value"]
        self.date = transData["Date"]
        self.category = transData["Category"]
        ## Initialization ==
        self.setMinimumSize(QtCore.QSize(parent.cardWidth, 100))
        self.setMaximumSize(QtCore.QSize(parent.cardWidth, 100))
        #self.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        ## Creation ==
        self.categoryLbl = QtWidgets.QLabel(self, text=self.category, objectName="categoryLbl")
        self.valueLbl = QtWidgets.QLabel(self, text=str(self.value), objectName="valueLbl")
        self.currencyLbl = QtWidgets.QLabel(self, text="R$", objectName="currencyLbl")
        self.dateLbl = QtWidgets.QLabel(self, text=self.date, objectName="dateLbl")
        self.commLbl = QtWidgets.QLabel(self, text=self.comment, objectName="commLbl")
        self.accLbl = QtWidgets.QLabel(self, text=self.acc, objectName="accLbl")
        self.editButton = QtWidgets.QPushButton(self, objectName="editButton")

        ## Customization ==
        self.editButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.editButton.setIcon(QtGui.QIcon('Icons/EditTransfer.png'))
        self.editButton.setIconSize(QtCore.QSize(24,24))
        self.editButton.setMinimumSize(QtCore.QSize(24, 24))
        self.editButton.setMaximumSize(QtCore.QSize(24, 24))

        self.currencyLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.accLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)

        self.editButton.clicked.connect(self.UpdateWindow)
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

    def UpdateWindow(self):
        mayProceed = False
        while mayProceed == False:
            debitOptions = self.cardArea.accPage.mainWin.DataBase.AllAccounts["debit"]
            creditOptions = self.cardArea.accPage.mainWin.DataBase.AllAccounts["credit"]
            catgOptions = self.cardArea.accPage.mainWin.DataBase.AllCategories
            prevTransData = {
                'Value': float(self.value),
                'Comment': self.comment,
                'Account': self.acc,
                'Category': self.category,
                'AccType': self.type,
                'Date': self.date
            }
            wind = TransactionWindow.Create(self, debitOptions, creditOptions, catgOptions, prevTransData)
            if wind.exec_():
                targetCatg = self.cardArea.accPage.mainWin.DataBase.CategoryTable.readByName(wind.inputs["Category"])
                targetAcc = self.cardArea.accPage.mainWin.DataBase.AccountTable.readByUnique(wind.inputs["AccType"], wind.inputs["AccName"])
                transInfo = {"Trans_ID":self.Id, "Catg_ID":targetCatg[0], "Acc_ID":targetAcc[0], "Comment":wind.inputs["Comment"], "Value":wind.inputs["Value"], "Date":wind.inputs["Date"]}
                updatedFlag = self.cardArea.accPage.mainWin.DataBase.UpdateTransaction(transInfo)
                if updatedFlag == 'OK':
                    self.cardArea.accPage.mainWin.DataBase.ReGetValues()  
                    self.cardArea.accPage.mainWin.homePage.debitGroupBox.UpdateValue()
                    self.cardArea.accPage.mainWin.homePage.creditGroupBox.UpdateValue()
                    mayProceed = True
                    self.Update(wind.inputs)                  
                else:
                    print('Problema na conta')
            else: 
                mayProceed = True

    def Update(self, transData):
        self.type = transData["AccType"]
        self.acc = transData["AccName"]
        self.comment = transData["Comment"]
        self.value = transData["Value"]
        self.date = transData["Date"]
        self.category = transData["Category"]

        self.categoryLbl.setText(transData['Category'])
        self.valueLbl.setText(str(transData['Value']))
        self.dateLbl.setText(transData['Date'])
        self.commLbl.setText(transData['Comment'])
        self.accLbl.setText(transData['AccName'])
        self.setObjectName(unidecode.unidecode(transData['Category']))
        self.setStyle(self.style())