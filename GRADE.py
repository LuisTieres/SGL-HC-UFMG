from PyQt6.QtGui import QIcon, QPalette, QColor, QPixmap, QGuiApplication
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QCompleter, QMessageBox, QStyledItemDelegate, QComboBox, QLabel, QToolTip, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QScrollArea, QFrame, QWidget, QApplication, QPushButton
from PyQt6.QtCore import QDateTime, Qt, QSettings, QStandardPaths, QFile, QDate
import mysql.connector
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import datetime
import csv
import pyqtgraph as pg
import numpy as np
from openpyxl import Workbook
import os
import re
import psycopg2
from datetime import datetime, timedelta

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class Ui_CTI_PED(QtWidgets.QMainWindow):
    def setupUi_grade(self, Form, para_teladem=None, dept=None, user=None, nome_user=None, MainWindow=None):
        #Dados Bancos Mysql:
        self.host_mysql = 'localhost'
        self.user_mysql = ('root',)
        self.password_mysql = 'camileejose'

        #Manter posição na Tabela
        self.posicao_inicial_row = 0
        self.posicao_inicial_colum = 0
        self.selection = None

        #Dados do usuário
        self.nome_user = nome_user
        self.user = user
        self.dept = dept

        #Informações para configuração da tela
        self.config_Aberta = False
        self.realocar_Aberta = False
        self.procurar_Aberta = False
        self.contas_Aberta = False
        self.conta_do_usuario_Aberta = False
        self.cria_unidade_Aberta = False

        #Dados de layout
        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        self.clicked = False
        self.teladem = para_teladem
        self.monitora = False

        #Form tela principal
        Form.setObjectName('Form')
        Form.showMaximized()
        icon = QIcon('icone_p_eUO_icon.ico')
        Form.setWindowIcon(icon)

        #Cti inicial
        self.ala = "cti ped"
        self.centralwidget = QtWidgets.QWidget(parent=Form)
        self.centralwidget.setObjectName('centralwidget')
        self.form = Form
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName('horizontalLayout')

        #FRAME PRINCIPAL
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setStyleSheet('background-color: #5DADE2;')
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')

        screen = QGuiApplication.primaryScreen()
        size = screen.size()
        width = size.width() - 10
        height = size.height() - 35

        #Frame do relátorio
        self.frame_relatorio = QtWidgets.QFrame(parent=self.frame)
        self.frame_relatorio.setStyleSheet('background-color: #5DADE2;')
        self.frame_relatorio.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_relatorio.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_relatorio.setObjectName('frame')
        self.frame_relatorio.setVisible(False)
        self.frame_relatorio.setGeometry(0, 25, width, height)

        #COMPOSIÇAO DO SENSO
        self.frame_senso = QtWidgets.QFrame(parent=self.frame)
        self.frame_senso.setStyleSheet('background-color: #5DADE2;')
        self.frame_senso.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_senso.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_senso.setObjectName('frame')
        self.frame_senso.setVisible(False)
        self.frame_senso.setGeometry(0, 25, width, height)

        self.btn_dowload_senso = QtWidgets.QPushButton('Baixar Senso', parent=self.frame)
        self.btn_dowload_senso.setGeometry(QtCore.QRect(230, 0, 150, 23))
        self.btn_dowload_senso.hide()
        self.btn_dowload_senso.setToolTip('Baixar Senso')

        self.btn_filtros = QtWidgets.QPushButton('▼ Selecione uma Data ', parent=self.frame)
        self.btn_filtros.setGeometry(QtCore.QRect(80, 0, 150, 23))
        self.btn_filtros.hide()
        self.btn_filtros.setToolTip('Filtros')

        self.btnfechar = QtWidgets.QPushButton(' X ', parent=self.frame)
        self.btnfechar.hide()
        self.btnfechar.setToolTip('Fechar')
        self.btnfechar.setGeometry(QtCore.QRect(190, 0, 30, 23))

        self.frame_personalisa = QtWidgets.QFrame(parent=self.frame)
        self.frame_personalisa.setStyleSheet('\n                            QFrame  {\n                                background-color: #FFFFFF;\n                                border-top-right-radius: 20px;\n                                border-bottom-right-radius: 20px;\n                                border-left: 1px solid black;\n                            }\n                        ')
        self.frame_personalisa.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_personalisa.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_personalisa.setObjectName('frame_box')
        self.frame_personalisa.setGeometry(QtCore.QRect(225, 23, 270, 125))
        self.frame_personalisa.hide()

        self.frame_box = QtWidgets.QFrame(parent=self.frame)
        self.frame_box.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.frame_box.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_box.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_box.setGeometry(QtCore.QRect(80, 23, 150, 125))
        self.frame_box.hide()
        #FIM DO SENSO

        self.horizontalLayout.addWidget(self.frame)
        self.setCentralWidget(self.frame)

        # Sidebar área destinada ao usuário
        screen = QGuiApplication.primaryScreen()
        size = screen.size()

        # Definindo a geometria do sidebar
        sidebar_width = 200
        sidebar_x = size.width() - sidebar_width
        sidebar_y = 40
        sidebar_height = self.height() - sidebar_y
        self.sidebar = QtWidgets.QFrame(parent=Form)
        self.sidebar.setGeometry(sidebar_x, sidebar_y, sidebar_width, sidebar_height)
        self.sidebar.setStyleSheet('border: 2px solid #2E3D48;background-color: #2E86C1; border-radius: 10px;')
        self.sidebar.setVisible(False)

        self.foto_do_usuario = QtWidgets.QLabel(parent=self.sidebar)
        self.foto_do_usuario.setGeometry(QtCore.QRect(10, 10, 145, 121))
        self.foto_do_usuario.setStyleSheet('\nborder: 2px solid #2E3D48;\nborder-radius: 10px;')
        self.foto_do_usuario.setText('')
        self.foto_do_usuario.setObjectName('foto_do_usuario')

        caminho_imagem = 'imagem_do_usuario.png'
        if QFile.exists(caminho_imagem):
            pixmap = QPixmap(caminho_imagem)
            self.foto_do_usuario.setPixmap(pixmap)
            self.foto_do_usuario.setScaledContents(True)

        icon = QtGui.QIcon('do-utilizador.ico')
        pixmap = icon.pixmap(40, 40)
        sidebar_width = 40
        sidebar_x = size.width() - sidebar_width
        sidebar_y = 40

        self.label_icone = ClickableLabel(parent=Form)
        self.label_icone.setPixmap(pixmap)
        self.label_icone.setGeometry(QtCore.QRect(sidebar_x, 3, 40, 40))
        self.label_icone.setStyleSheet('border-radius: 10px;color: black;')
        self.label_icone.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_icone.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)

        tooltip_text = self.nome_user
        self.label_icone.setToolTip(tooltip_text)
        self.label_icone.show()
        self.label_icone.clicked.connect(self.onIconClick)

        icon = QtGui.QIcon('notificacao.ico')
        pixmap = icon.pixmap(25, 25)
        width = size.width() - 99

        self.notificao_label = ClickableLabel(parent=Form)
        self.notificao_label.setPixmap(pixmap)
        self.notificao_label.setGeometry(QtCore.QRect(width, 15, 25, 25))

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor('white'))
        palette.setColor(QPalette.ColorRole.WindowText, QColor('black'))
        QToolTip.setPalette(palette)

        self.notificao_label.setStyleSheet('border-radius: 10px;color: black;')
        self.notificao_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.notificao_label.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)

        tooltip_text = 'Notificações'

        self.notificao_label.setToolTip(tooltip_text)
        self.notificao_label.show()
        width = size.width() - 86

        self.qt_notificao = ClickableLabel(parent=Form)
        self.qt_notificao.setGeometry(QtCore.QRect(width, 15, 20, 20))
        self.qt_notificao.setStyleSheet('background-color: red; color: #FFFFFF; border: 2px solid white; border-radius: 10px;')
        self.qt_notificao.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.qt_notificao.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        self.qt_notificao.hide()

        self.notificao_label.clicked.connect(self.abrir_email)

        self.usuario = QtWidgets.QPushButton('USUÁRIO', self.sidebar)
        self.usuario.clicked.connect(lambda: self.abrir_conta_do_usuario(Form))

        tooltip_text = 'Usuário'
        self.usuario.setToolTip(tooltip_text)
        self.procura_pac = QtWidgets.QPushButton('PROCCURAR PACIENTE', self.sidebar)
        self.procura_pac.clicked.connect(lambda: self.abrir_procura_pac(Form))

        tooltip_text = 'Procurar Paciente'

        self.procura_pac.setToolTip(tooltip_text)
        self.configura = QtWidgets.QPushButton('CONFIGURAÇÕES', self.sidebar)
        self.configura.clicked.connect(lambda: self.abrir_configuracoes(Form))

        #Tipo Admin administra Usuários
        if self.dept == 'Administrador':
            self.usuarios_contas = QtWidgets.QPushButton('USUÁRIOS', self.sidebar)
            self.usuarios_contas.clicked.connect(lambda: self.abrir_contas(Form))
            self.usuarios_contas.setGeometry(10, 350, 180, 30)

            self.criar_nova_unidade = QtWidgets.QPushButton('CRIAR NOVA UNIDADE', self.sidebar)
            self.criar_nova_unidade.clicked.connect(lambda: self.abrir_novas_unidades(Form))
            self.criar_nova_unidade.setGeometry(10, 400, 180, 30)

        self.t = 'Grade'

        # Fazer abreviação do Nome do usuário
        item = self.nome_user
        tamnaho = len(item)
        login = ''
        i = 0
        space_atual = 0
        quantidade_space = 0
        for j in range(tamnaho):
            if item[j] == ' ':
                quantidade_space += 1
        for i in range(tamnaho):
            if item[i]!= ' ' and space_atual == 0 or space_atual == quantidade_space:
                login += item[i]
            if space_atual!= 0 and space_atual!= quantidade_space and (item[i]!= ' ') and (analise == 0):
                login += item[i]
                analise = 1
            if item[i] == ' ':
                login += ' '
                space_atual += 1
                analise = 0
        font = QtGui.QFont()
        font.setPointSize(12)
        self.NOME = QtWidgets.QLabel(login, self.sidebar)
        self.NOME.setFont(font)

        self.NOME.setGeometry(10, 150, 180, 30)
        self.NOME.setStyleSheet('border: 2px solid transparent; border-radius: 10px;')

        self.configura.setGeometry(10, 300, 180, 30)
        self.usuario.setGeometry(10, 200, 180, 30)
        self.procura_pac.setGeometry(10, 250, 180, 30)

        tabela_width = size.width() - 226
        tabela_height = size.height() - 338

        #Tabela Principal

        self.tabela_grade = QtWidgets.QTableWidget(parent=self.frame)
        self.tabela_grade.setGeometry(QtCore.QRect(0, 200, tabela_width, tabela_height))
        self.tabela_grade.setMinimumSize(QtCore.QSize(681, 0))
        self.tabela_grade.setStyleSheet('background-color: rgb(255, 255, 255);gridline-color: black;')
        self.tabela_grade.setObjectName('tabela_grade')
        self.tabela_grade.setColumnCount(13)
        self.tabela_grade.setRowCount(11)
        self.tabela_grade.cellClicked.connect(self.close_frame)

        self.barra = self.tabela_grade.horizontalScrollBar().value()
        self.barra_vertical = self.tabela_grade.verticalScrollBar().value()

        self.tabela_grade.horizontalScrollBar().valueChanged.connect(self.check_scrollbar_value)
        self.tabela_grade.verticalScrollBar().valueChanged.connect(self.check_scrollbar_value)

        self.tabela_alt = QtWidgets.QTableWidget()
        self.tabela_alt2 = QtWidgets.QTableWidget()

        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_grade.setHorizontalHeaderItem(12, item)

        self.tabela_grade.horizontalHeader().setDefaultSectionSize(290)
        self.tabela_grade.horizontalHeader().setMinimumSectionSize(37)
        self.tabela_grade.verticalHeader().setDefaultSectionSize(33)
        self.tabela_grade.verticalHeader().setMinimumSectionSize(20)

        self.tabela_grade.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela_grade.currentCellChanged.connect(self.get_current_position)
        self.tabela_grade.itemSelectionChanged.connect(self.get_current_position)

        screen = QGuiApplication.primaryScreen()
        size = screen.size()

        self.btn_width = size.width() - 216
        conta_linha = self.tabela_grade.rowCount()

        for conta in range(conta_linha):
            selecao = QtWidgets.QTableWidgetItem()
            selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.tabela_grade.setItem(conta, 0, selecao)

        # Titulo do Frame
        self.TITULO_CTI = QtWidgets.QLabel(parent=self.frame)
        self.TITULO_CTI.setGeometry(QtCore.QRect(650, 30, 241, 71))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.TITULO_CTI.setFont(font)
        self.TITULO_CTI.setObjectName('TITULO_CTI_PED')

        #Btns para modifição da tabela
        self.btn_realocar = QtWidgets.QPushButton(parent=self.frame)
        self.btn_realocar.setGeometry(QtCore.QRect(self.btn_width, 240, 210, 31))
        self.btn_realocar.setObjectName('btn_realocar')
        self.btn_realocar.clicked.connect(lambda: self.abrir_realocar(Form))

        self.btn_alterar = QtWidgets.QPushButton(parent=self.frame)
        self.btn_alterar.setGeometry(QtCore.QRect(self.btn_width, 280, 210, 31))
        self.btn_alterar.setObjectName('btn_alterar')
        self.btn_alterar.clicked.connect(self.altera_table)

        self.editable = False

        # Abrir Monitoramento
        self.MONITORAMENTO = QtWidgets.QPushButton(parent=self.frame)
        self.MONITORAMENTO.setGeometry(QtCore.QRect(0, 0, 131, 23))
        self.MONITORAMENTO.setObjectName('MONITORAMENTO')
        self.MONITORAMENTO.clicked.connect(lambda: self.monitoramento(Form))

        # Abrir demandas
        self.DEMANDAS = QtWidgets.QPushButton(parent=self.frame)
        self.DEMANDAS.setGeometry(QtCore.QRect(135, 0, 75, 23))
        self.DEMANDAS.setObjectName('DEMANDAS')
        self.DEMANDAS.clicked.connect(lambda: self.abrir_demanda(Form))

        #Abrir GRADE
        self.GRADE = QtWidgets.QPushButton(parent=self.frame)
        self.GRADE.setGeometry(QtCore.QRect(216, 0, 75, 23))
        self.GRADE.setObjectName('GRADE')
        self.GRADE.clicked.connect(lambda: self.voltar_grade(Form))

        #Abrir Gráficos
        self.GRAFICOS = QtWidgets.QPushButton(parent=self.frame)
        self.GRAFICOS.setGeometry(QtCore.QRect(296, 0, 75, 23))
        self.GRAFICOS.setObjectName('GRAFICOS')

        self.frame_do_grafico = QtWidgets.QFrame(parent=Form)
        self.frame_do_grafico.setGeometry(QtCore.QRect(0, 200, 1500, 1000))
        self.frame_do_grafico.setStyleSheet('background-color: transparent;')
        self.frame_do_grafico.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_do_grafico.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_do_grafico.setObjectName('frame')
        self.frame_do_grafico.hide()

        self.layout = QVBoxLayout(self.frame_do_grafico)
        self.figure, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvas(self.figure)

        self.layout.addWidget(self.canvas)

        self.progress = QtWidgets.QProgressBar(parent=self.frame_do_grafico)
        self.progress.setGeometry(QtCore.QRect(900, 320, 210, 31))
        self.canvas.setMaximumSize(900, 1100)
        self.figure.set_size_inches(6, 9)

        self.GRAFICOS.clicked.connect(lambda: self.abrir_gráficos(Form))

        #Dar alta
        self.btn_alta = QtWidgets.QPushButton(parent=self.frame)
        self.btn_alta.setGeometry(QtCore.QRect(self.btn_width, 320, 210, 31))
        self.btn_alta.setObjectName('btn_alta')
        self.btn_alta.clicked.connect(lambda: self.alta(Form, self.teladem))

        # Pesquisa de pacientes
        self.BARRADEPESQUISA = QtWidgets.QLineEdit(parent=self.frame)
        self.BARRADEPESQUISA.setGeometry(QtCore.QRect(30, 70, 360, 21))
        self.BARRADEPESQUISA.setObjectName('BARRADEPESQUISA')
        self.BARRADEPESQUISA.textChanged.connect(self.pesquisar)
        self.BARRADEPESQUISA.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.BARRADEPESQUISA.setPlaceholderText('Pesquisar Paciente')
        icon = QIcon('lupa.ico')
        self.BARRADEPESQUISA.addAction(icon, QtWidgets.QLineEdit.ActionPosition.LeadingPosition)
        btn_width = size.width() - 236

        #Abrir outras ctis ou enfermarias
        self.scroll_area_btns = QScrollArea(self.frame)
        self.scroll_area_btns.setStyleSheet('border: none;')
        self.scroll_area_btns.setWidgetResizable(True)
        self.scroll_area_btns.setGeometry(QtCore.QRect(0, 135, btn_width, 60))

        # Crie um widget para a área de rolagem
        scroll_content = QWidget()
        self.scroll_area_btns.setWidget(scroll_content)

        # Layout para os botões
        self.button_layout = QHBoxLayout(scroll_content)
        scroll_content.setLayout(self.button_layout)

        self.btn_cti_ped = QtWidgets.QPushButton()
        self.button_layout.addWidget(self.btn_cti_ped)
        self.btn_cti_ped.setFixedSize(81, 21)
        self.btn_cti_ped.setObjectName('btn_cti_ped')
        self.btn_cti_ped.clicked.connect(lambda: self.abri_cti(Form, 'CTI PEDIÁTRICO - 06N'))

        self.btn_2leste = QtWidgets.QPushButton()
        self.btn_2leste.setFixedSize(71, 21)
        self.button_layout.addWidget(self.btn_2leste)
        self.btn_2leste.setObjectName('btn_2leste')
        self.btn_2leste.clicked.connect(lambda: self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 02L'))

        self.btn_CTI_3leste = QtWidgets.QPushButton()
        self.btn_CTI_3leste.setFixedSize(81, 21)
        self.button_layout.addWidget(self.btn_CTI_3leste)
        self.btn_CTI_3leste.setObjectName('btn_CTI_3leste')
        self.btn_CTI_3leste.clicked.connect(lambda: self.abri_cti(Form, 'CTI ADULTO - 03L'))

        self.btn_UCO = QtWidgets.QPushButton()
        self.btn_UCO.setFixedSize(71, 21)
        self.btn_UCO.setObjectName('btn_UCO')
        self.button_layout.addWidget(self.btn_UCO)
        self.btn_UCO.clicked.connect(lambda: self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO CORONARIANA - 03N'))

        self.btn_CTI_PS = QtWidgets.QPushButton()
        self.btn_CTI_PS.setFixedSize(71, 21)
        self.button_layout.addWidget(self.btn_CTI_PS)
        self.btn_CTI_PS.setObjectName('btn_CTI_PS')
        self.btn_CTI_PS.clicked.connect(lambda: self.abri_cti(Form, 'UTI - PRONTO SOCORRO'))

        self.btn_10norte = QtWidgets.QPushButton()
        self.btn_10norte.setFixedSize(71, 21)
        self.button_layout.addWidget(self.btn_10norte)
        self.btn_10norte.setObjectName('btn_10norte')
        self.btn_10norte.clicked.connect(lambda: self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 10N'))

        self.btn_6leste = QtWidgets.QPushButton()
        self.btn_6leste.setFixedSize(71, 21)
        self.button_layout.addWidget(self.btn_6leste)
        self.btn_6leste.setObjectName('btn_6leste')
        self.btn_6leste.clicked.connect(lambda: self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 06L'))

        self.btn_2sul = QtWidgets.QPushButton()
        self.btn_2sul.setFixedSize(71, 21)
        self.button_layout.addWidget(self.btn_2sul)
        self.btn_2sul.setObjectName('btn_2sul')
        self.btn_2sul.clicked.connect(lambda: self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 02S'))

        self.btn_8leste = QtWidgets.QPushButton()
        self.btn_8leste.setFixedSize(71, 21)
        self.button_layout.addWidget(self.btn_8leste)
        self.btn_8leste.setObjectName('btn_8leste')
        self.btn_8leste.clicked.connect(lambda: self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08L'))

        self.btn_8sul = QtWidgets.QPushButton()
        self.btn_8sul.setFixedSize(71, 21)
        self.button_layout.addWidget(self.btn_8sul)
        self.btn_8sul.setObjectName('btn_8sul')
        self.btn_8sul.clicked.connect(lambda: self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08S'))

        self.lista_modificacao = []
        self.btn_7norte = QtWidgets.QPushButton()
        self.btn_7norte.setFixedSize(71, 21)
        self.button_layout.addWidget(self.btn_7norte)
        self.btn_7norte.setObjectName('btn_7norte')
        self.btn_7norte.clicked.connect(lambda: self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 07N'))

        self.btn_7leste = QtWidgets.QPushButton()
        self.btn_7leste.setFixedSize(71, 21)
        self.button_layout.addWidget(self.btn_7leste)
        self.btn_7leste.setObjectName('btn_7leste')
        self.btn_7leste.clicked.connect(lambda: self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 07L'))

        self.btn_9leste = QtWidgets.QPushButton()
        self.btn_9leste.setFixedSize(71, 21)
        self.button_layout.addWidget(self.btn_9leste)
        self.btn_9leste.setObjectName('btn_9leste')
        self.btn_9leste.clicked.connect(lambda: self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 09L'))

        self.btn_8norte = QtWidgets.QPushButton()
        self.btn_8norte.setFixedSize(71, 21)
        self.button_layout.addWidget(self.btn_8norte)
        self.btn_8norte.setObjectName('btn_8norte')
        self.btn_8norte.clicked.connect(lambda: self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08N'))

        self.list_tabela = []

        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        comando = 'SELECT * FROM New_GRADES '
        cursor.execute(comando)
        rows = cursor.fetchall()

        for row in rows:
            tabela = row[1]
            btn = QtWidgets.QPushButton(f'{tabela}')
            btn.setFixedSize(90, 21)
            self.button_layout.addWidget(btn)
            btn.setObjectName(f'{row[1]}')
            self.list_tabela.append(row[1])
            btn.clicked.connect(lambda: self.abri_cti(Form, f'{tabela}'))
        cursor.close()
        conexao.close()

        #Abrir historico
        self.historio = QtWidgets.QPushButton(parent=self.frame)
        self.historio.setGeometry(QtCore.QRect(378, 0, 75, 23))
        self.historio.setObjectName('historio')
        self.historio.clicked.connect(lambda: self.abrir_historico(Form))

        #Abrir painel
        self.painel = QtWidgets.QPushButton('PAINEL', parent=self.frame)
        self.painel.setGeometry(QtCore.QRect(460, 0, 75, 23))
        self.painel.setObjectName('painel')
        self.painel.clicked.connect(lambda: self.abrir_painel(Form))

        #Abrir senso
        self.senso_Aberta = False
        self.senso = QtWidgets.QPushButton('CENSO', parent=self.frame)
        self.senso.setGeometry(QtCore.QRect(540, 0, 75, 23))
        self.senso.setObjectName('SENSO')
        self.senso.clicked.connect(lambda: self.abrir_senso(Form))

        #Abrir relatorio
        self.btn_relatorio = QtWidgets.QPushButton('RELATÓRIO', parent=self.frame)
        self.btn_relatorio.setGeometry(QtCore.QRect(620, 0, 75, 23))
        self.btn_relatorio.setObjectName('RELATORIO')
        self.btn_relatorio.clicked.connect(lambda: self.abri_relatorio(Form))

        #Fechar sgl
        self.SAIR = QtWidgets.QPushButton(parent=self.frame)
        self.SAIR.setGeometry(QtCore.QRect(700, 0, 75, 23))
        self.SAIR.setObjectName('SAIR')
        self.SAIR.clicked.connect(lambda: self.finalizar_operacao(MainWindow))

        self.frame_do_monitoramento = QtWidgets.QFrame(parent=self.frame)
        self.frame_do_monitoramento.setGeometry(QtCore.QRect(0, 240, 1500, 480))
        self.frame_do_monitoramento.setStyleSheet('background-color: transparent;border: 2px solid black;border-radius: 10px;')
        self.frame_do_monitoramento.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_do_monitoramento.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_do_monitoramento.setObjectName('frame')
        self.frame_do_monitoramento.hide()

        width = size.width() - 466

        #Abrir notificações
        self.email = QtWidgets.QFrame(self.frame)
        self.email.setGeometry(width, 40, 400, self.height())
        self.email.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.email.setContentsMargins(0, 80, 0, 0)
        self.email.setStyleSheet('QFrame { background-color: white; border: 1px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        self.email.setVisible(False)

        self.frames = []
        self.frame.mousePressEvent = lambda event: self.toggle_frame_visibility(self.sidebar, self.email)

        self.scrool = QScrollArea(self.email)
        self.scrool.setWidgetResizable(True)
        self.scrool.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: none;')
        self.scrool.setGeometry(3, 42, 394, self.height() - 42)

        self.content_widget = QWidget()
        self.scrool.setWidget(self.content_widget)
        self.main_layout = QVBoxLayout(self.content_widget)
        width = size.width() - 10
        height = size.height() - 100

        self.help_sccrol_painel = False
        self.scroll_painel = QScrollArea(self.frame)
        self.scroll_painel.setWidgetResizable(True)
        self.scroll_painel.setGeometry(QtCore.QRect(0, 25, width, height))
        self.scroll_painel.setStyleSheet('border: none; background-color: none;')
        self.content_widget_painel = QWidget()
        self.scroll_painel.setWidget(self.content_widget_painel)
        self.main_layout_painel = QVBoxLayout(self.content_widget_painel)
        self.scroll_painel.hide()

        titulo_label = QtWidgets.QLabel('Notificações', self.email)
        titulo_label.setStyleSheet('font-size: 50px; margin: 0; padding: 0;border: none;')
        font = titulo_label.font()
        font.setPointSize(20)
        titulo_label.setFont(font)
        titulo_label.setGeometry(20, 5, 400, 20)

        self.msm = QFrame(self.scrool)
        self.msm.setFrameShape(QFrame.Shape.Box)
        self.msm.setFrameShadow(QFrame.Shadow.Plain)
        self.msm.setStyleSheet('background-color: #C0C0C0;')
        self.msm.hide()

        self.fechar = QtWidgets.QPushButton('X', self.email)
        self.fechar.setGeometry(350, 5, 40, 20)
        self.fechar.setToolTip('Fechar')
        self.fechar.clicked.connect(self.abrir_email)
        tooltip_text = 'Fechar'
        self.fechar.setToolTip(tooltip_text)

        linha_frame = QtWidgets.QFrame(self.email)
        linha_frame.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        linha_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        linha_frame.setStyleSheet('margin: 0; padding: 0; ')
        linha_frame.setGeometry(0, 40, 400, 1)

        self.retranslateUi_cti_ped(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.temporizador()
        self.conf_layout()
        self.qt_notificao.clicked.connect(self.abrir_email)
        self.abri_cti(Form, 'CTI PEDIÁTRICO - 06N')

        for row in range(self.tabela_grade.rowCount()):
            selecao = self.tabela_grade.item(row, 0)
            item = self.tabela_grade.verticalHeaderItem(row)
            if 'aguardando' not in item.text() and selecao.checkState() == QtCore.Qt.CheckState.Checked:
                self.timer.stop()
                self.timer_post.stop()
                self.timer_mysql.stop()

        self.tela = 'Grade'
        self.horizontalLayout.addWidget(self.frame)
        Form.setCentralWidget(self.centralwidget)
        self.frame.raise_()

        #Layout dos btns
        for btn in self.frame.findChildren(QtWidgets.QPushButton):
            btn.setStyleSheet('\n                QPushButton {\n                    border: 2px solid #2E3D48;\n                    border-radius: 10px;\n                    background-color: #FFFFFF;\n                    color: #2E3D48;\n                }\n\n                QPushButton:hover {\n                    background-color: #DDDDDD;  /* Change this to your desired hover color */\n                    color: rgb(0, 0, 0);\n                }\n\n                QPushButton:pressed {\n                    background-color: #2E3D48;  /* Change this to your desired pressed color */\n                    color: #FFFFFF;\n                }\n            ')
            tooltip_text = btn.text()
            if btn.text() == 'X':
                tooltip_text = 'Fechar'
            btn.setToolTip(tooltip_text)
        for btn in self.sidebar.findChildren(QtWidgets.QPushButton):
            btn.setStyleSheet('\n                QPushButton {\n                    border: 2px solid #2E3D48;\n                    border-radius: 10px;\n                    background-color: #FFFFFF;\n                    color: #2E3D48;\n                }\n\n                QPushButton:hover {\n                    background-color: #DDDDDD;  /* Change this to your desired hover color */\n                    color: rgb(0, 0, 0);\n                }\n\n                QPushButton:pressed {\n                    background-color: #2E3D48;  /* Change this to your desired pressed color */\n                    color: #FFFFFF;\n                }\n            ')
            tooltip_text = btn.text()
            if btn.text() == 'X':
                tooltip_text = 'Fechar'
            btn.setToolTip(tooltip_text)

        self.atualizar_senso()
        self.atualizar_painel()

        #Configurções para telespectador
        if self.dept == 'Telespectador':
            self.btn_realocar.hide()
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.senso.hide()
            self.btn_relatorio.hide()
            self.SAIR.setGeometry(QtCore.QRect(540, 0, 75, 23))

    # Função ligada ao temporizador para que novo usuário seja aceito pelo admin
    def aceitar_user(self):
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        comando = 'SELECT * FROM cadastros'
        cursor.execute(comando)
        leitura = cursor.fetchall()
        analise = True
        cont = 0
        for linha in leitura:
            if len(linha) > 0 and linha[4] == '0':
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText(f'O usuário com Nome \'{linha[1]}\' e user \'{linha[0]}\' solicita acesso para logar no software. Aceitar?')
                icon = QIcon('warning.ico')
                msg_box.setWindowIcon(icon)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                reply = msg_box.exec()
                if reply == QMessageBox.StandardButton.Yes:
                    comando = f'UPDATE cadastros SET analise = True WHERE user = \"{linha[0]}\"'
                    cursor.execute(comando)
                    conexao.commit()
                if reply == QMessageBox.StandardButton.No:
                    comando = f'DELETE FROM cadastros WHERE user = \"{linha[0]}\"'
                    cursor.execute(comando)
                    conexao.commit()
        cursor.close()
        conexao.close()

    #Sair
    def finalizar_operacao(self, MainWindow):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Sair do Sistema de Gestão de Leitos ?')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.form.close()
            MainWindow.close()


    #abrir procura paciente
    def abrir_procura_pac(self, Form):
        self.sidebar.close()
        self.label_icone.setStyleSheet('border-radius: 10px;')
        from procura_paciente import Ui_Form
        self.procura_paciente = Ui_Form()
        self.procura_paciente.setupUi(Form, self)
        self.procurar_Aberta = True
        self.timer.stop()
        self.timer_post.stop()
        self.timer_mysql.stop()


    #abrir tela incial da grade
    def voltar_grade(self, Form):
        self.TITULO_CTI.show()
        if self.dept!= 'Telespectador':
            self.btn_alterar.show()
            self.btn_alta.show()
            self.btn_realocar.show()
            self.senso.show()
            self.btn_relatorio.show()
        self.tabela_grade.show()
        self.BARRADEPESQUISA.show()
        if self.frame_do_grafico.isVisible():
            self.frame_do_grafico.hide()
        if self.frame_do_monitoramento.isVisible():
            self.monitoramento(Form)

    #abrir historico
    def abrir_historico(self, Form):
        self.timer.stop()
        self.timer_post.stop()
        self.timer_mysql.stop()
        self.timer_email.stop()
        from historico import Ui_Form
        self.historico = Ui_Form()
        self.historico.setupUi(Form, self)
        self.timer.stop()
        self.timer_post.stop()
        self.timer_mysql.stop()


    #abrir monitoramento
    def monitoramento(self, Form):
        if self.frame_do_grafico.isVisible():
            self.frame_do_grafico.hide()
        if not self.frame_do_monitoramento.isVisible():
            if self.codigo_ala == 29:
                self.monitora_cti_ped(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 23:
                self.uco(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 30:
                self.monitora_6_leste(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 36:
                self.monitora_10_norte(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 169:
                self.monitora_cti_ps(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 22:
                self.monitora_2_leste(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 21:
                self.monitora_2_sul(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 32:
                self.monitora_7_leste(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 31:
                self.monitora_7_norte(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 33:
                self.monitora_8_sul(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 34:
                self.monitora_8_leste(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 193:
                self.monitora_8_norte(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 35:
                self.monitora_9_leste(Form, self.frame_do_monitoramento)
            if self.codigo_ala == 24:
                self.monitora_3_leste(Form, self.frame_do_monitoramento)
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
            self.frame_do_monitoramento.show()
        else:  # inserted
            self.monitora = False
            self.frame_do_monitoramento.hide()
            self.TITULO_CTI.show()
            if self.dept!= 'Telespectador':
                self.btn_alterar.show()
                self.btn_alta.show()
                self.btn_realocar.show()
                self.senso.show()
                self.btn_relatorio.show()
            self.tabela_grade.show()
            self.BARRADEPESQUISA.show()
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()

    # Abrir os monitoramentos especificos
    def monitora_cti_ped(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from cti_ped_monitoramento import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_6_leste(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from sexto_LESTE_monitoramento import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_10_norte(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from decimo_NORTE import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_cti_ps(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from cti_ps_monitoramento import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_2_leste(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from segundo_LESTE_monitoramento import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_2_sul(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from segundo_ALA_SUL import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_7_leste(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from setimo_ALA_LESTE import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_7_norte(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from setimo_ALA_NORTE import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_ucp_neo_natal(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from UCP_NEONATAL_monitoramento import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_8_sul(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from oitavo_ALA_SUL import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_10_sul(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from decimo_sul import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_8_leste(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from oitavo_ALA_LESTE import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_8_norte(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from oitavo_ALA_NORTE import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_9_leste(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from nono_LESTE_TRANSPLANTES import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def monitora_3_leste(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from CTIADULTOmonitoramento import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.tabela_grade.hide()
        self.BARRADEPESQUISA.hide()

    def uco(self, Form, frame):
        for widget in self.frame_do_monitoramento.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        from UNIDADECORONARIANAmonitoramento import Ui_Form
        self.MONI = Ui_Form()
        self.MONI.setupUi(Form, frame, self)
        self.monitora = True
        if self.dept!= 'Telespectador':
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_realocar.hide()
        self.BARRADEPESQUISA.hide()
        self.tabela_grade.hide()

    # Funcao ligada ao frame para mover frames
    def mousePressEvent(self, event, label):
        label.mouse_offset = event.pos()

    def mouseMoveEvent(self, event, label):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = label.mapToParent(event.pos() - label.mouse_offset)
            label.move(new_pos)
            x, y = (new_pos.x(), new_pos.y())

    # abrir graficos
    def abrir_gráficos(self, MainWindow):
        if self.frame_do_monitoramento.isVisible():
            self.frame_do_monitoramento.hide()
        if self.frame_do_grafico.isHidden():
            self.frame_do_grafico.show()
            if self.dept!= 'Telespectador':
                self.btn_alterar.hide()
                self.btn_alta.hide()
                self.btn_realocar.hide()
            self.tabela_grade.hide()
            self.BARRADEPESQUISA.hide()
            self.canvas.show()
            self.plot_pie_chart()
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
        else:  # inserted
            self.frame_do_grafico.hide()
            self.tabela_grade.show()
            if self.dept!= 'Telespectador':
                self.btn_alterar.show()
                self.btn_alta.show()
                self.btn_realocar.show()
                self.senso.show()
                self.btn_relatorio.show()
            self.BARRADEPESQUISA.show()

    # configurar gráficos
    def plot_pie_chart(self):
        qt = 0
        self.vago = 0
        self.reservado = 0
        self.ocupado = 0
        self.bloqueado = 0
        for colum in range(self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == 'STATUS DO LEITO':
                break
        for row in range(self.tabela_grade.rowCount()):
            item = self.tabela_grade.verticalHeaderItem(row)
            status = self.tabela_grade.item(row, colum)
            if 'aguardando' in item.text():
                continue
            qt += 1
            if status.text() == 'VAGO':
                self.vago += 1
            if status.text() == 'OCUPADO':
                self.ocupado += 1
            if status.text() == 'RESERVADO':
                self.reservado += 1
            if status.text() == 'BLOQUEADO' or status.text() == 'BLOQUEADO POR FALTA DE FUNCIONÁRIOS' or status.text() == 'PONTUAL - BLOQUEADO POR FALTA DE FUNCIONÁRIOS' or (status.text() == 'BLOQUEADO POR MANUTENÇÃO') or (status.text() == 'BLOQUEADO POR VM/VNI') or (status.text() == 'BLOQUEADO POR OUTROS MOTIVOS'):
                self.bloqueado += 1
        data = [self.reservado, self.vago, self.ocupado, self.bloqueado]
        labels = ['RESERVADOS', 'VAGOS', 'OCUPADOS', 'BLOQUEADOS']
        colors = ['#ffff99', '#99ff99', '#ff9999', '#3399ff']
        filtered_data = [data[i] for i in range(len(data)) if data[i] > 0]
        filtered_labels = [labels[i] for i in range(len(data)) if data[i] > 0]
        filtered_colors = [colors[i] for i in range(len(data)) if data[i] > 0]
        maior_indice = data.index(max(data))
        explode = [0.1 if i == maior_indice else 0 for i in range(len(data))]
        explode = tuple(explode)
        explode = tuple((explode[i] for i in range(len(data)) if data[i] > 0))

        def autopct_format(pct):
            quantidade = int(round(pct / 100.0 * sum(data)))
            return f'{pct:.1f}%\n({quantidade})'
        if qt!= 0:
            self.progress.setFormat('OCUPAÇÃO: {}%'.format(int(self.ocupado * 100 / qt)))
            self.progress.setValue(int(self.ocupado * 100 / qt))
        self.ax.clear()
        self.ax.pie(filtered_data, labels=filtered_labels, colors=filtered_colors, autopct=autopct_format, startangle=90, pctdistance=0.85, explode=explode)
        self.ax.axis('equal')
        self.figure.patch.set_facecolor('none')
        self.ax.figure.set_size_inches(9, 5)
        self.canvas.draw()

    # Função usada para procurar um paciente na tela de procurar paciente
    def selecionar(self, nome, tipo):
        if tipo == 3:
            texto = 'NOME DO PACIENTE'
        if tipo == 1:
            texto = 'PRONTUÁRIO'
        if tipo == 2:
            texto = 'NPF'
        colum = 2
        for colum in range(self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == texto:
                break
        for row in range(self.tabela_grade.rowCount()):
            item = self.tabela_grade.item(row, colum)
            item2 = self.tabela_grade.verticalHeaderItem(row)
            if item is not None:
                if nome.lower() in item.text().lower() or nome.lower() in item2.text().lower():
                    self.tabela_grade.showRow(row)
                else:  # inserted
                    self.tabela_grade.hideRow(row)

    # funções para retornar items, tabela, frames, numero de linhas e colunas
    def item(self, row, col):
        return self.tabela_grade.item(row, col)

    def tabela_grade1(self):
        return self.tabela_grade

    def leito(self, row):
        return self.tabela_grade.verticalHeaderItem(row)

    def retornar_frame(self):
        self.labels = []
        return self.labels

    def conta_linha(self):
        conta_linha = self.tabela_grade.rowCount()
        return conta_linha

    def conta_coluna(self):
        conta_coluna = self.tabela_grade.columnCount()
        return conta_coluna


    #abrir tela de realocação das demandas
    def abrir_realocar(self, Form):
        cont = self.conta_linha()
        analise = False
        for row in range(cont):
            selec = self.tabela_grade.item(row, 0)
            if selec.checkState() == QtCore.Qt.CheckState.Checked:
                analise = True
        if analise == True:
            from realocar_paciente import Ui_Form
            self.realocar = Ui_Form()
            self.realocar.setupUi(Form, self.ala, self)
            self.realocar_Aberta = True
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
        else:  # inserted
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('Nenhum Leito selecionado!')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply = msg_box.exec()
            icon = QIcon('warning.ico')
            msg_box.setWindowIcon(icon)

    def remover_substring(self, string):
        # Define a substring a ser removida
        substring_a_remover = 'grade_tabela_'

        # Verifica se a substring está presente na string
        if substring_a_remover in string:
            # Remove a substring da string
            string_sem_substring = string.replace(substring_a_remover, '')
            return string_sem_substring
        return string
    # Le o dabase PostgreSQL
    def ler_PostgreSQL(self, nome):
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
                f"SELECT seq, descricao, ind_unid_cti, ind_unid_internacao "
                f"FROM AGH.AGH_UNIDADES_FUNCIONAIS WHERE descricao = '{nome}'"
            )
            rows = cursor.fetchall()

            self.lista_sexo = []
            for row in rows:
                self.codigo_ala = row[0]
                self.codigo_cti = False
                if row[3] == 'S' or row[2] == 'S':
                    self.codigo_cti = True

            cursor.execute(
                f"SELECT unf_seq, sexo_determinante, descricao "
                f"FROM agh.ain_quartos WHERE unf_seq = {self.codigo_ala}"
            )
            rows = cursor.fetchall()
            for row in rows:
                self.lista_sexo.append((row[2], row[1]))

        except psycopg2.Error as e:
            print('Erro ao conectar ao PostgreSQL:', e)

        finally:
            if connection:
                cursor.close()
                connection.close()

    # Usa os dados do AGHU para atualizar o databse do SGL
    def atualiza_mysql(self):
        lista_leitos = []
        try:
            connection = psycopg2.connect(user='ugen_integra', password='aghuintegracao', host='10.36.2.35',
                                          port='6544', database='dbaghu')
            cursor = connection.cursor()
            cursor.execute(f'SELECT lto_id, leito FROM AGH.ain_leitos WHERE unf_seq = {self.codigo_ala}')
            rows = cursor.fetchall()
            sexo_leito = 'INDI'

            for row in rows:
                sem_hifen = row[0].split('-')[0]
                semzero = row[1].lstrip('0')
                dados = f'{sem_hifen}_{semzero}'

                for descricao, sexo in self.lista_sexo:
                    if descricao in row[0]:
                        if sexo == 'F':
                            sexo_leito = 'FEMININO'
                            break
                        if sexo == 'M':
                            sexo_leito = 'MASCULINO'
                            break
                        if sexo == 'Q':
                            sexo_leito = 'PEDIÁTRICO'
                lista_leitos.append((dados, sexo_leito))

        except psycopg2.Error as e:
            print('Erro ao conectar ao PostgreSQL:', e)

        finally:
            if connection:
                cursor.close()
                connection.close()

            conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
            cursor = conexao.cursor()

            for leitos, sexo_leito in lista_leitos:
                comando = f'SELECT idGRADE FROM GRADE WHERE idGRADE = \'{leitos}\''
                cursor.execute(comando)
                resultado = cursor.fetchone()

                if not resultado:
                    comando = f'INSERT INTO GRADE (idGRADE) VALUES (\'{leitos}\')'
                    cursor.execute(comando)
                    conexao.commit()

                comando = f'UPDATE GRADE SET SEXO_DA_ENFERMARIA = \"{sexo_leito}\" WHERE idGRADE = \"{leitos}\"'
                cursor.execute(comando)
                conexao.commit()

            cursor.close()
            conexao.close()

    #abrir os cti's e enfermarias
    def abri_cti(self, Form, nome):
        self.tabela_grade.setColumnCount(15)
        self.tabela_grade.setRowCount(11)
        for cont in range(self.tabela_grade.columnCount()):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
            font.setPointSize(8)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tabela_grade.setHorizontalHeaderItem(cont, item)
        self.retranslateUi_CTI(Form)
        self.nome_tabela_post = nome
        self.ler_PostgreSQL(nome)
        self.timer.stop()
        self.timer_post.stop()
        self.timer_mysql.stop()
        self.atualiza_cti()
        text_width = self.fontMetrics().boundingRect(nome).width()
        self.TITULO_CTI.setFixedSize(text_width * 10, 71)
        self.TITULO_CTI.setText(f'{nome}')
        self.timer.stop()
        self.timer_post.stop()
        self.timer_mysql.stop()
        self.temporizador()
        if not self.frame_do_monitoramento.isHidden():
            self.frame_do_monitoramento.hide()
            self.monitoramento(Form)
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
        if not self.frame_do_grafico.isHidden():
            self.canvas.show()
            self.plot_pie_chart()
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()

    #função get_corrent usada para pegar a posicao na tabela
    def get_current_position(self):
        current_item = self.tabela_grade.currentItem()
        if current_item:
            self.posicao_inicial_row = current_item.row()
            self.posicao_inicial_colum = current_item.column()

    #Identifica a movimentação de Leitos
    def ler_movimentacao_post(self):
        lista_leitos_alta = []
        lista_leitos_internacao = []
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
                f"SELECT leitos.lto_id, leitos.unf_seq, leitos.leito, mov.dthr_lancamento, mov.int_seq "
                f"FROM agh.ain_leitos leitos "
                f"INNER JOIN agh.ain_movimentos_internacao mov ON mov.lto_lto_id = leitos.lto_id "
                f"WHERE tmi_seq = 21 OR tmi_seq = 14 AND leitos.unf_seq = {self.codigo_ala} "
                f"ORDER BY seq DESC LIMIT 100"
            )
            rows = cursor.fetchall()
            data_atual = datetime.now()
            data_tres_dias_atras = data_atual - timedelta(days=10)

            for row in rows:
                sem_hifen = row[0].split('-')[0]
                semzero = row[2].lstrip('0')
                dados = f'{sem_hifen}_{semzero}'
                data_fornecida = row[3]
                if data_fornecida > data_tres_dias_atras:
                    lista_leitos_alta.append((dados, row[4]))

            cursor.execute(
                f"SELECT leitos.lto_id, leitos.unf_seq, leitos.leito, mov.dthr_lancamento, mov.int_seq, interna.pac_codigo "
                f"FROM agh.ain_leitos leitos "
                f"INNER JOIN agh.ain_movimentos_internacao mov ON mov.lto_lto_id = leitos.lto_id "
                f"INNER JOIN agh.ain_internacoes interna ON interna.seq = mov.int_seq "
                f"WHERE tmi_seq = 1 AND leitos.unf_seq = {self.codigo_ala} "
                f"ORDER BY mov.seq DESC LIMIT 100"
            )
            rows = cursor.fetchall()

            for row in rows:
                sem_hifen = row[0].split('-')[0]
                semzero = row[2].lstrip('0')
                dados = f'{sem_hifen}_{semzero}'
                data_fornecida = row[3]
                if data_fornecida > data_tres_dias_atras:
                    lista_leitos_internacao.append((dados, row[4], row[5]))

        except psycopg2.Error as e:
            print('Erro ao conectar ao PostgreSQL:', e)

        finally:
            if connection:
                cursor.close()
                connection.close()

        colum_status = 0
        colum_codigo = 0
        colum_npf = 0

        for colum in range(self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == 'STATUS DO LEITO':
                colum_status = colum
            elif item_pac.text() == 'CÓDIGO DE INTERNACAO':
                colum_codigo = colum
            elif item_pac.text() == 'NPF':
                colum_npf = colum

        for row in range(self.tabela_grade.rowCount()):
            status = self.tabela_grade.item(row, colum_status)
            if status is not None and status.text() != 'VAGO' and 'BLOQUEA' not in status.text():
                for leito, codigo in lista_leitos_alta:
                    leito = leito.replace('_', ' ')
                    if leito == self.tabela_grade.verticalHeaderItem(row).text():
                        item = self.tabela_grade.item(row, colum_codigo)
                        if item is not None and item.text() == str(codigo):
                            self.alta_automatica(row)

            if status is not None and status.text() == 'RESERVADO':
                for leito, codigo, codigo_npf in lista_leitos_internacao:
                    leito = leito.replace('_', ' ')
                    if leito == self.tabela_grade.verticalHeaderItem(row).text():
                        item = self.tabela_grade.item(row, colum_npf)
                        if item is not None and item.text() == str(codigo_npf):
                            self.ocupacao_automatica(row, codigo)

        self.atualiza_cti()

    # funcao atualiza_cti atualiza as tabelas
    def atualiza_cti(self):
        for colum in range(self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == 'NPF':
                self.tabela_grade.hideColumn(colum)

        lista_leitos = []
        connection = psycopg2.connect(user='ugen_integra', password='aghuintegracao', host='10.36.2.35', port='6544', database='dbaghu')
        cursor = connection.cursor()
        cursor.execute(f'SELECT lto_id, leito FROM AGH.ain_leitos WHERE unf_seq = {self.codigo_ala}')
        rows = cursor.fetchall()
        for row in rows:
            sem_hifen = row[0].split('-')[0]
            semzero = row[1].lstrip('0')
            dados = f'{sem_hifen}_{semzero}'
            lista_leitos.append(dados)
            dados = dados + '_aguardando'
            lista_leitos.append(dados)
        if self.tabela_grade.currentItem():
            self.selection = (self.tabela_grade.currentRow(), self.tabela_grade.currentColumn())
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        leitos_str = ', '.join([f'\"{leito}\"' for leito in lista_leitos])
        comando = f'SELECT * FROM GRADE WHERE idGRADE IN ({leitos_str})'
        cursor.execute(comando)
        leitura = cursor.fetchall()
        self.tabela_grade.clearContents()
        self.tabela_grade.setRowCount(0)
        row = 0
        for linha in leitura:
            for column, valor in enumerate(linha):
                if column == 0:
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    if item.text() not in lista_leitos:
                        parts = item.text().split('_')
                        new_string = '_'.join(parts[:2])
                        if new_string not in lista_leitos:
                            continue
                    row = self.tabela_grade.rowCount()
                    self.tabela_grade.insertRow(row)
                    item = item.text().replace('_', ' ')
                    item = QtWidgets.QTableWidgetItem(item)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabela_grade.setVerticalHeaderItem(row, item)
                    _translate = QtCore.QCoreApplication.translate
                    self.increase_column_width(0, 16)
                    item_pac = self.tabela_grade.verticalHeaderItem(row)
                    item_pac.setText(_translate('MainWindow', item.text()))
                if column!= 0:
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    if item is None or item.text() == 'None':
                        item = QtWidgets.QTableWidgetItem(str(''))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabela_grade.setItem(row, column, item)
                    Leito = item.text()
        for row in range(self.tabela_grade.rowCount()):
            item = self.tabela_grade.verticalHeaderItem(row)
            excel_blue = QtGui.QColor(255, 255, 255)
            adjusted_color = excel_blue.lighter(100)
            if 'aguardando' in item.text():
                btn_excluir = QtWidgets.QPushButton('X')
                btn_excluir.setStyleSheet('\n                                           QPushButton {\n                                               border: 2px solid #2E3D48;\n                                               border-radius: 10px;\n                                               background-color: transparent;\n                                               color: black;\n                                           }\n                                           QPushButton:pressed {\n                                               background-color: #black;\n                                               color: #FFFFFF;\n                                           }\n                                       ')
                btn_excluir.clicked.connect(lambda _, r=row: self.apagar_linha(r))
                self.tabela_grade.setCellWidget(row, 0, btn_excluir)
            colum_status = 0
            colum_sexo = 0
            for colum in range(self.tabela_grade.columnCount()):
                item_pac = self.tabela_grade.horizontalHeaderItem(colum)
                if item_pac.text() == 'SEXO DA ENFERMARIA':
                    colum_sexo = colum
                if item_pac.text() == 'STATUS DO LEITO':
                    colum_status = colum
            sexo = self.tabela_grade.item(row, colum_sexo)
            status = self.tabela_grade.item(row, colum_status)
            if sexo is not None and sexo.text() == 'MASCULINO':
                for coluna in range(colum_status - 1):
                    item2 = self.tabela_grade.item(row, coluna + 1)
                    if item2 is not None:
                        new_item = QtWidgets.QTableWidgetItem(item2.text())
                        new_item.setBackground(QtGui.QColor(173, 216, 230))
                        new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        self.tabela_grade.setItem(row, coluna + 1, new_item)
                        excel_blue = QtGui.QColor(173, 216, 230)
                        adjusted_color = excel_blue.lighter(100)
            else:  # inserted
                if sexo is not None and sexo.text() == 'FEMININO':
                    for coluna in range(colum_status - 1):
                        item2 = self.tabela_grade.item(row, coluna + 1)
                        if item2 is not None:
                            new_item = QtWidgets.QTableWidgetItem(item2.text())
                            new_item.setBackground(QtGui.QColor(255, 182, 193))
                            new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                            self.tabela_grade.setItem(row, coluna + 1, new_item)
                            excel_blue = QtGui.QColor(255, 182, 193)
                            adjusted_color = excel_blue.lighter(100)
                else:  # inserted
                    if sexo is not None and sexo.text() == 'PEDIÁTRICO':
                        for coluna in range(colum_status - 1):
                            item2 = self.tabela_grade.item(row, coluna + 1)
                            if item2 is not None:
                                new_item = QtWidgets.QTableWidgetItem(item2.text())
                                new_item.setBackground(QtGui.QColor(255, 255, 204))
                                new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                                self.tabela_grade.setItem(row, coluna + 1, new_item)
                                excel_blue = QtGui.QColor(255, 255, 204)
                                adjusted_color = excel_blue.lighter(100)
            if status is not None and status.text() == 'VAGO':
                item2 = self.tabela_grade.item(row, colum_status)
                item2.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                if item2 is not None:
                    new_item = QtWidgets.QTableWidgetItem(item2.text())
                    new_item.setBackground(QtGui.QColor(200, 250, 150))
                    new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabela_grade.setItem(row, colum_status, new_item)
            else:  # inserted
                if status is not None and status.text() == 'OCUPADO':
                    item2 = self.tabela_grade.item(row, colum_status)
                    if item2 is not None:
                        new_item = QtWidgets.QTableWidgetItem(item2.text())
                        new_item.setBackground(QtGui.QColor(255, 0, 0))
                        new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        self.tabela_grade.setItem(row, colum_status, new_item)
                else:  # inserted
                    if status is not None and status.text() == 'BLOQUEADO' or status.text() == 'BLOQUEADO POR FALTA DE FUNCIONÁRIOS' or status.text() == 'PONTUAL - BLOQUEADO POR FALTA DE FUNCIONÁRIOS' or (status.text() == 'BLOQUEADO POR MANUTENÇÃO') or (status.text() == 'BLOQUEADO POR VM/VNI') or (status.text() == 'BLOQUEADO POR OUTROS MOTIVOS'):
                        item2 = self.tabela_grade.item(row, colum_status)
                        if item2 is not None:
                            new_item = QtWidgets.QTableWidgetItem(item2.text())
                            new_item.setBackground(QtGui.QColor(200, 200, 200))
                            new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                            self.tabela_grade.setItem(row, colum_status, new_item)
                    else:  # inserted
                        if status is not None and status.text() == 'RESERVADO':
                            item2 = self.tabela_grade.item(row, colum_status)
                            if item2 is not None:
                                new_item = QtWidgets.QTableWidgetItem(item2.text())
                                r = int('ff', 16)
                                g = int('ff', 16)
                                b = int('99', 16)
                                cor = QColor(r, g, b)
                                new_item.setBackground(cor)
                                new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                                self.tabela_grade.setItem(row, colum_status, new_item)
            if 'aguardando' not in item.text():
                selecao = QtWidgets.QTableWidgetItem()
                selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
                selecao.setBackground(QtGui.QBrush(adjusted_color))
                self.tabela_grade.setItem(row, 0, selecao)

            # Atualiza cor da celula para verde claro se Sim e vermelho claro se Não
            for colum in range(self.tabela_grade.columnCount()):
                dados = self.tabela_grade.item(row, colum).text()
                if dados == 'SIM':
                    new_item = QtWidgets.QTableWidgetItem(dados)
                    excel_color = QtGui.QColor(0, 255, 127)
                    adjusted_color = excel_color.lighter(140)
                    new_item.setBackground(adjusted_color)
                    new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabela_grade.setItem(row, colum, new_item)
                if dados == 'NÃO':
                    new_item = QtWidgets.QTableWidgetItem(dados)
                    excel_color = QtGui.QColor(250, 128, 114)
                    adjusted_color = excel_color.lighter(140)
                    new_item.setBackground(adjusted_color)
                    new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabela_grade.setItem(row, colum, new_item)
        cursor.close()
        conexao.close()
        for colum in range(1, self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum).text()
            text_width = self.fontMetrics().boundingRect(item_pac).width()
            self.increase_column_width(colum, text_width + 100)
        item = self.tabela_grade.item(self.posicao_inicial_row, self.posicao_inicial_colum)
        self.tabela_grade.scrollToItem(item)
        if self.selection:
            row, col = self.selection
            self.tabela_grade.setCurrentCell(row, col)

    #Identifica se o paciente teve alta pelo sistema
    def alta_automatica(self, row):
        colum_nome = 0
        colum_data_nas = 0
        for colum in range(self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == 'NOME DO PACIENTE':
                colum_nome = colum
            if item_pac.text() == 'DATA DE NASCIMENTO':
                colum_data_nas = colum
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        current_datetime = QDateTime.currentDateTime()
        formatted_date = current_datetime.toString('dd/MM/yyyy')
        formatted_time = current_datetime.toString('hh:mm')
        nome = self.tabela_grade.item(row, colum_nome).text()
        DATA = self.tabela_grade.item(row, colum_data_nas).text()
        texto = f'{formatted_time}                AGHU DEU ALTA AO PACIENTE \"{nome}\" NASCIDO NO DIA {DATA}'
        data = formatted_date
        comando = 'INSERT INTO history (data, histo) VALUES (%s, %s)'
        valores = (data, texto)
        cursor.execute(comando, valores)
        conexao.commit()
        cursor.close()
        conexao.close()
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        cursor.execute('SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'GRADE\' ORDER BY ORDINAL_POSITION')
        colunas = [coluna[0] for coluna in cursor.fetchall()]
        for colum in range(1, self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == 'STATUS DO LEITO':
                item_text = 'VAGO'
            else:  # inserted
                if item_pac.text() == 'SEXO DA ENFERMARIA':
                    item_text = self.tabela_grade.item(row, colum).text()
                else:  # inserted
                    item_text = ''
            valor_para_atualizar = item_text
            leito = self.tabela_grade.verticalHeaderItem(row)
            leito = leito.text().replace(' ', '_')
            Comando = f'UPDATE GRADE SET {colunas[colum]} = \"{valor_para_atualizar}\" WHERE idGRADE = \"{leito}\"'
            cursor.execute(Comando)
        conexao.commit()
        cursor.close()
        conexao.close()
        item = self.tabela_grade.verticalHeaderItem(row + 1)
        if item is not None and 'aguardando' in item.text():
            item = self.tabela_grade.verticalHeaderItem(row + 1)
            conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
            leito = self.tabela_grade.verticalHeaderItem(row)
            cursor = conexao.cursor()
            leito = leito.text().replace(' ', '_')
            comando = f'DELETE FROM GRADE WHERE idGRADE = \"{leito}\"'
            cursor.execute(comando)
            conexao.commit()
            comando = f'UPDATE GRADE SET  idGRADE = \"{leito}\"  WHERE idGRADE = \"{leito}_aguardando\"'
            cursor.execute(comando)
            conexao.commit()
            cursor.close()
            conexao.close()

    def ocupacao_automatica(self, row, codigo):
        colum_status = 0
        for colum in range(self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == 'STATUS DO LEITO':
                colum_status = colum
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        leito = self.tabela_grade.verticalHeaderItem(row)
        leito = leito.text().replace(' ', '_')
        Comando = f'UPDATE GRADE SET STATUS_DO_LEITO = \"OCUPADO\", CODIGO_DE_INTERNACAO = {codigo} WHERE idGRADE = \"{leito}\"'
        cursor.execute(Comando)
        item_ocupado = QTableWidgetItem('OCUPADO')
        self.tabela_grade.setItem(row, colum_status, item_ocupado)
        conexao.commit()
        cursor.close()
        conexao.close()

    def alta(self, Form, para_teladem):
        colum_prontuario = 0
        colum_npf = 0
        colum_nome = 0
        colum_data_nas = 0
        for colum in range(self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == 'NPF':
                colum_npf = colum
            if item_pac.text() == 'PRONTUÁRIO':
                colum_prontuario = colum
            if item_pac.text() == 'NOME DO PACIENTE':
                colum_nome = colum
            if item_pac.text() == 'DATA DE NASCIMENTO':
                colum_data_nas = colum
        analise = 0
        selecionado = []
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        cursor.execute('SELECT COUNT(*) FROM alta_cti')
        conta_linha = cursor.fetchone()[0]
        cursor.close()
        conexao.close()
        for row in range(self.tabela_grade.rowCount()):
            selecao = self.tabela_grade.item(row, 0)
            item = self.tabela_grade.verticalHeaderItem(row)
            if 'aguardando' not in item.text():
                if selecao.checkState() == QtCore.Qt.CheckState.Checked:
                    self.timer.stop()
                    self.timer_post.stop()
                    self.timer_mysql.stop()
                    selecionado.append(row)
                analise = 1
        if analise == 1:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('DAR ALTA?')
            icon = QIcon('warning.ico')
            msg_box.setWindowIcon(icon)
            btn_Enfermaria = None
            if self.codigo_cti == True:
                btn_Enfermaria = msg_box.addButton('Para Demanda Altas Cti\'s', QMessageBox.ButtonRole.YesRole)
            btn_Casa = msg_box.addButton('Para Casa', QMessageBox.ButtonRole.NoRole)
            cancel_button = msg_box.addButton('Cancelar', QMessageBox.ButtonRole.RejectRole)
            msg_box.setDefaultButton(btn_Casa)
            msg_box.exec()
            if msg_box.clickedButton() == btn_Enfermaria:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText('Alta para Enfermaria')
                icon = QIcon('warning.ico')
                msg_box.setWindowIcon(icon)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.exec()
                for row in reversed(selecionado):
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    cursor.execute('SELECT COUNT(*) FROM alta_cti')
                    conta_linha = cursor.fetchone()[0]
                    cursor.close()
                    conexao.close()
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    nome = self.tabela_grade.item(row, colum_nome)
                    data_nasc = self.tabela_grade.item(row, colum_data_nas)
                    pronto = self.tabela_grade.item(row, colum_prontuario).text()
                    npf = self.tabela_grade.item(row, colum_npf).text()
                    current_datetime = QDateTime.currentDateTime()
                    formatted_date = current_datetime.toString('dd/MM/yyyy')
                    formatted_time = current_datetime.toString('hh:mm:ss')
                    leitos = self.tabela_grade.verticalHeaderItem(row)
                    LEITOS = leitos.text()
                    comando = f'INSERT INTO alta_cti (PRONTUARIO,NPF,idnew_table_alta_cti, DATA_DA_ALTA,HORA_DE_SOLICITACAO_DA_ALTA,NOME_DO_PACIENTE, DATA_DE_NASCIMENTO, UNIDADE_DE_INTERNAÇÃO_ATUAL, STATUS_DAS_ALTAS, LEITO_ATUAL) VALUES (\"{pronto}\",\"{npf}\",\"{conta_linha + 1}\",\"{formatted_date}\",\"{formatted_time}\",\"{nome.text()}\", \"{data_nasc.text()}\", \"{self.nome_tabela_post}\", \"PRÉ ALTA\", \"{LEITOS}\")'
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
                    texto = f'{formatted_time}                {self.nome_user} ADCIONOU O PACIENTE {nome.text()} NASCIDO NO DIA {data_nasc.text()} NAS DEMANDAS ALTAS CTI'
                    data = formatted_date
                    comando = 'INSERT INTO history (data, histo) VALUES (%s, %s)'
                    valores = (data, texto)
                    cursor.execute(comando, valores)
                    conexao.commit()
                    cursor.close()
                    conexao.close()
            if msg_box.clickedButton() == btn_Casa:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText('Confirmar ALTA PARA CASA?')
                icon = QIcon('warning.ico')
                msg_box.setWindowIcon(icon)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                reply = msg_box.exec()
                if reply == QMessageBox.StandardButton.Yes:
                    for row in reversed(selecionado):
                        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                        cursor = conexao.cursor()
                        current_datetime = QDateTime.currentDateTime()
                        formatted_date = current_datetime.toString('dd/MM/yyyy')
                        formatted_time = current_datetime.toString('hh:mm')
                        nome = self.tabela_grade.item(row, colum_nome)
                        texto = f'{formatted_time}                {self.nome_user} DEU ALTA AO PACIENTE \"{nome}\" NASCIDO NO DIA {data_nasc}'
                        data = formatted_date
                        comando = 'INSERT INTO history (data, histo) VALUES (%s, %s)'
                        valores = (data, texto)
                        cursor.execute(comando, valores)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                        cursor = conexao.cursor()
                        cursor.execute('SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'GRADE\' ORDER BY ORDINAL_POSITION')
                        colunas = [coluna[0] for coluna in cursor.fetchall()]
                        for colum in range(1, self.tabela_grade.columnCount()):
                            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
                            if item_pac.text() == 'STATUS DO LEITO':
                                item_text = 'VAGO'
                            else:
                                if item_pac.text() == 'SEXO DA ENFERMARIA':
                                    item_text = self.tabela_grade.item(row, colum).text()
                                else:
                                    item_text = ''
                            item_copy = QtWidgets.QTableWidgetItem(item_text)
                            self.tabela_grade.setItem(row, colum, item_copy)
                            valor_para_atualizar = item_text
                            leito = self.tabela_grade.verticalHeaderItem(row)
                            leito = leito.text().replace(' ', '_')
                            Comando = f'UPDATE GRADE SET {colunas[colum]} = \"{valor_para_atualizar}\" WHERE idGRADE = \"{leito}\"'
                            cursor.execute(Comando)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                        item = self.tabela_grade.verticalHeaderItem(row + 1)
                        if item is not None and 'aguardando' in item.text():
                            for row in reversed(selecionado):
                                item = self.tabela_grade.verticalHeaderItem(row + 1)
                                conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                                leito = self.tabela_grade.verticalHeaderItem(row)
                                cursor = conexao.cursor()
                                leito = leito.text().replace(' ', '_')
                                comando = f'DELETE FROM GRADE WHERE idGRADE = \"{leito}\"'
                                cursor.execute(comando)
                                conexao.commit()
                                comando = f'UPDATE GRADE SET  idGRADE = \"{leito}\"  WHERE idGRADE = \"{leito}_aguardando\"'
                                cursor.execute(comando)
                                conexao.commit()
                                cursor.close()
                                conexao.close()
            self.abri_cti(self.form, self.nome_tabela_post)

    def temporizador(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(60000)
        self.timer.timeout.connect(self.atualiza_cti)
        self.timer.start()
        self.timer_email = QtCore.QTimer()
        self.timer_email.setInterval(60000)
        self.indices = []
        self.timer_email.timeout.connect(self.adicionar_email)
        self.timer_email.start()
        if self.dept == 'Administrador':
            self.time_user = QtCore.QTimer()
            self.time_user.setInterval(2000)
            self.time_user.timeout.connect(self.aceitar_user)
            self.time_user.start()
        self.timer_post = QtCore.QTimer()
        self.timer_post.setInterval(300000)
        self.timer_post.timeout.connect(self.ler_movimentacao_post)
        self.timer_post.start()
        self.timer_mysql = QtCore.QTimer()
        self.timer_mysql.setInterval(300000)
        self.timer_mysql.timeout.connect(self.atualiza_mysql)
        self.timer_mysql.start()

    #copiadora função auxliar para copiar a tabela em momentos necessários

    def copiadora(self):
        conta_linha = self.tabela_grade.rowCount()
        conta_coluna = self.tabela_grade.columnCount()
        self.tabela_alt.setColumnCount(conta_coluna)
        self.tabela_alt.setRowCount(conta_linha)
        for analisa_linha in range(conta_linha):
            for analisa_coluna in range(conta_coluna):
                item = self.tabela_grade.item(analisa_linha, analisa_coluna)
                if item is not None:
                    item_text = item.text()
                    item_copy = QtWidgets.QTableWidgetItem(item_text)
                    self.tabela_alt.setItem(analisa_linha, analisa_coluna, item_copy)
            leitos = self.tabela_grade.verticalHeaderItem(analisa_linha)
            leitos = QtWidgets.QTableWidgetItem(leitos.text())
            self.tabela_alt.setVerticalHeaderItem(analisa_linha, leitos)
        for analisa_coluna in range(conta_coluna):
            item = self.tabela_grade.horizontalHeaderItem(analisa_coluna)
            item = QtWidgets.QTableWidgetItem(item.text())
            self.tabela_alt.setHorizontalHeaderItem(analisa_coluna, item)

    def copiadora2(self):
        conta_linha = self.tabela_grade.rowCount()
        conta_coluna = self.tabela_grade.columnCount()
        self.tabela_alt2.setColumnCount(conta_coluna)
        self.tabela_alt2.setRowCount(conta_linha)
        for analisa_linha in range(conta_linha):
            for analisa_coluna in range(conta_coluna):
                item = self.tabela_grade.item(analisa_linha, analisa_coluna)
                if item is not None:
                    item_text = item.text()
                    item_copy = QtWidgets.QTableWidgetItem(item_text)
                    self.tabela_alt2.setItem(analisa_linha, analisa_coluna, item_copy)

    def abrir_demanda(self, Form):
        self.janela_demanda = QtWidgets.QMainWindow()
        self.teladem.setupUi(self.janela_demanda, self.dept, self.user, self.nome_user)
        self.janela_demanda.show()
        self.timer.stop()
        self.timer_post.stop()
        self.timer_mysql.stop()
        Form.close()

    # Procura o paciente no aghu
    def procurar_paciente(self):
        import psycopg2
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
                'select codigo, prontuario, nome, dt_nascimento from agh.aip_pacientes order by codigo desc limit 2000')
            rows = cursor.fetchall()

            # Inicialização das listas
            self.lista_prontuario = []
            self.lista_nome = []
            self.lista_npf = []
            self.lista_data_nascimento = []

            # Iteração para extrair os dados
            for row in rows:
                if row[1] is not None:
                    self.lista_prontuario.append(row[1])
                    self.lista_nome.append(row[2])
                    self.lista_npf.append(row[0])
                    self.lista_data_nascimento.append(row[3])

            # Convertendo listas para strings
            self.lista_prontuario = [str(item) for item in self.lista_prontuario]
            self.lista_npf = [str(item) for item in self.lista_npf]

        except psycopg2.Error as e:
            print('Erro ao conectar ao PostgreSQL:', e)

    def prontu_text(self, text, row, colum_nome, colum_data_nas, colum_npf):
        self.data_nas_dateEdit = self.tabela_grade.cellWidget(row, colum_data_nas)
        self.line_edit_npf = self.tabela_grade.cellWidget(row, colum_npf)
        if text in self.lista_prontuario:
            posicao = self.lista_prontuario.index(text)
            nome = self.lista_nome[posicao] if self.lista_nome[posicao] is not None else 'N/A'
            item = QtWidgets.QTableWidgetItem(str(nome))
            self.tabela_grade.setItem(row, colum_nome, item)
            npf = self.lista_npf[posicao] if self.lista_npf[posicao] is not None else 'N/A'
            self.line_edit_npf.setText(npf)
            data_nasc = self.lista_data_nascimento[posicao]
            if data_nasc is not None:
                ano = data_nasc.year
                mes = data_nasc.month
                dia = data_nasc.day
                self.data_nas_dateEdit.setDate(QtCore.QDate(ano, mes, dia))
            else:  # inserted
                ccurrent_datetime = QtCore.QDateTime.currentDateTime()
                tomorrow_datetime = ccurrent_datetime.addDays(30000)
                initial_datetime = tomorrow_datetime
                self.data_nas_dateEdit.setDateTime(initial_datetime)
        else:  # inserted
            item = QtWidgets.QTableWidgetItem(str(''))
            self.tabela_grade.setItem(row, colum_nome, item)
            self.line_edit_npf.clear()
            self.data_nas_dateEdit.setDate(QtCore.QDate())
            ccurrent_datetime = QtCore.QDateTime.currentDateTime()
            tomorrow_datetime = ccurrent_datetime.addDays(30000)
            initial_datetime = tomorrow_datetime
            self.data_nas_dateEdit.setDateTime(initial_datetime)

    def npf_text(self, text, row, colum_nome, colum_data_nas, colum_pronto):
        self.data_nas_dateEdit = self.tabela_grade.cellWidget(row, colum_data_nas)
        self.line_edit_prontuario = self.tabela_grade.cellWidget(row, colum_pronto)
        if text in self.lista_npf:
            posicao = self.lista_npf.index(text)
            nome = self.lista_nome[posicao] if self.lista_nome[posicao] is not None else 'N/A'
            item = QtWidgets.QTableWidgetItem(str(nome))
            self.tabela_grade.setItem(row, colum_nome, item)
            prontuario = self.lista_prontuario[posicao] if self.lista_prontuario[posicao] is not None else 'N/A'
            print(prontuario)
            self.line_edit_prontuario.setText(prontuario)
            data_nasc = self.lista_data_nascimento[posicao]
            if data_nasc is not None:
                ano = data_nasc.year
                mes = data_nasc.month
                dia = data_nasc.day
                self.data_nas_dateEdit.setDate(QtCore.QDate(ano, mes, dia))
            else:  # inserted
                ccurrent_datetime = QtCore.QDateTime.currentDateTime()
                tomorrow_datetime = ccurrent_datetime.addDays(30000)
                initial_datetime = tomorrow_datetime
                self.data_nas_dateEdit.setDateTime(initial_datetime)
        else:  # inserted
            item = QtWidgets.QTableWidgetItem(str(''))
            self.tabela_grade.setItem(row, colum_nome, item)
            self.line_edit_prontuario.clear()
            ccurrent_datetime = QtCore.QDateTime.currentDateTime()
            tomorrow_datetime = ccurrent_datetime.addDays(30000)
            initial_datetime = tomorrow_datetime
            self.data_nas_dateEdit.setDateTime(initial_datetime)

    def altera_table(self):
        self.copiadora()
        _translate = QtCore.QCoreApplication.translate
        self.procurar_paciente()
        if self.tabela_grade.rowCount() > 0:
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
            self.btn_alterar.setText(_translate('Form', 'CONCLUIR ALTERAÇÃO'))
            self.editable = not self.editable
            self.tabela_grade.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.AllEditTriggers if self.editable else QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
            colum_sexo = 0
            colum_status = 0
            colum_prontuario = 0
            colum_npf = 0
            colum_obs = 0
            colum_nome = 0
            colum_data_nas = 0
            colum_tipo_leito = 0
            colum_previsao_alta = 0
            colum_data_atualizao_status = 0
            colum_solicitante = 0
            colum_pergunta_reserva_comunicada = 0
            colum_reserva_comunicada_a_quem = 0
            colum_codigo = 0
            list_colum = []
            for colum in range(self.tabela_grade.columnCount()):
                item_pac = self.tabela_grade.horizontalHeaderItem(colum)
                if item_pac.text() == 'NPF':
                    colum_npf = colum
                if item_pac.text() == 'CÓDIGO DE INTERNACAO':
                    colum_codigo = colum
                    list_colum.append(colum)
                if item_pac.text() == 'SEXO DA ENFERMARIA':
                    colum_sexo = colum
                if item_pac.text() == 'STATUS DO LEITO':
                    colum_status = colum
                if item_pac.text() == 'PRONTUÁRIO':
                    colum_prontuario = colum
                if item_pac.text() == 'OBSERVAÇÕES':
                    colum_obs = colum
                    list_colum.append(colum)
                if item_pac.text() == 'NOME DO PACIENTE':
                    colum_nome = colum
                    list_colum.append(colum)
                if item_pac.text() == 'DATA DE NASCIMENTO':
                    colum_data_nas = colum
                if item_pac.text() == 'TIPO DE LEITO':
                    colum_tipo_leito = colum
                if item_pac.text() == 'PREVISÃO DE ALTA':
                    colum_previsao_alta = colum
                if item_pac.text() == 'DATA E HORA DE ATUALIZAÇÃO DO STATUS':
                    colum_data_atualizao_status = colum
                if item_pac.text() == 'SOLICITANTE':
                    colum_solicitante = colum
                    list_colum.append(colum)
                if item_pac.text() == 'RESERVA COMUNICADA AO ANDAR?':
                    colum_pergunta_reserva_comunicada = colum
                    list_colum.append(colum)
                if item_pac.text() == 'RESERVA COMUNICADA À: NOME/DATA E HORÁRIO:':
                    colum_reserva_comunicada_a_quem = colum
                    list_colum.append(colum)
            if self.editable:
                for btn in self.frame.findChildren(QtWidgets.QPushButton):
                    if btn!= self.btn_alterar:
                        btn.setEnabled(False)
                self.label_icone.setEnabled(False)
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText('A tabela está habilitada para edição')
                icon = QIcon('warning.ico')
                msg_box.setWindowIcon(icon)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.exec()
                for row in range(self.tabela_grade.rowCount()):
                    if colum_previsao_alta!= 0:
                        item = self.tabela_grade.item(row, colum_previsao_alta)
                        if item is not None:
                            date = item.text()
                        date = ''
                        self.previsao_alta_dateEdit = QtWidgets.QDateEdit()
                        self.previsao_alta_dateEdit.setCalendarPopup(True)
                        self.previsao_alta_dateEdit.setDate(QDate.fromString(date, 'dd/MM/yyyy'))
                        self.tabela_grade.setCellWidget(row, colum_previsao_alta, self.previsao_alta_dateEdit)
                    if colum_tipo_leito!= 0:
                        self.combo_box_tipo_leito = QComboBox()
                        item = self.tabela_grade.item(row, colum_tipo_leito)
                        if item is not None:
                            self.combo_box_tipo_leito.addItem(item.text())
                            self.combo_box_tipo_leito.addItem('BERÇO')
                            self.combo_box_tipo_leito.addItem('CAMA')
                        self.tabela_grade.setCellWidget(row, colum_tipo_leito, self.combo_box_tipo_leito)
                    if colum_data_nas!= 0:
                        item = self.tabela_grade.item(row, colum_data_nas)
                        if item is not None:
                            date = item.text()
                            self.data_nas_dateEdit = QtWidgets.QDateEdit()
                            self.data_nas_dateEdit.setCalendarPopup(True)
                            self.data_nas_dateEdit.setDate(QDate.fromString(date, 'dd/MM/yyyy'))
                            self.tabela_grade.setCellWidget(row, colum_data_nas, self.data_nas_dateEdit)
                    if colum_data_atualizao_status!= 0:
                        item = self.tabela_grade.item(row, colum_data_atualizao_status)
                        if item is not None:
                            date = item.text()
                            self.data_atualizao_status_dateEdit = QtWidgets.QDateTimeEdit()
                            self.data_atualizao_status_dateEdit.setCalendarPopup(True)
                            self.data_atualizao_status_dateEdit.setDate(QDate.fromString(date, 'dd/MM/yyyy HH:mm'))
                            self.tabela_grade.setCellWidget(row, colum_data_atualizao_status, self.data_atualizao_status_dateEdit)
                    if colum_status!= 0:
                        self.combo_box = QComboBox()
                        item = self.tabela_grade.item(row, colum_status)
                        if item is not None:
                            self.combo_box.addItem(item.text())
                            self.combo_box.addItem('VAGO')
                            self.combo_box.addItem('RESERVADO')
                            self.combo_box.addItem('OCUPADO')
                            self.combo_box.addItem('BLOQUEADO')
                            self.combo_box.addItem('ALTA CONFIRMADA')
                            self.combo_box.addItem('BLOQUEADO POR FALTA DE FUNCIONÁRIOS')
                            self.combo_box.addItem('PONTUAL - BLOQUEADO POR FALTA DE FUNCIONÁRIOS')
                            self.combo_box.addItem('BLOQUEADO POR MANUTENÇÃO')
                            self.combo_box.addItem('BLOQUEADO POR VM/VNI')
                            self.combo_box.addItem('BLOQUEADO POR OUTROS MOTIVOS')
                            self.combo_box.addItem('DESATIVADO')
                            self.combo_box.addItem('TRANSFERÊNCIA INTERNA')
                            self.combo_box.addItem('NÃO MONITORADO')
                        self.tabela_grade.setCellWidget(row, colum_status, self.combo_box)
                    if colum_sexo!= 0:
                        self.combo_box2 = QComboBox()
                        item = self.tabela_grade.item(row, colum_sexo)
                        if item is None:
                            self.combo_box2.addItem('PEDIÁTRICO')
                            self.combo_box2.addItem('FEMININO')
                            self.combo_box2.addItem('MASCULINO')
                            self.combo_box2.addItem('INDIFERENTE')
                            self.combo_box2.addItem('MISTA')
                        if item is not None:
                            self.combo_box2.addItem(item.text())
                            if item.text() == ' ' or item.text() == '':
                                self.combo_box2.addItem('PEDIÁTRICO')
                                self.combo_box2.addItem('FEMININO')
                                self.combo_box2.addItem('MASCULINO')
                                self.combo_box2.addItem('INDIFERENTE')
                                self.combo_box2.addItem('MISTA')
                            if item.text() == 'PEDIÁTRICO':
                                self.combo_box2.addItem('FEMININO')
                                self.combo_box2.addItem('MASCULINO')
                                self.combo_box2.addItem('INDIFERENTE')
                                self.combo_box2.addItem('MISTA')
                            if item.text() == 'FEMININO':
                                self.combo_box2.addItem('PEDIÁTRICO')
                                self.combo_box2.addItem('MASCULINO')
                                self.combo_box2.addItem('INDIFERENTE')
                                self.combo_box2.addItem('MISTA')
                            if item.text() == 'MASCULINO':
                                self.combo_box2.addItem('PEDIÁTRICO')
                                self.combo_box2.addItem('FEMININO')
                                self.combo_box2.addItem('INDIFERENTE')
                                self.combo_box2.addItem('MISTA')
                            if item.text() == 'INDIFERENTE':
                                self.combo_box2.addItem('PEDIÁTRICO')
                                self.combo_box2.addItem('FEMININO')
                                self.combo_box2.addItem('MASCULINO')
                                self.combo_box2.addItem('MISTA')
                            if item.text() == 'MISTA':
                                self.combo_box2.addItem('PEDIÁTRICO')
                                self.combo_box2.addItem('FEMININO')
                                self.combo_box2.addItem('MASCULINO')
                                self.combo_box2.addItem('INDIFERENTE')
                        self.tabela_grade.setCellWidget(row, colum_sexo, self.combo_box2)
                    if colum_prontuario!= 0:
                        completer = QCompleter(self.lista_prontuario)
                        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                        self.line_edit_npf = QtWidgets.QLineEdit()
                        item = self.tabela_grade.item(row, colum_npf)
                        self.line_edit_npf.setText(item.text())
                        self.line_edit_prontuario = QtWidgets.QLineEdit()
                        item = self.tabela_grade.item(row, colum_prontuario)
                        self.line_edit_prontuario.setText(item.text())
                        self.line_edit_prontuario.setCompleter(completer)
                        self.line_edit_prontuario.textChanged.connect(lambda text, row1=row, nome=colum_nome, data=colum_data_nas, col_npf=colum_npf: self.prontu_text(text, row1, nome, data, col_npf))
                        self.tabela_grade.setCellWidget(row, colum_prontuario, self.line_edit_prontuario)
                    if colum_npf!= 0:
                        completer1 = QCompleter(self.lista_npf)
                        completer1.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                        self.line_edit_npf.setCompleter(completer1)
                        self.line_edit_npf.textChanged.connect(lambda text, row1=row, nome=colum_nome, data=colum_data_nas, colum_pronto=colum_prontuario: self.npf_text(text, row1, nome, data, colum_pronto))
                        self.tabela_grade.setCellWidget(row, colum_npf, self.line_edit_npf)
                    for colum in range(self.tabela_grade.columnCount()):
                        if colum in list_colum and colum!= 0:
                            item = self.tabela_grade.item(row, colum)
                            line_edit = QtWidgets.QLineEdit()
                            line_edit.setText(item.text())
                            self.tabela_grade.setCellWidget(row, colum, line_edit)
                    for l in list_colum:
                        print(l)
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText('Confirmar Alteração ?')
                icon = QIcon('warning.ico')
                msg_box.setWindowIcon(icon)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                reply = msg_box.exec()
                self.btn_alterar.setText(_translate('Form', 'ALTERAR TABELA'))
                if reply == QMessageBox.StandardButton.No:
                    for row in range(self.tabela_grade.rowCount()):
                        self.combo_box = self.tabela_grade.cellWidget(row, colum_status)
                        self.combo_box2 = self.tabela_grade.cellWidget(row, colum_sexo)
                        self.combo_box.deleteLater()
                        self.combo_box2.deleteLater()
                if reply == QMessageBox.StandardButton.Yes:
                    for row in range(self.tabela_grade.rowCount()):
                        combo_box = self.tabela_grade.cellWidget(row, colum_status)
                        if combo_box is not None:
                            combo_box = self.tabela_grade.cellWidget(row, colum_status)
                            item_text = combo_box.currentText()
                            item = QTableWidgetItem(item_text)
                            status = item.text()
                        else:  # inserted
                            status = 'VAGO'
                        combo_box = self.tabela_grade.cellWidget(row, colum_sexo)
                        if combo_box is not None:
                            item_text = combo_box.currentText()
                            item2 = QTableWidgetItem(item_text)
                            sexo = item2.text()
                        else:  # inserted
                            sexo = 'PEDIÁTRICO'
                        leitos = self.tabela_grade.verticalHeaderItem(row)
                        LEITOS = leitos.text()
                        nome_item = self.tabela_grade.cellWidget(row, colum_nome)
                        data_nasc = self.tabela_grade.cellWidget(row, colum_data_nas)
                        obs = self.tabela_grade.cellWidget(row, colum_obs)
                        npf = self.tabela_grade.cellWidget(row, colum_npf)
                        prontuario = self.tabela_grade.cellWidget(row, colum_prontuario)
                        tipo_leito = self.tabela_grade.cellWidget(row, colum_tipo_leito)
                        previsao_alta = self.tabela_grade.cellWidget(row, colum_previsao_alta)
                        data_atualizao_status = self.tabela_grade.cellWidget(row, colum_data_atualizao_status)
                        solicitante = self.tabela_grade.cellWidget(row, colum_solicitante)
                        pergunta_reserva_comunicada = self.tabela_grade.cellWidget(row, colum_pergunta_reserva_comunicada)
                        reserva_comunicada_a_quem = self.tabela_grade.cellWidget(row, colum_reserva_comunicada_a_quem)
                        TIPO = tipo_leito.currentText()
                        codigo = self.tabela_grade.cellWidget(row, colum_codigo)
                        self.alt_banco(codigo, prontuario, npf, obs, status, nome_item, data_nasc, sexo, LEITOS, previsao_alta, data_atualizao_status, solicitante, pergunta_reserva_comunicada, reserva_comunicada_a_quem, TIPO)
                        self.tabela_grade.setItem(row, colum_status, item)
                        self.tabela_grade.setItem(row, colum_sexo, item2)
                    for row in range(self.tabela_grade.rowCount()):
                        if colum_previsao_alta!= 0:
                            self.previsao_alta_dateEdit = self.tabela_grade.cellWidget(row, colum_previsao_alta)
                            self.previsao_alta_dateEdit.close()
                        if colum_tipo_leito!= 0:
                            self.combo_box_tipo_leito = self.tabela_grade.cellWidget(row, colum_tipo_leito)
                            self.combo_box_tipo_leito.close()
                        if colum_data_nas!= 0:
                            self.data_nas_dateEdit = self.tabela_grade.cellWidget(row, colum_data_nas)
                            self.data_nas_dateEdit.close()
                        self.combo_box = self.tabela_grade.cellWidget(row, colum_status)
                        self.combo_box2 = self.tabela_grade.cellWidget(row, colum_sexo)
                        self.combo_box.close()
                        self.combo_box2.close()
                    for row in range(len(self.lista_modificacao)):
                        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                        cursor = conexao.cursor()
                        current_datetime = QDateTime.currentDateTime()
                        formatted_date = current_datetime.toString('dd/MM/yyyy')
                        texto = self.lista_modificacao[row]
                        data = formatted_date
                        comando = 'INSERT INTO history (data, histo) VALUES (%s, %s)'
                        valores = (data, texto)
                        cursor.execute(comando, valores)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText('Alteração Concluída com Sucesso!')
                icon = QIcon('warning.ico')
                msg_box.setWindowIcon(icon)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply = msg_box.exec()
                for btn in self.frame.findChildren(QtWidgets.QPushButton):
                    if btn!= self.btn_alterar:
                        btn.setEnabled(True)
                self.label_icone.setEnabled(True)
                self.modificao()
                self.abri_cti(self.form, self.nome_tabela_post)

    def alt_banco_nova_tabela(self):
        lista = []
        for colum in range(1, self.tabela_grade.columnCount()):
            item = self.tabela_grade.horizontalHeaderItem(colum)
            if item is not None:
                item_novo = item.text()
                for row in range(self.tabela_grade.rowCount()):
                    LEITO = self.tabela_grade.verticalHeaderItem(row).text()
                    item = self.tabela_grade.item(row, colum)
                    if item is not None:
                        lista.append((item_novo.replace(' ', '_'), item.text(), LEITO))
        try:
            conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
            cursor = conexao.cursor()
            for coluna, valor, LEITO in lista:
                comando = f'UPDATE GRADE SET {coluna} = \"{valor}\" WHERE idGRADE = \"{LEITO}\"'
                cursor.execute(comando)
                conexao.commit()
            conexao.close()
        except mysql.connector.Error as error:
            print('Erro ao conectar ao MySQL:', error)

    def pesquisar(self, pesquisa):
        self.timer.stop()
        self.timer_post.stop()
        self.timer_mysql.stop()
        colum_nome = 7
        for colum in range(self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == 'NOME DO PACIENTE':
                colum_nome = colum
        for row in range(self.tabela_grade.rowCount()):
            item = self.tabela_grade.item(row, colum_nome)
            item2 = self.tabela_grade.verticalHeaderItem(row)
            if item is not None:
                if pesquisa.lower() in item.text().lower() or pesquisa.lower() in item2.text().lower():
                    self.tabela_grade.showRow(row)
                else:  # inserted
                    self.tabela_grade.hideRow(row)
        self.timer.start()
        self.timer_post.start()
        self.timer_mysql.start()

    def retranslateUi_cti_ped(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'Sistema de Gestão de Leitos'))
        item = self.tabela_grade.horizontalHeaderItem(0)
        item.setText(_translate('Form', ' '))
        item = self.tabela_grade.horizontalHeaderItem(1)
        item.setText(_translate('Form', 'PRONTUÁRIO'))
        item = self.tabela_grade.horizontalHeaderItem(2)
        item.setText(_translate('Form', 'NPF'))
        item = self.tabela_grade.horizontalHeaderItem(4)
        item.setText(_translate('Form', 'NOME DO PACIENTE'))
        item = self.tabela_grade.horizontalHeaderItem(7)
        item.setText(_translate('Form', 'DATA DE NASCIMENTO'))
        item = self.tabela_grade.horizontalHeaderItem(5)
        item.setText(_translate('Form', 'SEXO DA ENFERMARIA'))
        item = self.tabela_grade.horizontalHeaderItem(3)
        item.setText(_translate('Form', 'OBSERVAÇÕES'))
        item = self.tabela_grade.horizontalHeaderItem(6)
        item.setText(_translate('Form', 'PREVISÃO DE ALTA'))
        item = self.tabela_grade.horizontalHeaderItem(8)
        item.setText(_translate('Form', 'STATUS DO LEITO'))
        item = self.tabela_grade.horizontalHeaderItem(9)
        item.setText(_translate('Form', 'DATA E HORA DE ATUALIZAÇÃO DO STATUS'))
        item = self.tabela_grade.horizontalHeaderItem(10)
        item.setText(_translate('Form', 'SOLICITANTE'))
        item = self.tabela_grade.horizontalHeaderItem(11)
        item.setText(_translate('Form', 'RESERVA COMUNICADA AO ANDAR?'))
        item = self.tabela_grade.horizontalHeaderItem(12)
        item.setText(_translate('Form', 'RESERVA COMUNICADA À: NOME/DATA E HORÁRIO:'))
        self.TITULO_CTI.setText(_translate('Form', 'CTI PEDIATRICO'))
        if self.dept!= 'Telespectador':
            self.btn_realocar.setText(_translate('Form', 'REALOCAR PACIENTE DAS DEMANDAS'))
            self.btn_alterar.setText(_translate('Form', 'ALTERAR A GRADE DE LEITOS'))
            self.btn_alta.setText(_translate('Form', 'SOLICITAR ALTA'))
        self.usuario.setText(_translate('Form', 'USUÁRIO'))
        self.procura_pac.setText(_translate('Form', 'PROCURAR PACIENTE'))
        self.MONITORAMENTO.setText(_translate('Form', 'MONITORAMENTO'))
        self.DEMANDAS.setText(_translate('Form', 'DEMANDAS'))
        self.GRADE.setText(_translate('Form', 'GRADE'))
        self.GRAFICOS.setText(_translate('Form', 'GRÁFICOS'))
        self.btn_cti_ped.setText(_translate('Form', 'CTI PED'))
        self.btn_2leste.setText(_translate('Form', '2º LESTE'))
        self.btn_CTI_3leste.setText(_translate('Form', 'CTI 3º LESTE'))
        self.btn_UCO.setText(_translate('Form', 'UCO'))
        self.btn_CTI_PS.setText(_translate('Form', 'CTI PS'))
        self.btn_10norte.setText(_translate('Form', '10º NORTE'))
        self.btn_6leste.setText(_translate('Form', '6º LESTE'))
        self.btn_2sul.setText(_translate('Form', '2º SUL'))
        self.btn_8leste.setText(_translate('Form', '8º LESTE'))
        self.btn_8sul.setText(_translate('Form', '8º SUL'))
        self.btn_7norte.setText(_translate('Form', '7º NORTE'))
        self.btn_7leste.setText(_translate('Form', '7º LESTE'))
        self.btn_9leste.setText(_translate('Form', '9º LESTE'))
        self.btn_8norte.setText(_translate('Form', '8º NORTE'))
        self.SAIR.setText(_translate('Form', 'SAIR'))
        self.historio.setText(_translate('Form', 'HISTÓRICO'))

    def retranslateUi_CTI(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'Sistema de Gestão de Leitos'))
        item = self.tabela_grade.horizontalHeaderItem(0)
        item.setText(_translate('Form', ' '))
        item = self.tabela_grade.horizontalHeaderItem(1)
        item.setText(_translate('Form', 'CÓDIGO DE INTERNACAO'))
        item = self.tabela_grade.horizontalHeaderItem(2)
        item.setText(_translate('Form', 'PRONTUÁRIO'))
        item = self.tabela_grade.horizontalHeaderItem(3)
        item.setText(_translate('Form', 'NPF'))
        item = self.tabela_grade.horizontalHeaderItem(4)
        item.setText(_translate('Form', 'OBSERVAÇÕES'))
        item = self.tabela_grade.horizontalHeaderItem(5)
        item.setText(_translate('Form', 'NOME DO PACIENTE'))
        item = self.tabela_grade.horizontalHeaderItem(7)
        item.setText(_translate('Form', 'DATA DE NASCIMENTO'))
        item = self.tabela_grade.horizontalHeaderItem(8)
        item.setText(_translate('Form', 'SEXO DA ENFERMARIA'))
        item = self.tabela_grade.horizontalHeaderItem(9)
        item.setText(_translate('Form', 'TIPO DE LEITO'))
        item = self.tabela_grade.horizontalHeaderItem(6)
        item.setText(_translate('Form', 'PREVISÃO DE ALTA'))
        item = self.tabela_grade.horizontalHeaderItem(10)
        item.setText(_translate('Form', 'STATUS DO LEITO'))
        item = self.tabela_grade.horizontalHeaderItem(11)
        item.setText(_translate('Form', 'DATA E HORA DE ATUALIZAÇÃO DO STATUS'))
        item = self.tabela_grade.horizontalHeaderItem(12)
        item.setText(_translate('Form', 'SOLICITANTE'))
        item = self.tabela_grade.horizontalHeaderItem(13)
        item.setText(_translate('Form', 'RESERVA COMUNICADA AO ANDAR?'))
        item = self.tabela_grade.horizontalHeaderItem(14)
        item.setText(_translate('Form', 'RESERVA COMUNICADA À: NOME/DATA E HORÁRIO:'))
        if self.dept!= 'Telespectador':
            self.btn_realocar.setText(_translate('Form', 'REALOCAR PACIENTE DAS DEMANDAS'))
            self.btn_alterar.setText(_translate('Form', 'ALTERAR A GRADE DE LEITOS'))
            self.btn_alta.setText(_translate('Form', 'SOLICITAR ALTA'))
        self.usuario.setText(_translate('Form', 'USUÁRIO'))
        self.procura_pac.setText(_translate('Form', 'PROCURAR PACIENTE'))
        self.MONITORAMENTO.setText(_translate('Form', 'MONITORAMENTO'))
        self.DEMANDAS.setText(_translate('Form', 'DEMANDAS'))
        self.GRADE.setText(_translate('Form', 'GRADE'))
        self.GRAFICOS.setText(_translate('Form', 'GRÁFICOS'))
        self.btn_cti_ped.setText(_translate('Form', 'CTI PED'))
        self.btn_2leste.setText(_translate('Form', '2º LESTE'))
        self.btn_CTI_3leste.setText(_translate('Form', 'CTI 3º LESTE'))
        self.btn_UCO.setText(_translate('Form', 'UCO'))
        self.btn_CTI_PS.setText(_translate('Form', 'CTI PS'))
        self.btn_10norte.setText(_translate('Form', '10º NORTE'))
        self.btn_6leste.setText(_translate('Form', '6º LESTE'))
        self.btn_2sul.setText(_translate('Form', '2º SUL'))
        self.btn_8leste.setText(_translate('Form', '8º LESTE'))
        self.btn_8sul.setText(_translate('Form', '8º SUL'))
        self.btn_7norte.setText(_translate('Form', '7º NORTE'))
        self.btn_7leste.setText(_translate('Form', '7º LESTE'))
        self.btn_9leste.setText(_translate('Form', '9º LESTE'))
        self.btn_8norte.setText(_translate('Form', '8º NORTE'))
        self.SAIR.setText(_translate('Form', 'SAIR'))

    def increase_column_width(self, column, width):
        self.tabela_grade.setColumnWidth(column, width)

    def onIconClick(self):
        self.clicked = not self.clicked
        if self.clicked:
            self.label_icone.setStyleSheet('border-radius: 10px; background-color: #2E3D48;')
            self.barra = self.tabela_grade.horizontalScrollBar().value()
            self.barra_vertical = self.tabela_grade.verticalScrollBar().value()
            self.sidebar.setVisible(True)
            if self.email.isVisible():
                self.email.close()
        else:  # inserted
            self.label_icone.setStyleSheet('border-radius: 10px;')
            self.sidebar.setVisible(False)

    def abrir_email(self):
        self.clicked = not self.clicked
        if self.clicked:
            self.barra = self.tabela_grade.horizontalScrollBar().value()
            self.barra_vertical = self.tabela_grade.verticalScrollBar().value()
            self.email.setVisible(True)
            self.atualizar_email()
            if self.sidebar.isVisible():
                self.sidebar.close()
                self.label_icone.setStyleSheet('border-radius: 10px;')
        else:  # inserted
            self.email.setVisible(False)
            for frame in self.frames:
                frame.deleteLater()
                self.frames = []

    def adicionar_email(self):
        lista = ['tabela_internações_e_transf_externas', 'tabela_hemodinamica', 'tabela_agenda_bloco_demanda']
        filename = 'dados.csv'

        try:
            with open(filename, mode='r') as file:
                pass

        except FileNotFoundError:
            with open(filename, mode='w') as file:
                data = []
                reader = csv.reader(file)
                data = list(reader)

                for row in range(len(data)):
                    if data[row][1] == 'S':
                        self.indices.append(row)

                with open(filename, mode='w', newline='') as file:
                    writer = csv.writer(file)

                    for nome_tabela in lista:
                        if nome_tabela == 'tabela_internações_e_transf_externas':
                            ala = 'Internações e Transferências Externas'
                        elif nome_tabela == 'tabela_hemodinamica':
                            ala = 'Hemodinamica'
                        elif nome_tabela == 'tabela_agenda_bloco_demanda':
                            ala = 'Agenda Bloco'

                        conexao = mysql.connector.connect(
                            host='10.36.0.32',
                            user='sglHC2024',
                            password='S4g1L81',
                            database='sgl'
                        )
                        cursor = conexao.cursor()
                        comando = f'SELECT * FROM {nome_tabela}'
                        cursor.execute(comando)
                        leitura = cursor.fetchall()

                        for linha in leitura:
                            data_atual = datetime.now()
                            data_formatada = data_atual.strftime('%d/%m/%Y')

                            if nome_tabela == 'tabela_agenda_bloco_demanda':
                                data_string = linha[4]
                                data_objeto = datetime.strptime(data_string, '%d/%m/%Y %H:%M')
                                data_sem_hora = data_objeto.replace(hour=0, minute=0, second=0)
                                data_hora_obj = data_sem_hora.strftime('%d/%m/%Y')
                            elif nome_tabela == 'tabela_internações_e_transf_externas':
                                data_hora_obj = linha[8]
                            elif nome_tabela == 'tabela_hemodinamica':
                                data_string = linha[3]
                                data_objeto = datetime.strptime(data_string, '%d/%m/%Y %H:%M')
                                data_sem_hora = data_objeto.replace(hour=0, minute=0, second=0)
                                data_hora_obj = data_sem_hora.strftime('%d/%m/%Y')

                            if data_formatada == data_hora_obj:
                                prontuario = str(linha[1])
                                nome = str(linha[4])
                                text = f'{ala} - {data_hora_obj} - O paciente com nome {nome} e prontuário {prontuario} possui um procedimento marcado para a data atual.'

                                if self.indices:
                                    for row in self.indices:
                                        if data[row][0] == text:
                                            leu = 'S'
                                            self.indices.remove(row)
                                            break
                                        leu = 'N'
                                else:
                                    leu = 'N'

                                writer.writerow([text, leu, ala, nome, prontuario])

                        cursor.close()
                        conexao.close()

        # Check and update the notification count
        qt = 0
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row_data in reader:
                if str(row_data[1]) != 'S':
                    qt += 1

        if qt != 0:
            self.qt_notificao.setText(str(qt))
            self.qt_notificao.show()
        else:
            self.qt_notificao.hide()

    def atualizar_email(self):
        for frame in self.frames:
            frame.deleteLater()
            self.frames = []
        filename = 'dados.csv'
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
            for i, row_data in enumerate(data):
                texto = str(row_data[0])
                frame = QPushButton(texto)
                frame.setContentsMargins(0, 80, 0, 0)
                if str(row_data[1]) == 'N':
                    frame.setStyleSheet('QPushButton { background-color: white;font-weight: bold; border: 2px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; text-align: left; padding-left: 10px;}')
                    icon = QIcon('novo-email.ico')
                    frame.setIcon(icon)
                else:  # inserted
                    frame.setStyleSheet('QPushButton { background-color: white; border: 2px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; text-align: left; padding-left: 10px;}')
                self.main_layout.addWidget(frame)
                frame.setFixedSize(370, 50)
                frame.clicked.connect(lambda _, text=texto, date=data: self.abrir_notificao(text, date))
                self.frames.append(frame)

    def abrir_notificao(self, text, data):
        sender = self.sender()
        pos = sender.geometry().topLeft()
        self.indices = []
        for row in range(len(data)):
            if data[row][0] == text:
                self.indices.append(row)
                self.name = data[row][3]
                self.data = data[row][2]
        self.adicionar_email()
        self.atualizar_email()
        btnfechar = QtWidgets.QPushButton(' X ', self.msm)
        btnfechar.setToolTip('Fechar')
        btnfechar.setGeometry(200, 5, 40, 20)
        btnfechar.setStyleSheet('\n                                           QPushButton {\n                                               border: 2px solid #2E3D48;\n                                               border-radius: 10px;\n                                               background-color: balck;\n                                               color: #FFFFFF;\n                                           }\n                                           QPushButton:pressed {\n                                               background-color: #FFFFFF;\n                                               color: black;\n                                           }\n                                       ')
        tooltip_text = 'Fechar'
        btnfechar.setToolTip(tooltip_text)
        btnfechar.clicked.connect(self.fechar_correio)
        for frame in self.frames:
            frame.setFixedSize(80, 50)
        self.label_msm = QtWidgets.QLabel(self.msm)
        self.label_msm.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_msm.setGeometry(10, 30, 230, 200)
        self.label_msm.setWordWrap(True)
        self.label_msm.setText(text)
        text = f'Clique <span style=\'color: blue;\'>aqui</span> para seguir para a tabela {data[row][2]}.'
        label_link = QtWidgets.QLabel(text, self.msm)
        label_link.mousePressEvent = self.abrir_tela_demandas_
        label_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_link.setStyleSheet('font-size: 12px; margin: 0; padding: 0;border: none;')
        label_link.setGeometry(3, 300, 230, 30)
        label_link.setWordWrap(True)
        self.msm.setGeometry(100, 3, 250, 400)
        self.msm.show()
        self.label_msm.show()

    def fechar_correio(self):
        self.msm.close()
        for frame in self.frames:
            frame.setFixedSize(370, 50)

    def abrir_tela_demandas_(self, event):
        if self.data == 'Onco Hemato ped':
            self.teladem.abrir_tabela_Onco_Hemato_Ped(self.teladem.retornar_main_window)
        if self.data == 'Internações e Transferências Externas':
            self.teladem.abrir_tabela_Inter_Tran_Exte(self.teladem.retornar_main_window)
        if self.data == 'Hemodinamica':
            self.teladem.abrir_tabela_Hemodinamica(self.teladem.retornar_main_window)
        if self.data == 'Agenda Bloco':
            self.teladem.abrir_tabela_Agenda_Bloco(self.teladem.retornar_main_window)
        self.teladem.selecionar(self.name)

    def modificao(self):
        self.antigo = ''
        self.copiadora2()
        current_datetime = QDateTime.currentDateTime()
        formatted_time = current_datetime.toString('hh:mm')
        conta_linha = self.tabela_alt2.rowCount()
        conta_coluna = self.tabela_alt2.columnCount()
        for analisa_linha in range(conta_linha):
            for analisa_coluna in range(conta_coluna):
                item = self.tabela_alt2.item(analisa_linha, analisa_coluna)
                item2 = self.tabela_alt.item(analisa_linha, analisa_coluna)
                if item is not None and item.text()!= item2.text():
                    row_label = self.tabela_alt.verticalHeaderItem(analisa_linha).text()
                    col_label = self.tabela_alt.horizontalHeaderItem(analisa_coluna).text()
                    texto = f'{formatted_time}                {self.nome_user} ALTEROU O \"{col_label}\" DE \"{item2.text()}\" PARA \"{item.text()}\" NO LEITO \"{row_label}\"'
                    if texto!= self.antigo:
                        self.lista_modificacao.append(texto)
                        self.antigo = texto

    def alt_banco(self, codigo, prontuario, npf, obs, status, nome, data_nasc, sexo, LEITOS, previsao_alta, data_atualizao_status, solicitante, pergunta_reserva_comunicada, reserva_comunicada_a_quem, TIPO):
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        data_nasc = data_nasc.text()
        data_atualizao_status = data_atualizao_status.text()
        previsao_alta = previsao_alta.text()
        cursor = conexao.cursor()
        if status == 'VAGO':
            data_nasc = ''
            data_atualizao_status = ''
            previsao_alta = ''
        LEITOS = LEITOS.replace(' ', '_')
        comando = f'UPDATE GRADE SET CODIGO_DE_INTERNACAO = \"{codigo.text()}\",NPF = \"{npf.text()}\",PRONTUARIO = \"{prontuario.text()}\",OBSERVACOES = \"{obs.text()}\", STATUS_DO_LEITO = \"{status}\", NOME = \"{nome.text()}\", DATA_DE_NASCIMENTO = \"{data_nasc}\", SEXO_DA_ENFERMARIA = \"{sexo}\",PREVISÃO_DE_ALTA =  \"{previsao_alta}\",DATA_E_HORA_DE_ATUALIZAÇÃO = \"{data_atualizao_status}\", SOLICITANTE = \"{solicitante.text()}\", RESERVA_COMUNICADA = \"{pergunta_reserva_comunicada.text()}\", RESERVA_COMUNICADA_QUEM = \"{reserva_comunicada_a_quem.text()}\"  WHERE idGRADE = \"{LEITOS}\"'
        cursor.execute(comando)
        conexao.commit()
        cursor.close()
        conexao.close()

    def apagar_linha(self, row):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Apagar Reserva?')
        icon = QIcon('warning.ico')
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
            leito = self.tabela_grade.verticalHeaderItem(row)
            cursor = conexao.cursor()
            leito = leito.text().replace(' ', '_')
            comando = f'DELETE FROM GRADE WHERE idGRADE = \"{leito}\"'
            cursor.execute(comando)
            conexao.commit()
            cursor.close()
            conexao.close()
            self.abri_cti(self.form, self.nome_tabela_post)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('Solicitação apagada.')
            icon = QIcon('warning.ico')
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply = msg_box.exec()

    def abrir_novas_unidades(self, Form):
        self.sidebar.close()
        self.label_icone.setStyleSheet('border-radius: 10px;')
        from criar_unidade import Ui_Form
        self.novas_unidades_Aberta = True
        self.criar_unidade = Ui_Form()
        self.criar_unidade.setupUi(Form, self)
        self.cria_unidade_Aberta = True

    def abrir_contas(self, Form):
        self.sidebar.close()
        self.label_icone.setStyleSheet('border-radius: 10px;')
        from contas import Ui_Form
        self.contas_Aberta = True
        self.contas = Ui_Form()
        self.contas.setupUi(Form, self)
        self.timer.stop()
        self.timer_post.stop()
        self.timer_mysql.stop()

    def abrir_configuracoes(self, Form):
        self.sidebar.close()
        self.label_icone.setStyleSheet('border-radius: 10px;')
        from config import Ui_Form
        self.config = Ui_Form()
        self.config.setupUi(Form, self)
        self.config_Aberta = True
        self.timer.stop()
        self.timer_post.stop()
        self.timer_mysql.stop()

    def abrir_conta_do_usuario(self, Form):
        self.sidebar.close()
        self.label_icone.setStyleSheet('border-radius: 10px;')
        self.timer.stop()
        self.timer_post.stop()
        self.timer_mysql.stop()
        from conta_do_usuario import Ui_Form
        self.conta_user = Ui_Form()
        self.conta_user.setupUi(Form, self)
        self.conta_do_usuario_Aberta = True

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
        self.frame.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;')
        self.frame_senso.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;')
        self.frame_relatorio.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;')
        self.sidebar.setStyleSheet(f'border: 2px solid #2E3D48;background-color: {backcolocor}; border-radius: 10px;color: {color};font: {font_name} {tamanho}px;')
        for label in self.sidebar.findChildren(QtWidgets.QLabel):
            label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name}; border:none')
        self.qt_notificao.setStyleSheet('background-color: red; color: #FFFFFF; border: 2px solid white; border-radius: 10px;')
        self.TITULO_CTI.setStyleSheet(f'color: {color}; font:  23 px {font_name}; border:none')

    def toggle_frame_visibility(self, sidebar, email):
        if not sidebar.isHidden():
            sidebar.hide()
            self.label_icone.setStyleSheet('border-radius: 10px;')
        if not email.isHidden():
            email.hide()
        if self.config_Aberta == True:
            self.janela_config.close()
            self.config_Aberta = False
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
        if self.realocar_Aberta == True:
            self.janela_realocar.close()
            self.realocar_Aberta = False
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
        if self.procurar_Aberta == True:
            self.janela_procura.close()
            self.procurar_Aberta = False
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
        if self.contas_Aberta == True:
            self.janela_contas.close()
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
            self.contas_Aberta = False
        if self.conta_do_usuario_Aberta == True:
            self.janela_conta_do_usuario.close()
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
            self.conta_do_usuario_Aberta = False
        if self.cria_unidade_Aberta == True:
            self.janela_cria_unidade.close()
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
            self.cria_unidade_Aberta = False

    def close_frame(self, row, col):
        if not self.sidebar.isHidden():
            self.sidebar.hide()
            self.label_icone.setStyleSheet('border-radius: 10px;')
        if not self.email.isHidden():
            self.email.hide()
        if self.config_Aberta == True:
            self.janela_config.close()
            self.config_Aberta = False
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
        if self.realocar_Aberta == True:
            self.janela_realocar.close()
            self.realocar_Aberta = False
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
        if self.procurar_Aberta == True:
            self.janela_procura.close()
            self.procurar_Aberta = False
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
        if self.contas_Aberta == True:
            self.janela_contas.close()
            self.contas_Aberta = False
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
        if self.conta_do_usuario_Aberta == True:
            self.janela_conta_do_usuario.close()
            self.conta_do_usuario_Aberta = False
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
        if self.cria_unidade_Aberta == True:
            self.janela_cria_unidade.close()
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
            self.cria_unidade_Aberta = False

    def check_scrollbar_value(self):
        if self.tabela_grade.horizontalScrollBar().value()!= self.barra:
            if not self.sidebar.isHidden():
                self.sidebar.hide()
                self.label_icone.setStyleSheet('border-radius: 10px;')
            if not self.email.isHidden():
                self.email.hide()
            if self.config_Aberta == True:
                self.janela_config.close()
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                self.config_Aberta = False
            if self.realocar_Aberta == True:
                self.janela_realocar.close()
                self.realocar_Aberta = False
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
            if self.procurar_Aberta == True:
                self.janela_procura.close()
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                self.procurar_Aberta = False
            if self.contas_Aberta == True:
                self.janela_contas.close()
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                self.contas_Aberta = False
            if self.conta_do_usuario_Aberta == True:
                self.janela_conta_do_usuario.close()
                self.conta_do_usuario_Aberta = False
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
            if self.cria_unidade_Aberta == True:
                self.janela_cria_unidade.close()
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                self.cria_unidade_Aberta = False
        if self.tabela_grade.verticalScrollBar().value()!= self.barra_vertical:
            if not self.sidebar.isHidden():
                self.sidebar.hide()
                self.label_icone.setStyleSheet('border-radius: 10px;')
            if not self.email.isHidden():
                self.email.hide()
            if self.config_Aberta == True:
                self.janela_config.close()
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                self.config_Aberta = False
            if self.realocar_Aberta == True:
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                self.janela_realocar.close()
                self.realocar_Aberta = False
            if self.procurar_Aberta == True:
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                self.janela_procura.close()
                self.procurar_Aberta = False
            if self.contas_Aberta == True:
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                self.janela_contas.close()
                self.contas_Aberta = False
            if self.conta_do_usuario_Aberta == True:
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                self.janela_conta_do_usuario.close()
                self.conta_do_usuario_Aberta = False
            if self.cria_unidade_Aberta == True:
                self.janela_cria_unidade.close()
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                self.cria_unidade_Aberta = False

    def abrir_senso(self, Form):
        if self.frame_do_grafico.isVisible():
            self.frame_do_grafico.hide()
        if self.frame_do_monitoramento.isVisible():
            self.frame_do_monitoramento.hide()
        if self.senso_Aberta == False:
            self.senso.move(3, 0)
            self.senso.setText('VOLTAR')
            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                if btn!= self.senso:
                    if self.dept!= 'Telespectador':
                        btn.hide()
                    else:  # inserted
                        if btn!= self.btn_alta and btn!= self.btn_alterar and (btn!= self.btn_realocar) and (btn!= self.btn_relatorio) and (btn!= self.senso):
                            btn.hide()
            self.scroll_area_btns.hide()
            self.tabela_grade.hide()
            self.BARRADEPESQUISA.hide()
            self.label_icone.hide()
            self.notificao_label.hide()
            self.TITULO_CTI.hide()
            from senso import Ui_Form
            self.senso_leitos = Ui_Form()
            self.frame_senso.show()
            self.btn_filtros.show()
            self.senso_leitos.setupUi(Form, self.frame_senso, self)
            self.senso_Aberta = True
            self.btn_dowload_senso.show()
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
            return
        else:  # inserted
            self.frame_senso.hide()
            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                if self.dept!= 'Telespectador':
                    btn.show()
                else:  # inserted
                    if btn!= self.btn_alta and btn!= self.btn_alterar and (btn!= self.btn_realocar) and (btn!= self.btn_relatorio) and (btn!= self.senso):
                        btn.show()
            self.senso.setText('SENSO')
            self.tabela_grade.show()
            self.BARRADEPESQUISA.show()
            self.scroll_area_btns.show()
            self.btn_filtros.deleteLater()
            self.btnfechar.deleteLater()
            self.frame_personalisa.deleteLater()
            self.frame_box.deleteLater()
            self.btn_dowload_senso.deleteLater()
            self.btn_filtros = QtWidgets.QPushButton('▼ Selecione uma Data ', parent=self.frame)
            self.btn_filtros.setGeometry(QtCore.QRect(80, 0, 150, 23))
            self.btn_filtros.hide()
            self.btn_dowload_senso = QtWidgets.QPushButton('Baixar Senso', parent=self.frame)
            self.btn_dowload_senso.setGeometry(QtCore.QRect(230, 0, 150, 23))
            self.btn_dowload_senso.hide()
            self.btn_dowload_senso.setToolTip('Baixar Senso')
            self.btn_dowload_senso.setStyleSheet('\n                                        QPushButton {\n                                            border: 2px solid #2E3D48;\n                                            border-radius: 10px;\n                                            background-color: #FFFFFF;\n                                            color: #2E3D48;\n                                        }\n\n                                        QPushButton:hover {\n                                            background-color: #DDDDDD;  /* Change this to your desired hover color */\n                                            color: rgb(0, 0, 0);\n                                        }\n\n                                        QPushButton:pressed {\n                                            background-color: #2E3D48;  /* Change this to your desired pressed color */\n                                            color: #FFFFFF;\n                                        }\n                                    ')
            self.btnfechar = QtWidgets.QPushButton(' X ', parent=self.frame)
            self.btnfechar.hide()
            self.btnfechar.setGeometry(QtCore.QRect(190, 0, 30, 23))
            self.frame_personalisa = QtWidgets.QFrame(parent=self.frame)
            self.frame_personalisa.setStyleSheet('\n                                        QFrame  {\n                                            background-color: #FFFFFF;\n                                            border-top-right-radius: 20px;\n                                            border-bottom-right-radius: 20px;\n                                            border-left: 1px solid black;\n                                        }\n                                    ')
            self.frame_personalisa.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.frame_personalisa.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.frame_personalisa.setObjectName('frame_box')
            self.frame_personalisa.setGeometry(QtCore.QRect(225, 23, 270, 125))
            self.frame_personalisa.hide()
            self.frame_box = QtWidgets.QFrame(parent=self.frame)
            self.frame_box.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
            self.frame_box.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.frame_box.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.frame_box.setGeometry(QtCore.QRect(80, 23, 150, 70))
            self.frame_box.hide()
            self.label_icone.show()
            self.notificao_label.show()
            self.TITULO_CTI.show()
            self.senso_Aberta = False
            self.senso.move(540, 0)
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()

    def atualizar_senso(self):
        analise = True
        Form = self.form
        from datetime import datetime
        current_month_year = datetime.now().strftime('%B_%Y')
        senso_folder = os.path.join(os.getcwd(), 'senso')
        if not os.path.exists(senso_folder):
            os.makedirs(senso_folder)
        month_year_folder = os.path.join(senso_folder, current_month_year)
        if not os.path.exists(month_year_folder):
            os.makedirs(month_year_folder)
        for file in os.listdir(month_year_folder):
            if file.endswith('.xlsx'):
                filepath = os.path.join(month_year_folder, file)
                match = re.match('(\\d{2})-(\\d{2})-(\\d{4})', file)
                if match:
                    self.dia = match.group(1)
                    self.month = match.group(2)
                    self.year = match.group(3)
                data_atual = QDateTime.currentDateTime()
                dia = data_atual.date().day()
                mes = data_atual.date().month()
                ano = data_atual.date().year()
                dia = int(dia) - 1
                mes = int(mes)
                ano = int(ano)
                da = int(self.dia)
                month = int(self.month)
                year = int(self.year)
                if dia == da and ano == year and (month == mes):
                    analise = False
                    break
        if analise == True:
            rows = ['', 'PS|UDC - AGHU', 'PS|CORREDOR - AGHU', 'PS|PEDIATRIA - AGHU', 'PS|UTI - AGHU', '2º LESTE - GRADE', '2º SUL - GRADE', '3º LESTE/CTI - GRADE', '3º NORTE/UCO - GRADE', 'MÃE CANGURU - CENSO EBSERH', 'PRÉ-PARTO - CENSO EBSERH', 'MATERNIDADE - CENSO EBSERH', 'NEO (UTIN/UCIN) - CENSO EBSERH', '6º LESTE - GRADE', '6º NORTE/CTI PEDIATRICO - GRADE', '7º LESTE - GRADE', '7º NORTE - GRADE', '8º LESTE - GRADE', '8º NORTE - GRADE', '8º SUL - GRADE', '9º LESTE - GRADE', '10º NORTE - GRADE', 'HOSPITAL SÃO GERALDO - AGHU', 'CLÍNICO ADULTO', 'CIRÚRGICO ADULTO', 'OBSTÉTRICO', 'PEDIATRICO', 'CTI - ADULTO', 'CTI - PEDIATRICO']
            columns = ['OCUPAÇÃO', 'BLOQUEIOS', 'CNES', 'OCUPAÇÃO %', 'LEITO/DIA']
            save_folder = month_year_folder
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            from datetime import datetime, timedelta
            current_date = datetime.now()
            new_date = current_date - timedelta(days=1)
            formatted_date = new_date.strftime('%d-%m-%Y')
            file_path = os.path.join(save_folder, f'{formatted_date}.xlsx')
            workbook = Workbook()
            sheet = workbook.active
            ocupado_total = 0
            bloqueado_total = 0
            total_leitos = 0
            for row in range(1, len(rows)):
                self.total = 0
                self.ocupado_senso = 0
                self.bloqueado_senso = 0
                ala = rows[row]
                self.dados_senso(ala)
                for column in range(len(columns)):
                    if columns[column] == 'OCUPAÇÃO':
                        ocupado_total += self.ocupado_senso
                        item = str(self.ocupado_senso)
                    if columns[column] == 'BLOQUEIOS':
                        item = str(self.bloqueado_senso)
                        bloqueado_total += self.bloqueado_senso
                    if columns[column] == 'OCUPAÇÃO %':
                        if self.ocupado_senso!= 0:
                            item = '{:.2f} %'.format(self.ocupado_senso / (self.total - self.bloqueado_senso) * 100)
                        else:  # inserted
                            item = '0.00 %'
                    if columns[column] == 'CNES':
                        item = str(self.total)
                        total_leitos += self.total
                    if columns[column] == 'LEITO/DIA':
                        item = str(self.total - self.bloqueado_senso)
                    if item is not None:
                        sheet.cell(row=row + 1, column=column + 1, value=item)
                    else:  # inserted
                        sheet.cell(row=row + 1, column=column + 1, value='')
            sheet.cell(row=1, column=1, value=str(ocupado_total))
            sheet.cell(row=1, column=2, value=str(bloqueado_total))
            sheet.cell(row=1, column=3, value=str(total_leitos))
            item = '{:.2f} %'.format(ocupado_total / (total_leitos - bloqueado_total))
            sheet.cell(row=1, column=4, value=item)
            sheet.cell(row=1, column=5, value=str(total_leitos - bloqueado_total))
            try:
                workbook.save(file_path)
            except Exception as e:
                print(self, 'Erro', f'Ocorreu um erro ao salvar o arquivo:\n{str(e)}')
        if self.codigo_ala == 29:
            self.abri_cti(Form, 'CTI PEDIÁTRICO - 06N')
        if self.codigo_ala == 23:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO CORONARIANA - 03N')
        if self.codigo_ala == 30:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 06L')
        if self.codigo_ala == 36:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 10N')
        if self.codigo_ala == 169:
            self.abri_cti(Form, 'UTI - PRONTO SOCORRO')
        if self.codigo_ala == 22:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 02L')
        if self.codigo_ala == 21:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 02S')
        if self.codigo_ala == 32:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 07L')
        if self.codigo_ala == 31:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 07N')
        if self.codigo_ala == 33:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08S')
        if self.codigo_ala == 34:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08L')
        if self.codigo_ala == 193:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08N')
        if self.codigo_ala == 35:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 09L')
        if self.codigo_ala == 24:
            self.abri_cti(Form, 'CTI ADULTO - 03L')

    def dados_senso(self, ala):
        Form = self.form
        confir = False
        if ala == '6º NORTE/CTI PEDIATRICO - GRADE':
            self.abri_cti(Form, 'CTI PEDIÁTRICO - 06N')
            confir = True
        else:  # inserted
            if ala == '3º NORTE/UCO - GRADE':
                self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO CORONARIANA - 03N')
                confir = True
            else:  # inserted
                if ala == '6º LESTE - GRADE':
                    self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 06L')
                    confir = True
                else:  # inserted
                    if ala == '10º NORTE - GRADE':
                        self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 10N')
                        confir = True
                    else:  # inserted
                        if ala == 'PS|UTI - AGHU':
                            self.abri_cti(Form, 'UTI - PRONTO SOCORRO')
                            confir = True
                        else:  # inserted
                            if ala == '2º LESTE - GRADE':
                                self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 02L')
                                confir = True
                            else:  # inserted
                                if ala == '2º SUL - GRADE':
                                    self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 02S')
                                    confir = True
                                else:  # inserted
                                    if ala == '7º LESTE - GRADE':
                                        self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 07L')
                                        confir = True
                                    else:  # inserted
                                        if ala == '7º NORTE - GRADE':
                                            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 07N')
                                            confir = True
                                        else:  # inserted
                                            if ala == '8º SUL - GRADE':
                                                self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08S')
                                                confir = True
                                            else:  # inserted
                                                if ala == '8º LESTE - GRADE':
                                                    self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08L')
                                                    confir = True
                                                else:  # inserted
                                                    if ala == '8º NORTE - GRADE':
                                                        self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08N')
                                                        confir = True
                                                    else:  # inserted
                                                        if ala == '9º LESTE - GRADE':
                                                            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 09L')
                                                            confir = True
                                                        else:  # inserted
                                                            if ala == '3º LESTE/CTI - GRADE':
                                                                self.abri_cti(Form, 'CTI ADULTO - 03L')
                                                                confir = True
                                                                rows = ['', 'PS|UDC - AGHU', 'PS|CORREDOR - AGHU', 'PS|PEDIATRIA - AGHU', 'PS|UTI - AGHU', '2º LESTE - GRADE', '2º SUL - GRADE', '3º LESTE/CTI - GRADE', '3º NORTE/UCO - GRADE', 'MÃE CANGURU - CENSO EBSERH', 'PRÉ-PARTO - CENSO EBSERH', 'MATERNIDADE - CENSO EBSERH', 'NEO (UTIN/UCIN) - CENSO EBSERH', '6º LESTE - GRADE', '6º NORTE/CTI PEDIATRICO - GRADE', '7º LESTE - GRADE', '7º NORTE - GRADE', '8º LESTE - GRADE', '8º NORTE - GRADE', '8º SUL - GRADE', '9º LESTE - GRADE', '10º NORTE - GRADE', 'HOSPITAL SÃO GERALDO - AGHU', 'CLÍNICO ADULTO', 'CIRÚRGICO ADULTO', 'OBSTÉTRICO', 'PEDIATRICO', 'CTI - ADULTO', 'CTI - PEDIATRICO']
                                                            else:  # inserted
                                                                mapa_alas = {'PS|UDC - AGHU': 171, 'PS|CORREDOR - AGHU': 173, 'PS|PEDIATRIA - AGHU': 170, 'HOSPITAL SÃO GERALDO - AGHU': 47, 'OBSTÉTRICO': 93, 'PEDIATRICO': [141, 170, 29]}
                                                                codigo_ala = mapa_alas.get(ala)
                                                                if codigo_ala is not None:
                                                                    self.pegar_senso_aghu(codigo_ala)
        if confir == True:
            colum_status = 0
            for colum in range(self.tabela_grade.columnCount()):
                item_pac = self.tabela_grade.horizontalHeaderItem(colum)
                if item_pac.text() == 'STATUS DO LEITO':
                    colum_status = colum
            for row in range(self.conta_linha()):
                self.total += 1
                selecao = self.item(row, colum_status)
                if selecao.text() == 'OCUPADO':
                    self.ocupado_senso += 1
                if selecao.text() == 'BLOQUEADO':
                    self.bloqueado_senso += 1
                if selecao.text() == 'BLOQUEADO POR FALTA DE FUNCIONÁRIOS':
                    self.bloqueado_senso += 1
                if selecao.text() == 'PONTUAL - BLOQUEADO POR FALTA DE FUNCIONÁRIOS':
                    self.bloqueado_senso += 1
                if selecao.text() == 'BLOQUEADO POR MANUTENÇÃO':
                    self.bloqueado_senso += 1
                if selecao.text() == 'BLOQUEADO POR VM/VNI':
                    self.bloqueado_senso += 1
                if selecao.text() == 'BLOQUEADO POR OUTROS MOTIVOS':
                    self.bloqueado_senso += 1
    def pegar_senso_aghu(self, codigo_ala):
        qt = 0
        ocup = 0
        boq = 0
        try:
            connection = psycopg2.connect(
                user='ugen_integra',
                password='aghuintegracao',
                host='10.36.2.35',
                port='6544',
                database='dbaghu'
            )
            cursor = connection.cursor()
            cursor.execute('SELECT unf_seq, int_seq, ind_situacao FROM agh.ain_leitos WHERE unf_seq = 29')
            rows = cursor.fetchall()
            for row in rows:
                self.total += 1
                if row[1] is not None:
                    self.ocupado_senso += 1
                if row[2] == 'I':
                    self.bloqueado_senso += 1
        except psycopg2.Error as e:
            print('Erro ao conectar ao PostgreSQL:', e)
        finally:
            if connection:
                cursor.close()
                connection.close()



    def abri_relatorio(self, Form):
        if self.frame_do_grafico.isVisible():
            self.frame_do_grafico.hide()
        if self.frame_do_monitoramento.isVisible():
            self.frame_do_monitoramento.hide()
        if not self.frame_relatorio.isVisible():
            self.scroll_area_btns.hide()
            self.timer_post.stop()
            self.timer_mysql.stop()
            self.timer.stop()
            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                if btn!= self.btn_relatorio:
                    btn.hide()
            self.btn_relatorio.move(0, 0)
            self.btn_relatorio.setText('VOLTAR')
            self.tabela_grade.hide()
            self.BARRADEPESQUISA.hide()
            self.label_icone.hide()
            self.notificao_label.hide()
            self.TITULO_CTI.hide()
            from relatorio import Ui_Form
            self.relatorio = Ui_Form()
            self.frame_relatorio.show()
            self.relatorio.setupUi(Form, self.frame_relatorio, self)
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
        else:  # inserted
            self.timer_post.start()
            self.timer_mysql.start()
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
            self.scroll_area_btns.show()
            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                if self.dept!= 'Telespectador':
                    btn.show()
                else:  # inserted
                    if btn!= self.btn_alta and btn!= self.btn_alterar and (btn!= self.btn_realocar) and (btn!= self.btn_relatorio) and (btn!= self.senso):
                        btn.show()
            self.btn_relatorio.setGeometry(QtCore.QRect(620, 0, 75, 23))
            self.tabela_grade.show()
            self.btn_relatorio.setText('RELATÓRIO')
            self.BARRADEPESQUISA.show()
            self.label_icone.show()
            self.notificao_label.show()
            self.TITULO_CTI.show()
            self.frame_relatorio.hide()
            self.btn_filtros.deleteLater()
            self.btnfechar.deleteLater()
            self.frame_personalisa.deleteLater()
            self.frame_box.deleteLater()
            self.btn_dowload_senso.deleteLater()
            self.btn_filtros = QtWidgets.QPushButton('▼ Selecione uma Data ', parent=self.frame)
            self.btn_filtros.setGeometry(QtCore.QRect(80, 0, 150, 23))
            self.btn_filtros.hide()
            self.btn_dowload_senso = QtWidgets.QPushButton('Baixar Senso', parent=self.frame)
            self.btn_dowload_senso.setGeometry(QtCore.QRect(230, 0, 150, 23))
            self.btn_dowload_senso.hide()
            self.btn_dowload_senso.setToolTip('Baixar Senso')
            self.btn_dowload_senso.setStyleSheet('\n                            QPushButton {\n                                border: 2px solid #2E3D48;\n                                border-radius: 10px;\n                                background-color: #FFFFFF;\n                                color: #2E3D48;\n                            }\n\n                            QPushButton:hover {\n                                background-color: #DDDDDD;  /* Change this to your desired hover color */\n                                color: rgb(0, 0, 0);\n                            }\n\n                            QPushButton:pressed {\n                                background-color: #2E3D48;  /* Change this to your desired pressed color */\n                                color: #FFFFFF;\n                            }\n                        ')
            self.btnfechar = QtWidgets.QPushButton(' X ', parent=self.frame)
            self.btnfechar.hide()
            self.btnfechar.setGeometry(QtCore.QRect(190, 0, 30, 23))
            self.frame_personalisa = QtWidgets.QFrame(parent=self.frame)
            self.frame_personalisa.setStyleSheet('\n                                                    QFrame  {\n                                                        background-color: #FFFFFF;\n                                                        border-top-right-radius: 20px;\n                                                        border-bottom-right-radius: 20px;\n                                                        border-left: 1px solid black;\n                                                    }\n                                                ')
            self.frame_personalisa.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.frame_personalisa.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.frame_personalisa.setObjectName('frame_box')
            self.frame_personalisa.setGeometry(QtCore.QRect(225, 23, 270, 125))
            self.frame_personalisa.hide()
            self.frame_box = QtWidgets.QFrame(parent=self.frame)
            self.frame_box.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
            self.frame_box.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.frame_box.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.frame_box.setGeometry(QtCore.QRect(80, 23, 150, 125))
            self.frame_box.hide()
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()

    def abrir_painel(self, Form):
        if not self.frame_do_monitoramento.isHidden():
            self.frame_do_monitoramento.hide()
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
        if not self.frame_do_grafico.isHidden():
            self.canvas.hide()
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
        if not self.scroll_painel.isVisible():
            self.painel.setText('VOLTAR')
            self.painel.setToolTip('VOLTAR')
            self.painel.move(0, 0)
            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                if btn!= self.painel:
                    btn.hide()
            self.tabela_grade.hide()
            self.BARRADEPESQUISA.hide()
            self.label_icone.hide()
            self.notificao_label.hide()
            self.TITULO_CTI.hide()
            self.scroll_painel.show()
            self.scroll_area_btns.hide()
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
        else:  # inserted
            self.painel.setText('PAINEL')
            self.painel.setToolTip('PAINEL')
            self.painel.move(460, 0)
            for widget in self.list_painel:
                widget.deleteLater()
            self.frame_terapia_intensiva.deleteLater()
            self.frame_unidades_internacao_1.deleteLater()
            self.scroll_painel.hide()
            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                if self.dept!= 'Telespectador':
                    btn.show()
                else:  # inserted
                    if btn!= self.btn_alta and btn!= self.btn_alterar and (btn!= self.btn_realocar) and (btn!= self.btn_relatorio) and (btn!= self.senso):
                        btn.show()
            self.tabela_grade.show()
            self.BARRADEPESQUISA.show()
            self.label_icone.show()
            self.notificao_label.show()
            self.TITULO_CTI.show()
            self.btn_dowload_senso.hide()
            self.btnfechar.hide()
            self.btn_filtros.hide()
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
            self.scroll_area_btns.show()

    def atualizar_painel(self):
        self.help_sccrol_painel = True
        self.qt_int_adulto = 0
        self.qt_int_ped = 0
        self.qt_int_adulto_total = 0
        self.qt_int_neo = 0
        self.qt_int_ped_total = 0
        self.qt_int_adulto2 = 0
        self.qt_int_adulto_total2 = 0
        self.qt_int_ped2 = 0
        self.qt_int_ped_total2 = 0
        self.total_bloq = 0
        self.total_vago = 0
        self.total_rese = 0
        self.total_ocup = 0
        self.qt_bl_manu = 0
        self.qt_bl_VM_VNI = 0
        self.qt_se_fun = 0
        self.qt_pront = 0
        self.qt_vagos_2leste = 0
        self.qt_vagos_2sul = 0
        self.qt_vagos_7norte = 0
        self.qt_vagos_10norte = 0
        self.qt_vagos_8leste = 0
        self.qt_vagos_6leste = 0
        self.qt_vagos_8norte = 0
        self.qt_vagos_uco = 0
        self.qt_vagos_uti_ps = 0
        self.qt_vagos_9leste = 0
        self.qt_vagos_7leste = 0
        self.qt_vagos_8sul = 0
        self.qt_vagos_3leste = 0
        self.qt_vagos_cti_ped = 0
        Form = self.form
        self.list_painel = []
        titulo_label = QtWidgets.QLabel('TERAPIAS INTENSIVAS')
        titulo_label.setFixedHeight(40)
        titulo_label.setStyleSheet(' background-color: rgb(127, 127, 127);color: white;font: 20 px arial; border: 1px solid #C0C0C0; border-radius: 10px; ')
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.list_painel.append(titulo_label)
        self.frame_terapia_intensiva = QtWidgets.QFrame()
        self.frame_terapia_intensiva.setStyleSheet('QFrame { background-color: white; border: 1px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        self.frame_terapia_intensiva.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_terapia_intensiva.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_terapia_intensiva.setObjectName('frame')
        self.main_layout_painel.addWidget(titulo_label)
        self.main_layout_painel.addWidget(self.frame_terapia_intensiva)
        h_layout_terapia_intensiva = QtWidgets.QHBoxLayout()
        self.frame_terapia_intensiva.setLayout(h_layout_terapia_intensiva)
        frame_ctips = QFrame()
        frame_ctips.setFrameShape(QFrame.Shape.Box)
        frame_ctips.setContentsMargins(0, 80, 0, 0)
        frame_ctips.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_ctips.setFixedSize(1110, 461)
        titulo_ctips = QtWidgets.QLabel('CTI PS', frame_ctips)
        titulo_ctips.setFixedWidth(1110)
        titulo_ctips.setFixedHeight(20)
        titulo_ctips.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_ctips.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_cti_ps(Form, frame_ctips)
        self.list_painel.append(frame_ctips)
        h_layout_terapia_intensiva.addWidget(frame_ctips)
        frame_ctiadulto = QFrame()
        frame_ctiadulto.setFrameShape(QFrame.Shape.Box)
        frame_ctiadulto.setContentsMargins(0, 80, 0, 0)
        frame_ctiadulto.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_ctiadulto.setFixedSize(1150, 461)
        self.list_painel.append(frame_ctiadulto)
        self.monitora_3_leste(Form, frame_ctiadulto)
        titulo_ctiadulto = QtWidgets.QLabel('CTI ADULTO', frame_ctiadulto)
        titulo_ctiadulto.setFixedWidth(1150)
        titulo_ctiadulto.setFixedHeight(20)
        titulo_ctiadulto.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_ctiadulto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_layout_terapia_intensiva.addWidget(frame_ctiadulto)
        frame_unidade_coronariana = QFrame()
        frame_unidade_coronariana.setFrameShape(QFrame.Shape.Box)
        frame_unidade_coronariana.setContentsMargins(0, 80, 0, 0)
        frame_unidade_coronariana.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_unidade_coronariana.setFixedSize(1091, 461)
        self.list_painel.append(frame_ctiadulto)
        h_layout_terapia_intensiva.addWidget(frame_unidade_coronariana)
        titulo_unidade_coronariana = QtWidgets.QLabel('UNIDADE CORONARIANA', frame_unidade_coronariana)
        titulo_unidade_coronariana.setFixedWidth(1091)
        titulo_unidade_coronariana.setFixedHeight(20)
        titulo_unidade_coronariana.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_unidade_coronariana.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.uco(Form, frame_unidade_coronariana)
        frame_ctiped = QFrame()
        frame_ctiped.setFrameShape(QFrame.Shape.Box)
        frame_ctiped.setContentsMargins(0, 80, 0, 0)
        frame_ctiped.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_ctiped.setFixedSize(665, 461)
        self.list_painel.append(frame_ctiped)
        h_layout_terapia_intensiva.addWidget(frame_ctiped)
        titulo_ctiped = QtWidgets.QLabel('CTI PEDIÁTRICO', frame_ctiped)
        titulo_ctiped.setFixedWidth(665)
        titulo_ctiped.setFixedHeight(20)
        titulo_ctiped.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_ctiped.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_cti_ped(Form, frame_ctiped)
        frame_ucpneonatal = QFrame()
        frame_ucpneonatal.setFrameShape(QFrame.Shape.Box)
        frame_ucpneonatal.setContentsMargins(0, 80, 0, 0)
        frame_ucpneonatal.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_ucpneonatal.setFixedSize(666, 461)
        self.list_painel.append(frame_ucpneonatal)
        h_layout_terapia_intensiva.addWidget(frame_ucpneonatal)
        titulo_ucpneonatal = QtWidgets.QLabel(' UCP NEONATAL ', frame_ucpneonatal)
        titulo_ucpneonatal.setFixedWidth(666)
        titulo_ucpneonatal.setFixedHeight(20)
        titulo_ucpneonatal.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_ucpneonatal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_ucp_neo_natal(Form, frame_ucpneonatal)
        frame_dados1 = QFrame()
        frame_dados1.setFrameShape(QFrame.Shape.Box)
        frame_dados1.setContentsMargins(0, 80, 0, 0)
        frame_dados1.setStyleSheet('QFrame { background-color: white; border: none; }')
        frame_dados1.setFixedSize(500, 461)
        h_layout_terapia_intensiva.addWidget(frame_dados1)
        adulto_label = QtWidgets.QLabel('ADULTO', frame_dados1)
        adulto_label.setGeometry(30, 20, 200, 30)
        font = QtGui.QFont()
        font.setPointSize(25)
        adulto_label.setFont(font)
        adulto_label.setStyleSheet('background-color: rgb(250, 250, 250); color: black; font-weight: bold; border: none;')
        adulto_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        pediatrica_label = QtWidgets.QLabel('PEDIÁTRICA', frame_dados1)
        pediatrica_label.setGeometry(30, 170, 230, 30)
        font = QtGui.QFont()
        font.setPointSize(25)
        pediatrica_label.setFont(font)
        pediatrica_label.setStyleSheet('background-color: rgb(250, 250, 250); color: black; font-weight: bold; border: none;')
        pediatrica_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        neonatal_label = QtWidgets.QLabel('NEONATAL', frame_dados1)
        neonatal_label.setGeometry(30, 320, 200, 30)
        font = QtGui.QFont()
        font.setPointSize(25)
        neonatal_label.setFont(font)
        neonatal_label.setStyleSheet('background-color: rgb(250, 250, 250); color: black; font-weight: bold; border: none;')
        neonatal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.qt_int_adulto!= 0 and self.qt_int_adulto_total!= 0:
            valor = '{:.2f} %'.format(self.qt_int_adulto / self.qt_int_adulto_total * 100)
        else:  # inserted
            valor = '0.0 %'
        qt_adulto_label = QtWidgets.QLabel(valor, frame_dados1)
        qt_adulto_label.setGeometry(300, 20, 50, 30)
        qt_adulto_label.setStyleSheet(' color: rgb(250, 250, 250);background-color: black;font-size: 100 px;font-weight: bold; border: none; ')
        qt_adulto_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.qt_int_ped!= 0 and self.qt_int_ped_total!= 0:
            valor = '{:.2f} %'.format(self.qt_int_ped / self.qt_int_ped_total * 100)
        else:  # inserted
            valor = '0.0 %'
        qt_ped_label = QtWidgets.QLabel(valor, frame_dados1)
        qt_ped_label.setGeometry(300, 170, 50, 30)
        qt_ped_label.setStyleSheet(' color: rgb(250, 250, 250);background-color: black;font-size: 100 px;font-weight: bold; border: none; ')
        qt_ped_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qt_neo_label = QtWidgets.QLabel(str(self.qt_int_neo), frame_dados1)
        qt_neo_label.setGeometry(300, 320, 50, 30)
        qt_neo_label.setStyleSheet(' color: rgb(250, 250, 250);background-color: black;font-size: 100 px;font-weight: bold; border: none; ')
        qt_neo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo_label_2 = QtWidgets.QLabel('UNIDADES DE INTERNAÇÃO')
        titulo_label_2.setFixedHeight(40)
        titulo_label_2.setStyleSheet(' background-color: rgb(127, 127, 127);color: white;font: 20 px arial; border: 1px solid #C0C0C0; border-radius: 10px; ')
        titulo_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.list_painel.append(titulo_label_2)
        h_layout_terapia_intensiva.addWidget(titulo_label_2)
        self.frame_unidades_internacao_1 = QtWidgets.QFrame()
        self.frame_unidades_internacao_1.setStyleSheet('QFrame { background-color: white; border: 1px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        self.frame_unidades_internacao_1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_unidades_internacao_1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_unidades_internacao_1.setObjectName('frame')
        self.main_layout_painel.addWidget(titulo_label_2)
        self.main_layout_painel.addWidget(self.frame_unidades_internacao_1)
        h_layout_unidades_internacao_1 = QtWidgets.QHBoxLayout()
        self.frame_unidades_internacao_1.setLayout(h_layout_unidades_internacao_1)
        frame_7_norte = QFrame()
        frame_7_norte.setFrameShape(QFrame.Shape.Box)
        frame_7_norte.setContentsMargins(0, 80, 0, 0)
        frame_7_norte.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_7_norte.setFixedSize(1110, 1280)
        self.list_painel.append(frame_7_norte)
        h_layout_unidades_internacao_1.addWidget(frame_7_norte)
        titulo_7_norte = QtWidgets.QLabel(' 7º ANDAR \n ALA NORTE', frame_7_norte)
        titulo_7_norte.setFixedWidth(1110)
        titulo_7_norte.setFixedHeight(25)
        titulo_7_norte.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_7_norte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_7_norte(Form, frame_7_norte)
        frame_8_norte = QFrame()
        frame_8_norte.setFrameShape(QFrame.Shape.Box)
        frame_8_norte.setContentsMargins(0, 80, 0, 0)
        frame_8_norte.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_8_norte.setFixedSize(1150, 1280)
        self.list_painel.append(frame_8_norte)
        h_layout_unidades_internacao_1.addWidget(frame_8_norte)
        titulo_8_norte = QtWidgets.QLabel(' 8º ANDAR \n ALA NORTE', frame_8_norte)
        titulo_8_norte.setFixedWidth(1150)
        titulo_8_norte.setFixedHeight(28)
        titulo_8_norte.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_8_norte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_8_norte(Form, frame_8_norte)
        frame_2_leste = QFrame()
        frame_2_leste.setFrameShape(QFrame.Shape.Box)
        frame_2_leste.setContentsMargins(0, 80, 0, 0)
        frame_2_leste.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_2_leste.setFixedSize(1091, 1280)
        self.list_painel.append(frame_2_leste)
        h_layout_unidades_internacao_1.addWidget(frame_2_leste)
        titulo_2_leste = QtWidgets.QLabel(' 2º ANDAR \n ALA LESTE', frame_2_leste)
        titulo_2_leste.setFixedWidth(1091)
        titulo_2_leste.setFixedHeight(25)
        titulo_2_leste.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_2_leste.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_2_leste(Form, frame_2_leste)
        frame_10_norte = QFrame()
        frame_10_norte.setFrameShape(QFrame.Shape.Box)
        frame_10_norte.setContentsMargins(0, 80, 0, 0)
        frame_10_norte.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_10_norte.setFixedSize(1331, 1280)
        self.list_painel.append(frame_10_norte)
        h_layout_unidades_internacao_1.addWidget(frame_10_norte)
        titulo_10_norte = QtWidgets.QLabel(' 10º NORTE ', frame_10_norte)
        titulo_10_norte.setFixedWidth(1330)
        titulo_10_norte.setFixedHeight(20)
        titulo_10_norte.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_10_norte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_10_norte(Form, frame_10_norte)
        frame_7_leste = QFrame(frame_7_norte)
        frame_7_leste.setFrameShape(QFrame.Shape.Box)
        frame_7_leste.setContentsMargins(0, 80, 0, 0)
        frame_7_leste.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        self.list_painel.append(frame_7_leste)
        frame_7_leste.setGeometry(0, 415, 1110, 431)
        titulo_7_leste = QtWidgets.QLabel(' ALA LESTE ', frame_7_leste)
        titulo_7_leste.setFixedWidth(1110)
        titulo_7_leste.setFixedHeight(20)
        titulo_7_leste.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_7_leste.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_7_leste(Form, frame_7_leste)
        frame_8_leste = QFrame(frame_8_norte)
        frame_8_leste.setFrameShape(QFrame.Shape.Box)
        frame_8_leste.setContentsMargins(0, 80, 0, 0)
        frame_8_leste.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_8_leste.setGeometry(0, 415, 1150, 430)
        self.list_painel.append(frame_8_leste)
        titulo_8_leste = QtWidgets.QLabel(' ALA LESTE ', frame_8_leste)
        titulo_8_leste.setFixedWidth(1150)
        titulo_8_leste.setFixedHeight(20)
        titulo_8_leste.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_8_leste.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_8_leste(Form, frame_8_leste)
        frame_2_sul = QFrame(frame_2_leste)
        frame_2_sul.setFrameShape(QFrame.Shape.Box)
        frame_2_sul.setContentsMargins(0, 80, 0, 0)
        frame_2_sul.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_2_sul.setGeometry(0, 415, 1091, 430)
        self.list_painel.append(frame_2_sul)
        titulo_2_sul = QtWidgets.QLabel(' ALA SUL ', frame_2_sul)
        titulo_2_sul.setFixedWidth(1091)
        titulo_2_sul.setFixedHeight(20)
        titulo_2_sul.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_2_sul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_2_sul(Form, frame_2_sul)
        frame_6_leste = QFrame(frame_10_norte)
        frame_6_leste.setFrameShape(QFrame.Shape.Box)
        frame_6_leste.setContentsMargins(0, 80, 0, 0)
        frame_6_leste.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_6_leste.setGeometry(0, 415, 1331, 360)
        self.list_painel.append(frame_6_leste)
        titulo_6_leste = QtWidgets.QLabel(' 6º LESTE ', frame_6_leste)
        titulo_6_leste.setFixedWidth(1330)
        titulo_6_leste.setFixedHeight(20)
        titulo_6_leste.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_6_leste.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_6_leste(Form, frame_6_leste)
        frame_9_leste = QFrame(frame_7_norte)
        frame_9_leste.setFrameShape(QFrame.Shape.Box)
        frame_9_leste.setContentsMargins(0, 80, 0, 0)
        frame_9_leste.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_9_leste.setGeometry(0, 845, 1110, 435)
        self.list_painel.append(frame_9_leste)
        titulo_9_leste = QtWidgets.QLabel(' 9º LESTE - TRANSPLANTES ', frame_9_leste)
        titulo_9_leste.setFixedWidth(1110)
        titulo_9_leste.setFixedHeight(20)
        titulo_9_leste.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_9_leste.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_9_leste(Form, frame_9_leste)
        frame_8_sul = QFrame(frame_8_norte)
        frame_8_sul.setFrameShape(QFrame.Shape.Box)
        frame_8_sul.setContentsMargins(0, 80, 0, 0)
        frame_8_sul.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_8_sul.setGeometry(0, 845, 1150, 435)
        self.list_painel.append(frame_8_sul)
        titulo_8_sul = QtWidgets.QLabel(' ALA SUL ', frame_8_sul)
        titulo_8_sul.setFixedWidth(1150)
        titulo_8_sul.setFixedHeight(20)
        titulo_8_sul.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_8_sul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitora_8_sul(Form, frame_8_sul)
        frame_10_sul = QFrame(frame_2_leste)
        frame_10_sul.setFrameShape(QFrame.Shape.Box)
        frame_10_sul.setContentsMargins(0, 80, 0, 0)
        frame_10_sul.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_10_sul.setGeometry(0, 845, 1091, 435)
        self.list_painel.append(frame_10_sul)
        self.monitora_10_sul(Form, frame_10_sul)
        titulo_10_sul = QtWidgets.QLabel(' 10° SUL ', frame_10_sul)
        titulo_10_sul.setFixedWidth(1091)
        titulo_10_sul.setFixedHeight(20)
        titulo_10_sul.setStyleSheet('border-radius: 10px;border: none; background-color: rgb(127, 127, 127);color: white;')
        titulo_10_sul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_dados = QFrame()
        frame_dados.setFrameShape(QFrame.Shape.Box)
        frame_dados.setContentsMargins(0, 80, 0, 0)
        frame_dados.setStyleSheet('QFrame { background-color: white; border: none; }')
        frame_dados.setFixedSize(500, 1280)
        h_layout_unidades_internacao_1.addWidget(frame_dados)
        adulto_label2 = QtWidgets.QLabel('ADULTO', frame_dados)
        adulto_label2.setGeometry(30, 30, 230, 30)
        font = QtGui.QFont()
        font.setPointSize(30)
        adulto_label2.setFont(font)
        adulto_label2.setStyleSheet('background-color: rgb(250, 250, 250); color: black; font-weight: bold; border: none;')
        adulto_label2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        pediatrica_label2 = QtWidgets.QLabel('INFANTIL', frame_dados)
        pediatrica_label2.setGeometry(30, 200, 230, 30)
        font = QtGui.QFont()
        font.setPointSize(30)
        pediatrica_label2.setFont(font)
        pediatrica_label2.setStyleSheet('background-color: rgb(250, 250, 250); color: black; font-weight: bold; border: none;')
        pediatrica_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.qt_int_adulto_total2!= 0 and self.qt_int_adulto2!= 0:
            valor = '{:.2f} %'.format(self.qt_int_adulto2 / self.qt_int_adulto_total2 * 100)
        else:  # inserted
            valor = '0.0 %'
        qt_adulto_label2 = QtWidgets.QLabel(valor, frame_dados)
        qt_adulto_label2.setGeometry(300, 30, 50, 30)
        qt_adulto_label2.setStyleSheet(' color: rgb(250, 250, 250);background-color: black;font-size: 100 px;font-weight: bold; border: none; ')
        qt_adulto_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.qt_int_ped2!= 0 and self.qt_int_ped_total2!= 0:
            valor = '{:.2f} %'.format(self.qt_int_ped2 / self.qt_int_ped_total2 * 100)
        else:  # inserted
            valor = '0.0 %'
        qt_ped_label2 = QtWidgets.QLabel(valor, frame_dados)
        qt_ped_label2.setGeometry(300, 200, 50, 30)
        qt_ped_label2.setStyleSheet(' color: rgb(250, 250, 250);background-color: black;font-size: 100 px;font-weight: bold; border: none; ')
        qt_ped_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_global_leitos = QFrame(frame_dados)
        frame_global_leitos.setFrameShape(QFrame.Shape.Box)
        frame_global_leitos.setContentsMargins(0, 80, 0, 0)
        frame_global_leitos.setStyleSheet('QFrame { background-color: white; border: 2px solid black; border-radius: 0px;}')
        frame_global_leitos.setGeometry(30, 415, 273, 543)
        self.plot_frame = QFrame(frame_10_norte)
        self.plot_frame.setFrameShape(QFrame.Shape.Box)
        self.plot_frame.setContentsMargins(0, 80, 0, 0)
        self.plot_frame.setStyleSheet('QFrame { background-color: white; border: 2px solid black; }')
        self.plot_frame.setGeometry(0, 775, 1330, 435)
        title_label = QLabel('RANKING DE SETORES COM MAIS LEITOS VAGOS', self.plot_frame)
        title_label.setStyleSheet('font-size: 16px; font-weight: bold;border:none;')
        title_label.setGeometry(3, 5, 1325, 20)
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.plot()
        from global_leitos import Ui_Form
        self.global_leitos = Ui_Form()
        self.global_leitos.setupUi(Form, frame_global_leitos, self)
        self.monitora = False
        self.frames_painel = []
        self.frames_painel2 = []
        self.size = h_layout_terapia_intensiva.sizeHint()
        self.size2 = h_layout_unidades_internacao_1.sizeHint()
        for frame in self.frame_terapia_intensiva.findChildren(QtWidgets.QFrame):
            self.frames_painel.append((frame, frame.size()))
            for widget in frame.findChildren(QtWidgets.QWidget):
                self.frames_painel2.append((frame, widget, widget.size(), widget.pos()))
        for frame in self.frame_unidades_internacao_1.findChildren(QtWidgets.QFrame):
            self.frames_painel.append((frame, frame.size()))
            for widget in frame.findChildren(QtWidgets.QWidget):
                self.frames_painel2.append((frame, widget, widget.size(), widget.pos()))
        self.abri_cti(self.form, 'CTI PEDIÁTRICO - 06N')
        if self.dept!= 'Telespectador':
            self.btn_alterar.show()
            self.btn_alta.show()
            self.btn_realocar.show()
        self.tabela_grade.show()
        self.BARRADEPESQUISA.show()
        self.help_sccrol_painel = False

    def plot(self):
        categories = ['2° LESTE', '2° SUL', '7° NORTE', '10° NORTE', '8° LESTE', '6° LESTE', '8° NORTE', 'UCO', 'UTI PS', '9° LESTE', '7° LESTE', '8° SUL', '3° LESTE', 'CTI PED']
        values = [self.qt_vagos_2leste, self.qt_vagos_2sul, self.qt_vagos_7norte, self.qt_vagos_10norte, self.qt_vagos_8leste, self.qt_vagos_6leste, self.qt_vagos_8norte, self.qt_vagos_uco, self.qt_vagos_uti_ps, self.qt_vagos_9leste, self.qt_vagos_7leste, self.qt_vagos_8sul, self.qt_vagos_3leste, self.qt_vagos_cti_ped]
        sorted_data = sorted(zip(categories, values), key=lambda x: x[1], reverse=True)
        sorted_categories = [x[0] for x in sorted_data]
        sorted_values = [x[1] for x in sorted_data]
        self.plot_widget = pg.PlotWidget()
        self.plot_frame.layout = QVBoxLayout(self.plot_frame)
        self.plot_frame.layout.addWidget(self.plot_widget)
        x = np.arange(len(sorted_categories))
        self.plot_widget.clear()
        self.plot_widget.setBackground('w')
        self.plot_widget.getPlotItem().getAxis('bottom').setTicks([[(i, v) for i, v in enumerate(sorted_categories)]])
        self.plot_widget.getPlotItem().getAxis('left').setLabel('Valores')
        self.plot_widget.getPlotItem().showGrid(True, True)
        bar = pg.BarGraphItem(x=x, height=sorted_values, width=0.6, brush='b')
        self.plot_widget.addItem(bar)
        tooltips = pg.TextItem(anchor=(0, 1))
        self.plot_widget.addItem(tooltips)

    def conferir_ocupacao_cti(self):
        grade = self.codigo_ala
        qt = 0
        Form = self.form
        colum = 0
        total = 0
        list = ['CTI PEDIÁTRICO - 06N', 'UNIDADE DE INTERNAÇÃO CORONARIANA - 03N', 'UTI - PRONTO SOCORRO', 'CTI ADULTO - 03L']
        for funcao in list:
            self.abri_cti(Form, funcao)
            total += 1
            for colum in range(self.tabela_grade.columnCount()):
                item_pac = self.tabela_grade.horizontalHeaderItem(colum)
                if item_pac.text() == 'STATUS DO LEITO':
                    for row in range(self.tabela_grade.rowCount()):
                        item = self.tabela_grade.item(row, colum).text()
                        if item == 'OCUPADO':
                            qt += 1
                    break
        valor = '{:.2f} %'.format(qt / total * 100)
        self.codigo_ala = grade
        return valor

    def conferir_ocupacao_enfermaria(self):
        grade = self.codigo_ala
        Form = self.form
        qt = 0
        total = 0
        colum = 0
        list = ['UNIDADE DE INTERNAÇÃO - 06L', 'UNIDADE DE INTERNAÇÃO - 10N', 'UNIDADE DE INTERNAÇÃO - 02L', 'UNIDADE DE INTERNAÇÃO - 02S', 'UNIDADE DE INTERNAÇÃO - 07L', 'UNIDADE DE INTERNAÇÃO - 07N', 'UNIDADE DE INTERNAÇÃO - 08S', 'UNIDADE DE INTERNAÇÃO - 08L', 'UNIDADE DE INTERNAÇÃO - 08N', 'UNIDADE DE INTERNAÇÃO - 09L']
        for funcao in list:
            self.abri_cti(Form, funcao)
            total += 1
            for colum in range(self.tabela_grade.columnCount()):
                item_pac = self.tabela_grade.horizontalHeaderItem(colum)
                if item_pac.text() == 'STATUS DO LEITO':
                    for row in range(self.tabela_grade.rowCount()):
                        item = self.tabela_grade.item(row, colum).text()
                        if item == 'OCUPADO':
                            qt += 1
                    break
        valor = '{:.2f} %'.format(qt / total * 100)
        self.codigo_ala = grade
        if self.codigo_ala == 29:
            self.abri_cti(Form, 'CTI PEDIÁTRICO - 06N')
        if self.codigo_ala == 23:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO CORONARIANA - 03N')
        if self.codigo_ala == 30:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 06L')
        if self.codigo_ala == 36:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 10N')
        if self.codigo_ala == 169:
            self.abri_cti(Form, 'UTI - PRONTO SOCORRO')
        if self.codigo_ala == 22:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 02L')
        if self.codigo_ala == 21:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 02S')
        if self.codigo_ala == 32:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 07L')
        if self.codigo_ala == 31:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 07N')
        if self.codigo_ala == 33:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08S')
        if self.codigo_ala == 34:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08L')
        if self.codigo_ala == 193:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08N')
        if self.codigo_ala == 35:
            self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 09L')
        if self.codigo_ala == 24:
            self.abri_cti(Form, 'CTI ADULTO - 03L')
        return valor

    def novas_unidades(self):
        list = ['tabela_2_sul', 'tabela_6_leste', 'tabela_10°_norte', 'tabela_cti_ps', 'tabela_2_leste', 'tabela_cti_ped', 'tabela_7_leste', 'tabela_8_sul', 'tabela_7_norte', 'tabela_8_leste', 'tabela_8_norte', 'tabela_uco', 'tabela_9_leste', 'tabela_3_leste']
        try:
            connection = mysql.connector.connect(host='localhost', user='root', password='camileejose', database='grade')
            cursor = connection.cursor()
            cursor.execute('SHOW TABLES')
            tables = cursor.fetchall()
            for i, table in enumerate(tables):
                if table[0] not in list:
                    button = QtWidgets.QPushButton(f'{table[0].upper()}')
                    button.setFixedSize(71, 21)
                    self.button_layout.addWidget(button)
                    button.clicked.connect(lambda checked, text=table[0]: self.abrir_nova_unidade(text))
                    button.setStyleSheet('\n                                    QPushButton {\n                                        border: 2px solid #2E3D48;\n                                        border-radius: 10px;\n                                        background-color: #FFFFFF;\n                                        color: #2E3D48;\n                                    }\n\n                                    QPushButton:hover {\n                                        background-color: #DDDDDD;  /* Change this to your desired hover color */\n                                        color: rgb(0, 0, 0);\n                                    }\n\n                                    QPushButton:pressed {\n                                        background-color: #2E3D48;  /* Change this to your desired pressed color */\n                                        color: #FFFFFF;\n                                    }\n                                ')
            connection.close()
        except mysql.connector.Error as error:
            print('Erro ao conectar ao MySQL:', error)

    def abrir_nova_unidade(self, tabela):
        conexao = mysql.connector.connect(host='localhost', user='root', password='camileejose', database='grade')
        cursor = conexao.cursor()
        comando = f'SELECT * FROM {tabela}'
        cursor.execute(comando)
        leitura = cursor.fetchall()
        for row, linha in enumerate(leitura):
            if row == 0:
                Colum_total = len(linha) + 1
                self.tabela_grade.setColumnCount(Colum_total)
                for column, valor in enumerate(linha):
                    if column == 0:
                        continue
                    self.ala = f'{tabela}'
                    item = QtWidgets.QTableWidgetItem()
                    font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
                    font.setPointSize(8)
                    font.setBold(True)
                    font.setWeight(75)
                    item.setFont(font)
                    self.tabela_grade.setHorizontalHeaderItem(column, item)
                    _translate = QtCore.QCoreApplication.translate
                    item = self.tabela_grade.horizontalHeaderItem(column)
                    item.setText(_translate('Form', f'{valor}'))
                    self.TITULO_CTI.setText(_translate('Form', f'{tabela}'))
                    self.atualiza_cti(f'{tabela}')
                    self.timer.stop()
                    self.timer_post.stop()
                    self.timer_mysql.stop()
                    self.temporizador()
            else:  # inserted
                break
        if self.monitora == True:
            self.frame_do_monitoramento.hide()
            self.monitoramento(self.form)
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
        if not self.frame_do_grafico.isHidden():
            self.canvas.show()
            self.plot_pie_chart()
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()