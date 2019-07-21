from PySide2 import QtWidgets, QtCore, QtGui
import HomePage
import AccPage
from DialogWindows import AccountWindow
from DialogWindows import CategoryWindow
from DialogWindows import TransactionWindow
from DialogWindows import TransferWindow
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

        ## Creation ==      
        if SimulateData == 1:
            self.DataBase = SQLDB.Create(1)
            self.DataBase.simulateData()
        else:
            self.DataBase = SQLDB.Create(2)

        firstRun = self.DataBase.CategoryTable.readAll()
        if not firstRun:
            # CreteDefaultCategories()
            defaultCatg = Funs.generateCatg(rand="off")
            for iCatg in list(defaultCatg.keys()):
                self.DataBase.CategoryTable.insert(iCatg, defaultCatg[iCatg])
            
        self.styleObj = Style.Create(self.DataBase.CategoryTable)
        self.setStyleSheet(self.styleObj.InterfaceStyle)
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

    def UpdateStyle(self):
        pass

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).closeEvent(*args, **kwargs)
        self.DataBase.close_db()

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
            self.button[button].setObjectName(button)
            self.verticalLayout.addWidget(self.button[button])

        ## Customization ==

        ## Layout ==
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addItem(spacerItem)
        
class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWin = parent
        ## Initialization ==
        self.setObjectName("toolbar")
        self.button = {}
        #toolbarButtons = ("HomeButton", "AddExpenseBank",
        #"AddRevenueBank", "AddAccBank",
        #"RemoveAccBank", "AddAccCC",
        #"RemoveAccCC", "AddRevenueCC",
        #"Transfer", "EditTransfer")
        toolbarButtons = ("HomeButton", "AddExpenseBank",
        "AddAccBank",
        "RemoveAccBank",
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
        #self.button["AddRevenueBank"].triggered.connect(self.goToHome)
        self.button["AddAccBank"].triggered.connect(self.addAccount)
        self.button["RemoveAccBank"].triggered.connect(self.removeAccount)
        #self.button["AddAccCC"].triggered.connect(self.goToHome)
        #self.button["RemoveAccCC"].triggered.connect(self.goToHome)
        #self.button["AddRevenueCC"].triggered.connect(self.goToHome)
        self.button["Transfer"].triggered.connect(self.transfer)
        self.button["EditTransfer"].triggered.connect(self.debug)

        ## Layout ==

    def goToHome(self):
        self.mainWin.stackFrame.setCurrentIndex(0)
    
    def addTransaction(self):
        mayProceed = False
        while mayProceed == False:
            debitOptions = self.mainWin.DataBase.AllAccounts["debit"]
            creditOptions = self.mainWin.DataBase.AllAccounts["credit"]
            catgOptions = self.mainWin.DataBase.AllCategories
            wind = TransactionWindow.Create(self, debitOptions, creditOptions, catgOptions)
            if wind.exec_():
                targetCatg = self.mainWin.DataBase.CategoryTable.readByName(wind.inputs["Category"])
                targetAcc = self.mainWin.DataBase.AccountTable.readByUnique(wind.inputs["AccType"], wind.inputs["AccName"])
                transInfo = {"Catg_ID":targetCatg[0], "Acc_ID":targetAcc[0], "Comment":wind.inputs["Comment"], "Value":wind.inputs["Value"], "Date":wind.inputs["Date"]}
                transID = self.mainWin.DataBase.NewTransaction(transInfo)
                if transID != 'Error':
                    self.mainWin.DataBase.ReGetValues()
                    if wind.inputs['AccType'] == 1:
                        self.mainWin.homePage.debitGroupBox.UpdateValue()
                    else:
                        self.mainWin.homePage.creditGroupBox.UpdateValue()
                    mayProceed = True
                    self.mainWin.accPage.cardArea.AddCard(wind.inputs, transID)
                else:
                    print('Problema na conta')
            else: 
                mayProceed = True

    def transfer(self):
        mayProceed = False
        while mayProceed == False:
            debitOptions = self.mainWin.DataBase.AllAccounts["debit"][:]
            wind = TransferWindow.Create(self, debitOptions)
            if wind.exec_():
                transferCatg = self.mainWin.DataBase.CategoryTable.readByName("Transferência")
                srcData = self.mainWin.DataBase.AccountTable.readByUnique(1, wind.inputs["srcName"])
                dstData = self.mainWin.DataBase.AccountTable.readByUnique(1, wind.inputs["dstName"])
                sourceData = {
                    'Catg_ID':transferCatg[0],
                    'Acc_ID':srcData[0],
                    'Category':"Transferência",
                    'Date':wind.inputs['Date'],
                    'AccName':wind.inputs['srcName'],
                    'Comment':'Transferência p/ '+wind.inputs['dstName'],
                    'AccType':1,
                    'Value':wind.inputs['Value']*(-1)
                }
                destData = {
                    'Catg_ID':transferCatg[0],
                    'Acc_ID':dstData[0],
                    'Category':"Transferência",
                    'Date':wind.inputs['Date'],
                    'AccName':wind.inputs['dstName'],
                    'Comment':'Transferência de '+wind.inputs['srcName'],
                    'AccType':1,
                    'Value':wind.inputs['Value']
                }
                transID = self.mainWin.DataBase.NewTransaction(sourceData)
                if transID != 'Error':
                    self.mainWin.accPage.cardArea.AddCard(sourceData, transID)
                else:
                    print('Problema na conta')
                transID = self.mainWin.DataBase.NewTransaction(destData)
                if transID != 'Error':
                    self.mainWin.DataBase.ReGetValues()
                    self.mainWin.homePage.debitGroupBox.UpdateValue()
                    mayProceed = True
                    self.mainWin.accPage.cardArea.AddCard(destData, transID)
                else:
                    print('Problema na conta')
            else: 
                mayProceed = True

    def addAccount(self):
        mayProceed = False
        while mayProceed == False:
            wind = AccountWindow.New(self)
            if wind.exec_():
                addedFlag = self.mainWin.DataBase.AccountTable.insert(wind.inputs)
                if addedFlag:
                    mayProceed = True
                    self.mainWin.DataBase.ReGetValues()
                    if wind.inputs['Type'] == 1:
                        self.mainWin.homePage.debitGroupBox.comboBox.addItem(wind.inputs['Name'])
                        self.mainWin.homePage.debitGroupBox.UpdateValue()
                    else:
                        self.mainWin.homePage.creditGroupBox.comboBox.addItem(wind.inputs['Name'])
                        self.mainWin.homePage.creditGroupBox.UpdateValue()
                else:
                    print('acc ja existe')
            else: 
                mayProceed = True

    def removeAccount(self):
        mayProceed = False
        while mayProceed == False:
            debitOptions = self.mainWin.DataBase.AllAccounts["debit"]
            creditOptions = self.mainWin.DataBase.AllAccounts["credit"]
            wind = AccountWindow.Remove(self, debitOptions, creditOptions)
            if wind.exec_():
                removedFlag = self.mainWin.DataBase.AccountTable.deleteByUnique(wind.inputs['Type'], wind.inputs['Name'])
                if removedFlag:
                    mayProceed = True
                    self.mainWin.DataBase.ReGetValues()
                    if wind.inputs['Type'] == 1:
                        itemToRemove = debitOptions.index(wind.inputs['Name']) + 1
                        self.mainWin.homePage.debitGroupBox.comboBox.removeItem(itemToRemove)
                    else:
                        itemToRemove = creditOptions.index(wind.inputs['Name']) + 1
                        self.mainWin.homePage.creditGroupBox.comboBox.removeItem(itemToRemove)
                else:
                    print('acc ja existe')
            else: 
                mayProceed = True

    def debug(self):
        Funs.debugAccounts(self.mainWin.allAcc)

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWin = parent
        ## Initialization ==
        self.button = {}
        #self.setGeometry(QtCore.QRect(0,0,1315,21))
        self.setObjectName("menubar")
        FileButtons = {"Save", "Save As..."}
        EditButtons = {"Categorias"}
        AccButtons = {"Adicionar", "Remover", "Renomear", "Definir Valor Atual"}
        ToolsButtons = {"Exportar"}

        ## Creation ==
        self.menuFile = QtWidgets.QMenu(self, objectName="MenuFile", title="File")
        for button in FileButtons:
            self.button[button] = QtWidgets.QAction(parent, objectName=button, text=button)
            self.menuFile.addAction(self.button[button])
        self.addAction(self.menuFile.menuAction())
        
        self.menuEdit = QtWidgets.QMenu(self, objectName="MenuEdit", title="Editar")
        for button in EditButtons:
            self.button[button] = QtWidgets.QAction(parent, objectName=button, text=button)
            self.menuEdit.addAction(self.button[button])
        self.addAction(self.menuEdit.menuAction())
        
        self.menuAcc = QtWidgets.QMenu(self, objectName="menuAcc", title="Contas")
        for button in AccButtons:
            self.button[button] = QtWidgets.QAction(parent, objectName=button, text=button)
            self.menuAcc.addAction(self.button[button])
        self.addAction(self.menuAcc.menuAction())
        
        self.menuTools = QtWidgets.QMenu(self, objectName="menuTools", title="Ferramentas")
        for button in ToolsButtons:
            self.button[button] = QtWidgets.QAction(parent, objectName=button, text=button)
            self.menuTools.addAction(self.button[button])
        self.addAction(self.menuTools.menuAction())
        
        ## Customization ==
        self.button["Save"].triggered.connect(self.save)
        self.button["Categorias"].triggered.connect(self.configCategory)
        ## Layout ==

    def save(self):
        Funs.saveData('Data', self.mainWin.allAcc)
        Funs.saveData('Categories', self.mainWin.allCategories)
        self.mainWin.styleObj.createQSSFile()
        print("Saved")
    
    def configCategory(self):
        wind = CategoryWindow.Create(self.mainWin)
        if wind.exec_():
            self.mainWin.styleObj.InterfaceStyle = wind.inputs["EditData"]
            if "AppendData" in wind.inputs:
                self.mainWin.styleObj.appendStyle(wind.inputs["AppendData"]["StyleFrame"])
                self.mainWin.styleObj.appendStyle(wind.inputs["AppendData"]["StyleLabel"])
                self.mainWin.DataBase.CategoryTable.insert(wind.inputs["AppendData"]["Name"], wind.inputs["AppendData"]["rgb"])
            if "RemoveData" in wind.inputs:
                removedCatg = wind.inputs["RemoveData"]
                self.mainWin.DataBase.RemoveCategory(removedCatg)
                self.mainWin.styleObj.removeStyle(removedCatg)
            if "RenameData" in wind.inputs:
                oldName = wind.inputs["RenameData"]['oldName']
                newName = wind.inputs["RenameData"]['newName']
                self.mainWin.styleObj.renameStyle(oldName, newName)
                for iCatg in self.mainWin.DataBase.CategoryTable.get_ids():
                    currCatg = self.mainWin.DataBase.CategoryTable.readById(iCatg)
                    if currCatg[1] == oldName:
                        self.mainWin.DataBase.CategoryTable.updateById(iCatg, newName, currCatg[2])
            self.mainWin.setStyleSheet(self.mainWin.styleObj.InterfaceStyle)
            self.mainWin.styleObj.createQSSFile()
            self.mainWin.setStyle(self.mainWin.style())
            self.mainWin.DataBase.ReGetValues()
            self.mainWin.accPage.cardArea.UpdateALLCards()

class SideButton(QtWidgets.QPushButton):
    def __init__(self, pageNumber, parent, text = ""):
        super().__init__(parent)
        self.mainWin = parent
        self.pageNumber = pageNumber
        self.setText(text)
        self.clicked.connect(self.goTo)
        
    def goTo(self):
        self.mainWin.stackFrame.setCurrentIndex(self.pageNumber)