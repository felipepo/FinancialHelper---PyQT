import sqlite3
import Funs
from sqlite3 import Error
from DataBase import AccountTable
from DataBase import CategoryTable
from DataBase import CategoryTotalTable
from DataBase import ExtractTable

class Create():
    def __init__(self, inMemory):
        if inMemory == 1:
            self.db_file = ':memory:'
        else:
            self.db_file = 'DataBase/Data.db'
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            with self.conn:
                self.conn.execute("PRAGMA foreign_keys = ON")
            self.AccountTable = AccountTable.Create(self.conn, self.cursor)
            self.CategoryTable = CategoryTable.Create(self.conn, self.cursor)
            self.CategoryTotalTable = CategoryTotalTable.Create(self.conn, self.cursor)
            self.ExtractTable = ExtractTable.Create(self.conn, self.cursor)

            # Create tables
            self.create_table(self.AccountTable.createText)
            self.create_table(self.CategoryTable.createText)
            self.create_table(self.CategoryTotalTable.createText)
            self.create_table(self.ExtractTable.createText)

            # Store some data
            self.AllAccounts = self.AccountTable.get_names()
            self.AllCategories = self.CategoryTable.get_names()
            self.Totals = self.AccountTable.get_totals()
        except Error as e:
            print(e)
            print("Não criou conexão")

    def ResetValues(self):
        self.AllAccounts = self.AccountTable.get_names()
        self.AllCategories = self.CategoryTable.get_names()
        self.Totals = self.AccountTable.get_totals()

    def NewTransaction(self, transInfo):
        self.ExtractTable.insert(transInfo)
        # Update Accounts Table
        targetAcc = self.AccountTable.readById(transInfo["Acc_ID"])
        accUpdt = {"Name":targetAcc[2], "Type":targetAcc[1], "Total":targetAcc[3]+transInfo["Value"], "Limit":targetAcc[4], "DueDay":targetAcc[5], "ClosingDay":targetAcc[6]}
        self.AccountTable.updateByUnique(accUpdt)

        # Update Categories Table
        month, year = Funs.GetMY(transInfo["Date"])
        year = int(year)
        month = Funs.GetMonth(month)
        targetCategoryTotal = self.CategoryTotalTable.readByUnique(transInfo["Catg_ID"], month, year)
        if targetCategoryTotal is None:
            catgTotalUpdt = {"Catg_ID":transInfo["Catg_ID"], "Month":month, "Year":year, "Total":transInfo["Value"]}
            self.CategoryTotalTable.insert(catgTotalUpdt)
        else:
            catgTotalUpdt = {"Catg_ID":transInfo["Catg_ID"], "Month":month, "Year":year, "Total":transInfo["Value"]+targetCategoryTotal[2]}
            self.CategoryTotalTable.updateByUnique(catgTotalUpdt)
    
    def UpdateTransaction(self, transInfo):
        targetTrans = self.ExtractTable.readById(transInfo["Trans_ID"])
        valueDiff = transInfo["Value"] - targetTrans[4]
        self.ExtractTable.update(transInfo)
        # Update Accounts Table
        targetAcc = self.AccountTable.readById(transInfo["Acc_ID"])
        accUpdt = {"Name":targetAcc[2], "Type":targetAcc[1], "Total":targetAcc[3]+valueDiff, "Limit":targetAcc[4], "DueDay":targetAcc[5], "ClosingDay":targetAcc[6]}
        self.AccountTable.updateByUnique(accUpdt)

        # Update Categories Table
        month, year = Funs.GetMY(transInfo["Date"])
        year = int(year)
        month = Funs.GetMonth(month)
        targetCategoryTotal = self.CategoryTotalTable.readByUnique(transInfo["Catg_ID"], month, year)
        if targetCategoryTotal is None:
            catgTotalUpdt = {"Catg_ID":transInfo["Catg_ID"], "Month":month, "Year":year, "Total":transInfo["Value"]}
            self.CategoryTotalTable.insert(catgTotalUpdt)
        else:
            catgTotalUpdt = {"Catg_ID":transInfo["Catg_ID"], "Month":month, "Year":year, "Total":transInfo["Value"]+targetCategoryTotal[0]}
            self.CategoryTotalTable.updateByUnique(catgTotalUpdt)

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        """
        try:
            self.cursor.execute(create_table_sql)
            print("Table criada")
        except Error as e:
            print('Table Não foi criada')
            print(e)

    def close_db(self):
        self.conn.close()
        print("Closed Database")

if __name__ == "__main__":
    inMemory = 1
    create_Data = 1
    sql_db = Create(inMemory)

    if create_Data == 1:

        # Create Accounts
        # AccInfo -> Name, Type, Total, Limit, DueDay, ClosingDay
        for _ in range(30):
            accInfo = Funs.generateAcc()
            accID = sql_db.AccountTable.insert(accInfo)

        # Create categories
        # catgInfo -> Name, Color
        for _ in range(10):
            catgInfo = Funs.generateCatg()
            catgID = sql_db.CategoryTable.insert(catgInfo["Name"], catgInfo["Color"])

        Catg_ID_list = sql_db.CategoryTable.get_ids()
        Acc_ID_list = sql_db.AccountTable.get_ids()

        # Create transactions
        # transInfo -> Acc_ID, Catg_ID, Comment, Date, Value
        for _ in range(10):
            transInfo = Funs.generateTrans(Catg_ID_list, Acc_ID_list)
            sql_db.NewTransaction(transInfo)

        print(list(sql_db.CategoryTable.get_names()))
    else:
        transInfo = {"Trans_ID":2, "Acc_ID":3, "Catg_ID":6, "Comment":"Atualizado", "Date":"18/2/2019", "Value":0}
        sql_db.UpdateTransaction(transInfo)

    sql_db.close_db()