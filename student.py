import json


from sql_query import *


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.SQL = SqlDBQuery()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(479, 508)
        with open('instruction.json','r') as file:
            self.data = json.load(file)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 20, 75, 23))
        self.pushButton.setObjectName("Find")
        self.pushButton.pressed.connect(self.find_for_groupe_or_name)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 351, 421))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Имя","Фамилия","Группа","Удалить"])
        self.all_data_student()
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(30, 20, 111, 22))
        self.comboBox.setObjectName("groupe")
        self.comboBox.addItem("")
        self.comboBox.addItems(x[0] for x in self.SQL.get_query(self.data['get_groupes']))
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 60, 121, 31))
        self.pushButton_2.setObjectName("AddStudent")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(150, 20, 113, 21))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("EnterNameSurname")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 0, 91, 21))
        self.label.setObjectName("ChoseGroupe")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150, 0, 121, 21))
        self.label_2.setObjectName("LabelNameSurname")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(370, 100, 101, 31))
        self.pushButton_3.setObjectName("AllStudent")
        self.pushButton_3.pressed.connect(self.all_data_student)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(360, 460, 111, 23))
        self.pushButton_4.setObjectName("DeleteStudent")
        self.pushButton_4.pressed.connect(self.delete_student)
        self.tableWidget.resizeColumnsToContents()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def find_for_groupe_or_name(self):
        if self.comboBox.currentText() == '' and self.lineEdit.text() !='':
            if len(self.lineEdit.text().split(' ')) == 2:
                name,surname = self.lineEdit.text().split(' ')
                student_srt_by_grp = self.SQL.get_query(self.data['sorted_by_name'],(name,surname))
                if len(student_srt_by_grp) != 0 and len(name)!=0 and len(surname)!=0:
                    self._row_place(student_srt_by_grp)
                else: 
                    self.not_found(f"Студента {name} {surname} не найденно")
            else:
                self.not_found("Введенны неверные данные!")
        elif self.comboBox.currentText() != '' and self.lineEdit.text() =='':
            groupe_id =self.groupe_id()
            student_srt_by_name = self.SQL.get_query(self.data["sorted_by_grp"],str(groupe_id))
            self._row_place(student_srt_by_name)
        elif self.comboBox.currentText() != '' and self.lineEdit.text() !='':
            groupe_id = self.groupe_id()
            if len(self.lineEdit.text().split(' ')) == 2:
                name,surname = self.lineEdit.text().split(' ')
                if len(name)!=0 and len(surname)!=0:
                    student_srt_by_grp_and_name = self.SQL.get_query(self.data['get_student_by_grp_and_name'],(name,surname,groupe_id))
                    if len(student_srt_by_grp_and_name) != 0:
                        self._row_place(student_srt_by_grp_and_name)
                    else: 
                        self.not_found(f"Студента {name} {surname} не найденно")
                else:
                    self.not_found("Введенны неверные данные!")
            else:
                self.not_found("Введенны неверные данные!")
        else:
            self.all_data_student()

    def groupe_id(self):
        for el in self.SQL.get_query(self.data['get_groupes']):
                if el[0] == self.comboBox.currentText():
                    groupe_id = el[1]
        return groupe_id

    def all_data_student(self):
        self.all_student = self.SQL.get_query(self.data["get_all_student"])
        self._row_place(self.all_student)
    

    def delete_student(self):
        all_data_student = self.SQL.get_query(self.data["get_student_wth_id"])
        for i in range(self.tableWidget.rowCount()):
            checkbox = self.tableWidget.item(i,3)
            if checkbox.checkState():
                student_id=0
                name,surname = self.tableWidget.model().index(i,0).data(),self.tableWidget.model().index(i,1).data()
                for el in all_data_student:
                    if el[1] == name and el[2] == surname:
                        student_id = el[0]
                self.SQL.delete_query(self.data['delete_student'],(student_id,))
        self.all_data_student()

    def _row_place(self,data):
        self.tableWidget.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(len(data[i])+1):
                if j==3:
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                              QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self.tableWidget.setItem(i,j,item)
                else:
                    self.tableWidget.setItem(i,j,QTableWidgetItem(data[i][j]))

    def not_found(self,text):
        massage_box = QtWidgets.QMessageBox()
        massage_box.setWindowTitle('StudentError')
        massage_box.setText(text)
        massage_box.exec_()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Таблица студентов"))
        self.pushButton.setText(_translate("MainWindow", "Найти"))
        self.pushButton_2.setText(_translate("MainWindow", "Добавить студента"))
        self.label.setText(_translate("MainWindow", "Выберите группу:"))
        self.label_2.setText(_translate("MainWindow", "Введите ФИ студента:"))
        self.pushButton_3.setText(_translate("MainWindow", "Все студенты"))
        self.pushButton_4.setText(_translate("MainWindow", "Удалить студента"))

