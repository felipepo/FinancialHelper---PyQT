import sqlite3
import Funs
from sqlite3 import Error

class Create():
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
        return True

    def deleteByUnique(self, Type, Name):
        with self.conn:
            self.cursor.execute("DELETE FROM Account WHERE Type = :Type AND Name = :Name", {"Type": Type, "Name": Name})
        return True