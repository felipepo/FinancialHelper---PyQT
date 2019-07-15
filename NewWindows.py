from PySide2 import QtCore, QtGui, QtWidgets
import copy
import unidecode
import Funs

class Transaction(QtWidgets.QDialog):
    def __init__(self, parent,debitOptions,creditOptions,CAToptions, transData={}):
        super().__init__(parent)
        self.debitOptions = debitOptions
        self.creditOptions = creditOptions
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
        self.debitRadio = QtWidgets.QRadioButton(self, checked=True, objectName="debitRadio", text="Conta")
        self.CCRadio = QtWidgets.QRadioButton(self, objectName="CCRadio", text="Cartão")
        self.groupBox = QtWidgets.QGroupBox(self, objectName="groupBox", title="Tipo de Transação")
        self.revenueRadio = QtWidgets.QRadioButton(self.groupBox, objectName="revenueRadio", text="Receita")
        self.expenseRadio = QtWidgets.QRadioButton(self.groupBox, checked=True, objectName="expenseRadio", text="Despesa")

        ## Customization ==
        self.accountCombo.addItems(self.debitOptions)        
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
        self.debitRadio.toggled.connect(self.accTypeSwitch)
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
                self.debitRadio.setChecked(True)
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
        self.gridLayout.addWidget(self.debitRadio, 4, 2, 1, 1)
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
        self.CCRadio.setChecked(not self.debitRadio.isChecked())
        self.UpdateAccounts()

    def CCTypeSwitch(self):
        self.debitRadio.setChecked(not self.CCRadio.isChecked())
        self.UpdateAccounts()

    def UpdateAccounts(self):
        self.accountCombo.clear()
        if self.debitRadio.isChecked():
            options = self.debitOptions
        else:
            options = self.creditOptions
        self.accountCombo.addItems(options)

    def getInputs(self):
        try:
            self.inputs['Category'] = self.categoryCombo.currentText()
            self.inputs['Date'] = self.dateEdit.date().toString('dd/MM/yyyy')
            self.inputs['AccName'] = self.accountCombo.currentText()
            self.inputs['Comment'] = self.commentEdit.text()
            if self.debitRadio.isChecked():
                self.inputs['AccType'] = 1
            else: 
                self.inputs['AccType'] = 2
            if self.expenseRadio.isChecked():
                self.inputs['Value'] = float("-" + self.valueEdit.text())
            else:
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
        self.resize(306, 227)

        ## Creation ==
        self.OK = QtWidgets.QPushButton(self, text="OK", objectName="OK")
        self.CCRadio = QtWidgets.QRadioButton(self, text="Cartão de Crédito", objectName="CCRadio")
        self.newEdit = QtWidgets.QLineEdit(self, objectName="newEdit", alignment=QtCore.Qt.AlignCenter)
        self.debitRadio = QtWidgets.QRadioButton(self, text="Conta", objectName="debitRadio")
        self.nameLbl = QtWidgets.QLabel(self, text="Nome", objectName="nameLbl", alignment=QtCore.Qt.AlignRight)
        self.initialValueLbl = QtWidgets.QLabel(self, objectName="initialValueLbl", text="Valor Inicial (R$)")
        self.initialValueEdit = QtWidgets.QLineEdit(self, objectName="newEdit", placeholderText="00.0", alignment=QtCore.Qt.AlignCenter)
        self.groupBox = QtWidgets.QGroupBox(self, objectName="groupBox", title="Fatura")
        self.closingDayLbl = QtWidgets.QLabel(self.groupBox, objectName="closingDayLbl", text="Dia de Fechamento")
        self.closingDayEdit = QtWidgets.QLineEdit(self.groupBox, objectName="newEdit", placeholderText="00", alignment=QtCore.Qt.AlignCenter)
        self.dueDatLbl = QtWidgets.QLabel(self.groupBox, objectName="dueDatLbl", text="Dia de Vencimento")
        self.dueDatEdit = QtWidgets.QLineEdit(self.groupBox, objectName="newEdit", placeholderText="00", alignment=QtCore.Qt.AlignCenter)
        self.limitLbl = QtWidgets.QLabel(self, objectName="limitLbl", text="Limite (R$)", alignment=QtCore.Qt.AlignRight)
        self.limitEdit = QtWidgets.QLineEdit(self, objectName="limitEdit", placeholderText="00.0", alignment=QtCore.Qt.AlignCenter)
        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        ## Customization ==
        self.debitRadio.setChecked(True)
        self.groupBox.hide()
        self.nameLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.initialValueLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.closingDayLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.dueDatLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.limitLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.OK.clicked.connect(self.getInputs)
        self.newEdit.setFocus()

        self.debitRadio.toggled.connect(self.accTypeSwitch)

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.addWidget(self.debitRadio, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.CCRadio, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.nameLbl, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.newEdit, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.initialValueLbl, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.initialValueEdit, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 3, 0, 1, 2)
        self.gridLayout.addItem(self.spacerItem, 3, 0, 1, 2)
        self.gridLayout.addWidget(self.OK, 4, 1, 1, 1)

        self.groupLayout = QtWidgets.QGridLayout(self.groupBox, objectName="groupLayout")
        self.groupLayout.addWidget(self.limitLbl, 0, 0, 1, 1)
        self.groupLayout.addWidget(self.limitEdit, 0, 1, 1, 1)
        self.groupLayout.addWidget(self.closingDayLbl, 1, 0, 1, 1)
        self.groupLayout.addWidget(self.closingDayEdit, 1, 1, 1, 1)
        self.groupLayout.addWidget(self.dueDatLbl, 2, 0, 1, 1)
        self.groupLayout.addWidget(self.dueDatEdit, 2, 1, 1, 1)
             
    def accTypeSwitch(self):
        self.CCRadio.setChecked(not self.debitRadio.isChecked())
        self.HideShowBill()

    def HideShowBill(self):
        if self.debitRadio.isChecked():
            self.groupBox.hide()
        else:
            self.groupBox.show()
   
    def getInputs(self):
        try:
            self.inputs['NewAcc'] = self.newEdit.text()
            self.inputs['InitialValue'] = float(self.initialValueEdit.text())
            if self.debitRadio.isChecked():
                self.inputs['AccType'] = 'bank'
            else: 
                self.inputs['AccType'] = 'creditCard'
                self.inputs['LimitValue'] = float(self.limitEdit.text())
                self.inputs['DueDay'] = int(self.dueDatEdit.text())
                self.inputs['ClosingDay'] = int(self.closingDayEdit.text())
            self.accept()
        except:
            print('Números errados')

class RemoveAccount(QtWidgets.QDialog):
    def __init__(self,parent, debitOptions, creditOptions):
        super().__init__()
        self.mainWin = parent
        self.setWindowTitle("Remover Conta")
        self.inputs = {}
        self.resize(237,90)
        self.setObjectName("RemoveAccount")

        ## Initialization ==
        self.debitOptions = debitOptions
        self.creditOptions = creditOptions
        
        ## Creation ==
        self.nameLbl = QtWidgets.QLabel(self, objectName="nameLbl", text="Nome", alignment=QtCore.Qt.AlignRight)
        self.OK = QtWidgets.QPushButton(self, objectName="OK", text="OK")
        self.debitRadio = QtWidgets.QRadioButton(self, objectName="debitRadio", text="Conta")
        self.CCRadio = QtWidgets.QRadioButton(self, objectName="CCRadio", text="Cartão de Crédito")
        self.comboBox = QtWidgets.QComboBox(self, objectName="comboBox")

        ## Customization ==
        self.nameLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.debitRadio.setChecked(True)
        self.comboBox.addItems(self.debitOptions)  
        self.OK.clicked.connect(self.getInputs)

        self.debitRadio.toggled.connect(self.accTypeSwitch)

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.addWidget(self.debitRadio, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.CCRadio, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.nameLbl, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.OK, 2, 1, 1, 1)

    def accTypeSwitch(self):
        self.CCRadio.setChecked(not self.debitRadio.isChecked())
        self.ChangeOptions()

    def ChangeOptions(self):
        self.comboBox.clear()
        if self.debitRadio.isChecked():
            options = self.debitOptions
        else:
            options = self.creditOptions
        self.comboBox.addItems(options)
   
    def getInputs(self):
        try:
            self.inputs['AccName'] = self.comboBox.currentText()
            if self.debitRadio.isChecked():
                self.inputs['AccType'] = 'bank'
            else: 
                self.inputs['AccType'] = 'creditCard'
            self.accept()
        except:
            print('Números errados')

class TransferWindow(QtWidgets.QDialog):
    def __init__(self, parent, options):
        super().__init__()
        self.resize(303, 131)
        self.setWindowTitle('Transferência')
        self.setObjectName("TransferWindow")
        self.inputs = {}
        self.options = options
        ## Initialization ==
        ## Creation ==
        self.originLbl = QtWidgets.QLabel(self, objectName="originLbl", text="Origem")
        self.destinLbl = QtWidgets.QLabel(self, objectName="destinLbl", text="Destino")
        self.dateLbl = QtWidgets.QLabel(self, objectName="dateLbl", text="Data")
        self.valueLbl = QtWidgets.QLabel(self, objectName="valueLbl", text="Valor (R$)")
        self.sourceCombo = QtWidgets.QComboBox(self, objectName="sourceCombo")
        self.destCombo = QtWidgets.QComboBox(self, objectName="destCombo")
        self.valueEdit = QtWidgets.QLineEdit(self, objectName="valueEdit", placeholderText="00.0", alignment=QtCore.Qt.AlignCenter)
        self.dateEdit = QtWidgets.QDateEdit(self, date=QtCore.QDate.currentDate(), objectName="dateEdit")
        self.OK = QtWidgets.QPushButton(self, objectName="OK", text="OK")

        ## Customization ==
        self.originLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.destinLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.dateLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.valueLbl.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")

        self.dateEdit.setCalendarPopup(True)
        self.sourceCombo.addItems(self.options)  
        self.ExcludeInputs()
        self.OK.clicked.connect(self.getInputs)

        self.sourceCombo.currentIndexChanged.connect(self.ExcludeInputs)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy)

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.addWidget(self.originLbl, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.destinLbl, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.sourceCombo, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.destCombo, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.valueLbl, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.dateLbl, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.valueEdit, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.dateEdit, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.OK, 4, 1, 1, 1)

    def ExcludeInputs(self):
        self.destCombo.clear()
        textToExclude = self.sourceCombo.currentText()
        index  = self.options.index(textToExclude)
        tempOptions = self.options[:]
        del tempOptions[index]
        self.destCombo.addItems(tempOptions)

    def getInputs(self):
        # try:
            self.inputs['srcName'] = self.sourceCombo.currentText()
            self.inputs['dstName'] = self.destCombo.currentText()
            self.inputs['Date'] = self.dateEdit.date().toString('dd/MM/yyyy')
            self.inputs['Value'] = float(self.valueEdit.text())
            self.accept()
        # except:
        #     print('Números errados')

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