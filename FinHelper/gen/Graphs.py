# from PySide2 import QtWidgets, QtCore, QtGui
# import sys
# import matplotlib
# matplotlib.use('Qt5Agg')
# import pylab

# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

def my_plotter(ax, data1, data2, param_dict):
    """
    A helper function to make a graph

    Parameters
    ----------
    ax : Axes
        The axes to draw to

    data1 : array
       The x data

    data2 : array
       The y data

    param_dict : dict
       Dictionary of kwargs to pass to ax.plot

    Returns
    -------
    out : list
        list of artists added
    """
    out = ax.plot(data1, data2, **param_dict)
    return out

if __name__ == '__main__':
    # PySide Example ======================================================
    # app = QtWidgets.QApplication(sys.argv)

    # # generate the plot
    # fig = Figure(figsize=(600,600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
    # ax = fig.add_subplot(111)
    # ax.plot([0,1])
    # # generate the canvas to display the plot
    # canvas = FigureCanvas(fig)

    # win = QtWidgets.QMainWindow()
    # # add the plot canvas to a window
    # win.setCentralWidget(canvas)

    # win.show()

    # sys.exit(app.exec_())

    # Example 1======================================================
    # fig = plt.figure()  # an empty figure with no axes
    # fig.suptitle('No axes on this figure')  # Add a title so we know which it is

    # fig, ax_lst = plt.subplots(2, 2)  # a figure with a 2x2 grid of Axes
    # plt.show()
    # Example 2======================================================
    # x = np.linspace(0, 2, 100)
    # print(x)

    # plt.plot(x, x, label='linear')
    # plt.plot(x, x**2, label='quadratic')
    # plt.plot(x, x**3, label='cubic')

    # plt.xlabel('x label')
    # plt.ylabel('y label')

    # plt.title("Simple Plot")

    # plt.legend()
    # plt.show()
    # Example 3======================================================
    # x = np.arange(0, 10, 0.2)

    # y = np.sin(x)
    # fig, ax = plt.subplots()
    # ax.plot(x, y)
    # plt.show()

    # Example 4======================================================
    # data1, data2, data3, data4 = np.random.randn(4, 100)
    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # my_plotter(ax1, data1, data2, {'marker': 'x'})
    # my_plotter(ax2, data3, data4, {'marker': 'o'})
    # plt.show()
    
    # Example 5 - Interactive Plot ======================================================
    # Only works in python IDLE if interactive is on
    # plt.ion()
    plt.plot([1.6, 2.7])
    plt.title("interactive test")
    plt.xlabel("index")
    ax = plt.gca()
    ax.plot([3.1, 2.2])
    # plt.draw() # Re draw plot

    # plt.ioff()
    # plt.plot([1.6, 2.7])
    plt.show() # Blocks any further code. Only advances after plot is closed
    print('oi')