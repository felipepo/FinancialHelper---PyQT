from PySide2 import QtWidgets, QtCore, QtGui
from ..pages import homepage, debit_page, credit_page
from . import menu, toolbar
from ..utilities import generate, funs
from ..database import sql_class
from ..interfacestyle import style

class Create(QtWidgets.QMainWindow):
    ## Signals ==
    resized = QtCore.Signal()
    def __init__(self, SimulateData):
        ## Initialization ==
        super().__init__()
        self.setWindowTitle('Financial Helper')
        icon = QtGui.QIcon()
        finHelperFolder = funs.getFinHelperPath()
        iconPath = "{}/data/images/Icon.ico".format(finHelperFolder)
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
        self.toolbar = toolbar.ToolBar(self)
        self.menubar = menu.MenuBar(self)

        # Pages
        self.homePage = homepage.Create(self)
        self.accPage = debit_page.Page(self)
        self.creditCardPage = credit_page.Page(self)

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
        funs.checkFolderExist()
        self.DataBase = sql_class.Create(self.SimulateData)
        allCategories = {}
        emptyTable = self.DataBase.category_tbl.readAll()
        if not emptyTable:
            defaultCatg = generate.generateCatg(rand="off")
            allCategories = defaultCatg
            for iCatg in list(defaultCatg.keys()):
                self.DataBase.category_tbl.insert(iCatg, defaultCatg[iCatg])
            if self.SimulateData == 1:
                print("Simulating Data")
                self.DataBase.simulateData(nTrans=40, nAcc=10)
        else:
            allCategories = dict( [(iRow[1], iRow[2]) for iRow in emptyTable] )

        self.styleObj = style.Create(allCategories)
        self.setStyleSheet(self.styleObj.InterfaceStyle)
        self.setStyle(self.style())

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).closeEvent(*args, **kwargs)
        self.DataBase.close_db()

    def updateValuePlaces(self):
        self.DataBase.ReGetValues()
        # Update Total
        self.homePage.debitGroupBox.UpdateValue()
        self.homePage.creditGroupBox.UpdateValue()
        self.accPage.controlFrame.setValueGroup.UpdateEditBox()
        self.creditCardPage.controlFrame.setValueGroup.UpdateEditBox()
        # Update filters
        self.accPage.controlFrame.filterGroup.getComboValues()
        self.creditCardPage.controlFrame.filterGroup.getComboValues()
        # Update Plots
        self.homePage.updateGraph()
        self.creditCardPage.updateGraph()
        self.accPage.updateGraph()

    def newCategory(self, catgData):
        for iStyle in catgData["AppendData"]:
            if iStyle != "Name" and iStyle != "rgb":
                self.styleObj.appendStyle(catgData["AppendData"][iStyle])
        self.DataBase.category_tbl.insert(catgData["AppendData"]["Name"], catgData["AppendData"]["rgb"])
        self.setStyleSheet(self.styleObj.InterfaceStyle)
        self.styleObj.createQSSFile()
        self.setStyle(self.style())

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
        sideButtons = {"AccPageButton": "Contas de Débito", "CCPageButton": "Cartões de Crédito",
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