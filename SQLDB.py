import sqlite3
import Funs
from sqlite3 import Error

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
            self.AccountTable = AccountTable(self.conn, self.cursor)
            self.CategoryTable = CategoryTable(self.conn, self.cursor)
            self.CategoryTotalTable = CategoryTotalTable(self.conn, self.cursor)
            self.ExtractTable = ExtractTable(self.conn, self.cursor)

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

class AccountTable():
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.createText = """CREATE TABLE IF NOT EXISTS Account (
            Acc_ID integer PRIMARY KEY,
            Type integer NOT NULL,
            Name text NOT NULL,
            Total real NOT NULL,
            LimitVal integer,
            DueDay integer,
            ClosingDay integer,
            UNIQUE (Type, Name)
            );"""

    def get_ids(self):
        getStr = "SELECT Acc_ID FROM Account"
        IDs = tuple(ID[0] for ID in self.cursor.execute(getStr))
        return IDs

    def get_names(self):
        getStr = "SELECT Type, Name FROM Account"
        acc = {'credit':[], 'debit':[]}
        for data in self.cursor.execute(getStr):
            if data[0] == 2:
                acc['credit'].append(data[1])
            else:
                acc['debit'].append(data[1])
        return acc
    
    def get_totals(self):
        getStr = "SELECT Type, Total, Name FROM Account"
        total = {'credit':{"Todas":0}, 'debit':{"Todas":0}}
        for data in self.cursor.execute(getStr):
            if data[0] == 2:
                total['credit']["Todas"] = total['credit']["Todas"] + data[1]
                total['credit'][data[2]] = data[1]
            else:
                total['debit']["Todas"] = total['debit']["Todas"] + data[1]
                total['debit'][data[2]] = data[1]
        return total
    
    def insert(self, accInfo):
        try:
            insertStr = """INSERT INTO Account (Type, Name, Total, LimitVal, DueDay, ClosingDay) 
                            VALUES (:Type, :Name, :Total, :Limit, :DueDay, :ClosingDay)"""
            with self.conn:
                self.cursor.execute(insertStr, accInfo)
            return self.cursor.lastrowid
        except:
            print("Account " + str(accInfo) + " already exist")

    def readAll(self):
        # Provide results that we can iterate through
        self.cursor.execute("SELECT * FROM Account")
        return self.cursor.fetchall() # - Fetch all remaining rows as a list. If there is no row available, returns empty list

    def readById(self, Acc_ID):
        # Provide results that we can iterate through
        self.cursor.execute("SELECT * FROM Account WHERE Acc_ID = :Acc_ID", {"Acc_ID":Acc_ID})
        return self.cursor.fetchone() # - Fetch the next row in result. If there is no row available, returns one

    def readByUnique(self, Type, Name):
        # Provide results that we can iterate through
        self.cursor.execute("SELECT * FROM Account WHERE Type = :Type AND Name = :Name", {"Type":Type, "Name":Name})
        return self.cursor.fetchone() # - Fetch the next row in result. If there is no row available, returns one

    def updateById(self, accInfo):
        self.cursor.execute("""UPDATE Account SET Type = :Type, Name = :Name, Total = :Total, LimitVal = :Limit, DueDay = :DueDay, ClosingDay = :ClosingDay
                    WHERE Acc_ID = :Acc_ID""", accInfo)

    def updateByUnique(self, accInfo):
        with self.conn:
            self.cursor.execute("""UPDATE Account SET Total = :Total, LimitVal = :Limit, DueDay = :DueDay, ClosingDay = :ClosingDay
                        WHERE Type = :Type AND Name = :Name""", accInfo)

    def deleteById(self, Acc_ID):
        with self.conn:
            self.cursor.execute("DELETE FROM Account WHERE Acc_ID = :Acc_ID", {"Acc_ID": Acc_ID})

    def deleteByUnique(self, Type, Name):
        with self.conn:
            self.cursor.execute("DELETE FROM Account WHERE Type = :Type AND Name = :Name", {"Type": Type, "Name": Name})

class CategoryTable():
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.createText = """CREATE TABLE IF NOT EXISTS Category (
            Catg_ID integer PRIMARY KEY,
            Name text NOT NULL UNIQUE,
            Color text NOT NULL
            );"""

    def get_ids(self):
        getStr = "SELECT Catg_ID FROM Category"
        IDs = tuple(ID[0] for ID in self.cursor.execute(getStr))
        return IDs

    def get_names(self):
        getStr = "SELECT Name FROM Category"
        names = tuple(name[0] for name in self.cursor.execute(getStr))
        return names

    def insert(self, Name, Color):
        try:
            insertStr = """INSERT INTO Category (Name, Color) 
                            VALUES (:Name, :Color)"""
            with self.conn:
                self.cursor.execute(insertStr, {"Name":Name, "Color":Color})
            return self.cursor.lastrowid
        except:
            print('Category already exists')

    def readAll(self):
        # Provide results that we can iterate through
        self.cursor.execute("SELECT * FROM Category")
        return self.cursor.fetchall() # - Fetch all remaining rows as a list. If there is no row available, returns empty list

    def readById(self, Catg_ID):
        # Provide results that we can iterate through
        self.cursor.execute("SELECT * FROM Category WHERE Catg_ID = :Catg_ID", {"Catg_ID": Catg_ID})
        return self.cursor.fetchone() # - Fetch the next row in result. If there is no row available, returns one

    def readByName(self, Catg_Name):
        # Provide results that we can iterate through
        self.cursor.execute("SELECT * FROM Category WHERE Name = :Name", {"Name": Catg_Name})
        return self.cursor.fetchone() # - Fetch the next row in result. If there is no row available, returns one

    def updateById(self, Catg_ID, Catg_Name, Color):
        with self.conn:
            self.cursor.execute("""UPDATE Category SET Color = :Color, Name = :Name
                        WHERE Catg_ID = :Catg_ID""", {"Catg_ID": Catg_ID, "Name":Catg_Name, "Color": Color})

    def updateByName(self, Catg_Name, Color):
        with self.conn:
            self.cursor.execute("""UPDATE Category SET Color = :Color
                        WHERE Name = :Name""", {"Name":Catg_Name, "Color": Color})

    def deleteById(self, Catg_ID):
        with self.conn:
            self.cursor.execute("DELETE FROM Category WHERE Catg_ID = :Catg_ID", {"Catg_ID": Catg_ID})

    def deleteByName(self, Name):
        with self.conn:
            self.cursor.execute("DELETE FROM Category WHERE Name = :Name", {"Name": Name})

class CategoryTotalTable():
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.createText = """CREATE TABLE IF NOT EXISTS CategoryTotal (
            Total_Catg_ID integer PRIMARY KEY,
            Catg_ID integer NOT NULL,
            Total real NOT NULL,
            Month integer NOT NULL,
            Year integer NOT NULL,
            UNIQUE (Catg_ID, Month, Year),
            FOREIGN KEY (Catg_ID) REFERENCES Category (Catg_ID) ON DELETE NO ACTION ON UPDATE NO ACTION
            );"""

    def get_ids(self):
        getStr = "SELECT Total_Catg_ID FROM CategoryTotal"
        IDs = tuple(ID[0] for ID in self.cursor.execute(getStr))
        return IDs

    def insert(self, catgTotalInfo):
        try:
            insertStr = """INSERT INTO CategoryTotal (Catg_ID, Month, Year, Total) 
                            VALUES (:Catg_ID, :Month, :Year, :Total)"""
            with self.conn:
                self.cursor.execute(insertStr, catgTotalInfo)
            return self.cursor.lastrowid
        except:
            print('Total already exists')

    def readAll(self):
        # Provide results that we can iterate through
        self.cursor.execute("SELECT * FROM CategoryTotal")
        return self.cursor.fetchall() # - Fetch all remaining rows as a list. If there is no row available, returns empty list

    def readById(self, catgTotalID):
        # Provide results that we can iterate through
        self.cursor.execute("SELECT * FROM CategoryTotal WHERE Total_Catg_ID = :Total_Catg_ID", {'Total_Catg_ID': catgTotalID})
        return self.cursor.fetchone() # - Fetch the next row in result. If there is no row available, returns one

    def readByUnique(self, Catg_ID, Month, Year):
        # Provide results that we can iterate through
        self.cursor.execute("SELECT * FROM CategoryTotal WHERE Catg_ID = :Catg_ID AND Month = :Month AND Year = :Year", {'Catg_ID': Catg_ID, 'Month':Month, 'Year':Year})
        return self.cursor.fetchone() # - Fetch the next row in result. If there is no row available, returns one

    def updateById(self, catgTotalInfo):
        with self.conn:
            self.cursor.execute("""UPDATE CategoryTotal SET Catg_ID = :Catg_ID, Month = :Month, Year = :Year, Total = :Total
                        WHERE Total_Catg_ID = :Total_Catg_ID""", catgTotalInfo)

    def updateByUnique(self, catgTotalInfo):
        with self.conn:
            self.cursor.execute("""UPDATE CategoryTotal SET Total = :Total
                        WHERE Catg_ID = :Catg_ID AND Month = :Month AND Year = :Year""", catgTotalInfo)

    def deleteById(self, catgTotalID):
        with self.conn:
            self.cursor.execute("DELETE FROM CategoryTotal WHERE Total_Catg_ID = :Total_Catg_ID", {'Total_Catg_ID': catgTotalID})

    def deleteByUnique(self, Catg_ID, Month, Year):
        with self.conn:
            self.cursor.execute("DELETE FROM CategoryTotal WHERE Catg_ID = :Catg_ID AND Month = :Month AND Year = :Year", {'Catg_ID': Catg_ID, 'Month':Month, 'Year':Year})

class ExtractTable():
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.createText = """CREATE TABLE IF NOT EXISTS Extract (
            Trans_ID integer PRIMARY KEY,
            Catg_ID integer NOT NULL,
            Acc_ID integer NOT NULL,
            Date text NOT NULL,
            Value real NOT NULL,
            Comment text NOT NULL,
            FOREIGN KEY (Catg_ID) REFERENCES Category (Catg_ID) ON DELETE NO ACTION ON UPDATE NO ACTION,
            FOREIGN KEY (Acc_ID) REFERENCES Account (Acc_ID) ON DELETE NO ACTION ON UPDATE NO ACTION
            );"""

    def get_ids(self):
        getStr = "SELECT Trans_ID FROM Extract"
        IDs = tuple(ID[0] for ID in self.cursor.execute(getStr))
        return IDs

    def insert(self, transInfo):
        insertStr = """INSERT INTO Extract (Catg_ID, Acc_ID, Date, Value, Comment) 
                        VALUES (:Catg_ID, :Acc_ID, :Date, :Value, :Comment)"""
        with self.conn:
            self.cursor.execute(insertStr, transInfo)
        return self.cursor.lastrowid

    def readAll(self):
        # Provide results that we can iterate through
        self.cursor.execute("SELECT * FROM Extract")
        return self.cursor.fetchall() # - Fetch all remaining rows as a list. If there is no row available, returns empty list - Fetch X number of rows as a list. If there is no row availabe, returns empty list

    def readById(self, transID):
        # Provide results that we can iterate through
        self.cursor.execute("SELECT * FROM Extract WHERE Trans_ID = :Trans_ID", {'Trans_ID': transID})
        return self.cursor.fetchone() # - Fetch the next row in result. If there is no row available, returns one

    def update(self, transInfo):
        with self.conn:
            self.cursor.execute("""UPDATE Extract SET Catg_ID = :Catg_ID, Acc_ID = :Acc_ID, Date = :Date, Value = :Value, Comment = :Comment
                        WHERE Trans_ID = :Trans_ID""", transInfo)

    def deleteByID(self, transID):
        with self.conn:
            self.cursor.execute("DELETE FROM Extract WHERE Trans_ID = :Trans_ID", {'Trans_ID': transID})

if __name__ == "__main__":
    inMemory = 2
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
    else:
        transInfo = {"Trans_ID":2, "Acc_ID":3, "Catg_ID":6, "Comment":"Atualizado", "Date":"18/2/2019", "Value":0}
        sql_db.UpdateTransaction(transInfo)

    sql_db.close_db()