import Funs
import os,binascii

'''Classes related to the functioning of the program

    Account
    AllAccounts
    CreditCard
    Transaction
'''

class Account:
    #Class to create the accounts
    def __init__(self):
        self.name = None
        self.totalAmount = 0
        self.transactions = {}

    def AddTransaction(self, category, value, date, comment, bankAccount,transID = "default"):
        self.totalAmount += float(value)
        if transID == "default":
            currTrans = binascii.b2a_hex(os.urandom(15))
        else:
            currTrans = transID
        self.transactions[currTrans] = Transaction(currTrans, category, value, date, comment, bankAccount)
        return currTrans

    def UpdateTransaction(self, currTrans, allAcc):
        # Get previous Values
        prev_value = float(self.transactions[currTrans].value)
        prev_mon_year = self.transactions[currTrans].month + "_" + self.transactions[currTrans].year
        prev_category = self.transactions[currTrans].category

        # Update all the necessary parameters before assigning updated values
        self.totalAmount -= prev_value
        allAcc.categoriesTotal[prev_mon_year][prev_category] -= float(prev_value)
        if allAcc.categoriesTotal[prev_mon_year][prev_category] == 0:
            del allAcc.categoriesTotal[prev_mon_year][prev_category]
            if not allAcc.categoriesTotal[prev_mon_year]:
                del allAcc.categoriesTotal[prev_mon_year]

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

    def Update(self, cat, val, date, com, acc):
        self.category = cat
        self.value = val
        self.date = date
        self.comment = com
        self.bankAccount = acc
        self.month, self.year = Funs.GetMY(date)
    
#=========================================================================================
class AllAccounts():
    #Class to create an overall account
    def __init__(self):
        Account.__init__(self)
        self.accountsObjs = {}
        self.creditCardObjs = {}
        self.categoriesTotal = {}
        self.categoriesColor = {
            "Feira": 'navajo white',
            "Transporte": 'coral',
            "Remédio": 'hot pink',
            "Academia": 'violet red',
            "Aluguel": 'PaleGreen1',
            "Condomínio": 'DarkSlateGray1',
            "Telefone": 'khaki3',
            "Internet": 'LightGoldenrod1',
            "Luz": 'firebrick1',
            }

    def AddTransaction(self, category, value, date, comment, bankAccount,transID = "default", bank_or_creditCard = "bank"):
        matched = Funs.checkDate(date)
        if not matched:
            return False
        else:
            if bank_or_creditCard == "bank":
                addedFlag = self.accountsObjs[bankAccount].AddTransaction(category, value, date, comment, bankAccount,transID)
            else:
                addedFlag = self.creditCardObjs[bankAccount].AddTransaction(category, value, date, comment, bankAccount,transID)
            if addedFlag:
                currTrans = addedFlag
                if bank_or_creditCard == "bank":
                    mon_year = self.accountsObjs[bankAccount].transactions[currTrans].month + "_" + self.accountsObjs[bankAccount].transactions[currTrans].year
                else:
                    mon_year = self.creditCardObjs[bankAccount].transactions[currTrans].month + "_" + self.creditCardObjs[bankAccount].transactions[currTrans].year
                self.UpdateCategoriesTotal(mon_year, category, value)
                return currTrans
            else:
                return False
    
    def UpdateTransaction(self, currTrans, category, value, date, comment, bankAccount, prev_bankAccount, bank_or_creditCard = "bank"):
        matched = Funs.checkDate(date)
        if not matched:
            return False
        else:
            if bank_or_creditCard == "bank":
                self.accountsObjs[prev_bankAccount].UpdateTransaction(currTrans, self)
            else:
                self.creditCardObjs[prev_bankAccount].UpdateTransaction(currTrans, self)
            
            # Assign updated values to target transaction object
            if bankAccount != prev_bankAccount:
                if bank_or_creditCard == "bank":
                    self.AddTransaction(category, value, date, comment, bankAccount, currTrans, "bank")
                    del self.accountsObjs[prev_bankAccount].transactions[currTrans]
                else:
                    self.AddTransaction(category, value, date, comment, bankAccount, currTrans, "creditCard")
                    del self.creditCardObjs[prev_bankAccount].transactions[currTrans]
            else:
                month, year = Funs.GetMY(date)
                mon_year = month + "_" + year
                if bank_or_creditCard == "bank":
                    self.accountsObjs[bankAccount].totalAmount += float(value)
                    self.accountsObjs[bankAccount].transactions[currTrans].Update(category, value, date, comment, bankAccount)
                else:
                    self.creditCardObjs[bankAccount].totalExpenses += float(value)
                    self.creditCardObjs[bankAccount].transactions[currTrans].Update(category, value, date, comment, bankAccount)
                
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
                self.accountsObjs[accName] = Account()
                self.accountsObjs[accName].name = accName
                return True #Added a new account
        elif bank_or_creditCard == "creditCard":
            if accName in self.creditCardObjs:
                return False #Didn't add a new credit card
            else:
                self.creditCardObjs[accName] = CreditCard()
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
class CreditCard():
    #Class to create the credit cards accounts
    def __init__(self):
        self.name = None
        self.limit = 0
        self.transactions = {}
        self.totalExpenses = 0

    def AddTransaction(self, category, value, date, comment, bankAccount,transID = "default"):
        self.totalExpenses += float(value)
        if transID == "default":
            currTrans = binascii.b2a_hex(os.urandom(15))
        else:
            currTrans = transID
        self.transactions[currTrans] = Transaction(currTrans, category, value, date, comment, bankAccount)
        return currTrans
   
    def UpdateTransaction(self, currTrans, allAcc):
        # Get previous Values
        prev_value = float(self.transactions[currTrans].value)
        prev_mon_year = self.transactions[currTrans].month + "_" + self.transactions[currTrans].year
        prev_category = self.transactions[currTrans].category

        # Update all the necessary parameters before assigning updated values
        self.totalExpenses -= prev_value
        allAcc.categoriesTotal[prev_mon_year][prev_category] -= float(prev_value)
        if allAcc.categoriesTotal[prev_mon_year][prev_category] == 0:
            del allAcc.categoriesTotal[prev_mon_year][prev_category]
            if not allAcc.categoriesTotal[prev_mon_year]:
                del allAcc.categoriesTotal[prev_mon_year]

#=========================================================================================     
if __name__ == "__main__":
    #Create all accounts
    allAcc = AllAccounts()

    #Add transaction when there is no accounts
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","BB")

    #Add Account
    allAcc.AddAcc("BB")
    #Add transaction to an account that doesn't exist
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")

    allAcc.AddAcc("Santander")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","BB")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.AddTransaction("Feira",50,"05/03/2015","BK","BB")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.AddTransaction("Remédio",50,"05/03/2015","BK","BB")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.AddTransaction("Feira",50,"05/03/2015","BK","BB")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","BB")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.AddTransaction("Feira",50,"05/03/2015","BK","BB")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")


    #Check all accounts attributes
    print(allAcc.accountsObjs)
    #Funs.showdic(allAcc.transactions)
    print(allAcc.accountsObjs["BB"].transactions.keys())

    #Check specific accounts attributes
    print(allAcc.accountsObjs["BB"].totalAmount)
    #Funs.showdic(allAcc.accountsObjs["Santander"].transactions)
