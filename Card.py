from PySide2 import QtWidgets, QtCore, QtGui
import Funs
import math
from DialogWindows import TransactionWindow

class CardArea(QtWidgets.QScrollArea):
    resized = QtCore.Signal()   
    def __init__(self,parent, debitOrCredit):
        super().__init__(parent)
        self.parentPage = parent
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
        allTransaction = self.parentPage.mainWin.DataBase.ExtractTable.readAll()
        for iTrans in allTransaction:
            currAcc = self.parentPage.mainWin.DataBase.AccountTable.readById(iTrans[2])
            if "DELETED" not in currAcc[2]:
                if currAcc[1] == debitOrCredit:
                    currCatg = self.parentPage.mainWin.DataBase.CategoryTable.readById(iTrans[1])
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
        cardsToBeRemoved = []
        for iCard in self.card:
            currCard = self.parentPage.mainWin.DataBase.ExtractTable.readById(self.card[iCard].Id)
            currCard = Funs.trans_dictFromlist(currCard)
            accName = self.parentPage.mainWin.DataBase.AccountTable.readById(currCard["Acc_ID"])
            if "DELETED" not in accName[2]:
                catgName = self.parentPage.mainWin.DataBase.CategoryTable.readById(currCard["Catg_ID"])
                transData = {
                    "AccType": accName[1],
                    "AccName":accName[2],
                    "Comment":currCard["Comment"],
                    "Value":currCard["Value"],
                    "Date":currCard["Date"],
                    "Category":catgName[1]
                }
                self.card[currCard["Trans_ID"]].Update(transData)
            else:
                cardsToBeRemoved.append(currCard["Trans_ID"])
        for iCard in cardsToBeRemoved:
                self.RemoveCard(iCard)

    def RemoveCardandTransaction(self, transID):
        self.RemoveCard(transID)
        self.parentPage.mainWin.DataBase.ExtractTable.deleteByID(transID)

    def RemoveCard(self, transID):
        self.card[transID].hide()
        del self.card[transID]
        self.HideAllCards()
        self.ShowAllCards()
    
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
        self.card[transID].setObjectName(Funs.formatCategoryName(transData['Category']))
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
        # 0 | 1 | 2 | 3 | 4 | 5 | 6
        # CAT       |        Date
        # RS|    00.00  |banco
        # comment               |OK
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.setContentsMargins(9,9,9,9)

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
            debitOptions = self.cardArea.parentPage.mainWin.DataBase.AllAccounts["debit"]
            creditOptions = self.cardArea.parentPage.mainWin.DataBase.AllAccounts["credit"]
            catgOptions = self.cardArea.parentPage.mainWin.DataBase.AllCategories
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
                if "Remove" not in wind.inputs:
                    targetCatg = self.cardArea.parentPage.mainWin.DataBase.CategoryTable.readByName(wind.inputs["Category"])
                    targetAcc = self.cardArea.parentPage.mainWin.DataBase.AccountTable.readByUnique(wind.inputs["AccType"], wind.inputs["AccName"])
                    transInfo = {"Trans_ID":self.Id, "Catg_ID":targetCatg[0], "Acc_ID":targetAcc[0], "Comment":wind.inputs["Comment"], "Value":wind.inputs["Value"], "Date":wind.inputs["Date"]}
                    updatedFlag = self.cardArea.parentPage.mainWin.DataBase.UpdateTransaction(transInfo)
                    if updatedFlag == 'OK':
                        self.cardArea.parentPage.mainWin.DataBase.ReGetValues()  
                        self.cardArea.parentPage.mainWin.updateValuePlaces()
                        mayProceed = True
                        self.Update(wind.inputs)                  
                    else:
                        print('Problema na conta')
                else:
                    self.cardArea.RemoveCardandTransaction(self.Id)
                    mayProceed = True
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
        self.setObjectName(Funs.formatCategoryName(transData['Category']))
        self.setStyle(self.style())