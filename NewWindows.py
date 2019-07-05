from PySide2 import QtCore, QtGui, QtWidgets

class Transaction(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
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
        accOptions = list(self.caller.mainWin.allAcc.accountsObjs.keys())
        del accOptions[0]
        self.accountCombo.addItems(accOptions)
        
        catOptions = list(self.caller.mainWin.allCategories.category.keys())
        self.categoryCombo.addItems(catOptions)

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
            options = list(self.caller.mainWin.allAcc.accountsObjs.keys())
        else:
            options = list(self.caller.mainWin.allAcc.creditCardObjs.keys())
        del options[0]
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
        
    def getInputs(self):
        self.inputs['NewAcc'] = self.newEdit.text()
        if self.accRadio.isChecked():
            self.inputs['AccType'] = 'bank'
        else: 
            self.inputs['AccType'] = 'creditCard'
        self.accept()