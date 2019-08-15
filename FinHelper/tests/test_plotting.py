from ..utilities import plotting
from PySide2 import QtWidgets
from ..database import sql_class
print(__name__)

def run_test():
    print("Testing Plots")

    plotTest = QtWidgets.QApplication([])

    app = QtWidgets.QFrame()
    DataBase = sql_class.Create(2)

    # Month CHART -----------------------
    # Bar Chart - Value x Categories
    chart = plotting.BarChart(DataBase)
    chart.createGraph()
    updatePlot = QtWidgets.QPushButton(app, text="Testing")
    updatePlot.clicked.connect(chart.buttonPush)

    layout = QtWidgets.QVBoxLayout(app)
    layout.addWidget(chart)
    layout.addWidget(updatePlot)

    # Pie Chart - Value/Percentage x Categories
    # Multiple Months CHART -------------
    # Bar Chart - Value(Income/Outcome) x Months
    # Horizontal Bar

    app.show()
    plotTest.exec_()

if __name__ == "__main__":
    run_test()