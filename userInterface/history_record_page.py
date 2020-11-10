# _*_ coding:utf-8 _*_
# author: zizle
# date 22/04/2019
import sys

from DataOperation import data_operation
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPalette,QBrush,QPixmap
import re
from PyQt5.QtCore import QSize, QCoreApplication, QSettings
from PyQt5.QtWidgets import QFileDialog,QApplication
import time
class Ui_historyRecord(QWidget):
    control_signal = pyqtSignal(list)

    '''
    def __init__(self, *args, **kwargs):
         super(Ui_historyRecord, self).__init__(*args, **kwargs)
         self.setupUi()
    '''

    def setupUi(self):
        style_sheet = """
            QTableWidget {
                border: none;
                background-color:rgb(255,255,255)
                
            }
            QPushButton{
                
                border-radius:25px;
                background-color:rgb(255, 255, 255); 
                color: rgb(0, 0, 0);
                font-size:15px;
                font-family:华文隶书;
            }
            QPushButton:pressed{
                background-color:rgb(173, 115, 0)
            }
            QLineEdit{
                
                font-size:15px;
                font-family:华文隶书;
            }
            QLabel
            {
                
                font-size:18px;
                font-family:华文隶书;
            }
            
        """
        self.setWindowTitle("History Record")
        self.setMinimumSize(1000, 400)
        self.setMaximumSize(1000, 400)

        # data=test_data.get_test_data(1)
        data_list = data_operation.get_record_list(1, 10)
        data = self.convert_data_to_dict(data_list)
        # self.table = QTableWidget(len(data), 4)  # 3 行 5 列的表格
        self.table = QTableWidget(10, 6)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('userInterface/haoche.jpg')))
        self.setPalette(palette)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应宽度
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应宽度
        self.table.setHorizontalHeaderLabels(['date','scenario','agent name','score','see details','id'])
        font = QtGui.QFont()
        font.setFamily("华文隶书")
        font.setPointSize(10)
        self.table.setFont(font)
        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.table)
        self.setLayout(self.__layout)
        self.setStyleSheet(style_sheet)
        self.setPageController(int(len((data))/10+1))  # 表格设置页码控制
        self.control_signal.connect(self.page_controller)
        self.control_signal.connect(self.page_controller)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.queryButton = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.table.setColumnHidden(5, True)
        for dataId in range(10):

            self.queryButton[dataId] = QtWidgets.QPushButton('See details')
            self.queryButton[dataId].setDown(False)
        for dataId in range(len(data)):
            self.table.setItem(dataId,0,QTableWidgetItem(data[dataId]['date']))
            self.table.setItem(dataId,1, QTableWidgetItem(data[dataId]['scenario']))
            self.table.setItem(dataId, 2, QTableWidgetItem(data[dataId]['agent name']))
            self.table.setItem(dataId,3, QTableWidgetItem(data[dataId]['score']))
            self.table.setCellWidget(dataId, 4, self.queryButton[dataId])
            self.table.setItem(dataId, 5, QTableWidgetItem(str(data[dataId]['id'])))

            # self.queryButton[dataId].clicked.connect(reprotDetail.show)


    def getCurpage(self):
        # print(self.curPage.text())
        return int(self.curPage.text())


    def page_controller(self, signal):
        total_page = self.showTotalPage()
        if "home" == signal[0]:
            self.curPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "prompt", "Already the first page", QMessageBox.Yes)
                return
            self.curPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                QMessageBox.information(self, "prompt", "Already the last page", QMessageBox.Yes)
                return
            self.curPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            self.curPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 0:
                QMessageBox.information(self, "prompt", "Jump page number out of range", QMessageBox.Yes)
                return
            self.curPage.setText(signal[1])

        self.changeTableContent()  # 改变表格内容

    def changeTableContent(self):
        """根据当前页改变表格的内容"""
        cur_page = self.curPage.text()
        data_list = data_operation.get_record_list(int(cur_page), 10)
        data = self.convert_data_to_dict(data_list)
        # print(data)
        # data=test_data.get_test_data(int(cur_page))
        # self.settings = QSettings("user_interface.ini", QSettings.IniFormat)
        # self.settings.setIniCodec("UTF-8")
        # self.settings.setValue("SETUP/cur_page", str(cur_page))


        # self.table = QTableWidget(len(data), 4)

        # a=QTableWidgetItem(data[2]['date'])
        # self.table.setItem(0,0,a)
        # print(a)
        temp = 10
        if len(data) < 10:

            for dataId in range(10 - len(data)):
                temp = temp - 1
                # self.table.removeRow(temp)
                self.table.setRowHidden(temp,True)
        else:
            for dataId in range(10):
                self.table.setRowHidden(dataId,False)
        for dataId in range(len(data)):
            self.table.setItem(dataId,0,QTableWidgetItem(data[dataId]['date']))
            self.table.setItem(dataId,1, QTableWidgetItem(data[dataId]['scenario']))
            self.table.setItem(dataId, 2, QTableWidgetItem(data[dataId]['agent name']))
            self.table.setItem(dataId,3, QTableWidgetItem(data[dataId]['score']))
            self.table.setCellWidget(dataId, 4, self.queryButton[dataId])
            self.table.setItem(dataId, 5, QTableWidgetItem(str(data[dataId]['id'])))

    def convert_data_to_dict(self, db_record):
        db_list = []
        for record in db_record:
            record_dict = {}
            record_dict['id'] = record[0]
            record_dict['date'] = record[7]
            record_dict['scenario'] = self.get_scenario_name(record[1])
            record_dict['agent name'] = record[4]
            record_dict['score'] = str(record[3])
            db_list.append(record_dict)
        return db_list


    def get_scenario_name(self, sce_id):
        sce_name = ""
        if sce_id == 1:
            sce_name = "Blind Point"
        elif sce_id == 2:
            sce_name = "Leading Vehicle"
        elif sce_id == 3:
            sce_name = "Object Detection"
        elif sce_id == 4:
            sce_name = "Traffic Light"
        elif sce_id == 5:
            sce_name = "Turning Obstacle"
        return sce_name



    def setPageController(self, page):
        """自定义页码控制器"""
        control_layout = QHBoxLayout()
        homePage = QPushButton("homePage")
        prePage = QPushButton("<pre")
        self.curPage = QLabel("1")
        nextPage = QPushButton("next>")
        finalPage = QPushButton("final")
        self.totalPage = QLabel("Total" + "-"+ str(page) + "-")
        skipLable_0 = QLabel("skip")
        self.skipPage = QLineEdit()
        # skipLabel_1 = QLabel("页")
        confirmSkip = QPushButton("confirm")
        homePage.clicked.connect(self.__home_page)
        prePage.clicked.connect(self.__pre_page)
        nextPage.clicked.connect(self.__next_page)
        finalPage.clicked.connect(self.__final_page)
        confirmSkip.clicked.connect(self.__confirm_skip)
        control_layout.addStretch(1)
        control_layout.addWidget(homePage)
        control_layout.addWidget(prePage)
        control_layout.addWidget(self.curPage)
        control_layout.addWidget(nextPage)
        control_layout.addWidget(finalPage)
        control_layout.addWidget(self.totalPage)
        control_layout.addWidget(skipLable_0)
        control_layout.addWidget(self.skipPage)
        # control_layout.addWidget(skipLabel_1)
        control_layout.addWidget(confirmSkip)
        control_layout.addStretch(1)
        self.__layout.addLayout(control_layout)

    def __home_page(self):
        """点击首页信号"""
        self.control_signal.emit(["home", self.curPage.text()])

    def __pre_page(self):
        """点击上一页信号"""
        self.control_signal.emit(["pre", self.curPage.text()])

    def __next_page(self):
        """点击下一页信号"""
        self.control_signal.emit(["next", self.curPage.text()])

    def __final_page(self):
        """尾页点击信号"""
        self.control_signal.emit(["final", self.curPage.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.control_signal.emit(["confirm", self.skipPage.text()])

    def showTotalPage(self):
        """返回当前总页数"""
        totalpage=re.findall(r"\d+\.?\d*", self.totalPage.text())
        # print("totalpage[0]",totalpage[0])
        return int(totalpage[0])








# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = Ui_historyRecord()
#     window.show()
#     sys.exit(app.exec_())