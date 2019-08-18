from PySide2 import QtWidgets, QtCore
from decimal import Decimal

class MonthlyProfitTable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__(12,5)

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
                    total = self.comma(numerator/denominator)
                    test = QtWidgets.QTableWidgetItem(total)
                self.setItem(iRow,iCol,test)
            perc += 0.001
        self.setHorizontalHeaderLabels(self.columnLabels)

    def comma(self, num):
        '''Add comma to every 3rd digit. Takes int or float and
        returns string.'''
        if type(num) == int:
            return '{:,}'.format(num)
        elif type(num) == float:
            return '{:,.2f}'.format(num) # Rounds to 2 decimal places
        else:
            print("Need int or float as input to function comma()!")