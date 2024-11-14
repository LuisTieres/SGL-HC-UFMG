# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: tela_reserva.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QDateTime, Qt, QSettings, QStandardPaths
import mysql.connector
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
import psycopg2

class Ui_reserva(QtWidgets.QMainWindow):
    def setupUi(self, Form, variavel, dados_demanda=None):
        self.ala = 'CTI PEDIÁTRICO - 06N'
        self.dados = dados_demanda
        self.variavel = variavel
        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setStyleSheet('background-color: #5DADE2;')
        self.frame.setGeometry(QtCore.QRect(350, 80, 729, 580))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.dados.janela_reserva = self.frame
        self.frame.setCursor(Qt.CursorShape.OpenHandCursor)
        self.frame.mousePressEvent = lambda event, frame=self.frame: self.mousePressEvent_2(event, frame)
        self.frame.mouseReleaseEvent = lambda event, frame=self.frame: self.mouseReleaseEvent_2(event, frame)
        self.frame.mouseMoveEvent = lambda event, frame=self.frame: self.mouseMoveEvent_2(event, frame)
        icon = QIcon('emergencia.ico')
        pixmap = icon.pixmap(50, 50)
        self.icone = QtWidgets.QLabel(parent=self.frame)
        self.icone.setPixmap(pixmap)
        self.icone.setGeometry(QtCore.QRect(3, 3, 50, 50))
        self.icone.show()
        self.tabela_reserva = QtWidgets.QTreeWidget(parent=self.frame)
        self.tabela_reserva.setGeometry(QtCore.QRect(100, 120, 551, 400))
        self.tabela_reserva.setStyleSheet('background-color: rgb(255, 255, 255);border: none;gridline-color: black;')
        self.tabela_reserva.setObjectName('Tabela de reserva')
        self.btn_2leste_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_2leste_3.setGeometry(QtCore.QRect(100, 60, 71, 21))
        self.btn_2leste_3.setObjectName('btn_2leste_3')
        self.btn_2leste_3.clicked.connect(lambda: self.vagos('UNIDADE DE INTERNAÇÃO - 02L'))
        self.btn_2leste_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_6leste_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_6leste_3.setGeometry(QtCore.QRect(180, 30, 71, 21))
        self.btn_6leste_3.setObjectName('btn_6leste_3')
        self.btn_6leste_3.clicked.connect(lambda: self.vagos('UNIDADE DE INTERNAÇÃO - 06L'))
        self.btn_6leste_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_UCO_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_UCO_3.setGeometry(QtCore.QRect(340, 60, 71, 21))
        self.btn_UCO_3.setObjectName('btn_UCO_3')
        self.btn_UCO_3.clicked.connect(lambda: self.vagos('UNIDADE DE INTERNAÇÃO CORONARIANA - 03N'))
        self.btn_UCO_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_CTI_3leste_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_CTI_3leste_3.setGeometry(QtCore.QRect(260, 60, 71, 21))
        self.btn_CTI_3leste_3.setObjectName('btn_CTI_3leste_3')
        self.btn_CTI_3leste_3.clicked.connect(lambda: self.vagos('CTI ADULTO - 03L'))
        self.btn_CTI_3leste_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_2sul_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_2sul_3.setGeometry(QtCore.QRect(500, 60, 71, 21))
        self.btn_2sul_3.setObjectName('btn_2sul_3')
        self.btn_2sul_3.clicked.connect(lambda: self.vagos('UNIDADE DE INTERNAÇÃO - 02S'))
        self.btn_2sul_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_8sul_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_8sul_3.setGeometry(QtCore.QRect(420, 30, 71, 21))
        self.btn_8sul_3.setObjectName('btn_8sul_3')
        self.btn_8sul_3.clicked.connect(lambda: self.vagos('UNIDADE DE INTERNAÇÃO - 08S'))
        self.btn_8sul_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_8norte_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_8norte_3.setGeometry(QtCore.QRect(580, 60, 71, 21))
        self.btn_8norte_3.setObjectName('btn_8norte_3')
        self.btn_8norte_3.clicked.connect(lambda: self.vagos('UNIDADE DE INTERNAÇÃO - 08N'))
        self.btn_8norte_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_CTI_PS_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_CTI_PS_3.setGeometry(QtCore.QRect(180, 60, 71, 21))
        self.btn_CTI_PS_3.setObjectName('btn_CTI_PS_3')
        self.btn_CTI_PS_3.clicked.connect(lambda: self.vagos('UTI - PRONTO SOCORRO'))
        self.btn_CTI_PS_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.final = False
        self.btn_10norte_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_10norte_3.setGeometry(QtCore.QRect(260, 30, 71, 21))
        self.btn_10norte_3.setObjectName('btn_10norte_3')
        self.btn_10norte_3.clicked.connect(lambda: self.vagos('UNIDADE DE INTERNAÇÃO - 10N'))
        self.btn_10norte_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_8leste_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_8leste_3.setGeometry(QtCore.QRect(500, 30, 71, 21))
        self.btn_8leste_3.setObjectName('btn_8leste_3')
        self.btn_8leste_3.clicked.connect(lambda: self.vagos('UNIDADE DE INTERNAÇÃO - 08L'))
        self.btn_8leste_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_7norte_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_7norte_3.setGeometry(QtCore.QRect(420, 60, 71, 21))
        self.btn_7norte_3.setObjectName('btn_7norte_3')
        self.btn_7norte_3.clicked.connect(lambda: self.vagos('UNIDADE DE INTERNAÇÃO - 07N'))
        self.btn_7norte_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_9leste_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_9leste_3.setGeometry(QtCore.QRect(580, 30, 71, 21))
        self.btn_9leste_3.setObjectName('btn_9leste_3')
        self.btn_9leste_3.clicked.connect(lambda: self.vagos('UNIDADE DE INTERNAÇÃO - 09L'))
        self.btn_9leste_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_cti_ped_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_cti_ped_3.setGeometry(QtCore.QRect(100, 30, 71, 21))
        self.btn_cti_ped_3.setObjectName('btn_cti_ped_3')
        self.btn_cti_ped_3.clicked.connect(lambda: self.vagos('CTI PEDIÁTRICO - 06N'))
        self.btn_cti_ped_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_7leste_3 = QtWidgets.QPushButton(parent=self.frame)
        self.btn_7leste_3.setGeometry(QtCore.QRect(340, 30, 71, 21))
        self.btn_7leste_3.setObjectName('btn_7leste_3')
        self.btn_7leste_3.clicked.connect(lambda: self.vagos('UNIDADE DE INTERNAÇÃO - 07L'))
        self.btn_7leste_3.setStyleSheet('\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.proc_leito = QtWidgets.QLineEdit(parent=self.frame)
        self.proc_leito.setGeometry(QtCore.QRect(100, 97, 350, 20))
        self.proc_leito.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.proc_leito.setObjectName('Proc Leito')
        self.proc_leito.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        icon = QIcon('lupa.ico')
        self.proc_leito.addAction(icon, QtWidgets.QLineEdit.ActionPosition.LeadingPosition)
        self.proc_leito.setPlaceholderText('Pesquisar Paciente')
        self.btn_reserva = QtWidgets.QPushButton(parent=self.frame)
        self.btn_reserva.setGeometry(QtCore.QRect(550, 530, 101, 31))
        self.btn_reserva.setObjectName('pushButton')
        self.btn_reserva.clicked.connect(lambda: self.reservar_leito('RESERVADO'))
        self.btn_reserva.setStyleSheet('\n                QPushButton {\n                    border: 2px solid #2E3D48;\n                    border-radius: 10px;\n                    background-color: #FFFFFF;\n                    color: #2E3D48;\n                }\n\n                QPushButton:hover {\n                    background-color: #DDDDDD;  /* Change this to your desired hover color */\n                    color: rgb(0, 0, 0);\n                }\n\n                QPushButton:pressed {\n                    background-color: #2E3D48;  /* Change this to your desired pressed color */\n                    color: #FFFFFF;\n                }\n            ')
        self.btn_reserva.hide()
        self.btn_ocupa = QtWidgets.QPushButton(parent=self.frame)
        self.btn_ocupa.setGeometry(QtCore.QRect(430, 530, 101, 31))
        self.btn_ocupa.setObjectName('pushButton')
        self.btn_ocupa.clicked.connect(lambda: self.reservar_leito('OCUPADO'))
        self.btn_ocupa.setStyleSheet('\n                QPushButton {\n                    border: 2px solid #2E3D48;\n                    border-radius: 10px;\n                    background-color: #FFFFFF;\n                    color: #2E3D48;\n                }\n\n                QPushButton:hover {\n                    background-color: #DDDDDD;  /* Change this to your desired hover color */\n                    color: rgb(0, 0, 0);\n                }\n\n                QPushButton:pressed {\n                    background-color: #2E3D48;  /* Change this to your desired pressed color */\n                    color: #FFFFFF;\n                }\n            ')
        self.btn_ocupa.hide()
        self.proc_leito.textChanged.connect(self.pesquisar)
        for widget in self.frame.findChildren(QtWidgets.QWidget):
            widget.show()
        self.frame.show()
        self.retranslateUi(Form)
        self.vagos(self.ala)
        self.conf_layout()

    def pesquisar(self, pesquisa):
        num_linhas = self.tabela_reserva.topLevelItemCount()
        for row in range(num_linhas):
            item = self.tabela_reserva.topLevelItem(row)
            selecao = item.text(1)
            if pesquisa.lower() in selecao.lower():
                item.setHidden(False)
            else:  # inserted
                item.setHidden(True)

    def reservar_leito(self, acao):
        ala = self.ala
        analise = False
        analise2 = False
        selecionado = []
        selecionado2 = []
        selecao_demanda = self.dados.tabela_dem()
        cont = self.dados.conta_linha()
        for row in range(cont):
            selec = selecao_demanda.item(row, 0)
            if selec.checkState() == QtCore.Qt.CheckState.Checked:
                analise = True
                selecionado.append(row)
        num_linhas = self.tabela_reserva.topLevelItemCount()
        for row in range(num_linhas):
            item = self.tabela_reserva.topLevelItem(row)
            selecao = self.tabela_reserva.itemWidget(item, 0)
            if selecao.isChecked():
                analise2 = True
                selecionado2.append(row)
        if analise and analise2:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('Reservar Leito?')
            icon = QIcon('warning.ico')
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            reply = msg_box.exec()
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                colum_nome = 0
                colum_data_nas = 0
                colum_pronto = 0
                colum_npf = 0
                colum_obs = 0
                for row, raw in zip(selecionado, selecionado2):
                    for colum in range(1, self.dados.tabelademan.columnCount()):
                        item_pac = self.dados.tabelademan.horizontalHeaderItem(colum)
                        if item_pac.text() == 'NOME DO PACIENTE':
                            colum_nome = colum
                        if item_pac.text() == 'DATA DE NASCIMENTO':
                            colum_data_nas = colum
                        if item_pac.text() == 'PRONTUÁRIO':
                            colum_pronto = colum
                        if item_pac.text() == 'NPF':
                            colum_npf = colum
                        if item_pac.text() == 'OBSERVAÇÕES':
                            colum_obs = colum
                    nome = selecao_demanda.item(row, colum_nome)
                    print(nome.text())
                    data_nas = selecao_demanda.item(row, colum_data_nas)
                    pronto = selecao_demanda.item(row, colum_pronto).text()
                    npf = selecao_demanda.item(row, colum_npf).text()
                    print(nome.text(), data_nas, pronto, npf)
                    item = self.tabela_reserva.topLevelItem(raw)
                    leito = item.text(1)
                    status_atual = item.text(2)
                    tipo = item.text(3)
                    obs = selecao_demanda.item(row, colum_obs).text()
                    current_datetime = QDateTime.currentDateTime()
                    formatted_datetime = current_datetime.toString('dd/MM/yyyy hh:mm:ss')
                    status = acao
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    if self.variavel == 0:
                        tabela = 'tabela_demanda_ps'
                        cursor = conexao.cursor()
                        comando = f'UPDATE {tabela} SET STATUS_SOLICITACAO = \"{status}\", LEITO_RESERVADO = \"{leito}\", DATA_HORA_RESERVA = \"{formatted_datetime}\" WHERE NOME = \"{nome.text()}\"'
                        cursor.execute(comando)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                    if self.variavel == 1:
                        tabela = 'alta_cti'
                        cursor = conexao.cursor()
                        comando = f'UPDATE alta_cti SET STATUS_SOLICITACAO = \"{status}\", LEITO_RESERVADO = \"{leito}\", DATA_HORÁRIO_DA_RESERVA = \"{formatted_datetime}\" WHERE NOME_DO_PACIENTE = \"{nome.text()}\"'
                        cursor.execute(comando)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                    if self.variavel == 2:
                        tabela = 'tabela_agenda_bloco_demanda'
                        cursor = conexao.cursor()
                        comando = f'UPDATE tabela_agenda_bloco_demanda SET STATUS_SOLICITACAO = \"{status}\", LEITO_RESERVADO = \"{leito}\", DATA_HORÁRIO_DA_RESERVA = \"{formatted_datetime}\" WHERE NOME_DO_PACIENTE = \"{nome.text()}\"'
                        cursor.execute(comando)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                    if self.variavel == 3:
                        tabela = 'tabela_hemodinamica'
                        cursor = conexao.cursor()
                        comando = f'UPDATE tabela_hemodinamica SET STATUS_SOLICITACAO = \"{status}\", LEITO_RESERVADO = \"{leito}\", DATA_HORÁRIO_DA_RESERVA = \"{formatted_datetime}\" WHERE NOME_DO_PACIENTE = \"{nome.text()}\"'
                        cursor.execute(comando)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                    if self.variavel == 4:
                        tabela = 'tabela_internações_e_transf_externas'
                        cursor = conexao.cursor()
                        comando = f'UPDATE tabela_internações_e_transf_externas SET STATUS_DA_SOLICITAÇÃO = \"{status}\", LEITO_RESERVADO = \"{leito}\", DATA_HORÁRIO_RESERVA = \"{formatted_datetime}\" WHERE NOME_DO_PACIENTE = \"{nome.text()}\"'
                        cursor.execute(comando)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                    if self.variavel == 5:
                        tabela = 'tabela_transferencias_internas'
                        cursor = conexao.cursor()
                        comando = f'UPDATE tabela_transferencias_internas SET STATUS_DA_SOLICITAÇÃO = \"{status}\", LEITO_RESERVADO = \"{leito}\", DATA_E_HORÁRIO_RESERVA = \"{formatted_datetime}\" WHERE NOME_DO_PACIENTE = \"{nome.text()}\"'
                        cursor.execute(comando)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                    if self.variavel == 6:
                        tabela = 'tabela_onco_hemato_ped'
                        cursor = conexao.cursor()
                        comando = f'UPDATE tabela_onco_hemato_ped SET STATUS_SOLICITACAO = \"{status}\", LEITO_RESERVADO = \"{leito}\", DATA_HORÁRIO_RESERVA = \"{formatted_datetime}\" WHERE NOME_DO_PACIENTE = \"{nome.text()}\"'
                        cursor.execute(comando)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    leito = leito.replace(' ', '_')
                    if status_atual!= 'OCUPADO' and 'RESERVA' not in status_atual:
                        print(leito)
                        comando = f'UPDATE GRADE SET SEXO_DA_ENFERMARIA = \"{tipo}\",OBSERVACOES = \"{obs}\",PRONTUARIO = \"{pronto}\",NPF = \"{npf}\",NOME = \"{nome.text()}\", STATUS_DO_LEITO = \"{status}\", DATA_DE_NASCIMENTO = \"{data_nas.text()}\" WHERE idGRADE = \"{leito}\"'
                    else:  # inserted
                        comando = f"INSERT INTO GRADE (SEXO_DA_ENFERMARIA,OBSERVACOES,PRONTUARIO,NPF,idGRADE,NOME,DATA_DE_NASCIMENTO,STATUS_DO_LEITO) VALUES (\"{tipo}\",\"{obs}\",\"{pronto}\",\"{npf}\",\"{leito + '_aguardando'}\",\"{nome.text()}\",\"{data_nas.text()}\", \"RESERVADO\")"
                    cursor.execute(comando)
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    current_datetime = QDateTime.currentDateTime()
                    formatted_date = current_datetime.toString('dd/MM/yyyy')
                    current_datetime = QDateTime.currentDateTime()
                    formatted_time = current_datetime.toString('hh:mm')
                    texto = f'{formatted_time}                LEITO {leito} FOI RESERVADO POR {self.dados.nome_user} PARA {nome.text()} NASCIDO NO DIA {data_nas.text()}'
                    data = formatted_date
                    comando = 'INSERT INTO history (data, histo) VALUES (%s, %s)'
                    valores = (data, texto)
                    cursor.execute(comando, valores)
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Information)
                    msg_box.setWindowTitle('AVISO')
                    msg_box.setText('Rerserva Realizda')
                    icon = QIcon('warning.ico')
                    msg_box.setWindowIcon(icon)
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg_box.exec()
                    self.vagos(ala)
                    self.dados.atualiza_ps(tabela)

    def apagar_leito(self):
        analise = False
        selecionado = []
        num_linhas = self.tabela_reserva.topLevelItemCount()
        for row in range(num_linhas):
            item = self.tabela_reserva.topLevelItem(row)
            selecao = item.checkState(0)
            if selecao == QtCore.Qt.CheckState.Checked:
                analise = True
                selecionado.append(row)
        if analise:
            for row in reversed(selecionado):
                self.tabela_reserva.takeTopLevelItem(row)

    import psycopg2

    def ler_PostgreSQL(self, nome):
        try:
            # Establish connection to the PostgreSQL database
            connection = psycopg2.connect(
                user='ugen_integra',
                password='aghuintegracao',
                host='10.36.2.35',
                port='6544',
                database='dbaghu'
            )
            cursor = connection.cursor()

            # Execute the query
            cursor.execute('SELECT * FROM AGH.AGH_UNIDADES_FUNCIONAIS')
            rows = cursor.fetchall()

            # Iterate through results to find the desired 'nome'
            for row in rows:
                if row[1] == nome:
                    self.codigo_ala = row[0]
                    break  # Stop loop if the matching 'nome' is found

        except psycopg2.Error as e:
            print('Erro ao conectar ao PostgreSQL:', e)

        finally:
            # Ensure resources are released properly
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def vagos(self, ala):
        self.ler_PostgreSQL(ala)
        lista_leitos = []
        connection = psycopg2.connect(user='ugen_integra', password='aghuintegracao', host='10.36.2.35', port='6544', database='dbaghu')
        cursor = connection.cursor()
        cursor.execute('select * from AGH.ain_leitos')
        rows = cursor.fetchall()
        for row in rows:
            if row[6] == self.codigo_ala:
                sem_hifen = row[0].split('-')[0]
                semzero = row[2].lstrip('0')
                dados = f'{sem_hifen}_{semzero}'
                lista_leitos.append(dados)
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        comando = 'SELECT * FROM GRADE '
        cursor.execute(comando)
        leitura = cursor.fetchall()
        self.tabela_reserva.clear()
        self.tabela_reserva.setColumnCount(4)
        self.tabela_reserva.setHeaderLabels(['', 'LEITOS', 'STATUS', 'SEXO DA ENFERMARIA'])
        i = 0
        for linha in leitura:
            if i + 1 < len(leitura):
                proxima_linha = leitura[i + 1]
                if 'aguardando' in str(linha[0]) or 'aguardando' in str(proxima_linha):
                    continue
            if str(linha[0]) not in lista_leitos:
                continue
            item = str(linha[0]).replace('_', ' ')
            self.addTreeItem(i, item, str(linha[10]), str(linha[8]))
            i += 1
        cursor.close()
        conexao.close()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.btn_2leste_3.setText(_translate('Form', '2º LESTE'))
        self.btn_6leste_3.setText(_translate('Form', '6º LESTE'))
        self.btn_UCO_3.setText(_translate('Form', 'UCO'))
        self.btn_CTI_3leste_3.setText(_translate('Form', 'CTI 3º LESTE'))
        self.btn_2sul_3.setText(_translate('Form', '2º SUL'))
        self.btn_8sul_3.setText(_translate('Form', '8º SUL'))
        self.btn_8norte_3.setText(_translate('Form', '8º NORTE'))
        self.btn_CTI_PS_3.setText(_translate('Form', 'CTI PS'))
        self.btn_10norte_3.setText(_translate('Form', '10º NORTE'))
        self.btn_8leste_3.setText(_translate('Form', '8º LESTE'))
        self.btn_7norte_3.setText(_translate('Form', '7º NORTE'))
        self.btn_9leste_3.setText(_translate('Form', '9º LESTE'))
        self.btn_cti_ped_3.setText(_translate('Form', 'CTI PED'))
        self.btn_7leste_3.setText(_translate('Form', '7º LESTE'))
        self.btn_reserva.setText(_translate('Form', 'RESERVAR LEITO'))
        self.btn_ocupa.setText(_translate('Form', 'OCUPAR LEITO'))

    def addTreeItem(self, i, leito, status, tipo):
        item = QtWidgets.QTreeWidgetItem(self.tabela_reserva)
        checkbox = QtWidgets.QCheckBox()
        checkbox.setChecked(False)
        item.setText(1, leito)
        item.setText(2, status)
        item.setText(3, tipo)
        self.tabela_reserva.setItemWidget(item, 0, checkbox)
        checkbox.stateChanged.connect(lambda state, row=i: self.checkboxStateChanged(state, row))
        self.apagar_leito()

    def checkboxStateChanged(self, state, row):
        item = self.tabela_reserva.topLevelItem(row)
        status = item.text(2)
        if status == 'OCUPADO' or 'RESERVA' in status:
            self.btn_ocupa.setEnabled(False)
        else:  # inserted
            self.btn_ocupa.setEnabled(True)
        selected_count = 0
        column = self.tabela_reserva.columnCount()
        quantidade_selecionados_demanda = 0
        selecao_demanda = self.dados.tabela_dem()
        cont = self.dados.conta_linha()
        for row in range(cont):
            selec = selecao_demanda.item(row, 0)
            if selec.checkState() == QtCore.Qt.CheckState.Checked:
                quantidade_selecionados_demanda += 1
        for row in range(self.tabela_reserva.topLevelItemCount()):
            item2 = self.tabela_reserva.topLevelItem(row)
            checkbox = self.tabela_reserva.itemWidget(item2, 0)
            if checkbox.isChecked():
                if selected_count < quantidade_selecionados_demanda:
                    selected_count += 1
        if selected_count == quantidade_selecionados_demanda:
            for i in range(self.tabela_reserva.topLevelItemCount()):
                item = self.tabela_reserva.topLevelItem(i)
                checkbox = self.tabela_reserva.itemWidget(item, 0)
                item.setDisabled(not checkbox.isChecked())
                checkbox.setEnabled(checkbox.isChecked())
        else:  # inserted
            for i in range(0, self.tabela_reserva.topLevelItemCount()):
                item = self.tabela_reserva.topLevelItem(i)
                checkbox = self.tabela_reserva.itemWidget(item, 0)
                item.setDisabled(checkbox.isChecked())
                checkbox.setEnabled(not checkbox.isChecked())

    def conf_layout(self):
        if self.settings.contains('tema'):
            font_name = self.settings.value('font', defaultValue='')
            backcolocor = self.settings.value('tema', defaultValue='')
            color = self.settings.value('color', defaultValue='')
            tamanho = int(self.settings.value('tamanho', defaultValue=10))
        else:  # inserted
            backcolocor = '#5DADE2'
            color = 'Black'
            tamanho = 12
            font_name = 'Segoe UI'
        self.backcolocor = backcolocor
        self.color = color
        self.font = font_name
        self.tamanho = tamanho
        for label in self.frame.findChildren(QtWidgets.QLabel):
            label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name}; border:none')
        self.frame.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;border: 2px solid #2E3D48;border-radius: 10px;')

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