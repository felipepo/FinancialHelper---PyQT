from PySide2 import QtCore, QtGui, QtWidgets
import copy
import Funs

class Create(QtWidgets.QDialog):
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
        self.valueEdit = QtWidgets.QLineEdit(self, placeholderText="00.0", alignment=QtCore.Qt.AlignCenter, objectName="valueEdit")
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
            if transData['AccType'] == 1:
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