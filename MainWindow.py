from ui_mainwindow import Ui_MainWindow
from PySide2 import QtWidgets, QtCore, QtGui
import HomePage
import AccPage
import NewWindows
import Classes

class Create(QtWidgets.QMainWindow):
    ## Signals ==
    resized = QtCore.Signal()       
    def __init__(self):
        ## Initialization ==
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(1315, 682)
        self.setIconSize(QtCore.QSize(32, 32)) 

        ## Creation ==
        self.centralwidget = QtWidgets.QWidget(self, objectName="centralwidget", styleSheet="")
        self.showHideSide = QtWidgets.QPushButton(self.centralwidget, text="<<", objectName="showHideSide")
        self.stackFrame = QtWidgets.QStackedWidget(self.centralwidget, objectName="stackFrame", styleSheet="")
        self.sideFrame = SideFrame(self)
        self.statusbar = QtWidgets.QStatusBar(self, objectName="statusbar")
        self.toolbar = ToolBar(self)
        self.menubar = MenuBar(self)
        # Pages
        self.homePage = HomePage.Create(self)
        self.accPage = AccPage.Create(self)

        # Create Object with all accounts
        try:
            categoryData = Funs.loadData("Categories")
            accountData = Funs.loadData("Data") #Loads the data from file
            self.allAcc = accountData #Creates object from loaded data
            self.categories = categoryData
        except:
            self.allAcc = Classes.AllAccounts() #Creates object from scratch
            self.allAcc.AddAcc("Todas", "bank")
            self.allAcc.AddAcc("Todas", "creditCard")
            self.allCategories = Classes.Categories()


        ## Customization ==
        self.stackFrame.addWidget(self.homePage)
        self.stackFrame.addWidget(self.accPage)
        self.stackFrame.setCurrentIndex(0)

        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.setCentralWidget(self.centralwidget)
        self.setStatusBar(self.statusbar)
        self.setMenuBar(self.menubar)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showHideSide.sizePolicy().hasHeightForWidth())
        self.showHideSide.setSizePolicy(sizePolicy)
        self.showHideSide.setMaximumSize(QtCore.QSize(20, 16777215))
        self.showHideSide.clicked.connect(self.showHide)

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

    def showHide(self):
        print(self.accPage.filterFrame.frameGeometry().width())
        currText = self.showHideSide.text()
        if currText == "<<":
            self.showHideSide.setText('>>')
            self.sideFrame.hide()
        else:
            self.showHideSide.setText('<<')
            self.sideFrame.show()

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

class SideFrame(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
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
            self.button[button] = SideButton(pageNumber, self.parent, text=sideButtons[button])
            self.button[button].setObjectName(button)
            self.verticalLayout.addWidget(self.button[button])

        ## Customization ==

        ## Layout ==
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addItem(spacerItem)
        
class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        ## Initialization ==
        self.setObjectName("toolbar")
        self.button = {}
        toolbarButtons = ("HomeButton", "AddExpenseBank",
        "AddRevenueBank", "AddAccBank",
        "RemoveAccBank", "AddAccCC",
        "RemoveAccCC", "AddRevenueCC",
        "Transfer", "EditTransfer")

        ## Creation ==
        for button in toolbarButtons:
            self.button[button] = QtWidgets.QAction(parent, objectName=button)
            icon = QtGui.QIcon()
            iconPath = "Icons/" + button + ".png"
            icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.button[button].setIcon(icon)
            self.addAction(self.button[button])

        ## Customization ==
        self.button["HomeButton"].triggered.connect(self.goToHome)
        self.button["AddExpenseBank"].triggered.connect(self.addTransaction)
        self.button["AddRevenueBank"].triggered.connect(self.goToHome)
        self.button["AddAccBank"].triggered.connect(self.goToHome)
        self.button["RemoveAccBank"].triggered.connect(self.goToHome)
        self.button["AddAccCC"].triggered.connect(self.goToHome)
        self.button["RemoveAccCC"].triggered.connect(self.goToHome)
        self.button["AddRevenueCC"].triggered.connect(self.goToHome)
        self.button["Transfer"].triggered.connect(self.goToHome)
        self.button["EditTransfer"].triggered.connect(self.goToHome)

        ## Layout ==

    def goToHome(self):
        self.parent.stackFrame.setCurrentIndex(0)
    
    def addTransaction(self):
        wind = NewWindows.Transaction(self)
        wind.show()

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        ## Initialization ==
        self.setGeometry(QtCore.QRect(0,0,1315,21))
        self.setObjectName("menubar")

        ## Creation ==
        ## Customization ==
        ## Layout ==

class SideButton(QtWidgets.QPushButton):
    def __init__(self, pageNumber, parent, text = ""):
        super().__init__(parent)
        self.parent = parent
        self.pageNumber = pageNumber
        self.setText(text)
        self.clicked.connect(self.goTo)
        
    def goTo(self):
        self.parent.stackFrame.setCurrentIndex(self.pageNumber)