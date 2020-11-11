# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'agentSelection.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette,QBrush,QPixmap

class Ui_agentSelection(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(700, 367)
        Form.setMinimumSize(QtCore.QSize(700, 367))
        Form.setMaximumSize(QtCore.QSize(700, 367))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('userInterface/haoche.jpg')))
        self.setPalette(palette)
        Form.setStyleSheet("#Form{\n"
"\n"
"border-image:url(:/mainwindow/haoche.jpg)\n"
"}")
        self.agentfile = QtWidgets.QPushButton(Form)
        self.agentfile.setGeometry(QtCore.QRect(280, 90, 51, 51))
        self.agentfile.setStyleSheet("border-image:url(:/mainwindow/filepath.jpg)")
        self.agentfile.setText("")
        self.agentfile.setObjectName("agentfile")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 80, 251, 71))
        font = QtGui.QFont()
        font.setFamily("华文隶书")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setStyleSheet("color:rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 180, 191, 71))
        font = QtGui.QFont()
        font.setFamily("华文隶书")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(240, 200, 411, 41))
        font = QtGui.QFont()
        font.setFamily("华文隶书")
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(340, 100, 311, 41))
        font = QtGui.QFont()
        font.setFamily("华文隶书")
        font.setPointSize(14)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(500, 280, 131, 51))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"    border-radius:25px;\n"
"    background-color:rgb(255, 255, 255); \n"
"    color: rgb(0, 170, 255)\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color:rgb(173, 115, 0)\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Agent Filename:"))
        self.label_2.setText(_translate("Form", "Class Name:"))
        self.pushButton_2.setText(_translate("Form", "Save"))
import userInterface.background_rc