# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: CTIADULTOmonitoramento.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

from PyQt6 import QtCore, QtGui, QtWidgets
import csv
from PyQt6.QtCore import QRect, Qt, QSettings, QStandardPaths, Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont

class Ui_Form(object):
    def setupUi(self, Form, frame, tela):
        self.tela = tela
        self.frame_tela = frame
        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        self.form = Form
        self.frame = QtWidgets.QFrame(parent=self.frame_tela)
        self.frame.setGeometry(QtCore.QRect(80, 110, 731, 181))
        self.frame.setStyleSheet('                border-top: 2px solid black;\nbackground-color: rgb(255, 255, 255);\n                border-bottom: 2px solid black;\n                border-right: 2px solid black;\n')
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.line = QtWidgets.QFrame(parent=self.frame)
        self.line.setGeometry(QtCore.QRect(0, 155, 3, 24))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName('line')
        self.line_2 = QtWidgets.QFrame(parent=self.frame)
        self.line_2.setGeometry(QtCore.QRect(0, 52, 3, 74))
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName('line_2')
        self.line_4 = QtWidgets.QFrame(parent=self.frame)
        self.line_4.setGeometry(QtCore.QRect(104, 52, 3, 74))
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_4.setObjectName('line_4')
        self.line_5 = QtWidgets.QFrame(parent=self.frame)
        self.line_5.setGeometry(QtCore.QRect(0, 101, 107, 3))
        self.line_5.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_5.setObjectName('line_5')
        self.line_6 = QtWidgets.QFrame(parent=self.frame)
        self.line_6.setGeometry(QtCore.QRect(53, 156, 3, 24))
        self.line_6.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_6.setObjectName('line_6')
        self.line_7 = QtWidgets.QFrame(parent=self.frame)
        self.line_7.setGeometry(QtCore.QRect(53, 103, 3, 24))
        self.line_7.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_7.setObjectName('line_7')
        self.line_8 = QtWidgets.QFrame(parent=self.frame)
        self.line_8.setGeometry(QtCore.QRect(105, 155, 3, 25))
        self.line_8.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_8.setObjectName('line_8')
        self.line_10 = QtWidgets.QFrame(parent=self.frame)
        self.line_10.setGeometry(QtCore.QRect(260, 51, 3, 128))
        self.line_10.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_10.setObjectName('line_10')
        self.line_12 = QtWidgets.QFrame(parent=self.frame)
        self.line_12.setGeometry(QtCore.QRect(420, 51, 3, 128))
        self.line_12.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_12.setObjectName('line_12')
        self.line_14 = QtWidgets.QFrame(parent=self.frame)
        self.line_14.setGeometry(QtCore.QRect(570, 51, 3, 128))
        self.line_14.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_14.setObjectName('line_14')
        self.line_15 = QtWidgets.QFrame(parent=self.frame)
        self.line_15.setGeometry(QtCore.QRect(879, 130, 51, 3))
        self.line_15.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_15.setObjectName('line_15')
        self.line_13 = QtWidgets.QFrame(parent=self.frame)
        self.line_13.setGeometry(QtCore.QRect(726, 130, 95, 3))
        self.line_13.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_13.setObjectName('line_13')
        self.frame_2 = QtWidgets.QFrame(parent=self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 2, 729, 52))
        self.frame_2.setStyleSheet('border-color: transparent\n;background-color: #c0c0c0')
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName('frame_2')
        self.line_9 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_9.setGeometry(QtCore.QRect(369, 66, 95, 3))
        self.line_9.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_9.setObjectName('line_9')
        self.frame_3 = QtWidgets.QFrame(parent=self.frame)
        self.frame_3.setGeometry(QtCore.QRect(3, 54, 102, 47))
        self.frame_3.setStyleSheet('border-color: transparent\n;background-color: #c0c0c0')
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName('frame_3')
        self.frame_4 = QtWidgets.QFrame(parent=self.frame_3)
        self.frame_4.setGeometry(QtCore.QRect(0, (-20), 102, 75))
        self.frame_4.setStyleSheet('border-color: transparent\n;background-color: #c0c0c0')
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName('frame_4')
        self.frame_5 = QtWidgets.QFrame(parent=self.frame_4)
        self.frame_5.setGeometry(QtCore.QRect(70, 40, 102, 47))
        self.frame_5.setStyleSheet('border-color: transparent\n;background-color: #c0c0c0')
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName('frame_5')
        self.line_16 = QtWidgets.QFrame(parent=self.frame)
        self.line_16.setGeometry(QtCore.QRect(53, 50, 107, 3))
        self.line_16.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_16.setObjectName('line_16')
        self.line_17 = QtWidgets.QFrame(parent=self.frame)
        self.line_17.setGeometry(QtCore.QRect(210, 50, 107, 3))
        self.line_17.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_17.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_17.setObjectName('line_17')
        self.line_18 = QtWidgets.QFrame(parent=self.frame)
        self.line_18.setGeometry(QtCore.QRect(370, 50, 107, 3))
        self.line_18.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_18.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_18.setObjectName('line_18')
        self.line_19 = QtWidgets.QFrame(parent=self.frame)
        self.line_19.setGeometry(QtCore.QRect(520, 50, 107, 3))
        self.line_19.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_19.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_19.setObjectName('line_19')
        self.line_20 = QtWidgets.QFrame(parent=self.frame)
        self.line_20.setGeometry(QtCore.QRect(672, 50, 58, 3))
        self.line_20.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_20.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_20.setObjectName('line_20')
        self.frame_7 = QtWidgets.QFrame(parent=self.frame)
        self.frame_7.setGeometry(QtCore.QRect(320, 20, 49, 63))
        self.frame_7.setStyleSheet('border-color: transparent\n;background-color: #c0c0c0')
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName('frame_7')
        self.frame_8 = QtWidgets.QFrame(parent=self.frame_7)
        self.frame_8.setGeometry(QtCore.QRect(160, 0, 49, 63))
        self.frame_8.setStyleSheet('border-color: transparent\n;background-color: #c0c0c0')
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName('frame_8')
        self.frame_9 = QtWidgets.QFrame(parent=self.frame)
        self.frame_9.setGeometry(QtCore.QRect(480, 20, 49, 63))
        self.frame_9.setStyleSheet('border-color: transparent\n;background-color: #c0c0c0')
        self.frame_9.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_9.setObjectName('frame_9')
        self.frame_10 = QtWidgets.QFrame(parent=self.frame)
        self.frame_10.setGeometry(QtCore.QRect(630, 20, 49, 63))
        self.frame_10.setStyleSheet('border-color: transparent\n;background-color: #c0c0c0')
        self.frame_10.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_10.setObjectName('frame_10')
        self.frame_13 = QtWidgets.QFrame(parent=self.frame)
        self.frame_13.setGeometry(QtCore.QRect(160, 20, 49, 63))
        self.frame_13.setStyleSheet('border-color: transparent\n;background-color: #c0c0c0')
        self.frame_13.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_13.setObjectName('frame_13')
        self.frame_14 = QtWidgets.QFrame(parent=self.frame_13)
        self.frame_14.setGeometry(QtCore.QRect(160, 0, 49, 63))
        self.frame_14.setStyleSheet('border-color: transparent\n;background-color: #c0c0c0')
        self.frame_14.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_14.setObjectName('frame_14')
        self.frame_12 = QtWidgets.QFrame(parent=self.frame_tela)
        self.frame_12.setGeometry(QtCore.QRect(340, 300, 147, 157))
        self.frame_12.setStyleSheet('background-color: rgb(255, 255, 255);\nborder: 2px solid #2E3D48')
        self.frame_12.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_12.setObjectName('frame_12')
        self.label_ocupado2_2 = QtWidgets.QLabel(parent=self.frame_12)
        self.label_ocupado2_2.setGeometry(QtCore.QRect(40, 130, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_ocupado2_2.setFont(font)
        self.label_ocupado2_2.setStyleSheet('\nborder: transparent;background-color: rgb(255, 255, 255);')
        self.label_ocupado2_2.setObjectName('label_ocupado2_2')
        self.label_bloqueado2_2 = QtWidgets.QLabel(parent=self.frame_12)
        self.label_bloqueado2_2.setGeometry(QtCore.QRect(40, 100, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_bloqueado2_2.setFont(font)
        self.label_bloqueado2_2.setStyleSheet('\nborder: transparent;background-color: rgb(255, 255, 255);')
        self.label_bloqueado2_2.setObjectName('label_bloqueado2_2')
        self.label_vago2_2 = QtWidgets.QLabel(parent=self.frame_12)
        self.label_vago2_2.setGeometry(QtCore.QRect(40, 40, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_vago2_2.setFont(font)
        self.label_vago2_2.setStyleSheet('background-color: rgb(255, 255, 255);\nborder: transparent;')
        self.label_vago2_2.setObjectName('label_vago2_2')
        self.label_reservado2_2 = QtWidgets.QLabel(parent=self.frame_12)
        self.label_reservado2_2.setGeometry(QtCore.QRect(40, 70, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_reservado2_2.setFont(font)
        self.label_reservado2_2.setStyleSheet('background-color: rgb(255, 255, 255);\nborder: transparent;')
        self.label_reservado2_2.setObjectName('label_reservado2_2')
        self.cor_legenda_red_2 = QtWidgets.QLabel(parent=self.frame_12)
        self.cor_legenda_red_2.setGeometry(QtCore.QRect(10, 130, 21, 21))
        self.cor_legenda_red_2.setStyleSheet('\nborder: transparent;background-color: rgb(255, 0, 0);')
        self.cor_legenda_red_2.setText('')
        self.cor_legenda_red_2.setObjectName('cor_legenda_red_2')
        self.cor_b_2 = QtWidgets.QLabel(parent=self.frame_12)
        self.cor_b_2.setGeometry(QtCore.QRect(10, 100, 21, 21))
        self.cor_b_2.setStyleSheet('\nborder: transparent;background-color: rgb(170, 170, 255);')
        self.cor_b_2.setText('')
        self.cor_b_2.setObjectName('cor_b_2')
        self.cor_legenda_blue_3 = QtWidgets.QLabel(parent=self.frame_12)
        self.cor_legenda_blue_3.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.cor_legenda_blue_3.setStyleSheet('background-color: rgb(170, 255, 255);\nborder-left-color: rgb(0, 0, 0);\nborder-bottom-color: rgb(0, 0, 0);\nborder-right-color: rgb(0, 0, 0);\nborder-right-color: rgb(0, 0, 0);\nborder-top-color: rgb(0, 0, 0);\nborder-color: rgb(0, 0, 0);\nborder: transparent;')
        self.cor_legenda_blue_3.setText('')
        self.cor_legenda_blue_3.setObjectName('cor_legenda_blue_3')
        self.legenda_2 = QtWidgets.QLabel(parent=self.frame_12)
        self.legenda_2.setGeometry(QtCore.QRect(10, 10, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.legenda_2.setFont(font)
        self.legenda_2.setStyleSheet('background-color: rgb(255, 255, 255);\nborder: transparent;')
        self.legenda_2.setObjectName('legenda_2')
        self.cor_legenda_yellow_2 = QtWidgets.QLabel(parent=self.frame_12)
        self.cor_legenda_yellow_2.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.cor_legenda_yellow_2.setStyleSheet('\nborder: transparent;\nbackground-color: rgb(255, 255, 0);')
        self.cor_legenda_yellow_2.setText('')
        self.cor_legenda_yellow_2.setObjectName('cor_legenda_yellow_2')
        self.label = QtWidgets.QLabel(parent=self.frame_tela)
        self.label.setGeometry(QtCore.QRect(510, 109, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet('color: white;\nbackground-color:BLACK;\nborder-color: transparent; \ntransform: rotate(270deg);')
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName('label')
        self.line_3 = QtWidgets.QFrame(parent=self.frame_tela)
        self.line_3.setGeometry(QtCore.QRect(270, 193, 3, 97))
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName('line_3')
        self.line_11 = QtWidgets.QFrame(parent=self.frame_tela)
        self.line_11.setGeometry(QtCore.QRect(422, 192, 3, 97))
        self.line_11.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_11.setObjectName('line_11')
        self.line_21 = QtWidgets.QFrame(parent=self.frame_tela)
        self.line_21.setGeometry(QtCore.QRect(582, 192, 3, 97))
        self.line_21.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_21.setObjectName('line_21')
        self.line_22 = QtWidgets.QFrame(parent=self.frame_tela)
        self.line_22.setGeometry(QtCore.QRect(734, 192, 3, 97))
        self.line_22.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_22.setObjectName('line_22')
        self.line_25 = QtWidgets.QFrame(parent=self.frame_tela)
        self.line_25.setGeometry(QtCore.QRect(187, 240, 623, 3))
        self.line_25.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_25.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_25.setObjectName('line_25')
        self.frame_6 = QtWidgets.QFrame(parent=self.frame_tela)
        self.frame_6.setGeometry(QtCore.QRect(510, 300, 199, 161))
        self.frame_6.setStyleSheet('background-color: rgb(255, 255, 255);\nborder: 2px solid #2E3D48')
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName('frame_6')
        self.label_ocupado1_2 = QtWidgets.QLabel(parent=self.frame_6)
        self.label_ocupado1_2.setGeometry(QtCore.QRect(10, 130, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_ocupado1_2.setFont(font)
        self.label_ocupado1_2.setStyleSheet('\nborder: transparent;background-color: rgb(255, 255, 255);')
        self.label_ocupado1_2.setObjectName('label_ocupado1_2')
        self.label_tabela_2 = QtWidgets.QLabel(parent=self.frame_6)
        self.label_tabela_2.setGeometry(QtCore.QRect(10, 10, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_tabela_2.setFont(font)
        self.label_tabela_2.setStyleSheet('\nborder: transparent;background-color: rgb(255, 255, 255);')
        self.label_tabela_2.setObjectName('label_tabela_2')
        self.qt_vago_2 = QtWidgets.QLabel(parent=self.frame_6)
        self.qt_vago_2.setGeometry(QtCore.QRect(130, 40, 61, 21))
        font = QtGui.QFont()
        self.qt_vago_2.setFont(font)
        self.qt_vago_2.setStyleSheet('\nborder: transparent;background-color: rgb(255, 255, 255);')
        self.qt_vago_2.setObjectName('qt_vago_2')
        self.label_bloq1_2 = QtWidgets.QLabel(parent=self.frame_6)
        self.label_bloq1_2.setGeometry(QtCore.QRect(10, 100, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_bloq1_2.setFont(font)
        self.label_bloq1_2.setStyleSheet('\nborder: transparent;background-color: rgb(255, 255, 255);')
        self.label_bloq1_2.setObjectName('label_bloq1_2')
        self.qt_reservado_2 = QtWidgets.QLabel(parent=self.frame_6)
        self.qt_reservado_2.setGeometry(QtCore.QRect(130, 70, 61, 21))
        font = QtGui.QFont()
        self.qt_reservado_2.setFont(font)
        self.qt_reservado_2.setStyleSheet('\nborder: transparent;background-color: rgb(255, 255, 255);')
        self.qt_reservado_2.setObjectName('qt_reservado_2')
        self.qt_bloqueado_2 = QtWidgets.QLabel(parent=self.frame_6)
        self.qt_bloqueado_2.setGeometry(QtCore.QRect(130, 100, 61, 21))
        font = QtGui.QFont()
        self.qt_bloqueado_2.setFont(font)
        self.qt_bloqueado_2.setStyleSheet('\nborder: transparent;background-color: rgb(255, 255, 255);')
        self.qt_bloqueado_2.setObjectName('qt_bloqueado_2')
        self.label_reser1_2 = QtWidgets.QLabel(parent=self.frame_6)
        self.label_reser1_2.setGeometry(QtCore.QRect(10, 70, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_reser1_2.setFont(font)
        self.label_reser1_2.setStyleSheet('\nborder: transparent;background-color: rgb(255, 255, 255);')
        self.label_reser1_2.setObjectName('label_reser1_2')
        self.qt_ocupado_2 = QtWidgets.QLabel(parent=self.frame_6)
        self.qt_ocupado_2.setGeometry(QtCore.QRect(130, 130, 61, 21))
        font = QtGui.QFont()
        self.qt_ocupado_2.setFont(font)
        self.qt_ocupado_2.setStyleSheet('\nborder: transparent;background-color: rgb(255, 255, 255);')
        self.qt_ocupado_2.setObjectName('qt_ocupado_2')
        self.label_vago1_2 = QtWidgets.QLabel(parent=self.frame_6)
        self.label_vago1_2.setGeometry(QtCore.QRect(10, 40, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_vago1_2.setFont(font)
        self.label_vago1_2.setStyleSheet('\nborder: transparent;background-color: rgb(255, 255, 255);')
        self.label_vago1_2.setObjectName('label_vago1_2')
        if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
            self.tela.monitora = False
            #self.tela.abri_cti(Form, 'CTI ADULTO - 03L')
            for cont, id in enumerate(self.tela.lista_titulo):
                if id == 'CTI ADULTO - 03L':
                    self.tela.abri_cti(Form, self.tela.lista_ids[cont], self.tela.lista_titulo[cont], self.tela.lista_dos_btn[cont])
                    break
        self.labels = []
        for row in range(self.tela.conta_linha()):
            leito = self.tela.leito(row)
            if 'aguardando' in leito.text():
                continue
            if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel:
                label = QLabel(leito.text(), self.frame_tela)
            else:  # inserted
                label = QLabel(leito.text(), self.tela.frame_do_monitoramento)
            label.setGeometry(0, 20, 60, 25)

            filename = 'monitora_3_leste.csv'
            if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
                filename = 'monitora_monitora_3_lestepainel.csv'

            try:
                with open(filename, mode='r') as file:
                    reader = csv.reader(file)
                    data = list(reader)
                    for row in range(len(data)):
                        if data[row][0] == leito.text():
                            x = int(data[row][1])
                            y = int(data[row][2])
                            label.setGeometry(x, y, 70, 25)
                            break
            except FileNotFoundError:
                print('Arquivo não encontrado, criando novo arquivo.')

            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setCursor(Qt.CursorShape.OpenHandCursor)
            label.mousePressEvent = lambda event, label_aux=label: self.mousePressEvent(event, label_aux)
            label.mouseMoveEvent = lambda event, label_aux=label: self.mouseMoveEvent(event, label_aux)
            label.setWordWrap(True)
            fonte = QFont()
            fonte.setPointSize(10)
            label.setFont(fonte)
            label.setStyleSheet('background-color: rgb(170, 255, 255);')
            self.labels.append(label)
            self.atualizar_monitoramento(Form)
            self.conf_layout()
            if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel:
                self.frame.move(80, 109)
                self.frame_6.hide()
                self.frame_12.hide()
                self.tela.qt_int_adulto = self.ocupado
                self.tela.total_bloq += self.bloqueado
                self.tela.total_vago += self.vago
                self.tela.total_rese += self.reservado
                self.tela.total_ocup += self.ocupado
                self.tela.qt_int_adulto_total = self.total
                self.tela.qt_vagos_3leste = self.vago

    def atualizar_monitoramento(self, Form):
        self.vago = 0
        self.reservado = 0
        self.ocupado = 0
        self.bloqueado = 0
        self.total = 0
        colum_nome = 0
        colum_status = 0
        for colum in range(1, self.tela.tabela_grade.columnCount()):
            item_pac = self.tela.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == 'NOME DO PACIENTE':
                colum_nome = colum
            if item_pac.text() == 'STATUS DO LEITO':
                colum_status = colum
        for row in range(self.tela.conta_linha()):
            selecao = self.tela.item(row, colum_status)
            leitos = self.tela.leito(row)
            LEITOS = leitos.text()
            paciente = self.tela.item(row, colum_nome).text()
            self.total += 1
            if selecao.text() == 'VAGO':
                print(1)
                self.vago += 1
                for label in self.labels:
                    if label.text() == LEITOS:
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        tooltip_text = 'Leito Vago'
                        label.setToolTip(tooltip_text)
            if selecao.text() == 'OCUPADO':
                for label in self.labels:
                    if label.text() == LEITOS:
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        tooltip_text = f'Paciente: {paciente} \n Leito: {LEITOS}'
                        label.setToolTip(tooltip_text)
                        font = QtGui.QFont()
                        font.setBold(True)
                        font.setWeight(75)
                        label.setFont(font)
                        label.setStyleSheet('background-color: rgb(255, 0, 0);')
                self.ocupado += 1
            if selecao.text() == 'RESERVADO':
                print(4145)
                for label in self.labels:
                    if label.text() == LEITOS:
                        print(LEITOS)
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        tooltip_text = f'Paciente: {paciente} \n Leito: {LEITOS}'
                        label.setToolTip(tooltip_text)
                        font = QtGui.QFont()
                        font.setBold(True)
                        font.setWeight(75)
                        label.setFont(font)
                        label.setStyleSheet('background-color: rgb(255, 255, 0);')
                self.reservado += 1
            if selecao.text() == 'BLOQUEADO':
                for label in self.labels:
                    if label.text() == LEITOS:
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        tooltip_text = 'Leito Bloqueado'
                        label.setToolTip(tooltip_text)
                        font = QtGui.QFont()
                        font.setBold(True)
                        font.setWeight(75)
                        label.setFont(font)
                        label.setStyleSheet('background-color: rgb(170, 170, 255);')
                self.bloqueado += 1
                if selecao.text() == 'BLOQUEADO POR FALTA DE FUNCIONÁRIOS':
                    self.tela.qt_se_fun += 1
                    self.bloqueado += 1
                if selecao.text() == 'PONTUAL - BLOQUEADO POR FALTA DE FUNCIONÁRIOS':
                    self.tela.qt_pront += 1
                    self.bloqueado += 1
                if selecao.text() == 'BLOQUEADO POR MANUTENÇÃO':
                    self.tela.qt_bl_manu += 1
                    self.bloqueado += 1
                if selecao.text() == 'BLOQUEADO POR VM/VNI':
                    self.tela.qt_bl_VM_VNI += 1
                    self.bloqueado += 1
        self.retranslateUi(Form)

    def mousePressEvent(self, event, label):
        label.mouse_offset = event.pos()

    def mouseMoveEvent(self, event, label):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = label.mapToParent(event.pos() - label.mouse_offset)
            label.move(new_pos)
            x, y = (new_pos.x(), new_pos.y())
            if not self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
                frame = self.tela.frame_do_monitoramento
            else:  # inserted
                frame = self.frame_tela
            if frame:
                frame_rect = frame.rect()
                new_pos.setX(max(frame_rect.left(), min(new_pos.x(), frame_rect.right() - label.width())))
                new_pos.setY(max(frame_rect.top(), min(new_pos.y(), frame_rect.bottom() - label.height())))
                label.move(new_pos)
        filename = 'monitora_3_leste.csv'
        if self.tela.help_sccrol_painel == True:
            filename = 'monitora_3_lestepainel.csv'
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for lisa in self.labels:
                texto = lisa.text()
                posicao = lisa.pos()
                writer.writerow([texto, posicao.x(), posicao.y()])

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        vago = str(self.vago)
        reservado = str(self.reservado)
        bloqueado = str(self.bloqueado)
        ocupado = str(self.ocupado)
        self.label_ocupado2_2.setText(_translate('Form', 'OCUPADO'))
        self.label_bloqueado2_2.setText(_translate('Form', 'BLOQUEADO'))
        self.label_vago2_2.setText(_translate('Form', 'VAGO'))
        self.label_reservado2_2.setText(_translate('Form', 'RESERVADO'))
        self.legenda_2.setText(_translate('Form', 'LEGENDA :'))
        self.label.setText(_translate('Form', 'POSTO'))
        self.label_ocupado1_2.setText(_translate('Form', 'OCUPADO :'))
        self.label_tabela_2.setText(_translate('Form', 'TABELA :'))
        self.qt_vago_2.setText(_translate('Form', vago))
        self.label_bloq1_2.setText(_translate('Form', 'BLOQUEADO :'))
        self.qt_reservado_2.setText(_translate('Form', reservado))
        self.qt_bloqueado_2.setText(_translate('Form', bloqueado))
        self.label_reser1_2.setText(_translate('Form', 'RESERVADO :'))
        self.qt_ocupado_2.setText(_translate('Form', ocupado))
        self.label_vago1_2.setText(_translate('Form', 'VAGO :'))

    def conf_layout(self):
        if self.settings.contains('tema'):
            font_name = self.settings.value('font', defaultValue='')
            backcolocor = self.settings.value('tema', defaultValue='')
            color = self.settings.value('color', defaultValue='')
            tamanho = int(self.settings.value('tamanho', defaultValue=10))
            self.backcolocor = backcolocor
            self.color = color
            self.font = font_name
            self.tamanho = tamanho
            if not self.tela.help_sccrol_painel == True:
                self.tela.frame_do_monitoramento.setStyleSheet('QFrame { background-color: transparent; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')