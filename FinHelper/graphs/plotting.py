from PySide2 import QtWidgets
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from ..utilities import funs, generate

class HorBarChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(0.5, 0.5),dpi=100)
        super().__init__(self.fig)
        self.bar_chart = self.figure.subplots()
        self.budget = generate.generateBudget()

    def formatGraph(self):
        self.bar_chart.axis('off')
        self.bar_chart.set_yticks([1])
        self.bar_chart.invert_yaxis()
        self.fig.tight_layout()

        # Set up the legend so it is arranged across the top of the chart.
        anchor_vals = (0.01, 0.6, 0.95, 0.2)
        # self.fig.legend(bbox_to_anchor=anchor_vals, loc=4, ncol=4, mode="expand", borderaxespad=0.0)

    def createGraph(self):
        self.displayData()

    def displayData(self):
        categories = list(self.budget.keys())
        x_np = np.arange(len(categories))
        # Sum up the value total.
        outer_bar_length = 0
        for iCatg in categories:
            outer_bar_length += self.budget[iCatg][1]
        outer_bar_label = 'Budget'
        # In this case we expect only 1 item in the entries list.
        y_pos = [0]
        width = 0.5
        # self.bar_chart.barh(y_pos, 0, 1.0, align='center', color='white', ecolor='black', label=None)
        # Is there an 'outer' or container bar?
        # if outer_bar_length != -1:
        #     self.bar_chart.barh(y_pos, outer_bar_length, 0.12, align='center', color='#D9DCDE', label=outer_bar_label, left=0)
        left_pos = 0
        for iCatg in categories:
            seglabel = iCatg
            segval = self.budget[iCatg][1]
            segcol = funs.getHexFromRGB(self.budget[iCatg][0])

            self.bar_chart.barh(y_pos, [segval], width, align='center', color=segcol, label=seglabel, left=left_pos, edgecolor=['black', 'black'], linewidth=0.5)
            left_pos += segval
        self.formatGraph()

class BarChart(FigureCanvas):
    def __init__(self, DataBase):
        self.fig = Figure(figsize=(5, 3),dpi=100)
        super().__init__(self.fig)
        self.DataBase = DataBase
        self.bar_chart = self.figure.subplots()
        allCat = DataBase.category_tbl.readAll()
        self.graphData = {}
        self.catgColors = dict( [(iCatg[1], iCatg[2]) for iCatg in allCat] )

    def formatGraph(self, categories):
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
        self.formatGraph(categories)

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
        allCat = self.DataBase.category_tbl.readAll()
        self.catgColors = dict( [(iCatg[1], iCatg[2]) for iCatg in allCat] )
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