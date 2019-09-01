from PySide2 import QtWidgets, QtCore
from decimal import Decimal

def comma(num):
    '''Add comma to every 3rd digit. Takes int or float and
    returns string.'''
    if type(num) == int:
        return '{:,}'.format(num)
    elif type(num) == float:
        return '{:,.2f}'.format(num) # Rounds to 2 decimal places
    else:
        print("Need int or float as input to function comma()!")

class MonthlyProfitTable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__(13,3)
        self.columnLabels = ["Lucro Mensal","Lucro Total","Montante"]
        self.setHorizontalHeaderLabels(self.columnLabels)
        self.rowLabels = ["Meses","","","","","","","","","","","",""]
        self.setVerticalHeaderLabels(self.rowLabels)
        self.fill_table(25, 0.004)

    def fill_table(self, offset, percentage):
        init = 1400
        nMonths = 1 + 12*offset
        monthly = 300
        prevAmount = init*((1+percentage)**(nMonths-1)) + monthly * ((((1+percentage)**((nMonths-1)+1)-1)/percentage)-1)
        totalAmount = init*((1+percentage)**nMonths) + monthly * ((((1+percentage)**(nMonths+1)-1)/percentage)-1)
        monthlyProfit = totalAmount-monthly-prevAmount
        totalProfit = totalAmount-monthly*nMonths-init
        self.setItem(1,0,QtWidgets.QTableWidgetItem(comma(monthlyProfit)))
        self.setItem(1,1,QtWidgets.QTableWidgetItem(comma(totalProfit)))
        self.setItem(1,2,QtWidgets.QTableWidgetItem(comma(totalAmount)))
        self.rowLabels[1] = comma(nMonths)
        for iRow in range(2,13):
            nMonths += 1
            prevAmount = totalAmount
            totalAmount = init*((1+percentage)**nMonths) + monthly * ((((1+percentage)**(nMonths+1)-1)/percentage)-1)
            monthlyProfit = totalAmount-monthly-prevAmount
            totalProfit = totalAmount-monthly*nMonths-init
            self.setItem(iRow,0,QtWidgets.QTableWidgetItem(comma(monthlyProfit)))
            self.setItem(iRow,1,QtWidgets.QTableWidgetItem(comma(totalProfit)))
            self.setItem(iRow,2,QtWidgets.QTableWidgetItem(comma(totalAmount)))
            self.rowLabels[iRow] = comma(nMonths)
        self.setVerticalHeaderLabels(self.rowLabels)

class ContributionTable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__(12,5)
        self.columnLabels = ["","","","",""]
        self.rowLabels = ["0.4%","0.5%","0.6%","0.7%","0.8%","0.9%","1.0%","1.1%","1.2%","1.3%","1.4%","1.5%"]
        self.setVerticalHeaderLabels(self.rowLabels)

    def fill_table(self, offset, goal):
        perc = 0.004
        init = 0
        for iRow in range(12):
            for iCol in range(5):
                year = (iCol + 1 + offset)
                if year == 1:
                    self.columnLabels[iCol] = "{} ano{}".format(year, "")
                else:
                    self.columnLabels[iCol] = "{} ano{}".format(year, "s")
                totalMonths = year*12
                currPerc = 1 + perc
                if (init*(currPerc**totalMonths)) >= goal:
                    test = QtWidgets.QTableWidgetItem(0)
                else:
                    numerator = goal - init*(currPerc**totalMonths)
                    denominator = ((currPerc**(totalMonths+1) - 1) / perc) - 1
                    total = comma(numerator/denominator)
                    test = QtWidgets.QTableWidgetItem(total)
                self.setItem(iRow,iCol,test)
            perc += 0.001
        self.setHorizontalHeaderLabels(self.columnLabels)