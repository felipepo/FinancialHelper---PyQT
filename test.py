from FinHelper import tests
from PySide2 import QtWidgets

def manuallyChoose(chosenTest):
    if chosenTest == 1: # Test plots
        tests.test_plotting.run_test()
    elif chosenTest == 2: # Test sql - database
        tests.test_sql.run_test()
    elif chosenTest == 3: # Test adding account window
        tests.test_acc_win.run_test()
    elif chosenTest == 4: # Test transaction window
        tests.test_trans_win.run_test()
    elif chosenTest == 5: # Test plots
        tests.test_aux_table.run_test()
    elif chosenTest == 6: # Test Stock
        tests.test_request.run_test()
    elif chosenTest == 7: # Test plots
        tests.test_sql.run_test()
    elif chosenTest == 8: # Test plots
        tests.test_sql.run_test()

def autoChoose():
    app = QtWidgets.QApplication([])
    main = QtWidgets.QFrame()
    verticalLayout = QtWidgets.QVBoxLayout(main)
    testButton = QtWidgets.QPushButton(main, text="Test Plots")
    testButton.clicked.connect(run_test)
    verticalLayout.addWidget(testButton)
    main.show()
    app.exec_()

def run_test():
    QtWidgets.QApplication.instance().quit()
    tests.test_plotting.run_test()

if __name__ == "__main__":
    chosenTest = 6
    manuallyChoose(chosenTest)
    # autoChoose()