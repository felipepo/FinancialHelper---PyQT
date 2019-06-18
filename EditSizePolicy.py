from PySide2 import QtWidgets

class SizePolicy(QtWidgets.QSizePolicy):
    def __init__(self, horizontalPolicy, verticalPolicy):
        super().__init__(horizontalPolicy, verticalPolicy)
