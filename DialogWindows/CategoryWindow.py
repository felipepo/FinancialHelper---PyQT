from PySide2 import QtCore, QtGui, QtWidgets
import copy
import unidecode
import Funs

class Create(QtWidgets.QDialog):
    def __init__(self, mainWin):
        super().__init__()
        self.mainWin = mainWin
        self.DataBase = mainWin.DataBase
        self.styleSTR = mainWin.styleObj.InterfaceStyle
        self.inputs = {}
        ## Initialization ==
        self.setObjectName('CategoryWindow')
        self.setWindowTitle("Configuração Categorias")
        self.resize(319, 256)
        self.setStyleSheet(self.styleSTR)

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

        self.exitButton.clicked.connect(self.CloseWindow)
        self.apllyButton.clicked.connect(self.Apply)

        ## Layout == 
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 3)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.apllyButton, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.exitButton, 1, 2, 1, 1)

    def Apply(self):
        mayProceed = 1
        # Remove Category
        if self.removeTab.catCombo.currentText():
            # Confirm if the user really wants to delete category
            # Do you really want to delete category "X"? Keep in mind that this will delete all its data
            # and all transactions related to it will be changed to "Outros"
            if mayProceed:
                self.inputs["RemoveData"] = self.removeTab.catCombo.currentText()

        if mayProceed:
            # Edit category color 
            self.inputs["EditData"] = self.styleSTR

            # Append new Category
            if self.addTab.newEntry.text():
                self.inputs["AppendData"] = {}
                self.inputs["AppendData"]["Name"] = self.addTab.newEntry.text()
                self.inputs["AppendData"]["rgb"] = self.addTab.rgb
                temp = self.addTab.getStyle()
                self.inputs["AppendData"]["StyleFrame"] = temp["Frame"]
                self.inputs["AppendData"]["StyleLabel"] = temp["Label"]

            # Rename Category
            if self.renameTab.newEntry.text():
                oldName = self.renameTab.catCombo.currentText()
                newName = self.renameTab.newEntry.text()
                self.inputs["RenameData"] = {"oldName": oldName, "newName":newName}
            self.accept()

    def CloseWindow(self):
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

        self.showColor.setMinimumSize(QtCore.QSize(24, 24))
        self.showColor.setMaximumSize(QtCore.QSize(24, 24))
        self.showColor.setStyleSheet('border:2px solid black')

        ## Layout ==
        self.gridLayout = QtWidgets.QGridLayout(self, objectName="gridLayout")
        
        self.gridLayout.addWidget(self.catLbl, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.newEntry, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.colorLbl, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.showColor, 2, 1, 1, 1, alignment = QtCore.Qt.AlignLeft)
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
        frameStyle = {
            'selectorStr':['QFrame'],
            'idStr':[category],
            'classStr':[""],
            'descendantStr':[""],
            'childStr':[""],
            'propStr':[{}],
            'propertyDic':{'background-color':self.rgb}
        }
        labelStyle = {
            'selectorStr':['QLabel'],
            'idStr':['Color'+category],
            'classStr':[""],
            'descendantStr':[""],
            'childStr':[""],
            'propStr':[{}],
            'propertyDic':{'background-color':self.rgb, "border": "2px solid black"}
        }
        styleDict = {"Frame":frameStyle,"Label":labelStyle}
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
        options = list(parent.DataBase.CategoryTable.get_names()[:])
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
        options = list(parent.DataBase.CategoryTable.get_names()[:])
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
        options = parent.DataBase.CategoryTable.get_names()[:]
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
            self.parent.styleSTR = self.parent.styleSTR.replace(prevBackRGB,backRGB)
            self.parent.setStyleSheet(self.parent.styleSTR)
            self.UpdateTemplate()

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