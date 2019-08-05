from PySide2 import QtWidgets
import matplotlib.pyplot as plt
import numpy as np

class BarChart():
    def __init__(self, parent, xLbls, yValues):
        # super().__init__(parent)
        plt.bar(xLbls, yValues, color="green")
        plt.show()

if __name__ == "__main__":
    Categories = ["Cat1", "Cat2", "Cat3"]
    Values = [4, 2, -6]
    plotTest = QtWidgets.QApplication([])

    app = QtWidgets.QWidget()

    # Month CHART -----------------------
    # Bar Chart - Value x Categories
    BarChart(app, Categories, Values)
    # Pie Chart - Value/Percentage x Categories

    # Multiple Months CHART -------------
    # Bar Chart - Value(Income/Outcome) x Months
    # Horizontal Bar

    app.show()
    plotTest.exec_()