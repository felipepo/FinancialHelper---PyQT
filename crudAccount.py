
def create_account(conn, accInfo):
    try:
        cursor = conn.cursor()
        insertStr = """INSERT INTO Account (Type, Name, Total, LimitVal, DueDay, ClosingDay) 
                        VALUES (:Type, :Name, :Total, :Limit, :DueDay, :ClosingDay)"""
        cursor.execute(insertStr, accInfo)
        return cursor.lastrowid
    except:
        print("Account " + str(accInfo) + " already exist")

def read_account(conn, accInfo, chooseFetch, howmany = 1):
    # c.fetchall() - Fetch all remaining rows as a list. If there is no row available, returns empty list
    # c.fetchmany() - Fetch X number of rows as a list. If there is no row availabe, returns empty list
    # c.fetchone() - Fetch the next row in result. If there is no row available, returns one
    cursor = conn.cursor()

    # Provide results that we can iterate through
    cursor.execute("SELECT * FROM Account WHERE Type = :Type AND Name = :Name", accInfo)
    if chooseFetch == 1:
        return cursor.fetchone()
    elif chooseFetch == 2:
        return cursor.fetchall()
    else:
        return cursor.fetchmany(howmany)

def update_account(conn, accInfo):
    cursor = conn.cursor()
    cursor.execute("""UPDATE Account SET Total = :Total, LimitVal = :Limit, DueDay = :DueDay, ClosingDay = :ClosingDay
                WHERE Type = :Type AND Name = :Name""", accInfo)

def delete_account(conn, accInfo):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Account WHERE Type = :Type AND Name = :Name", accInfo)
