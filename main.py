# -*- coding: utf-8 -*-

# 
# Created by: FUNNYDMAN
#
# WARNING! All changes made in this file will be lost!

import sys
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QLabel)

styleSheetPath = "qss/style.stylesheet"

class QCustomWidget(QWidget):
     def __init__ (self, parent = None):
         super(QCustomWidget, self).__init__(parent)
         self.setAcceptDrops(True)

         self.mimeQLabel = QtWidgets.QWidget()
         self.mimeQLabel.setObjectName("mimeQLabel")
         allQHBoxLayout = QtWidgets.QHBoxLayout()
         allQHBoxLayout.addWidget(self.mimeQLabel)
         self.setLayout(allQHBoxLayout)



     def dragEnterEvent(self, e):
         if e.mimeData().hasFormat('text/uri-list'):
             e.accept()
         else:
             e.ignore()
             print("faled")

     def dropEvent(self, e):
         print(e.mimeData().text())



class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.name_programm = QtWidgets.QLabel('PyResizer')
        self.icon = QtWidgets.QPushButton('icon')
        self.exit_button = QtWidgets.QPushButton('X')
        self.minimize_button = QtWidgets.QPushButton('_')

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

        v_main_box = QtWidgets.QVBoxLayout()
        v_main_box.addLayout(h_header_box)
        v_main_box.addLayout(h_field_box)
        
        
        
        self.setLayout(v_main_box)
        
        


        #load stylesheets
        with open(styleSheetPath, "r") as fh:
            self.setStyleSheet(fh.read())

        self.show()
  

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
