import pickle
import time
import re
import os,binascii

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
        for y in dict[x]:
            print ('               ',y,':',dict[x][y])
   
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