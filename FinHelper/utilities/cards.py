from PySide2 import QtWidgets, QtCore, QtGui
from utilities import funs, dict_from_list
import math
from dialogwin import transaction_window
from decimal import Decimal

class CardArea(QtWidgets.QScrollArea):
    resized = QtCore.Signal()
    def __init__(self,parent, debitOrCredit):
        super().__init__(parent)
        self.parentPage = parent
        ## Initialization ==
        self.width = 750
        self.cardWidth = 160
        self.debitOrCredit = debitOrCredit
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

        ## Creation ==
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.filters = {
            "Month": funs.GetMonth(QtCore.QDate.currentDate().month()),
            "Year": str(QtCore.QDate.currentDate().year()),
            "AccName": "Todas",
            "Category": "Todas"
        }
        self.initializeCards()

        ## Customization ==
        ## Layout ==
        self.gridLayout.addItem(spacerItem, self.row+1, 0, 1, 1)

        self.resized.connect(self.Reshape)

    def initializeCards(self):
        transData={}
        self.HideAllCards()
        self.card = {}
        allTransaction = self.parentPage.mainWin.DataBase.extract_tbl.readAll()
        for iTrans in allTransaction:
            currAcc = self.parentPage.mainWin.DataBase.acc_tbl.readById(iTrans[2])
            if "DELETED" not in currAcc[2]:
                if currAcc[1] == self.debitOrCredit:
                    currCatg = self.parentPage.mainWin.DataBase.category_tbl.readById(iTrans[1])
                    transData = {
                        "Category": currCatg[1],
                        "AccName": currAcc[2],
                        "Date": iTrans[3],
                        "Value": iTrans[4],
                        "Comment": iTrans[5],
                        "AccType": currAcc[1],
                    }
                    self.AddCard(transData, iTrans[0])

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
            currCard = self.parentPage.mainWin.DataBase.extract_tbl.readById(self.card[iCard].Id)
            currCard = dict_from_list.trans(currCard)
            accName = self.parentPage.mainWin.DataBase.acc_tbl.readById(currCard["Acc_ID"])
            if "DELETED" not in accName[2]:
                catgName = self.parentPage.mainWin.DataBase.category_tbl.readById(currCard["Catg_ID"])
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
                self.UpdateArea()

    def RemoveCardandTransaction(self, transID):
        self.RemoveCard(transID)
        self.parentPage.mainWin.DataBase.RemoveTransaction(transID)
        self.parentPage.mainWin.DataBase.extract_tbl.deleteByID(transID)
        self.parentPage.mainWin.DataBase.ReGetValues()
        self.parentPage.mainWin.updateValuePlaces()
        self.UpdateArea()

    def RemoveCard(self, transID):
        self.card[transID].hide()
        del self.card[transID]

    def UpdateArea(self):
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
        if funs.checkFilter(transData, self.filters):
            self.card[transID] = Card(self, transData, transID)
            self.card[transID].setObjectName(funs.formatCategoryName(transData['Category']))
            self.gridLayout.addWidget(self.card[transID], self.row, self.col, 1, 1)
            self.updatePosition()

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
        self.categoryLbl = QtWidgets.QLabel(self, text=self.category, objectName="CardCategoryLbl")
        self.valueLbl = QtWidgets.QLabel(self, text=str(round(Decimal(self.value), 2)), objectName="CardPositive")
        self.currencyLbl = QtWidgets.QLabel(self, text="R$", objectName="CardCurrencyLbl")
        self.dateLbl = QtWidgets.QLabel(self, text=self.date, objectName="CardDateLbl")
        self.commLbl = QtWidgets.QLabel(self, text=self.comment, objectName="CardCommentLbl")
        self.accLbl = QtWidgets.QLabel(self, text=self.acc, objectName="CardBankLbl")
        self.editButton = QtWidgets.QPushButton(self, objectName="editButton")

        ## Customization ==
        self.editButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.editButton.setIcon(QtGui.QIcon('FinHelper/data/images/EditTransfer.png'))
        self.editButton.setIconSize(QtCore.QSize(24,24))
        self.editButton.setMinimumSize(QtCore.QSize(24, 24))
        self.editButton.setMaximumSize(QtCore.QSize(24, 24))

        if self.value < 0:
            self.valueLbl.setObjectName("CardNegative")
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
                'Value': self.value,
                'Comment': self.comment,
                'AccName': self.acc,
                'Category': self.category,
                'AccType': self.type,
                'Date': self.date
            }
            wind = transaction_window.Create(self, debitOptions, creditOptions, catgOptions, prevTransData)
            if wind.exec_():
                if "Remove" not in wind.inputs:
                    targetCatg = self.cardArea.parentPage.mainWin.DataBase.category_tbl.readByName(wind.inputs["Category"])
                    targetAcc = self.cardArea.parentPage.mainWin.DataBase.acc_tbl.readByUnique(wind.inputs["AccType"], wind.inputs["AccName"])
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
        self.valueLbl.setText( str( round(Decimal(transData['Value']), 2) ))
        self.dateLbl.setText(transData['Date'])
        self.commLbl.setText(transData['Comment'])
        self.accLbl.setText(transData['AccName'])
        self.setObjectName(funs.formatCategoryName(transData['Category']))
        self.setStyle(self.style())