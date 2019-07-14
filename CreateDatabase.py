import sqlite3
import Funs
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
    
def get_all_ids(conn):
    cursor = conn.cursor()
    getStr = "SELECT Acc_ID FROM Account"
    IDs = [accID[0] for accID in cursor.execute(getStr)]
    return IDs

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_account(conn, accInfo):
    cursor = conn.cursor()
    insertStr = "INSERT INTO Account (Type, Name, Total) VALUES (:Type, :Name, :Total)"
    cursor.execute(insertStr, accInfo)
    return cursor.lastrowid

def read_account(conn, accInfo, chooseFetch, howmany = 1):
    # c.fetchall() - Fetch all remaining rows as a list. If there is no row available, returns empty list
    # c.fetchmany() - Fetch X number of rows as a list. If there is no row availabe, returns empty list
    # c.fetchone() - Fetch the next row in result. If there is no row available, returns one
    cursor = conn.cursor()
    # Provide results that we can iterate through
    cursor.execute("SELECT * FROM Account WHERE Name = :Name", accInfo)
    if chooseFetch == 1:
        return cursor.fetchone()
    elif chooseFetch == 2:
        return cursor.fetchall()
    else:
        return cursor.fetchmany(howmany)

def update_account(conn, accInfo):
    cursor = conn.cursor()
    cursor.execute("""UPDATE Transaction WHERE SET 
                WHERE x = x AND x = x""", accInfo)

def delete_account(conn, accInfo):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Transaction WHERE x = x AND last = last", accInfo)

if __name__ == "__main__":
    accTable = """CREATE TABLE IF NOT EXISTS Account (
        Acc_ID integer PRIMARY KEY,
        Type integer NOT NULL,
        Name text NOT NULL,
        Total integer NOT NULL
        );"""
    catgTable = """CREATE TABLE IF NOT EXISTS Category (
        Catg_ID integer PRIMARY KEY,
        Name text NOT NULL,
        Color text NOT NULL
        );"""
    transTable = """CREATE TABLE IF NOT EXISTS Transaction (
        Trans_ID integer PRIMARY KEY,
        Catg_ID integer NOT NULL,
        Acc_ID integer NOT NULL,
        Date text NOT NULL,
        Value real NOT NULL,
        Comment text NOT NULL,
        Type integer NOT NULL,
        FOREIGN KEY (Catg_ID) REFERENCES Category (Catg_ID) ON DELETE NO ACTION ON UPDATE NO ACTION,
        FOREIGN KEY (Acc_ID) REFERENCES Account (Acc_ID) ON DELETE ON NO ACTION UPDATE NO ACTION
        );"""
    dbfile = ':memory:'
    # dbfile = 'DataBase/Data.db'
    conn = create_connection(dbfile)
    if conn is not None:
        create_table(conn, accTable)
        create_table(conn, catgTable)
        for i in range(2000):
            # test = generateData()
            # print(test['Value'])
            accInfo = Funs.generateAcc()
            # test = Funs.generateCatg()
            # print("Row to be added ---")
            # print(accInfo)
            with conn:
                idS = create_account(conn, accInfo)
                # print(idS)
                # print(read_account(conn, {'Name':'BB'},2))
        allIDs = get_all_ids(conn)
        print(allIDs)
        conn.close()
    else:
        print("Could not create the database connection")