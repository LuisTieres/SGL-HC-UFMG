# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: procura_paciente.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSettings, QStandardPaths, Qt
import pymysql
import sys
import os

def resource_path(relative_path):
    """Resolve path para PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)# Verifica se o código foi "congelado" pelo PyInstaller

from database_Demandas import Ui_data_Demanda
class Ui_Form(object):

    def setupUi(self, Form, grade):

        self.data_deman = Ui_data_Demanda()
        self.grade = grade
        self.form = Form
        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setGeometry(QtCore.QRect(400, 65, 641, 511))
        self.frame.setStyleSheet('background-color: #5DADE2;')
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.frame.mousePressEvent = lambda event, frame=self.frame: self.mousePressEvent(event, frame)
        self.frame.mouseReleaseEvent = lambda event, frame=self.frame: self.mouseReleaseEvent(event, frame)
        self.frame.mouseMoveEvent = lambda event, frame=self.frame: self.mouseMoveEvent(event, frame)
        self.grade.janela_procura = self.frame
        self.PESQUISAR = QtWidgets.QLineEdit(parent=self.frame)
        self.PESQUISAR.setGeometry(QtCore.QRect(30, 60, 421, 31))
        self.Titulo = QtWidgets.QLabel('Procurar Paciente', parent=self.frame)
        self.Titulo.setGeometry(QtCore.QRect(90, 15, 330, 38))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.Titulo.setFont(font)
        icon = QIcon(resource_path('procurar/jogar.ico'))
        pixmap = icon.pixmap(50, 50)
        self.icone = QtWidgets.QLabel(parent=self.frame)
        self.icone.setPixmap(pixmap)
        self.icone.setGeometry(QtCore.QRect(3, 3, 50, 50))
        self.icone.show()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.PESQUISAR.setPlaceholderText('Pesquisar Paciente')
        self.PESQUISAR.setFont(font)
        self.PESQUISAR.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.PESQUISAR.setText('')
        self.PESQUISAR.setObjectName('PESQUISAR')
        self.tipo = 3
        self.btn_nome = QtWidgets.QPushButton('Pesquisr pelo Nome', parent=self.frame)
        self.btn_nome.setGeometry(QtCore.QRect(30, 95, 121, 31))
        self.btn_nome.setStyleSheet('QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')
        self.btn_nome.setObjectName('btn_nome')
        self.btn_nome.clicked.connect(lambda: self.set_tipo(3))
        self.btn_NPF = QtWidgets.QPushButton('Pesquisr pelo NPF', parent=self.frame)
        self.btn_NPF.setGeometry(QtCore.QRect(160, 95, 121, 31))
        self.btn_NPF.setStyleSheet('QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')
        self.btn_NPF.setObjectName('btn_NPF')
        self.btn_NPF.clicked.connect(lambda: self.set_tipo(2))
        self.btn_prontuario = QtWidgets.QPushButton('Pesquisr pelo Prontuário', parent=self.frame)
        self.btn_prontuario.setGeometry(QtCore.QRect(290, 95, 151, 31))
        self.btn_prontuario.setStyleSheet('QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')
        self.btn_prontuario.setObjectName('btn_prontuario')
        self.btn_prontuario.clicked.connect(lambda: self.set_tipo(1))
        icon = QIcon(resource_path('procurar/lupa.ico'))
        self.PESQUISAR.addAction(icon, QtWidgets.QLineEdit.ActionPosition.LeadingPosition)
        self.label_QT = QtWidgets.QLabel(parent=self.frame)
        self.label_QT.setGeometry(QtCore.QRect(30, 110, 231, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_QT.setFont(font)
        self.label_QT.setObjectName('label_QT')
        self.frame_2 = QtWidgets.QFrame(parent=self.frame)
        self.frame_2.setGeometry(QtCore.QRect(30, 140, 590, 320))
        self.frame_2.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName('frame_2')
        self.commandLinkButton = QtWidgets.QCommandLinkButton(parent=self.frame)
        self.commandLinkButton.setGeometry(QtCore.QRect(460, 470, 161, 31))
        self.commandLinkButton.setStyleSheet('QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')
        font = QtGui.QFont()
        font.setPointSize(8)
        self.commandLinkButton.setFont(font)
        self.commandLinkButton.setObjectName('commandLinkButton')
        icon = QIcon(resource_path('imagens/jogar.ico'))
        self.BTNseta = QtWidgets.QPushButton(parent=self.frame_2)
        self.BTNseta.setStyleSheet('\n                                                    QPushButton {\n                                                        border: none;\n                                                        background-color: transparent;\n                                                        color: #2E3D48;\n                                                    }\n                                                    QPushButton:pressed {\n                                                        background-color: #5DADE2;\n                                                        color: #FFFFFF;\n                                                    }\n                                                ')
        self.BTNseta.setIcon(icon)
        inverted_icon = QtGui.QIcon(icon)
        inverted_icon.addPixmap(icon.pixmap(48, 48).transformed(QtGui.QTransform().scale(-1, 1)))
        self.BTNseta2 = QtWidgets.QPushButton('', self.frame_2)
        self.BTNseta2.setIcon(inverted_icon)
        self.BTNseta2.setContentsMargins(0, 0, 0, 0)
        self.BTNseta2.setStyleSheet('\n                                QPushButton {\n                                    border: none;\n                                    background-color: transparent;\n                                    color: #2E3D48;\n                                }\n                                QPushButton:pressed {\n                                    background-color: #5DADE2;\n                                    color: #FFFFFF;\n                                }\n                            ')
        self.BTNseta.move(560, 0)
        self.BTNseta2.move(540, 0)
        self.nome = QtWidgets.QLabel('Nome: ', parent=self.frame_2)
        self.nome.setGeometry(QtCore.QRect(0, 15, 200, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.nome.setFont(font)
        self.nome.hide()
        self.leito = QtWidgets.QLabel(parent=self.frame_2)
        self.leito.setGeometry(QtCore.QRect(0, 175, 200, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.leito.setFont(font)
        self.leito.hide()
        self.prontuario = QtWidgets.QLabel(parent=self.frame_2)
        self.prontuario.setGeometry(QtCore.QRect(0, 95, 200, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.prontuario.setFont(font)
        self.prontuario.hide()
        self.NPF = QtWidgets.QLabel(parent=self.frame_2)
        self.NPF.setGeometry(QtCore.QRect(0, 135, 200, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.NPF.setFont(font)
        self.NPF.hide()
        self.ala = QtWidgets.QLabel('Ala: ', parent=self.frame_2)
        self.ala.setGeometry(QtCore.QRect(0, 55, 400, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ala.setFont(font)
        self.ala.hide()
        if self.grade.t == 'Demanda':
            self.commandLinkButton.clicked.connect(lambda: self.localizar_de(Form))
            self.BTNseta.clicked.connect(self.proximo_de)
            self.BTNseta2.clicked.connect(self.anterior_de)
        else:
            self.commandLinkButton.clicked.connect(lambda: self.localizar(Form))
            self.BTNseta.clicked.connect(self.proximo)
            self.BTNseta2.clicked.connect(self.anterior)
        self.retranslateUi(Form)
        for widget in self.frame.findChildren(QtWidgets.QWidget):
            widget.show()
        self.frame.show()
        self.load(Form)
        self.commandLinkButton.hide()
        self.BTNseta.hide()
        self.BTNseta2.hide()
        self.label_QT.hide()
        self.PESQUISAR.textChanged.connect(self.ocultar_user_label)

    def ocultar_user_label(self):
        self.label_QT.hide()
        self.btn_prontuario.show()
        self.btn_nome.show()
        self.btn_NPF.show()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.commandLinkButton.setText(_translate('Form', 'ECONTRAR PACIENTE'))

    def set_tipo(self, value):
        self.tipo = value
        if self.grade.t == 'Demanda':
            self.pesquisa_de()
        else:
            self.pesquisa()

    def pesquisa(self):
        grade = self.grade.ala
        Form = self.form
        list = [self.grade.abri_cti_ped, self.grade.abrir_UCO, self.grade.abrir_CTI_PS, self.grade.abrir_CTI_3_leste, self.grade.abrir_6_leste, self.grade.abrir_10_norte, self.grade.abrir_2_leste, self.grade.abrir_2_sul, self.grade.abrir_7_leste, self.grade.abrir_7_norte, self.grade.abrir_8_sul, self.grade.abrir_8_leste, self.grade.abrir_8_norte, self.grade.abrir_9_leste]
        self.quantidade_pacientes = 0
        self.leituras = []
        self.pacientes = []
        self.lugar = []
        for funcao in list:
            self.colum_nome = 0
            self.colum_prontuario = 0
            self.colum_npf = 0
            self.grade.procurar_Aberta = False
            funcao(Form)
            self.grade.procurar_Aberta = True
            for colum in range(self.grade.tabela_grade.columnCount()):
                item_pac = self.grade.tabela_grade.horizontalHeaderItem(colum)
                if item_pac.text() == 'NOME DO PACIENTE':
                    self.colum_nome = colum
                elif item_pac.text() == 'PRONTUÁRIO':
                    self.colum_prontuario = colum
                elif item_pac.text() == 'NPF':
                    self.colum_npf = colum
            if self.tipo == 3:
                for row in range(self.grade.conta_linha()):
                    item = self.grade.tabela_grade.item(row, self.colum_nome)
                    if item is not None and item.text() == self.PESQUISAR.text():
                        self.quantidade_pacientes += 1
                        nome_paciente = item.text()
                        label_titulo = self.grade.TITULO_CTI.text()
                        prontuario = self.grade.tabela_grade.item(row, self.colum_prontuario).text()
                        npf = self.grade.tabela_grade.item(row, self.colum_npf).text()
                        leito = self.grade.tabela_grade.verticalHeaderItem(row).text()
                        self.pacientes.append((nome_paciente, label_titulo, prontuario, npf, leito))
            if self.tipo == 1:
                for row in range(self.grade.conta_linha()):
                    item = self.grade.tabela_grade.item(row, self.colum_prontuario)
                    if item is not None and item.text() == self.PESQUISAR.text():
                        self.quantidade_pacientes += 1
                        nome_paciente = self.grade.tabela_grade.item(row, self.colum_nome).text()
                        label_titulo = self.grade.TITULO_CTI.text()
                        prontuario = self.grade.tabela_grade.item(row, self.colum_prontuario).text()
                        npf = self.grade.tabela_grade.item(row, self.colum_npf).text()
                        leito = self.grade.tabela_grade.verticalHeaderItem(row).text()
                        self.pacientes.append((nome_paciente, label_titulo, prontuario, npf, leito))
            if self.tipo == 2:
                for row in range(self.grade.conta_linha()):
                    item = self.grade.tabela_grade.item(row, self.colum_npf)
                    if item is not None and item.text() == self.PESQUISAR.text():
                        self.quantidade_pacientes += 1
                        nome_paciente = self.grade.tabela_grade.item(row, self.colum_nome).text()
                        label_titulo = self.grade.TITULO_CTI.text()
                        prontuario = self.grade.tabela_grade.item(row, self.colum_prontuario).text()
                        npf = self.grade.tabela_grade.item(row, self.colum_npf).text()
                        leito = self.grade.tabela_grade.verticalHeaderItem(row).text()
                        self.pacientes.append((nome_paciente, label_titulo, prontuario, npf, leito))
        if grade == 'cti ped':
            self.grade.abri_cti_ped(Form)
        if grade == 'UCO':
            self.grade.abrir_UCO(Form)
        if grade == '6 leste':
            self.grade.abrir_6_leste(Form)
        if grade == '10 norte':
            self.grade.abrir_10_norte(Form)
        if grade == 'CTI PS':
            self.grade.abrir_CTI_PS(Form)
        if grade == '2 leste':
            self.grade.abrir_2_leste(Form)
        if grade == '2 sul':
            self.grade.abrir_2_sul(Form)
        if grade == '7 leste':
            self.grade.abrir_7_leste(Form)
        if grade == '7 norte':
            self.grade.abrir_7_norte(Form)
        if grade == '8 sul':
            self.grade.abrir_8_sul(Form)
        if grade == '8 leste':
            self.grade.abrir_8_leste(Form)
        if grade == '8 norte':
            self.grade.abrir_8_norte(Form)
        if grade == '9 leste':
            self.grade.abrir_9_leste(Form)
        if grade == '3 leste':
            self.grade.abrir_CTI_3_leste(Form)
        self.label_QT.setText(str(self.quantidade_pacientes) + ' PACIENTES ENCONTRADOS')
        self.label_QT.show()
        self.btn_prontuario.hide()
        self.btn_nome.hide()
        self.btn_NPF.hide()
        if self.quantidade_pacientes != 0:
            self.nome.show()
            self.ala.show()
            self.leito.show()
            self.prontuario.show()
            self.NPF.show()
            self.BTNseta2.show()
            self.BTNseta.show()
            self.commandLinkButton.show()
            if self.pacientes:
                self.contador_linha = 0
                self.proximo()
        else:
            self.BTNseta.hide()
            self.BTNseta2.hide()

    def proximo(self):
        print(self.quantidade_pacientes)
        for index, paciente in enumerate(self.pacientes):
            if self.contador_linha == index:
                self.primeiro_paciente = paciente
                nome = self.primeiro_paciente[0]
                Prontuario = self.primeiro_paciente[2]
                self.setor = self.primeiro_paciente[1]
                npf = self.primeiro_paciente[3]
                ala = self.primeiro_paciente[1]
                leito = self.primeiro_paciente[4]
                print(nome, 'rata')
                self.nome.setText('Nome: ' + nome)
                self.prontuario.setText('Prontuário: ' + Prontuario)
                self.NPF.setText('NPF: ' + npf)
                self.leito.setText('Leito: ' + leito)
                self.ala.setText('Ala: ' + ala)
                self.npf_usu = npf
                self.pronto = Prontuario
                self.name = nome
        if self.contador_linha < index:
            self.contador_linha += 1

    def anterior(self):
        for index, paciente in enumerate(self.pacientes):
            if self.contador_linha == index and self.contador_linha > 0:
                self.primeiro_paciente = paciente
                nome = self.primeiro_paciente[0]
                Prontuario = self.primeiro_paciente[2]
                self.setor = self.primeiro_paciente[1]
                npf = self.primeiro_paciente[3]
                ala = self.primeiro_paciente[1]
                leito = self.primeiro_paciente[4]
                self.nome.setText('Nome: ' + nome)
                self.prontuario.setText('Prontuário: ' + Prontuario)
                self.NPF.setText('NPF: ' + npf)
                self.leito.setText('Leito: ' + leito)
                self.ala.setText('Ala: ' + ala)
                self.npf_usu = npf
                self.pronto = Prontuario
                self.name = nome
        if self.contador_linha > 0:
            self.contador_linha -= 1

    def localizar(self, Form):
        if self.setor == 'CTI PEDIÁTRICO':
            self.grade.abri_cti_ped()
        if self.setor == '6° LESTE':
            self.grade.abrir_6_leste()
        if self.setor == '10° NORTE':
            self.grade.abrir_10_norte()
        if self.setor == 'CTI PS':
            self.grade.abrir_CTI_PS()
        if self.setor == '2° LESTE':
            self.grade.abrir_2_leste()
        if self.setor == '2° SUL':
            self.grade.abrir_2_sul()
        if self.setor == '7° LESTE':
            self.grade.abrir_7_lestee()
        if self.setor == '7° NORTE':
            self.grade.abrir_7_norte()
        if self.setor == '8° SUL':
            self.grade.abrir_8_sul()
        if self.setor == '8° LESTE':
            self.grade.abrir_8_leste()
        if self.setor == '8° NORTE':
            self.grade.abrir_8_norte()
        if self.setor == '9° LESTE':
            self.grade.abrir_9_leste()
        if self.tipo == 3:
            self.grade.selecionar(self.name, self.tipo)
        if self.tipo == 2:
            self.grade.selecionar(self.npf_usu, self.tipo)
        if self.tipo == 1:
            self.grade.selecionar(self.pronto, self.tipo)
        self.frame.close()

    def pesquisa_de(self):
        MainWindow = self.form
        variavel = self.grade.variavel
        self.quantidade_pacientes = 0
        self.leituras = []
        self.pacientes = []
        self.lugar = []
        lista_de_Resultados = []

        if self.tipo == 3:
            lista_de_Resultados = self.data_deman.procurar_paciente_mysql(self.grade, 'NOME_DO_PACIENTE',self.PESQUISAR.text(), lista_de_Resultados)
            if lista_de_Resultados != False:
                for resultados, label_titulo,id in lista_de_Resultados:
                    for dado in resultados:
                        self.pacientes.append((dado[0], label_titulo, dado[1], dado[2],id))
                        self.quantidade_pacientes += 1
        if self.tipo == 1:
            lista_de_Resultados = self.data_deman.procurar_paciente_mysql(self.grade, 'PRONTUARIO', self.PESQUISAR.text(), lista_de_Resultados)
            if lista_de_Resultados != False:
                for resultados, label_titulo,id in lista_de_Resultados:
                    for dado in resultados:
                        self.pacientes.append((dado[0], label_titulo, dado[1], dado[2],id))
                        self.quantidade_pacientes += 1
        if self.tipo == 2:
            lista_de_Resultados = self.data_deman.procurar_paciente_mysql(self.grade, 'NPF', self.PESQUISAR.text(), lista_de_Resultados)
            if lista_de_Resultados != False:
                for resultados, label_titulo,id in lista_de_Resultados:
                    for dado in resultados:
                        self.pacientes.append((dado[0], label_titulo, dado[1], dado[2],id))
                        self.quantidade_pacientes += 1
        self.label_QT.setText(str(self.quantidade_pacientes) + ' PACIENTES ENCONTRADOS')
        self.label_QT.show()
        self.btn_prontuario.hide()
        self.btn_nome.hide()
        self.btn_NPF.hide()
        if self.quantidade_pacientes > 1:
            self.nome.show()
            self.ala.show()
            self.leito.show()
            self.prontuario.show()
            self.NPF.show()
            self.BTNseta2.show()
            self.BTNseta.show()
            self.commandLinkButton.show()
            if self.pacientes:
                self.contador_linha = 0
                self.proximo_de()

    def localizar_de(self, Form):
        MainWindow = self.form
        btn = self.grade.lista_dos_btn[0]
        for col ,setor in enumerate(self.grade.lista_ids):
            if self.setor == setor:
                btn = self.grade.lista_dos_btn[col]
        ala = self.ala.text().replace('Demanda : ', '')
        self.grade.abrir_tabela(self.grade.mainwindow,self.setor, ala, btn)
        if self.tipo == 3:
            self.grade.selecionar(self.name, self.tipo)
        if self.tipo == 2:
            self.grade.selecionar(self.npf_usu, self.tipo)
        if self.tipo == 1:
            self.grade.selecionar(self.pronto, self.tipo)
        self.frame.close()

    def proximo_de(self):
        for index, paciente in enumerate(self.pacientes):
            if self.contador_linha == index:
                self.primeiro_paciente = paciente
                nome = self.primeiro_paciente[0]
                Prontuario = str(self.primeiro_paciente[2])
                self.setor = self.primeiro_paciente[4]
                npf = str(self.primeiro_paciente[3])
                ala = self.primeiro_paciente[1]
                self.nome.setText('Nome: ' + nome)
                self.prontuario.setText('Prontuário: ' + Prontuario)
                self.NPF.setText('NPF: ' + npf)
                self.ala.setText('Demanda : ' + ala)
                self.name = nome
                self.pronto = Prontuario
                self.npf_usu = npf
        if self.contador_linha < index:
            self.contador_linha += 1

    def anterior_de(self):
        for index, paciente in enumerate(self.pacientes):
            if self.contador_linha == index and self.contador_linha > 0:
                self.primeiro_paciente = paciente
                nome = self.primeiro_paciente[0]
                Prontuario = str(self.primeiro_paciente[2])
                self.setor = self.primeiro_paciente[4]
                npf = str(self.primeiro_paciente[3])
                ala = self.primeiro_paciente[1]
                self.nome.setText('Nome: ' + nome)
                self.prontuario.setText('Prontuário: ' + Prontuario)
                self.NPF.setText('NPF: ' + npf)
                self.ala.setText('Demanda : ' + ala)
                self.name = nome
                self.pronto = Prontuario
                self.npf_usu = npf
        if self.contador_linha > 0:
            self.contador_linha -= 1

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        print('Tecla pressionada:', event.key())

    def load(self, Form):
        if self.settings.contains('tema'):
            font_name = self.settings.value('font', defaultValue='')
            backcolocor = self.settings.value('tema', defaultValue='')
            color = self.settings.value('color', defaultValue='')
            tamanho = int(self.settings.value('tamanho', defaultValue=10))
            self.backcolocor = backcolocor
            self.color = color
            self.frame.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;border: 2px solid #2E3D48;border-radius: 10px;')
            for label in self.frame.findChildren(QtWidgets.QLabel):
                label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name}; border:none')
            self.Titulo.setStyleSheet(f'color: {color}; font:  30 px {font_name}; border:none;')

    def mousePressEvent(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            # centralwidget.setCursor(Qt.CursorShape.ClosedHandCursor)  # Removido
            centralwidget.mouse_offset = event.pos()

    def mouseReleaseEvent(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            # centralwidget.setCursor(Qt.CursorShape.OpenHandCursor)  # Removido
            centralwidget.setCursor(Qt.CursorShape.ArrowCursor)  # Garante que volta para a seta

    def mouseMoveEvent(self, event, centralwidget):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = centralwidget.mapToParent(event.pos() - centralwidget.mouse_offset)
            centralwidget.move(new_pos)