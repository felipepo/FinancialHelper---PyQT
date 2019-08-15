import sqlite3
from ..utilities import generate, dict_from_list, funs
from . import account_table, category_table, category_total_table, extract_table

class Create():
    def __init__(self, inMemory):
        finHelperFolder = funs.getFinHelperPath()
        self.db_file = 'DataBase/DataTest.db' if inMemory == 1 else '{}/data/sql/data.db'.format(finHelperFolder)
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            with self.conn:
                self.conn.execute("PRAGMA foreign_keys = ON")
            self.acc_tbl = account_table.Create(self.conn, self.cursor)
            self.category_tbl = category_table.Create(self.conn, self.cursor)
            self.category_total_tbl = category_total_table.Create(self.conn, self.cursor)
            self.extract_tbl = extract_table.Create(self.conn, self.cursor)

            # Create tables
            self.create_table(self.acc_tbl.createText)
            self.create_table(self.category_tbl.createText)
            self.create_table(self.category_total_tbl.createText)
            self.create_table(self.extract_tbl.createText)

            # Store some data
            self.AllAccounts = self.acc_tbl.get_names()
            self.AllCategories = self.category_tbl.get_names()
            self.AllTransactions = self.extract_tbl.get_ids()
            self.Totals = self.acc_tbl.get_totals()
        except sqlite3.Error as e:
            print(e)
            print("Não criou conexão")

    def ReGetValues(self):
        self.AllAccounts = self.acc_tbl.get_names()
        self.AllCategories = self.category_tbl.get_names()
        self.AllTransactions = self.extract_tbl.get_ids()
        self.Totals = self.acc_tbl.get_totals()

    def RemoveTransaction(self, transID):
        transInfo = self.extract_tbl.readById(transID)
        transInfo = dict_from_list.trans(transInfo)
        targetAcc = self.acc_tbl.readById(transInfo["Acc_ID"])
        accUpdt = {"Name":targetAcc[2], "Type":targetAcc[1], "Total":targetAcc[3]-transInfo["Value"], "Limit":targetAcc[4], "DueDay":targetAcc[5], "ClosingDay":targetAcc[6]}
        self.acc_tbl.updateByUnique(accUpdt)

        # Update Categories Table
        month, year = funs.GetMY(transInfo["Date"])
        year = int(year)
        month = funs.GetMonth(month)
        targetCategoryTotal = self.category_total_tbl.readByUnique(transInfo["Catg_ID"], month, year)
        catgTotalUpdt = {"Catg_ID":transInfo["Catg_ID"], "Month":month, "Year":year, "Total":targetCategoryTotal[2]-transInfo["Value"]}
        self.category_total_tbl.updateByUnique(catgTotalUpdt)

    def NewTransaction(self, transInfo):
        newTransID = self.extract_tbl.insert(transInfo)
        # Update Accounts Table
        targetAcc = self.acc_tbl.readById(transInfo["Acc_ID"])
        accUpdt = {"Name":targetAcc[2], "Type":targetAcc[1], "Total":targetAcc[3]+transInfo["Value"], "Limit":targetAcc[4], "DueDay":targetAcc[5], "ClosingDay":targetAcc[6]}
        self.acc_tbl.updateByUnique(accUpdt)

        # Update Categories Table
        month, year = funs.GetMY(transInfo["Date"])
        year = int(year)
        month = funs.GetMonth(month)
        targetCategoryTotal = self.category_total_tbl.readByUnique(transInfo["Catg_ID"], month, year)
        if targetCategoryTotal is None:
            catgTotalUpdt = {"Catg_ID":transInfo["Catg_ID"], "Month":month, "Year":year, "Total":transInfo["Value"]}
            self.category_total_tbl.insert(catgTotalUpdt)
        else:
            catgTotalUpdt = {"Catg_ID":transInfo["Catg_ID"], "Month":month, "Year":year, "Total":transInfo["Value"]+targetCategoryTotal[2]}
            self.category_total_tbl.updateByUnique(catgTotalUpdt)
        return newTransID

    def UpdateTransaction(self, transInfo):
        targetTrans = self.extract_tbl.readById(transInfo["Trans_ID"])
        valueDiff = transInfo["Value"] - targetTrans[4]
        self.extract_tbl.update(transInfo)
        # Update Accounts Table
        targetAcc = self.acc_tbl.readById(transInfo["Acc_ID"])
        accUpdt = {"Name":targetAcc[2], "Type":targetAcc[1], "Total":targetAcc[3]+valueDiff, "Limit":targetAcc[4], "DueDay":targetAcc[5], "ClosingDay":targetAcc[6]}
        self.acc_tbl.updateByUnique(accUpdt)

        # Update Categories Table
        month, year = funs.GetMY(transInfo["Date"])
        year = int(year)
        month = funs.GetMonth(month)
        targetCategoryTotal = self.category_total_tbl.readByUnique(transInfo["Catg_ID"], month, year)
        if targetCategoryTotal is None:
            catgTotalUpdt = {"Catg_ID":transInfo["Catg_ID"], "Month":month, "Year":year, "Total":transInfo["Value"]}
            self.category_total_tbl.insert(catgTotalUpdt)
        else:
            catgTotalUpdt = {"Catg_ID":transInfo["Catg_ID"], "Month":month, "Year":year, "Total":transInfo["Value"]+targetCategoryTotal[0]}
            self.category_total_tbl.updateByUnique(catgTotalUpdt)
        return "OK"

    def RemoveCategory(self, catName):
        # Get categories
        removedCatgData = self.category_tbl.readByName(catName)
        outros = self.category_tbl.readByName("Outros")
        allTrans = self.extract_tbl.readAll()
        for iTrans in allTrans:
            if iTrans[1] == removedCatgData[0]:
                transInfo = list(iTrans)
                transInfo[1] = outros[0]
                transInfo = dict_from_list.trans(transInfo)
                self.UpdateTransaction(transInfo)
                break
        allCatgTotal = self.category_total_tbl.readAll()
        for iCatg in allCatgTotal:
            if iCatg[1] == removedCatgData[0]:
                outrosTotal = self.category_total_tbl.readByUnique(outros[0], iCatg[3], iCatg[4])
                self.category_total_tbl.deleteByUnique(removedCatgData[0], iCatg[3], iCatg[4])
                if outrosTotal is None:
                    catgTotalUpdt = {"Catg_ID":outros[0], "Month":iCatg[3], "Year":iCatg[4], "Total":iCatg[2]}
                    self.category_total_tbl.insert(catgTotalUpdt)
                else:
                    outrosTotal = dict_from_list.catgTotal(outrosTotal)
                    outrosTotal["Total"] = outrosTotal["Total"] + iCatg[2]
                    self.category_total_tbl.updateByUnique(outrosTotal)


    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        """
        try:
            self.cursor.execute(create_table_sql)
            print("Table criada")
        except sqlite3.Error as e:
            print('Table Não foi criada')
            print(e)

    def close_db(self):
        self.conn.close()
        print("Closed Database")

    def simulateData(self, nTrans=10, nAcc=10):
        for _ in range(nAcc):
            accInfo = generate.generateAcc()
            self.acc_tbl.insert(accInfo)

        Catg_ID_list = self.category_tbl.get_ids()
        Acc_ID_list = self.acc_tbl.get_ids()

        # Create transactions
        # transInfo -> Acc_ID, Catg_ID, Comment, Date, Value
        for _ in range(nTrans):
            transInfo = generate.generateTrans(Catg_ID_list, Acc_ID_list)
            self.NewTransaction(transInfo)