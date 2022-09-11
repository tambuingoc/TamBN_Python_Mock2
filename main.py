from plistlib import load
import sys
import json
import re
import time
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QMessageBox, QCheckBox, QPushButton, QTableWidget
from PyQt5.uic import loadUi
from login import Ui_MainWindow

#login page
class Login(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def open_json(self):
        with open ('save_acc.json', 'r', encoding='utf-8') as fr:
            data = json.load(fr)
        fr.close()
        return data
    
    def connectSignalsSlots(self):
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.checkBox1.stateChanged.connect(self.b_RememberInfor)
        self.createaccbutton.clicked.connect(self.gotocreate)
    
    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def b_RememberInfor(self):
        return self.checkBox1.isChecked()

    def getInfor(self):
        list_infor  = []
        username = self.username.text()
        password = self.password.text()
        list_infor.append(username)
        list_infor.append(password)
        return list_infor  

    def loginfunction(self):
        if self.checkBox1.isChecked() == True:
            infor = self.getInfor()
            data = self.open_json()
            if infor[0] in data.keys():
                QMessageBox.about(self, "Report","Login Succesfully")
                home = Home()
                widget.addWidget(home)
                widget.setCurrentIndex(widget.currentIndex() + 1)  
            else:
                QMessageBox.about(self, "Report","Account does not exit. Try again")  

#sign up page
from createacc import Ui_MainWindow
class CreateAcc(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        if self.checkacc.isChecked() == True:
            acc_infor = self.getAcc() 
            data = self.open_json()
            #if (username, password) in dict_data.items()
            if acc_infor[0] in data.keys():
                QMessageBox.about(self, "Report","This account have already existed. Let's create a new account!")
            else:
                self.write_json(acc_infor)
                QMessageBox.about(self, "Report","Create account successfuly")
                #create account successfuly -> return to login page
                login = Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex() + 1)
    
    #write json
    def write_json(self, acc):
        data = self.open_json()
        data[acc[0]] = acc[1]
        with open('save_acc.json', 'w') as fw:
            json.dump(data, fw, ensure_ascii=False)
        fw.close()

    #open json
    def open_json(self):
        with open ('save_acc.json', 'r', encoding='utf-8') as fr:
            data = json.load(fr)
        fr.close()
        return data

    #getInfor
    def getAcc(self):
        list_infor = []
        username = self.username.text()
        password = self.password.text()
        confirmpass = self.confirmpass.text()
        if password == confirmpass:
            list_infor.append(username)
            list_infor.append(password)
        return list_infor 

#HN Weather 
url1 = "https://thoitiet.edu.vn/ha-noi/theo-gio"
url2 = "https://thoitiet.edu.vn/da-nang/theo-gio"
url3 = "https://thoitiet.edu.vn/ho-chi-minh/theo-gio"
#home page
from home import Ui_MainWindow
class Home(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.hnbutton.clicked.connect(self.hanoiweatherfunction)
        self.dnbutton.clicked.connect(self.danangweatherfunction)
        self.hcmbutton.clicked.connect(self.hcmweatherfunction)
        self.logoutbutton.clicked.connect(self.logoutfunction)

    #get weather/temp/date on the weather website and display on the screen after login successfully
    def hanoiweatherfunction(self):
        table = Table_HN(url_web = url1)
        widget.addWidget(table)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def danangweatherfunction(self):
        table = Table_HN(url_web = url2)
        widget.addWidget(table)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def hcmweatherfunction(self):
        table = Table_HN(url_web = url3)
        widget.addWidget(table)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    #logoutfunction
    def logoutfunction(self):
        QMessageBox.about(self, "Report","Log out successfully")
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Table_HN(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None, url_web = ""):
        super().__init__(parent)
        self.url_web = url_web
        self.setupUi(self)
        loadUi("table.ui", self)       
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)
        self.backbutton.clicked.connect(self.gotohomefunction)
        self.historybutton.clicked.connect(self.historyfunction)
        self.loaddata()

    

    def gotohomefunction(self):
        home = Home()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def historyfunction(self):
        history = History()
        widget.addWidget(history)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def text_reg(self, data):
        return re.sub("\r\n\s+","",data)

    #display table weather on the screen
    def loaddata(self):
        # print("load data")
        content = requests.get(self.url_web).text
        soup = BeautifulSoup(content, 'html.parser')

        # #get weather of HN
        weather_list = []
        for tag in soup.find_all("span", attrs = {"class":"summary-description-detail align-self-center ms-2"}):
            weather_list.append(self.text_reg(tag.text))
        print(weather_list)

        # #get temperate min of HN
        # tempmin_list = []
        # for tag in soup.find_all("span", attrs = {"class":"summary-temperature-min"}):
        #     tempmin_list.append(self.text_reg(tag.text))

        # #get temperature max of HN
        # tempmax_list = []
        # for tag in soup.find_all("span", attrs = {"class":"summary-temperature-max-value"}):
        #     tempmax_list.append(self.text_reg(tag.text))

        # #get weather HN with diffrent hours
        # hour_list = []
        # for tag in soup.find_all("h2", attrs = {"class":"summary-day text-dark font-h2"}):
        #     hour_list.append(self.text_reg(tag.text)[1:-1])

        # #convert three arrays to dictionary
        # infor_datas = []
        # for x, y, z, t in zip(weather_list, tempmin_list, tempmax_list, hour_list):
        #     infor_data = {'weather': x, 'temp_min': y, 'temp_max': z, 'hour': t}
        #     infor_datas.append(infor_data)


        # print("infor_datas",infor_datas)

        # self.infor_datas= infor_datas
        # row = 0
        # self.tableWidget.setRowCount(len(infor_datas))
        # for data in infor_datas:
        #     self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(data["weather"]))
        #     self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(data["temp_min"]))
        #     self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(data["temp_max"]))
        #     self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(data["hour"]))
        #     row += 1
        #     #save results to json file
        # dict_data = dict(weather = weather_list, temp_min = tempmin_list, temp_max = tempmax_list, hour = hour_list )
    
        # list_history = []
        # with open('history_data.json', 'r', encoding = 'utf-8') as fw:
        #     list_history = json.load(fw)
        # fw.close()
        # list_history.append(dict_data)

        # with open('history_data.json', 'w', encoding='utf-8') as fw:
        #     json.dump(list_history, fw, ensure_ascii=False)
        # fw.close()
        
    def show_table(self):
        #QWidfetTable: display table on the screen
        print("show table")

#History data
class History(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None, url = ""):
        super().__init__(parent)
        self.url = url
        self.history = self.open_file()
        self.setupUi(self)
        loadUi("history.ui", self)

    def open_file(self):
        with open("history_data.json", "r", encoding="utf-8") as fr:
            data = json.load(fr)
        fr.close()
        return data
    def show(self):
        row = 0
        self.tableWidget.setRowCount(len(self.history))
        for data in self.history:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(data["time"]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(data["data"]))
            row += 1


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # win = Login()
    win = Home()
    #exchange between diferent screens -> stack -> change index
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(win)
    widget.setFixedWidth(800)
    widget.setFixedHeight(650)
    widget.show()
    sys.exit(app.exec_())