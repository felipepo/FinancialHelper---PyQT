from PySide2 import QtWidgets, QtCore

class Create(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("AccPage")
        ## Initialization ==
        ## Creation ==
        self.cardArea = CardArea(self)
        self.filterFrame = FilterFrame(self)
        self.graphicsView = QtWidgets.QGraphicsView(self, objectName="graphicsView")
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 200))
        self.graphicsView.setMaximumSize(QtCore.QSize(16777215, 300))

        ## Customization ==
        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.cardArea, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.filterFrame, 1, 1, 1, 1)

class FilterFrame(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
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
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        for iFilter in self.filterNames:
            self.filter[iFilter] = Filter(self, iFilter)
            self.gridLayout.addWidget(self.filter[iFilter].filterLbl, self.row,self.col,1,1)
            self.gridLayout.addWidget(self.filter[iFilter].chooseCombo, self.row,self.col+1,1,1)
            self.updatePosition()

        ## Customization ==
        ## Layout ==
        self.gridLayout.addItem(spacerItem, self.row+1, 0, 1, 1)
    
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
    def __init__(self,parent):
        super().__init__(parent)
        ## Initialization ==
        self.setMinimumSize(QtCore.QSize(700, 0))
        #self.setMaximumSize(QtCore.QSize(700, 16777215))
        self.setWidgetResizable(True)
        self.setObjectName("cardArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 698, 285))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents, objectName="gridLayout")
        self.row = 0
        self.col = 0
        self.setWidget(self.scrollAreaWidgetContents)
        self.card = {}

        ## Creation ==
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        for iFrame in range(40):
            self.AddCard("card"+str(iFrame))

        ## Customization ==
        ## Layout ==
        self.gridLayout.addItem(spacerItem, self.row+1, 0, 1, 1)

    def updatePosition(self):
        self.col = self.col + 1
        if self.col == 4:
            self.col = 0
            self.row = self.row + 1

    def Update(self):
        pass

    def HideCard(self):
        pass

    def RemoveCard(self, transID):
        del self.card[transID]
    
    def HideAllCards(self):
        self.gridLayout.removeItem
    
    def AddCard(self, transID):
        self.card[transID] = Card(self, transID)
        self.card[transID].setObjectName(transID)
        self.gridLayout.addWidget(self.card[transID], self.row, self.col, 1, 1)
        self.updatePosition()
    
    def ShiftCards(self,tow=0,col=0):
        pass

    def Reshape(self):
        currWidth = self.frameGeometry().width()
        self.gridLayout

        print(currWidth)

class Card(QtWidgets.QFrame):
    def __init__(self, parent, transID):
        super().__init__(parent)
        self.Id = transID
        ## Initialization ==
        self.setMinimumSize(QtCore.QSize(150, 100))
        self.setMaximumSize(QtCore.QSize(150, 100))
        self.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        ## Creation ==
        self.categoryLbl = QtWidgets.QLabel(self, text="Categoria", objectName="categoryLbl")
        self.valueLbl = QtWidgets.QLabel(self, text="00,00", objectName="valueLbl")
        self.currencyLbl = QtWidgets.QLabel(self, text="R$", objectName="currencyLbl")
        self.dateLbl = QtWidgets.QLabel(self, text="10/10/2010", objectName="dateLbl")
        self.commLbl = QtWidgets.QLabel(self, text="Compras da feira", objectName="commLbl")
        self.accLbl = QtWidgets.QLabel(self, text="Nubank", objectName="accLbl")
        self.editButton = QtWidgets.QPushButton(self, text="e", objectName="editButton")

        ## Customization ==
        self.editButton.setCursor(QtCore.Qt.PointingHandCursor)

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.setContentsMargins(3,3,3,3)

        self.gridLayout.addWidget(self.categoryLbl, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.dateLbl, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.currencyLbl, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.valueLbl, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.accLbl, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.commLbl, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.editButton, 2, 2, 1, 1)

    def Update(self):
        pass