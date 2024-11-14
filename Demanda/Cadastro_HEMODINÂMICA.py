# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: Demanda\Cadastro_HEMODINÂMICA.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDateTime, Qt, QSettings, QStandardPaths
import mysql.connector
from PyQt6.QtGui import QIcon

class Ui_HEMODINAMICA(object):
    def setupUi(self, MainWindow, para_teladem=None):
        self.teladem = para_teladem
        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        self.centralwidget = QtWidgets.QFrame(parent=MainWindow)
        self.centralwidget.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.centralwidget.setGeometry(QtCore.QRect(450, 50, 554, 470))
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
        self.Titulo.setObjectName('Titulo')
        self.Nomepascedit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Nomepascedit.setGeometry(QtCore.QRect(10, 120, 231, 21))
        self.Nomepascedit.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.Nomepascedit.setObjectName('Nomepascedit')
        self.Nomepasc = QtWidgets.QLabel(parent=self.centralwidget)
        self.Nomepasc.setGeometry(QtCore.QRect(10, 100, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Nomepasc.setFont(font)
        self.Nomepasc.setObjectName('Nomepasc')
        self.datanas = QtWidgets.QDateEdit(parent=self.centralwidget)
        self.datanas.setGeometry(QtCore.QRect(10, 170, 91, 21))
        colo = 'border: 2px solid #2E3D48  ; border-radius: 10px; background-color: white;'
        self.prontuario_edit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.prontuario_edit.setGeometry(QtCore.QRect(10, 70, 231, 21))
        self.prontuario_edit.setObjectName('prontuario_edit')
        self.prontuario_edit.setStyleSheet(colo)
        self.npf_edit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.npf_edit.setGeometry(QtCore.QRect(260, 70, 231, 21))
        self.npf_edit.setObjectName('npf_edit')
        self.npf_edit.setStyleSheet(colo)
        self.npf_edit.textChanged.connect(self.procurar_paciente)
        self.prontuario_edit.textChanged.connect(self.procurar_paciente)
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
        current_datetime = QtCore.QDateTime.currentDateTime()
        tomorrow_datetime = current_datetime.addDays(30000)
        initial_datetime = tomorrow_datetime
        self.dataalt = QtWidgets.QDateEdit()
        self.dataalt.setDateTime(initial_datetime)
        self.datanas.setDateTime(initial_datetime)
        self.datanas.setCalendarPopup(True)
        self.datanas.setObjectName('datanas')
        self.datanas.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.Datanasclabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.Datanasclabel.setGeometry(QtCore.QRect(10, 150, 181, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Datanasclabel.setFont(font)
        self.Datanasclabel.setObjectName('Datanasclabel')
        self.data_hora_proced_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.data_hora_proced_label.setGeometry(QtCore.QRect(260, 150, 261, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.data_hora_proced_label.setFont(font)
        self.data_hora_proced_label.setObjectName('data_hora_proced_label')
        self.ClnicaLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.ClnicaLabel.setGeometry(QtCore.QRect(10, 310, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ClnicaLabel.setFont(font)
        self.ClnicaLabel.setObjectName('ClnicaLabel')
        self.Clinicaedit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Clinicaedit.setGeometry(QtCore.QRect(10, 330, 231, 20))
        self.Clinicaedit.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.Clinicaedit.setObjectName('Clinicaedit')
        self.Labeltipodeleito = QtWidgets.QLabel(parent=self.centralwidget)
        self.Labeltipodeleito.setGeometry(QtCore.QRect(10, 200, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Labeltipodeleito.setFont(font)
        self.Labeltipodeleito.setObjectName('Labeltipodeleito')
        self.Combotipoleito = QtWidgets.QComboBox(parent=self.centralwidget)
        self.Combotipoleito.setGeometry(QtCore.QRect(10, 220, 221, 31))
        self.Combotipoleito.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
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
        self.Label_data_internacao = QtWidgets.QLabel(parent=self.centralwidget)
        self.Label_data_internacao.setGeometry(QtCore.QRect(260, 260, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Label_data_internacao.setFont(font)
        self.Label_data_internacao.setObjectName('Label_data_internacao')
        self.prioridade_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.prioridade_label.setGeometry(QtCore.QRect(10, 260, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.prioridade_label.setFont(font)
        self.prioridade_label.setObjectName('prioridade_label')
        self.Btnconf = QtWidgets.QPushButton('CANCELAR', parent=self.centralwidget)
        self.Btnconf1 = QtWidgets.QPushButton('SALVAR', parent=self.centralwidget)
        self.Btnconf.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n\n                        QPushButton:hover {\n                            background-color: #DDDDDD;  /* Change this to your desired hover color */\n                            color: rgb(0, 0, 0);\n                        }\n\n                        QPushButton:pressed {\n                            background-color: #2E3D48;  /* Change this to your desired pressed color */\n                            color: #FFFFFF;\n                        }\n                    ')
        self.Btnconf1.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n\n                        QPushButton:hover {\n                            background-color: #DDDDDD;  /* Change this to your desired hover color */\n                            color: rgb(0, 0, 0);\n                        }\n\n                        QPushButton:pressed {\n                            background-color: #2E3D48;  /* Change this to your desired pressed color */\n                            color: #FFFFFF;\n                        }\n                    ')
        tooltip_text = self.Btnconf.text()
        self.Btnconf.setToolTip(tooltip_text)
        tooltip_text = self.Btnconf1.text()
        self.Btnconf1.setToolTip(tooltip_text)
        self.Btnconf.setGeometry(QtCore.QRect(410, 400, 70, 23))
        self.Btnconf1.setGeometry(QtCore.QRect(330, 400, 70, 23))
        self.Btnconf.clicked.connect(self.Cancel)
        self.Btnconf1.clicked.connect(self.atualiza_banco)
        self.prioridade_line_edit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.prioridade_line_edit.setGeometry(QtCore.QRect(10, 280, 231, 21))
        self.prioridade_line_edit.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.prioridade_line_edit.setObjectName('prioridade_line_edit')
        self.Confirm = QtWidgets.QLabel(parent=self.centralwidget)
        self.Confirm.setGeometry(QtCore.QRect(350, 370, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Confirm.setFont(font)
        self.Confirm.setObjectName('Confirm')
        self.labelleito_atual = QtWidgets.QLabel(parent=self.centralwidget)
        self.labelleito_atual.setGeometry(QtCore.QRect(260, 100, 231, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelleito_atual.setFont(font)
        self.labelleito_atual.setObjectName('labelleito_atual')
        self.line_edit_leito_atual = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.line_edit_leito_atual.setGeometry(QtCore.QRect(260, 120, 231, 20))
        self.line_edit_leito_atual.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.line_edit_leito_atual.setObjectName('line_edit_leito_atual')
        self.procedimento_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.procedimento_label.setGeometry(QtCore.QRect(260, 200, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.procedimento_label.setFont(font)
        self.procedimento_label.setObjectName('procedimento_label')
        self.procedimento_edit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.procedimento_edit.setGeometry(QtCore.QRect(260, 220, 231, 31))
        self.procedimento_edit.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.procedimento_edit.setObjectName('procedimento_edit')
        self.data_hora_proced_date_time = QtWidgets.QDateTimeEdit(parent=self.centralwidget)
        self.data_hora_proced_date_time.setGeometry(QtCore.QRect(260, 170, 194, 22))
        self.data_hora_proced_date_time.setDateTime(initial_datetime)
        self.data_hora_proced_date_time.setCalendarPopup(True)
        self.data_hora_proced_date_time.setCurrentSectionIndex(0)
        self.data_hora_proced_date_time.setTimeSpec(QtCore.Qt.TimeSpec.TimeZone)
        self.data_hora_proced_date_time.setObjectName('data_hora_proced_date_time')
        self.data_hora_proced_date_time.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.date_internacao_Edit = QtWidgets.QDateEdit(parent=self.centralwidget)
        self.date_internacao_Edit.setGeometry(QtCore.QRect(260, 280, 110, 22))
        self.date_internacao_Edit.setDateTime(initial_datetime)
        self.date_internacao_Edit.setCalendarPopup(True)
        self.date_internacao_Edit.setObjectName('date_internacao_Edit')
        self.date_internacao_Edit.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.retranslateUi(MainWindow)
        for widget in self.centralwidget.findChildren(QtWidgets.QWidget):
            widget.show()
        self.centralwidget.show()
        self.load()

    def procurar_paciente(self, pesquisa):
        import psycopg2
        from PyQt6.QtWidgets import QCompleter
        from PyQt6.QtCore import Qt

        if pesquisa != '':
            try:
                connection = psycopg2.connect(
                    user='ugen_integra',
                    password='aghuintegracao',
                    host='10.36.2.35',
                    port='6544',
                    database='dbaghu'
                )
                cursor = connection.cursor()
                cursor.execute(
                    'SELECT codigo, prontuario, nome, dt_nascimento '
                    'FROM agh.aip_pacientes '
                    'ORDER BY codigo DESC LIMIT 2000'
                )
                rows = cursor.fetchall()

                # Inicializa listas para armazenar os dados dos pacientes
                self.lista_prontuario = []
                self.lista_nome = []
                self.lista_npf = []
                self.lista_data_nascimento = []

                # Preenche as listas com os dados recuperados
                for row in rows:
                    if row[1] is not None:
                        self.lista_prontuario.append(row[1])
                        self.lista_nome.append(row[2])
                        self.lista_npf.append(row[0])
                        self.lista_data_nascimento.append(row[3])

                # Converte os itens da lista_prontuario para strings
                self.lista_prontuario = [str(item) for item in self.lista_prontuario]
                self.lista_npf = [str(item) for item in self.lista_npf]

                # Configura o QCompleter para auto completar
                completer = QCompleter(self.lista_prontuario, self.centralwidget)
                completer.setCaseSensitivity(Qt.CaseInsensitive)
                self.prontuario_edit.setCompleter(completer)
                self.prontuario_edit.textChanged.connect(self.prontu_text)

                completer1 = QCompleter(self.lista_npf, self.centralwidget)
                completer1.setCaseSensitivity(Qt.CaseInsensitive)
                # Adicione aqui qualquer configuração necessária para `completer1`

            except psycopg2.Error as e:
                print('Erro ao conectar ao PostgreSQL:', e)

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

    def atualiza_banco(self):
        conta_linha = self.teladem.conta_linha()
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        name = self.Nomepascedit.text()
        clinica_pac = self.Clinicaedit.text()
        leito_atual = self.line_edit_leito_atual.text()
        data_procd_obj = self.data_hora_proced_date_time.date()
        hora_procd_obj = self.data_hora_proced_date_time.time()
        data_procd_str = data_procd_obj.toString('dd/MM/yyyy')
        hora_procd_str = hora_procd_obj.toString('hh:mm')
        procedimento = self.procedimento_edit.text()
        data_int_obj = self.date_internacao_Edit.date()
        data_int_str = data_int_obj.toString('dd/MM/yyyy')
        data_nasc_obj = self.datanas.date()
        data_nasc = data_nasc_obj.toString('dd/MM/yyyy')
        tipo_leito = self.Combotipoleito.currentText()
        prioridade = self.prioridade_line_edit.text()
        current_datetime = QDateTime.currentDateTime()
        formatted_date = current_datetime.toString('dd/MM/yyyy')
        formatted_time = current_datetime.toString('hh:mm:ss')
        cursor = conexao.cursor()
        pronto = self.prontuario_edit.text()
        npf = self.npf_edit.text()
        comando = f"INSERT INTO tabela_hemodinamica (PRONTUARIO,NPF,DATA_E_HORA_DO_PROCEDIMENTO, NOME_DO_PACIENTE, DATA_DE_NASCIMENTO, DATA_DA_INTERNAÇÃO, DATA_E_HORA_DA_SOLICITAÇÃO, LEITO_DE_INTERNAÇÃO_ATUAL, CLÍNICA, PROCEDIMENTO, PRIORIDADE, TIPO_DE_LEITO_SOLICITADO) VALUES (\"{pronto}\",\"{npf}\", \"{data_procd_str + ' ' + hora_procd_str}\",\"{name}\", \"{data_nasc}\",\"{data_int_str}\",\"{formatted_date + ' ' + formatted_time}\",\"{leito_atual}\",\"{clinica_pac}\",\"{procedimento}\",\"{prioridade}\",\"{tipo_leito}\")"
        if name and data_nasc and tipo_leito and prioridade and clinica_pac and data_procd_str and hora_procd_str:
            if data_nasc == self.dataalt.text():
                self.aviso = QtWidgets.QLabel(self.centralwidget)
                self.aviso.setGeometry(QtCore.QRect(10, 0, 300, 31))
                self.aviso.setStyleSheet('color: red;')
                self.aviso.setText('O campo \"DATA DE NASCIMENTO\" é obrigatório!')
                self.aviso.setVisible(True)
                self.temporizador1()
            else:  # inserted
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText('Confirmar Demanda?')
                msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                reply = msg_box.exec()
                if reply == QMessageBox.StandardButton.Yes:
                    cursor.execute(comando)
                    self.teladem.add_dados_hemodinamica(data_procd_str + ' ' + hora_procd_str, name, data_nasc, data_int_str, formatted_date + ' ' + formatted_time, leito_atual, clinica_pac, procedimento, prioridade, tipo_leito)
                    self.apagar_Demanda()
        else:  # inserted
            self.aviso = QtWidgets.QLabel(self.centralwidget)
            self.aviso.setGeometry(QtCore.QRect(10, 0, 500, 31))
            self.aviso.setStyleSheet('color: red;')
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
                        if not prioridade:
                            self.aviso.setText('O campo \"PRIORIDADE DA SOLICITAÇÃO\" é obrigatório!')
                            self.aviso.setVisible(True)
                            self.temporizador1()
                        else:  # inserted
                            self.aviso.setText('O campo \"CLÍNICA\" é obrigatório!')
                            self.aviso.setVisible(True)
                            self.temporizador1()
        conexao.commit()
        cursor.close()
        conexao.close()

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
        self.Clinicaedit.clear()
        self.line_edit_leito_atual.clear()
        self.prioridade_line_edit.clear()
        self.Clinicaedit.clear()
        self.Combotipoleito.setCurrentIndex(0)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'MainWindow'))
        self.Titulo.setText(_translate('MainWindow', 'Cadastrar Demanda'))
        self.Nomepasc.setText(_translate('MainWindow', 'NOME DO PACIENTE '))
        self.Datanasclabel.setText(_translate('MainWindow', 'DATA DE NASCIMENTO'))
        self.data_hora_proced_label.setText(_translate('MainWindow', 'DATA E HORA DO PROCEDIMENTO'))
        self.ClnicaLabel.setText(_translate('MainWindow', 'CLÍNICA'))
        self.prontuario.setText(_translate('Cadastro', 'PRONTUÁRIO '))
        self.Labeltipodeleito.setText(_translate('MainWindow', 'TIPO DE LEITO SOLICITADO'))
        self.Combotipoleito.setItemText(1, _translate('MainWindow', 'ENFERMARIA FEMININA'))
        self.Combotipoleito.setItemText(2, _translate('MainWindow', 'ENFERMARIA MASCULINA'))
        self.Combotipoleito.setItemText(3, _translate('MainWindow', 'PEDIÁTRICO'))
        self.Combotipoleito.setItemText(4, _translate('MainWindow', 'CTI ADULT/UCO'))
        self.Combotipoleito.setItemText(5, _translate('MainWindow', 'CTI NEONATOLOGIA'))
        self.Combotipoleito.setItemText(6, _translate('MainWindow', 'CTI PEDIÁTRICO'))
        self.Combotipoleito.setItemText(7, _translate('MainWindow', 'ISOLAMENTO CONTATO'))
        self.Combotipoleito.setItemText(8, _translate('MainWindow', 'ISOLAMENTO RESPIRATÓRIO'))
        self.Combotipoleito.setItemText(9, _translate('MainWindow', 'MATERNIDADE'))
        self.Combotipoleito.setItemText(10, _translate('MainWindow', 'APARTAMENTO'))
        self.Combotipoleito.setItemText(11, _translate('MainWindow', 'ENFERMARIA COVID'))
        self.Label_data_internacao.setText(_translate('MainWindow', 'DATA DA INTERNAÇÃO'))
        self.prioridade_label.setText(_translate('MainWindow', 'PRIORIDADE'))
        self.Confirm.setText(_translate('MainWindow', 'Confirmar Socitação ?'))
        self.labelleito_atual.setText(_translate('MainWindow', 'LEITO DE INTERNAÇÃO ATUAL '))
        self.procedimento_label.setText(_translate('MainWindow', 'PROCEDIMENTO'))

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