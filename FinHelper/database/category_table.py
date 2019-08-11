class Create():
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