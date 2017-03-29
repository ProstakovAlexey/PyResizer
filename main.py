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
from PyQt5 import *
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QLabel, QDialog)
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
global draged_img_paths
draged_img_paths = set()

class QCustomWidget(QWidget):
     def __init__ (self, parent = None):
         super(QCustomWidget, self).__init__(parent)
         self.setAcceptDrops(True)

         self.mineField = QtWidgets.QPushButton('Drag image here')
         #self.mineField.setFixedHeight(200)
         self.mineField.setObjectName("mineField")
         allQHBoxLayout = QtWidgets.QHBoxLayout()
         allQHBoxLayout.addWidget(self.mineField)
         self.setLayout(allQHBoxLayout)

         self.mineField.clicked.connect(self.function_select_image)
     def function_select_image(self):
         filename = QFileDialog.getOpenFileName(self, 'Open File', '',
                                               "Images (*.png)")
         if filename[0] and draged_img_paths is None:
            draged_img_paths.add(filename[0])
         

     def dragEnterEvent(self, e):
         if e.mimeData().hasFormat('text/uri-list'):
             e.accept()
         else:
             e.ignore()

     def dropEvent(self, e):
         data_raw = e.mimeData().urls()
         for i in data_raw:
              draged_img_paths.add(i.toString())
         self.mineField.setText(str(len(draged_img_paths)))
         
class Dialog(QDialog):
    def __init__ (self, parent = None):
        super(Dialog, self).__init__(parent)
        self.setWindowTitle("Settings")
        #self.setWindowIcon(QIcon(path_to_img))
        self.save_settings = QtWidgets.QPushButton('Save')
        self.save_settings.setObjectName("save_settings")
        self.extension_1 = QtWidgets.QRadioButton('png')
        self.extension_2 = QtWidgets.QRadioButton('jpg')
        self.extension_3 = QtWidgets.QRadioButton('Как у исходного изображения')
        self.extension_3.setChecked(True)


        self.extension_group = QtWidgets.QGroupBox('extension')
                 
        v_dmain_box = QtWidgets.QVBoxLayout()
        v_dmain_box.addWidget(self.extension_1)
        v_dmain_box.addWidget(self.extension_2)
        v_dmain_box.addWidget(self.extension_3)
        
        self.extension_group.setLayout(v_dmain_box)

        
        self.size_1 = QtWidgets.QRadioButton('С соблюдением пропорций')
        self.size_2 = QtWidgets.QRadioButton('Точно до указанных размеров')
        self.size_2.setChecked(True)

        self.size_group = QtWidgets.QGroupBox('size')
        v_dsize_box = QtWidgets.QVBoxLayout()
        v_dsize_box.addWidget(self.size_1)
        v_dsize_box.addWidget(self.size_2)
        self.size_group.setLayout(v_dsize_box)
        
        self.name_1 = QtWidgets.QRadioButton('Оставить прежним')
        self.name_2 = QtWidgets.QRadioButton('По формату')
        self.name_1.setChecked(True)

        self.name_group = QtWidgets.QGroupBox('name of file')
        v_dname_box = QtWidgets.QVBoxLayout()
        v_dname_box.addWidget(self.name_1)
        v_dname_box.addWidget(self.name_2)
        self.name_group.setLayout(v_dname_box)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(self.extension_group)
        vlayout.addWidget(self.size_group)
        vlayout.addWidget(self.name_group)
        
        vlayout.addWidget(self.save_settings)
        
        self.setLayout(vlayout)
        
        """connecting"""
        self.save_settings.clicked.connect(self.function_set_settings)
    
    def function_set_settings(self):
        extensions_list = [self.extension_1, self.extension_2, self.extension_3]
        sizes_list = [self.size_1, self.size_2]
        names_list = [self.name_1, self.name_2]
        settings_dict = {}

        for extension in extensions_list:
            if extension.isChecked():
               settings_dict.update({'extension' : extension.text()})

        for size in sizes_list:
            if size.isChecked():
               settings_dict.update({'size' : size.text()})

        for name in names_list:
            if name.isChecked():
               settings_dict.update({'name' : name.text()})
        
        return settings_dict     
        
        
class Example(QWidget):

    def __init__(self):
        super().__init__()
        
        self.title = 'PyResizer'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 200

        self.init_ui()

    def init_ui(self):
        #self.resize(300, 300)
        #self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)

        self.icon = QtWidgets.QPushButton(self.title)
        self.icon.setIcon(QtGui.QIcon('387.png'));
        self.icon.setIconSize(QtCore.QSize(16, 16));
        self.icon.setObjectName("icon")
        
        
        self.exit_button = QtWidgets.QToolButton()
        self.exit_button.setText('X')
        self.exit_button.setObjectName("exit_button")
         
        self.minimize_button = QtWidgets.QToolButton()
        self.minimize_button.setText('_')
        self.minimize_button.setObjectName("minimize_button")

        self.status_label = QtWidgets.QLabel()
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.status_label.hide()
        
        self.width_lineEdit = QtWidgets.QLineEdit()
        self.width_lineEdit.setValidator(QIntValidator(1, 9999))
        self.width_lineEdit.setPlaceholderText('width')
        
        self.height_lineEdit = QtWidgets.QLineEdit()
        self.height_lineEdit.setValidator(QIntValidator(1, 9999))
        self.height_lineEdit.setPlaceholderText('height')
          
        self.convert_button = QtWidgets.QPushButton('Convert')

        self.settings_button = QtWidgets.QPushButton('Settings')

        self.delete_button = QtWidgets.QToolButton()
        self.delete_button.setIcon(QtGui.QIcon('delete-icon.png'));
        self.delete_button.setIconSize(QtCore.QSize(16, 16));
        
        self.drag_field = QCustomWidget()

        
        h_header_box = QtWidgets.QHBoxLayout()
        h_header_box.setContentsMargins(0, 0, 0, 0)
        h_header_box.setSpacing(0)
        h_header_box.addWidget(self.icon, alignment = QtCore.Qt.AlignLeft)
        h_header_box.addWidget(self.exit_button, alignment = QtCore.Qt.AlignRight)
        h_header_box.insertWidget(1, self.minimize_button, stretch=15, alignment = QtCore.Qt.AlignRight)

        h_add_box = QtWidgets.QHBoxLayout()
        h_add_box.addWidget(self.delete_button)
        h_add_box.addWidget(self.settings_button)
        

        h_field_box = QtWidgets.QHBoxLayout()
        #h_field_box.addStretch(2)
        h_field_box.addWidget(self.drag_field)
        h_field_box.setContentsMargins(0, 0, 0, 0)
        h_field_box.setSpacing(0)

        h_error_box = QtWidgets.QHBoxLayout()
        h_error_box.addWidget(self.status_label)


        h_size_box = QtWidgets.QHBoxLayout()
        h_size_box.addWidget(self.width_lineEdit)
        h_size_box.addWidget(self.height_lineEdit)

        h_button_box = QtWidgets.QHBoxLayout()
        h_button_box.addWidget(self.convert_button)
        

        v_main_box = QtWidgets.QVBoxLayout()
        v_main_box.addLayout(h_header_box)
        v_main_box.addLayout(h_add_box)
        v_main_box.addLayout(h_field_box)
        #v_main_box.addLayout(h_error_box)
        v_main_box.addLayout(h_size_box)
        v_main_box.addLayout(h_button_box)
        v_main_box.setContentsMargins(5, 5, 5, 5)
        
        self.setLayout(v_main_box)
        
        """connecting buttons"""
        self.convert_button.clicked.connect(self.function_convert)
        self.settings_button.clicked.connect(self.function_show_settings)
        self.delete_button.clicked.connect(self.function_del_paths)

        """headers buttons"""
        self.exit_button.clicked.connect(self.function_exit)
        self.minimize_button.clicked.connect(self.function_minimize)

        #load stylesheets
        with open(styleSheetPath, "r") as fh:
            self.setStyleSheet(fh.read())

        self.show()

    def function_exit(self):
        self.close()

    def function_minimize(self):
        self.showMinimized()
        
    def function_del_paths(self):
        draged_img_paths.clear()
        #QCustomWidget().mineField.setText('0')
        print(draged_img_paths)
        

    def function_show_settings(self):
        some = Dialog(self)
        result = some.exec_()
        if result == QtWidgets.QDialog.Accepted:
            pass
        else:
            print("нажата кнопка cancel")

    def process_file_extension(self, file_extension):
        setting_adict = Dialog().function_set_settings()
        if setting_adict['extension']=='png':
            file_extension='.png'
            return file_extension
        elif setting_adict['extension']=='jpg':
            file_extension='.jpg'
            return file_extension
        else:
            return file_extension

    def process_file_name(self, filename):
        if setting_adict['name']=='Как у исходного изображения':
            return filename
        else:
            return 'some_image'

    def process_file_size(self, size):
        setting_adict = Dialog().function_set_settings()
        if setting_adict['size']=='Точно до указанных размеров':
            pass
  
    def function_convert(self):
        try:
             width = int(self.width_lineEdit.text())
             height = int(self.height_lineEdit.text())
        except:
             self.status_label.show()
             self.status_label.setText("Введите размер")
        else:
             self.status_label.hide()
             size = (width, height)
             setting_adict = Dialog().function_set_settings()
             draged_img_paths_clean= [string[8:] for string in draged_img_paths]
             for i in draged_img_paths_clean:
                  image = Image.open(i)
                  filename, file_extension = os.path.splitext(i)
                  resized_image = image.resize(size, Image.ANTIALIAS)
                  resized_image.save(filename+self.process_file_extension(file_extension))
             self.status_label.show()
             self.status_label.setText("Готово")
             
    #Переопределяем методы, тем самым давая возможность перемещать окно
    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
