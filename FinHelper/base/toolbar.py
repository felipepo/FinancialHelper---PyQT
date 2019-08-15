from PySide2 import QtWidgets, QtCore, QtGui
from ..dialogwin import transaction_window, account_window, transfer_window
from ..utilities import dict_from_list, funs

class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWin = parent
        ## Initialization ==
        self.setObjectName("toolbar")
        self.button = {}
        toolbarButtons = ("HomeButton", "AddExpenseBank",
        "AddAccBank",
        "RemoveAccBank",
        "Transfer", "EditTransfer")

        ## Creation ==
        for button in toolbarButtons:
            self.button[button] = QtWidgets.QAction(parent, objectName="ToolbarButton")
            icon = QtGui.QIcon()
            finHelperFolder = funs.getFinHelperPath()
            iconPath = "{}/data/images/{}.png".format(finHelperFolder, button)
            icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.button[button].setIcon(icon)
            self.addAction(self.button[button])

        ## Customization ==
        self.button["HomeButton"].triggered.connect(self.goToHome)
        self.button["AddExpenseBank"].triggered.connect(self.addTransaction)
        #self.button["AddRevenueBank"].triggered.connect(self.goToHome)
        self.button["AddAccBank"].triggered.connect(self.addAccount)
        self.button["RemoveAccBank"].triggered.connect(self.removeAccount)
        #self.button["AddAccCC"].triggered.connect(self.goToHome)
        #self.button["RemoveAccCC"].triggered.connect(self.goToHome)
        #self.button["AddRevenueCC"].triggered.connect(self.goToHome)
        self.button["Transfer"].triggered.connect(self.transfer)
        # self.button["EditTransfer"].triggered.connect(self.debug)

        ## Layout ==

    def goToHome(self):
        self.mainWin.stackFrame.setCurrentIndex(0)

    def addTransaction(self):
        mayProceed = False
        while mayProceed == False:
            debitOptions = self.mainWin.DataBase.AllAccounts["debit"]
            creditOptions = self.mainWin.DataBase.AllAccounts["credit"]
            catgOptions = self.mainWin.DataBase.AllCategories
            wind = transaction_window.Create(self, debitOptions, creditOptions, catgOptions)
            if wind.exec_():
                if "AppendData" in wind.inputs:
                    self.mainWin.newCategory(wind.inputs)
                instalments = wind.inputs['Instalments']
                targetCatg = self.mainWin.DataBase.category_tbl.readByName(wind.inputs["Category"])
                targetAcc = self.mainWin.DataBase.acc_tbl.readByUnique(wind.inputs["AccType"], wind.inputs["AccName"])
                wind.inputs["Value"] = wind.inputs["Value"]/instalments
                transInfo = {"Catg_ID":targetCatg[0], "Acc_ID":targetAcc[0], "Comment":wind.inputs["Comment"], "Value":wind.inputs["Value"], "Date":wind.inputs["Date"]}
                if targetAcc[1] == 2:
                    for iMonth in range(instalments):
                        instalmentInfo = transInfo.copy()
                        cardData = wind.inputs.copy()
                        if instalments > 1:
                            instalmentInfo["Comment"] = '({}/{}) {}'.format(iMonth+1, instalments, instalmentInfo["Comment"])
                            instalmentInfo["Date"] = QtCore.QDate.fromString(instalmentInfo["Date"], 'dd/MM/yyyy').addDays((iMonth)*30).toString('dd/MM/yyyy')
                        transID = self.mainWin.DataBase.NewTransaction(instalmentInfo)
                        cardData["Comment"] = instalmentInfo["Comment"]
                        cardData["Date"] = instalmentInfo["Date"]
                        self.mainWin.creditCardPage.cardArea.AddCard(cardData, transID)
                else:
                    transID = self.mainWin.DataBase.NewTransaction(transInfo)
                    self.mainWin.accPage.cardArea.AddCard(wind.inputs, transID)
                self.mainWin.updateValuePlaces()
                mayProceed = True
            else:
                mayProceed = True

    def transfer(self):
        mayProceed = False
        while mayProceed == False:
            debitOptions = self.mainWin.DataBase.Totals['debit']
            wind = transfer_window.Create(self, debitOptions)
            if wind.exec_():
                transferCatg = self.mainWin.DataBase.category_tbl.readByName("Transferência")
                srcData = self.mainWin.DataBase.acc_tbl.readByUnique(1, wind.inputs["srcName"])
                dstData = self.mainWin.DataBase.acc_tbl.readByUnique(1, wind.inputs["dstName"])
                sourceData = {
                    'Catg_ID':transferCatg[0],
                    'Acc_ID':srcData[0],
                    'Category':"Transferência",
                    'Date':wind.inputs['Date'],
                    'AccName':wind.inputs['srcName'],
                    'Comment':'Transferência p/ {}'.format(wind.inputs['dstName']),
                    'AccType':1,
                    'Value':wind.inputs['Value']*(-1)
                }
                destData = {
                    'Catg_ID':transferCatg[0],
                    'Acc_ID':dstData[0],
                    'Category':"Transferência",
                    'Date':wind.inputs['Date'],
                    'AccName':wind.inputs['dstName'],
                    'Comment':'Transferência de {}'.format(wind.inputs['srcName']),
                    'AccType':1,
                    'Value':wind.inputs['Value']
                }
                transID = self.mainWin.DataBase.NewTransaction(sourceData)
                if transID != 'Error':
                    self.mainWin.accPage.cardArea.AddCard(sourceData, transID)
                else:
                    print('Problema na conta')
                transID = self.mainWin.DataBase.NewTransaction(destData)
                if transID != 'Error':
                    mayProceed = True
                    self.mainWin.accPage.cardArea.AddCard(destData, transID)
                    self.mainWin.updateValuePlaces()
                else:
                    print('Problema na conta')
            else:
                mayProceed = True

    def addAccount(self):
        mayProceed = False
        while mayProceed == False:
            wind = account_window.New(self)
            if wind.exec_():
                addedFlag = self.mainWin.DataBase.acc_tbl.insert(wind.inputs)
                if addedFlag:
                    mayProceed = True
                    self.mainWin.updateValuePlaces()
                    if wind.inputs['Type'] == 1:
                        self.mainWin.homePage.debitGroupBox.comboBox.addItem(wind.inputs['Name'])
                        self.mainWin.accPage.controlFrame.setValueGroup.nameDropDown.addItem(wind.inputs['Name'])
                    else:
                        self.mainWin.homePage.creditGroupBox.comboBox.addItem(wind.inputs['Name'])
                        self.mainWin.creditCardPage.controlFrame.setValueGroup.nameDropDown.addItem(wind.inputs['Name'])
                else:
                    print('acc ja existe')
            else:
                mayProceed = True

    def removeAccount(self):
        mayProceed = False
        while mayProceed == False:
            debitOptions = self.mainWin.DataBase.AllAccounts["debit"]
            creditOptions = self.mainWin.DataBase.AllAccounts["credit"]
            wind = account_window.Remove(self, debitOptions, creditOptions)
            if wind.exec_():
                toBeRemoved = self.mainWin.DataBase.acc_tbl.readByUnique(wind.inputs['Type'], wind.inputs['Name'])
                toBeRemoved = dict_from_list.account(toBeRemoved)
                updatedFlag = 0
                counter = 0
                toBeRemoved['Name'] = 'DELETED{}{}'.format(counter, toBeRemoved['Name'])
                while not updatedFlag:
                    try:
                        self.mainWin.DataBase.acc_tbl.updateById(toBeRemoved)
                        updatedFlag = 1
                    except:
                        toBeRemoved['Name'] = toBeRemoved['Name'].replace(str(counter), str(counter+1))
                        counter = counter + 1
                mayProceed = True
                if wind.inputs['Type'] == 1:
                    itemToRemove = debitOptions.index(wind.inputs['Name']) + 1
                    self.mainWin.homePage.debitGroupBox.comboBox.removeItem(itemToRemove)
                    self.mainWin.accPage.controlFrame.setValueGroup.nameDropDown.removeItem(itemToRemove-1)
                    self.mainWin.accPage.cardArea.UpdateALLCards()
                else:
                    itemToRemove = creditOptions.index(wind.inputs['Name']) + 1
                    self.mainWin.homePage.creditGroupBox.comboBox.removeItem(itemToRemove)
                    self.mainWin.creditCardPage.controlFrame.setValueGroup.nameDropDown.removeItem(itemToRemove-1)
                    self.mainWin.creditCardPage.cardArea.UpdateALLCards()
                self.mainWin.updateValuePlaces()
            else:
                mayProceed = True