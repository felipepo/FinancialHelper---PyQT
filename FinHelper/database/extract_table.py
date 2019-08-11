class Create():
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