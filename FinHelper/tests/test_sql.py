from ..database import sql_class

def run_test():
    print("Testing creation of database")
    inMemory = 1
    create_Data = 1
    sql_db = sql_class.Create(inMemory)

    if create_Data == 1:
        sql_db.simulateData()

        print(list(sql_db.category_tbl.get_names()))
    else:
        transInfo = {"Trans_ID":2, "Acc_ID":3, "Catg_ID":6, "Comment":"Atualizado", "Date":"18/2/2019", "Value":0}
        sql_db.UpdateTransaction(transInfo)

    sql_db.close_db()