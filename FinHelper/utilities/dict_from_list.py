def transt(transList):
    transDict = {
        'Trans_ID': transList[0],
        'Catg_ID': transList[1],
        'Acc_ID': transList[2],
        'Date': transList[3],
        'Value': transList[4],
        'Comment': transList[5]
    }
    return transDict

def catgTotal(catgTotalList):
    catgTotalDict = {
        'Total_Catg_ID': catgTotalList[0],
        'Catg_ID': catgTotalList[1],
        'Total': catgTotalList[2],
        'Month': catgTotalList[3],
        'Year': catgTotalList[4]
    }
    return catgTotalDict

def account(accountList):
    accDict = {
        'Acc_ID':accountList[0],
        'Type':accountList[1],
        'Name':accountList[2],
        'Total':accountList[3],
        'Limit':accountList[4],
        'DueDay':accountList[5],
        'ClosingDay':accountList[6]
    }
    return accDict