import sqlite3
import Funs
from sqlite3 import Error

class Create():
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