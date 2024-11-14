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
        self.frame.setGeometry(QtCore.QRect(200, 80, 681, 221))
        self.frame.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.line_15 = QtWidgets.QFrame(parent=self.frame)
        self.line_15.setGeometry(QtCore.QRect(1149, 130, 51, 3))
        self.line_15.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_15.setObjectName('line_15')
        self.line_25 = QtWidgets.QFrame(parent=self.frame)
        self.line_25.setGeometry(QtCore.QRect(0, 165, 679, 4))
        self.line_25.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_25.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_25.setObjectName('line_25')
        self.line_26 = QtWidgets.QFrame(parent=self.frame)
        self.line_26.setGeometry(QtCore.QRect(0, 50, 681, 4))
        self.line_26.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_26.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_26.setObjectName('line_26')
        self.line_27 = QtWidgets.QFrame(parent=self.frame)
        self.line_27.setGeometry(QtCore.QRect(580, 0, 4, 51))
        self.line_27.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_27.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_27.setObjectName('line_27')
        self.line_34 = QtWidgets.QFrame(parent=self.frame)
        self.line_34.setGeometry(QtCore.QRect(50, 110, 630, 3))
        self.line_34.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.line_34.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_34.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_34.setObjectName('line_34')
        self.line_28 = QtWidgets.QFrame(parent=self.frame)
        self.line_28.setGeometry(QtCore.QRect(600, 50, 4, 61))
        self.line_28.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_28.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_28.setObjectName('line_28')
        self.line_36 = QtWidgets.QFrame(parent=self.frame)
        self.line_36.setGeometry(QtCore.QRect(410, 50, 4, 61))
        self.line_36.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_36.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_36.setObjectName('line_36')
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(330, 90, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet('color: white;\nbackground-color:BLACK;\nborder-color: transparent; \ntransform: rotate(270deg);')
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName('label')
        self.line_37 = QtWidgets.QFrame(parent=self.frame)
        self.line_37.setGeometry(QtCore.QRect(460, 0, 4, 51))
        self.line_37.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_37.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_37.setObjectName('line_37')
        self.line_38 = QtWidgets.QFrame(parent=self.frame)
        self.line_38.setGeometry(QtCore.QRect(340, 0, 4, 51))
        self.line_38.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_38.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_38.setObjectName('line_38')
        self.line_39 = QtWidgets.QFrame(parent=self.frame)
        self.line_39.setGeometry(QtCore.QRect(210, 0, 4, 51))
        self.line_39.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_39.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_39.setObjectName('line_39')
        self.line_40 = QtWidgets.QFrame(parent=self.frame)
        self.line_40.setGeometry(QtCore.QRect(100, 0, 4, 51))
        self.line_40.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_40.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_40.setObjectName('line_40')
        self.line_41 = QtWidgets.QFrame(parent=self.frame)
        self.line_41.setGeometry(QtCore.QRect(510, 50, 4, 61))
        self.line_41.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_41.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_41.setObjectName('line_41')
        self.line_42 = QtWidgets.QFrame(parent=self.frame)
        self.line_42.setGeometry(QtCore.QRect(210, 114, 4, 105))
        self.line_42.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_42.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_42.setObjectName('line_42')
        self.line_43 = QtWidgets.QFrame(parent=self.frame)
        self.line_43.setGeometry(QtCore.QRect(460, 114, 4, 105))
        self.line_43.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_43.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_43.setObjectName('line_43')
        self.line_44 = QtWidgets.QFrame(parent=self.frame)
        self.line_44.setGeometry(QtCore.QRect(560, 113, 4, 105))
        self.line_44.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_44.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_44.setObjectName('line_44')
        self.line_45 = QtWidgets.QFrame(parent=self.frame)
        self.line_45.setGeometry(QtCore.QRect(340, 130, 4, 88))
        self.line_45.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_45.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_45.setObjectName('line_45')
        self.line_60 = QtWidgets.QFrame(parent=self.frame)
        self.line_60.setGeometry(QtCore.QRect(0, 164, 3, 56))
        self.line_60.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.line_60.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_60.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_60.setObjectName('line_60')
        self.line_61 = QtWidgets.QFrame(parent=self.frame)
        self.line_61.setGeometry(QtCore.QRect(0, 0, 3, 56))
        self.line_61.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.line_61.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_61.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_61.setObjectName('line_61')
        self.frame_8 = QtWidgets.QFrame(parent=self.frame)
        self.frame_8.setGeometry(QtCore.QRect(0, 50, 50, 121))
        self.frame_8.setStyleSheet('background-color: #c0c0c0;\nborder-color: transparent; ')
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName('frame_8')
        self.frame_4 = QtWidgets.QFrame(parent=self.frame)
        self.frame_4.setGeometry(QtCore.QRect(45, 50, 50, 43))
        self.frame_4.setStyleSheet('background-color: #c0c0c0;border: none; ')
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName('frame_4')
        self.frame_7 = QtWidgets.QFrame(parent=self.frame)
        self.frame_7.setGeometry(QtCore.QRect(45, 130, 50, 43))
        self.frame_7.setStyleSheet('background-color: #c0c0c0; border: none;')
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName('frame_7')
        self.frame_12 = QtWidgets.QFrame(parent=self.frame_tela)
        self.frame_12.setGeometry(QtCore.QRect(900, 160, 147, 157))
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
        self.frame_6 = QtWidgets.QFrame(parent=self.frame_tela)
        self.frame_6.setGeometry(QtCore.QRect(1060, 160, 199, 161))
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
        self.frame_3 = QtWidgets.QFrame(parent=self.frame_tela)
        self.frame_3.setGeometry(QtCore.QRect(150, 520, 50, 50))
        self.frame_3.setStyleSheet('background-color: #c0c0c0;\nborder-color: transparent; ')
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName('frame_3')
        if self.tela.help_sccrol_painel == True:
            self.tela.monitora = False
            self.tela.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO CORONARIANA - 03N')
        self.labels = []
        for row in range(self.tela.conta_linha()):
            leito = self.tela.leito(row)
            if self.tela.help_sccrol_painel:
                label = QLabel(leito.text(), self.frame_tela)
            else:  # Inserido
                label = QLabel(leito.text(), self.tela.frame_do_monitoramento)

            label.setGeometry(0, 0, 60, 25)
            filename = 'monitora_UCO.csv'
            if self.tela.help_sccrol_painel:
                filename = 'monitora_UCOpainel.csv'

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
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    label.setCursor(Qt.CursorShape.OpenHandCursor)
                    label.mousePressEvent = lambda event, label=label: self.mousePressEvent(event, label)
                    label.mouseMoveEvent = lambda event, label=label: self.mouseMoveEvent(event, label)
                    label.setWordWrap(True)
                    fonte = QFont()
                    fonte.setPointSize(10)
                    label.setFont(fonte)
                    label.setStyleSheet('background-color: rgb(170, 255, 255);')
                    self.labels.append(label)
            except FileNotFoundError:
                print(1)
        else:  # Inserido
            self.atualizar_monitoramento(Form)
            self.conf_layout()
            if self.tela.help_sccrol_painel:
                self.frame.move(120, 120)
                self.frame_6.hide()
                self.frame_12.hide()
                self.tela.qt_vagos_uco = self.vago
                self.tela.qt_int_adulto = self.ocupado
                self.tela.total_bloq += self.bloqueado
                self.tela.total_vago += self.vago
                self.tela.total_rese += self.reservado
                self.tela.total_ocup += self.ocupado
                self.tela.qt_int_adulto_total = self.total

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
                new_pos.setY(max(frame_rect.top(), min(new_pos.y(), frame_rect.bottom() - label.height())))
                label.move(new_pos)
        filename = 'monitora_UCO.csv'
        if self.tela.help_sccrol_painel == True:
            filename = 'monitora_UCOpainel.csv'
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
        self.label.setText(_translate('Form', 'POSTO'))
        self.label_ocupado2_2.setText(_translate('Form', 'OCUPADO'))
        self.label_bloqueado2_2.setText(_translate('Form', 'BLOQUEADO'))
        self.label_vago2_2.setText(_translate('Form', 'VAGO'))
        self.label_reservado2_2.setText(_translate('Form', 'RESERVADO'))
        self.legenda_2.setText(_translate('Form', 'LEGENDA :'))
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