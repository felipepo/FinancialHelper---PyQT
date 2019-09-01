from ..Graphs import plotting
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
    val_x_catg = plotting.BarChart(DataBase)
    val_x_catg.createGraph()

    # Pie Chart - Value/Percentage x Categories
    # Multiple Months CHART -------------
    # Bar Chart - Value(Income/Outcome) x Months
    # Horizontal Bar - Bugeting
    buget_bar = plotting.HorBarChart()
    buget_bar.createGraph()

    # General Interface setup
    updatePlot = QtWidgets.QPushButton(app, text="Testing")
    updatePlot.clicked.connect(val_x_catg.buttonPush)

    layout = QtWidgets.QVBoxLayout(app)
    layout.addWidget(val_x_catg)
    layout.addWidget(buget_bar)
    layout.addWidget(updatePlot)

    app.show()
    plotTest.exec_()

if __name__ == "__main__":
    run_test()