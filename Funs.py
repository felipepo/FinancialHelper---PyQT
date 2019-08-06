import pickle
import time
import re
import os,binascii
import random
import sys
import unidecode

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

def formatCategoryName(name):
    return unidecode.unidecode(name.replace(' ', '_'))

def testCategoryName(name):
    return "Not OK" if re.search(r"\.|\/|\&", name) else 'OK'

def shift(input):

    # slice string in two parts for left and right
    dotPost = input.index('.') + 1
    input = input.replace('.','')
    result =  '{}.{}'.format(input[:dotPost], input[dotPost:])
    if result[0] == '0':
        result = result[1:]
    return result
#=========================================================================================
def GetMY(date):
    months = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")
    splitDate = date.split("/")
    month = months[int(splitDate[1])-1]
    year = splitDate[2]
    return month, year
#=========================================================================================
def GetMonth(month):
    if type(month) is int:
        result = {1:"Janeiro", 2:"Fevereiro", 3:"Março", 4:"Abril", 5:"Maio", 6:"Junho", 7:"Julho", 8:"Agosto", 9:"Setembro", 10:"Outubro", 11:"Novembro", 12:"Dezembro"}
        return result[month]
    else:
        result = {"Janeiro":1, "Fevereiro":2, "Março":3, "Abril":4, "Maio":5, "Junho":6, "Julho":7, "Agosto":8, "Setembro":9, "Outubro":10, "Novembro":11, "Dezembro":12}
        return result[month]

#=========================================================================================
def getDate():
    clk = list(time.localtime())
    day = "0" + str(clk[2]) if len(str(clk[2])) == 1 else str(clk[2])
    month = "0" + str(clk[1]) if len(str(clk[1])) == 1 else str(clk[1])
    year = str(clk[0])
    dateVal = "{}/{}/{}".format(day, month, year)
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

def generateCatg(rand="on"):
    catgData = {}
    category = ("Feira","Transporte","Remédio","Academia","Aluguel","Condomínio","Telefone","Internet","Luz","Outros", "Transferência")

    if rand == "on":
        color = 'rgb({}, {}, {})'.format(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        catgData={
            'Name': random.choice(category),
            'Color': color
        }
    else:
        for iColor in category:
            color = 'rgb({}, {}, {})'.format(random.randint(0,255), random.randint(0,255), random.randint(0,255))
            catgData[iColor] = color
    return catgData

def generateCatgTotal(Catg_ID_list):
    catgTotalData = {}
    month = random.randint(1,12)
    year = random.randint(2017,2019)

    catgTotalData={
        'Catg_ID': random.choice(Catg_ID_list),
        'Total': round(random.uniform(-500,500), 2),
        'Month': month,
        'Year': year
    }
    return catgTotalData

def generateAcc():
    accData = {}
    limit = None
    dueday = None
    closingday = None
    accType = (1, 2) # 1 = Debit; 2 = Credit
    accName = ("BB", "NuBank", "Santander","Inter")
    currType = random.choice(accType)
    if currType == 2:
        limit = round(random.uniform(-500,500), 2)
        dueday = random.randint(1,28)
        closingday = dueday - 10
        if (dueday - 10) < 1:
            closingday = closingday + 28

    accData={
        'Type': currType,
        'Name': random.choice(accName),
        'Total': 0,#round(random.uniform(-500,500), 2),
        'Limit':limit,
        'DueDay':dueday,
        'ClosingDay':closingday
    }
    return accData

def generateTrans(Catg_ID_list, Acc_ID_list):
    transData = {}
    Comment = ("Comentário mais longo", "Curto", "Esse seria um comentário imenso")
    month = random.randint(1,12)
    year = random.randint(2017,2019)
    if month == 2:
        day = random.randint(1,28)
    elif month in (1,3,5,7,8,10,12):
        day = random.randint(1,31)
    else:
        day = random.randint(1,30)
    date = "{}/{}/{}".format(day, month, year)
    transData={
        'Catg_ID': random.choice(Catg_ID_list),
        'Acc_ID': random.choice(Acc_ID_list),
        'Value':round(random.uniform(-500,500), 2),
        'Comment':random.choice(Comment),
        'Date':date
    }
    return transData

def checkFilter(transData, filters):
    # Tipos de filtros:
    # Mês
    # Ano
    # Conta
    # Categoria

    passedTest = 1
    month, year = GetMY(transData["Date"])
    if month != filters["Month"] and filters["Month"] != "Todos":
        passedTest = 0
    if year != filters["Year"] and filters["Year"] != "Todos":
        passedTest = 0
    if transData["AccName"] != filters["AccName"] and filters["AccName"] != "Todas":
        passedTest = 0
    if transData["Category"] != filters["Category"] and filters["Category"] != "Todas":
        passedTest = 0
    return passedTest


def trans_dictFromlist(transList):
    transDict = {
        'Trans_ID': transList[0],
        'Catg_ID': transList[1],
        'Acc_ID': transList[2],
        'Date': transList[3],
        'Value': transList[4],
        'Comment': transList[5]
    }
    return transDict

def catgTotal_dictFromlist(catgTotalList):
    catgTotalDict = {
        'Total_Catg_ID': catgTotalList[0],
        'Catg_ID': catgTotalList[1],
        'Total': catgTotalList[2],
        'Month': catgTotalList[3],
        'Year': catgTotalList[4]
    }
    return catgTotalDict

def account_dictFromlist(accountList):
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

def getHexFromRGB(rgbString):
    rgbString = rgbString.replace('rgb','').replace('(','').replace(')','')
    rgbSplit = rgbString.split(',')
    red = int(rgbSplit[0])
    green = int(rgbSplit[1])
    blue = int(rgbSplit[2])
    return '#{:02x}{:02x}{:02x}'.format( red, green , blue )

if __name__ == "__main__":
    print(getHexFromRGB('rgb(100,100,100)'))
    # print(testCategoryName('Cartão po'))
    # print(formatCategoryName('Remédio Cartão'))
    # sys.path.append("C:/Users/felip/AppData/Roaming/Python/Python37/Scripts")
    # for i in range(60):
    #     test = generateTrans(tuple(range(8)),tuple(range(8)))
    #     test = generateCatgTotal(tuple(range(40)))
    #     print(test['Date'])
    #     test = generateAcc()
    #     print(test)