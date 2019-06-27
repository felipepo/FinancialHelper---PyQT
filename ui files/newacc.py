# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newacc.ui',
# licensing of 'newacc.ui' applies.
#
# Created: Tue Jun 18 22:05:24 2019
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(275, 90)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.OK = QtWidgets.QPushButton(Dialog)
        self.OK.setObjectName("OK")
        self.gridLayout.addWidget(self.OK, 2, 1, 1, 1)
        self.CCRadio = QtWidgets.QRadioButton(Dialog)
        self.CCRadio.setObjectName("CCRadio")
        self.gridLayout.addWidget(self.CCRadio, 1, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 0, 1, 1)
        self.AccRadio = QtWidgets.QRadioButton(Dialog)
        self.AccRadio.setObjectName("AccRadio")
        self.gridLayout.addWidget(self.AccRadio, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.OK.setText(QtWidgets.QApplication.translate("Dialog", "Ok", None, -1))
        self.CCRadio.setText(QtWidgets.QApplication.translate("Dialog", "Cartão de Crédito", None, -1))
        self.AccRadio.setText(QtWidgets.QApplication.translate("Dialog", "Conta", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Nome", None, -1))

