
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtWidgets, QtCore


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        #Убираем стандартное окно
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
