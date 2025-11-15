# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: oitavo_ALA_NORTE.py
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
        self.form = Form
        self.frame_12 = QtWidgets.QFrame(parent=self.frame_tela)
        self.frame_12.setGeometry(QtCore.QRect(711, 260, 147, 157))
        self.frame_12.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
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
        self.frame_13 = QtWidgets.QFrame(parent=self.frame_tela)
        self.frame_13.setGeometry(QtCore.QRect(351, 30, 351, 181))
        self.frame_13.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.frame_13.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_13.setObjectName('frame_13')
        self.line_21 = QtWidgets.QFrame(parent=self.frame_13)
        self.line_21.setGeometry(QtCore.QRect(140, 2, 3, 210))
        self.line_21.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.line_21.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_21.setObjectName('line_21')
        self.frame_14 = QtWidgets.QFrame(parent=self.frame_13)
        self.frame_14.setGeometry(QtCore.QRect(102, 140, 38, 50))
        self.frame_14.setStyleSheet('background-color: #c0c0c0;\nborder-color: transparent; ')
        self.frame_14.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_14.setObjectName('frame_14')
        self.frame_15 = QtWidgets.QFrame(parent=self.frame_13)
        self.frame_15.setGeometry(QtCore.QRect(180, 140, 38, 50))
        self.frame_15.setStyleSheet('background-color: #c0c0c0;\nborder-color: transparent; ')
        self.frame_15.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_15.setObjectName('frame_15')
        self.line_31 = QtWidgets.QFrame(parent=self.frame_13)
        self.line_31.setGeometry(QtCore.QRect(270, 0, 4, 179))
        self.line_31.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_31.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_31.setObjectName('line_31')
        self.line_32 = QtWidgets.QFrame(parent=self.frame_13)
        self.line_32.setGeometry(QtCore.QRect(180, 80, 170, 4))
        self.line_32.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_32.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_32.setObjectName('line_32')
        self.line_33 = QtWidgets.QFrame(parent=self.frame_13)
        self.line_33.setGeometry(QtCore.QRect(0, 80, 141, 4))
        self.line_33.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_33.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_33.setObjectName('line_33')
        self.line_34 = QtWidgets.QFrame(parent=self.frame_13)
        self.line_34.setGeometry(QtCore.QRect(70, 0, 4, 179))
        self.line_34.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_34.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_34.setObjectName('line_34')
        self.frame_6 = QtWidgets.QFrame(parent=self.frame_tela)
        self.frame_6.setGeometry(QtCore.QRect(871, 260, 199, 161))
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
        self.frame = QtWidgets.QFrame(parent=self.frame_tela)
        self.frame.setGeometry(QtCore.QRect(61, 250, 641, 171))
        self.frame.setStyleSheet('background-color: rgb(255, 255, 255);\n')
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.line_25 = QtWidgets.QFrame(parent=self.frame)
        self.line_25.setGeometry(QtCore.QRect(0, 110, 640, 4))
        self.line_25.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_25.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_25.setObjectName('line_25')
        self.line_26 = QtWidgets.QFrame(parent=self.frame)
        self.line_26.setGeometry(QtCore.QRect(0, 50, 640, 4))
        self.line_26.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_26.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_26.setObjectName('line_26')
        if self.tela.help_sccrol_painel == True:
            self.line_23 = QtWidgets.QFrame(parent=self.frame)
            self.line_23.setGeometry(QtCore.QRect(230, 0, 4, 179))
        else:  # inserted
            self.line_23 = QtWidgets.QFrame(parent=self.frame_12)
            self.line_23.setGeometry(QtCore.QRect(290, 490, 4, 179))
        self.line_23.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_23.setObjectName('line_23')
        self.line_27 = QtWidgets.QFrame(parent=self.frame)
        self.line_27.setGeometry(QtCore.QRect(380, 0, 4, 179))
        self.line_27.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_27.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_27.setObjectName('line_27')
        self.line_28 = QtWidgets.QFrame(parent=self.frame)
        self.line_28.setGeometry(QtCore.QRect(550, 0, 4, 179))
        self.line_28.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_28.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_28.setObjectName('line_28')
        self.line_4 = QtWidgets.QFrame(parent=self.frame)
        self.line_4.setGeometry(QtCore.QRect(160, 0, 3, 170))
        self.line_4.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_4.setObjectName('line_4')
        self.line_7 = QtWidgets.QFrame(parent=self.frame)
        self.line_7.setGeometry(QtCore.QRect(308, 0, 3, 170))
        self.line_7.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.line_7.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_7.setObjectName('line_7')
        self.frame_7 = QtWidgets.QFrame(parent=self.frame)
        self.frame_7.setGeometry(QtCore.QRect(2, (-8), 38, 50))
        self.frame_7.setStyleSheet('background-color: #c0c0c0;\nborder-color: transparent; ')
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName('frame_7')
        self.frame_9 = QtWidgets.QFrame(parent=self.frame)
        self.frame_9.setGeometry(QtCore.QRect(270, (-5), 38, 50))
        self.frame_9.setStyleSheet('background-color: #c0c0c0;\nborder-color: transparent; ')
        self.frame_9.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_9.setObjectName('frame_9')
        self.frame_10 = QtWidgets.QFrame(parent=self.frame)
        self.frame_10.setGeometry(QtCore.QRect(311, (-5), 38, 50))
        self.frame_10.setStyleSheet('background-color: #c0c0c0;\nborder-color: transparent; ')
        self.frame_10.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_10.setObjectName('frame_10')
        self.line_15 = QtWidgets.QFrame(parent=self.frame)
        self.line_15.setGeometry(QtCore.QRect(470, 0, 3, 170))
        self.line_15.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.line_15.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_15.setObjectName('line_15')
        self.frame_11 = QtWidgets.QFrame(parent=self.frame)
        self.frame_11.setGeometry(QtCore.QRect(473, (-5), 38, 50))
        self.frame_11.setStyleSheet('background-color: #c0c0c0;\nborder-color: transparent; ')
        self.frame_11.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_11.setObjectName('frame_11')
        self.line_10 = QtWidgets.QFrame(parent=self.frame_13)
        self.line_10.setGeometry(QtCore.QRect(180, 2, 3, 181))
        self.line_10.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.line_10.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_10.setObjectName('line_10')
        self.frame_2 = QtWidgets.QFrame(parent=self.frame_tela)
        if self.tela.help_sccrol_painel == True:
            self.frame_2.setGeometry(QtCore.QRect(62, 210, 640, 35))
        else:  # inserted
            self.frame_2.setGeometry(QtCore.QRect(62, 210, 640, 40))
        self.frame_2.setStyleSheet('background-color: #c0c0c0;\nborder: none;')
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName('frame_2')
        self.line_24 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_24.setGeometry(QtCore.QRect(0, 0, 391, 3))
        self.line_24.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.line_24.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_24.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_24.setObjectName('line_24')
        self.line_30 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_30.setGeometry(QtCore.QRect(507, 0, 130, 2))
        self.line_30.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.line_30.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_30.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_30.setObjectName('line_30')
        self.line_22 = QtWidgets.QFrame(parent=self.frame_tela)
        self.line_22.setGeometry(QtCore.QRect(90, (-3), 4, 170))
        self.line_22.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_22.setObjectName('line_22')
        self.labels = []
        if self.tela.help_sccrol_painel == True:
            self.tela.monitora = False
            # self.tela.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08N')

            for cont, id in enumerate(self.tela.lista_titulo):
                if id == 'UNIDADE DE INTERNAÇÃO - 08N':
                    self.tela.abri_cti(Form, self.tela.lista_ids[cont], self.tela.lista_titulo[cont], self.tela.lista_dos_btn[cont])
                    break
        for row in range(self.tela.conta_linha()):
            leito = self.tela.leito(row)
            if 'aguardando' in leito.text():
                continue
            if self.tela.help_sccrol_painel:
                label = QLabel(leito.text(), self.frame_tela)
            else:
                label = QLabel(leito.text(), self.tela.frame_do_monitoramento)

            label.setGeometry(0, 0, 60, 25)
            filename = 'monitora_oitavo_norte.csv'
            if self.tela.help_sccrol_painel:
                filename = 'monitora_oitavo_nortepainel.csv'

            try:
                with open(filename, mode='r') as file:
                    reader = csv.reader(file)
                    data = list(reader)
                    for data_row in data:
                        if data_row[0] == leito.text():
                            x = int(data_row[1])
                            y = int(data_row[2])
                            label.setGeometry(x, y, 70, 25)
                            break
            except FileNotFoundError:
                print('Arquivo não encontrado:', filename)

            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setCursor(Qt.CursorShape.OpenHandCursor)
            label.mousePressEvent = lambda event, label_aux=label: self.mousePressEvent(event, label_aux)
            label.mouseMoveEvent = lambda event, label_aux=label: self.mouseMoveEvent(event, label_aux)
            label.setWordWrap(True)
            fonte = QFont()
            fonte.setPointSize(10)
            label.setFont(fonte)
            label.setStyleSheet('background-color: rgb(170, 255, 255)')
            self.labels.append(label)
            self.atualizar_monitoramento(Form)

            self.conf_layout()
            if self.tela.help_sccrol_painel:
                self.frame.move(250, 243)
                self.frame_13.move(540, 28)
                self.frame_2.move(250, 208)
                self.line_22.move(330, 248)
                self.frame_12.hide()
                self.tela.qt_vagos_8norte = self.vago
                self.frame_6.hide()
                self.tela.total_bloq += self.bloqueado
                self.tela.total_vago += self.vago
                self.tela.total_rese += self.reservado
                self.tela.total_ocup += self.ocupado
                self.tela.qt_int_adulto2 += self.ocupado
                self.tela.qt_int_adulto_total2 += self.total

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
                for label in self.labels:
                    if label.text() == LEITOS:
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
            if self.tela.help_sccrol_painel == True:
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
            if not self.tela.help_sccrol_painel == True:
                frame = self.tela.frame_do_monitoramento
            else:  # inserted
                frame = self.frame_tela
            if frame:
                frame_rect = frame.rect()
                new_pos.setX(max(frame_rect.left(), min(new_pos.x(), frame_rect.right() - label.width())))
                new_pos.setY(max(frame_rect.top(), min(new_pos.y(), 415 - label.height())))
                if not self.tela.help_sccrol_painel == True:
                    new_pos.setY(max(frame_rect.top(), min(new_pos.y(), frame_rect.bottom() - label.height())))
                label.move(new_pos)
        filename = 'monitora_oitavo_norte.csv'
        if self.tela.help_sccrol_painel == True:
            filename = 'monitora_oitavo_nortepainel.csv'
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for lisa in self.labels:
                texto = lisa.text()
                posicao = lisa.pos()
                writer.writerow([texto, posicao.x(), posicao.y()])

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label_ocupado2_2.setText(_translate('Form', 'OCUPADO'))
        self.label_bloqueado2_2.setText(_translate('Form', 'BLOQUEADO'))
        self.label_vago2_2.setText(_translate('Form', 'VAGO'))
        self.label_reservado2_2.setText(_translate('Form', 'RESERVADO'))
        self.legenda_2.setText(_translate('Form', 'LEGENDA :'))
        self.label_ocupado1_2.setText(_translate('Form', 'OCUPADO :'))
        self.label_tabela_2.setText(_translate('Form', 'TABELA :'))
        vago = str(self.vago)
        reservado = str(self.reservado)
        bloqueado = str(self.bloqueado)
        ocupado = str(self.ocupado)
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