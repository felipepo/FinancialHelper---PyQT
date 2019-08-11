from PySide2 import QtWidgets
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from utilities import funs

class BarChart(FigureCanvas):
    def __init__(self, parent, DataBase):
        self.fig = Figure(figsize=(5, 3),dpi=100)
        super().__init__(self.fig)
        self.DataBase = DataBase
        self.bar_chart = self.figure.subplots()
        allCat = DataBase.category_tbl.readAll()
        self.graphData = {}
        self.catgColors = dict( [(iCatg[1], iCatg[2]) for iCatg in allCat] )

    def fomartGraph(self, categories):
        self.bar_chart.grid(True)
        self.fig.tight_layout()
        self.bar_chart.axis('off')
        self.bar_chart.axhline(0, color="black")
        count = 0
        for iBar in self.barlist:
            iBar.set_color(funs.getHexFromRGB(self.catgColors[categories[count]]))
            height = iBar.get_height()
            self.bar_chart.text(iBar.get_x() + iBar.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom', bbox=dict(boxstyle="square",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   ))
            self.bar_chart.text(iBar.get_x() + iBar.get_width()/2.0, 0, categories[count], ha='center', va='bottom', bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1, 1, 1),
                   ))
            count = count + 1

    def createGraph(self, cards = []):
        self.getCardsData(cards) if (type(cards)==dict) else self.getTableData()
        self.displayData()

    def displayData(self):
        categories = list(self.graphData.keys())
        values = list(self.graphData.values())
        x_np = np.arange(len(categories))
        self.barlist = self.bar_chart.bar(x_np, values)
        self.fomartGraph(categories)

    def getTableData(self):
        _, _, month, year = funs.getDate()
        self.graphData = {}
        allCatg = self.DataBase.category_total_tbl.readAll()
        for iRow in allCatg:
            if iRow[3] == month and iRow[4] == year:
                currCatg = self.DataBase.category_tbl.readById(iRow[1])
                self.graphData[currCatg[1]] = iRow[2]

    def getCardsData(self, cards):
        self.graphData = {}
        for iCard in cards:
            currCategory = cards[iCard].category
            currValue = cards[iCard].value
            if currCategory in self.graphData:
                self.graphData[currCategory] = self.graphData[currCategory] + currValue
            else:
                self.graphData[currCategory] = currValue

    def updateGraph(self, cards=[]):
        self.bar_chart.cla()
        self.createGraph(cards)
        self.bar_chart.figure.canvas.draw()

    def clearGraph(self):
        self.bar_chart.clear()

    def buttonPush(self):
        self.graphData = dict( [(data, self.graphData[data] + 1) for data in self.graphData] )
        print(self.graphData)
        self.clearGraph()
        self.displayData()
        self.bar_chart.figure.canvas.draw()

if __name__ == "__main__":
    from database import sql_class

    plotTest = QtWidgets.QApplication([])

    app = QtWidgets.QFrame()
    DataBase = sql_class.Create(2)

    a = DataBase.extract_tbl.readAll()
    # Month CHART -----------------------
    # Bar Chart - Value x Categories
    chart = BarChart(app, DataBase)
    chart.createGraph()
    updatePlot = QtWidgets.QPushButton(app, text="Testing")

    layout = QtWidgets.QVBoxLayout(app)
    layout.addWidget(chart)
    layout.addWidget(updatePlot)
    # chart.clearGraph()
    # chart.createGraph()

    updatePlot.clicked.connect(chart.buttonPush)
    # Pie Chart - Value/Percentage x Categories

    # Multiple Months CHART -------------
    # Bar Chart - Value(Income/Outcome) x Months
    # Horizontal Bar

    app.show()
    plotTest.exec_()