from PySide2 import QtCore, QtGui, QtWidgets
import copy
import unidecode
import Funs

class New(QtWidgets.QDialog):
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
            self.inputs['Name'] = self.newEdit.text()
            self.inputs['Total'] = 0 if self.initialValueEdit.text() == "" else float(self.initialValueEdit.text())
            if self.debitRadio.isChecked():
                self.inputs['Type'] = 1
                self.inputs['Limit'] = None
                self.inputs['DueDay'] = None
                self.inputs['ClosingDay'] = None
            else: 
                self.inputs['Type'] = 2
                self.inputs['Limit'] = 0 if self.limitEdit.text() == "" else float(self.limitEdit.text())
                self.inputs['DueDay'] = 0 if self.dueDatEdit.text() == "" else int(self.dueDatEdit.text())
                self.inputs['ClosingDay'] = 0 if self.closingDayEdit.text() == "" else int(self.closingDayEdit.text())
            self.accept()
        except:
            print('Números errados')

class Remove(QtWidgets.QDialog):
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
            self.inputs['Name'] = self.comboBox.currentText()
            self.inputs['Type'] = 1 if self.debitRadio.isChecked() else 2
            self.accept()
        except:
            print('Números errados')