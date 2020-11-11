# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'carla.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys

from Execution import MainLoop
from DataOperation import data_operation
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow, QMessageBox, QInputDialog, QDialog, QWidget, QAction
from PyQt5.QtCore import QSize, QCoreApplication, QSettings, pyqtSignal
# from dialogsetting import Ui_Setting
from userInterface.customize_WandT import Ui_WandT
from userInterface.Mainwindow import Ui_MainWindow
from userInterface.configuration_path import Ui_PathConfi
from userInterface.history_record_page import Ui_historyRecord
from userInterface.detailreport_driving import Ui_Details_Driving
from userInterface.agentSelection import Ui_agentSelection
from PyQt5.QtWidgets import QTableWidgetItem
from userInterface.detailreport_detect import Ui_detailReport_detect
import time

# from message_send import DictConstruction
#
# import MainLoop
from Execution.message_send import DictConstruction


class Slave(QtCore.QProcess):
    def __init__(self, parent=None):
        super().__init__()
        self.readyReadStandardOutput.connect(self.stdoutEvent)
        self.readyReadStandardError.connect(self.stderrEvent)

    def stdoutEvent(self):
        stdout = self.readAllStandardOutput()
        self.echo(stdout)

    def stderrEvent(self):
        stderr = self.readAllStandardError()
        self.echo(stderr)

    def echo(self, data):
        data = bytes(data).decode("utf8")



class parentWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.settings = QSettings("userInterface/user_interface.ini", QSettings.IniFormat)
        self.settings.setIniCodec("UTF-8")
        self.readInit()
        # self.main_ui.AgentSelection.clicked.connect(self.openAgentSelection())

    def carlaRun(self):

        carla_path_name = self.settings.value("SETUP/userInterface/carla_path", 1, type=str)
        # print(carla_path_name)
        if carla_path_name == "":
            self.warning_message("Sorry! Please configure the correct path of CarlaUE4.exe/.sh")
        else:
            try:
                self.slave = Slave()
                self.slave.start(carla_path_name)
            except Exception as e:
                self.warning_message("Sorry! Please configure the correct path of CarlaUE4.exe/.sh")

    def selectionTimer(self):

        Timer_currentvalue = self.main_ui.Timer.currentText()
        self.settings.setValue("SETUP/userInterface/Timer", Timer_currentvalue)

    def readInit(self):
        self.settings.setValue("SETUP/userInterface/customize", "false")
        Timer_record = self.settings.value("SETUP/userInterface/Timer", 3, type=str)
        Weather_CB_record = self.settings.value("SETUP/userInterface/Weather_CB", 4, type=str)
        scenario_record = self.settings.value("SETUP/userInterface/scenario", 11, type=str)
        self.main_ui.Timer.setCurrentText(Timer_record)
        self.main_ui.Weather_CB.setCurrentText(Weather_CB_record)
        self.main_ui.ScenearioSelection.setCurrentText(scenario_record)
        self.main_ui.WeatherAndT.setChecked(True)
        self.main_ui.label_4.setVisible(True)
        self.main_ui.label_5.setVisible(True)
        self.main_ui.label_6.setVisible(True)
        self.main_ui.label_7.setVisible(True)
        self.main_ui.label_8.setVisible(True)
        self.main_ui.Timer.setHidden(False)
        self.main_ui.Weather_CB.setHidden(False)
        self.main_ui.Customize.setHidden(True)


    def judgement_WeatherAndT(self):
        self.settings.setValue("SETUP/userInterface/customize", "false")
        self.main_ui.label_4.setVisible(True)
        self.main_ui.label_5.setVisible(True)
        self.main_ui.label_6.setVisible(True)
        self.main_ui.label_7.setVisible(True)
        self.main_ui.label_8.setVisible(True)
        self.main_ui.Timer.setHidden(False)
        self.main_ui.Weather_CB.setHidden(False)
        self.main_ui.Customize.setHidden(True)

    def selectionWeather_CB(self):
        Weather_CB_currentvalue = self.main_ui.Weather_CB.currentText()
        self.settings.setValue("SETUP/userInterface/Weather_CB", Weather_CB_currentvalue)

    def selectionScenario_CB(self):
        selectionScenario_CB_currentvalue = self.main_ui.ScenearioSelection.currentText()
        self.settings.setValue("SETUP/userInterface/scenario", selectionScenario_CB_currentvalue)

    def judgement_CustoizeWAndT(self):
        self.settings.setValue("SETUP/userInterface/customize", "true")

    def customize_hidden(self):
        self.main_ui.label_4.setVisible(False)
        self.main_ui.label_5.setVisible(False)
        self.main_ui.label_6.setVisible(False)
        self.main_ui.label_7.setVisible(False)
        self.main_ui.label_8.setVisible(False)
        self.main_ui.Timer.setHidden(True)
        self.main_ui.Weather_CB.setHidden(True)
        self.main_ui.Customize.setHidden(False)

    # self.main_ui.Customize.setHidden(customize_record)

    def runProgram(self):
        # self.slave.start(pyfile path input)

        # agent_path_name = self.settings.value("SETUP/userInterface/agent_path", 0, type=str)
        # carla_path_name = self.settings.value("SETUP/carla_path", 1, type=str)
        customize_record = self.settings.value("SETUP/userInterface/customize", 2, type=str)
        Timer_record = self.settings.value("SETUP/userInterface/Timer", 3, type=str)
        Weather_CB_record = self.settings.value("SETUP/userInterface/Weather_CB", 4, type=str)
        timedial_record = self.settings.value("SETUP/userInterface/timeDial", 5, type=str)
        rainfall_capacity_record = self.settings.value("SETUP/userInterface/rainfall_capacity", 6, type=str)
        ground_humidity_record = self.settings.value("SETUP/userInterface/ground_humidity", 7, type=str)
        wind_power_record = self.settings.value("SETUP/userInterface/wind_power", 8, type=str)
        fog_record = self.settings.value("SETUP/userInterface/fog", 9, type=str)
        air_humidity_record = self.settings.value("SETUP/userInterface/air_humidity", 10, type=str)
        cloudiness_record = self.settings.value("SETUP/userInterface/cloudiness", 13, type=str)
        scenario_record = self.settings.value("SETUP/userInterface/scenario", 11, type=str)
        agent_filename = self.settings.value("SETUP/userInterface/agent_filename", 12, type=str)
        class_name = self.settings.value("SETUP/userInterface/class_name", 14, type=str)
        message = DictConstruction(agent_path=agent_filename,
                                   if_custom=customize_record,
                                   preset_time=Timer_record,
                                   preset_weather=Weather_CB_record,
                                   custom_time=timedial_record,
                                   custom_rainfall=rainfall_capacity_record,
                                   custom_ground_humidity=ground_humidity_record,
                                   custom_wind=wind_power_record,
                                   custom_fog=fog_record,
                                   custom_air_humidity=air_humidity_record,
                                   custom_cloud=cloudiness_record,
                                   scenario=scenario_record,
                                   agent_name=class_name)
        pass_standard = True
        exception_str = ""
        if agent_filename == "":
            exception_str += " agent file path (Agent Selection);"
            pass_standard = False
        if class_name == "":
            exception_str += " agent class name (Agent Selection);"
            pass_standard = False
        if pass_standard:
            try:
                import multiprocessing
                err_msg_queue=multiprocessing.Queue()
                main_process = multiprocessing.Process(target=MainLoop.main_loop,
                                                       kwargs={'data_frame':message, 'err_queue': err_msg_queue})
                self.hide()
                main_process.start()
                # MainLoop.main_loop(message)
                QApplication.processEvents()  # 刷新界面
                time.sleep(0.2)
                # main_thread.join()
                main_process.join()
                self.show()
                result = err_msg_queue.get()

                if type(result) is dict:
                    result_report = "Test Done! Your Result is:\n"
                    result_report += 'Test Scenario: ' + str(result['Scenario']) + '\n'
                    result_report += 'Agent Name: ' + str(result['agent_name']) + '\n'
                    result_report += 'Mark: ' + str(result['mark']) + '\n'
                    result_report += "For more details you can see the detail report in the history list\n"
                    QMessageBox.information(self,
                                            "Test Result",
                                            result_report)
                elif type(result) is str:
                    self.warning_message(str(result))

            except Exception as err:
                self.warning_message(str(err))
        else:
            self.warning_message("Sorry! Execution Failed! You should configure" + exception_str)

    def warning_message(self, err_str):
        QMessageBox.warning(self, "Execution Error!", err_str)

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self,
                                               "QUIT QUERY",
                                               "Are you sure to exit the system?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:

            event.accept()
            sys.exit(0)
        else:
            event.ignore()


# class childWindow(QDialog):
#     def __init__(self):
#         QDialog.__init__(self)
#         self.child=Ui_Setting()
#         self.child.setupUi(self)
class childWindow_WT(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.child = Ui_WandT()
        self.child.setupUi(self)
        self.settings = QSettings("userInterface/user_interface.ini", QSettings.IniFormat)
        self.settings.setIniCodec("UTF-8")
        self.readWeatherandTimer()
        self.child.timeDial.valueChanged.connect(self.changedValue)
        self.child.rainfall_capacity.valueChanged.connect(self.changedValue)
        self.child.ground_humidity.valueChanged.connect(self.changedValue)
        self.child.wind_power.valueChanged.connect(self.changedValue)
        self.child.fog.valueChanged.connect(self.changedValue)
        self.child.air_humidity.valueChanged.connect(self.changedValue)
        self.child.cloundiness.valueChanged.connect(self.changedValue)

    def readWeatherandTimer(self):
        timedial_record = self.settings.value("SETUP/userInterface/timeDial", 5, type=str)
        self.child.timeDial.setValue(int(timedial_record))
        rainfall_capacity_record = self.settings.value("SETUP/userInterface/rainfall_capacity", 6, type=str)
        self.child.rainfall_capacity.setValue(int(rainfall_capacity_record))
        ground_humidity_record = self.settings.value("SETUP/userInterface/ground_humidity", 7, type=str)
        self.child.ground_humidity.setValue(int(ground_humidity_record))
        wind_power_record = self.settings.value("SETUP/userInterface/wind_power", 8, type=str)
        self.child.wind_power.setValue(int(wind_power_record))
        fog_record = self.settings.value("SETUP/userInterface/fog", 9, type=str)
        self.child.fog.setValue(int(fog_record))
        air_humidity_record = self.settings.value("SETUP/userInterface/air_humidity", 10, type=str)
        self.child.air_humidity.setValue(int(air_humidity_record))
        cloudiness_record = self.settings.value("SETUP/userInterface/cloudiness", 14, type=str)
        self.child.cloundiness.setValue(int(cloudiness_record))

    def changedValue(self):
        self.settings.setValue("SETUP/userInterface/timeDial", self.child.timeDial.value())
        self.settings.setValue("SETUP/userInterface/rainfall_capacity", self.child.rainfall_capacity.value())
        self.settings.setValue("SETUP/userInterface/ground_humidity", self.child.ground_humidity.value())

        self.settings.setValue("SETUP/userInterface/fog", self.child.fog.value())
        self.settings.setValue("SETUP/userInterface/wind_power", self.child.wind_power.value())
        self.settings.setValue("SETUP/userInterface/air_humidity", self.child.air_humidity.value())
        self.settings.setValue("SETUP/userInterface/cloudiness", self.child.cloundiness.value())


class PathConfiForm(QWidget, Ui_PathConfi):
    def __init__(self, parent=None):
        super(PathConfiForm, self).__init__(parent)
        self.setupUi(self)
        self.settings = QSettings("userInterface/user_interface.ini", QSettings.IniFormat)
        self.settings.setIniCodec("UTF-8")
        self.lineEdit_3.setText(self.settings.value("SETUP/userInterface/agent_path", 0, type=str))
        self.lineEdit_2.setText(self.settings.value("SETUP/userInterface/carla_path", 1, type=str))
        self.agentPath.clicked.connect(self.slot_btn_chooseDir_agentPath)
        self.carlaPath.clicked.connect(self.slot_btn_chooseDir_carlaPath)

    def slot_btn_chooseDir_agentPath(self):
        get_directory_path = QFileDialog.getExistingDirectory(self,
                                                              "directory path",
                                                              "./")
        self.lineEdit_3.setText(str(get_directory_path))
        self.settings.setValue("SETUP/userInterface/agent_path", get_directory_path)

    def slot_btn_chooseDir_carlaPath(self):
        get_carla_path = QFileDialog.getOpenFileName(self, 'carla path', "./")

        self.lineEdit_2.setText(str(get_carla_path[0]))
        self.settings.setValue("SETUP/userInterface/carla_path", str(get_carla_path[0]))


class HistoryRecordForm(Ui_historyRecord):
    signal_driving0 = pyqtSignal()
    signal_driving1 = pyqtSignal()
    signal_driving2 = pyqtSignal()
    signal_driving3 = pyqtSignal()
    signal_driving4 = pyqtSignal()
    signal_driving5 = pyqtSignal()
    signal_driving6 = pyqtSignal()
    signal_driving7 = pyqtSignal()
    signal_driving8 = pyqtSignal()
    signal_driving9 = pyqtSignal()
    signal_detecting0 = pyqtSignal()
    signal_detecting1 = pyqtSignal()
    signal_detecting2 = pyqtSignal()
    signal_detecting3 = pyqtSignal()
    signal_detecting4 = pyqtSignal()
    signal_detecting5 = pyqtSignal()
    signal_detecting6 = pyqtSignal()
    signal_detecting7 = pyqtSignal()
    signal_detecting8 = pyqtSignal()
    signal_detecting9 = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(HistoryRecordForm, self).__init__(*args, **kwargs)
        self.setupUi()
        self.settings = QSettings("userInterface/user_interface.ini", QSettings.IniFormat)
        self.settings.setIniCodec("UTF-8")

    def setRecordId(self, colunm):
        self.settings.setValue("SETUP/userInterface/cur_page", str(self.table.item(colunm, 5).text()))
        traffic_light_scenario = "Traffic Light"
        object_detection = "Object Detection"
        # print(self.table.item(colunm, 1).text())
        if colunm == 0:
            if self.table.item(colunm, 1).text() == traffic_light_scenario or self.table.item(colunm, 1).text() == object_detection:
                self.signal_detecting0.emit()
            else:
                self.signal_driving0.emit()
        if colunm == 1:
            if self.table.item(colunm, 1).text() == traffic_light_scenario or self.table.item(colunm, 1).text() == object_detection:
                self.signal_detecting1.emit()
            else:
                self.signal_driving1.emit()
        if colunm == 2:
            if self.table.item(colunm, 1).text() == traffic_light_scenario or self.table.item(colunm, 1).text() == object_detection:
                self.signal_detecting2.emit()
            else:
                self.signal_driving2.emit()
        if colunm == 3:
            if self.table.item(colunm, 1).text() == traffic_light_scenario or self.table.item(colunm, 1).text() == object_detection:
                self.signal_detecting3.emit()
            else:
                self.signal_driving3.emit()
        if colunm == 4:
            if self.table.item(colunm, 1).text() == traffic_light_scenario or self.table.item(colunm, 1).text() == object_detection:
                self.signal_detecting4.emit()
            else:
                self.signal_driving4.emit()
        if colunm == 5:
            if self.table.item(colunm, 1).text() == traffic_light_scenario or self.table.item(colunm, 1).text() == object_detection:
                self.signal_detecting5.emit()
            else:
                self.signal_driving5.emit()
        if colunm == 6:
            if self.table.item(colunm, 1).text() == traffic_light_scenario or self.table.item(colunm, 1).text() == object_detection:
                self.signal_detecting6.emit()
            else:
                self.signal_driving6.emit()
        if colunm == 7:
            if self.table.item(colunm, 1).text() == traffic_light_scenario or self.table.item(colunm, 1).text() == object_detection:
                self.signal_detecting7.emit()
            else:
                self.signal_driving7.emit()
        if colunm == 8:
            if self.table.item(colunm, 1).text() == traffic_light_scenario or self.table.item(colunm, 1).text() == object_detection:
                self.signal_detecting8.emit()
            else:
                self.signal_driving8.emit()
        if colunm == 9:
            if self.table.item(colunm, 1).text() == traffic_light_scenario or self.table.item(colunm, 1).text() == object_detection:
                self.signal_detecting9.emit()
            else:
                self.signal_driving9.emit()

        '''
        print(colunm)
        print("selftable", self.table)
        print(self.table.item(colunm, 5).text())
        '''



    # def show(self):
    #     details_button = self.queryButton[2]
    #     details_button_1 = self.queryButton[3]
    #     details_button.clicked.connect(reprotDetail.show)
    #     details_button_1.clicked.connect(reprotDetail.show)


class agentSelection(QWidget, Ui_agentSelection):
    def __init__(self, parent=None):
        super(agentSelection, self).__init__(parent)
        self.setupUi(self)
        self.settings = QSettings("userInterface/user_interface.ini", QSettings.IniFormat)
        self.settings.setIniCodec("UTF-8")
        self.agentfile.clicked.connect(self.openAgentSelection)
        self.lineEdit.textChanged.connect(lambda: self.onChanged())
        self.lineEdit_2.setText(self.settings.value("SETUP/userInterface/agent_filename", 3, type=str))
        self.lineEdit.setText(self.settings.value("SETUP/userInterface/class_name", 14, type=str))
        self.lineEdit_2.setReadOnly(True)

    def openAgentSelection(self):
        agent_path_name = self.settings.value("SETUP/userInterface/agent_path", 0, type=str)
        openfile_name = QFileDialog.getOpenFileName(self, 'Agent selection', agent_path_name, 'Python(*.py)')
        self.lineEdit_2.setText(str(openfile_name[0]))
        self.settings.setValue("SETUP/userInterface/agent_filename", str(openfile_name[0]))

    def onChanged(self):
        clas_name = self.lineEdit.text()

        self.settings.setValue("SETUP/userInterface/class_name", clas_name)


class reportDetail_driving(QWidget, Ui_Details_Driving):
    def __init__(self, parent=None):
        super(reportDetail_driving, self).__init__(parent)
        self.setupUi(self)
        self.settings = QSettings("userInterface/user_interface.ini", QSettings.IniFormat)
        self.settings.setIniCodec("UTF-8")

    def setData(self):
        # self.settings = QSettings("userInterface/user_interface.ini", QSettings.IniFormat)
        # self.settings.setIniCodec("UTF-8")

        record_id = self.settings.value("SETUP/userInterface/cur_page", 13, type=str)

        self.information.setItem(0, 5, QTableWidgetItem(str(5)))

        record_list = data_operation.get_detailed_list(int(record_id))

        this_record = record_list[0]
        self.information.setItem(0, 1, QTableWidgetItem(str(this_record[4])))
        self.information.setItem(1, 1, QTableWidgetItem(str(this_record[21])))
        is_arrive = ""
        if this_record[22] == 1:
            is_arrive = "Yes"
        else:
            is_arrive = "No"
        self.information.setItem(2, 1, QTableWidgetItem(is_arrive))
        self.information.setItem(3, 1, QTableWidgetItem(str(this_record[23])))
        self.information.setItem(4, 1, QTableWidgetItem(str(this_record[5])))

        self.information_3.setItem(0, 0, QTableWidgetItem(str(this_record[7])))
        self.information_3.setItem(0, 1, QTableWidgetItem(str(this_record[18])))

        self.information_2.setItem(0, 1, QTableWidgetItem(str(this_record[3])))

        self.weather.setItem(1, 0, QTableWidgetItem(str(this_record[9])))
        self.weather.setItem(1, 1, QTableWidgetItem(str(this_record[10])))
        self.weather.setItem(1, 2, QTableWidgetItem(str(int(this_record[11]))))
        self.weather.setItem(1, 3, QTableWidgetItem(str(this_record[12])))
        self.weather.setItem(1, 4, QTableWidgetItem(str(this_record[13])))
        self.weather.setItem(1, 5, QTableWidgetItem(str(this_record[14])))
        self.weather.setItem(1, 6, QTableWidgetItem(str(this_record[15])))
        self.weather.setItem(1, 7, QTableWidgetItem(str(this_record[16])))


class reportDetail_detecting(QWidget, Ui_detailReport_detect):
    def __init__(self, parent=None):
        super(reportDetail_detecting, self).__init__(parent)
        self.setupUi(self)

    def setData(self):
        self.settings = QSettings("userInterface/user_interface.ini", QSettings.IniFormat)
        self.settings.setIniCodec("UTF-8")
        cur_page = self.settings.value("SETUP/userInterface/cur_page", 13, type=str)

        record_list = data_operation.get_detailed_list(int(cur_page))
        this_record = record_list[0]

        self.weather.setItem(1, 0, QTableWidgetItem(str(this_record[9])))
        self.weather.setItem(1, 1, QTableWidgetItem(str(this_record[10])))
        self.weather.setItem(1, 2, QTableWidgetItem(str(int(this_record[11]))))
        self.weather.setItem(1, 3, QTableWidgetItem(str(this_record[12])))
        self.weather.setItem(1, 4, QTableWidgetItem(str(this_record[13])))
        self.weather.setItem(1, 5, QTableWidgetItem(str(this_record[14])))
        self.weather.setItem(1, 6, QTableWidgetItem(str(this_record[15])))
        self.weather.setItem(1, 7, QTableWidgetItem(str(this_record[16])))

        # set test time
        self.information_3.setItem(0, 0, QTableWidgetItem(str(this_record[7])))

        # set scenario name
        self.information_3.setItem(0, 1, QTableWidgetItem(str(this_record[18])))

        #set mark
        self.information_2.setItem(0, 1, QTableWidgetItem(str(this_record[3])))

        # agent information
        self.information.setItem(0, 1, QTableWidgetItem(str(this_record[4])))
        self.information.setItem(3, 1, QTableWidgetItem(str(this_record[5])))

        # accuracy
        self.information.setItem(1, 1, QTableWidgetItem(str(this_record[21]) + '%'))

        # avg time
        self.information.setItem(2, 1, QTableWidgetItem(str(this_record[22]) + 's'))

        # detects and answer setting
        detects_str = str(this_record[23])
        answer_str = str(this_record[24])

        detects_arr = detects_str.split(sep="|")
        answer_arr = answer_str.split(sep="|")

        attr_length = len(detects_arr)

        self.details.setColumnCount(attr_length + 1)
        for i in range(0, attr_length + 1):
            self.details.setItem(0, i, QtWidgets.QTableWidgetItem())

        _translate = QtCore.QCoreApplication.translate

        item = self.details.item(0, 0)
        item.setText(_translate("Form", "Detects"))
        item = self.details.item(1, 0)
        item.setText(_translate("Form", "Answers"))
        for i in range(0, attr_length):
            item = self.details.item(0, i + 1)
            item.setText(_translate("Form", detects_arr[i]))
            item = self.details.item(1, i + 1)
            item.setText(_translate("Form", answer_arr[i]))



if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        global window
        window = parentWindow()
        childWandT = childWindow_WT()
        childPathconfi = PathConfiForm()
        childHistoryRecord = HistoryRecordForm()
        childAgentSelection = agentSelection()

        # #通过toolButton将两个窗体关联
        # btn = window.main_ui.toolButton
        # btn.clicked.connect(child.show)
        PathSetting_button = window.main_ui.PathSetting
        PathSetting_button.clicked.connect(childPathconfi.show)

        customizeWAndT_button = window.main_ui.CustoizeWAndT
        customizeWAndT_button.clicked.connect(lambda: window.customize_hidden())

        Customize_button = window.main_ui.Customize
        back_Customize_button = childWandT.child.canclepath_2

        Customize_button.clicked.connect(childWandT.show)
        back_Customize_button.clicked.connect(childWandT.close)

        historyrecord_button = window.main_ui.HistoryTestRecord
        historyrecord_button.clicked.connect(childHistoryRecord.changeTableContent)
        historyrecord_button.clicked.connect(childHistoryRecord.show)
        # historyrecord_button.clicked.connect(lambda:HistoryRecordForm().setCurpage(0))


        reprotDetail_driving = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        reprotDetail_detecting = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        # historyrecord_button.clicked.connect(lambda:HistoryRecordForm().setCurpage(0))
        for dataID in range(10):
            reprotDetail_driving[dataID] = reportDetail_driving()
        for dataID in range(10):
            reprotDetail_detecting[dataID] = reportDetail_detecting()

        childHistoryRecord.queryButton[0].clicked.connect(lambda: childHistoryRecord.setRecordId(0))
        childHistoryRecord.signal_driving0.connect(lambda: reprotDetail_driving[0].setData())
        childHistoryRecord.signal_driving0.connect(reprotDetail_driving[0].show)
        childHistoryRecord.signal_detecting0.connect(lambda: reprotDetail_detecting[0].setData())
        childHistoryRecord.signal_detecting0.connect(reprotDetail_detecting[0].show)

        childHistoryRecord.queryButton[1].clicked.connect(lambda: childHistoryRecord.setRecordId(1))
        childHistoryRecord.signal_driving1.connect(lambda: reprotDetail_driving[1].setData())
        childHistoryRecord.signal_driving1.connect(reprotDetail_driving[1].show)
        childHistoryRecord.signal_detecting1.connect(lambda: reprotDetail_detecting[1].setData())
        childHistoryRecord.signal_detecting1.connect(reprotDetail_detecting[1].show)

        childHistoryRecord.queryButton[2].clicked.connect(lambda: childHistoryRecord.setRecordId(2))
        childHistoryRecord.signal_driving2.connect(lambda: reprotDetail_driving[2].setData())
        childHistoryRecord.signal_driving2.connect(reprotDetail_driving[2].show)
        childHistoryRecord.signal_detecting2.connect(lambda: reprotDetail_detecting[2].setData())
        childHistoryRecord.signal_detecting2.connect(reprotDetail_detecting[2].show)

        childHistoryRecord.queryButton[3].clicked.connect(lambda: childHistoryRecord.setRecordId(3))
        childHistoryRecord.signal_driving3.connect(lambda: reprotDetail_driving[3].setData())
        childHistoryRecord.signal_driving3.connect(reprotDetail_driving[3].show)
        childHistoryRecord.signal_detecting3.connect(lambda: reprotDetail_detecting[3].setData())
        childHistoryRecord.signal_detecting3.connect(reprotDetail_detecting[3].show)

        childHistoryRecord.queryButton[4].clicked.connect(lambda: childHistoryRecord.setRecordId(4))
        childHistoryRecord.signal_driving4.connect(lambda: reprotDetail_driving[4].setData())
        childHistoryRecord.signal_driving4.connect(reprotDetail_driving[4].show)
        childHistoryRecord.signal_detecting4.connect(lambda: reprotDetail_detecting[4].setData())
        childHistoryRecord.signal_detecting4.connect(reprotDetail_detecting[4].show)

        childHistoryRecord.queryButton[5].clicked.connect(lambda: childHistoryRecord.setRecordId(5))
        childHistoryRecord.signal_driving5.connect(lambda: reprotDetail_driving[5].setData())
        childHistoryRecord.signal_driving5.connect(reprotDetail_driving[5].show)
        childHistoryRecord.signal_detecting5.connect(lambda: reprotDetail_detecting[5].setData())
        childHistoryRecord.signal_detecting5.connect(reprotDetail_detecting[5].show)

        childHistoryRecord.queryButton[6].clicked.connect(lambda: childHistoryRecord.setRecordId(6))
        childHistoryRecord.signal_driving6.connect(lambda: reprotDetail_driving[6].setData())
        childHistoryRecord.signal_driving6.connect(reprotDetail_driving[6].show)
        childHistoryRecord.signal_detecting6.connect(lambda: reprotDetail_detecting[6].setData())
        childHistoryRecord.signal_detecting6.connect(reprotDetail_detecting[6].show)

        childHistoryRecord.queryButton[7].clicked.connect(lambda: childHistoryRecord.setRecordId(7))
        childHistoryRecord.signal_driving7.connect(lambda: reprotDetail_driving[7].setData())
        childHistoryRecord.signal_driving7.connect(reprotDetail_driving[7].show)
        childHistoryRecord.signal_detecting7.connect(lambda: reprotDetail_detecting[7].setData())
        childHistoryRecord.signal_detecting7.connect(reprotDetail_detecting[7].show)

        childHistoryRecord.queryButton[8].clicked.connect(lambda: childHistoryRecord.setRecordId(8))
        childHistoryRecord.signal_driving8.connect(lambda: reprotDetail_driving[8].setData())
        childHistoryRecord.signal_driving8.connect(reprotDetail_driving[8].show)
        childHistoryRecord.signal_detecting8.connect(lambda: reprotDetail_detecting[8].setData())
        childHistoryRecord.signal_detecting8.connect(reprotDetail_detecting[8].show)

        childHistoryRecord.queryButton[9].clicked.connect(lambda: childHistoryRecord.setRecordId(9))
        childHistoryRecord.signal_driving9.connect(lambda: reprotDetail_driving[9].setData())
        childHistoryRecord.signal_driving9.connect(reprotDetail_driving[9].show)
        childHistoryRecord.signal_detecting9.connect(lambda: reprotDetail_detecting[9].setData())
        childHistoryRecord.signal_detecting9.connect(reprotDetail_detecting[9].show)

        AgentSelection_button = window.main_ui.AgentSelection

        AgentSelection_button.clicked.connect(childAgentSelection.show)

        CarlaRun_button = window.main_ui.CarlaRun
        CarlaRun_button.clicked.connect(lambda: window.carlaRun())  #

        Timer_button = window.main_ui.Timer
        Timer_button.currentIndexChanged.connect(lambda: window.selectionTimer())

        Weather_CB_button = window.main_ui.Weather_CB
        Weather_CB_button.currentIndexChanged.connect(lambda: window.selectionWeather_CB())

        WeatherAndT_button = window.main_ui.WeatherAndT
        WeatherAndT_button.clicked.connect(lambda: window.judgement_WeatherAndT())

        CustoizeWAndT_button = window.main_ui.CustoizeWAndT
        CustoizeWAndT_button.clicked.connect(lambda: window.judgement_CustoizeWAndT())

        ScenearioSelection_button = window.main_ui.ScenearioSelection
        ScenearioSelection_button.currentIndexChanged.connect(lambda: window.selectionScenario_CB())

        run_button = window.main_ui.Run
        run_button.clicked.connect(lambda: window.runProgram())

        # 显示
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        window.warning_message(str(e))




