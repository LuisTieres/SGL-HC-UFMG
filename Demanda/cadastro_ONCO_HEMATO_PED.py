# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: Demanda\cadastro_ONCO_HEMATO_PED.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDateTime, QDate, Qt
import mysql.connector
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QDateTime, QSettings, QStandardPaths

class Ui_ONCO_HEMATO_PED(object):
    def setupUi(self, MainWindow, para_teladem=None):
        self.teladem = para_teladem
        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        self.centralwidget = QtWidgets.QFrame(parent=MainWindow)
        self.centralwidget.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.centralwidget.setGeometry(QtCore.QRect(450, 50, 552, 600))
        self.centralwidget.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.centralwidget.setObjectName('frame')
        self.teladem.janela_cadastro = self.centralwidget
        self.centralwidget.setCursor(Qt.CursorShape.OpenHandCursor)
        self.centralwidget.mousePressEvent = lambda event, centralwidget=self.centralwidget: self.mousePressEvent(event, centralwidget)
        self.centralwidget.mouseReleaseEvent = lambda event, centralwidget=self.centralwidget: self.mouseReleaseEvent(event, centralwidget)
        self.centralwidget.mouseMoveEvent = lambda event, centralwidget=self.centralwidget: self.mouseMoveEvent(event, centralwidget)
        colo = 'border: 2px solid #2E3D48; border-radius: 10px; background-color: white;'
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
        self.Nomepascedit.setGeometry(QtCore.QRect(10, 120, 231, 31))
        self.Nomepascedit.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.Nomepascedit.setObjectName('Nomepascedit')
        self.Nomepasc = QtWidgets.QLabel(parent=self.centralwidget)
        self.Nomepasc.setGeometry(QtCore.QRect(10, 100, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Nomepasc.setFont(font)
        self.Nomepasc.setObjectName('Nomepasc')
        self.datanas = QtWidgets.QDateEdit(parent=self.centralwidget)
        self.datanas.setGeometry(QtCore.QRect(10, 180, 91, 21))
        self.datanas.setStyleSheet('')
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
        self.Datanasclabel.setGeometry(QtCore.QRect(10, 160, 181, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Datanasclabel.setFont(font)
        self.Datanasclabel.setObjectName('Datanasclabel')
        self.PESO_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.PESO_label.setGeometry(QtCore.QRect(259, 210, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.PESO_label.setFont(font)
        self.PESO_label.setObjectName('PESO_label')
        self.ClnicaLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.ClnicaLabel.setGeometry(QtCore.QRect(10, 320, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ClnicaLabel.setFont(font)
        self.ClnicaLabel.setObjectName('ClnicaLabel')
        self.Clinicaedit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Clinicaedit.setGeometry(QtCore.QRect(10, 340, 231, 31))
        self.Clinicaedit.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.Clinicaedit.setObjectName('Clinicaedit')
        self.Labeltipodeleito = QtWidgets.QLabel(parent=self.centralwidget)
        self.Labeltipodeleito.setGeometry(QtCore.QRect(10, 260, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Labeltipodeleito.setFont(font)
        self.Labeltipodeleito.setObjectName('Labeltipodeleito')
        self.Combotipoleito = QtWidgets.QComboBox(parent=self.centralwidget)
        self.Combotipoleito.setGeometry(QtCore.QRect(10, 280, 221, 31))
        self.Combotipoleito.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
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
        self.Label_data_internacao.setGeometry(QtCore.QRect(260, 160, 80, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Label_data_internacao.setFont(font)
        self.Label_data_internacao.setObjectName('Label_data_internacao')
        self.ALTURA_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.ALTURA_label.setGeometry(QtCore.QRect(10, 210, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ALTURA_label.setFont(font)
        self.ALTURA_label.setObjectName('ALTURA_label')
        self.Btnconf = QtWidgets.QPushButton('CANCELAR', parent=self.centralwidget)
        self.Btnconf1 = QtWidgets.QPushButton('SALVAR', parent=self.centralwidget)
        self.Btnconf.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n\n                        QPushButton:hover {\n                            background-color: #DDDDDD;  /* Change this to your desired hover color */\n                            color: rgb(0, 0, 0);\n                        }\n\n                        QPushButton:pressed {\n                            background-color: #2E3D48;  /* Change this to your desired pressed color */\n                            color: #FFFFFF;\n                        }\n                    ')
        self.Btnconf1.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n\n                        QPushButton:hover {\n                            background-color: #DDDDDD;  /* Change this to your desired hover color */\n                            color: rgb(0, 0, 0);\n                        }\n\n                        QPushButton:pressed {\n                            background-color: #2E3D48;  /* Change this to your desired pressed color */\n                            color: #FFFFFF;\n                        }\n                    ')
        self.Btnconf.setGeometry(QtCore.QRect(410, 540, 70, 23))
        self.Btnconf1.setGeometry(QtCore.QRect(330, 540, 70, 23))
        self.Btnconf.clicked.connect(self.Cancel)
        self.Btnconf1.clicked.connect(self.atualiza_banco)
        self.Confirm = QtWidgets.QLabel(parent=self.centralwidget)
        self.Confirm.setGeometry(QtCore.QRect(320, 506, 161, 20))
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
        self.line_edit_leito_atual.setGeometry(QtCore.QRect(260, 120, 231, 31))
        self.line_edit_leito_atual.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.line_edit_leito_atual.setObjectName('line_edit_leito_atual')
        self.label_pos = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_pos.setGeometry(QtCore.QRect(260, 260, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_pos.setFont(font)
        self.label_pos.setObjectName('label_pos')
        self.comboBox_pos = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox_pos.setGeometry(QtCore.QRect(260, 280, 211, 31))
        self.comboBox_pos.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.comboBox_pos.setObjectName('comboBox_pos')
        self.comboBox_pos.addItem('')
        self.comboBox_pos.setItemText(0, '')
        self.comboBox_pos.addItem('')
        self.comboBox_pos.addItem('')
        self.Contato = QtWidgets.QLabel(parent=self.centralwidget)
        self.Contato.setGeometry(QtCore.QRect(260, 380, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Contato.setFont(font)
        self.Contato.setObjectName('Contato')
        self.Contatoedit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Contatoedit.setGeometry(QtCore.QRect(260, 400, 231, 31))
        self.Contatoedit.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.Contatoedit.setObjectName('Contatoedit')
        self.Nomesoliedit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Nomesoliedit.setGeometry(QtCore.QRect(10, 400, 231, 31))
        self.Nomesoliedit.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.Nomesoliedit.setObjectName('Nomesoliedit')
        self.Nomesol = QtWidgets.QLabel(parent=self.centralwidget)
        self.Nomesol.setGeometry(QtCore.QRect(10, 380, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Nomesol.setFont(font)
        self.Nomesol.setObjectName('Nomesol')
        self.double_PESO = QtWidgets.QDoubleSpinBox(parent=self.centralwidget)
        self.double_PESO.setGeometry(QtCore.QRect(260, 230, 101, 22))
        self.double_PESO.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.double_PESO.setMaximum(9999999999999.99)
        self.double_PESO.setObjectName('double_PESO')
        self.double_ALTURA = QtWidgets.QDoubleSpinBox(parent=self.centralwidget)
        self.double_ALTURA.setGeometry(QtCore.QRect(10, 230, 101, 22))
        self.double_ALTURA.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.double_ALTURA.setMaximum(9999999999999.99)
        self.double_ALTURA.setObjectName('double_ALTURA')
        self.label_procedimento = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_procedimento.setGeometry(QtCore.QRect(260, 321, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_procedimento.setFont(font)
        self.label_procedimento.setObjectName('label_procedimento')
        self.lineEdit_procedimento = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_procedimento.setGeometry(QtCore.QRect(260, 340, 231, 31))
        self.lineEdit_procedimento.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.lineEdit_procedimento.setObjectName('lineEdit_procedimento')
        self.dateEdit_internacao = QtWidgets.QDateEdit(parent=self.centralwidget)
        self.dateEdit_internacao.setGeometry(QtCore.QRect(260, 180, 110, 22))
        self.dateEdit_internacao.setCalendarPopup(True)
        self.dateEdit_internacao.setObjectName('dateEdit')
        self.dateEdit_internacao.setStyleSheet('background-color: rgb(255, 255, 255);border:none;')
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 440, 381, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName('label')
        self.comboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 460, 121, 31))
        self.comboBox.setStyleSheet('background-color: rgb(255, 255, 255);border: none;')
        self.comboBox.setObjectName('comboBox')
        self.comboBox.addItem('')
        self.comboBox.setItemText(0, '')
        self.comboBox.addItem('')
        self.comboBox.addItem('')
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
                    'ORDER BY codigo DESC LIMIT 100'
                )
                rows = cursor.fetchall()
                self.lista_prontuario = []
                self.lista_nome = []
                self.lista_npf = []
                self.lista_data_nascimento = []

                for row in rows:
                    if row[1] is not None:
                        self.lista_prontuario.append(row[1])
                        self.lista_nome.append(row[2])
                        self.lista_npf.append(row[0])
                        self.lista_data_nascimento.append(row[3])

                self.lista_prontuario = [str(item) for item in self.lista_prontuario]
                self.lista_npf = [str(item) for item in self.lista_npf]

                # Configurações dos Completers
                completer = QCompleter(self.lista_prontuario, self.centralwidget)
                completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                self.prontuario_edit.setCompleter(completer)
                self.prontuario_edit.textChanged.connect(self.prontu_text)

                completer1 = QCompleter(self.lista_npf, self.centralwidget)
                completer1.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                self.prontuario_edit.setCompleter(completer1)

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
        data_internacao_obj = self.dateEdit_internacao.date()
        data_internacao = data_internacao_obj.toString('dd/MM/yyyy')
        leito_atual = self.line_edit_leito_atual.text()
        clinica = self.Clinicaedit.text()
        procedimento = self.lineEdit_procedimento.text()
        internado = self.comboBox.currentText()
        data_nasc_obj = self.datanas.date()
        data_nasc = data_nasc_obj.toString('dd/MM/yyyy')
        tipo_leito = self.Combotipoleito.currentText()
        altura_obj = float(self.double_ALTURA.value())
        altura = str(altura_obj)
        peso_obj = float(self.double_PESO.value())
        peso = str(peso_obj)
        sol_nome = self.Nomesoliedit.text()
        contato = self.Contatoedit.text()
        pos = self.comboBox_pos.currentText()
        current_datetime = QtCore.QDateTime.currentDateTime()
        formatted_date = current_datetime.toString('dd/MM/yyyy')
        formatted_time = current_datetime.toString('hh:mm:ss')
        cursor = conexao.cursor()
        selected_date = self.datanas.date()
        current_date = QDate.currentDate()
        age = current_date.year() - selected_date.year()
        if selected_date.month() > current_date.month() or (selected_date.month() == current_date.month() and selected_date.day() > current_date.day()):
            age -= 1
        pronto = self.prontuario_edit.text()
        npf = self.npf_edit.text()
        comando = f"INSERT INTO tabela_onco_hemato_ped (PRONTUARIO,NPF,DATA_E_HORA_DA_INTERNAÇÃO, NOME_DO_PACIENTE, DATA_DE_NASCIMENTO, IDADE, PESO_ALTURA, DATA_HORARIO_DA_SOLICITAÇÃO, PACIENTE_PRONTO_SOCORRO, CLÍNICA, PROCEDIMENTO, TIPO_DE_LEITO_SOLICITADO, PÓS_OPERATÓRIO_EM_CTI, NOME_CONTATO_SOLICITANTE) VALUES (\"{pronto}\",\"{npf}\",\"{data_internacao}\", \"{name}\",\"{data_nasc}\",\"{age}\",\"{peso + ' kg e ' + altura + ' m'}\",\"{formatted_date + ' ' + formatted_time}\",\"{internado}\",\"{clinica}\",\"{procedimento}\",\"{tipo_leito}\", \"{pos}\", \"{sol_nome + ' / ' + contato}\")"
        if name and data_nasc and tipo_leito:
            if data_nasc == self.dataalt.text():
                self.aviso = QtWidgets.QLabel(self.centralwidget)
                self.aviso.setGeometry(QtCore.QRect(10, 0, 500, 31))
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
                    print(age)
                    self.teladem.add_dados_onco_hemato_ped(data_internacao, name, data_nasc, age, peso + ' kg e ' + altura + ' m ', formatted_date + ' ' + formatted_time, internado, clinica, procedimento, tipo_leito, pos, sol_nome + ' / ' + contato)
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
        self.line_edit_leito_atual.clear()
        self.Combotipoleito.setCurrentIndex(0)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'MainWindow'))
        self.Titulo.setText(_translate('MainWindow', 'Cadastrar Demanda'))
        self.Nomepasc.setText(_translate('MainWindow', 'NOME DO PACIENTE '))
        self.prontuario.setText(_translate('Cadastro', 'PRONTUÁRIO '))
        self.Datanasclabel.setText(_translate('MainWindow', 'DATA DE NASCIMENTO'))
        self.PESO_label.setText(_translate('MainWindow', 'PESO DA CRIANÇA'))
        self.ClnicaLabel.setText(_translate('MainWindow', 'CLÍNICA'))
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
        self.ALTURA_label.setText(_translate('MainWindow', 'ALTURA DA CRIANÇA'))
        self.Confirm.setText(_translate('MainWindow', 'Confirmar Socitação ?'))
        self.labelleito_atual.setText(_translate('MainWindow', 'LEITO DE INTERNAÇÃO ATUAL '))
        self.label_pos.setText(_translate('MainWindow', 'PÓS OPERATÓRIO EM CTI?'))
        self.comboBox_pos.setItemText(1, _translate('MainWindow', 'SIM'))
        self.comboBox_pos.setItemText(2, _translate('MainWindow', 'NÃO'))
        self.Contato.setText(_translate('MainWindow', 'CONTATO DO SOLICITANTE'))
        self.Nomesol.setText(_translate('MainWindow', 'NOME  DO SOLICITANTE'))
        self.label_procedimento.setText(_translate('MainWindow', 'PROCEDIMENTO'))
        self.label.setText(_translate('MainWindow', 'PACIENTE JA INTERNADO NO PRONTO SOCORRO?'))
        self.comboBox.setItemText(1, _translate('MainWindow', 'SIM'))
        self.comboBox.setItemText(2, _translate('MainWindow', 'NÃO'))

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