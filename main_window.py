from sql_query import *

from student import Ui_MainWindow
from create_student import Ui_Dialog
from PyQt5 import  QtWidgets


class My_win(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self)    
        self.ui.pushButton_2.pressed.connect(self.openDialog)

    def openDialog(self):
        dialog = Ui_Dialog(self)
        dialog.exec_()
        if dialog.buttonBox.accepted:
            self.ui.all_data_student()





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = My_win()
    window.show()
    sys.exit(app.exec_())
