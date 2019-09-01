from PySide2 import QtWidgets, QtCore, QtGui
from ..dialogwin import category_window
from ..utilities import funs
import os

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWin = parent
        ## Initialization ==
        self.button = {}
        self.setObjectName("menubar")
        FileButtons = ["Novo", "Save", "Save As..."]
        CatgButtons = ["Editar"]
        # AccButtons = ["Adicionar", "Remover", "Renomear", "Definir Valor Atual"]
        ToolsButtons = ["Exportar"]

        ## Creation ==
        self.menuFile = QtWidgets.QMenu(self, objectName="MenuFile", title="File")
        for button in FileButtons:
            self.button[button] = QtWidgets.QAction(parent, objectName=button, text=button)
            self.menuFile.addAction(self.button[button])
        self.addAction(self.menuFile.menuAction())

        self.menuEdit = QtWidgets.QMenu(self, objectName="MenuEdit", title="Categorias")
        for button in CatgButtons:
            self.button[button] = QtWidgets.QAction(parent, objectName=button, text=button)
            self.menuEdit.addAction(self.button[button])
        self.addAction(self.menuEdit.menuAction())

        # self.menuAcc = QtWidgets.QMenu(self, objectName="menuAcc", title="Contas")
        # for button in AccButtons:
        #     self.button[button] = QtWidgets.QAction(parent, objectName=button, text=button)
        #     self.menuAcc.addAction(self.button[button])
        # self.addAction(self.menuAcc.menuAction())

        self.menuTools = QtWidgets.QMenu(self, objectName="menuTools", title="Ferramentas")
        for button in ToolsButtons:
            self.button[button] = QtWidgets.QAction(parent, objectName=button, text=button)
            self.menuTools.addAction(self.button[button])
        self.addAction(self.menuTools.menuAction())

        ## Customization ==
        self.button["Novo"].triggered.connect(self.newDB)
        self.button["Editar"].triggered.connect(self.configCategory)
        ## Layout ==

    def newDB(self):
        finHelperFolder = funs.getFinHelperPath()
        self.mainWin.DataBase.close_db()
        os.remove('{}/data/sql/data.db'.format(finHelperFolder))
        print("Saved")
        os.remove('{}/data/style/Style.qss'.format(finHelperFolder))
        self.mainWin.initialize()

    def configCategory(self):
        catgList = list(self.mainWin.DataBase.category_tbl.get_names())
        styleStr = self.mainWin.styleObj.InterfaceStyle
        wind = category_window.Create(catgList, styleStr)
        if wind.exec_():
            self.mainWin.styleObj.InterfaceStyle = wind.inputs["EditData"]
            if "AppendData" in wind.inputs:
                self.mainWin.styleObj.appendStyle(wind.inputs["AppendData"]["StyleFrame"])
                self.mainWin.styleObj.appendStyle(wind.inputs["AppendData"]["StyleLabel"])
                self.mainWin.DataBase.category_tbl.insert(wind.inputs["AppendData"]["Name"], wind.inputs["AppendData"]["rgb"])
            if "RemoveData" in wind.inputs:
                removedCatg = wind.inputs["RemoveData"]
                self.mainWin.DataBase.RemoveCategory(removedCatg)
                self.mainWin.DataBase.category_tbl.deleteByName(removedCatg)
            if "RenameData" in wind.inputs:
                oldName = wind.inputs["RenameData"]['oldName']
                newName = wind.inputs["RenameData"]['newName']
                self.mainWin.styleObj.renameStyle(oldName, newName)
                for iCatg in self.mainWin.DataBase.category_tbl.get_ids():
                    currCatg = self.mainWin.DataBase.category_tbl.readById(iCatg)
                    if currCatg[1] == oldName:
                        self.mainWin.DataBase.category_tbl.updateById(iCatg, newName, currCatg[2])
            self.mainWin.setStyleSheet(self.mainWin.styleObj.InterfaceStyle)
            self.mainWin.styleObj.createQSSFile()
            self.mainWin.setStyle(self.mainWin.style())
            self.mainWin.accPage.cardArea.UpdateALLCards()
            self.mainWin.updateInteface()