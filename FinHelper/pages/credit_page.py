from PySide2 import QtWidgets, QtCore, QtGui
from ..utilities import cards, plotting, funs
from decimal import Decimal

class SetValue(QtWidgets.QGroupBox):
    def __init__(self, parentPage):
        ## Initialization ==
        super().__init__(parentPage)
        self.mainWin = parentPage.mainWin
        self.cardArea = parentPage.cardArea
        self.setTitle("Cartão de Crédito")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setObjectName("SetValueGroup")
        self.count_change = 0

        ## Creation ==
        self.accName = QtWidgets.QLabel(self, text="Nome", objectName="NameLbl")
        self.nameDropDown = QtWidgets.QComboBox(self, objectName="nameDropDown")
        self.valLbl = QtWidgets.QLabel(self, text="Definir valor atual", objectName="valLbl")
        self.finalValue = QtWidgets.QLineEdit(self, placeholderText="00.0", alignment=QtCore.Qt.AlignCenter, objectName="finalValue")
        self.limitLbl = QtWidgets.QLabel(self, text="Limite", objectName="limitLbl")
        self.limitValue = QtWidgets.QLineEdit(self, placeholderText="00.0", alignment=QtCore.Qt.AlignCenter, objectName="limitValue")
        self.dueLbl = QtWidgets.QLabel(self, text="Vencimeto", objectName="dueLbl")
        self.DueDay = QtWidgets.QLineEdit(self, placeholderText="00", alignment=QtCore.Qt.AlignCenter, objectName="DueDay")
        self.closingLbl = QtWidgets.QLabel(self, text="Fechamento", objectName="closingLbl")
        self.ClosingDay = QtWidgets.QLineEdit(self, placeholderText="00", alignment=QtCore.Qt.AlignCenter, objectName="ClosingDay")
        self.applyButton = QtWidgets.QPushButton(self, text="Aplicar", objectName="button2")

        ## Customization ==
        self.applyButton.clicked.connect(self.SetFinalValue)
        options = self.mainWin.DataBase.AllAccounts["credit"][:]
        self.nameDropDown.addItems(options)
        self.nameDropDown.currentIndexChanged.connect(self.UpdateEditBox)
        self.UpdateEditBox()

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.finalValue.setSizePolicy(sizePolicy)
        self.nameDropDown.setSizePolicy(sizePolicy)

        self.finalValue.textChanged.connect(lambda state, targetEdit=self.finalValue: self.numberEntered(targetEdit))

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        self.gridLayout.addWidget(self.accName,0,1,1,1)
        self.gridLayout.addWidget(self.nameDropDown,0,2,1,1)
        self.gridLayout.addWidget(self.valLbl,1,0,1,1)
        self.gridLayout.addWidget(self.finalValue,1,1,1,1)
        self.gridLayout.addWidget(self.limitLbl,1,2,1,1)
        self.gridLayout.addWidget(self.limitValue,1,3,1,1)
        self.gridLayout.addWidget(self.dueLbl,2,0,1,1)
        self.gridLayout.addWidget(self.DueDay,2,1,1,1)
        self.gridLayout.addWidget(self.closingLbl,2,2,1,1)
        self.gridLayout.addWidget(self.ClosingDay,2,3,1,1)
        self.gridLayout.addWidget(self.applyButton,3,3,1,1)

    def UpdateEditBox(self):
        currAcc = self.nameDropDown.currentText()
        if currAcc:
            currAccData = self.mainWin.DataBase.acc_tbl.readByUnique(2,currAcc)
            self.finalValue.setText( str(round(Decimal(currAccData[3]), 2)) )
            self.limitValue.setText( str(round(Decimal(currAccData[4]), 2)) )
            self.DueDay.setText(str(currAccData[5]))
            self.ClosingDay.setText(str(currAccData[6]))

    def SetFinalValue(self):
        accName = self.nameDropDown.currentText()
        Acc_ID = self.mainWin.DataBase.acc_tbl.readByUnique(2, accName)
        Catg_ID = self.mainWin.DataBase.category_tbl.readByName("Outros")
        diffValue = float(self.finalValue.text()) - self.mainWin.DataBase.Totals["credit"][accName]
        accData = {
            'Acc_ID':Acc_ID[0],
            'Type':Acc_ID[1],
            'Name':Acc_ID[2],
            'Total':Acc_ID[3],
            'Limit':float(self.limitValue.text()),
            'DueDay':int(self.DueDay.text()),
            'ClosingDay':int(self.ClosingDay.text())
        }
        self.mainWin.DataBase.acc_tbl.updateById(accData)
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