import time
import re
import os
import binascii
import unidecode
from pathlib import Path

'''
General Functions
	showdic
	AddTransaction
	GetMY
	saveData
	loadData
'''

def checkFolderExist():
    parentPath = getFinHelperPath()
    dataFolder = "{}/data".format(parentPath)
    imagesFolder = "{}/data/images".format(parentPath)
    sqlFolder = "{}/data/sql".format(parentPath)
    styleFolder = "{}/data/style".format(parentPath)
    if not os.path.exists(dataFolder):
        os.makedirs(dataFolder)
        os.makedirs(imagesFolder)
        os.makedirs(sqlFolder)
        os.makedirs(styleFolder)
        print("Create data folder")
    if not os.path.exists(imagesFolder):
        os.makedirs(imagesFolder)
        print("Created ../data/images folder")
    if not os.path.exists(sqlFolder):
        os.makedirs(sqlFolder)
        print("Created ../data/sql folder")
    if not os.path.exists(styleFolder):
        os.makedirs(styleFolder)
        print("Created ../data/style folder")

def getFinHelperPath():
    currFilePath = __file__
    finHelperFolder = Path(Path(currFilePath).parent).parent
    finHelperFolder = os.fspath(finHelperFolder)
    finHelperFolder = finHelperFolder.replace("\\","/")
    return finHelperFolder

def formatCategoryName(name):
    return unidecode.unidecode(name.replace(' ', '_'))

def testCategoryName(name):
    return "Not OK" if re.search(r"\.|\/|\&", name) else 'OK'

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
    return dateVal, clk[2], clk[1], clk[0]

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

def getHexFromRGB(rgbString):
    rgbString = rgbString.replace('rgb','').replace('(','').replace(')','')
    rgbSplit = rgbString.split(',')
    red = int(rgbSplit[0])
    green = int(rgbSplit[1])
    blue = int(rgbSplit[2])
    return '#{:02x}{:02x}{:02x}'.format( red, green , blue )

def shift(input):
    try:
        dotPost = -2
        input = input.replace('.','')
    except:
        dotPost = -2
    result =  '{}.{}'.format(input[:dotPost], input[dotPost:])
    if result[0] == '0':
        result = result[1:]
    if result[0] == '.':
        result = "0" + result
    return result

if __name__ == "__main__":
    datapath = getDataPath()
    print(datapath)
    # for i in range(60):
    #     test = generateTrans(tuple(range(8)),tuple(range(8)))
    #     test = generateCatgTotal(tuple(range(40)))
    #     print(test['Date'])
    #     test = generateAcc()
    #     print(test)