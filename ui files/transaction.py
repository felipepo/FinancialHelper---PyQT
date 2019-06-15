# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'transaction.ui',
# licensing of 'transaction.ui' applies.
#
# Created: Sat Jun 15 17:57:19 2019
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(391, 232)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 5, 3, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 5, 0, 1, 3)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 3, 0, 1, 2)
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 3, 2, 1, 2)
        self.dateEdit = QtWidgets.QDateEdit(Dialog)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 1, 2, 1, 2)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 1, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 2)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 2)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setStyleSheet("font: 63 11pt \"Segoe UI Semibold\";")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Dialog", "Comentário", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Dialog", "OK", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "Valor (R$)", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "Conta", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Data", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Categoria", None, -1))

