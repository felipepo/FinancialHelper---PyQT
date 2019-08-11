from PySide2 import QtCore, QtGui, QtWidgets
import copy

class Create(QtWidgets.QDialog):
    def __init__(self, parent, options):
        super().__init__()
        self.resize(303, 131)
        self.setWindowTitle('Transferência')
        self.setObjectName("TransferWindow")
        self.inputs = {}
        self.options = list(options.keys())
        del self.options[0]
        self.optDict = options
        self.count_change = 0
        ## Initialization ==
        ## Creation ==
        self.origin_label = QtWidgets.QLabel(self, objectName="origin_label", text="Origem")
        self.destin_label = QtWidgets.QLabel(self, objectName="destin_label", text="Destino")
        self.date_label = QtWidgets.QLabel(self, objectName="date_label", text="Data")
        self.value_label = QtWidgets.QLabel(self, objectName="value_label", text="Valor (R$)")
        self.sourceCombo = QtWidgets.QComboBox(self, objectName="sourceCombo")
        self.destCombo = QtWidgets.QComboBox(self, objectName="destCombo")
        self.valueEdit = QtWidgets.QLineEdit(self, objectName="valueEdit", placeholderText="00.0", alignment=QtCore.Qt.AlignCenter)
        self.dateEdit = QtWidgets.QDateEdit(self, date=QtCore.QDate.currentDate(), objectName="dateEdit")
        self.value_available_label = QtWidgets.QLabel(self, objectName="value_available_label")
        self.OK = QtWidgets.QPushButton(self, objectName="OK", text="OK")

        ## Customization ==
        self.origin_label.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.destin_label.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.date_label.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.value_label.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")

        self.dateEdit.setCalendarPopup(True)
        self.sourceCombo.addItems(self.options)
        self.ExcludeInputs()
        self.OK.clicked.connect(self.getInputs)
        self.valueEdit.textChanged.connect(self.numberEntered)

        self.sourceCombo.currentIndexChanged.connect(self.ExcludeInputs)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy)

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.addWidget(self.origin_label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.destin_label, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.sourceCombo, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.destCombo, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.value_label, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.date_label, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.valueEdit, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.dateEdit, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.value_available_label, 4, 0, 1, 1, alignment = QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.OK, 4, 1, 1, 1)

    def ExcludeInputs(self):
        self.destCombo.clear()
        textToExclude = self.sourceCombo.currentText()
        index  = self.options.index(textToExclude)
        tempOptions = self.options[:]
        del tempOptions[index]
        self.destCombo.addItems(tempOptions)
        strToWrite = "Disponível: R$ {}".format(self.optDict[textToExclude])
        self.value_available_label.setText(strToWrite)

    def shift(self, input):
        try:
            dotPost = -2
            input = input.replace('.','')
        except:
            dotPost = -2
        result =  '{}.{}'.format(input[:dotPost], input[dotPost:])
        if result[0] == '0':
            result = result[1:]
        if result[0] == '.':
            result = "0" + result
        return result

    def numberEntered(self):
        self.count_change += 1
        if self.count_change < 2:
            currText = self.valueEdit.text()
            shiftedText = self.shift(currText)
            self.valueEdit.setText(shiftedText)
            if shiftedText == currText:
                self.count_change -= 1
        else:
            self.count_change = 0

    def getInputs(self):
        self.inputs['srcName'] = self.sourceCombo.currentText()
        self.inputs['dstName'] = self.destCombo.currentText()
        self.inputs['Date'] = self.dateEdit.date().toString('dd/MM/yyyy')
        self.inputs['Value'] = float(self.valueEdit.text())
        self.accept()

if __name__ == "__main__":
    financHelper = QtWidgets.QApplication([])
    parent = QtWidgets.QFrame()
    accTotal = {
        "Todas": 30,
        "Debit1": 10,
        "Debit2": 20
    }
    wind = Create(parent, accTotal)
    if wind.exec_():
        print(wind.inputs)
    wind.show()
    financHelper.exec_()