import pickle
import time
import re
import os,binascii
import random

'''
General Functions
	showdic
	AddTransaction
	GetMY
	saveData
	loadData
'''

def showdic(dict):
    for x in dict:
        print (x)
        print ('               ',dict[x])
        # for y in dict[x]:
        #     print ('               ',y,':',dict[x][y])
   
#=========================================================================================     
def AddTransaction(objAcc, category, value, date, comment, bankAccount):
    month, year = GetMY(date)
    objAcc.totalAmount += int(value)
    objAcc.transactions["trans"+str(len(objAcc.transactions))] = {
            "Category": category,
            "Value": value,
            "Date": date,
            "Comment": comment,
            "BankAccount": bankAccount,
            "Month": month,
            "Year": year
        }

#=========================================================================================
def GetMY(date):
    months = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")
    splitDate = date.split("/")
    month = months[int(splitDate[1])-1]
    year = splitDate[2]
    return month, year

#=========================================================================================
def saveData(fileName, data):
    path = "DataBase/" + fileName
    outfile = open(path, "wb")
    pickle.dump(data,outfile)
    outfile.close()

#=========================================================================================
def loadData(fileName):
    path = "DataBase/" + fileName
    infile = open(path, "rb")
    loadedData = pickle.load(infile)
    infile.close()
    return loadedData

#=========================================================================================
def getDate():
    clk = list(time.localtime())
    day = str(clk[2])
    month = str(clk[1])
    year = str(clk[0])
    if len(day) == 1:
        day = "0" + day
    if len(month) == 1:
        month = "0" + month
    dateVal = day + "/" + month + "/" +  year
    return dateVal

#=========================================================================================
def checkDate(date):
    datePattern = re.compile(r'[0-3]\d/[0-1]\d/\d{4}\Z')
    matched = datePattern.match(date)
    return matched
    
#=========================================================================================
def createID():
    newID = binascii.b2a_hex(os.urandom(15))
    return newID
    
#=========================================================================================
def debugAccounts(Accounts):
    print("===============================")
    print("CONTAS")
    for acc in Accounts.accountsObjs:
        print("-----")
        print(acc)
        print(Accounts.accountsObjs[acc].totalAmount)
        for trans in Accounts.accountsObjs[acc].transactions:
            print("                Transition")
            try:
                print(Accounts.accountsObjs[acc].transactions[trans].value)
                print(Accounts.accountsObjs[acc].transactions[trans].category)
                print(Accounts.accountsObjs[acc].transactions[trans].date)
            except:
                print("None")
    print("===============================")
    print("Cartão de Crédito")
    for acc in Accounts.creditCardObjs:
        print("-----")
        print(acc)
        print(Accounts.creditCardObjs[acc].totalAmount)
        value = ""
        category = ""
        date = ""
        print("                Transitions")
        for trans in Accounts.creditCardObjs[acc].transactions:
            #try:
            currValue = str(Accounts.creditCardObjs[acc].transactions[trans].value)
            currCat = Accounts.creditCardObjs[acc].transactions[trans].category
            currDate = Accounts.creditCardObjs[acc].transactions[trans].date
            value = value + currValue + getSpace(currValue)
            category = category + currCat + getSpace(currCat)
            date = date + currDate + getSpace(currDate)
            #except:
            #    print("None")
        print(value)
        print(date)
        print(category)

def getSpace(targetStr):
    length = len(targetStr)
    spaces = ""
    while len(spaces) < 15-length:
        spaces = spaces + " "
    return spaces

def generateData():
    transData = {}
    category = ("Feira","Transporte","Remédio","Academia","Aluguel","Condomínio","Telefone","Internet","Luz","Outros")
    conta = ("BB", "NuBank", "Santander","Inter")
    cartoes = ("Santander", "Inter")
    tipo = ("bank", "creditCard")
    Comment = ("Comentário mais longo", "Curto", "Esse seria um comentário imenso")
    acctype = random.choice(tipo)
    if acctype == "bank":
        acc = random.choice(conta)
    else:
        acc = random.choice(cartoes)
    transData={
        'Value':round(random.uniform(-500,500), 2),
        'Category':random.choice(category),
        'Account':acc,
        'Comment':random.choice(Comment),
        'Date':'10/10/2010',
        'AccType':acctype
    }
    return transData

if __name__ == "__main__":
    for i in range(60):
        test = generateData()
        print(test['Value'])