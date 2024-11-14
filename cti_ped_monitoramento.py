from PyQt6.QtCore import QRect, Qt, QSettings, QStandardPaths, Qt
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QLabel
from functools import partial
import csv

class Ui_Form(object):
    def setupUi(self, Form, frame, tela):
        print(21)
        self.tela = tela
        self.settings = QSettings('HC', 'SGL')
        self.form = Form
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        self.frame = frame
        self.frame_2 = QtWidgets.QFrame(parent=self.frame)
        self.frame_2.setGeometry(QtCore.QRect(300, 10, 401, 441))
        self.frame_2.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName('frame_2')
        self.label_6 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(228, 260, 61, 91))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet('alternate-background-color: rgb(144, 144, 144);\nbackground-color: rgb(103, 103, 103);')
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_6.setObjectName('label_6')
        self.label_7 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(140, 280, 3, 161))
        self.label_7.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_7.setObjectName('label_7')
        self.label_8 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(140, 120, 3, 121))
        self.label_8.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_8.setObjectName('label_8')
        self.label_9 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_9.setGeometry(QtCore.QRect(0, 230, 142, 3))
        self.label_9.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_9.setObjectName('label_9')
        self.label_10 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_10.setGeometry(QtCore.QRect(228, 150, 172, 3))
        self.label_10.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_10.setObjectName('label_10')
        self.label_11 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_11.setGeometry(QtCore.QRect(228, 380, 3, 59))
        self.label_11.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_11.setObjectName('label_11')
        self.label_17 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_17.setGeometry(QtCore.QRect(228, 150, 3, 59))
        self.label_17.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_17.setObjectName('label_17')
        self.label_18 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_18.setGeometry(QtCore.QRect(0, 330, 142, 3))
        self.label_18.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_18.setObjectName('label_18')
        self.label_19 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_19.setGeometry(QtCore.QRect(0, 297, 102, 3))
        self.label_19.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_19.setObjectName('label_19')
        self.label_20 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_20.setGeometry(QtCore.QRect(0, 268, 102, 3))
        self.label_20.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_20.setObjectName('label_20')
        self.label_21 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_21.setGeometry(QtCore.QRect(100, 230, 3, 101))
        self.label_21.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_21.setObjectName('label_21')
        self.label_22 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_22.setGeometry(QtCore.QRect(31, 120, 110, 3))
        self.label_22.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_22.setObjectName('label_22')
        self.label_23 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_23.setGeometry(QtCore.QRect(30, 20, 3, 101))
        self.label_23.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_23.setObjectName('label_23')
        self.label_24 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_24.setGeometry(QtCore.QRect(31, 20, 310, 3))
        self.label_24.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_24.setObjectName('label_24')
        self.label_25 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_25.setGeometry(QtCore.QRect(340, 20, 3, 101))
        self.label_25.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_25.setObjectName('label_25')
        self.label_26 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_26.setGeometry(QtCore.QRect(230, 120, 111, 3))
        self.label_26.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.label_26.setObjectName('label_26')
        self.label_29 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_29.setGeometry(QtCore.QRect(160, 60, 71, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setStyleSheet('alternate-background-color: rgb(144, 144, 144);\nbackground-color: rgb(103, 103, 103);')
        self.label_29.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_29.setObjectName('label_29')
        self.line_17 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_17.setGeometry(QtCore.QRect(33, 70, 126, 3))
        self.line_17.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_17.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_17.setObjectName('line_17')
        self.line_18 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_18.setGeometry(QtCore.QRect(231, 70, 110, 3))
        self.line_18.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_18.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_18.setObjectName('line_18')
        self.line_19 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_19.setGeometry(QtCore.QRect(230, 200, 171, 3))
        self.line_19.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_19.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_19.setObjectName('line_19')
        self.line_20 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_20.setGeometry(QtCore.QRect(319, 330, 79, 3))
        self.line_20.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_20.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_20.setObjectName('line_20')
        self.line = QtWidgets.QFrame(parent=self.frame_2)
        self.line.setGeometry(QtCore.QRect(320, 153, 3, 286))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName('line')
        self.line_21 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_21.setGeometry(QtCore.QRect(233, 390, 164, 3))
        self.line_21.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_21.setObjectName('line_21')
        self.line_22 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_22.setGeometry(QtCore.QRect(320, 280, 79, 3))
        self.line_22.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_22.setObjectName('line_22')
        self.line_23 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_23.setGeometry(QtCore.QRect(320, 240, 79, 3))
        self.line_23.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_23.setObjectName('line_23')
        self.line_2 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_2.setGeometry(QtCore.QRect(130, 23, 3, 97))
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName('line_2')
        self.line_3 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_3.setGeometry(QtCore.QRect(240, 23, 3, 97))
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName('line_3')
        self.leito9_25 = QtWidgets.QLabel(parent=self.frame_2)
        self.leito9_25.setGeometry(QtCore.QRect(143, 120, 85, 319))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.leito9_25.setFont(font)
        self.leito9_25.setStyleSheet('\nbackground-color: rgb(211, 211, 211);border:none;')
        self.leito9_25.setText('')
        self.leito9_25.setObjectName('leito9_25')
        self.leito9_26 = QtWidgets.QLabel(parent=self.frame_2)
        self.leito9_26.setGeometry(QtCore.QRect(220, 350, 41, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.leito9_26.setFont(font)
        self.leito9_26.setStyleSheet('\nbackground-color: rgb(211, 211, 211);border:none;')
        self.leito9_26.setText('')
        self.leito9_26.setObjectName('leito9_26')
        self.leito9_27 = QtWidgets.QLabel(parent=self.frame_2)
        self.leito9_27.setGeometry(QtCore.QRect(103, 240, 50, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.leito9_27.setFont(font)
        self.leito9_27.setStyleSheet('\nbackground-color: rgb(211, 211, 211);border:none;')
        self.leito9_27.setText('')
        self.leito9_27.setObjectName('leito9_27')
        self.leito9_28 = QtWidgets.QLabel(parent=self.frame_2)
        self.leito9_28.setGeometry(QtCore.QRect(103, 233, 37, 97))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.leito9_28.setFont(font)
        self.leito9_28.setStyleSheet('\nbackground-color: rgb(211, 211, 211);border:none;')
        self.leito9_28.setText('')
        self.leito9_28.setObjectName('leito9_28')
        self.frame2 = QtWidgets.QLabel(parent=self.frame)
        self.frame2.setGeometry(QtCore.QRect(870, 290, 199, 161))
        self.frame2.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.frame2.setText('')
        self.frame2.setObjectName('frame2')
        self.frame1 = QtWidgets.QLabel(parent=self.frame)
        self.frame1.setGeometry(QtCore.QRect(713, 293, 147, 157))
        self.frame1.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.frame1.setText('')
        self.frame1.setObjectName('frame1')
        self.label_reservado2 = QtWidgets.QLabel(parent=self.frame)
        self.label_reservado2.setGeometry(QtCore.QRect(750, 360, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_reservado2.setFont(font)
        self.label_reservado2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.label_reservado2.setObjectName('label_reservado2')
        self.label_ocupado2 = QtWidgets.QLabel(parent=self.frame)
        self.label_ocupado2.setGeometry(QtCore.QRect(750, 420, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_ocupado2.setFont(font)
        self.label_ocupado2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.label_ocupado2.setObjectName('label_ocupado2')
        self.cor_legenda_red = QtWidgets.QLabel(parent=self.frame)
        self.cor_legenda_red.setGeometry(QtCore.QRect(720, 420, 21, 21))
        self.cor_legenda_red.setStyleSheet('background-color: rgb(255, 0, 0);')
        self.cor_legenda_red.setText('')
        self.cor_legenda_red.setObjectName('cor_legenda_red')
        self.label_bloqueado2 = QtWidgets.QLabel(parent=self.frame)
        self.label_bloqueado2.setGeometry(QtCore.QRect(750, 390, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_bloqueado2.setFont(font)
        self.label_bloqueado2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.label_bloqueado2.setObjectName('label_bloqueado2')
        self.cor_b = QtWidgets.QLabel(parent=self.frame)
        self.cor_b.setGeometry(QtCore.QRect(720, 390, 21, 21))
        self.cor_b.setStyleSheet('background-color: rgb(170, 170, 255);')
        self.cor_b.setText('')
        self.cor_b.setObjectName('cor_b')
        self.cor_legenda_blue_2 = QtWidgets.QLabel(parent=self.frame)
        self.cor_legenda_blue_2.setGeometry(QtCore.QRect(720, 330, 21, 21))
        self.cor_legenda_blue_2.setStyleSheet('background-color: rgb(170, 255, 255);\nborder-left-color: rgb(0, 0, 0);\nborder-bottom-color: rgb(0, 0, 0);\nborder-right-color: rgb(0, 0, 0);\nborder-right-color: rgb(0, 0, 0);\nborder-top-color: rgb(0, 0, 0);\nborder-color: rgb(0, 0, 0);')
        self.cor_legenda_blue_2.setText('')
        self.cor_legenda_blue_2.setObjectName('cor_legenda_blue_2')
        self.cor_legenda_yellow = QtWidgets.QLabel(parent=self.frame)
        self.cor_legenda_yellow.setGeometry(QtCore.QRect(720, 360, 21, 21))
        self.cor_legenda_yellow.setStyleSheet('background-color: rgb(255, 255, 0);')
        self.cor_legenda_yellow.setText('')
        self.cor_legenda_yellow.setObjectName('cor_legenda_yellow')
        self.legenda = QtWidgets.QLabel(parent=self.frame)
        self.legenda.setGeometry(QtCore.QRect(720, 300, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.legenda.setFont(font)
        self.legenda.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.legenda.setObjectName('legenda')
        self.label_vago2 = QtWidgets.QLabel(parent=self.frame)
        self.label_vago2.setGeometry(QtCore.QRect(750, 330, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_vago2.setFont(font)
        self.label_vago2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.label_vago2.setObjectName('label_vago2')
        self.qt_bloqueado_2 = QtWidgets.QLabel(parent=self.frame)
        self.qt_bloqueado_2.setGeometry(QtCore.QRect(1000, 390, 61, 21))
        font = QtGui.QFont()
        self.qt_bloqueado_2.setFont(font)
        self.qt_bloqueado_2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.qt_bloqueado_2.setObjectName('qt_bloqueado_2')
        self.qt_vago_2 = QtWidgets.QLabel(parent=self.frame)
        self.qt_vago_2.setGeometry(QtCore.QRect(1000, 330, 61, 21))
        font = QtGui.QFont()
        self.qt_vago_2.setFont(font)
        self.qt_vago_2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.qt_vago_2.setObjectName('qt_vago_2')
        self.label_tabela_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_tabela_2.setGeometry(QtCore.QRect(880, 300, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_tabela_2.setFont(font)
        self.label_tabela_2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.label_tabela_2.setObjectName('label_tabela_2')
        self.label_bloq1_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_bloq1_2.setGeometry(QtCore.QRect(880, 390, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_bloq1_2.setFont(font)
        self.label_bloq1_2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.label_bloq1_2.setObjectName('label_bloq1_2')
        self.label_ocupado1_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_ocupado1_2.setGeometry(QtCore.QRect(880, 420, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_ocupado1_2.setFont(font)
        self.label_ocupado1_2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.label_ocupado1_2.setObjectName('label_ocupado1_2')
        self.label_vago1_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_vago1_2.setGeometry(QtCore.QRect(880, 330, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_vago1_2.setFont(font)
        self.label_vago1_2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.label_vago1_2.setObjectName('label_vago1_2')
        self.qt_reservado_2 = QtWidgets.QLabel(parent=self.frame)
        self.qt_reservado_2.setGeometry(QtCore.QRect(1000, 360, 61, 21))
        font = QtGui.QFont()
        self.qt_reservado_2.setFont(font)
        self.qt_reservado_2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.qt_reservado_2.setObjectName('qt_reservado_2')
        self.qt_ocupado_2 = QtWidgets.QLabel(parent=self.frame)
        self.qt_ocupado_2.setGeometry(QtCore.QRect(1000, 420, 61, 21))
        font = QtGui.QFont()
        self.qt_ocupado_2.setFont(font)
        self.qt_ocupado_2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.qt_ocupado_2.setObjectName('qt_ocupado_2')
        self.label_reser1_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_reser1_2.setGeometry(QtCore.QRect(880, 360, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_reser1_2.setFont(font)
        self.label_reser1_2.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.label_reser1_2.setObjectName('label_reser1_2')
        self.lisa = self.tela.retornar_frame()
        if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
            self.tela.monitora = False
            self.tela.abri_cti(Form, 'CTI PEDIÁTRICO - 06N')

        for row in range(self.tela.conta_linha()):
            leito = self.tela.leito(row)

            if 'aguardando' in leito.text():
                continue

            icon = QtGui.QIcon('emergencia.ico')
            pixmap = icon.pixmap(40, 40)

            if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
                label = QLabel(leito.text(), self.frame_2)
            else:
                label = QLabel(leito.text(), self.tela.frame_do_monitoramento)

            label.setGeometry(0, 0, 60, 30)

            filename = 'monitora_cti_ped.csv'
            if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
                filename = 'monitora_cti_pedpainel.csv'

            try:
                with open(filename, mode='r') as file:
                    reader = csv.reader(file)
                    data = list(reader)

                    for row in range(len(data)):
                        if data[row][0] == leito.text():
                            x = int(data[row][1])
                            y = int(data[row][2])
                            label.setGeometry(x, y, 60, 30)
                            break

                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    label.setCursor(Qt.CursorShape.OpenHandCursor)
                    label.mousePressEvent = lambda event, label=label: self.mousePressEvent(event, label)
                    label.mouseReleaseEvent = lambda event, label=label: self.mouseReleaseEvent(event, label)
                    label.mouseMoveEvent = lambda event, label=label: self.mouseMoveEvent(event, label)
                    label.setStyleSheet('background-color: rgb(170, 255, 255);')
                    self.lisa.append(label)

            except FileNotFoundError:
                print(1)

        else:
            self.atualizar_monitoramento(Form)
            self.conf_layout()

            if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
                self.tela.qt_int_ped = self.ocupado
                self.tela.qt_int_ped_total = self.total
                self.tela.qt_vagos_cti_ped = self.vago
                self.frame_2.move(150, 20)
                self.frame1.hide()
                self.frame2.hide()
                self.label_reservado2.hide()
                self.label_ocupado2.hide()
                self.label_bloqueado2.hide()
                self.legenda.hide()
                self.label_vago2.hide()
                self.label_tabela_2.hide()
                self.label_bloq1_2.hide()
                self.label_ocupado1_2.hide()
                self.label_vago1_2.hide()
                self.label_reser1_2.hide()
                self.qt_vago_2.hide()
                self.qt_reservado_2.hide()
                self.qt_bloqueado_2.hide()
                self.qt_ocupado_2.hide()
                self.cor_legenda_red.hide()
                self.cor_legenda_blue_2.hide()
                self.cor_legenda_yellow.hide()
                self.cor_b.hide()

                self.tela.total_bloq += self.bloqueado
                self.tela.total_vago += self.vago
                self.tela.total_rese += self.reservado
                self.tela.total_ocup += self.ocupado

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
                for label in self.lisa:
                    if label.text() == LEITOS:
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        tooltip_text = 'Leito Vago'
                        label.setToolTip(tooltip_text)
            if selecao.text() == 'OCUPADO':
                for label in self.lisa:
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
                for label in self.lisa:
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
                for label in self.lisa:
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
            if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
                if selecao.text() == 'BLOQUEADO POR FALTA DE FUNCIONÁRIOS':
                    self.bloqueado += 1
                    self.tela.qt_se_fun += 1
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
        if event.button() == Qt.MouseButton.LeftButton:
            label.setCursor(Qt.CursorShape.ClosedHandCursor)
        label.mouse_offset = event.pos()

    def mouseReleaseEvent(self, event, label):
        if event.button() == Qt.MouseButton.LeftButton:
            label.setCursor(Qt.CursorShape.OpenHandCursor)

    def mouseMoveEvent(self, event, label):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = label.mapToParent(event.pos() - label.mouse_offset)
            label.move(new_pos)
            x, y = (new_pos.x(), new_pos.y())
            if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
                frame = self.frame_2
            else:  # inserted
                frame = self.frame
            if frame:
                frame_rect = frame.rect()
                new_pos.setX(max(frame_rect.left(), min(new_pos.x(), frame_rect.right() - label.width())))
                new_pos.setY(max(frame_rect.top(), min(new_pos.y(), frame_rect.bottom() - label.height())))
                label.move(new_pos)
        filename = 'monitora_cti_ped.csv'
        if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
            filename = 'monitora_cti_pedpainel.csv'
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for lisa in self.lisa:
                texto = lisa.text()
                posicao = lisa.pos()
                writer.writerow([texto, posicao.x(), posicao.y()])

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label_6.setText(_translate('Form', '  POSTO'))
        self.label_29.setText(_translate('Form', '  POSTO'))
        self.label_reservado2.setText(_translate('Form', 'RESERVADO'))
        self.label_ocupado2.setText(_translate('Form', 'OCUPADO'))
        self.label_bloqueado2.setText(_translate('Form', 'BLOQUEADO'))
        self.legenda.setText(_translate('Form', 'LEGENDA :'))
        self.label_vago2.setText(_translate('Form', 'VAGO'))
        self.label_tabela_2.setText(_translate('Form', 'TABELA :'))
        self.label_bloq1_2.setText(_translate('Form', 'BLOQUEADO :'))
        self.label_ocupado1_2.setText(_translate('Form', 'OCUPADO :'))
        self.label_vago1_2.setText(_translate('Form', 'VAGO :'))
        self.label_reser1_2.setText(_translate('Form', 'RESERVADO :'))
        vago = str(self.vago)
        reservado = str(self.reservado)
        bloqueado = str(self.bloqueado)
        ocupado = str(self.ocupado)
        self.qt_vago_2.setText(_translate('Form', vago))
        self.qt_reservado_2.setText(_translate('Form', reservado))
        self.qt_bloqueado_2.setText(_translate('Form', bloqueado))
        self.qt_ocupado_2.setText(_translate('Form', ocupado))

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
            self.tela.frame_do_monitoramento.setStyleSheet('QFrame { background-color: transparent; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')