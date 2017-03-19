
import sys
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QLabel)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        path_to_img = 'smile.png'
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon(path_to_img))
        #im = Image.open(path_to_img)
        #(width, height) = im.size
        #print(width)
        #Убираем стандартное окно
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setWindowFlags(QtCore.Qt.WindowTitleHint)
        self.button = QtWidgets.QPushButton('Go')
        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.button)
        self.setLayout(v_box)
        """connecting"""
        self.button.clicked.connect(self.bnt_click)
        self.show()

    def bnt_click(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '',
                                               "Images (*.png)")
        image = Image.open(filename[0])
        width = image.size[0] #Определяем ширину. 
        height = image.size[1] #Определяем высоту. 	
        print(width)
        
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
