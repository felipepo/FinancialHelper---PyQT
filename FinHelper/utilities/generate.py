import random

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

def generateBudget():
    budget = {}
    category = ("Feira","Transporte","Remédio","Academia","Aluguel","Condomínio","Telefone","Internet","Luz","Outros", "Transferência")
    for iColor in category:
        color = 'rgb({}, {}, {})'.format(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        budget[iColor] = (color, random.randint(0, 1000))
    return budget
