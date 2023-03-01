from PyQt5 import QtCore, QtGui, QtWidgets
from sql_query import SqlDBQuery
import json

class Ui_Dialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Ui_Dialog, self).__init__(parent)
        self.setObjectName("Dialog")
        self.resize(263, 209)
        with open('instruction.json','r') as file:
            self.data = json.load(file)
        self.SQL = SqlDBQuery()
        self.groupes = self.SQL.get_query(self.data['get_groupes'])
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(50, 170, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.student_create)
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(70, 130, 121, 22))
        self.comboBox.setObjectName("comboBox")
        for el in self.groupes:
            self.comboBox.addItem(el[0])
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(70, 80, 121, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 29, 121, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(70, 10, 121, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(60, 60, 151, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(80, 110, 101, 16))
        self.label_3.setObjectName("label_3")

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def student_create(self):
        if str(self.lineEdit.text())!='' and str(self.lineEdit_2.text())!='':
            for el in self.groupes:
                if el[0] == self.comboBox.currentText():
                    self.SQL.put_query(self.data['insert_student'],(str(self.lineEdit_2.text()),str(self.lineEdit.text()),str(el[1])))

        else:
            massage_box = QtWidgets.QMessageBox()
            massage_box.setWindowTitle('StudentError')
            massage_box.setText("Введенны неверные данные")
            massage_box.exec_()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Добавить студента"))
        self.label.setText(_translate("Dialog", "Введите имя студента:"))
        self.label_2.setText(_translate("Dialog", "Введите фамилию студента:"))
        self.label_3.setText(_translate("Dialog", "Выберите группу:"))


