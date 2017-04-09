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
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication, QLabel, QDialog, QWidget)

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
global draged_img_paths, settings_dict
draged_img_paths = set()
settings_dict = {}

class QDragDropWidget(QWidget):
    def __init__(self, parent=None):
        super(QDragDropWidget, self).__init__(parent)
        self.setAcceptDrops(True)

        self.mineField = QtWidgets.QPushButton('Drag image here')
        self.mineField.setObjectName("mineField")
        allQHBoxLayout = QtWidgets.QHBoxLayout()
        allQHBoxLayout.addWidget(self.mineField)
        self.setLayout(allQHBoxLayout)

        self.mineField.clicked.connect(self.function_select_image)

    def function_select_image(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '',
                                               "Images (*.png *.jpg)")
        draged_img_paths.add(filename[0])
        self.mineField.setText("Selected:" + str(len(draged_img_paths)))

    def dragEnterEvent(self, e):
        self.mineField.setText('Drop here')
        if e.mimeData().hasFormat('text/uri-list'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        data_raw = e.mimeData().urls()
        for i in data_raw:
            draged_img_paths.add(i.toString())
        self.showSelectedImages()

    def showSelectedImages(self):
        # Перерисовывает кол-во выбранных файлов,
        # т.к. глобальная переменная меняется после конвертации
        self.mineField.setText("Selected:" + str(len(draged_img_paths)))

    def showMessage(self, num_message):
        message_alist = ["Error. You need input width or height",
                         "You need selected one or more images",
                         "Fail to convert",
                         "Convert successfull"]
        self.mineField.setText(message_alist[num_message])
 
class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon('images/logo.png'))
        
        self.save_settings = QtWidgets.QPushButton('Save')
        self.save_settings.setObjectName("save_settings")
        self.extension_1 = QtWidgets.QRadioButton('png')
        self.extension_2 = QtWidgets.QRadioButton('jpg')
        self.extension_3 = QtWidgets.QRadioButton('Как у исходного изображения')

        self.extension_1.setObjectName("extension_1")
        self.extension_2.setObjectName("extension_2")
        self.extension_3.setObjectName("extension_3")

        self.extension_3.setChecked(True)

        self.extension_group = QtWidgets.QGroupBox('extension')

        v_dmain_box = QtWidgets.QVBoxLayout()
        v_dmain_box.addWidget(self.extension_1)
        v_dmain_box.addWidget(self.extension_2)
        v_dmain_box.addWidget(self.extension_3)

        self.extension_group.setLayout(v_dmain_box)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(self.extension_group)
        vlayout.addWidget(self.save_settings)

        self.setLayout(vlayout)

        """connecting"""
        self.save_settings.clicked.connect(self.accept)

    def function_set_settings(self):
        extensions_list = [self.extension_1, self.extension_2, self.extension_3]
        
        for extension in extensions_list:
            if extension.isChecked():
                settings_dict.update({'extension': extension.text()})
                return extension


class QMainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'PyResizer v1.1'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 200

        self.init_ui()

    def init_ui(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)

        self.icon = QtWidgets.QPushButton(self.title)
        self.icon.setIcon(QtGui.QIcon('images/logo.png'));
        self.icon.setIconSize(QtCore.QSize(16, 16));
        self.icon.setObjectName("icon")

        self.exit_button = QtWidgets.QToolButton()
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setIcon(QtGui.QIcon('images/exit.png'));
        self.exit_button.setIconSize(QtCore.QSize(16, 16));

        self.minimize_button = QtWidgets.QToolButton()
        self.minimize_button.setObjectName("minimize_button")
        self.minimize_button.setIcon(QtGui.QIcon('images/min.png'));
        self.minimize_button.setIconSize(QtCore.QSize(16, 16));

        self.width_lineEdit = QtWidgets.QLineEdit()
        self.width_lineEdit.setValidator(QIntValidator(1, 9999))
        self.width_lineEdit.setPlaceholderText('width: px')

        self.height_lineEdit = QtWidgets.QLineEdit()
        self.height_lineEdit.setValidator(QIntValidator(1, 9999))
        self.height_lineEdit.setPlaceholderText('height: px')

        self.convert_button = QtWidgets.QPushButton('Convert')
        self.convert_button.setObjectName('convert_button')

        self.settings_button = QtWidgets.QPushButton('Settings')
        self.settings_button.setObjectName('settings_button')

        self.delete_button = QtWidgets.QToolButton()
        self.delete_button.setIcon(QtGui.QIcon('images/trash.png'));
        self.delete_button.setIconSize(QtCore.QSize(16, 16));
        self.delete_button.setObjectName('delete_button')

        self.drag_field = QDragDropWidget()

        h_header_box = QtWidgets.QHBoxLayout()
        h_header_box.setContentsMargins(0, 0, 0, 0)
        h_header_box.setSpacing(0)
        h_header_box.addWidget(self.icon, alignment=QtCore.Qt.AlignLeft)
        h_header_box.addWidget(self.exit_button, alignment=QtCore.Qt.AlignRight)
        h_header_box.insertWidget(1, self.minimize_button, stretch=15, alignment=QtCore.Qt.AlignRight)

        h_add_box = QtWidgets.QHBoxLayout()
        h_add_box.addWidget(self.delete_button)
        h_add_box.addWidget(self.settings_button)

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
        v_main_box.addLayout(h_add_box)
        v_main_box.addLayout(h_field_box)
        v_main_box.addLayout(h_size_box)
        v_main_box.addLayout(h_button_box)
        v_main_box.setContentsMargins(5, 5, 5, 5)

        self.setLayout(v_main_box)

        """connecting buttons"""
        self.convert_button.clicked.connect(self.function_convert)
        self.settings_button.clicked.connect(self.function_show_settings)
        self.delete_button.clicked.connect(self.function_del_paths)

        """headers buttons connecting"""
        self.exit_button.clicked.connect(self.function_exit)
        self.minimize_button.clicked.connect(self.function_minimize)

        # load stylesheets
        with open(styleSheetPath, "r") as fh:
            self.setStyleSheet(fh.read())

        self.show()

    def function_exit(self):
        self.close()

    def function_minimize(self):
        self.showMinimized()

    def function_del_paths(self):
        draged_img_paths.clear()
        self.drag_field.showSelectedImages()

    def function_show_settings(self):
        dialog = Dialog(self)
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            #сохраняем значение выбранной radiobutton
            data = dialog.function_set_settings()
            selected_option = data.objectName()

    def process_file_extension(self, file_extension):  
        if settings_dict['extension'] == 'png':
            file_extension = '.png'
            return file_extension
        elif settings_dict['extension'] == 'jpg':
            file_extension = '.jpg'
            return file_extension
        else:
            return file_extension

    def function_convert(self):
        if settings_dict:
            pass
        else:
            data = Dialog().function_set_settings()
    
        """You can input only one variable: width or height.
        If have only one: convert will be make proportionally"""
        width = 0
        height = 0
        make_convert = 0
        """Пытаемся выполнить конвертацию только в случае,
        если есть выбранные файлы."""
        if len(draged_img_paths):
            try:
                width = int(self.width_lineEdit.text().strip())
            except:
                pass
            try:
                height = int(self.height_lineEdit.text().strip())
            except:
                pass
            # В linux ссылка на файл имеет вид file:///home/alexey/..., делает и нее абсолютную
            draged_img_paths_clean = [string.replace(r'file:///', '') for string in draged_img_paths]
            # Обработка случая, когда не задали высоту и ширину
            if width == 0 and height == 0:
                self.drag_field.showMessage(0)
            # Задано одно или оба
            else:
                for i in draged_img_paths_clean:
                    # Возможно не удасться сконвертировать файл. Это может оказатся не изображение
                    # или файл защищен от записи
                    try:
                        image = Image.open(i)
                        # Ширина не задана
                        if width == 0:
                            ratio = (height / float(image.size[1]))
                            size = (int(image.size[0]*ratio), height)
                        # Не задана высота
                        elif height == 0:
                            ratio = (width / float(image.size[0]))
                            size = (width, int(image.size[1] * ratio))
                        # Заданы обе
                        else:
                            size = (width, height)
                        filename, file_extension = os.path.splitext(i)
                        resized_image = image.resize(size, Image.ANTIALIAS)
                        resized_image.save(str(filename + self.process_file_extension(file_extension)))
                    except:
                        self.drag_field.showMessage(2)
                    else:
                        make_convert += 1
        else:
            self.drag_field.showMessage(1)
        # Выполнили конвертацию, вывели сообщение. 
        if make_convert:
            #self.function_del_paths()
            self.drag_field.showMessage(3)

    # Переопределяем методы, тем самым давая возможность перемещать окно
    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QMainWindow()
    sys.exit(app.exec_())
