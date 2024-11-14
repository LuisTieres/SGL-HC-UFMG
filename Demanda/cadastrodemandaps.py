# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: Demanda\cadastrodemandaps.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import mysql.connector
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QCompleter
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QDateTime, QSettings, QStandardPaths
import psycopg2
from PyQt6.QtWidgets import QMessageBox, QCompleter
from datetime import datetime

class Ui_Cadastro(QtWidgets.QMainWindow):
    def setupUi(self, Cadastro, para_teladem=None):
        self.teladem = para_teladem
        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        self.centralwidget = QtWidgets.QFrame(parent=Cadastro)
        self.centralwidget.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.centralwidget.setGeometry(QtCore.QRect(450, 50, 505, 610))
        self.centralwidget.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.centralwidget.setObjectName('frame')
        self.teladem.janela_cadastro = self.centralwidget
        self.centralwidget.setCursor(Qt.CursorShape.OpenHandCursor)
        self.centralwidget.mousePressEvent = lambda event, centralwidget=self.centralwidget: self.mousePressEvent(event, centralwidget)
        self.centralwidget.mouseReleaseEvent = lambda event, centralwidget=self.centralwidget: self.mouseReleaseEvent(event, centralwidget)
        self.centralwidget.mouseMoveEvent = lambda event, centralwidget=self.centralwidget: self.mouseMoveEvent(event, centralwidget)
        icon = QIcon('register.png')
        pixmap = icon.pixmap(50, 50)
        self.icone = QtWidgets.QLabel(parent=self.centralwidget)
        self.icone.setPixmap(pixmap)
        self.icone.setGeometry(QtCore.QRect(3, 3, 50, 50))
        self.Titulo = QtWidgets.QLabel(parent=self.centralwidget)
        self.Titulo.setGeometry(QtCore.QRect(90, 15, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Titulo.setFont(font)
        colo = 'border: 2px solid #2E3D48; border-radius: 10px; background-color: white;'
        self.Titulo.setObjectName('Titulo')
        self.prontuario_edit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.prontuario_edit.setGeometry(QtCore.QRect(10, 70, 231, 21))
        self.prontuario_edit.setObjectName('prontuario_edit')
        self.prontuario_edit.setStyleSheet(colo)
        self.prontuario_edit.textChanged.connect(self.procurar_paciente)
        self.npf_edit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.npf_edit.setGeometry(QtCore.QRect(260, 70, 231, 21))
        self.npf_edit.setObjectName('npf_edit')
        self.npf_edit.setStyleSheet(colo)
        self.npf_edit.textChanged.connect(self.procurar_paciente)
        self.Nomepascedit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Nomepascedit.setGeometry(QtCore.QRect(260, 120, 231, 21))
        self.Nomepascedit.setObjectName('Nomepascedit')
        self.Nomepascedit.setStyleSheet(colo)
        self.Nomepasc = QtWidgets.QLabel(parent=self.centralwidget)
        self.Nomepasc.setGeometry(QtCore.QRect(260, 100, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Nomepasc.setFont(font)
        self.Nomepasc.setObjectName('Nomepasc')
        self.prontuario = QtWidgets.QLabel(parent=self.centralwidget)
        self.prontuario.setGeometry(QtCore.QRect(10, 50, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.prontuario.setFont(font)
        self.prontuario.setObjectName('prontuario')
        self.npf_label = QtWidgets.QLabel('NPF', parent=self.centralwidget)
        self.npf_label.setGeometry(QtCore.QRect(260, 50, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.npf_label.setFont(font)
        self.npf_label.setObjectName('prontuario')
        self.datanas = QtWidgets.QDateEdit(parent=self.centralwidget)
        self.datanas.setGeometry(QtCore.QRect(10, 120, 91, 21))
        ccurrent_datetime = QtCore.QDateTime.currentDateTime()
        tomorrow_datetime = ccurrent_datetime.addDays(30000)
        initial_datetime = tomorrow_datetime
        self.dataalt = QtWidgets.QDateEdit()
        self.dataalt.setDateTime(initial_datetime)
        self.datanas.setDateTime(initial_datetime)
        self.datanas.setCalendarPopup(True)
        self.datanas.setObjectName('datanas')
        self.datanas.setStyleSheet('border: none;')
        self.Datanasclabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.Datanasclabel.setGeometry(QtCore.QRect(10, 100, 181, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Datanasclabel.setFont(font)
        self.Datanasclabel.setObjectName('Datanasclabel')
        self.Pontoscorelabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.Pontoscorelabel.setGeometry(QtCore.QRect(260, 150, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Pontoscorelabel.setFont(font)
        self.Pontoscorelabel.setObjectName('Pontoscorelabel')
        self.ClnicaLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.ClnicaLabel.setGeometry(QtCore.QRect(10, 210, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ClnicaLabel.setFont(font)
        self.ClnicaLabel.setObjectName('ClnicaLabel')
        self.Clinicaedit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Clinicaedit.setGeometry(QtCore.QRect(10, 230, 231, 20))
        self.Clinicaedit.setObjectName('Clinicaedit')
        self.Clinicaedit.setStyleSheet(colo)
        self.Labeltipodeleito = QtWidgets.QLabel(parent=self.centralwidget)
        self.Labeltipodeleito.setGeometry(QtCore.QRect(10, 150, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Labeltipodeleito.setFont(font)
        self.Labeltipodeleito.setObjectName('Labeltipodeleito')
        self.Pontoscoescolhe = QtWidgets.QDoubleSpinBox(parent=self.centralwidget)
        self.Pontoscoescolhe.setGeometry(QtCore.QRect(260, 170, 81, 22))
        self.Pontoscoescolhe.setMaximum(1000)
        self.Pontoscoescolhe.setObjectName('Pontoscoescolhe')
        self.Pontoscoescolhe.setStyleSheet(colo)
        self.Lbelobs = QtWidgets.QLabel(parent=self.centralwidget)
        self.Lbelobs.setGeometry(QtCore.QRect(10, 310, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Lbelobs.setFont(font)
        self.Lbelobs.setObjectName('Lbelobs')
        self.Combotipoleito = QtWidgets.QComboBox(parent=self.centralwidget)
        self.Combotipoleito.setGeometry(QtCore.QRect(10, 170, 180, 31))
        self.Combotipoleito.setObjectName('Combotipoleito')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.setItemText(0, '')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.addItem('')
        self.Combotipoleito.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.Labelpriorida = QtWidgets.QLabel(parent=self.centralwidget)
        self.Labelpriorida.setGeometry(QtCore.QRect(260, 200, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Labelpriorida.setFont(font)
        self.Labelpriorida.setObjectName('Labelpriorida')
        self.Comboprioridade = QtWidgets.QComboBox(parent=self.centralwidget)
        self.Comboprioridade.setGeometry(QtCore.QRect(260, 220, 151, 31))
        self.Comboprioridade.setObjectName('Comboprioridade')
        self.Comboprioridade.addItem('')
        self.Comboprioridade.setItemText(0, '')
        self.Comboprioridade.addItem('')
        self.Comboprioridade.addItem('')
        self.Comboprioridade.addItem('')
        self.Comboprioridade.addItem('')
        self.Comboprioridade.addItem('')
        self.Comboprioridade.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.Nomesol = QtWidgets.QLabel(parent=self.centralwidget)
        self.Nomesol.setGeometry(QtCore.QRect(260, 250, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Nomesol.setFont(font)
        self.Nomesol.setObjectName('Nomesol')
        self.Nomesoliedit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Nomesoliedit.setGeometry(QtCore.QRect(260, 280, 231, 20))
        self.Nomesoliedit.setObjectName('Nomesoliedit')
        self.Nomesoliedit.setStyleSheet(colo)
        self.Nomesoliedit.setText(self.teladem.nome_user)
        self.Contato = QtWidgets.QLabel(parent=self.centralwidget)
        self.Contato.setGeometry(QtCore.QRect(10, 260, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Contato.setFont(font)
        self.Contato.setObjectName('Contato')
        self.Btnconf = QtWidgets.QPushButton('CANCELAR', parent=self.centralwidget)
        self.Btnconf1 = QtWidgets.QPushButton('SALVAR', parent=self.centralwidget)
        self.Btnconf.setStyleSheet('\n                QPushButton {\n                    border: 2px solid #2E3D48;\n                    border-radius: 10px;\n                    background-color: #FFFFFF;\n                    color: #2E3D48;\n                }\n\n                QPushButton:hover {\n                    background-color: #DDDDDD;  /* Change this to your desired hover color */\n                    color: rgb(0, 0, 0);\n                }\n\n                QPushButton:pressed {\n                    background-color: #2E3D48;  /* Change this to your desired pressed color */\n                    color: #FFFFFF;\n                }\n            ')
        self.Btnconf1.setStyleSheet('\n                QPushButton {\n                    border: 2px solid #2E3D48;\n                    border-radius: 10px;\n                    background-color: #FFFFFF;\n                    color: #2E3D48;\n                }\n\n                QPushButton:hover {\n                    background-color: #DDDDDD;  /* Change this to your desired hover color */\n                    color: rgb(0, 0, 0);\n                }\n\n                QPushButton:pressed {\n                    background-color: #2E3D48;  /* Change this to your desired pressed color */\n                    color: #FFFFFF;\n                }\n            ')
        self.Btnconf.clicked.connect(self.Cancel)
        self.Btnconf1.clicked.connect(lambda: self.Salva(Cadastro))
        self.Btnconf.setGeometry(QtCore.QRect(410, 544, 70, 23))
        self.Btnconf1.setGeometry(QtCore.QRect(330, 544, 70, 23))
        self.Contatoedit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Contatoedit.setGeometry(QtCore.QRect(10, 280, 231, 21))
        self.Contatoedit.setObjectName('Contatoedit')
        self.Contatoedit.setStyleSheet(colo)
        self.Confirm = QtWidgets.QLabel(parent=self.centralwidget)
        self.Confirm.setGeometry(QtCore.QRect(330, 520, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Confirm.setFont(font)
        self.Confirm.setObjectName('Confirm')
        self.Obseredit = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.Obseredit.setGeometry(QtCore.QRect(10, 340, 481, 181))
        self.Obseredit.setObjectName('Obseredit')
        self.Obseredit.setStyleSheet(colo)
        for widget in self.centralwidget.findChildren(QtWidgets.QWidget):
            widget.show()
        self.centralwidget.show()
        self.retranslateUi(Cadastro)
        self.load()

    def retranslateUi(self, Cadastro):
        _translate = QtCore.QCoreApplication.translate
        self.Titulo.setText(_translate('Cadastro', 'Cadastrar Demanda'))
        self.Nomepasc.setText(_translate('Cadastro', 'NOME DO PACIENTE '))
        self.prontuario.setText(_translate('Cadastro', 'PRONTUÁRIO '))
        self.Datanasclabel.setText(_translate('Cadastro', 'DATA DE NASCIMENTO'))
        self.Pontoscorelabel.setText(_translate('Cadastro', 'PONTUAÇÃO SCORE'))
        self.ClnicaLabel.setText(_translate('Cadastro', 'CLÍNICA'))
        self.Labeltipodeleito.setText(_translate('Cadastro', 'TIPO DE LEITO SOLICITADO'))
        self.Lbelobs.setText(_translate('Cadastro', 'OBSERVAÇÕES'))
        self.Combotipoleito.setItemText(1, _translate('Cadastro', 'ENFERMARIA FEMININA'))
        self.Combotipoleito.setItemText(2, _translate('Cadastro', 'ENFERMARIA MASCULINA'))
        self.Combotipoleito.setItemText(3, _translate('Cadastro', 'PEDIÁTRICO'))
        self.Combotipoleito.setItemText(4, _translate('Cadastro', 'CTI ADULT/UCO'))
        self.Combotipoleito.setItemText(5, _translate('Cadastro', 'CTI NEONATOLOGIA'))
        self.Combotipoleito.setItemText(6, _translate('Cadastro', 'CTI PEDIÁTRICO'))
        self.Combotipoleito.setItemText(7, _translate('Cadastro', 'ISOLAMENTO CONTATO'))
        self.Combotipoleito.setItemText(8, _translate('Cadastro', 'ISOLAMENTO RESPIRATÓRIO'))
        self.Combotipoleito.setItemText(9, _translate('Cadastro', 'MATERNIDADE'))
        self.Combotipoleito.setItemText(10, _translate('Cadastro', 'APARTAMENTO'))
        self.Combotipoleito.setItemText(11, _translate('Cadastro', 'ENFERMARIA COVID'))
        self.Combotipoleito.setItemText(12, _translate('Cadastro', 'CTI COVID'))
        self.Combotipoleito.setItemText(13, _translate('Cadastro', 'INTERNAÇÃO VIRTUAL'))
        self.Labelpriorida.setText(_translate('Cadastro', 'PRIORIDADE DA SOLICITAÇÃO'))
        self.Comboprioridade.setItemText(1, _translate('Cadastro', 'BAIXA'))
        self.Comboprioridade.setItemText(2, _translate('Cadastro', 'MÉDIA BAIXA'))
        self.Comboprioridade.setItemText(3, _translate('Cadastro', 'MÉDIA MÉDIA'))
        self.Comboprioridade.setItemText(4, _translate('Cadastro', 'MÉDIA ALTA'))
        self.Comboprioridade.setItemText(5, _translate('Cadastro', 'ALTA'))
        self.Nomesol.setText(_translate('Cadastro', 'NOME  DO SOLICITANTE'))
        self.Contato.setText(_translate('Cadastro', 'CONTATO DO SOLICITANTE'))
        self.Confirm.setText(_translate('Cadastro', 'Confirmar Socitação ?'))

    def Salva(self, Cadastro):
        npf = self.npf_edit.text()
        pronto = self.prontuario_edit.text()
        name = self.Nomepascedit.text()
        clinica_pac = self.Clinicaedit.text()
        nome_contato_sol = self.Nomesoliedit.text() + ' / ' + self.Contatoedit.text()
        obs_ps = self.Obseredit.toPlainText()
        data_nasc_obj = self.datanas.date()
        data_nasc = data_nasc_obj.toString('dd/MM/yyyy')
        ponto_score_obj = float(self.Pontoscoescolhe.value())
        ponto_score = str(ponto_score_obj)
        tipo_leito = self.Combotipoleito.currentText()
        prioridade_solic = self.Comboprioridade.currentText()
        if name and tipo_leito and prioridade_solic and clinica_pac:
            if data_nasc!= self.dataalt.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText('Confirmar Demanda?')
                msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                reply = msg_box.exec()
                if reply == QMessageBox.StandardButton.Yes:
                    print(7)
                    self.teladem.add_dados(pronto, npf, name, ponto_score, data_nasc, clinica_pac, obs_ps, tipo_leito, prioridade_solic, nome_contato_sol)
                    self.apagar_Demanda()
            else:  # inserted
                self.aviso = QtWidgets.QLabel(self.centralwidget)
                self.aviso.setGeometry(QtCore.QRect(10, 0, 500, 50))
                self.aviso.setStyleSheet('color: red;')
                font = QtGui.QFont()
                font.setPointSize(20)
                self.aviso.setFont(font)
                self.aviso.setText('O campo \"DATA DE NASCIMENTO\" é obrigatório!')
                self.aviso.setVisible(True)
                self.temporizador1()
        else:  # inserted
            self.aviso = QtWidgets.QLabel(self.centralwidget)
            self.aviso.setGeometry(QtCore.QRect(10, 5, 500, 31))
            self.aviso.setStyleSheet('color: red;border: none;')
            if not npf:
                self.aviso.setText('O campo \"NPF\" é obrigatório!')
                self.aviso.setVisible(True)
                self.temporizador1()
            else:  # inserted
                if not name:
                    self.aviso.setText('O campo \"NOME DO PACIENTE\" é obrigatório!')
                    self.aviso.setVisible(True)
                    self.temporizador1()
                else:  # inserted
                    if not tipo_leito:
                        self.aviso.setText('O campo \"TIPO DE LEITO\" é obrigatório!')
                        self.aviso.setVisible(True)
                        self.temporizador1()
                    else:  # inserted
                        if not prioridade_solic:
                            self.aviso.setText('O campo \"PRIORIDADE DA SOLICITAÇÃO\" é obrigatório!')
                            self.aviso.setVisible(True)
                            self.temporizador1()
                        else:  # inserted
                            self.aviso.setText('O campo \"CLÍNICA\" é obrigatório!')
                            self.aviso.setVisible(True)
                            self.temporizador1()

    def temporizador1(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_aviso)
        self.timer.start()

    def hide_aviso(self):
        self.aviso.hide()

    def Cancel(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Cancelar Demanda?')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.apagar_Demanda()

    def apagar_Demanda(self):
        self.Nomepascedit.clear()
        self.npf_edit.clear()
        self.prontuario_edit.clear()
        self.Clinicaedit.clear()
        self.Nomesoliedit.clear()
        self.Contatoedit.clear()
        self.Obseredit.clear()
        self.Combotipoleito.setCurrentIndex(0)
        self.Comboprioridade.setCurrentIndex(0)

    def procurar_paciente(self, pesquisa):
        if pesquisa != '':
            try:
                # Conectando ao banco de dados PostgreSQL
                connection = psycopg2.connect(
                    user='ugen_integra',
                    password='aghuintegracao',
                    host='10.36.2.35',
                    port='6544',
                    database='dbaghu'
                )
                cursor = connection.cursor()

                # Executa a consulta no banco de dados
                cursor.execute(
                    'SELECT codigo, prontuario, nome, dt_nascimento FROM agh.aip_pacientes ORDER BY codigo DESC LIMIT 2000')
                rows = cursor.fetchall()

                # Inicializa listas para armazenar dados dos pacientes
                self.lista_prontuario = []
                self.lista_nome = []
                self.lista_npf = []
                self.lista_data_nascimento = []

                # Preenche as listas com os dados do banco
                for row in rows:
                    if row[1] is not None:
                        self.lista_prontuario.append(row[1])
                        self.lista_nome.append(row[2])
                        self.lista_npf.append(row[0])
                        self.lista_data_nascimento.append(row[3])

                # Converte prontuários para strings
                self.lista_prontuario = [str(item) for item in self.lista_prontuario]
                self.lista_npf = [str(item) for item in self.lista_npf]

                # Configura QCompleter para campo de prontuário
                completer = QCompleter(self.lista_prontuario, self.centralwidget)
                completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                self.prontuario_edit.setCompleter(completer)
                self.prontuario_edit.textChanged.connect(self.prontu_text)

                # Configura QCompleter para campo de npf
                completer1 = QCompleter(self.lista_npf, self.centralwidget)
                completer1.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                self.npf_edit.setCompleter(completer1)
                self.npf_edit.textChanged.connect(self.npf_text)

            except psycopg2.Error as e:
                print('Erro ao conectar ao PostgreSQL:', e)

            finally:
                # Fecha a conexão com o banco de dados, se aberta
                if connection:
                    cursor.close()
                    connection.close()

    def prontu_text(self, text):
        if text in self.lista_prontuario:
            posicao = self.lista_prontuario.index(text)
            nome = self.lista_nome[posicao] if self.lista_nome[posicao] is not None else 'N/A'
            self.Nomepascedit.setText(nome)
            npf = self.lista_npf[posicao] if self.lista_npf[posicao] is not None else 'N/A'
            self.npf_edit.setText(npf)
            data_nasc = self.lista_data_nascimento[posicao]
            if data_nasc is not None:
                ano = data_nasc.year
                mes = data_nasc.month
                dia = data_nasc.day
                self.datanas.setDate(QtCore.QDate(ano, mes, dia))
            else:  # inserted
                ccurrent_datetime = QtCore.QDateTime.currentDateTime()
                tomorrow_datetime = ccurrent_datetime.addDays(30000)
                initial_datetime = tomorrow_datetime
                self.datanas.setDateTime(initial_datetime)
        else:  # inserted
            self.Nomepascedit.clear()
            self.npf_edit.clear()
            self.datanas.setDate(QtCore.QDate())
            ccurrent_datetime = QtCore.QDateTime.currentDateTime()
            tomorrow_datetime = ccurrent_datetime.addDays(30000)
            initial_datetime = tomorrow_datetime
            self.datanas.setDateTime(initial_datetime)

    def npf_text(self, text):
        if text in self.lista_npf:
            posicao = self.lista_npf.index(text)
            nome = self.lista_nome[posicao] if self.lista_nome[posicao] is not None else 'N/A'
            self.Nomepascedit.setText(nome)
            prontuario = self.lista_prontuario[posicao] if self.lista_prontuario[posicao] is not None else 'N/A'
            self.prontuario_edit.setText(prontuario)
            data_nasc = self.lista_data_nascimento[posicao]
            if data_nasc is not None:
                ano = data_nasc.year
                mes = data_nasc.month
                dia = data_nasc.day
                self.datanas.setDate(QtCore.QDate(ano, mes, dia))
            else:  # inserted
                ccurrent_datetime = QtCore.QDateTime.currentDateTime()
                tomorrow_datetime = ccurrent_datetime.addDays(30000)
                initial_datetime = tomorrow_datetime
                self.datanas.setDateTime(initial_datetime)
        else:  # inserted
            self.Nomepascedit.clear()
            self.prontuario_edit.clear()
            ccurrent_datetime = QtCore.QDateTime.currentDateTime()
            tomorrow_datetime = ccurrent_datetime.addDays(30000)
            initial_datetime = tomorrow_datetime
            self.datanas.setDateTime(initial_datetime)

    def load(self):
        if self.settings.contains('tema'):
            font_name = self.settings.value('font', defaultValue='')
            backcolocor = self.settings.value('tema', defaultValue='')
            color = self.settings.value('color', defaultValue='')
            tamanho = int(self.settings.value('tamanho', defaultValue=10))
            self.backcolocor = backcolocor
            self.color = color
            self.centralwidget.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;border: 2px solid #2E3D48;border-radius: 10px;')
            for label in self.centralwidget.findChildren(QtWidgets.QLabel):
                if self.Titulo == label:
                    label.setStyleSheet(f'color: {color}; font:  {30}px {font_name}; border:none')
                else:  # inserted
                    label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name}; border:none')

    def mousePressEvent(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            centralwidget.setCursor(Qt.CursorShape.ClosedHandCursor)
        centralwidget.mouse_offset = event.pos()

    def mouseReleaseEvent(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            centralwidget.setCursor(Qt.CursorShape.OpenHandCursor)

    def mouseMoveEvent(self, event, centralwidget):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = centralwidget.mapToParent(event.pos() - centralwidget.mouse_offset)
            centralwidget.move(new_pos)
            x, y = (new_pos.x(), new_pos.y())