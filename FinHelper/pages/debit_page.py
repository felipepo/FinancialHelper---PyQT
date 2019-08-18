from PySide2 import QtWidgets, QtCore, QtGui
from ..utilities import cards, plotting, funs
from decimal import Decimal

class SetValue(QtWidgets.QGroupBox):
    def __init__(self, parentPage):
        ## Initialization ==
        super().__init__(parentPage)
        self.mainWin = parentPage.mainWin
        self.cardArea = parentPage.cardArea
        self.setTitle("Conta")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setObjectName("SetValueGroup")
        self.count_change = 0

        ## Creation ==
        self.accName = QtWidgets.QLabel(self, text="Nome", objectName="NameLbl")
        self.nameDropDown = QtWidgets.QComboBox(self, objectName="nameDropDown")
        self.valLbl = QtWidgets.QLabel(self, text="Definir valor atual", objectName="valLbl")
        self.finalValue = QtWidgets.QLineEdit(self, placeholderText="00.0", alignment=QtCore.Qt.AlignCenter, objectName="finalValue")
        self.applyButton = QtWidgets.QPushButton(self, text="Aplicar", objectName="button2")

        ## Customization ==
        self.applyButton.clicked.connect(self.SetFinalValue)
        options = self.mainWin.DataBase.AllAccounts["debit"][:]
        self.nameDropDown.addItems(options)
        self.nameDropDown.currentIndexChanged.connect(self.UpdateEditBox)
        self.UpdateEditBox()

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.finalValue.setSizePolicy(sizePolicy)
        self.nameDropDown.setSizePolicy(sizePolicy)

        self.finalValue.textChanged.connect(lambda state, targetEdit=self.finalValue: self.numberEntered(targetEdit))

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.addWidget(self.accName,0,0,1,1)
        self.gridLayout.addWidget(self.nameDropDown,0,1,1,1)
        self.gridLayout.addWidget(self.valLbl,1,0,1,1)
        self.gridLayout.addWidget(self.finalValue,1,1,1,1)
        self.gridLayout.addWidget(self.applyButton,2,1,1,1)

    def UpdateEditBox(self):
        currAcc = self.nameDropDown.currentText()
        if currAcc:
            currAccTotal = self.mainWin.DataBase.Totals['debit'][currAcc]
            self.finalValue.setText( str(round(Decimal(currAccTotal), 2)) )

    def SetFinalValue(self):
        accName = self.nameDropDown.currentText()
        Acc_ID = self.mainWin.DataBase.acc_tbl.readByUnique(1, accName)
        Catg_ID = self.mainWin.DataBase.category_tbl.readByName("Outros")
        diffValue = float(self.finalValue.text()) - self.mainWin.DataBase.Totals["debit"][accName]
        if diffValue != 0:
            transData = {
                "Catg_ID": Catg_ID[0],
                "Category": "Outros",
                "AccType": 1,
                "AccName": accName,
                "Acc_ID": Acc_ID[0],
                "Date": QtCore.QDate.currentDate().toString('dd/MM/yyyy'),
                "Value": diffValue,
                "Comment": "Atualização do valor final"
            }
            transID = self.mainWin.DataBase.NewTransaction(transData)
            self.cardArea.AddCard(transData, transID)
            self.mainWin.updateInteface()

    def numberEntered(self, targetEdit):
        self.count_change += 1
        if self.count_change < 2:
            currText = targetEdit.text()
            shiftedText = funs.shift(currText)
            targetEdit.setText(shiftedText)
            if shiftedText == currText:
                self.count_change -= 1
        else:
            self.count_change = 0