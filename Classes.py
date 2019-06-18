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
        self.AddTransaction('Outros', diff, Funs.getDate(), "Atualização de valor")
        
    def AddTransaction(self, category, value, date, comment,transID = "default"):
        matched = Funs.checkDate(date)
        if not matched:
            return False
        else:
            self.totalAmount += float(value)
            if transID == "default":
                currTrans = Funs.createID()
            else:
                currTrans = transID
            self.transactions[currTrans] = Transaction(currTrans, category, value, date, comment, self.name)
            mon_year = self.transactions[currTrans].month + "_" + self.transactions[currTrans].year
            self.parent.UpdateCategoriesTotal(mon_year, category, value)
            return currTrans

    def UpdateAccount(self, transID, allAcc):
        # Get previous Values
        prev_value = float(self.transactions[transID].value)
        prev_mon_year = self.transactions[transID].month + "_" + self.transactions[transID].year
        prev_category = self.transactions[transID].category

        # Update all the necessary parameters before assigning updated values
        self.totalAmount -= prev_value
        allAcc.categoriesTotal[prev_mon_year][prev_category] -= float(prev_value)
        if allAcc.categoriesTotal[prev_mon_year][prev_category] == 0:
            del allAcc.categoriesTotal[prev_mon_year][prev_category]
            if not allAcc.categoriesTotal[prev_mon_year]:
                del allAcc.categoriesTotal[prev_mon_year]

    def RemoveTransaction(self, transID, allAcc):
        self.UpdateAccount(transID, allAcc)
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

    def Update(self, cat, val, date, com):
        self.category = cat
        self.value = val
        self.date = date
        self.comment = com
        self.month, self.year = Funs.GetMY(date)
    
#=========================================================================================
class AllAccounts():
    #Class to create an overall account
    def __init__(self):
        self.accountsObjs = {}
        self.creditCardObjs = {}
        self.categoriesTotal = {}

    def UpdateTransaction(self, currTrans, category, value, date, comment, bankAccount, prev_bankAccount, bank_or_creditCard = "bank"):
        matched = Funs.checkDate(date)
        if not matched:
            return False
        else:
            
            # Assign updated values to target transaction object
            if bankAccount != prev_bankAccount:
                if bank_or_creditCard == "bank":
                    self.accountsObjs[bankAccount].RemoveTransaction(currTrans, self)
                    self.accountsObjs[bankAccount].AddTransaction(category, value, date, comment, currTrans, "bank")
                else:
                    self.creditCardObjs[bankAccount].RemoveTransaction(currTrans, self)
                    self.creditCardObjs[bankAccount].AddTransaction(category, value, date, comment, currTrans, "creditCard")
            else:
                month, year = Funs.GetMY(date)
                mon_year = month + "_" + year
                if bank_or_creditCard == "bank":
                    self.accountsObjs[prev_bankAccount].UpdateAccount(currTrans, self)
                    self.accountsObjs[bankAccount].totalAmount += float(value)
                    self.accountsObjs[bankAccount].transactions[currTrans].Update(category, value, date, comment, self.accountsObjs[bankAccount].name)
                else:
                    self.creditCardObjs[prev_bankAccount].UpdateAccount(currTrans, self)
                    self.creditCardObjs[bankAccount].totalAmount += float(value)
                    self.creditCardObjs[bankAccount].transactions[currTrans].Update(category, value, date, comment, self.creditCardObjs[bankAccount].name)
                
                self.UpdateCategoriesTotal(mon_year, category, value)
            return True

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
    #allAcc.AddTransaction("Food",50,"05/03/2015","BK","BB")

    #Add Account
    allAcc.AddAcc("BB")
    #Add transaction to an account that doesn't exist
    #allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")

    allAcc.AddAcc("Santander")
    allAcc.accountsObjs["BB"].AddTransaction("Food",50,"05/03/2015","BK","BB")
    allAcc.accountsObjs["Santander"].AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.accountsObjs["BB"].AddTransaction("Feira",50,"05/03/2015","BK","BB")
    allAcc.accountsObjs["Santander"].AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.accountsObjs["BB"].AddTransaction("Remédio",50,"05/03/2015","BK","BB")
    allAcc.accountsObjs["Santander"].AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.accountsObjs["BB"].AddTransaction("Feira",50,"05/03/2015","BK","BB")
    allAcc.accountsObjs["Santander"].AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.accountsObjs["BB"].AddTransaction("Food",50,"05/03/2015","BK","BB")
    allAcc.accountsObjs["Santander"].AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.accountsObjs["BB"].AddTransaction("Feira",50,"05/03/2015","BK","BB")
    allAcc.accountsObjs["Santander"].AddTransaction("Food",50,"05/03/2015","BK","Santander")


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
    #Funs.showdic(allAcc.accountsObjs["Santander"].transactions)
