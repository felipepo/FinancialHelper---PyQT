from PySide2 import QtWidgets, QtCore, QtGui
import HomePage
import AccPage
import Menu
import ToolBar
import CreditCardPage
import Funs
import SQLDB
from InterfaceStyle import Style

class Create(QtWidgets.QMainWindow):
    ## Signals ==
    resized = QtCore.Signal()
    def __init__(self, SimulateData):
        ## Initialization ==
        super().__init__()
        self.setWindowTitle('Financial Helper')
        icon = QtGui.QIcon()
        iconPath = "Icons/Icon.ico"
        icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setObjectName("MainWindow")
        self.resize(1315, 682)
        self.setIconSize(QtCore.QSize(32, 32))
        self.SimulateData = SimulateData

        self.initialize()
        ## Creation ==
        self.centralwidget = QtWidgets.QWidget(self, objectName="centralwidget", styleSheet="")
        self.showHideSide = HideShowButton(self)
        self.stackFrame = QtWidgets.QStackedWidget(self.centralwidget, objectName="stackFrame", styleSheet="")
        self.sideFrame = SideFrame(self)
        self.statusbar = QtWidgets.QStatusBar(self, objectName="statusbar")
        self.toolbar = ToolBar.ToolBar(self)
        self.menubar = Menu.MenuBar(self)

        # Pages
        self.homePage = HomePage.Create(self)
        self.accPage = AccPage.Create(self)
        self.creditCardPage = CreditCardPage.Create(self)

        ## Customization ==
        self.stackFrame.addWidget(self.homePage)
        self.stackFrame.addWidget(self.accPage)
        self.stackFrame.addWidget(self.creditCardPage)
        self.stackFrame.setCurrentIndex(0)

        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.setCentralWidget(self.centralwidget)
        self.setStatusBar(self.statusbar)
        self.setMenuBar(self.menubar)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackFrame.sizePolicy().hasHeightForWidth())
        self.stackFrame.setSizePolicy(sizePolicy)

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget, objectName="gridLayout", spacing=0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.addWidget(self.showHideSide, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.stackFrame, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.sideFrame, 0, 0, 1, 1)

        self.resized.connect(self.accPage.cardArea.Reshape)

    def initialize(self):
        if self.SimulateData == 1:
            self.DataBase = SQLDB.Create(1)
            self.DataBase.simulateData(nTrans=40, nAcc=10, nCatg=10)
        else:
            self.DataBase = SQLDB.Create(2)

        firstRun = self.DataBase.CategoryTable.readAll()
        if not firstRun:
            defaultCatg = Funs.generateCatg(rand="off")
            for iCatg in list(defaultCatg.keys()):
                self.DataBase.CategoryTable.insert(iCatg, defaultCatg[iCatg])

        self.styleObj = Style.Create(self.DataBase.CategoryTable)
        self.setStyleSheet(self.styleObj.InterfaceStyle)
        self.setStyle(self.style())

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).closeEvent(*args, **kwargs)
        self.DataBase.close_db()

    def updateValuePlaces(self):
        self.homePage.debitGroupBox.UpdateValue()
        self.accPage.controlFrame.setValueGroup.UpdateEditBox()
        self.homePage.creditGroupBox.UpdateValue()
        self.creditCardPage.controlFrame.setValueGroup.UpdateEditBox()
        self.accPage.controlFrame.filterGroup.getComboValues()

class SideFrame(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWin = parent
        ## Initialization ==
        self.setObjectName("sideFrame")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(150, 150))
        self.setMaximumSize(QtCore.QSize(150, 16777215))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.button = {}
        sideButtons = {"AccPageButton": "Contas", "CCPageButton": "Cartões de Crédito",
        "BudgetPageButton": "Orçamento", "TablesPageButton": "Tabelas",
        "InvestPageButton": "Investimentos Geral", "BondsPageButton": "Renda Fixa", "StocksPageButton": "Ações"}

        ## Creation ==
        pageNumber = 0
        self.verticalLayout = QtWidgets.QVBoxLayout(self, objectName="verticalLayout", spacing=0)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        for button in list(sideButtons.keys()):
            pageNumber = pageNumber + 1
            self.button[button] = SideButton(pageNumber, self.mainWin, text=sideButtons[button])
            self.verticalLayout.addWidget(self.button[button])

        ## Customization ==

        ## Layout ==
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addItem(spacerItem)

class SideButton(QtWidgets.QPushButton):
    def __init__(self, pageNumber, parent, text = ""):
        super().__init__(parent)
        self.mainWin = parent
        self.pageNumber = pageNumber
        self.setObjectName("SideButton")
        self.setText(text)
        self.clicked.connect(self.goTo)

    def goTo(self):
        self.mainWin.stackFrame.setCurrentIndex(self.pageNumber)

class HideShowButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        super().__init__(parent.centralwidget)
        self.parent = parent
        self.setText("<<")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMaximumSize(QtCore.QSize(20, 16777215))
        self.clicked.connect(self.showHide)

    def showHide(self):
        currText = self.text()
        if currText == "<<":
            self.setText('>>')
            self.parent.sideFrame.hide()
        else:
            self.setText('<<')
            self.parent.sideFrame.show()