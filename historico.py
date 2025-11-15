import pymysql
import datetime
from PyQt6.QtCore import QDateTime, QSettings, QStandardPaths, QDate
from PyQt6.QtGui import QKeyEvent, QGuiApplication
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QListWidget, QScrollArea, QFrame, QWidget, QVBoxLayout, QLabel, QRadioButton,QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtCore import Qt, QDateTime, QSettings, QStandardPaths
import psycopg2
from PyQt6.QtWidgets import QMessageBox, QCompleter
from datetime import datetime
from database_Demandas import Ui_data_Demanda
from datetime import datetime, timedelta, date
from PyQt6.QtCore import Qt
import csv
import unicodedata
import re
import os
import sys
def resource_path(relative_path):
    """Resolve path para PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Ui_Form(object):
    def __init__(self):
        super().__init__()

    def setupUi(self, Form, tela):
        self.tables_data = []  # List of (titulo_label, tabela_hist, btn_exportar)
        self.current_index = 0
        self.indice = 0
        self.tabela_grade_escolha = False
        self.data_deman = Ui_data_Demanda()
        self.tipo = 'history'
        colo = """
                            QPushButton {

                            background-color: #FFFFFF;
                            color: #2E3D48;
                            border-radius: 10px;
                            border-color: transparent;
                            }
                            QPushButton:hover {
                            background-color: #c0c0c0;
                            color: #000000;
                            }
                            QPushButton:pressed {
                                background-color: #2E3D48;
                                color: #FFFFFF;
                            }
                        """

        self.host_mysql = 'localhost'
        self.user_mysql = ('root',)
        self.password_mysql = 'camileejose'
        self.tela = tela
        Form.setObjectName('Form')
        Form.showMaximized()
        icon = QIcon('imagens/documentario.ico')
        Form.setWindowIcon(icon)
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        screen = QGuiApplication.primaryScreen()
        size = screen.size()
        width = size.width()
        height = size.height() - 10
        size_frame = tela.frame.size()
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setStyleSheet('background-color: #5DADE2;')
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.frame.show()
        posicao = tela.frame.pos()
        x = posicao.x()
        y = 41
        self.frame.setGeometry(QtCore.QRect(x, 40, size_frame.width(), size_frame.height()))
        print(width, height)

        self.lista_titulo = []
        self.lista_ids = []
        for cont, tit in enumerate(self.tela.lista_titulo):
            self.lista_titulo.append(tit)
            self.lista_ids.append(self.tela.lista_ids[cont])

        for cont, tit in enumerate(self.tela.teladem.lista_titulo):
            self.lista_titulo.append(tit)
            self.lista_ids.append(self.tela.teladem.lista_ids[cont])

        self.label_Data = QtWidgets.QLabel('Data de Aniversário:',  parent=self.frame)
        self.label_Data.setGeometry(QtCore.QRect(480, 5, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_Data.setFont(font)
        self.label_Data.setObjectName('label_grupo')

        self.datanas = QtWidgets.QDateEdit(parent=self.frame)
        self.datanas.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.datanas.setGeometry(QtCore.QRect(480, 30, 120, 31))
        ccurrent_datetime = QtCore.QDateTime.currentDateTime()
        tomorrow_datetime = ccurrent_datetime.addDays(1)
        initial_datetime = tomorrow_datetime
        self.datanas.setDateTime(initial_datetime)
        self.datanas.setCalendarPopup(True)
        self.datanas.setObjectName('datanas')

        self.labels_Data = []

        self.pesquisa_historico_nome = QtWidgets.QLineEdit(parent=self.frame)
        self.pesquisa_historico_nome.setGeometry(QtCore.QRect(40, 25, 200, 31))
        self.pesquisa_historico_nome.setAccessibleName('')
        self.pesquisa_historico_nome.setAccessibleDescription('')
        self.pesquisa_historico_nome.setAutoFillBackground(False)
        self.pesquisa_historico_nome.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.pesquisa_historico_nome.setInputMask('')
        self.pesquisa_historico_nome.setText('')
        self.pesquisa_historico_nome.setObjectName('pesquisa_historico')
        self.pesquisa_historico_nome.setPlaceholderText('Pesquisar Nome do Paciente')
        #self.pesquisa_historico_nome.textChanged.connect(self.pesquisar)
        icon = QIcon('imagens/lupa.ico')
        self.pesquisa_historico_nome.addAction(icon, QtWidgets.QLineEdit.ActionPosition.LeadingPosition)


        self.pesquisa_historico_prontu = QtWidgets.QLineEdit(parent=self.frame)
        self.pesquisa_historico_prontu.setGeometry(QtCore.QRect(260, 25, 200, 31))
        self.pesquisa_historico_prontu.setAccessibleName('')
        self.pesquisa_historico_prontu.setAccessibleDescription('')
        self.pesquisa_historico_prontu.setAutoFillBackground(False)
        self.pesquisa_historico_prontu.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.pesquisa_historico_prontu.setInputMask('')
        self.pesquisa_historico_prontu.setText('')
        self.pesquisa_historico_prontu.setObjectName('pesquisa_historico_prontu')
        self.pesquisa_historico_prontu.setPlaceholderText('Pesquisar Prontuário')
        #self.pesquisa_historico_prontu.textChanged.connect(self.pesquisar)
        icon = QIcon('imagens/lupa.ico')
        self.pesquisa_historico_prontu.addAction(icon, QtWidgets.QLineEdit.ActionPosition.LeadingPosition)

        self.table_selector_button = QPushButton(parent=self.frame)
        self.table_selector_button.setGeometry(QtCore.QRect(620, 25, 350, 31))
        self.table_selector_button.setStyleSheet(
            'border: 2px solid white; border-radius: 10px; background-color: white; text-align: left; padding-left: 5px;')
        self.table_selector_button.setText("Todas Tabelas")  # texto inicial
        self.table_selector_button.setEnabled(True)
        self.table_selector_button.show()
        self.table_selector_button.raise_()

        item = 'SELECIONE A TABELA...'

        self.table_selector_button.setText(item)
        # Lista suspensa (oculta por padrão)
        self.table_selector_list = QListWidget(parent=self.frame)
        self.table_selector_list.setGeometry(QtCore.QRect(620, 56, 350, 100))  # abaixo do botão
        self.table_selector_list.setStyleSheet('border: 2px solid white; border-radius: 5px; background-color: white;')
        #self.table_selector_list.addItems(self.tela.lista_titulo)
        self.table_selector_list.raise_()

        # Conectar comportamento
        self.table_selector_button.clicked.connect(
            lambda: self.table_selector_list.setVisible(not self.table_selector_list.isVisible()))
        self.table_selector_list.itemClicked.connect(self.set_table_selection)
        self.table_selector_list.hide()

        self.radio_recente = QRadioButton('Modificação mais Recente', parent=self.frame)
        self.radio_recente.setChecked(False)
        self.radio_antigo = QRadioButton('Modificação mais  Antiga', parent=self.frame)
        self.radio_antigo.setChecked(True)
        self.radio_recente.toggled.connect(self.pesquisar)
        self.radio_antigo.toggled.connect(self.pesquisar)
        self.radio_recente.setGeometry(QtCore.QRect(950, 100, 160, 20))
        self.radio_antigo.setGeometry(QtCore.QRect(1120, 100, 160, 20))
        self.label_ordenar = QtWidgets.QLabel(parent=self.frame)
        self.label_ordenar.setGeometry(QtCore.QRect(900, 70, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_ordenar.setFont(font)
        self.label_ordenar.setObjectName('label_grupo')
        self.btn_filtros = QtWidgets.QPushButton('▼ Selecione uma Data', parent=self.frame)
        self.btn_filtros.setGeometry(QtCore.QRect(990, 20, 150, 23))

        self.btn_pesquisar = QtWidgets.QPushButton('Pesquisar', parent=self.frame)
        self.btn_pesquisar.setGeometry(QtCore.QRect(1160, 20, 150, 35))
        LAYOUT_BTN = """
                                            QPushButton {
                                                background-color: #2E3D48;
                                                color: white;
                                                padding: 8px 16px;
                                                border: 2px solid transparent;
                                                border-radius: 4px;
                                            }
                                            QPushButton:hover {
                                                background-color: #3E4D58;
                                            }
                                            QPushButton:pressed {
                                                background-color: #1E2D38;
                                            }
                                            QPushButton:disabled {
                                                background-color: #666;
                                                color: #ccc;
                                            }
                                        """
        self.btn_pesquisar.setStyleSheet(LAYOUT_BTN)
        self.btn_pesquisar.clicked.connect(self.pesquisar)
        self.btnfechar = QtWidgets.QPushButton(' X ', parent=self.frame)
        self.btn_filtros.setFocus()
        self.btnfechar.setStyleSheet('QPushButton {    border-top-right-radius: 10px;    border-bottom-right-radius: 10px;    border-top-left-radius: 0px;    border-bottom-left-radius: 0px;    background-color: #FFFFFF;    color: #2E3D48;    border: 2px solid #2E3D48;}QPushButton:pressed {    background-color: #2E3D48;    color: #FFFFFF;}')
        current_datetime = QDateTime.currentDateTime()
        formatted_date = current_datetime.toString('yyyy')
        formatted_date2 = current_datetime.addYears((-1)).toString('yyyy')
        self.frame_box = QtWidgets.QFrame(parent=self.frame)
        self.frame_box.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.frame_box.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_box.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_box.setGeometry(QtCore.QRect(990, 43, 150, 125))
        self.frame_personalisa = QtWidgets.QFrame(parent=self.frame)
        self.frame_personalisa.setStyleSheet('\n            QFrame  {\n                background-color: #FFFFFF;\n                border-top-right-radius: 20px;\n                border-bottom-right-radius: 20px;\n                border-left: 1px solid black;\n            }\n        ')
        self.frame_personalisa.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_personalisa.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_personalisa.setObjectName('frame_box')
        self.frame_personalisa.setGeometry(QtCore.QRect(1139, 43, 270, 125))
        ccurrent_datetime = QtCore.QDateTime.currentDateTime()

        # Correção da criação e configuração de frames e widgets
        self.borda_inicio = QtWidgets.QFrame(parent=self.frame_personalisa)
        self.borda_inicio.setStyleSheet('border: 2px solid black; border-radius: 10px; background-color: #FFFFFF;')
        self.borda_inicio.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.borda_inicio.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.borda_inicio.setObjectName('frame')
        self.borda_inicio.setGeometry(QtCore.QRect(8, 25, 140, 29))

        self.data_inicio = QtWidgets.QDateEdit(parent=self.frame_personalisa)
        self.data_inicio.setGeometry(QtCore.QRect(10, 30, 130, 20))
        self.data_inicio.setDateTime(QtCore.QDateTime.currentDateTime())
        self.data_inicio.setCalendarPopup(True)
        self.data_inicio.setStyleSheet('border-color: #FFFFFF; border-radius: 10px; background-color: #FFFFFF;')
        self.data_inicio.setObjectName('data_inicio')

        self.inicio = QtWidgets.QLabel('Depois de ', self.frame_personalisa)
        self.inicio.setStyleSheet('font-size: 13px; margin: 0; padding: 0; border: none; background-color: #FFFFFF')
        self.inicio.setGeometry(15, 20, 63, 13)

        self.borda_fim = QtWidgets.QFrame(parent=self.frame_personalisa)
        self.borda_fim.setStyleSheet('border: 2px solid black; border-radius: 10px; background-color: #FFFFFF;')
        self.borda_fim.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.borda_fim.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.borda_fim.setObjectName('frame')
        self.borda_fim.setGeometry(QtCore.QRect(8, 80, 140, 29))

        # Configuração do botão 'HISTORICO DA GRADE'
        self.bnt_historico_grade =QtWidgets.QPushButton('HISTORICO DA GRADE', parent=self.frame)
        self.bnt_historico_grade.setGeometry(QtCore.QRect(40, 100, 200, 31))
        self.bnt_historico_grade.setObjectName('bnt_historico_grade')
        self.bnt_historico_grade.clicked.connect(self.ativar_historico_grade)
        self.bnt_historico_grade.setStyleSheet(f'''
                    QPushButton {{
                        background-color: #ddd;
                        border: 2px solid #aaa;
                        border-top-left-radius: 10px;
                        border-top-right-radius: 10px;
                        padding: 8px 15px;
                    }}
                    QPushButton:hover {{
                        background-color: #eee;
                    }}
                ''')
        
        # Configuração do botão 'HISTORICO DAS DEMANDAS'
        self.bnt_historico_demanda = QtWidgets.QPushButton('HISTORICO DAS DEMANDAS', parent=self.frame)
        self.bnt_historico_demanda.setGeometry(QtCore.QRect(235, 100, 200, 31))
        self.bnt_historico_demanda.setObjectName('bnt_historico_demanda')
        self.bnt_historico_demanda.clicked.connect(self.ativar_historico_demandas)
        self.bnt_historico_demanda.setStyleSheet(f'''
                                                        QPushButton {{
                                                            background-color: #bbb;
                                                            border: 2px solid #aaa;
                                                            border-top-left-radius: 10px;
                                                            border-top-right-radius: 10px;
                                                            padding: 8px 15px;
                                                        }}
                                                        QPushButton:hover {{
                                                            background-color: #eee;
                                                        }}
                                                    ''')

        self.data_final = QtWidgets.QDateEdit(parent=self.frame_personalisa)
        self.data_final.setGeometry(QtCore.QRect(10, 85, 130, 20))
        self.data_final.setStyleSheet('border-color: #FFFFFF; border-radius: 10px; background-color: #FFFFFF;')
        self.data_final.setDateTime(QtCore.QDateTime.currentDateTime())
        self.data_final.setCalendarPopup(True)
        self.data_final.setObjectName('data_final')

        self.fim = QtWidgets.QLabel('Antes de ', self.frame_personalisa)
        self.fim.setStyleSheet('font-size: 13px; margin: 0; padding: 0; border: none; background-color: #FFFFFF')
        self.fim.setGeometry(15, 75, 57, 13)

        self.aplicar = QtWidgets.QPushButton('Aplicar', self.frame_personalisa)
        self.aplicar.setGeometry(QtCore.QRect(165, 100, 101, 23))
        self.aplicar.clicked.connect(lambda: self.filtros(6))
        self.aplicar.setStyleSheet(
            'QPushButton {border: 2px solid #000000; border-radius: 10px; background-color: #FFFFFF; color: #2E3D48;} QPushButton:pressed {background-color: #2E3D48; color: #FFFFFF;}')

        self.btn_hoje = QtWidgets.QPushButton('Hoje', self.frame_box)
        self.btn_hoje.setGeometry(QtCore.QRect(0, 0, 150, 20))
        self.btn_hoje.setStyleSheet(colo)
        self.btn_hoje.show()

        self.btn_7 = QtWidgets.QPushButton('Últimos 7 dias', self.frame_box)
        self.btn_7.setGeometry(QtCore.QRect(0, 20, 150, 20))
        self.btn_7.setStyleSheet(colo)

        self.btn_30 = QtWidgets.QPushButton('Últimos 30 dias', self.frame_box)
        self.btn_30.setGeometry(QtCore.QRect(0, 40, 150, 20))
        self.btn_30.setStyleSheet(colo)

        self.btn_ano = QtWidgets.QPushButton(f'{formatted_date}', self.frame_box)
        self.btn_ano.setGeometry(QtCore.QRect(0, 60, 150, 20))
        self.btn_ano.setStyleSheet(colo)

        self.btn_2ano = QtWidgets.QPushButton(f'{formatted_date2}', self.frame_box)
        self.btn_2ano.setGeometry(QtCore.QRect(0, 80, 150, 20))
        self.btn_2ano.setStyleSheet(colo)

        self.btn_personalisa = QtWidgets.QPushButton('Período personalizado >', self.frame_box)
        self.btn_personalisa.setStyleSheet(colo)
        self.btn_personalisa.setGeometry(QtCore.QRect(0, 100, 150, 20))

        self.btn_filtros.clicked.connect(self.abrir_items)

        self.btnfechar.setGeometry(QtCore.QRect(1110, 20, 30, 23))
        self.btnfechar.setGeometry(QtCore.QRect(1110, 20, 30, 23))
        # self.btn_7.clicked.connect(lambda: self.filtros(2))
        # self.btn_30.clicked.connect(lambda: self.filtros(3))
        # self.btn_ano.clicked.connect(lambda: self.filtros(4))
        # self.btn_2ano.clicked.connect(lambda: self.filtros(5))
        # self.btn_hoje.clicked.connect(lambda: self.filtros(1))
        self.btnfechar.clicked.connect(lambda: self.filtros(0))
        self.btn_personalisa.clicked.connect(self.abrir_personalisa)
        self.btn_filtros.setStyleSheet("QPushButton {\n"
                                       "                border: 2px solid #2E3D48;\n"
                                       "                border-radius: 10px;\n"
                                       "                background-color: #FFFFFF;\n"
                                       "                color: #2E3D48;\n"
                                       "            }\n"
                                       "            QPushButton:pressed {\n"
                                       "                background-color: #2E3D48;\n"
                                       "                color: #FFFFFF;\n"
                                       "            }")

        self.retranslateUi(Form)



        self.guia = 1
        self.day = "ONTEM"
        #self.atualiza_historico()
        for widget in self.frame.findChildren(QtWidgets.QWidget):
            widget.show()
        self.btnfechar.hide()
        self.frame_personalisa.hide()
        self.frame_box.hide()
        self.btn_voltar = QtWidgets.QPushButton('Voltar', parent=Form)
        self.btn_voltar.setGeometry(QtCore.QRect(1, y, 50, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_voltar.setFont(font)
        self.btn_voltar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_voltar.setStyleSheet("QPushButton{\n"
                                      "background-color: rgb(0, 0, 0);\n"
                                      "    color: rgb(255, 255, 255);\n"
                                      "    border-radius:10px;\n"
                                      "}\n"
                                      "QPushButton:hover{\n"
                                      "    background-color: rgb(255, 255, 255);\n"
                                      "    color: rgb(0, 0, 0);\n"
                                      "}")
        self.btn_voltar.setObjectName("login_2")
        self.btn_voltar.clicked.connect(lambda: self.voltar(Form))
        self.btn_voltar.show()
        self.conf_layout()
        self.table_selector_list.hide()

        self.table_selector_list.raise_()
        self.frame_box.raise_()
        self.frame_personalisa.raise_()

    def voltar(self, Form):
        self.tela.frame.show()
        self.frame.hide()
        self.btn_voltar.hide()
        self.tela.timer.start()
        _translate = QtCore.QCoreApplication.translate
        icon = QIcon('imagens/icone_p_eUO_icon.ico')
        Form.setWindowIcon(icon)
        Form.setWindowTitle(_translate('Form', 'Sistema de Gestão de Leitos'))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'HISTÓRICO'))
        self.label_ordenar.setText(_translate('Form', 'ORDENAR POR: '))

    def obter_dia_semana(self, data):
        dias_da_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
        dia_da_semana = data.weekday()
        return dias_da_semana[dia_da_semana]

    def atualiza_historico(self):
        self.frames = []
        self.labels = []
        self.labels_Data = []
        conexao = pymysql.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        analise = ''
        cursor = conexao.cursor()
        history = self.tipo
        comando = f'SELECT * FROM {history}'
        cursor.execute(comando)
        leitura = cursor.fetchall()
        self.onRadioButtonToggled(leitura)
        leitura = self.leitura
        for linha in leitura:
            for column, valor in enumerate(linha):
                item = QtWidgets.QTableWidgetItem(str(valor))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                if analise!= item.text() and item.text()!= 'None' and (item is not None) and (column == 1):
                    print(analise, item.text())
                    texto = item.text()
                    data_celula = datetime.datetime.strptime(texto, '%d/%m/%Y').date()
                    partes_data = texto.split('/')
                    data_ano_celula = partes_data[(-1)]
                    data_atual = datetime.datetime.now().date()
                    data_atual_ano = str(data_atual.year)
                    data_atual_2ano = str((data_atual - datetime.timedelta(days=365)).year)
                    if self.day == 'HOJE' and data_celula!= data_atual:
                        break
                    if self.day == 'SEMANA' and data_celula < data_atual - datetime.timedelta(days=7):
                        break
                    if self.day == 'MES' and data_celula < data_atual - datetime.timedelta(days=30):
                        break
                    if self.day == 'ANO' and data_ano_celula!= data_atual_ano:
                        break
                    if self.day == '2ANO' and data_ano_celula!= data_atual_2ano:
                        break
                    self.data_inicio1 = datetime.datetime.strptime(self.data_inicio.date().toString('dd/MM/yyyy'), '%d/%m/%Y').date()
                    self.data_final1 = datetime.datetime.strptime(self.data_final.date().toString('dd/MM/yyyy'), '%d/%m/%Y').date()
                    if self.day == 'PERSONALIZADO' and (not self.data_inicio1 <= data_celula <= self.data_final1):
                        frame = QFrame()
                        layout = QVBoxLayout(frame)
                        labels = []
                        continue
                    labels = []
                    frame = QFrame()
                    frame.setFrameShape(QFrame.Shape.Box)
                    frame.setContentsMargins(0, 80, 0, 0)
                    frame.setStyleSheet('QFrame { background-color: white; border: 1px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
                    x = 61
                    self.main_layout.addWidget(frame)
                    print(data_celula, data_atual)
                    if data_celula == data_atual:
                        dia_da_semana = self.obter_dia_semana(data_celula)
                        texto_formatado = f"Hoje - {dia_da_semana}, {data_celula.strftime('%d/%m/%Y')}"
                    else:  # inserted
                        if data_celula == data_atual - datetime.timedelta(days=1):
                            dia_da_semana = self.obter_dia_semana(data_celula)
                            texto_formatado = f"Ontem - {dia_da_semana}, {data_celula.strftime('%d/%m/%Y')}"
                        else:  # inserted
                            dia_da_semana = self.obter_dia_semana(data_celula)
                            texto_formatado = f" {dia_da_semana}, {data_celula.strftime('%d/%m/%Y')}"
                    layout = QVBoxLayout(frame)
                    titulo_label = QtWidgets.QLabel(texto_formatado, frame)
                    titulo_label.setStyleSheet('font-size: 30px; font-weight: bold; margin: 0; padding: 0;border: none;')
                    titulo_label.setGeometry(5, 10, 1000, 40)
                    linha_frame = QFrame(frame)
                    linha_frame.setFrameShape(QFrame.Shape.HLine)
                    linha_frame.setFrameShadow(QFrame.Shadow.Sunken)
                    linha_frame.setStyleSheet('margin: 0; padding: 0; ')
                    linha_frame.setGeometry(0, 60, 3000, 1)
                    self.frames.append((frame, titulo_label))
                    self.labels_Data.append(titulo_label)
                    analise = item.text()
                if column == 2 and item.text()!= 'None' and (item is not None):
                    label = QtWidgets.QLabel(item.text(), frame)
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    label.setFont(font)
                    label.setStyleSheet(' background-color: none; border: none; border-radius: none; box-shadow: none; ')
                    self.labels.append(label)
                    labels.append(label)
                    label.setGeometry(3, x, 3000, 20)
                    x += 20

                    frame.setFixedSize(3000, x)
                if analise == item.text():
                    if column == 2:
                        if item.text()!= 'None':
                            if item is not None:
                                label = QtWidgets.QLabel(item.text(), frame)
                                font = QtGui.QFont()
                                label.setFont(font)
                                label.setStyleSheet(' background-color: none; border: none; border-radius: none; box-shadow: none; ')
                                label
                                label()
                                label.setGeometry(3, x, 3000, 20)
                                x += 20

    def onRadioButtonToggled(self, leitura):
        if self.guia!= 0:
            self.leitura = reversed(leitura)
        self.radio_recente.toggled.connect(lambda checked: self.onRadioRecenteToggled(checked, leitura))
        self.radio_antigo.toggled.connect(lambda checked: self.onRadioAntigoToggled(checked, leitura))

    def onRadioRecenteToggled(self, checked, leitura):
        if checked:
            self.leitura = reversed(leitura)
            for i in reversed(range(self.main_layout.count())):
                widget = self.main_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
            self.guia = 0
            self.atualiza_historico()

    def onRadioAntigoToggled(self, checked, leitura):
        if checked:
            self.leitura = leitura
            for i in reversed(range(self.main_layout.count())):
                widget = self.main_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
            self.guia = 0
            self.atualiza_historico()

    def filtros(self, index):
        self.btn_filtros.setStyleSheet('QPushButton {    border-top-right-radius: 0px;    border-bottom-right-radius: 0px;    border-top-left-radius: 10px;    border-bottom-left-radius: 10px;    background-color: #FFFFFF;    color: #2E3D48;    border: 2px solid black;}QPushButton:pressed {    background-color: #2E3D48;    color: #FFFFFF;}')
        if index == 1:
            self.day = 'HOJE'
            for i in reversed(range(self.main_layout.count())):
                widget = self.main_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
            self.btn_filtros.setText('Hoje')
            self.btn_filtros.setGeometry(QtCore.QRect(990, 20, 120, 23))
            self.btnfechar.show()
            #self.atualiza_historico()
        else:  # inserted
            if index == 2:
                self.day = 'SEMANA'
                for i in reversed(range(self.main_layout.count())):
                    widget = self.main_layout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()
                self.btn_filtros.setText('Ultimos 7 dias')
                self.btn_filtros.setGeometry(QtCore.QRect(990, 20, 120, 23))
                self.btnfechar.show()
                #self.atualiza_historico()
            else:  # inserted
                if index == 3:
                    self.day = 'MES'
                    for i in reversed(range(self.main_layout.count())):
                        widget = self.main_layout.itemAt(i).widget()
                        if widget is not None:
                            widget.deleteLater()
                    self.btn_filtros.setText('Ultimos 30 dias')
                    self.btn_filtros.setGeometry(QtCore.QRect(990, 20, 120, 23))
                    self.btnfechar.show()
                    #self.atualiza_historico()
                else:  # inserted
                    if index == 4:
                        self.day = 'ANO'
                        for i in reversed(range(self.main_layout.count())):
                            widget = self.main_layout.itemAt(i).widget()
                            if widget is not None:
                                widget.deleteLater()
                        current_datetime = QDateTime.currentDateTime()
                        formatted_date = current_datetime.toString('yyyy')
                        self.btn_filtros.setGeometry(QtCore.QRect(990, 20, 120, 23))
                        self.btn_filtros.setText(f'{formatted_date}')
                        self.btnfechar.show()
                        #self.atualiza_historico()
                    else:  # inserted
                        if index == 5:
                            self.day = '2ANO'
                            for i in reversed(range(self.main_layout.count())):
                                widget = self.main_layout.itemAt(i).widget()
                                if widget is None:
                                    continue
                                widget.deleteLater()
                            current_datetime = QDateTime.currentDateTime()
                            formatted_date = current_datetime.addYears((-1)).toString('yyyy')
                            self.btn_filtros.setGeometry(QtCore.QRect(990, 20, 120, 23))
                            self.btn_filtros.setText(f'{formatted_date}')
                            self.btnfechar.show()
                            #self.atualiza_historico()
                        else:  # inserted
                            if index == 6:
                                self.day = 'PERSONALIZADO'
                                self.data_i = self.data_inicio.date()
                                self.data_f = self.data_final.date()
                                for i in reversed(range(self.main_layout.count())):
                                    widget = self.main_layout.itemAt(i).widget()
                                    if widget is not None:
                                        widget.deleteLater()
                                self.btn_filtros.setText('Período personalizado')
                                self.btn_filtros.setGeometry(QtCore.QRect(990, 20, 120, 23))
                                self.btnfechar.show()
                                #self.atualiza_historico()
                            else:  # inserted
                                if index == 0:
                                    self.day = 'ONTEM'
                                    for i in reversed(range(self.main_layout.count())):
                                        widget = self.main_layout.itemAt(i).widget()
                                        if widget is not None:
                                            widget.deleteLater()
                                    self.btn_filtros.setGeometry(QtCore.QRect(990, 20, 150, 23))
                                    self.btn_filtros.setText('▼ Selecione uma Data ')
                                    self.btn_filtros.setStyleSheet('QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')
                                    self.btnfechar.hide()
                                    #self.atualiza_historico()

    def abrir_personalisa(self):
        if self.frame_personalisa.isHidden():
            self.frame_personalisa.show()
            self.frame_box.setStyleSheet('background-color: #FFFFFF; border-top-left-radius: 20px; border-bottom: 1px solid black;')
            self.frame_personalisa.setStyleSheet('\n                        QFrame  {\n                            background-color: #FFFFFF;\n                            border-top-right-radius: 20px;\n                            border-bottom: 1px solid black;\n                            border-left: 1px solid black;\n                        }\n                    ')
        else:  # inserted
            self.frame_personalisa.hide()
            self.frame_box.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
            self.frame_personalisa.setStyleSheet('\n                        QFrame  {\n                            background-color: #FFFFFF;\n                            border-top-right-radius: 20px;\n                            border-bottom-right-radius: 20px;\n                            border-left: 1px solid black;\n                        }\n                    ')

    def abrir_items(self):
        if self.frame_box.isHidden():
            self.frame_box.show()
        else:  # inserted
            self.frame_box.hide()
            if not self.frame_personalisa.isHidden():
                self.frame_personalisa.hide()


    def formartar_texto(self, texto):
        def obter_dia_semana(data):
            dias_semana_pt = {
                'Monday': 'Segunda-feira',
                'Tuesday': 'Terça-feira',
                'Wednesday': 'Quarta-feira',
                'Thursday': 'Quinta-feira',
                'Friday': 'Sexta-feira',
                'Saturday': 'Sábado',
                'Sunday': 'Domingo'
            }
            dia_ingles = data.strftime("%A")
            return dias_semana_pt.get(dia_ingles, dia_ingles)

        if isinstance(texto, str):
            data_celula = datetime.strptime(texto, "%Y-%m-%d").date()
        elif isinstance(texto, date):
            data_celula = texto
        else:
            data_celula = datetime.strptime(str(texto), "%Y-%m-%d").date()

        data_atual = date.today()

        if data_celula == data_atual:
            dia_da_semana = obter_dia_semana(data_celula)
            texto_formatado = f"Hoje - {dia_da_semana}, {data_celula.strftime('%d/%m/%Y')}"
        elif data_celula == data_atual - timedelta(days=1):
            dia_da_semana = obter_dia_semana(data_celula)
            texto_formatado = f"Ontem - {dia_da_semana}, {data_celula.strftime('%d/%m/%Y')}"
        else:
            dia_da_semana = obter_dia_semana(data_celula)
            texto_formatado = f"{dia_da_semana}, {data_celula.strftime('%d/%m/%Y')}"

        return texto_formatado
    def scrol(self):
        screen = QGuiApplication.primaryScreen()
        size = screen.size()
        width = size.width() - 100
        height = size.height() - 220
        self.scroll = QScrollArea(self.frame)
        self.scroll.setWidgetResizable(True)
        self.scroll.setGeometry(QtCore.QRect(39, 130, width, height))
        self.scroll.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: none;')
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.content_widget = QWidget()
        self.scroll.setWidget(self.content_widget)
        self.scroll.show()

        self.main_layout = QVBoxLayout(self.content_widget)

        self.frame_tabela = QFrame()
        self.frame_tabela.setFrameShape(QFrame.Shape.Box)
        self.frame_tabela.setContentsMargins(0, 80, 0, 0)
        self.frame_tabela.setStyleSheet(
            'QFrame { background-color: white; border: 1px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; }'
        )
        LAYOUT_BTN = """
                                                            QPushButton {
                                                                background-color: #2E3D48;
                                                                color: white;
                                                                padding: 8px 16px;
                                                                border: 2px solid transparent;
                                                                border-radius: 4px;
                                                            }
                                                            QPushButton:hover {
                                                                background-color: #3E4D58;
                                                            }
                                                            QPushButton:pressed {
                                                                background-color: #1E2D38;
                                                            }
                                                            QPushButton:disabled {
                                                                background-color: #666;
                                                                color: #ccc;
                                                            }
                                                        """
        self.frame_tabela.show()
        # Layout vertical dentro do frame
        self.frame_layout = QVBoxLayout(self.frame_tabela)

        btn_prev = QtWidgets.QPushButton("Voltar Tabela", self.frame_tabela)
        btn_prev.move(220, 10)
        btn_prev.clicked.connect(lambda: self.show_table(self.current_index - 1 if self.current_index > 0 else 0))
        btn_prev.show()

        btn_next = QtWidgets.QPushButton("Próximo Tabela", self.frame_tabela)
        btn_next.move(350, 10)
        btn_next.clicked.connect(lambda: self.show_table(
            self.current_index + 1 if self.current_index < len(self.tables_data) - 1 else self.current_index))
        btn_next.show()

        btn_next.setStyleSheet(LAYOUT_BTN)
        btn_prev.setStyleSheet(LAYOUT_BTN)

        self.titulo_label = QtWidgets.QLabel("Título da Tabela")
        self.titulo_label.setStyleSheet(
            'font-size: 30px; font-weight: bold; margin: 0; padding: 0; border: none;'
        )
        # self.frame_layout.addWidget(self.titulo_label)

        self.tabela_hist = QtWidgets.QTableWidget()
        self.tabela_hist.setStyleSheet(
            """
            QTableWidget {
                background-color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: #2E3D48;
                color: white;
                padding: 8px;
                font-size: 14px;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: white;
                color: black;
            }
            QTableCornerButton::section {
                width: 0px;
            }
            QScrollBar:vertical {
                background: #2E3D48;
                width: 16px;
                margin: 0px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #1C2A33;
                min-height: 24px;
                border: 2px solid #F0F0F0;
                border-radius: 2px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                subcontrol-origin: margin;
            }
            QScrollBar:horizontal {
                background: #2E3D48;
                height: 16px;
                margin: 0px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background: #1C2A33;
                min-width: 24px;
                border: 2px solid #F0F0F0;
                border-radius: 2px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
                subcontrol-origin: margin;
            }
            """
        )
        # self.frame_layout.addWidget(self.tabela_hist)

        self.main_layout.addWidget(self.frame_tabela)
    def iniciar(self):
        LAYOUT_BTN = """
                                                    QPushButton {
                                                        background-color: #2E3D48;
                                                        color: white;
                                                        border: 2px solid transparent;
                                                        border-radius: 4px;
                                                    }
                                                    QPushButton:hover {
                                                        background-color: #3E4D58;
                                                    }
                                                    QPushButton:pressed {
                                                        background-color: #1E2D38;
                                                    }
                                                    QPushButton:disabled {
                                                        background-color: #666;
                                                        color: #ccc;
                                                    }
                                                """

        btn_exportar = QtWidgets.QPushButton("Exportar Tabela", self.frame_tabela)
        btn_exportar.setFixedWidth(130)
        btn_exportar.setFixedHeight(50)
        btn_exportar.move(10, 10)
        btn_exportar.setStyleSheet(LAYOUT_BTN)

        def exportar_csv():
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                None, "Salvar CSV", f"{titulo_label.text()}.csv", "CSV Files (*.csv)"
            )

            if path:
                with open(path, 'w', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    headers = [tabela_hist.horizontalHeaderItem(i).text() for i in range(tabela_hist.columnCount())]
                    writer.writerow(headers)

                    for row in range(tabela_hist.rowCount()):
                        row_data = []
                        for col in range(tabela_hist.columnCount()):
                            item = tabela_hist.item(row, col)
                            row_data.append(item.text() if item else '')
                        writer.writerow(row_data)

        btn_exportar.clicked.connect(exportar_csv)

        titulo_label = QtWidgets.QLabel("Título da Tabela")
        titulo_label.setStyleSheet(
            'font-size: 15px; font-weight: bold; margin: 0; padding: 0; border: none;'
        )

        self.frame_layout.addWidget(titulo_label)

        tabela_hist = QtWidgets.QTableWidget()
        tabela_hist.setFixedHeight(600)
        tabela_hist.setStyleSheet(
            """
            QTableWidget {
                background-color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: #2E3D48;
                color: white;
                padding: 8px;
                font-size: 14px;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: white;
                color: black;
            }
            QTableCornerButton::section {
                width: 0px;
            }
            QScrollBar:vertical {
                background: #2E3D48;
                width: 16px;
                margin: 0px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #1C2A33;
                min-height: 24px;
                border: 2px solid #F0F0F0;
                border-radius: 2px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                subcontrol-origin: margin;
            }
            QScrollBar:horizontal {
                background: #2E3D48;
                height: 16px;
                margin: 0px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background: #1C2A33;
                min-width: 24px;
                border: 2px solid #F0F0F0;
                border-radius: 2px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
                subcontrol-origin: margin;
            }
            """
        )
        self.frame_layout.addWidget(tabela_hist)

        self.tables_data.append((titulo_label, tabela_hist, btn_exportar))

        # Initially hide all tables
        titulo_label.hide()
        tabela_hist.hide()
        btn_exportar.hide()

        self.table_selector_list.raise_()
        self.frame_box.raise_()
        self.frame_personalisa.raise_()

        return titulo_label, tabela_hist

    import unicodedata
    import re

    def formatar_nome(self,nome_original):
        # Remove acentos
        nome = unicodedata.normalize('NFKD', nome_original)
        nome = nome.encode('ASCII', 'ignore').decode('utf-8')

        # Coloca tudo em minúsculas
        nome = nome.lower()

        # Remove preposições
        preposicoes = [' de ', ' da ', ' do ']
        for prep in preposicoes:
            nome = nome.replace(prep, ' ')

        # Substitui hífens e múltiplos espaços por underscore
        nome = nome.replace('-', ' ')
        nome = re.sub(r'\s+', '_', nome)  # troca múltiplos espaços por um underscore
        nome = re.sub(r'[^a-z0-9_]', '', nome)  # remove qualquer caractere inválido
        return  nome
    def pesquisar(self):
        self.tables_data = []
        self.scrol()
        nome = self.pesquisa_historico_nome.text()
        prontu = self.pesquisa_historico_prontu.text()
        tabela =self.table_selector_button.text()

        print(tabela)
        if self.tabela_grade_escolha == True:
            tabela = self.formatar_nome(tabela)

        else:
            for cont, titulo in enumerate(self.lista_titulo):
                if tabela == titulo:
                    tabela = self.lista_ids[cont]
                    break
            print(tabela, titulo, self.lista_ids[cont])
        current_datetime = QtCore.QDateTime.currentDateTime()
        tomorrow_datetime = current_datetime.addDays(1)
        initial_date = tomorrow_datetime.date()  # pega só a data (QDate)

        data_nasc_obj = self.datanas.date()
        data_nasc = data_nasc_obj.toString('dd/MM/yyyy')
        print(data_nasc_obj, initial_date)

        if data_nasc_obj == initial_date:
            data_nasc = None
        print(data_nasc,initial_date)
        data_filtrada= self.day
        print('HSITOA')

        self.data_i = self.data_inicio.date().toPyDate()
        self.data_f = self.data_final.date().toPyDate()

        leitura = (self.data_deman.ler_historico_por_data(
            tabela, nome, prontu, data_nasc, data_filtrada,self.data_i,
            data_final=self.data_f))

        if len(leitura) > 0:
            leitura_iter = list(leitura.values())

            if self.radio_antigo.isChecked():
                leitura_iter = leitura_iter  # ordem natural (mais antigo primeiro)
            else:
                leitura_iter = reversed(leitura_iter)  # mais recente primeiro

            for idx, registros in enumerate(leitura_iter):
                texto = ''
                titulo_label, tabela_hist = self.iniciar()
                tabela_hist.setRowCount(0)
                row = 0
                print(registros)
                col_offset = 10  # offset para ignorar as primeiras 8 colunas

                # >>> Definir as colunas que não são vazias no cabeçalho
                cabecalho = registros[0]  # primeira linha
                colunas_validas = []
                for idx_col, valor in enumerate(cabecalho[col_offset:]):
                    if valor not in (None, ''):
                        colunas_validas.append((idx_col + col_offset, str(valor)))

                tabela_hist.setColumnCount(len(colunas_validas))

                # >>> Definir o header
                for i, (_, header_text) in enumerate(colunas_validas):
                    header_item = QtWidgets.QTableWidgetItem(header_text)
                    tabela_hist.setHorizontalHeaderItem(i, header_item)
                    tabela_hist.setColumnWidth(i, 200)

                for lin, linha in enumerate(registros):
                    for coluna, valor in enumerate(linha):
                        if valor is None:
                            valor = ''

                        if lin == 0:
                            row = -1
                            continue  # já tratamos o header antes


                        if coluna == 10 and str(valor).isdigit():
                            target_row = int(valor)
                            while row < target_row - 1:
                                tabela_hist.setRowCount(row + 1)
                                for i, (col_real, _) in enumerate(colunas_validas):
                                    item = QtWidgets.QTableWidgetItem('')
                                    tabela_hist.setItem(row, i, item)
                                row += 1

                        if coluna > 10:
                            if row >= tabela_hist.rowCount():
                                tabela_hist.setRowCount(row + 1)

                            # identificar o índice correspondente na tabela (com base nas colunas válidas)
                            col_idx_tabela = None
                            for i, (col_real, _) in enumerate(colunas_validas):
                                if col_real == coluna:
                                    col_idx_tabela = i
                                    break

                            if col_idx_tabela is not None:
                                item = QtWidgets.QTableWidgetItem(str(valor))
                                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                                tabela_hist.setItem(row, col_idx_tabela-1, item)

                        if coluna == 2:
                            texto = self.formartar_texto(valor)
                        if coluna == 7:
                            texto += ' ' + str(valor)
                            titulo_label.setText(texto)

                        if coluna == 9:
                            print('verificando alteração:', valor)
                            alteracao = str(valor).upper()
                            coluna_alteracao = linha[8]  # índice da coluna 9
                            print(alteracao, coluna_alteracao)
                            if alteracao == 'INSERIU':
                                row_idx = int(coluna_alteracao)
                                tabela_hist.setRowCount(row + 1)
                                for col in range(tabela_hist.columnCount()):
                                    item = tabela_hist.item(row_idx, col)
                                    if item is None:
                                        item = QtWidgets.QTableWidgetItem('')
                                        tabela_hist.setItem(row_idx, col, item)
                                    item.setBackground(QtGui.QColor('#c8f7c5'))  # verde claro

                            elif alteracao == 'EDITOU':
                                if coluna_alteracao:
                                    try:
                                        row_idx, col_idx = eval(coluna_alteracao)
                                        item = tabela_hist.item(row_idx, col_idx - 1)
                                        if item is None:
                                            item = QtWidgets.QTableWidgetItem('')
                                            tabela_hist.setItem(row_idx, col_idx - 1, item)
                                        item.setBackground(QtGui.QColor('#fff3b0'))  # amarelo claro
                                    except:
                                        pass

                            elif alteracao == 'EXCLUIU':
                                if coluna_alteracao.isdigit():
                                    row_idx = int(coluna_alteracao)
                                    if row_idx >= tabela_hist.rowCount():
                                        tabela_hist.setRowCount(row_idx + 1)

                                    for col in range(tabela_hist.columnCount()):
                                        item = tabela_hist.item(row_idx, col)
                                        if item is None:
                                            item = QtWidgets.QTableWidgetItem('')
                                            tabela_hist.setItem(row_idx, col, item)

                                        item.setBackground(QtGui.QColor('#f7c5c5'))  # vermelho claro
                                        print(f'Alterado ({row_idx}, {col}):', item.text())
                            else:
                                if coluna_alteracao.isdigit():
                                    row_idx = int(coluna_alteracao)
                                    if row_idx >= tabela_hist.rowCount():
                                        tabela_hist.setRowCount(row_idx + 1)

                                    for col in range(tabela_hist.columnCount()):
                                        item = tabela_hist.item(row_idx, col)
                                        if item is None:
                                            item = QtWidgets.QTableWidgetItem('')
                                            tabela_hist.setItem(row_idx, col, item)

                                        item.setBackground(QtGui.QColor('#fff3b0'))  # vermelho claro
                                        print(f'Alterado ({row_idx}, {col}):', item.text())

                    row += 1

                titulo_label.setStyleSheet('font-size: 15px; font-weight: bold; margin: 0; padding: 0;border: none;')
                titulo_label.show()
                tabela_hist.show()

            self.frame_tabela.show()
            self.show_table(0)


        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('Não existe Nenhum Historico com esse Filtro!')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply = msg_box.exec()
            icon = QIcon(resource_path('imagens/warning.ico'))
            msg_box.setWindowIcon(icon)

        # for frame, titulo in self.frames:
        #     frame_visible = any((text in label.text().lower() and label.text()!= titulo.text() for label in frame.findChildren(QtWidgets.QLabel)))
        #     frame.setVisible(frame_visible)
        #     titulo.setVisible(frame_visible)
        #     labels = []
        #     i = 61
        #     for label in frame.findChildren(QtWidgets.QLabel):
        #         labels.append(label)
        #         if text not in label.text().lower() and label.text()!= titulo.text():
        #             label.setVisible(False)
        #             labels.append(label)
        #         else:  # inserted
        #             label.setVisible(True)
        #             if label.text()!= titulo.text():
        #                 label.move(0, i)
        #                 i += 20
        #     frame.setFixedSize(3000, i)

    def show_table(self, index):
        # Hide all
        for label, table, export_btn in self.tables_data:
            label.hide()
            table.hide()
            export_btn.hide()

        # Show selected
        if 0 <= index < len(self.tables_data):
            label, table, export_btn = self.tables_data[index]
            label.show()
            table.show()
            export_btn.show()
            self.current_index = index

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.btn_filtros.click()

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
            if label not in self.labels_Data:
                label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name};border-top: 0.2px solid white;border-bottom: 0.2px solid white;border-right: 0.2px solid white;border-left: none;')
        self.frame.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;')

    def histo(self, tipo,btn, btn2):
        btn.setStyleSheet(f'''
                            QPushButton {{
                                background-color: #fff;
                                border: 2px solid #ccc;
                                border-top-left-radius: 10px;
                                border-top-right-radius: 10px;
                                padding: 8px 15px;
                            }}
                            QPushButton:hover {{
                                background-color: #eee;
                            }}
                        ''')
        btn2.setStyleSheet(f'''
                                    QPushButton {{
                                        background-color: #ddd;
                                        border: 2px solid #aaa;
                                        border-top-left-radius: 10px;
                                        border-top-right-radius: 10px;
                                        padding: 8px 15px;
                                    }}
                                    QPushButton:hover {{
                                        background-color: #eee;
                                    }}
                                ''')
        self.tipo = tipo
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.atualiza_historico()
        if (tipo == 'history'):
            self.bnt_historico_grade.setStyleSheet(f'''
                            QPushButton {{
                                background-color: #fff;
                                border: 2px solid #ccc;
                                border-top-left-radius: 10px;
                                border-top-right-radius: 10px;
                                padding: 8px 15px;
                            }}
                            QPushButton:hover {{
                                background-color: #eee;
                            }}
                        ''')
            self.bnt_historico_demanda.setStyleSheet(f'''
                                                QPushButton {{
                                                    background-color: #bbb;
                                                    border: 2px solid #aaa;
                                                    border-top-left-radius: 10px;
                                                    border-top-right-radius: 10px;
                                                    padding: 8px 15px;
                                                }}
                                                QPushButton:hover {{
                                                    background-color: #eee;
                                                }}
                                            ''')
        else:
            self.bnt_historico_demanda.setStyleSheet(f'''
                                        QPushButton {{
                                            background-color: #fff;
                                            border: 2px solid #ccc;
                                            border-top-left-radius: 10px;
                                            border-top-right-radius: 10px;
                                            padding: 8px 15px;
                                        }}
                                        QPushButton:hover {{
                                            background-color: #eee;
                                        }}
                                    ''')
            self.bnt_historico_grade.setStyleSheet(f'''
                                                            QPushButton {{
                                                                background-color: #bbb;
                                                                border: 2px solid #aaa;
                                                                border-top-left-radius: 10px;
                                                                border-top-right-radius: 10px;
                                                                padding: 8px 15px;
                                                            }}
                                                            QPushButton:hover {{
                                                                background-color: #eee;
                                                            }}
                                                        ''')
    def ativar_historico_demandas(self):
        self.table_selector_list.clear()
        self.table_selector_list.addItems(self.tela.teladem.lista_titulo)

        self.bnt_historico_demanda.setStyleSheet(f'''
                                    QPushButton {{
                                        background-color: #fff;
                                        border: 2px solid #ccc;
                                        border-top-left-radius: 10px;
                                        border-top-right-radius: 10px;
                                        padding: 8px 15px;
                                    }}
                                    QPushButton:hover {{
                                        background-color: #eee;
                                    }}
                                ''')
        self.bnt_historico_grade.setStyleSheet(f'''
                                            QPushButton {{
                                                background-color: #ddd;
                                                border: 2px solid #aaa;
                                                border-top-left-radius: 10px;
                                                border-top-right-radius: 10px;
                                                padding: 8px 15px;
                                            }}
                                            QPushButton:hover {{
                                                background-color: #eee;
                                            }}
                                        ''')

        self.tabela_grade_escolha = False
    def ativar_historico_grade(self):
        self.bnt_historico_grade.setStyleSheet(f'''
                                    QPushButton {{
                                        background-color: #fff;
                                        border: 2px solid #ccc;
                                        border-top-left-radius: 10px;
                                        border-top-right-radius: 10px;
                                        padding: 8px 15px;
                                    }}
                                    QPushButton:hover {{
                                        background-color: #eee;
                                    }}
                                ''')
        self.bnt_historico_demanda.setStyleSheet(f'''
                                            QPushButton {{
                                                background-color: #ddd;
                                                border: 2px solid #aaa;
                                                border-top-left-radius: 10px;
                                                border-top-right-radius: 10px;
                                                padding: 8px 15px;
                                            }}
                                            QPushButton:hover {{
                                                background-color: #eee;
                                            }}
                                        ''')
        self.table_selector_list.clear()
        self.table_selector_list.addItems(self.tela.lista_titulo)
        self.tabela_grade_escolha = True

    def set_table_selection(self, item):
        self.table_selector_button.setText(item.text())
        self.table_selector_list.hide()
