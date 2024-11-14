# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: cti_ps_monitoramento.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import csv
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QRect, Qt, QSettings, QStandardPaths, Qt
from PyQt6.QtWidgets import QLabel

class Ui_Form(object):
    def setupUi(self, Form, frame, tela):
        self.tela = tela
        self.frame = frame
        self.settings = QSettings('HC', 'SGL')
        self.form = Form
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        self.frame_3 = QtWidgets.QFrame(parent=self.frame)
        self.frame_3.setGeometry(QtCore.QRect(384, 102, 446, 121))
        self.frame_3.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName('frame_3')
        self.posto = QtWidgets.QLabel(parent=self.frame_3)
        self.posto.setGeometry(QtCore.QRect(117, 90, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.posto.setFont(font)
        self.posto.setStyleSheet('background-color: rgb(0, 0, 0);\nbackground-color: rgb(127, 127, 127);')
        self.posto.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.posto.setObjectName('posto')
        self.line = QtWidgets.QFrame(parent=self.frame_3)
        self.line.setGeometry(QtCore.QRect(60, 0, 4, 120))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName('line')
        self.line_2 = QtWidgets.QFrame(parent=self.frame_3)
        self.line_2.setGeometry(QtCore.QRect(0, 35, 451, 4))
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName('line_2')
        self.line_3 = QtWidgets.QFrame(parent=self.frame_3)
        self.line_3.setGeometry(QtCore.QRect(0, 80, 451, 4))
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName('line_3')
        self.line_4 = QtWidgets.QFrame(parent=self.frame_3)
        self.line_4.setGeometry(QtCore.QRect(290, 0, 4, 121))
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_4.setObjectName('line_4')
        self.line_5 = QtWidgets.QFrame(parent=self.frame_3)
        self.line_5.setGeometry(QtCore.QRect(370, 0, 4, 121))
        self.line_5.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_5.setObjectName('line_5')
        self.line_7 = QtWidgets.QFrame(parent=self.frame_3)
        self.line_7.setGeometry(QtCore.QRect(130, 0, 4, 90))
        self.line_7.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_7.setObjectName('line_7')
        self.line_8 = QtWidgets.QFrame(parent=self.frame_3)
        self.line_8.setGeometry(QtCore.QRect(220, 0, 4, 90))
        self.line_8.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_8.setObjectName('line_8')
        self.titulo = QtWidgets.QLabel(parent=self.frame)
        self.titulo.setGeometry(QtCore.QRect(500, 40, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.titulo.setFont(font)
        self.titulo.setObjectName('titulo')
        self.titulo.setStyleSheet('border:none;')
        if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
            self.corredor1 = QtWidgets.QLabel(parent=self.frame)
            corredor1 = QtWidgets.QLabel(parent=self.frame_3)
            corredor1.setGeometry(QtCore.QRect(65, 91, 51, 81))
            corredor1.setStyleSheet('background-color: rgb(223, 223, 223);border: none;')
            corredor1.setText('')
        else:  # inserted
            self.corredor1 = QtWidgets.QLabel(parent=self.frame)
            self.corredor1.setGeometry(QtCore.QRect(450, 192, 51, 81))
        self.corredor1.setStyleSheet('background-color: rgb(223, 223, 223);border: none;')
        self.corredor1.setText('')
        self.corredor1.setObjectName('corredor1')
        if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
            self.corredor2 = QtWidgets.QLabel(parent=self.frame)
        else:  # inserted
            self.corredor2 = QtWidgets.QLabel(parent=self.frame)
            self.corredor2.setGeometry(QtCore.QRect(380, 226, 70, 47))
        self.corredor2.setStyleSheet('background-color: rgb(223, 223, 223);border: none;')
        self.corredor2.setText('')
        self.corredor2.setObjectName('corredor2')
        self.frame1 = QtWidgets.QLabel(parent=self.frame)
        self.frame1.setGeometry(QtCore.QRect(253, 283, 147, 157))
        self.frame1.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.frame1.setText('')
        self.frame1.setObjectName('frame1')
        self.cor_b = QtWidgets.QLabel(parent=self.frame)
        self.cor_b.setGeometry(QtCore.QRect(260, 380, 21, 21))
        self.cor_b.setStyleSheet('background-color: rgb(170, 170, 255);')
        self.cor_b.setText('')
        self.cor_b.setObjectName('cor_b')
        self.legenda = QtWidgets.QLabel(parent=self.frame)
        self.legenda.setGeometry(QtCore.QRect(260, 290, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.legenda.setFont(font)
        self.legenda.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.legenda.setObjectName('legenda')
        self.label_bloqueado2 = QtWidgets.QLabel(parent=self.frame)
        self.label_bloqueado2.setGeometry(QtCore.QRect(290, 380, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_bloqueado2.setFont(font)
        self.label_bloqueado2.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.label_bloqueado2.setObjectName('label_bloqueado2')
        self.label_ocupado2 = QtWidgets.QLabel(parent=self.frame)
        self.label_ocupado2.setGeometry(QtCore.QRect(290, 410, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_ocupado2.setFont(font)
        self.label_ocupado2.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.label_ocupado2.setObjectName('label_ocupado2')
        self.label_reservado2 = QtWidgets.QLabel(parent=self.frame)
        self.label_reservado2.setGeometry(QtCore.QRect(290, 350, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_reservado2.setFont(font)
        self.label_reservado2.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.label_reservado2.setObjectName('label_reservado2')
        self.label_vago2 = QtWidgets.QLabel(parent=self.frame)
        self.label_vago2.setGeometry(QtCore.QRect(290, 320, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_vago2.setFont(font)
        self.label_vago2.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.label_vago2.setObjectName('label_vago2')
        self.cor_legenda_red = QtWidgets.QLabel(parent=self.frame)
        self.cor_legenda_red.setGeometry(QtCore.QRect(260, 410, 21, 21))
        self.cor_legenda_red.setStyleSheet('background-color: rgb(255, 0, 0);')
        self.cor_legenda_red.setText('')
        self.cor_legenda_red.setObjectName('cor_legenda_red')
        self.cor_legenda_blue = QtWidgets.QLabel(parent=self.frame)
        self.cor_legenda_blue.setGeometry(QtCore.QRect(260, 320, 21, 21))
        self.cor_legenda_blue.setStyleSheet('background-color: rgb(170, 255, 255);\nborder-left-color: rgb(0, 0, 0);\nborder-bottom-color: rgb(0, 0, 0);\nborder-right-color: rgb(0, 0, 0);\nborder-right-color: rgb(0, 0, 0);\nborder-top-color: rgb(0, 0, 0);\nborder-color: rgb(0, 0, 0);')
        self.cor_legenda_blue.setText('')
        self.cor_legenda_blue.setObjectName('cor_legenda_blue')
        self.cor_legenda_yellow = QtWidgets.QLabel(parent=self.frame)
        self.cor_legenda_yellow.setGeometry(QtCore.QRect(260, 350, 21, 21))
        self.cor_legenda_yellow.setStyleSheet('background-color: rgb(255, 255, 0);')
        self.cor_legenda_yellow.setText('')
        self.cor_legenda_yellow.setObjectName('cor_legenda_yellow')
        self.frame2 = QtWidgets.QLabel(parent=self.frame)
        self.frame2.setGeometry(QtCore.QRect(483, 283, 195, 157))
        self.frame2.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.frame2.setText('')
        self.frame2.setObjectName('frame2')
        self.label_tabela = QtWidgets.QLabel(parent=self.frame)
        self.label_tabela.setGeometry(QtCore.QRect(490, 290, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_tabela.setFont(font)
        self.label_tabela.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.label_tabela.setObjectName('label_tabela')
        self.label_ocupado1 = QtWidgets.QLabel(parent=self.frame)
        self.label_ocupado1.setGeometry(QtCore.QRect(490, 410, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_ocupado1.setFont(font)
        self.label_ocupado1.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.label_ocupado1.setObjectName('label_ocupado1')
        self.label_vago1 = QtWidgets.QLabel(parent=self.frame)
        self.label_vago1.setGeometry(QtCore.QRect(490, 320, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_vago1.setFont(font)
        self.label_vago1.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.label_vago1.setObjectName('label_vago1')
        self.label_reser1 = QtWidgets.QLabel(parent=self.frame)
        self.label_reser1.setGeometry(QtCore.QRect(490, 350, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_reser1.setFont(font)
        self.label_reser1.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.label_reser1.setObjectName('label_reser1')
        self.label_bloq1 = QtWidgets.QLabel(parent=self.frame)
        self.label_bloq1.setGeometry(QtCore.QRect(490, 380, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_bloq1.setFont(font)
        self.label_bloq1.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.label_bloq1.setObjectName('label_bloq1')
        self.qt_vago = QtWidgets.QLabel(parent=self.frame)
        self.qt_vago.setGeometry(QtCore.QRect(610, 320, 61, 21))
        font = QtGui.QFont()
        self.qt_vago.setFont(font)
        self.qt_vago.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.qt_vago.setObjectName('qt_vago')
        self.qt_reservado = QtWidgets.QLabel(parent=self.frame)
        self.qt_reservado.setGeometry(QtCore.QRect(610, 350, 61, 21))
        font = QtGui.QFont()
        self.qt_reservado.setFont(font)
        self.qt_reservado.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.qt_reservado.setObjectName('qt_reservado')
        self.qt_bloqueado = QtWidgets.QLabel(parent=self.frame)
        self.qt_bloqueado.setGeometry(QtCore.QRect(610, 380, 61, 21))
        font = QtGui.QFont()
        self.qt_bloqueado.setFont(font)
        self.qt_bloqueado.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.qt_bloqueado.setObjectName('qt_bloqueado')
        self.qt_ocupado = QtWidgets.QLabel(parent=self.frame)
        self.qt_ocupado.setGeometry(QtCore.QRect(610, 410, 61, 21))
        font = QtGui.QFont()
        self.qt_ocupado.setFont(font)
        self.qt_ocupado.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.qt_ocupado.setObjectName('qt_ocupado')
        self.labels = []
        if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
            self.tela.monitora = False
            self.tela.abri_cti(Form, 'UTI - PRONTO SOCORRO')

        for row in range(self.tela.conta_linha()):
            leito = self.tela.leito(row)
            icon = QtGui.QIcon(
                'C:\\Users\\luist\\OneDrive\\Área de Trabalho\\Ti\\Nova pasta\\HC-UFMG\\SGL\\emergencia.ico')
            pixmap = icon.pixmap(40, 40)

            if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
                label = QLabel(leito.text(), self.frame)
            else:
                label = QLabel(leito.text(), self.tela.frame_do_monitoramento)

            label.setGeometry(0, 0, 60, 30)
            filename = 'monitora_cti_ps.csv'
            if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
                filename = 'monitora_cti_pspainel.csv'

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
                    label.mouseMoveEvent = lambda event, label=label: self.mouseMoveEvent(event, label)
                    label.setStyleSheet('background-color: rgb(170, 255, 255);')
                    self.labels.append(label)

            except FileNotFoundError:
                print("Arquivo não encontrado")

        else:
            self.atualizar_monitoramento(Form)
            self.conf_layout()
            if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
                self.frame_3.move(300, 200)
                self.corredor1.move(800, 322)
                self.corredor2.move(746, 322)
                self.titulo.hide()
                self.frame1.hide()
                self.frame2.hide()
                self.legenda.hide()
                self.label_bloqueado2.hide()
                self.label_ocupado2.hide()
                self.label_reservado2.hide()
                self.label_vago2.hide()
                self.label_tabela.hide()
                self.label_ocupado1.hide()
                self.label_vago1.hide()
                self.label_reser1.hide()
                self.label_bloq1.hide()
                self.qt_vago.hide()
                self.qt_reservado.hide()
                self.qt_bloqueado.hide()
                self.qt_ocupado.hide()
                self.cor_legenda_red.hide()
                self.cor_legenda_blue.hide()
                self.cor_legenda_yellow.hide()
                self.cor_b.hide()
                self.tela.qt_vagos_uti_ps = self.vago
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
            if paciente is not None:
                paciente = self.tela.item(row, 3).text()
            if selecao is not None and selecao.text() == 'VAGO':
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
            frame = self.frame
            if frame:
                frame_rect = frame.rect()
                new_pos.setX(max(frame_rect.left(), min(new_pos.x(), frame_rect.right() - label.width())))
                new_pos.setY(max(frame_rect.top(), min(new_pos.y(), frame_rect.bottom() - label.height())))
                label.move(new_pos)
        filename = 'monitora_cti_ps.csv'
        if self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True:
            filename = 'monitora_cti_pspainel.csv'
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for lisa in self.labels:
                texto = lisa.text()
                posicao = lisa.pos()
                writer.writerow([texto, posicao.x(), posicao.y()])

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.posto.setText(_translate('Form', 'POSTO'))
        self.titulo.setText(_translate('Form', 'CTI PS'))
        self.legenda.setText(_translate('Form', 'LEGENDA :'))
        self.label_bloqueado2.setText(_translate('Form', 'BLOQUEADO'))
        self.label_ocupado2.setText(_translate('Form', 'OCUPADO'))
        self.label_reservado2.setText(_translate('Form', 'RESERVADO'))
        self.label_vago2.setText(_translate('Form', 'VAGO'))
        self.label_tabela.setText(_translate('Form', 'TABELA :'))
        self.label_ocupado1.setText(_translate('Form', 'OCUPADO :'))
        self.label_vago1.setText(_translate('Form', 'VAGO :'))
        self.label_reser1.setText(_translate('Form', 'RESERVADO :'))
        self.label_bloq1.setText(_translate('Form', 'BLOQUEADO :'))
        vago = str(self.vago)
        reservado = str(self.reservado)
        bloqueado = str(self.bloqueado)
        ocupado = str(self.ocupado)
        self.qt_vago.setText(_translate('Form', vago))
        self.qt_reservado.setText(_translate('Form', reservado))
        self.qt_bloqueado.setText(_translate('Form', bloqueado))
        self.qt_ocupado.setText(_translate('Form', ocupado))

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
            if (not self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True) and (not self.tela.scroll_painel.isVisible() or self.tela.help_sccrol_painel == True):
                self.tela.frame_do_monitoramento.setStyleSheet('QFrame { background-color: transparent; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')