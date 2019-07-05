import Funs
import os,binascii

'''Classes related to the functioning of the program

    Account
    AllAccounts
    CreditCard
    Transaction
'''
class Categories():
    __slots__ = ("category")
    def __init__(self):
        self.category = {
            "Feira": 'navajo white',
            "Transporte": 'coral',
            "Remédio": 'hot pink',
            "Academia": 'violet red',
            "Aluguel": 'PaleGreen1',
            "Condomínio": 'DarkSlateGray1',
            "Telefone": 'khaki3',
            "Internet": 'LightGoldenrod1',
            "Luz": 'firebrick1',
            "Outros": "yellow"
            }
    
    def AddCategory(self, categoryName, categoryColor):
        self.category[categoryName] = categoryColor

    def RemoveCategory(self, categoryName):
        del self.category[categoryName]

    def UpdateCategory(self, categoryName, categoryColor):
        self.category[categoryName] = categoryColor

class Account():
    #Class to create the accounts
    def __init__(self, parent, name=None):
        self.parent = parent
        self.name = name
        self.totalAmount = 0
        self.transactions = {}

    def UpdateTotal(self, newTotal):
        diff = newTotal - self.totalAmount
        transData = {'Category': 'Outros',
        'Date':Funs.getDate(),
        'Value':diff,
        'Comment':'Atualização de valor'}
        self.AddTransaction(transData)
        
    def AddTransaction(self, transData, transID = "default"):
        try:
            self.totalAmount += float(transData["Value"])
            if transID == "default":
                currTrans = Funs.createID()
            else:
                currTrans = transID
            self.transactions[currTrans] = Transaction(currTrans, transData["Category"], transData["Value"], transData["Date"], transData["Comment"], self.name)
            mon_year = self.transactions[currTrans].month + "_" + self.transactions[currTrans].year
            self.parent.UpdateCategoriesTotal(mon_year, transData["Category"], transData["Value"])
            return currTrans
        except:
            return 'Error'

    def UpdateAccount(self, transID):
        # Get previous Values
        prev_value = float(self.transactions[transID].value)
        prev_mon_year = self.transactions[transID].month + "_" + self.transactions[transID].year
        prev_category = self.transactions[transID].category

        # Update all the necessary parameters before assigning updated values
        self.totalAmount -= prev_value
        self.parent.categoriesTotal[prev_mon_year][prev_category] -= float(prev_value)
        if self.parent.categoriesTotal[prev_mon_year][prev_category] == 0:
            del self.parent.categoriesTotal[prev_mon_year][prev_category]
            if not self.parent.categoriesTotal[prev_mon_year]:
                del self.parent.categoriesTotal[prev_mon_year]

    def RemoveTransaction(self, transID):
        self.UpdateAccount(transID)
        del self.transactions[transID]

    def RenameAccount(self, newName):
        self.name = newName

class Transaction:
    # Class to create a transaction using __slots__, which makes a class faster than a dictionary
    __slots__ = ('transID', 'category', 'value', 'date', 'comment', 'bankAccount', 'month', 'year')
    def __init__(self, transID, cat, val, date, com, acc):
        self.transID = transID
        self.category = cat
        self.value = val
        self.date = date
        self.comment = com
        self.bankAccount = acc
        self.month, self.year = Funs.GetMY(date)

    def Update(self, transData):
        self.category = transData["Category"]
        self.value = transData["Value"]
        self.date = transData["Date"]
        self.comment = transData["Comment"]
        self.month, self.year = Funs.GetMY(transData["Date"])  
#=========================================================================================
class AllAccounts():
    #Class to create an overall account
    def __init__(self):
        self.accountsObjs = {}
        self.creditCardObjs = {}
        self.categoriesTotal = {}

    def UpdateTransaction(self, currTrans, transData, bankAccount, prev_bankAccount, bank_or_creditCard = "bank"):     
        # Assign updated values to target transaction object
        if bankAccount != prev_bankAccount:
            if bank_or_creditCard == "bank":
                self.accountsObjs[prev_bankAccount].RemoveTransaction(currTrans, self)
                self.accountsObjs[bankAccount].AddTransaction(transData, currTrans)
            else:
                self.creditCardObjs[prev_bankAccount].RemoveTransaction(currTrans, self)
                self.creditCardObjs[bankAccount].AddTransaction(transData, currTrans)
        else:
            month, year = Funs.GetMY(transData['Date'])
            mon_year = month + "_" + year
            if bank_or_creditCard == "bank":
                self.callUpdate(self.accountsObjs[bankAccount], transData, currTrans)
            else:
                self.callUpdate(self.accountsObjs[bankAccount], transData, currTrans)
            
            self.UpdateCategoriesTotal(mon_year, transData['Category'], transData['Value'])

    def callUpdate(self, targetObj, transData, currTrans):
        targetObj.UpdateAccount(currTrans)
        targetObj.totalAmount += float(transData['Value'])
        targetObj.transactions[currTrans].Update(transData)

    def UpdateCategoriesTotal(self, mon_year, category, value):
        if mon_year in list(self.categoriesTotal.keys()):
            if category in list(self.categoriesTotal[mon_year].keys()):
                self.categoriesTotal[mon_year][category] += float(value)
            else:
                self.categoriesTotal[mon_year][category] = float(value)
        else:
            self.categoriesTotal[mon_year] = {}
            self.categoriesTotal[mon_year][category] = float(value)

    def AddAcc(self, accName, bank_or_creditCard = "bank"):
        if bank_or_creditCard == "bank":
            if accName in self.accountsObjs:
                return False #Didn't add a new account
            else:
                self.accountsObjs[accName] = Account(self, accName)
                self.accountsObjs[accName].name = accName
                return True #Added a new account
        elif bank_or_creditCard == "creditCard":
            if accName in self.creditCardObjs:
                return False #Didn't add a new credit card
            else:
                self.creditCardObjs[accName] = CreditCard(self, accName)
                self.creditCardObjs[accName].name = accName
                return True #Added a new credit card
        
    def DelAcc(self, accName, bank_or_creditCard = "bank"):
        if bank_or_creditCard == "bank":
            if accName in self.accountsObjs:
                del self.accountsObjs[accName]
                return True #Removed item from dictionary
            else:
                return False #Didn't remove item from dictionary
        elif bank_or_creditCard == "creditCard":
            if accName in self.creditCardObjs:
                del self.creditCardObjs[accName]
                return True #Removed item from dictionary
            else:
                return False #Didn't remove item from dictionary

#=========================================================================================
class CreditCard(Account):
    #Class to create the credit cards accounts
    def __init__(self, parent, name=None):
        super().__init__(parent, name)
        self.limit = 0

#=========================================================================================     
if __name__ == "__main__":
    #Create all accounts
    allAcc = AllAccounts()

    #Add transaction when there is no accounts
    #allAcc.AddTransaction(transData)
    transData = {'Category': 'Food',
    'Date':"05/03/2015",
    'Value':50,
    'Comment':'BK'}
    transData1 = {'Category': 'Feira',
    'Date':"05/03/2015",
    'Value':50,
    'Comment':'BK'}
    transData2 = {'Category': 'Remédio',
    'Date':"05/03/2015",
    'Value':50,
    'Comment':'BK'}

    #Add Account
    allAcc.AddAcc("BB")
    #Add transaction to an account that doesn't exist
    #allAcc.AddTransaction(transData)

    allAcc.AddAcc("Santander")
    allAcc.accountsObjs["BB"].AddTransaction(transData)
    allAcc.accountsObjs["Santander"].AddTransaction(transData)
    allAcc.accountsObjs["BB"].AddTransaction(transData1)
    allAcc.accountsObjs["Santander"].AddTransaction(transData)
    allAcc.accountsObjs["BB"].AddTransaction(transData2)
    allAcc.accountsObjs["Santander"].AddTransaction(transData)
    allAcc.accountsObjs["BB"].AddTransaction(transData1)
    allAcc.accountsObjs["Santander"].AddTransaction(transData)
    allAcc.accountsObjs["BB"].AddTransaction(transData)
    allAcc.accountsObjs["Santander"].AddTransaction(transData)
    allAcc.accountsObjs["BB"].AddTransaction(transData1)
    allAcc.accountsObjs["Santander"].AddTransaction(transData)


    #Check all accounts attributes
    print(allAcc.accountsObjs)
    #Funs.showdic(allAcc.transactions)
    print(allAcc.accountsObjs["BB"].transactions.keys())
    allKeys = list(allAcc.accountsObjs["BB"].transactions.keys())
    print(allKeys)
    print(allAcc.accountsObjs["BB"].name)
    allAcc.accountsObjs["BB"].RenameAccount("ASD")
    print(allAcc.accountsObjs["BB"].name)
    print(allAcc.accountsObjs["BB"].transactions[allKeys[0]].bankAccount)
    #Check specific accounts attributes
    print(allAcc.accountsObjs["BB"].totalAmount)
    print(allAcc.accountsObjs["Santander"].totalAmount)
    #Funs.showdic(allAcc.accountsObjs["Santander"].transactions)
