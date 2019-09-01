from PySide2 import QtCore, QtWidgets, QtGui
import sys

class TranslucentWidgetSignals(QtCore.QObject):
    # SIGNALS
    CLOSE = QtCore.Signal()


class TranslucentWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TranslucentWidget, self).__init__(parent)

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.fillColor = QtGui.QColor(30, 30, 30, 120)
        self.penColor = QtGui.QColor("#333333")

        self.popup_fillColor = QtGui.QColor(240, 240, 240, 255)
        self.popup_penColor = QtGui.QColor(200, 200, 200, 255)

        self.close_btn = QtWidgets.QPushButton(self)
        self.close_btn.setText("x")
        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setBold(True)
        self.close_btn.setFont(font)
        self.close_btn.setStyleSheet("background-color: rgb(0, 0, 0, 0)")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self._onclose)

        self.SIGNALS = TranslucentWidgetSignals()

    def resizeEvent(self, event):
        s = self.size()
        popup_width = 300
        popup_height = 120
        ow = int(s.width() / 2 - popup_width / 2)
        oh = int(s.height() / 2 - popup_height / 2)
        self.close_btn.move(ow + 265, oh + 5)

    def paintEvent(self, event):
        # This method is, in practice, drawing the contents of
        # your window.

        # get current window size
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(self.penColor)
        qp.setBrush(self.fillColor)
        qp.drawRect(0, 0, s.width(), s.height())

        # drawpopup
        qp.setPen(self.popup_penColor)
        qp.setBrush(self.popup_fillColor)
        popup_width = 300
        popup_height = 120
        ow = int(s.width()/2-popup_width/2)
        oh = int(s.height()/2-popup_height/2)
        qp.drawRoundedRect(ow, oh, popup_width, popup_height, 5, 5)

        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setBold(True)
        qp.setFont(font)
        qp.setPen(QtGui.QColor(70, 70, 70))
        tolw, tolh = 80, -5
        qp.drawText(ow + int(popup_width/2) - tolw, oh +
                    int(popup_height/2) - tolh, "Yep, I'm a pop up.")

        qp.end()

    def _onclose(self):
        print("Close")
        self.SIGNALS.CLOSE.emit()


class ParentWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ParentWidget, self).__init__(parent)

        self._popup = QtWidgets.QPushButton("Gimme Popup!!!")
        self._popup.setFixedSize(150, 40)
        self._popup.clicked.connect(self._onpopup)

        self._other1 = QtWidgets.QPushButton("A button")
        self._other2 = QtWidgets.QPushButton("A button")
        self._other3 = QtWidgets.QPushButton("A button")
        self._other4 = QtWidgets.QPushButton("A button")

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._popup)
        hbox.addWidget(self._other1)
        hbox.addWidget(self._other2)
        hbox.addWidget(self._other3)
        hbox.addWidget(self._other4)
        self.setLayout(hbox)

        self._popframe = None
        self._popflag = False

    def resizeEvent(self, event):
        if self._popflag:
            self._popframe.move(0, 0)
            self._popframe.resize(self.width(), self.height())

    def _onpopup(self):
        self._popframe = TranslucentWidget(self)
        self._popframe.move(0, 0)
        self._popframe.resize(self.width(), self.height())
        self._popframe.SIGNALS.CLOSE.connect(self._closepopup)
        self._popflag = True
        self._popframe.show()

    def _closepopup(self):
        self._popframe.close()
        self._popflag = False


# ====================================


class CtmWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.button = QtWidgets.QPushButton("Close Overlay")
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(self.button)

        self.button.clicked.connect(self.hideOverlay)

    def paintEvent(self, event):

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), 10, 10)
        QtGui.QRegion(path.toFillPolygon().toPolygon())
        pen = QtGui.QPen(QtCore.Qt.white, 1)
        painter.setPen(pen)
        painter.fillPath(path, QtCore.Qt.white)
        painter.drawPath(path)
        painter.end()

    def hideOverlay(self):
        self.parent().hide()


class Overlay(QtWidgets.QWidget):
    def __init__(self, parent, widget):
        QtWidgets.QWidget.__init__(self, parent)
        palette = QtGui.QPalette(self.palette())
        palette.setColor(palette.Background, QtCore.Qt.transparent)
        self.setPalette(palette)

        self.widget = widget
        self.widget.setParent(self)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(event.rect(), QtGui.QBrush(
            QtGui.QColor(0, 0, 0, 127)))
        painter.end()

    def resizeEvent(self, event):
        position_x = (self.frameGeometry().width() -
                      self.widget.frameGeometry().width())/2
        position_y = (self.frameGeometry().height() -
                      self.widget.frameGeometry().height())/2

        self.widget.move(position_x, position_y)
        event.accept()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.resize(800, 500)

        self.button = QtWidgets.QPushButton("Click Me")

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.button)
        self.popup = Overlay(self, CtmWidget())
        self.popup.hide()

        # Connections
        self.button.clicked.connect(self.displayOverlay)

    def displayOverlay(self):
        self.popup.show()
        print("clicked")

    def resizeEvent(self, event):
        self.popup.resize(event.size())
        event.accept()


if __name__ == "__main__":
    if 0:
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        app = QtWidgets.QApplication(sys.argv)
        main = ParentWidget()
        main.resize(500, 500)
        main.show()
        sys.exit(app.exec_())