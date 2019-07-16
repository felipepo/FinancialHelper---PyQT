from PySide2 import QtCore, QtGui, QtWidgets
import copy
import unidecode
import Funs

class Create(QtWidgets.QDialog):
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