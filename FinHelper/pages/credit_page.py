from PySide2 import QtWidgets, QtCore, QtGui
from ..utilities import cards, plotting, funs
from decimal import Decimal
from . import standard_page

class Page(standard_page.StandarPage):
    def __init__(self, parent):
        super().__init__(parent, "CreditPage")