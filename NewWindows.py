from PySide2 import QtCore, QtGui, QtWidgets
import copy
import unidecode
import Funs

class Transaction(QtWidgets.QDialog):
    def __init__(self, parent,ACCoptions,CCoptions,CAToptions, transData={}):
        super().__init__(parent)
        self.ACCoptions = ACCoptions
        self.CCoptions = CCoptions
        self.CAToptions = CAToptions
        self.caller = parent
        ## Initialization ==
        self.setObjectName("Dialog")
        self.resize(391, 232)
        self.inputs = {}

        ## Creation ==
        self.valueLbl = QtWidgets.QLabel(self, text="Valor", objectName="valueLbl")
        self.categoryLbl = QtWidgets.QLabel(self, text="Categoria", objectName="categoryLbl")
        self.dateLbl = QtWidgets.QLabel(self, text="Data", objectName="dateLbl")
        self.commentLbl = QtWidgets.QLabel(self, text="Comentário", objectName="commentLbl")
        self.accLbl = QtWidgets.QLabel(self, text="Fonte/Destino", objectName="accLbl")
        self.valueEdit = QtWidgets.QLineEdit(self, objectName="valueEdit")
        self.categoryCombo = QtWidgets.QComboBox(self, objectName="categoryCombo")
        self.dateEdit = QtWidgets.QDateEdit(self, date=QtCore.QDate.currentDate(), objectName="dateEdit")
        self.accountCombo = QtWidgets.QComboBox(self, objectName="accountCombo")
        self.commentEdit = QtWidgets.QLineEdit(self, objectName="commentEdit")
        self.okButton = QtWidgets.QPushButton(self, objectName="okButton", text="OK")
        self.accRadio = QtWidgets.QRadioButton(self, checked=True, objectName="accRadio", text="Conta")
        self.CCRadio = QtWidgets.QRadioButton(self, objectName="CCRadio", text="Cartão")
        self.groupBox = QtWidgets.QGroupBox(self, objectName="groupBox", title="Tipo de Transação")
        self.revenueRadio = QtWidgets.QRadioButton(self.groupBox, objectName="revenueRadio", text="Receita")
        self.expenseRadio = QtWidgets.QRadioButton(self.groupBox, checked=True, objectName="expenseRadio", text="Despesa")

        ## Customization ==
        self.accountCombo.addItems(self.ACCoptions)        
        self.categoryCombo.addItems(self.CAToptions)

        self.valueLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.categoryLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.dateLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.commentLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.accLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valueEdit.sizePolicy().hasHeightForWidth())
        self.valueEdit.setSizePolicy(sizePolicy)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commentEdit.sizePolicy().hasHeightForWidth())
        self.commentEdit.setSizePolicy(sizePolicy)

        self.okButton.clicked.connect(self.getInputs)
        self.dateEdit.setCalendarPopup(True)
        self.accRadio.toggled.connect(self.accTypeSwitch)
        self.CCRadio.toggled.connect(self.CCTypeSwitch)
        if transData:
            if "-" in str(transData['Value']):
                self.expenseRadio.setChecked(True)
                self.valueEdit.setText(str(transData['Value']*(-1)))
            else:
                self.revenueRadio.setChecked(True)
                self.valueEdit.setText(str(transData['Value']))
            self.commentEdit.setText(transData['Comment'])
            self.categoryCombo.setCurrentText(transData['Category'])
            if transData['AccType'] == "bank":
                self.accRadio.setChecked(True)
            else:
                self.CCRadio.setChecked(True)
            self.accountCombo.setCurrentText(transData['Account'])

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.setContentsMargins(-1, 4, -1, -1)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 4)
        self.gridLayout.addWidget(self.categoryLbl, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.dateLbl, 1, 2, 1, 2)
        self.gridLayout.addWidget(self.categoryCombo, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.dateEdit, 2, 2, 1, 2)
        self.gridLayout.addWidget(self.valueLbl, 3, 0, 1, 2)
        self.gridLayout.addWidget(self.accLbl, 3, 2, 1, 2)
        self.gridLayout.addWidget(self.valueEdit, 4, 0, 2, 2)
        self.gridLayout.addWidget(self.accRadio, 4, 2, 1, 1)
        self.gridLayout.addWidget(self.CCRadio, 4, 3, 1, 1)
        self.gridLayout.addWidget(self.accountCombo, 5, 2, 1, 2)
        self.gridLayout.addWidget(self.commentLbl, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.commentEdit, 7, 0, 1, 3)
        self.gridLayout.addWidget(self.okButton, 7, 3, 1, 1)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox, spacing=0, objectName="horizontalLayout")
        self.horizontalLayout.setContentsMargins(8, 0, 0, 3)
        self.horizontalLayout.addWidget(self.expenseRadio)
        self.horizontalLayout.addWidget(self.revenueRadio)

    def accTypeSwitch(self):
        self.CCRadio.setChecked(not self.accRadio.isChecked())
        self.UpdateAccounts()

    def CCTypeSwitch(self):
        self.accRadio.setChecked(not self.CCRadio.isChecked())
        self.UpdateAccounts()

    def UpdateAccounts(self):
        self.accountCombo.clear()
        if self.accRadio.isChecked():
            options = self.ACCoptions
        else:
            options = self.CCoptions
        self.accountCombo.addItems(options)

    def getInputs(self):
        try:
            self.inputs['Category'] = self.categoryCombo.currentText()
            self.inputs['Date'] = self.dateEdit.date().toString('dd/MM/yyyy')
            self.inputs['Account'] = self.accountCombo.currentText()
            self.inputs['Comment'] = self.commentEdit.text()
            if self.accRadio.isChecked():
                self.inputs['AccType'] = 'bank'
            else: 
                self.inputs['AccType'] = 'creditCard'
            if self.expenseRadio.isChecked():
                self.inputs['TransType'] = 'Expense'
                self.inputs['Value'] = float("-" + self.valueEdit.text())
            else:
                self.inputs['TransType'] = 'Revenue'
                self.inputs['Value'] = float(self.valueEdit.text())
            self.accept()
        except:
            print('problema na conta')

class AddAccount(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__()
        ## Initialization ==
        self.setObjectName("AddAccount")
        self.setWindowTitle("Nova Conta")
        self.inputs = {}
        self.resize(275, 90)

        ## Creation ==
        self.OK = QtWidgets.QPushButton(self, text="OK", objectName="OK")
        self.CCRadio = QtWidgets.QRadioButton(self, text="Cartão de Crédito", objectName="CCRadio")
        self.newEdit = QtWidgets.QLineEdit(self, objectName="newEdit")
        self.accRadio = QtWidgets.QRadioButton(self, text="Conta", objectName="accRadio")
        self.label = QtWidgets.QLabel(self, text="Nome", objectName="label")

        ## Customization ==
        self.accRadio.setChecked(True)
        self.label.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.OK.clicked.connect(self.getInputs)
        self.newEdit.setFocus()

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.addWidget(self.OK, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.CCRadio, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.newEdit, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.accRadio, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        
    def UpdateStyle(self):
        pass
        
    def getInputs(self):
        self.inputs['NewAcc'] = self.newEdit.text()
        if self.accRadio.isChecked():
            self.inputs['AccType'] = 'bank'
        else: 
            self.inputs['AccType'] = 'creditCard'
        self.accept()

class CategoryWindow(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__()
        self.mainWin = parent
        self.allCategories = parent.allCategories
        self.styleObj = copy.deepcopy(parent.styleObj)
        ## Initialization ==
        self.setObjectName('CategoryWindow')
        self.setWindowTitle("Configuração Categorias")
        self.resize(319, 256)
        self.setStyleSheet(self.styleObj.InterfaceStyle)

        ## Creation ==
        self.tabWidget = QtWidgets.QTabWidget(self, objectName="tabWidget")
        self.addTab = AddTab(self)
        self.removeTab = RemoveTab(self)
        self.renameTab = RenameTab(self)
        self.editTab = EditTab(self)
        self.apllyButton = QtWidgets.QPushButton(self, objectName="applyButton", text="Aplicar")
        self.exitButton = QtWidgets.QPushButton(self, objectName="exitButton", text="Sair")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        ## Customization ==
        self.tabWidget.addTab(self.addTab,'')
        self.tabWidget.addTab(self.removeTab,'')
        self.tabWidget.addTab(self.renameTab,'')
        self.tabWidget.addTab(self.editTab,'')
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.addTab), "Adicionar")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.editTab), "Editar Cor")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.renameTab), "Renomear")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.removeTab), "Remover")
        self.tabWidget.setCurrentIndex(0)

        self.exitButton.clicked.connect(self.Exit)
        self.apllyButton.clicked.connect(self.Apply)

        ## Layout == 
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 3)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.apllyButton, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.exitButton, 1, 2, 1, 1)

    def Apply(self):
        # Edit category color 
        self.mainWin.styleObj.InterfaceStyle = self.styleObj.InterfaceStyle

        # Append new Category
        if self.addTab.newEntry.text():
            self.mainWin.styleObj.appendStyle(self.addTab.getStyle())

        # Remove Category
        if self.removeTab.catCombo.currentText():
            self.mainWin.styleObj.removeStyle(self.removeTab.catCombo.currentText())
        
        # Rename Category
        if self.renameTab.newEntry.text():
            oldName = self.renameTab.catCombo.currentText()
            newName = self.renameTab.newEntry.text()
            self.mainWin.styleObj.renameStyle(oldName, newName)
            for iAcc in list(self.mainWin.allAcc.accountsObjs.keys()):
                for iTrans in list(self.mainWin.allAcc.accountsObjs[iAcc].transactions.keys()):
                    if self.mainWin.allAcc.accountsObjs[iAcc].transactions[iTrans].category == oldName:
                        self.mainWin.allAcc.accountsObjs[iAcc].transactions[iTrans].category = newName

            for iAcc in list(self.mainWin.allAcc.creditCardObjs.keys()):
                for iTrans in list(self.mainWin.allAcc.creditCardObjs[iAcc].transactions.keys()):
                    if self.mainWin.allAcc.creditCardObjs[iAcc].transactions[iTrans].category == oldName:
                        self.mainWin.allAcc.creditCardObjs[iAcc].transactions[iTrans].category = newName

        self.mainWin.setStyleSheet(self.mainWin.styleObj.InterfaceStyle)
        
        self.close()

    def Exit(self):
        self.close()

class AddTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setObjectName('AddTab')        
        ## Initialization ==
        self.rgb = ''

        ## Creation ==
        self.catLbl = QtWidgets.QLabel(self, objectName="catLbL", text="Categoria")
        self.newEntry = QtWidgets.QLineEdit(self, objectName="newEntry")
        self.colorLbl = QtWidgets.QLabel(self, objectName="colorLbl", text="Cor")
        self.showColor = QtWidgets.QLabel(self, objectName="-")
        self.cardTemplate = CardTemplate(self, {'Category':'','Value':'00.0','Date':'10/10/2010','Comment':'Template', 'Account':'Conta'})

        ## Customization ==
        self.newEntry.textChanged.connect(self.UpdateTemplate)

        self.showColor.mousePressEvent = self.GetColor

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        
        self.gridLayout.addWidget(self.catLbl, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.newEntry, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.colorLbl, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.showColor, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.cardTemplate, 3, 0, 1, 3)

    def UpdateTemplate(self):
        self.cardTemplate.categoryLbl.setText(self.newEntry.text())
        
    def GetColor(self, *args):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            rgb =  'rgb('+str(color.red())+', '+str(color.green())+', '+str(color.blue())+')'
            backRGB = 'background-color: '+rgb
            self.showColor.setStyleSheet(backRGB)
            self.cardTemplate.setStyleSheet(backRGB)
            self.rgb = rgb

    def getStyle(self):
        category = self.newEntry.text()
        styleDict = {
            'selectorStr':['QFrame', 'QLabel'],
            'idStr':[category, 'Color'+category],
            'classStr':["", ""],
            'descendantStr':["", ""],
            'childStr':["", ""],
            'propStr':[{}, {}],
            'propertyDic':{'background-color':self.rgb}
        }
        return styleDict

class RemoveTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setObjectName('RemoveTab')
        ## Initialization ==
        ## Creation ==
        self.catLbl = QtWidgets.QLabel(self, objectName="catLbL", text="Categoria")
        self.catCombo = QtWidgets.QComboBox(self, objectName="catCombo")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        ## Customization ==
        options = list(parent.allCategories.category.keys())
        options.insert(0,'')
        self.catCombo.addItems(options)

        ## Layout ==
        self.verticalLayout = QtWidgets.QVBoxLayout(self, objectName="verticalLayout")
        self.verticalLayout.addWidget(self.catLbl)
        self.verticalLayout.addWidget(self.catCombo)
        self.verticalLayout.addItem(spacerItem)
        
        
class RenameTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setObjectName('RenameTab')
        ## Initialization ==
        ## Creation ==
        self.catLbl = QtWidgets.QLabel(self, objectName="catLbL", text="Categoria")
        self.catCombo = QtWidgets.QComboBox(self, objectName="catCombo")
        self.newNameLbl = QtWidgets.QLabel(self, objectName="newNameLbl", text="Novo Nome")
        self.newEntry = QtWidgets.QLineEdit(self, objectName="newEntry")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        ## Customization ==
        options = list(parent.allCategories.category.keys())
        options.insert(0,'')
        self.catCombo.addItems(options)

        ## Layout ==
        self.verticalLayout = QtWidgets.QVBoxLayout(self, objectName="verticalLayout")
        self.verticalLayout.addWidget(self.catLbl)
        self.verticalLayout.addWidget(self.catCombo)
        self.verticalLayout.addWidget(self.newNameLbl)
        self.verticalLayout.addWidget(self.newEntry)
        self.verticalLayout.addItem(spacerItem)
        
class EditTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setObjectName('EditTab')
        ## Initialization ==
        ## Creation ==
        self.catLbl = QtWidgets.QLabel(self, objectName="catLbL", text="Categoria")
        self.catCombo = QtWidgets.QComboBox(self, objectName="catCombo")
        self.colorLbl = QtWidgets.QLabel(self, objectName="colorLbl", text="Cor")
        self.showColor = QtWidgets.QLabel(self)
        self.cardTemplate = CardTemplate(self, {'Category':'','Value':'00.0','Date':'10/10/2010','Comment':'Template', 'Account':'Conta'})

        ## Customization ==
        options = list(parent.allCategories.category.keys())
        self.catCombo.addItems(options)
        self.catCombo.currentIndexChanged.connect(self.UpdateTemplate)
        self.cardTemplate.setObjectName(unidecode.unidecode(self.catCombo.currentText()))
        self.UpdateTemplate()

        self.showColor.setMinimumSize(QtCore.QSize(24, 24))
        self.showColor.setMaximumSize(QtCore.QSize(24, 24))

        self.showColor.setObjectName('Color'+unidecode.unidecode(self.catCombo.currentText()))
        self.showColor.mousePressEvent = self.GetColor

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
                
        self.gridLayout.addWidget(self.catLbl, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.catCombo, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.colorLbl, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.showColor, 2, 1, 1, 1, alignment = QtCore.Qt.AlignLeft)
        self.gridLayout.addWidget(self.cardTemplate, 3, 0, 1, 3)

    def GetColor(self, *args):
        prevColor = self.showColor.palette().color(QtGui.QPalette.Base)
        color = QtWidgets.QColorDialog.getColor()
        prevRgb =  'rgb('+str(prevColor.red())+', '+str(prevColor.green())+', '+str(prevColor.blue())+')'
        prevBackRGB = 'background-color: '+prevRgb
        if color.isValid():
            rgb =  'rgb('+str(color.red())+', '+str(color.green())+', '+str(color.blue())+')'
            backRGB = 'background-color: '+rgb
            self.parent.styleObj.InterfaceStyle = self.parent.styleObj.InterfaceStyle.replace(prevBackRGB,backRGB)
            self.parent.setStyleSheet(self.parent.styleObj.InterfaceStyle)

    def UpdateTemplate(self):
        self.cardTemplate.categoryLbl.setText(self.catCombo.currentText())
        self.cardTemplate.setObjectName(unidecode.unidecode(self.catCombo.currentText()))
        self.cardTemplate.setStyle(self.cardTemplate.style())
        
        self.showColor.setObjectName('Color'+unidecode.unidecode(self.catCombo.currentText()))
        self.showColor.setStyle(self.cardTemplate.style())

class CardTemplate(QtWidgets.QFrame):
    def __init__(self, parent, transData):
        super().__init__(parent)
        ## Initialization ==
        self.setMinimumSize(QtCore.QSize(200, 100))
        self.setMaximumSize(QtCore.QSize(2000, 1000))
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

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        #self.gridLayout.setContentsMargins(3,3,3,3)

        self.gridLayout.addWidget(self.categoryLbl, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.dateLbl, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.currencyLbl, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.valueLbl, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.accLbl, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.commLbl, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.editButton, 2, 2, 1, 1, alignment = QtCore.Qt.AlignRight)