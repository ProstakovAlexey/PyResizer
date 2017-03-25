# -*- coding: utf-8 -*-

# 
# Created by: FUNNYDMAN
#
# WARNING! All changes made in this file will be lost!

import sys
import os
from PIL import Image
import logging
import logging.handlers
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QLabel)
from PyQt5.QtCore import *
from PyQt5.QtGui import *


###############################################
#### LOGGING CLASS SETTINGS (py25+, py30+) ####
###############################################

f = logging.Formatter(fmt='%(levelname)s:%(name)s: %(message)s '
    '(%(asctime)s; %(filename)s:%(lineno)d)',
    datefmt="%Y-%m-%d %H:%M:%S")
handlers = [
    logging.handlers.RotatingFileHandler('logging/logfile.log', encoding='utf8',
        maxBytes=100000, backupCount=1),
    logging.StreamHandler()
]
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
for h in handlers:
    h.setFormatter(f)
    h.setLevel(logging.DEBUG)
    root_logger.addHandler(h)

##############################
#### END LOGGING SETTINGS ####
##############################


styleSheetPath = "qss/style.stylesheet"
global paths_alist
paths_alist = []
class QCustomWidget(QWidget):
     def __init__ (self, parent = None):
         super(QCustomWidget, self).__init__(parent)
         self.setAcceptDrops(True)

         self.mimeQLabel = QtWidgets.QPushButton('Drag image here')
         self.mimeQLabel.setFixedHeight(200)
         self.mimeQLabel.setObjectName("mimeQLabel")
         allQHBoxLayout = QtWidgets.QHBoxLayout()
         allQHBoxLayout.addWidget(self.mimeQLabel)
         self.setLayout(allQHBoxLayout)

         self.mimeQLabel.clicked.connect(self.select_image)
     def select_image(self):
         filename = QFileDialog.getOpenFileName(self, 'Open File', '',
                                               "Images (*.png)")
         
         paths_alist.append(filename[0])
         print("select")
         print(paths_alist)

     def dragEnterEvent(self, e):
         if e.mimeData().hasFormat('text/uri-list'):
             e.accept()
         else:
             e.ignore()
             print("faled")

     def dropEvent(self, e):
         data_raw = e.mimeData().urls()
         for i in data_raw:
              paths_alist.append(i.toString())
         print(paths_alist)
         
         



class Example(QWidget):

    def __init__(self):
        super().__init__()
        
        self.title = 'PyResizer'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 300

        self.init_ui()

    def init_ui(self):
        #self.resize(300, 300)
        #self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.name_programm = QtWidgets.QLabel('PyResizer')
        self.icon = QtWidgets.QPushButton('icon')
        self.exit_button = QtWidgets.QPushButton('X')
        self.minimize_button = QtWidgets.QPushButton('_')

        self.width_lineEdit = QtWidgets.QLineEdit()
        self.width_lineEdit.setValidator(QIntValidator())
        
        self.height_lineEdit = QtWidgets.QLineEdit()
        self.height_lineEdit.setValidator(QIntValidator())
          
        self.convert_button = QtWidgets.QPushButton('Convert')

        self.drag_field = QCustomWidget()

        #self.exit_button.setIcon(QtGui.QIcon('exit-icon.png'));
        #self.exit_button.setIconSize(QtCore.QSize(32, 32));

        #self.minimize_button.setIcon(QtGui.QIcon('min-icon.png'));
        #self.minimize_button.setIconSize(QtCore.QSize(32, 32));

        
        h_header_box = QtWidgets.QHBoxLayout()
        h_header_box.setContentsMargins(0, 0, 0, 0)
        h_header_box.setSpacing(0)
        h_header_box.addWidget(self.icon, alignment = QtCore.Qt.AlignLeft)
        h_header_box.addWidget(self.exit_button, alignment = QtCore.Qt.AlignRight)
        h_header_box.insertWidget(1, self.minimize_button, stretch=15, alignment = QtCore.Qt.AlignRight)


        h_field_box = QtWidgets.QHBoxLayout()
        h_field_box.addWidget(self.drag_field)
        h_field_box.setContentsMargins(0, 0, 0, 0)
        h_field_box.setSpacing(0)

        h_size_box = QtWidgets.QHBoxLayout()
        h_size_box.addWidget(self.width_lineEdit)
        h_size_box.addWidget(self.height_lineEdit)

        h_button_box = QtWidgets.QHBoxLayout()
        h_button_box.addWidget(self.convert_button)
        

        v_main_box = QtWidgets.QVBoxLayout()
        v_main_box.addLayout(h_header_box)
        v_main_box.addLayout(h_field_box)
        v_main_box.addLayout(h_size_box)
        v_main_box.addLayout(h_button_box)
        v_main_box.setContentsMargins(5,5,5,5)
        
        
        
        
        self.setLayout(v_main_box)
        
        """connecting buttons"""
        self.convert_button.clicked.connect(self.function_convert)

        #load stylesheets
        with open(styleSheetPath, "r") as fh:
            self.setStyleSheet(fh.read())

        self.show()
  
    def function_convert(self):
        try:
             width = int(self.width_lineEdit.text())
             height = int(self.height_lineEdit.text())
        except:
             print("enter size")
        else:
             size = (width, height)
             ff = ['logo.jpg', 'test.png']
             for i in ff:
                  image = Image.open(i)
                  filename, file_extension = os.path.splitext(i)
                  resized_image = image.resize(size, Image.ANTIALIAS)
                  resized_image.save(filename+file_extension)
             print("done")
             
        


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
