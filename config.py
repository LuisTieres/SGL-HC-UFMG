# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: config.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QIcon, QColor
from functools import partial
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QRect, Qt, QSettings, QStandardPaths, QPoint
from PyQt6.QtGui import QPainter

class Ui_Form(object):

    def setupUi(self, Form, dados):
        self.dados = dados
        super().__init__()
        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setGeometry(QtCore.QRect(400, 50, 543, 600))
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.dados.janela_config = self.frame
        self.Titulo = QtWidgets.QLabel('Configurações', parent=self.frame)
        self.Titulo.setGeometry(QtCore.QRect(90, 15, 261, 38))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.Titulo.setFont(font)
        icon = QIcon('configuracao.ico')
        pixmap = icon.pixmap(50, 50)
        self.icone = QtWidgets.QLabel(parent=self.frame)
        self.icone.setPixmap(pixmap)
        self.icone.setGeometry(QtCore.QRect(3, 3, 50, 50))
        self.icone.show()
        self.frame.setCursor(Qt.CursorShape.OpenHandCursor)
        self.frame.mousePressEvent = lambda event, frame=self.frame: self.mousePressEvent_2(event, frame)
        self.frame.mouseReleaseEvent = lambda event, frame=self.frame: self.mouseReleaseEvent_2(event, frame)
        self.frame.mouseMoveEvent = lambda event, frame=self.frame: self.mouseMoveEvent_2(event, frame)
        self.frame_6 = QtWidgets.QFrame(parent=self.frame)
        self.frame_6.setGeometry(QtCore.QRect(20, 60, 481, 161))
        self.frame_6.setStyleSheet('border: 2px solid #2E3D48;\n                                border-radius: 10px;\n')
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName('frame_6')
        self.label = QtWidgets.QLabel(parent=self.frame_6)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet('border : none;')
        self.label.setObjectName('label')
        self.fontComboBox = QtWidgets.QFontComboBox(parent=self.frame_6)
        self.fontComboBox.setGeometry(QtCore.QRect(10, 40, 187, 22))
        self.fontComboBox.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.fontComboBox.setObjectName('fontComboBox')
        self.fontComboBox.currentFontChanged.connect(self.change_font)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.frame_6)
        self.doubleSpinBox.setGeometry(QtCore.QRect(270, 30, 91, 41))
        self.doubleSpinBox.setStyleSheet('border: 2px solid #2E3D48;\n                                border-radius: 10px;')
        self.doubleSpinBox.setProperty('value', 12.0)
        self.doubleSpinBox.setObjectName('doubleSpinBox')
        self.doubleSpinBox.valueChanged.connect(self.change_font)
        self.label_7 = QtWidgets.QLabel(parent=self.frame_6)
        self.label_7.setGeometry(QtCore.QRect(270, 10, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet('border : none;')
        self.label_7.setObjectName('label_7')
        self.label_8 = QtWidgets.QLabel(parent=self.frame_6)
        self.label_8.setGeometry(QtCore.QRect(10, 90, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet('border : none;')
        self.label_8.setObjectName('label_8')
        self.btn_confirma = QtWidgets.QPushButton(parent=self.frame)
        self.btn_confirma.setGeometry(QtCore.QRect(330, 540, 81, 31))
        self.btn_confirma.setStyleSheet('border: 2px solid #2E3D48;\n                                border-radius: 10px;\n                                background-color: #FFFFFF;\n                                color: #2E3D48;')
        self.btn_confirma.setObjectName('pushButton')
        self.btn_confirma.clicked.connect(lambda: self.save_(Form))
        self.btn_padrao = QtWidgets.QPushButton(parent=self.frame)
        self.btn_padrao.setGeometry(QtCore.QRect(430, 540, 71, 31))
        self.btn_padrao.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')
        self.btn_padrao.setObjectName('btn_padrao')
        self.btn_padrao.clicked.connect(lambda: self.retornar_padrao(Form))
        self.frame_2 = QtWidgets.QFrame(parent=self.frame)
        self.frame_2.setGeometry(QtCore.QRect(20, 240, 481, 271))
        self.frame_2.setStyleSheet('border: 2px solid #2E3D48;\n                                border-radius: 10px;\n')
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName('frame_2')
        self.label_2 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(18, 6, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet('border: none;')
        self.label_2.setObjectName('label_2')
        self.pushButton_10 = QtWidgets.QPushButton(parent=self.frame_2)
        self.pushButton_10.setGeometry(QtCore.QRect(20, 170, 121, 81))
        self.pushButton_10.setStyleSheet('border: 2px solid #2E3D48;\nbackground-color: rgb(192, 192, 192);\n')
        self.pushButton_10.setText('')
        self.pushButton_10.setObjectName('pushButton_10')
        self.pushButton_11 = QtWidgets.QPushButton(parent=self.frame_2)
        self.pushButton_11.setGeometry(QtCore.QRect(180, 170, 121, 81))
        self.pushButton_11.setStyleSheet('border: 2px solid #2E3D48;\nbackground-color: rgb(0, 255, 127);\n')
        self.pushButton_11.setText('')
        self.pushButton_11.setObjectName('pushButton_11')
        self.pushButton_12 = QtWidgets.QPushButton(parent=self.frame_2)
        self.pushButton_12.setGeometry(QtCore.QRect(180, 50, 121, 81))
        self.pushButton_12.setStyleSheet('border: 2px solid #2E3D48;\nbackground-color: rgb(250, 255, 250);\n')
        self.pushButton_12.setText('')
        self.pushButton_12.setObjectName('pushButton_12')
        self.pushButton_13 = QtWidgets.QPushButton(parent=self.frame_2)
        self.pushButton_13.setGeometry(QtCore.QRect(20, 50, 121, 81))
        self.pushButton_13.setStyleSheet('border: 2px solid #2E3D48;\nbackground-color:#5DADE2\n')
        self.pushButton_13.setText('')
        self.pushButton_13.setObjectName('pushButton_13')
        self.black_radio = QtWidgets.QRadioButton(parent=self.frame_2)
        self.black_radio.setGeometry(QtCore.QRect(40, 200, 91, 21))
        self.black_radio.setStyleSheet('border: none;\nbackground-color: rgb(192, 192, 192);\n                color: white;')
        self.black_radio.setObjectName('black_radio')
        self.green_radio = QtWidgets.QRadioButton(parent=self.frame_2)
        self.green_radio.setGeometry(QtCore.QRect(200, 200, 82, 17))
        self.green_radio.setStyleSheet('border: none;\nbackground-color: rgb(0, 255, 127);\n                color: black;')
        self.green_radio.setObjectName('green_radio')
        self.blue_radio = QtWidgets.QRadioButton(parent=self.frame_2)
        self.blue_radio.setGeometry(QtCore.QRect(30, 80, 82, 17))
        self.blue_radio.setStyleSheet('border: none;\nbackground-color: #5DADE2;\n                color: BLACK;')
        self.blue_radio.setObjectName('blue_radio')
        self.white_radio = QtWidgets.QRadioButton(parent=self.frame_2)
        self.white_radio.setGeometry(QtCore.QRect(200, 80, 82, 17))
        self.white_radio.setStyleSheet('border: none;\nbackground-color: white;\n                color: BLACK;')
        self.white_radio.setObjectName('white_radio')
        self.original_styles = {self.black_radio: self.black_radio.styleSheet(), self.white_radio: self.white_radio.styleSheet(), self.green_radio: self.green_radio.styleSheet(), self.blue_radio: self.blue_radio.styleSheet()}
        self.black_radio.clicked.connect(self.change_color)
        self.white_radio.clicked.connect(self.change_color)
        self.green_radio.clicked.connect(self.change_color)
        self.blue_radio.clicked.connect(self.change_color)
        self.pushButton_11.clicked.connect(partial(self.set_radio_and_change_color, self.green_radio))
        self.pushButton_10.clicked.connect(partial(self.set_radio_and_change_color, self.black_radio))
        self.pushButton_13.clicked.connect(partial(self.set_radio_and_change_color, self.blue_radio))
        self.pushButton_12.clicked.connect(partial(self.set_radio_and_change_color, self.white_radio))
        if self.pushButton_13.isHidden():
            self.blue_radio.setChecked(True)
        self.pushButton_12.raise_()
        self.label_2.raise_()
        self.pushButton_10.raise_()
        self.pushButton_11.raise_()
        self.pushButton_13.raise_()
        self.black_radio.raise_()
        self.green_radio.raise_()
        self.blue_radio.raise_()
        self.white_radio.raise_()
        self.load(Form)
        self.retranslateUi(Form)
        self.draggable = False
        self.offset = QPoint()
        for widget in self.frame.findChildren(QtWidgets.QWidget):
            widget.show()
        self.frame.show()

    def fecharJanela(self, Form):
        Form.close()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate('Form', 'FONTE :'))
        self.label_7.setText(_translate('Form', 'TAMANHO DA FONTE: '))
        self.label_8.setText(_translate('Form', 'COR :'))
        self.btn_confirma.setText(_translate('Form', 'CONCLUÍDO'))
        self.btn_padrao.setText(_translate('Form', 'PADRÃO'))
        self.label_2.setText(_translate('Form', 'TEMA :'))
        self.black_radio.setText(_translate('Form', 'BLACK'))
        self.green_radio.setText(_translate('Form', 'VERDE'))
        self.blue_radio.setText(_translate('Form', 'PADRÃO'))
        self.white_radio.setText(_translate('Form', 'CLARO'))

    def createButton(self, color, x_position):
        button = QtWidgets.QPushButton('', self.frame_6)
        button.setGeometry(QRect(30 + x_position, 120, 21, 21))
        cor = 'white'
        if color != 'black':
            cor = 'black'
        button.setStyleSheet(f'background-color: {color};\nborder: none;color: {cor};')
        if self.color == color:
            button.setText('✔')
        button.setCheckable(True)
        button.clicked.connect(lambda: self.transferCheck(button, color))
        return button

    def transferCheck(self, clicked_button, color):
        self.color = color
        buttons = [child for child in self.frame_6.children() if isinstance(child, QtWidgets.QPushButton)]
        for button in buttons:
            if button != clicked_button:
                button.setChecked(False)
                button.setText('')
        if clicked_button.isChecked():
            if color == 'black':
                clicked_button.setStyleSheet('background-color: black;\nborder: none;\ncolor: white;')
                self.frame.setStyleSheet(f'background-color: {self.backcolocor};color: {self.color};font: {self.font};')
                for label in self.frame.findChildren(QtWidgets.QLabel):
                    label.setStyleSheet(f'color: {self.color}; font:  12px ; border:none')
            else:
                clicked_button.setStyleSheet(f'background-color: {color};\nborder: none;color: black;')
                for label in self.frame.findChildren(QtWidgets.QLabel):
                    label.setStyleSheet(f'color: {self.color}; font:  12px ; border:none')
                self.frame.setStyleSheet(f'background-color: {self.backcolocor};color: {self.color};font: {self.font};')
            clicked_button.setText('✔')
        else:
            clicked_button.setStyleSheet(f'background-color: {self.backcolocor};\nborder: none;')
            clicked_button.setText('')

    def change_color(self):
        color = None
        if self.black_radio.isChecked():
            color = QColor(192, 192, 192)
        elif self.white_radio.isChecked():
            color = QColor(255, 255, 255)
        elif self.green_radio.isChecked():
            color = QColor(144, 238, 144)
        elif self.blue_radio.isChecked():
            color = QColor(93, 173, 226)
        if color:
            self.backcolocor = color.name()
            self.frame.setStyleSheet(f'background-color: {color.name()};color: {self.color};font: {self.font};border: 2px solid #2E3D48;border-radius: 10px;')
            self.dados.frame.setStyleSheet(f'background-color: {color.name()};color: {self.color};font: {self.font};')

    def change_font(self):
        print(4)
        tamanho = int(self.doubleSpinBox.value())
        print(tamanho)
        self.font = self.fontComboBox.currentFont().family()
        for label in self.frame.findChildren(QtWidgets.QLabel):
            label.setStyleSheet(f'color: {self.color}; font:  {tamanho}px {self.font}; border:none')
        for radio_button, original_style in self.original_styles.items():
            radio_button.setStyleSheet(f'{original_style} color: none; font:  {tamanho}px {self.font};')
        print(13)

    def set_radio_and_change_color(self, radio_button):
        radio_button.setChecked(True)
        self.change_color()

    def retornar_padrao(self, Form):
        self.blue_radio.setChecked(True)
        self.doubleSpinBox.setProperty('value', 12.0)
        self.frame.setStyleSheet('background-color: #5DADE2;border: 2px solid #2E3D48;border-radius: 10px;')
        self.dados.frame.setStyleSheet('background-color: #5DADE2;')
        self.frame_6.setStyleSheet('border: 2px solid #2E3D48;\n          border-radius: 10px;\n')
        for label in self.frame.findChildren(QtWidgets.QLabel):
            label.setStyleSheet('color: black; font:  12px ; border:none')
        for radio_button, original_style in self.original_styles.items():
            radio_button.setStyleSheet(f'{original_style} color: none; font:  12px;')
        buttons = [child for child in self.frame_6.children() if isinstance(child, QtWidgets.QPushButton)]
        for button in buttons:
            background_color = button.palette().color(button.backgroundRole())
            if background_color == QtGui.QColor('black'):
                button.setText('✔')
            else:
                button.setText('')
        color = QColor(93, 173, 226)
        self.color = 'black'
        self.backcolocor = color.name()
        self.font = self.fontComboBox.currentFont().family()

    def save_(self, Form):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Confirmar?')
        icon = QIcon('C:\\Users\\luist\\OneDrive\\Área de Trabalho\\Ti\\Nova pasta\\HC-UFMG\\SGL\\warning.ico')
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            print(self.backcolocor)
            tamanho = int(self.doubleSpinBox.value())
            self.font = self.fontComboBox.currentFont().family()
            self.settings.setValue('tema', self.backcolocor)
            self.settings.setValue('color', self.color)
            self.settings.setValue('font', self.font)
            print(self.font)
            self.settings.setValue('tamanho', tamanho)
            print(self.font)
            self.dados.conf_layout()
            self.dados.config_Aberta = False
            self.frame.close()
        else:
            self.load(Form)

    def load(self, Form):
        if self.settings.contains('tema'):
            font_name = self.settings.value('font', defaultValue='')
            backcolocor = self.settings.value('tema', defaultValue='')
            print(backcolocor)
            color = self.settings.value('color', defaultValue='')
            tamanho = int(self.settings.value('tamanho', defaultValue=10))
            self.backcolocor = backcolocor
            print(backcolocor)
            self.color = color
            self.doubleSpinBox.setValue(tamanho)
            self.frame.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;border: 2px solid #2E3D48;border-radius: 10px;')
            for label in self.frame.findChildren(QtWidgets.QLabel):
                if label == self.Titulo:
                    label.setStyleSheet(f'color: {color}; font:  30px {font_name}; border:none')
                else:
                    label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name}; border:none')
            for radio_button, original_style in self.original_styles.items():
                print(tamanho)
                radio_button.setStyleSheet(f'{original_style} color: none; font:  {tamanho}px {font_name};')
            self.font = font_name
            print('tema')
        if not self.settings.contains('tema'):
            self.retornar_padrao(Form)
        button_colors = ['black', 'pink', 'orange', 'yellow', 'green']
        for i, color in enumerate(button_colors):
            button = self.createButton(color, i * 50)
        if self.backcolocor == QColor(192, 192, 192).name():
            self.black_radio.setChecked(True)
        if self.backcolocor == QColor(255, 255, 255).name():
            self.white_radio.setChecked(True)
        if self.backcolocor == QColor(144, 238, 144).name():
            self.green_radio.setChecked(True)
        if self.backcolocor == QColor(93, 173, 226).name():
            self.blue_radio.setChecked(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.y() < 30:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.draggable = False

    def mousePressEvent_2(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            centralwidget.setCursor(Qt.CursorShape.ClosedHandCursor)
        centralwidget.mouse_offset = event.pos()

    def mouseReleaseEvent_2(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            centralwidget.setCursor(Qt.CursorShape.OpenHandCursor)

    def mouseMoveEvent_2(self, event, centralwidget):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = centralwidget.mapToParent(event.pos() - centralwidget.mouse_offset)
            centralwidget.move(new_pos)
            x, y = (new_pos.x(), new_pos.y())