from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QComboBox, QVBoxLayout
from GRADE import Ui_CTI_PED
from PyQt6.QtCore import QDateTime, QSettings, QStandardPaths, QFile, Qt
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication
import datetime
import sys
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import mysql.connector

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class CustomTableWidget(QTableWidget):

    def __init__(self, dept, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dept = dept

    def edit(self, index, trigger, event):
        if self.dept == 'PS':
            if index.column() == 10 or index.column() == 11 or index.column() == 12:
                return False
        return super().edit(index, trigger, event)

class Ui_Demanda(QtWidgets.QMainWindow):

    def setupUi(self, MainWindow, departamento=None, user=None, nome_user=None):
        #Define posição inicial na tabela
        self.posicao_inicial_row = 0
        self.posicao_inicial_colum = 0
        self.selection = None

        #Nome do Usuário
        self.nome_user = nome_user

        #Tela atual
        self.t = 'Demanda'

        # Login do usuário
        self.user = user

        #Tabela atual
        self.tabela_atual = 'tabela_demanda_ps'

        #Janela Principal
        self.janela_CTI_PED = QtWidgets.QMainWindow()
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)

        MainWindow.setObjectName('MainWindow')
        MainWindow.showMaximized()
        self.variavel = 0
        self.clicked = False

        # Define o ícone da janela principal
        icon = QIcon('icone_p_eUO_icon.ico')
        MainWindow.setWindowIcon(icon)
        self.mainwindow = MainWindow
        self.dept = departamento
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName('centralwidget')

        #Status das Pop-ups
        self.cadastro_Aberta = False
        self.reserva_Aberta = False
        self.procurar_Aberta = False
        self.conta_do_usuario_Aberta = False
        self.config_Aberta = False

        #Layout da Tela
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName('horizontalLayout')

        #Frame principal da tela
        self.frame = QtWidgets.QFrame(parent=MainWindow)
        self.frame.setStyleSheet('background-color: #5DADE2;')
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.horizontalLayout.addWidget(self.frame)

        #Todo o layout do gráfico
        self.frame_do_grafico = QtWidgets.QFrame(parent=MainWindow)
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

        screen = QGuiApplication.primaryScreen()
        size = screen.size()
        self.btn_width = size.width() - 206
        tabela_width = size.width() - 226
        tabela_height = size.height() - 338

        # Tabela de demandas
        self.tabelademan = CustomTableWidget(self.dept, parent=self.frame)
        self.tabelademan.setGeometry(QtCore.QRect(0, 125, tabela_width, tabela_height))
        self.tabelademan.setStyleSheet('background-color: rgb(255, 255, 255);gridline-color: black;')
        self.tabelademan.setObjectName('tabelademan')
        self.tabelademan.setColumnCount(15)
        self.tabelademan.setRowCount(0)

        self.tabelademan.cellClicked.connect(self.close_frame)

        # Ativa as funções para bloquear a atualização da tabela.
        self.barra = self.tabelademan.horizontalScrollBar().value()
        self.barra_vertical = self.tabelademan.verticalScrollBar().value()
        self.tabelademan.horizontalScrollBar().valueChanged.connect(self.check_scrollbar_value)
        self.tabelademan.verticalScrollBar().valueChanged.connect(self.check_scrollbar_value)

        # Definindo a geometria do sidebar
        screen = QGuiApplication.primaryScreen()
        size = screen.size()
        sidebar_width = 200
        sidebar_x = size.width() - sidebar_width
        sidebar_y = 40
        sidebar_height = self.height() - sidebar_y

        self.sidebar = QtWidgets.QFrame(parent=MainWindow)
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

        sidebar_width = 40
        sidebar_x = size.width() - sidebar_width
        sidebar_y = 40
        icon = QtGui.QIcon('do-utilizador.ico')
        pixmap = icon.pixmap(40, 40)

        self.label_icone = ClickableLabel(parent=self.frame)
        self.label_icone.setPixmap(pixmap)
        self.label_icone.setGeometry(QtCore.QRect(sidebar_x, 3, 40, 40))
        self.label_icone.setStyleSheet('border-radius: 10px;')
        self.label_icone.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_icone.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)

        tooltip_text = user
        self.label_icone.setToolTip(tooltip_text)
        self.label_icone.clicked.connect(self.onIconClick)

        # Adicionando botões à barra lateral
        if self.dept == 'NIR' or self.dept == 'Administrador':
            self.usuario = QtWidgets.QPushButton('USUÁRIO', self.sidebar)
            self.usuario.clicked.connect(lambda: self.abrir_conta_do_usuario(MainWindow))
            self.usuario.setStyleSheet(
                '\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

        self.procura_pac = QtWidgets.QPushButton('PROCCURAR PACIENTE', self.sidebar)
        self.procura_pac.clicked.connect(lambda: self.abrir_procura_pac(MainWindow))
        self.procura_pac.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

        self.configura = QtWidgets.QPushButton('CONFIGURAÇÕES', self.sidebar)
        self.configura.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')
        self.configura.clicked.connect(lambda: self.abrir_configuracoes(MainWindow))

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
            if item[i] != ' ' and space_atual == 0 or space_atual == quantidade_space:
                login += item[i]
            if space_atual != 0 and space_atual != quantidade_space and (item[i] != ' ') and (analise == 0):
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

        if self.dept == 'NIR' or self.dept == 'Administrador':
            self.usuario.setGeometry(10, 200, 180, 30)

        self.procura_pac.setGeometry(10, 250, 180, 30)

        #Tabela alternativa para analise de dados
        self.tabela_alt = QtWidgets.QTableWidget()
        self.setCentralWidget(self.frame)

        #Itens da tabela principal
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)

        self.tabelademan.setHorizontalHeaderItem(14, item)
        self.tabelademan.horizontalHeader().setDefaultSectionSize(140)
        self.tabelademan.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        self.tabelademan.currentCellChanged.connect(self.get_current_position)
        self.tabelademan.itemSelectionChanged.connect(self.get_current_position)

        #Line edit para pesquisa de pasciente
        self.editbarra = QtWidgets.QLineEdit(parent=self.frame)
        self.editbarra.setObjectName('editbarra')
        self.editbarra.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.editbarra.setPlaceholderText('Pesquisar Paciente')
        self.editbarra.textChanged.connect(self.pesquisar)
        icon = QIcon('lupa.ico')
        self.editbarra.addAction(icon, QtWidgets.QLineEdit.ActionPosition.LeadingPosition)

        self.labeltitulo = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.labeltitulo.setFont(font)
        self.labeltitulo.setObjectName('labeltitulo')

        self.btndeman = QtWidgets.QPushButton('SOLICITAÇÃO DE LEITOS', parent=self.frame)
        self.btndeman.setGeometry(QtCore.QRect(0, 0, 100, 23))
        self.btndeman.setObjectName('btndeman')
        self.btndeman.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }F\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

        self.btngraficos = QtWidgets.QPushButton('GRÁFICOS', parent=self.frame)
        self.btngraficos.setObjectName('btngraficos')
        self.btngraficos.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

        self.btnsair = QtWidgets.QPushButton('SAIR', parent=self.frame)
        self.btnsair.setObjectName('btnsair')
        self.btnsair.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')
        self.btnsair.clicked.connect(self.finalizar_operacao)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1332, 21))
        self.menubar.setObjectName('menubar')
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.tabelademan.setCurrentCell(self.tabelademan.rowCount() - 1, 0)
        self.frame.mousePressEvent = lambda event: self.toggle_frame_visibility(self.sidebar)
        _translate = QtCore.QCoreApplication.translate

        if self.dept == 'NIR' or self.dept == 'Administrador':
            self.btnregis = QtWidgets.QPushButton(parent=self.frame)
            self.btnregis.setGeometry(QtCore.QRect(self.btn_width, 123, 131, 31))
            self.btnregis.setObjectName('btnregis')
            self.btnregis.clicked.connect(lambda: self.abrir_cadastro(MainWindow))
            self.btnregis.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')

            self.btnalterar = QtWidgets.QPushButton(parent=self.frame)
            self.btnalterar.setGeometry(QtCore.QRect(self.btn_width, 160, 131, 31))
            self.btnalterar.setObjectName('btnalterar')
            self.btnalterar.clicked.connect(self.altera_table)
            self.btnalterar.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')
            self.editable = False

            self.btnexclu = QtWidgets.QPushButton(parent=self.frame)
            self.btnexclu.setGeometry(QtCore.QRect(self.btn_width, 200, 131, 31))
            self.btnexclu.setObjectName('btnexclu')
            self.btnexclu.clicked.connect(self.excluir_demanda)
            self.btnexclu.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')

            self.btn_reservar_leito = QtWidgets.QPushButton(parent=self.frame)
            self.btn_reservar_leito.setGeometry(QtCore.QRect(self.btn_width, 240, 131, 31))
            self.btn_reservar_leito.setObjectName('btn_reservar_leito')
            self.btn_reservar_leito.setText(_translate('MainWindow', 'RESERVAR LEITO'))
            self.btn_reservar_leito.clicked.connect(lambda: self.reservar_leito(MainWindow))
            self.btn_reservar_leito.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

            self.btn_grade = QtWidgets.QPushButton(parent=self.frame)
            self.btn_grade.setGeometry(QtCore.QRect(105, 0, 100, 23))
            self.btn_grade.setObjectName('btn_reservar_leito')
            self.btn_grade.setText(_translate('MainWindow', 'GRADE'))
            self.btn_grade.clicked.connect(lambda: self.abrir_grade(MainWindow))
            self.btn_grade.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

            self.btn_PRONTO_SOCORRO = QtWidgets.QPushButton(parent=self.frame)
            self.btn_PRONTO_SOCORRO.setGeometry(QtCore.QRect(0, 100, 120, 23))
            self.btn_PRONTO_SOCORRO.setObjectName('btn_PRONTO_SOCORRO')
            self.btn_PRONTO_SOCORRO.setText(_translate('MainWindow', 'PRONTO SOCORRO'))
            self.btn_PRONTO_SOCORRO.clicked.connect(lambda: self.setupUi(MainWindow, self.dept, self.user, self.nome_user))
            self.btn_PRONTO_SOCORRO.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

            self.btn_ALTAS_CTI = QtWidgets.QPushButton(parent=self.frame)
            self.btn_ALTAS_CTI.setGeometry(QtCore.QRect(125, 100, 100, 23))
            self.btn_ALTAS_CTI.setObjectName('btn_ALTAS_CTI')
            self.btn_ALTAS_CTI.setText(_translate('MainWindow', "ALTA CTI'S"))
            self.btn_ALTAS_CTI.clicked.connect(lambda: self.abrir_tabela_Alta_CTI(MainWindow))
            self.btn_ALTAS_CTI.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

            self.btn_AGENDA_BLOCO = QtWidgets.QPushButton(parent=self.frame)
            self.btn_AGENDA_BLOCO.setGeometry(QtCore.QRect(230, 100, 100, 23))
            self.btn_AGENDA_BLOCO.setObjectName('btn_AGENDA_BLOCO')
            self.btn_AGENDA_BLOCO.setText(_translate('MainWindow', 'AGENDA BLOCO'))
            self.btn_AGENDA_BLOCO.clicked.connect(lambda: self.abrir_tabela_Agenda_Bloco(MainWindow))
            self.btn_AGENDA_BLOCO.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

            self.btn_HEMODINÂMICA = QtWidgets.QPushButton(parent=self.frame)
            self.btn_HEMODINÂMICA.setGeometry(QtCore.QRect(335, 100, 100, 23))
            self.btn_HEMODINÂMICA.setObjectName('btn_HEMODINÂMICA')
            self.btn_HEMODINÂMICA.setText(_translate('MainWindow', 'HEMODINÂMICA'))
            self.btn_HEMODINÂMICA.clicked.connect(lambda: self.abrir_tabela_Hemodinamica(MainWindow))
            self.btn_HEMODINÂMICA.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

            self.btn_INTER_TRAN_EXTE = QtWidgets.QPushButton(parent=self.frame)
            self.btn_INTER_TRAN_EXTE.setGeometry(QtCore.QRect(440, 100, 200, 23))
            self.btn_INTER_TRAN_EXTE.setObjectName('btn_INTER_TRAN_EXTE')
            self.btn_INTER_TRAN_EXTE.setText(_translate('MainWindow', 'INTERNAÇÕES E TRANSF. EXTERNAS'))
            self.btn_INTER_TRAN_EXTE.clicked.connect(lambda: self.abrir_tabela_Inter_Tran_Exte(MainWindow))
            self.btn_INTER_TRAN_EXTE.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

            self.btn_TRANS_INT = QtWidgets.QPushButton(parent=self.frame)
            self.btn_TRANS_INT.setGeometry(QtCore.QRect(645, 100, 160, 23))
            self.btn_TRANS_INT.setObjectName('btn_TRANS_INT')
            self.btn_TRANS_INT.setText(_translate('MainWindow', 'TRANSFERÊNCIAS INTERNAS'))
            self.btn_TRANS_INT.clicked.connect(lambda: self.abrir_tabela_Tran_Inte(MainWindow))
            self.btn_TRANS_INT.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

            self.btn_ONCO_HEMATO_PED = QtWidgets.QPushButton(parent=self.frame)
            self.btn_ONCO_HEMATO_PED.setGeometry(QtCore.QRect(810, 100, 130, 23))
            self.btn_ONCO_HEMATO_PED.setObjectName('btn_ONCO_HEMATO_PED')
            self.btn_ONCO_HEMATO_PED.setText(_translate('MainWindow', 'ONCO HEMATO PED'))
            self.btn_ONCO_HEMATO_PED.clicked.connect(lambda: self.abrir_tabela_Onco_Hemato_Ped(MainWindow))
            self.btn_ONCO_HEMATO_PED.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

            self.btn_confirm_alta = QtWidgets.QPushButton(parent=self.frame)
            self.btn_confirm_alta.setObjectName('btn_confirm_alta')
            self.btn_confirm_alta.setText(_translate('MainWindow', 'CONFIRMAR ALTA'))
            self.btn_confirm_alta.clicked.connect(self.confirm_alta)
            self.btn_confirm_alta.setGeometry(QtCore.QRect())
            self.btn_confirm_alta.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

            self.frame_personalisa = QtWidgets.QFrame(parent=self.frame)
            self.frame_personalisa.setStyleSheet('\n                                QFrame  {\n                                    background-color: #FFFFFF;\n                                    border-top-right-radius: 20px;\n                                    border-bottom-right-radius: 20px;\n                                    border-left: 1px solid black;\n                                }\n                            ')
            self.frame_personalisa.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.frame_personalisa.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.frame_personalisa.setObjectName('frame_box')
            self.frame_personalisa.hide()

            self.btn_filtros = QtWidgets.QPushButton('▼ Selecione uma Data ', parent=self.frame)
            self.btnfechar = QtWidgets.QPushButton(' X ', parent=self.frame)
            self.btn_filtros.setFocus()
            self.btnfechar.setStyleSheet('QPushButton {    border-top-right-radius: 10px;    border-bottom-right-radius: 10px;    border-top-left-radius: 0px;    border-bottom-left-radius: 0px;    background-color: #FFFFFF;    color: #2E3D48;    border: 2px solid #2E3D48;}QPushButton:pressed {    background-color: #2E3D48;    color: #FFFFFF;}')

            current_datetime = QDateTime.currentDateTime()
            formatted_date = current_datetime.toString('yyyy')
            formatted_date2 = current_datetime.addYears(-1).toString('yyyy')

            self.frame_box = QtWidgets.QFrame(parent=self.frame)
            self.frame_box.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
            self.frame_box.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.frame_box.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            colo = '\n                                        QPushButton {\n\n                                        background-color: #FFFFFF;\n                                        color: #2E3D48;\n                                        border-radius: 10px;\n                                        border-color: transparent;\n                                        }\n                                        QPushButton:hover {\n                                        background-color: #c0c0c0;\n                                        color: #000000;\n                                        }\n                                        QPushButton:pressed {\n                                            background-color: #2E3D48;\n                                            color: #FFFFFF;\n                                        }\n                                    '

            self.btn_hoje = QtWidgets.QPushButton('Hoje', self.frame_box)
            self.btn_hoje.setGeometry(QtCore.QRect(0, 0, 150, 20))
            self.btn_hoje.setStyleSheet(colo)

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
            self.btn_filtros.clicked.connect(self.abrir_items)

            self.btn_7.clicked.connect(lambda: self.filtros(2))
            self.btn_30.clicked.connect(lambda: self.filtros(3))
            self.btn_ano.clicked.connect(lambda: self.filtros(4))
            self.btn_2ano.clicked.connect(lambda: self.filtros(5))
            self.btn_hoje.clicked.connect(lambda: self.filtros(1))
            self.btnfechar.clicked.connect(lambda: self.filtros(0))
            self.btn_personalisa.clicked.connect(self.abrir_personalisa)
            self.btn_personalisa.setGeometry(QtCore.QRect(0, 100, 150, 20))

            self.day = 'ONTEM'
            self.btnfechar.hide()
            self.frame_box.hide()
            self.btn_filtros.setStyleSheet('QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')
            ccurrent_datetime = QtCore.QDateTime.currentDateTime()

            self.borda_inicio = QtWidgets.QFrame(parent=self.frame_personalisa)
            self.borda_inicio.setStyleSheet('border: 2px solid black; border-radius: 10px; background-color: #FFFFFF;')
            self.borda_inicio.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.borda_inicio.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.borda_inicio.setObjectName('frame')
            self.borda_inicio.setGeometry(QtCore.QRect(8, 25, 140, 29))

            self.data_inicio = QtWidgets.QDateEdit(parent=self.frame_personalisa)
            self.data_inicio.setGeometry(QtCore.QRect(10, 30, 130, 20))
            self.data_inicio.setDateTime(ccurrent_datetime)
            self.data_inicio.setCalendarPopup(True)
            self.data_inicio.setStyleSheet('border_color: #FFFFFF; border-radius: 10px; background-color: #FFFFFF;')
            self.data_inicio.setObjectName('data_inicio')

            self.inicio = QtWidgets.QLabel('Depois de ', self.frame_personalisa)
            self.inicio.setStyleSheet('font-size: 13px; margin: 0; padding: 0;border: none; background-color: #FFFFFF')
            self.inicio.setGeometry(15, 20, 63, 13)

            self.borda_fim = QtWidgets.QFrame(parent=self.frame_personalisa)
            self.borda_fim.setStyleSheet('border: 2px solid black; border-radius: 10px; background-color: #FFFFFF;')
            self.borda_fim.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.borda_fim.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.borda_fim.setObjectName('frame')
            self.borda_fim.setGeometry(QtCore.QRect(8, 80, 140, 29))

            self.data_final = QtWidgets.QDateEdit(parent=self.frame_personalisa)
            self.data_final.setGeometry(QtCore.QRect(10, 85, 130, 20))
            self.data_final.setStyleSheet('border_color: #FFFFFF; border-radius: 10px; background-color: #FFFFFF;')
            self.data_final.setDateTime(QtCore.QDateTime.currentDateTime())
            self.data_final.setCalendarPopup(True)
            self.data_final.setObjectName('data_inicio')

            self.fim = QtWidgets.QLabel('Antes de ', self.frame_personalisa)
            self.fim.setStyleSheet('font-size: 13px; margin: 0; padding: 0;border: none; background-color: #FFFFFF')
            self.fim.setGeometry(15, 75, 57, 13)

            self.aplicar = QtWidgets.QPushButton('Aplicar', parent=self.frame_personalisa)
            self.aplicar.setGeometry(QtCore.QRect(165, 100, 101, 23))
            self.aplicar.clicked.connect(lambda: self.filtros(6))
            self.aplicar.setStyleSheet('QPushButton {\n                border: 2px solid #000000;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')

            self.labeltitulo.setGeometry(QtCore.QRect(540, 29, 400, 31))
            self.editbarra.setGeometry(QtCore.QRect(30, 65, 360, 21))
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 150, 23))
            self.btnfechar.setGeometry(QtCore.QRect(540, 65, 30, 23))
            self.frame_personalisa.setGeometry(QtCore.QRect(569, 89, 270, 125))
            self.frame_box.setGeometry(QtCore.QRect(420, 89, 150, 125))
            self.btngraficos.setGeometry(QtCore.QRect(210, 0, 100, 23))
            self.btngraficos.clicked.connect(lambda: self.abrir_gráficos(MainWindow))
            self.btnsair.setGeometry(QtCore.QRect(315, 0, 100, 23))
            self.retranslateUi_ps(MainWindow)

            self.atualiza_tabela_demandas('tabela_demanda_ps')
            self.temporizador(MainWindow)
        if self.dept == 'Pronto Socorro':
            self.procura_pac.hide()
            self.btngraficos.hide()

            self.btngraficos.setGeometry(QtCore.QRect(210, 0, 100, 23))
            self.btnsair.setGeometry(QtCore.QRect(105, 0, 100, 23))
            self.editbarra.setGeometry(QtCore.QRect(30, 100, 291, 21))
            self.labeltitulo.setGeometry(QtCore.QRect(540, 29, 400, 31))

            self.btnregis = QtWidgets.QPushButton(parent=self.frame)
            self.btnregis.setGeometry(QtCore.QRect(self.btn_width, 123, 131, 31))
            self.btnregis.setObjectName('btnregis')
            self.btnregis.clicked.connect(lambda: self.abrir_cadastro(MainWindow))
            self.btnregis.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')

            self.btnalterar = QtWidgets.QPushButton(parent=self.frame)
            self.btnalterar.setGeometry(QtCore.QRect(self.btn_width, 160, 131, 31))
            self.btnalterar.setObjectName('btnalterar')
            self.btnalterar.clicked.connect(self.altera_table)
            self.btnalterar.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')
            self.editable = False

            self.btnexclu = QtWidgets.QPushButton(parent=self.frame)
            self.btnexclu.setGeometry(QtCore.QRect(self.btn_width, 200, 131, 31))
            self.btnexclu.setObjectName('btnexclu')
            self.btnexclu.clicked.connect(self.excluir_demanda)
            self.btnexclu.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')

            self.retranslateUi_ps(MainWindow)
            self.atualiza_tabela_demandas('tabela_demanda_ps')
        if self.dept == 'Bloco Cirúrgico':
            self.procura_pac.hide()
            self.btngraficos.hide()

            self.btnsair.setGeometry(QtCore.QRect(105, 0, 100, 23))
            self.editbarra.setGeometry(QtCore.QRect(30, 100, 291, 21))
            self.labeltitulo.setGeometry(QtCore.QRect(540, 29, 400, 31))

            self.temporizador(MainWindow)
            self.abrir_tabela_Agenda_Bloco(MainWindow)

            self.btndeman.clicked.connect(lambda: self.abrir_tabela_Agenda_Bloco(MainWindow))

            self.btnregis = QtWidgets.QPushButton('REGISTRAR DEMANDA', parent=self.frame)
            self.btnregis.setGeometry(QtCore.QRect(self.btn_width, 123, 131, 31))
            self.btnregis.setObjectName('btnregis')
            self.btnregis.clicked.connect(lambda: self.abrir_cadastro(MainWindow))
            self.btnregis.setStyleSheet('\n                                    QPushButton {\n                                        border: 2px solid #2E3D48;\n                                        border-radius: 10px;\n                                        background-color: #FFFFFF;\n                                        color: #2E3D48;\n                                    }\n                                    QPushButton:pressed {\n                                        background-color: #2E3D48;\n                                        color: #FFFFFF;\n                                    }\n                                ')
            self.btnregis.clicked.connect(lambda: self.abrir_cadastro(MainWindow))

            self.btnalterar = QtWidgets.QPushButton('ALTERAR DEMANDA', parent=self.frame)
            self.btnalterar.setGeometry(QtCore.QRect(self.btn_width, 160, 131, 31))
            self.btnalterar.setObjectName('btnalterar')
            self.btnalterar.clicked.connect(self.altera_table)
            self.btnalterar.setStyleSheet('\n                                    QPushButton {\n                                        border: 2px solid #2E3D48;\n                                        border-radius: 10px;\n                                        background-color: #FFFFFF;\n                                        color: #2E3D48;\n                                    }\n                                    QPushButton:pressed {\n                                        background-color: #2E3D48;\n                                        color: #FFFFFF;\n                                    }\n                                ')
            self.editable = False

            self.btnexclu = QtWidgets.QPushButton('EXCLUIR DEMANDA', parent=self.frame)
            self.btnexclu.setGeometry(QtCore.QRect(self.btn_width, 200, 131, 31))
            self.btnexclu.setObjectName('btnexclu')
            self.btnexclu.clicked.connect(self.excluir_demanda)
            self.btnexclu.setStyleSheet('\n                                    QPushButton {\n                                        border: 2px solid #2E3D48;\n                                        border-radius: 10px;\n                                        background-color: #FFFFFF;\n                                        color: #2E3D48;\n                                    }\n                                    QPushButton:pressed {\n                                        background-color: #2E3D48;\n                                        color: #FFFFFF;\n                                    }\n                                ')
        if self.dept == 'Terapía Intensiva':
            self.btn_confirm_alta = QtWidgets.QPushButton(parent=self.frame)
            self.btn_confirm_alta.setObjectName('btn_confirm_alta')
            self.btn_confirm_alta.setText(_translate('MainWindow', 'CONFIRMAR ALTA'))
            self.btn_confirm_alta.clicked.connect(self.confirm_alta)
            self.btn_confirm_alta.setGeometry(QtCore.QRect())
            self.btn_confirm_alta.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }')

            self.procura_pac.hide()
            self.btngraficos.hide()
            self.btnsair.setGeometry(QtCore.QRect(105, 0, 100, 23))
            self.editbarra.setGeometry(QtCore.QRect(30, 100, 291, 21))
            self.labeltitulo.setGeometry(QtCore.QRect(540, 29, 400, 31))
            self.temporizador(MainWindow)
            self.abrir_tabela_Alta_CTI(MainWindow)

            self.btnregis = QtWidgets.QPushButton('REGISTRAR DEMANDA', parent=self.frame)
            self.btnregis.setGeometry(QtCore.QRect(self.btn_width, 123, 131, 31))
            self.btnregis.setObjectName('btnregis')
            self.btnregis.clicked.connect(lambda: self.abrir_cadastro(MainWindow))
            self.btnregis.setStyleSheet('\n                                    QPushButton {\n                                        border: 2px solid #2E3D48;\n                                        border-radius: 10px;\n                                        background-color: #FFFFFF;\n                                        color: #2E3D48;\n                                    }\n                                    QPushButton:pressed {\n                                        background-color: #2E3D48;\n                                        color: #FFFFFF;\n                                    }\n                                ')
            self.btnregis.clicked.connect(lambda: self.abrir_cadastro(MainWindow))

            self.btnalterar = QtWidgets.QPushButton('ALTERAR DEMANDA', parent=self.frame)
            self.btnalterar.setGeometry(QtCore.QRect(self.btn_width, 160, 131, 31))
            self.btnalterar.setObjectName('btnalterar')
            self.btnalterar.clicked.connect(self.altera_table)
            self.btnalterar.setStyleSheet('\n                                    QPushButton {\n                                        border: 2px solid #2E3D48;\n                                        border-radius: 10px;\n                                        background-color: #FFFFFF;\n                                        color: #2E3D48;\n                                    }\n                                    QPushButton:pressed {\n                                        background-color: #2E3D48;\n                                        color: #FFFFFF;\n                                    }\n                                ')
            self.editable = False

            self.btnexclu = QtWidgets.QPushButton('EXCLUIR DEMANDA', parent=self.frame)
            self.btnexclu.setGeometry(QtCore.QRect(self.btn_width, 200, 131, 31))
            self.btnexclu.setObjectName('btnexclu')
            self.btnexclu.clicked.connect(self.excluir_demanda)
            self.btnexclu.setStyleSheet('\n                                    QPushButton {\n                                        border: 2px solid #2E3D48;\n                                        border-radius: 10px;\n                                        background-color: #FFFFFF;\n                                        color: #2E3D48;\n                                    }\n                                    QPushButton:pressed {\n                                        background-color: #2E3D48;\n                                        color: #FFFFFF;\n                                    }\n                                ')
        if self.dept == 'Hemodinâmica':
            self.procura_pac.hide()
            self.btngraficos.hide()

            self.btnsair.setGeometry(QtCore.QRect(105, 0, 100, 23))
            self.editbarra.setGeometry(QtCore.QRect(30, 100, 291, 21))
            self.labeltitulo.setGeometry(QtCore.QRect(540, 29, 400, 31))
            self.temporizador(MainWindow)
            self.abrir_tabela_Hemodinamica(MainWindow)

            self.btnregis = QtWidgets.QPushButton('REGISTRAR DEMANDA', parent=self.frame)
            self.btnregis.setGeometry(QtCore.QRect(self.btn_width, 123, 131, 31))
            self.btnregis.setObjectName('btnregis')
            self.btnregis.clicked.connect(lambda: self.abrir_cadastro(MainWindow))
            self.btnregis.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')
            self.btnregis.clicked.connect(lambda: self.abrir_cadastro(MainWindow))

            self.btnalterar = QtWidgets.QPushButton('ALTERAR DEMANDA', parent=self.frame)
            self.btnalterar.setGeometry(QtCore.QRect(self.btn_width, 160, 131, 31))
            self.btnalterar.setObjectName('btnalterar')
            self.btnalterar.clicked.connect(self.altera_table)
            self.btnalterar.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')
            self.editable = False

            self.btnexclu = QtWidgets.QPushButton('EXCLUIR DEMANDA', parent=self.frame)
            self.btnexclu.setGeometry(QtCore.QRect(self.btn_width, 200, 131, 31))
            self.btnexclu.setObjectName('btnexclu')
            self.btnexclu.clicked.connect(self.excluir_demanda)
            self.btnexclu.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')
        if self.dept == 'Telespectador':
            self.labeltitulo.setGeometry(QtCore.QRect(540, 29, 400, 31))
            self.btngraficos.setGeometry(QtCore.QRect(210, 0, 100, 23))
            self.btnsair.setGeometry(QtCore.QRect(320, 0, 100, 23))

            self.btn_grade = QtWidgets.QPushButton(parent=self.frame)
            self.btn_grade.setGeometry(QtCore.QRect(105, 0, 100, 23))
            self.btn_grade.setObjectName('Grade')
            self.btn_grade.setText(_translate('MainWindow', 'GRADE'))
            self.btn_grade.clicked.connect(lambda: self.abrir_grade(MainWindow))
            self.btn_grade.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')

            self.btn_PRONTO_SOCORRO = QtWidgets.QPushButton(parent=self.frame)
            self.btn_PRONTO_SOCORRO.setGeometry(QtCore.QRect(0, 100, 120, 23))
            self.btn_PRONTO_SOCORRO.setObjectName('btn_PRONTO_SOCORRO')
            self.btn_PRONTO_SOCORRO.setText(_translate('MainWindow', 'PRONTO SOCORRO'))
            self.btn_PRONTO_SOCORRO.clicked.connect(lambda: self.setupUi(MainWindow, self.dept, self.user, self.nome_user))
            self.btn_PRONTO_SOCORRO.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')

            self.frame.mousePressEvent = lambda event: self.toggle_frame_visibility(self.sidebar)

            self.btn_ALTAS_CTI = QtWidgets.QPushButton(parent=self.frame)
            self.btn_ALTAS_CTI.setGeometry(QtCore.QRect(125, 100, 100, 23))
            self.btn_ALTAS_CTI.setObjectName('btn_ALTAS_CTI')
            self.btn_ALTAS_CTI.setText(_translate('MainWindow', "ALTA CTI'S"))
            self.btn_ALTAS_CTI.clicked.connect(lambda: self.abrir_tabela_Alta_CTI(MainWindow))
            self.btn_ALTAS_CTI.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')

            self.btn_AGENDA_BLOCO = QtWidgets.QPushButton(parent=self.frame)
            self.btn_AGENDA_BLOCO.setGeometry(QtCore.QRect(230, 100, 100, 23))
            self.btn_AGENDA_BLOCO.setObjectName('btn_AGENDA_BLOCO')
            self.btn_AGENDA_BLOCO.setText(_translate('MainWindow', 'AGENDA BLOCO'))
            self.btn_AGENDA_BLOCO.clicked.connect(lambda: self.abrir_tabela_Agenda_Bloco(MainWindow))
            self.btn_AGENDA_BLOCO.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')

            self.btn_HEMODINÂMICA = QtWidgets.QPushButton(parent=self.frame)
            self.btn_HEMODINÂMICA.setGeometry(QtCore.QRect(335, 100, 100, 23))
            self.btn_HEMODINÂMICA.setObjectName('btn_HEMODINÂMICA')
            self.btn_HEMODINÂMICA.setText(_translate('MainWindow', 'HEMODINÂMICA'))
            self.btn_HEMODINÂMICA.clicked.connect(lambda: self.abrir_tabela_Hemodinamica(MainWindow))
            self.btn_HEMODINÂMICA.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')

            self.btn_INTER_TRAN_EXTE = QtWidgets.QPushButton(parent=self.frame)
            self.btn_INTER_TRAN_EXTE.setGeometry(QtCore.QRect(440, 100, 200, 23))
            self.btn_INTER_TRAN_EXTE.setObjectName('btn_INTER_TRAN_EXTE')
            self.btn_INTER_TRAN_EXTE.setText(_translate('MainWindow', 'INTERNAÇÕES E TRANSF. EXTERNAS'))
            self.btn_INTER_TRAN_EXTE.clicked.connect(lambda: self.abrir_tabela_Inter_Tran_Exte(MainWindow))
            self.btn_INTER_TRAN_EXTE.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')

            self.btn_TRANS_INT = QtWidgets.QPushButton(parent=self.frame)
            self.btn_TRANS_INT.setGeometry(QtCore.QRect(645, 100, 160, 23))
            self.btn_TRANS_INT.setObjectName('btn_TRANS_INT')
            self.btn_TRANS_INT.setText(_translate('MainWindow', 'TRANSFERÊNCIAS INTERNAS'))
            self.btn_TRANS_INT.clicked.connect(lambda: self.abrir_tabela_Tran_Inte(MainWindow))
            self.btn_TRANS_INT.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')

            self.btn_ONCO_HEMATO_PED = QtWidgets.QPushButton(parent=self.frame)
            self.btn_ONCO_HEMATO_PED.setGeometry(QtCore.QRect(810, 100, 130, 23))
            self.btn_ONCO_HEMATO_PED.setObjectName('btn_ONCO_HEMATO_PED')
            self.btn_ONCO_HEMATO_PED.setText(_translate('MainWindow', 'ONCO HEMATO PED'))
            self.btn_ONCO_HEMATO_PED.clicked.connect(lambda: self.abrir_tabela_Onco_Hemato_Ped(MainWindow))
            self.btn_ONCO_HEMATO_PED.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n                        QPushButton:pressed {\n                            background-color: #2E3D48;\n                            color: #FFFFFF;\n                        }\n                    ')

            self.frame_personalisa = QtWidgets.QFrame(parent=self.frame)
            self.frame_personalisa.setStyleSheet('\n                                            QFrame  {\n                                                background-color: #FFFFFF;\n                                                border-top-right-radius: 20px;\n                                                border-bottom-right-radius: 20px;\n                                                border-left: 1px solid black;\n                                            }\n                                        ')
            self.frame_personalisa.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.frame_personalisa.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.frame_personalisa.setObjectName('frame_box')
            self.frame_personalisa.hide()

            self.btn_filtros = QtWidgets.QPushButton('▼ Selecione uma Data ', parent=self.frame)
            self.btnfechar = QtWidgets.QPushButton(' X ', parent=self.frame)
            self.btn_filtros.setFocus()
            self.btnfechar.setStyleSheet('QPushButton {    border-top-right-radius: 10px;    border-bottom-right-radius: 10px;    border-top-left-radius: 0px;    border-bottom-left-radius: 0px;    background-color: #FFFFFF;    color: #2E3D48;    border: 2px solid #2E3D48;}QPushButton:pressed {    background-color: #2E3D48;    color: #FFFFFF;}')
            current_datetime = QDateTime.currentDateTime()
            formatted_date = current_datetime.toString('yyyy')
            formatted_date2 = current_datetime.addYears(-1).toString('yyyy')

            self.frame_box = QtWidgets.QFrame(parent=self.frame)
            self.frame_box.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
            self.frame_box.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.frame_box.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            colo = '\n                                                    QPushButton {\n\n                                                    background-color: #FFFFFF;\n                                                    color: #2E3D48;\n                                                    border-radius: 10px;\n                                                    border-color: transparent;\n                                                    }\n                                                    QPushButton:hover {\n                                                    background-color: #c0c0c0;\n                                                    color: #000000;\n                                                    }\n                                                    QPushButton:pressed {\n                                                        background-color: #2E3D48;\n                                                        color: #FFFFFF;\n                                                    }\n                                                '

            self.btn_hoje = QtWidgets.QPushButton('Hoje', self.frame_box)
            self.btn_hoje.setGeometry(QtCore.QRect(0, 0, 150, 20))
            self.btn_hoje.setStyleSheet(colo)

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

            self.btn_filtros.clicked.connect(self.abrir_items)
            self.btn_7.clicked.connect(lambda: self.filtros(2))
            self.btn_30.clicked.connect(lambda: self.filtros(3))
            self.btn_ano.clicked.connect(lambda: self.filtros(4))
            self.btn_2ano.clicked.connect(lambda: self.filtros(5))
            self.btn_hoje.clicked.connect(lambda: self.filtros(1))
            self.btnfechar.clicked.connect(lambda: self.filtros(0))
            self.btn_personalisa.clicked.connect(self.abrir_personalisa)
            self.btn_personalisa.setGeometry(QtCore.QRect(0, 100, 150, 20))
            self.day = 'ONTEM'

            self.btnfechar.hide()
            self.frame_box.hide()

            self.btn_filtros.setStyleSheet('QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')

            ccurrent_datetime = QtCore.QDateTime.currentDateTime()
            self.borda_inicio = QtWidgets.QFrame(parent=self.frame_personalisa)
            self.borda_inicio.setStyleSheet('border: 2px solid black; border-radius: 10px; background-color: #FFFFFF;')
            self.borda_inicio.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.borda_inicio.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.borda_inicio.setObjectName('frame')
            self.borda_inicio.setGeometry(QtCore.QRect(8, 25, 140, 29))

            self.data_inicio = QtWidgets.QDateEdit(parent=self.frame_personalisa)
            self.data_inicio.setGeometry(QtCore.QRect(10, 30, 130, 20))
            self.data_inicio.setDateTime(ccurrent_datetime)
            self.data_inicio.setCalendarPopup(True)
            self.data_inicio.setStyleSheet('border_color: #FFFFFF; border-radius: 10px; background-color: #FFFFFF;')
            self.data_inicio.setObjectName('data_inicio')

            self.inicio = QtWidgets.QLabel('Depois de ', self.frame_personalisa)
            self.inicio.setStyleSheet('font-size: 13px; margin: 0; padding: 0;border: none; background-color: #FFFFFF')
            self.inicio.setGeometry(15, 20, 63, 13)

            self.borda_fim = QtWidgets.QFrame(parent=self.frame_personalisa)
            self.borda_fim.setStyleSheet('border: 2px solid black; border-radius: 10px; background-color: #FFFFFF;')
            self.borda_fim.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.borda_fim.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.borda_fim.setObjectName('frame')
            self.borda_fim.setGeometry(QtCore.QRect(8, 80, 140, 29))

            self.data_final = QtWidgets.QDateEdit(parent=self.frame_personalisa)
            self.data_final.setGeometry(QtCore.QRect(10, 85, 130, 20))
            self.data_final.setStyleSheet('border_color: #FFFFFF; border-radius: 10px; background-color: #FFFFFF;')
            self.data_final.setDateTime(QtCore.QDateTime.currentDateTime())
            self.data_final.setCalendarPopup(True)
            self.data_final.setObjectName('data_inicio')

            self.fim = QtWidgets.QLabel('Antes de ', self.frame_personalisa)
            self.fim.setStyleSheet('font-size: 13px; margin: 0; padding: 0;border: none; background-color: #FFFFFF')
            self.fim.setGeometry(15, 75, 57, 13)

            self.aplicar = QtWidgets.QPushButton('Aplicar', parent=self.frame_personalisa)
            self.aplicar.setGeometry(QtCore.QRect(165, 100, 101, 23))
            self.aplicar.clicked.connect(lambda: self.filtros(6))
            self.aplicar.setStyleSheet('QPushButton {\n                border: 2px solid #000000;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')

            self.labeltitulo.setGeometry(QtCore.QRect(540, 29, 400, 31))
            self.editbarra.setGeometry(QtCore.QRect(30, 65, 360, 21))
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 150, 23))
            self.btnfechar.setGeometry(QtCore.QRect(540, 65, 30, 23))
            self.frame_personalisa.setGeometry(QtCore.QRect(569, 89, 270, 125))
            self.frame_box.setGeometry(QtCore.QRect(420, 89, 150, 125))
            self.btngraficos.setGeometry(QtCore.QRect(210, 0, 100, 23))
            self.btngraficos.clicked.connect(lambda: self.abrir_gráficos(MainWindow))

            self.retranslateUi_ps(MainWindow)
            self.atualiza_tabela_demandas('tabela_demanda_ps')
        self.conf_layout()
        self.temporizador(MainWindow)
        if not self.frame_do_grafico.isHidden():
            self.canvas.show()
            self.plot_pie_chart()
            self.timer.stop()

    def finalizar_operacao(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Sair do Sistema de Gestão de Leitos ?')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.mainwindow.close()
            self.janela_CTI_PED.close()

    def abrir_items(self):
        if self.frame_box.isHidden():
            self.frame_box.show()
            return
        self.frame_box.hide()
        if not self.frame_personalisa.isHidden():
            self.frame_personalisa.hide()

    def filtros(self, index):
        self.btn_filtros.setStyleSheet('QPushButton {    border-top-right-radius: 0px;    border-bottom-right-radius: 0px;    border-top-left-radius: 10px;    border-bottom-left-radius: 10px;    background-color: #FFFFFF;    color: #2E3D48;    border: 2px solid black;}QPushButton:pressed {    background-color: #2E3D48;    color: #FFFFFF;}')
        if index == 1:
            self.day = 'HOJE'
            self.btn_filtros.setText('Hoje')
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 120, 23))
            self.btnfechar.show()
        elif index == 2:
            self.day = 'SEMANA'
            self.btn_filtros.setText('Ultimos 7 dias')
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 120, 23))
            self.btnfechar.show()
        elif index == 3:
            self.day = 'MES'
            self.btn_filtros.setText('Ultimos 30 dias')
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 120, 23))
            self.btnfechar.show()
        elif index == 4:
            self.day = 'ANO'
            current_datetime = QDateTime.currentDateTime()
            formatted_date = current_datetime.toString('yyyy')
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 120, 23))
            self.btn_filtros.setText(f'{formatted_date}')
            self.btnfechar.show()
        elif index == 5:
            self.day = '2ANO'
            current_datetime = QDateTime.currentDateTime()
            formatted_date = current_datetime.addYears(-1).toString('yyyy')
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 120, 23))
            self.btn_filtros.setText(f'{formatted_date}')
            self.btnfechar.show()
        elif index == 6:
            self.day = 'PERSONALIZADO'
            self.data_i = self.data_inicio.date()
            self.data_f = self.data_final.date()
            self.btn_filtros.setText('Período personalizado')
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 120, 23))
            self.btnfechar.show()
        elif index == 0:
            self.day = 'ONTEM'
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 150, 23))
            self.btn_filtros.setText('▼ Selecione uma Data ')
            self.btn_filtros.setStyleSheet('QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')
            self.btnfechar.hide()
            if not self.frame_personalisa.isHidden():
                self.frame_personalisa.hide()
        if self.day != 'ONTEM':
            self.filtrar_data()
            return

        if self.variavel == 0:
            self.atualiza_tabela_demandas('tabela_demanda_ps')
        if self.variavel == 1:
            self.atualiza_tabela_demandas('alta_cti')
        if self.variavel == 2:
            self.atualiza_tabela_demandas('tabela_agenda_bloco_demanda')
        if self.variavel == 3:
            self.atualiza_tabela_demandas('tabela_hemodinamica')
        if self.variavel == 4:
            self.atualiza_tabela_demandas('tabela_internações_e_transf_externas')
        if self.variavel == 5:
            self.atualiza_tabela_demandas('tabela_transferencias_internas')
        if self.variavel == 6:
            self.atualiza_tabela_demandas('tabela_onco_hemato_ped')
        self.timer_ps.start()

    def abrir_personalisa(self):
        if self.frame_personalisa.isHidden():
            self.frame_personalisa.show()
            self.frame_box.setStyleSheet('background-color: #FFFFFF; border-top-left-radius: 20px; border-bottom: 1px solid black;')
            self.frame_personalisa.setStyleSheet('\n                        QFrame  {\n                            background-color: #FFFFFF;\n                            border-top-right-radius: 20px;\n                            border-bottom: 1px solid black;\n                            border-left: 1px solid black;\n                        }\n                    ')
        else:
            self.frame_personalisa.hide()
            self.frame_box.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
            self.frame_personalisa.setStyleSheet('\n                        QFrame  {\n                            background-color: #FFFFFF;\n                            border-top-right-radius: 20px;\n                            border-bottom-right-radius: 20px;\n                            border-left: 1px solid black;\n                        }\n                    ')

    def abrir_gráficos(self, MainWindow):
        if self.frame_do_grafico.isHidden():
            self.frame_do_grafico.show()
            if self.dept != 'Telespectador':
                self.btnalterar.hide()
                self.btn_reservar_leito.hide()
                self.btnregis.hide()
                self.btnexclu.hide()
            self.tabelademan.hide()
            self.editbarra.hide()
            self.canvas.show()
            self.plot_pie_chart()
            self.timer_ps.stop()
        else:
            self.frame_do_grafico.hide()
            self.tabelademan.show()
            self.editbarra.show()
            if self.dept != 'Telespectador':
                self.btnalterar.show()
                self.btn_reservar_leito.show()
                self.btnregis.show()
                self.btnexclu.show()
            self.timer_ps.start()

    def plot_pie_chart(self):
        lista = ['ENFERMARIA FEMININA RESERVADA', 'ENFERMARIA FEMININA AGUARDANDO', 'ENFERMARIA MASCULINA RESERVADA', 'ENFERMARIA MASCULINA AGUARDANDO', 'LEITO PEDIÁTRICO RESERVADO', 'LEITO PEDIÁTRICO AGUARDANDO', 'CTI ADULT/UCO RESERVADO', 'CTI ADULT/UCO AGUARDANDO', 'LEITO OBSTETRICO/ MATERNIDADE ', 'ISOLAMENTO CONTATO RESERVADO', 'ISOLAMENTO CONTATO AGUARDANDO', 'ISOLAMENTO RESPIRATÓRIO RESERVADO', 'ISOLAMENTO RESPIRATÓRIO AGUARDANDO', 'APARTAMENTO RESERVADO', 'APARTAMENTO AGUARDANDO', 'CTI PEDIÁTRICO RESERVADO', 'CTI PEDIÁTRICO AGUARDANDO', 'CTI NEONATOLOGIA RESERVADO', 'LEITO VIRTUAL', 'SOLICITAÇÃO CANCELADA', 'ALTA PARA CASA', 'RERSERVADO', 'OCUPADO']
        qt = 0
        self.concluida = 0
        self.nao_concluida = 0
        for colum in range(self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum)
            if item_pac.text() == 'STATUS DA SOLICITAÇÃO':
                break
        for row in range(self.tabelademan.rowCount()):
            item = self.tabelademan.verticalHeaderItem(row)
            status = self.tabelademan.item(row, colum)
            qt += 1
            if status.text() in lista:
                self.concluida += 1
            else:
                self.nao_concluida += 1
        data = [self.concluida, self.nao_concluida]
        labels = ['SOLICITAÇÃO CONCLUÍDA', 'SOLICITAÇÃO EM ABERTO']
        colors = ['#ffff99', '#99ff99']
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
        if qt != 0:
            self.progress.setFormat('OCUPAÇÃO: {}%'.format(int(self.concluida * 100 / qt)))
            self.progress.setValue(int(self.concluida * 100 / qt))
        self.ax.clear()
        self.ax.pie(filtered_data, labels=filtered_labels, colors=filtered_colors, autopct=autopct_format, startangle=90, pctdistance=0.85, explode=explode)
        self.ax.axis('equal')
        self.figure.patch.set_facecolor('none')
        self.ax.figure.set_size_inches(9, 5)
        self.canvas.draw()

    def confirm_alta(self):
        colum_leito_atual = 0
        for colum in range(self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum)
            if item_pac.text() == 'LEITO ATUAL':
                colum_leito_atual = colum
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        analise = 0
        selecionado = []
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Confirmar Alta?')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            for row in range(self.tabelademan.rowCount()):
                selecao = self.tabelademan.item(row, 0)
                if selecao.checkState() == QtCore.Qt.CheckState.Checked:
                    analise = 1
                    selecionado.append(row)
            if analise == 1:
                current_datetime = QDateTime.currentDateTime()
                formatted_date = current_datetime.toString('dd/MM/yyyy')
                formatted_time = current_datetime.toString('hh:mm:ss')
                for row in reversed(selecionado):
                    pac = self.tabelademan.verticalHeaderItem(row).text()
                    novo_status = 'ALTA CONFIRMADA'
                    comando = 'UPDATE alta_cti SET STATUS_DAS_ALTAS = %s, HORARIO_DA_ALTA = %s, DATA_DE_CONFIRMACAO_DA_ALTA = %s WHERE idnew_table_alta_cti = %s'
                    valor = (novo_status, formatted_time, formatted_date, pac)
                    cursor.execute(comando, valor)
                    conexao.commit()
                    leito = self.tabelademan.item(row, colum_leito_atual)
                    leito = leito.text().replace(' ', '_')
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    comando = f'SELECT SEXO_DA_ENFERMARIA FROM GRADE WHERE idGRADE = "{leito}"'
                    cursor.execute(comando)
                    leitura = cursor.fetchall()
                    for lei in leitura:
                        sexo = lei[0]
                    comando = f'''UPDATE GRADE SET CODIGO_DE_INTERNACAO = "{''}",NPF = "{''}",PRONTUARIO = "{''}",OBSERVACOES = "{''}", STATUS_DO_LEITO = "{'VAGO'}", NOME = "{''}", DATA_DE_NASCIMENTO = "{''}", SEXO_DA_ENFERMARIA = "{sexo}",PREVISÃO_DE_ALTA =  "{''}",DATA_E_HORA_DE_ATUALIZAÇÃO = "{''}", SOLICITANTE = "{''}", RESERVA_COMUNICADA = "{''}", RESERVA_COMUNICADA_QUEM = "{''}"  WHERE idGRADE = "{leito}"'''
                    cursor.execute(comando)
                    conexao.commit()
                    comando_verificacao = f"SELECT COUNT(*) FROM GRADE WHERE idGRADE = '{leito}_aguardando'"
                    cursor.execute(comando_verificacao)
                    resultado = cursor.fetchone()
                    if resultado[0] > 0:
                        comando = f'DELETE FROM GRADE WHERE idGRADE = "{leito}"'
                        cursor.execute(comando)
                        conexao.commit()
                        comando = f'UPDATE GRADE SET  idGRADE = "{leito}"  WHERE idGRADE = "{leito}_aguardando"'
                        cursor.execute(comando)
                        conexao.commit()
                    cursor.close()
                    conexao.close()
        cursor.close()
        conexao.close()
        self.atualiza_tabela_demandas('alta_cti')

    def abrir_tabela_Onco_Hemato_Ped(self, MainWindow):
        if self.dept != 'Telespectador' and self.dept != 'Bloco Cirúrgico' and (self.dept != 'Pronto Socorro') and (self.dept != 'Hemodinâmica'):
            self.btn_confirm_alta.hide()

        if self.dept == 'NIR':
            self.alterar_cor_tela()
        self.tabelademan.setColumnCount(18)
        self.tabelademan.setRowCount(0)
        self.variavel = 6
        self.timer_ps.stop()
        self.temporizador(MainWindow)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(17, item)
        self.retranslateUi_onco_hemato_ped(MainWindow)
        self.atualiza_tabela_demandas('tabela_onco_hemato_ped')
        self.tabelademan.setCurrentCell(self.tabelademan.rowCount() - 1, 0)
        if not self.frame_do_grafico.isHidden():
            self.canvas.show()
            self.plot_pie_chart()
            self.timer.stop()

    def abrir_tabela_Tran_Inte(self, MainWindow):
        if self.dept != 'Telespectador' and self.dept != 'Bloco Cirúrgico' and (self.dept != 'Pronto Socorro') and (self.dept != 'Hemodinâmica'):
            self.btn_confirm_alta.hide()

        if self.dept == 'NIR':
            self.alterar_cor_tela()
        self.tabelademan.setColumnCount(13)
        self.tabelademan.setRowCount(0)
        self.variavel = 5
        self.timer_ps.stop()
        self.temporizador(MainWindow)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(12, item)
        self.retranslateUi_tran_inte(MainWindow)
        self.atualiza_tabela_demandas('tabela_transferencias_internas')
        self.tabelademan.setCurrentCell(self.tabelademan.rowCount() - 1, 0)
        if not self.frame_do_grafico.isHidden():
            self.canvas.show()
            self.plot_pie_chart()
            self.timer.stop()

    def abrir_tabela_Inter_Tran_Exte(self, MainWindow):
        if self.dept != 'Telespectador' and self.dept != 'Bloco Cirúrgico' and (self.dept != 'Pronto Socorro') and (self.dept != 'Hemodinâmica'):
            self.btn_confirm_alta.hide()
        if self.dept == 'NIR':
            self.alterar_cor_tela()
        self.tabelademan.setColumnCount(17)
        self.tabelademan.setRowCount(0)
        self.variavel = 4
        self.timer_ps.stop()
        self.temporizador(MainWindow)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(16, item)
        self.retranslateUi_inter_tran_exte(MainWindow)
        self.atualiza_tabela_demandas('tabela_internações_e_transf_externas')
        self.tabelademan.setCurrentCell(self.tabelademan.rowCount() - 1, 0)
        if not self.frame_do_grafico.isHidden():
            self.canvas.show()
            self.plot_pie_chart()
            self.timer.stop()

    def abrir_tabela_Hemodinamica(self, MainWindow):
        if self.dept != 'Telespectador' and self.dept != 'Bloco Cirúrgico' and (self.dept != 'Pronto Socorro') and (self.dept != 'Hemodinâmica'):
            self.btn_confirm_alta.hide()
        if self.dept == 'NIR':
            self.alterar_cor_tela()
        self.tabelademan.setColumnCount(18)
        self.tabelademan.setRowCount(0)
        self.variavel = 3
        self.timer_ps.stop()
        self.temporizador(MainWindow)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(17, item)
        self.retranslateUi_hemodinamica(MainWindow)
        self.atualiza_tabela_demandas('tabela_hemodinamica')
        self.tabelademan.setCurrentCell(self.tabelademan.rowCount() - 1, 0)
        if not self.frame_do_grafico.isHidden():
            self.canvas.show()
            self.plot_pie_chart()
            self.timer.stop()

    def abrir_tabela_Pronto_Socorro(self, MainWindow):
        if self.dept != 'Telespectador' and self.dept != 'Bloco Cirúrgico' and (self.dept != 'Pronto Socorro') and (self.dept != 'Hemodinâmica'):
            self.btn_confirm_alta.hide()
        if self.dept == 'NIR':
            self.alterar_cor_tela()
        self.variavel = 0
        self.tabelademan.setColumnCount(15)
        self.tabelademan.setRowCount(0)
        self.timer_ps.stop()
        self.temporizador(MainWindow)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(14, item)
        self.retranslateUi_ps(MainWindow)
        self.atualiza_tabela_demandas('tabela_demanda_ps')
        self.tabelademan.setCurrentCell(self.tabelademan.rowCount() - 1, 0)
        if not self.frame_do_grafico.isHidden():
            self.canvas.show()
            self.plot_pie_chart()
            self.timer.stop()

    def abrir_tabela_Agenda_Bloco(self, MainWindow):
        if self.dept != 'Telespectador' and self.dept != 'Bloco Cirúrgico' and (self.dept != 'Pronto Socorro') and (self.dept != 'Hemodinâmica'):
            self.btn_confirm_alta.hide()
        if self.dept == 'NIR':
            self.alterar_cor_tela()
        self.variavel = 2
        self.tabelademan.setColumnCount(19)
        self.tabelademan.setRowCount(0)
        self.timer_ps.stop()
        self.temporizador(MainWindow)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(18, item)
        self.retranslateUi_agenda_bloco(MainWindow)
        self.atualiza_tabela_demandas('tabela_agenda_bloco_demanda')
        self.tabelademan.setCurrentCell(self.tabelademan.rowCount() - 1, 0)
        if not self.frame_do_grafico.isHidden():
            self.canvas.show()
            self.plot_pie_chart()
            self.timer.stop()

    def abrir_tabela_Alta_CTI(self, MainWindow):
        if self.dept != 'Telespectador':
            self.btn_confirm_alta.setGeometry(QtCore.QRect(self.btn_width, 285, 131, 31))
        if self.dept == 'NIR':
            self.alterar_cor_tela()
        self.tabelademan.setColumnCount(19)
        self.tabelademan.setRowCount(0)
        self.variavel = 1
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.timer_ps.stop()
        self.temporizador(MainWindow)
        self.tabelademan.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(18, item)
        self.retranslateUi_alta_cti(MainWindow)
        self.atualiza_tabela_demandas('alta_cti')
        self.tabelademan.setCurrentCell(self.tabelademan.rowCount() - 1, 0)
        if not self.frame_do_grafico.isHidden():
            self.canvas.show()
            self.plot_pie_chart()
            self.timer.stop()

    def temporizador(self, MainWindow):
        self.timer_ps = QtCore.QTimer()
        self.timer_ps.setInterval(60000)
        self.tabelademan.cellChanged.connect(self.checkboxStateChanged)
        if self.variavel == 0:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_demanda_ps'))
        if self.variavel == 1:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('alta_cti'))
        if self.variavel == 2:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_agenda_bloco_demanda'))
        if self.variavel == 3:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_hemodinamica'))
        if self.variavel == 4:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_internações_e_transf_externas'))
        if self.variavel == 5:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_transferencias_internas'))
        if self.variavel == 6:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_onco_hemato_ped'))
        self.timer_ps.start()
        self.increase_column_width(0, 16)

    def get_current_position(self):
        current_item = self.tabelademan.currentItem()
        if current_item:
            self.posicao_inicial_row = current_item.row()
            self.posicao_inicial_colum = current_item.column()

    def atualiza_tabela_demandas(self, tabela):

        for colum in range(self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum)
            if item_pac.text() == 'NPF':
                self.tabelademan.hideColumn(colum)

        self.tabela_atual = tabela
        if self.tabelademan.currentItem():
            self.selection = (self.tabelademan.currentRow(), self.tabelademan.currentColumn())
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        comando = f'SELECT * FROM {tabela}'
        cursor.execute(comando)
        leitura = cursor.fetchall()
        self.tabelademan.clearContents()
        self.tabelademan.setRowCount(0)
        contador = 0
        for linha in leitura:
            row = self.tabelademan.rowCount()
            self.tabelademan.insertRow(contador)
            for column, valor in enumerate(linha):
                item = QtWidgets.QTableWidgetItem(str(valor))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                if column != 0:
                    if item is None or item.text() == 'None':
                        item = QtWidgets.QTableWidgetItem(str(''))
                        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setItem(contador, column, item)
                if column == 0:
                    self.tabelademan.setVerticalHeaderItem(contador, item)
                    _translate = QtCore.QCoreApplication.translate
                    self.increase_column_width(0, 16)
                    item_pac = self.tabelademan.verticalHeaderItem(contador)
                    item_pac.setText(_translate('MainWindow', item.text()))
            contador += 1
        for row in range(self.tabelademan.rowCount()):
            for colum in range(self.tabelademan.columnCount()):
                if self.tabelademan.horizontalHeaderItem(colum).text() == 'DATA E HORA DA RESERVA':
                    break
            data_reserva = self.tabelademan.item(row, colum).text()
            current_datetime = QDateTime.currentDateTime()
            formatted_date = current_datetime.toString('dd/MM/yyyy')
            self.increase_column_width(0, 16)
            excel_color = QtGui.QColor(255, 255, 255)
            adjusted_color = excel_color.lighter(100)
            data_celula = ''
            if data_reserva and ' ' in data_reserva:
                data_celula = data_reserva.split()[0]
            if data_reserva == '':
                for column in range(self.tabelademan.columnCount()):
                    item = self.tabelademan.item(row, column)
                    if item is None:
                        continue
                    new_item = QtWidgets.QTableWidgetItem(item.text())
                    excel_color = QtGui.QColor(255, 255, 255)
                    new_item.setBackground(excel_color)
                    new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setItem(row, column, new_item)
            else:
                if formatted_date == data_celula:
                    for column in range(self.tabelademan.columnCount()):
                        item = self.tabelademan.item(row, column)
                        if item is None:
                            continue
                        new_item = QtWidgets.QTableWidgetItem(item.text())
                        excel_color = QtGui.QColor(31, 73, 125)
                        adjusted_color = excel_color.lighter(140)
                        new_item.setBackground(adjusted_color)
                        new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        self.tabelademan.setItem(row, column, new_item)
                if data_celula < formatted_date:
                    for column in range(self.tabelademan.columnCount()):
                        item = self.tabelademan.item(row, column)
                        if item is not None:
                            new_item = QtWidgets.QTableWidgetItem(item.text())
                            excel_color = QtGui.QColor(255, 148, 74)
                            adjusted_color = excel_color.lighter(140)
                            new_item.setBackground(adjusted_color)
                            new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                            self.tabelademan.setItem(row, column, new_item)
            selecao = QtWidgets.QTableWidgetItem()
            selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
            selecao.setBackground(QtGui.QBrush(adjusted_color))
            self.tabelademan.setItem(row, 0, selecao)

            for colum in range(self.tabelademan.columnCount()):
                dados = self.tabelademan.item(row, colum).text()
                if dados == 'SIM':
                    new_item = QtWidgets.QTableWidgetItem(dados)
                    excel_color = QtGui.QColor(0,255,127)
                    adjusted_color = excel_color.lighter(140)
                    new_item.setBackground(adjusted_color)
                    new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setItem(row, colum, new_item)
                if dados == 'NÃO':
                    new_item = QtWidgets.QTableWidgetItem(dados)
                    excel_color = QtGui.QColor(250,128,114)
                    adjusted_color = excel_color.lighter(140)
                    new_item.setBackground(adjusted_color)
                    new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setItem(row, colum, new_item)


        cursor.close()
        conexao.close()
        item = self.tabelademan.item(self.posicao_inicial_row, self.posicao_inicial_colum)
        self.tabelademan.scrollToItem(item)
        if self.selection:
            row, col = self.selection
            self.tabelademan.setCurrentCell(row, col)

    def checkboxStateChanged(self, row, column):
        if column == 0:
            item = self.tabelademan.item(row, column)
            if item.checkState() == Qt.CheckState.Checked:
                self.timer_ps.stop()
            else:
                self.timer_ps.start()

    def filtrar_data(self):
        colum_data_da_demanda = 3
        for colum in range(self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum)
            if item_pac.text() == 'DATA E HORA DA SOLICITAÇÃO' or item_pac.text() == 'DATA DA ALTA':
                colum_data_da_demanda = colum
        for row in range(self.tabelademan.rowCount()):
            item = self.tabelademan.item(row, colum_data_da_demanda)
            if item is not None:
                texto = item.text()
            data_celula = datetime.datetime.strptime(texto.split()[0], '%d/%m/%Y').date()
            data_ano_celula = str(data_celula.year)
            data_atual = datetime.datetime.now().date()
            data_atual_ano = str(data_atual.year)
            data_atual_2ano = str((data_atual - datetime.timedelta(days=365)).year)
            self.data_inicio1 = datetime.datetime.strptime(self.data_inicio.date().toString('dd/MM/yyyy'), '%d/%m/%Y').date()
            self.data_final1 = datetime.datetime.strptime(self.data_final.date().toString('dd/MM/yyyy'), '%d/%m/%Y').date()
            if self.day == 'HOJE' and data_celula != data_atual:
                self.tabelademan.hideRow(row)
            elif self.day == 'SEMANA' and data_celula < data_atual - datetime.timedelta(days=7):
                self.tabelademan.hideRow(row)
            elif self.day == 'MES' and data_celula < data_atual - datetime.timedelta(days=30):
                self.tabelademan.hideRow(row)
            elif self.day == 'ANO' and data_ano_celula != data_atual_ano:
                self.tabelademan.hideRow(row)
            elif self.day == '2ANO' and data_ano_celula != data_atual_2ano:
                self.tabelademan.hideRow(row)
            elif self.day == 'PERSONALIZADO' and (not self.data_inicio1 <= data_celula <= self.data_final1):
                self.tabelademan.hideRow(row)
            elif self.day != 'ONTEM':
                self.tabelademan.showRow(row)
                self.timer_ps.stop()

    def copiadora(self):
        conta_linha = self.tabelademan.rowCount()
        conta_coluna = self.tabelademan.columnCount()
        self.tabela_alt.setColumnCount(conta_coluna)
        self.tabela_alt.setRowCount(conta_linha)
        for analisa_linha in range(conta_linha):
            for analisa_coluna in range(conta_coluna - 1):
                item = self.tabelademan.item(analisa_linha, analisa_coluna + 1)
                if item is not None:
                    item_text = item.text()
                    item_copy = QtWidgets.QTableWidgetItem(item_text)
                    self.tabela_alt.setItem(analisa_linha, analisa_coluna + 1, item_copy)

    def reservar_leito(self, MainWindow):
        cont = self.conta_linha()
        analise = False
        for row in range(cont):
            selec = self.tabelademan.item(row, 0)
            if selec.checkState() == QtCore.Qt.CheckState.Checked:
                analise = True
        if analise == True:
            from tela_reserva import Ui_reserva
            self.janela_reserva = QtWidgets.QMainWindow()
            self.reserva = Ui_reserva()
            self.timer_ps.stop()
            self.reserva.setupUi(MainWindow, self.variavel, self)
            self.reserva_Aberta = True
            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                btn.setEnabled(False)
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('Nenhum paciente selecionado!')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply = msg_box.exec()
            icon = QIcon('warning.ico')
            msg_box.setWindowIcon(icon)

    def refazer_alt(self):
        conta_linha = self.tabela_alt.rowCount()
        conta_coluna = self.tabela_alt.columnCount()
        for analisa_linha in range(conta_linha):
            for analisa_coluna in range(conta_coluna - 1):
                item = self.tabela_alt.item(analisa_linha, analisa_coluna + 1)
                if item is not None:
                    item_text = item.text()
                    item_copy = QtWidgets.QTableWidgetItem(item_text)
                    self.tabelademan.setItem(analisa_linha, analisa_coluna + 1, item_copy)

    def abrir_cadastro(self, Form):
        self.timer_ps.stop()
        if self.variavel == 0:
            from Demanda.cadastrodemandaps import Ui_Cadastro
            self.cadastro = Ui_Cadastro()
            self.cadastro.setupUi(Form, self)
        if self.variavel == 1:
            from Demanda.cadastro_altas_cti import Ui_Cadastro
            self.cadastro = Ui_Cadastro()
            self.cadastro.setupUi(Form, self.variavel, self)
        if self.variavel == 2:
            from Demanda.cadastrodemandaagenda import Ui_agenda
            self.cadastro = Ui_agenda()
            self.cadastro.setupUi(Form, self)
        if self.variavel == 3:
            from Demanda.Cadastro_HEMODINÂMICA import Ui_HEMODINAMICA
            self.cadastro = Ui_HEMODINAMICA()
            self.cadastro.setupUi(Form, self)
        if self.variavel == 4:
            from Demanda.cadastro_INTERNAÇÕES_E_TRANSF_EXTERNAS import Ui_INTERNAÇÕES_E_TRANSF_EXTERNAS
            self.cadastro = Ui_INTERNAÇÕES_E_TRANSF_EXTERNAS()
            self.cadastro.setupUi(Form, self)
        if self.variavel == 5:
            from Demanda.cadastro_TRANSFERÊNCIAS_INTERNAS import Ui_TRANSFERÊNCIAS_INTERNAS
            self.cadastro = Ui_TRANSFERÊNCIAS_INTERNAS()
            self.cadastro.setupUi(Form, self)
        if self.variavel == 6:
            from Demanda.cadastro_ONCO_HEMATO_PED import Ui_ONCO_HEMATO_PED
            self.cadastro = Ui_ONCO_HEMATO_PED()
            self.cadastro.setupUi(Form, self)
        self.cadastro_Aberta = True
        self.timer_ps.stop()
        for btn in self.frame.findChildren(QtWidgets.QPushButton):
            btn.setEnabled(False)

    def conta_linha(self):
        conta_linha = self.tabelademan.rowCount()
        return conta_linha

    def conta_coluna(self):
        conta_coluna = self.tabela_alt.columnCount()
        return conta_coluna

    def tabela_dem(self):
        return self.tabelademan

    def abrir_grade(self, MainWindow):
        self.CTI_PED = Ui_CTI_PED()
        self.CTI_PED.setupUi_grade(self.janela_CTI_PED, self, self.dept, self.user, self.nome_user, MainWindow)
        self.janela_CTI_PED.show()

    def add_dados_onco_hemato_ped(self, data_internacao, name, data_nasc, age, peso_altura, formatted_date_time, internado, clinica, procedimento, tipo_leito, pos, sol_nome_contato):
        conta_linha = self.tabelademan.rowCount()
        self.tabelademan.insertRow(conta_linha)
        self.tabelademan.setItem(conta_linha, 1, QtWidgets.QTableWidgetItem(data_internacao))
        self.tabelademan.setItem(conta_linha, 2, QtWidgets.QTableWidgetItem(name))
        self.tabelademan.setItem(conta_linha, 3, QtWidgets.QTableWidgetItem(data_nasc))
        self.tabelademan.setItem(conta_linha, 4, QtWidgets.QTableWidgetItem(str(age)))
        self.tabelademan.setItem(conta_linha, 5, QtWidgets.QTableWidgetItem(peso_altura))
        self.tabelademan.setItem(conta_linha, 6, QtWidgets.QTableWidgetItem(formatted_date_time))
        self.tabelademan.setItem(conta_linha, 7, QtWidgets.QTableWidgetItem(internado))
        self.tabelademan.setItem(conta_linha, 8, QtWidgets.QTableWidgetItem(clinica))
        self.tabelademan.setItem(conta_linha, 9, QtWidgets.QTableWidgetItem(procedimento))
        self.tabelademan.setItem(conta_linha, 10, QtWidgets.QTableWidgetItem(tipo_leito))
        self.tabelademan.setItem(conta_linha, 11, QtWidgets.QTableWidgetItem(pos))
        self.tabelademan.setItem(conta_linha, 12, QtWidgets.QTableWidgetItem(sol_nome_contato))
        selecao = QtWidgets.QTableWidgetItem()
        selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.tabelademan.setItem(conta_linha, 0, selecao)
        self.copiadora()
        self.atualiza_tabela_demandas('tabela_onco_hemato_ped')

    def add_dados_transferencias_internas(self, formatted_date_time, name, data_nasc, leito_atual, motivo, tipo_leito):
        conta_linha = self.tabelademan.rowCount()
        self.tabelademan.insertRow(conta_linha)
        self.tabelademan.setItem(conta_linha, 1, QtWidgets.QTableWidgetItem(formatted_date_time))
        self.tabelademan.setItem(conta_linha, 2, QtWidgets.QTableWidgetItem(name))
        self.tabelademan.setItem(conta_linha, 3, QtWidgets.QTableWidgetItem(data_nasc))
        self.tabelademan.setItem(conta_linha, 4, QtWidgets.QTableWidgetItem(leito_atual))
        self.tabelademan.setItem(conta_linha, 5, QtWidgets.QTableWidgetItem(motivo))
        self.tabelademan.setItem(conta_linha, 6, QtWidgets.QTableWidgetItem(tipo_leito))
        selecao = QtWidgets.QTableWidgetItem()
        selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.tabelademan.setItem(conta_linha, 0, selecao)
        self.copiadora()
        self.atualiza_tabela_demandas('tabela_transferencias_internas')

    def add_dados_internações_e_transf_externas(self, data_hora_inter_str, formatted_date_time, name, data_nasc, leito_atual, data_proced, clinica_pac, procedimento, tipo_leito, pos):
        conta_linha = self.tabelademan.rowCount()
        self.tabelademan.insertRow(conta_linha)
        self.tabelademan.setItem(conta_linha, 1, QtWidgets.QTableWidgetItem(data_hora_inter_str))
        self.tabelademan.setItem(conta_linha, 2, QtWidgets.QTableWidgetItem(formatted_date_time))
        self.tabelademan.setItem(conta_linha, 3, QtWidgets.QTableWidgetItem(name))
        self.tabelademan.setItem(conta_linha, 4, QtWidgets.QTableWidgetItem(data_nasc))
        self.tabelademan.setItem(conta_linha, 5, QtWidgets.QTableWidgetItem(leito_atual))
        self.tabelademan.setItem(conta_linha, 6, QtWidgets.QTableWidgetItem(data_proced))
        self.tabelademan.setItem(conta_linha, 7, QtWidgets.QTableWidgetItem(clinica_pac))
        self.tabelademan.setItem(conta_linha, 8, QtWidgets.QTableWidgetItem(procedimento))
        self.tabelademan.setItem(conta_linha, 9, QtWidgets.QTableWidgetItem(tipo_leito))
        self.tabelademan.setItem(conta_linha, 10, QtWidgets.QTableWidgetItem(pos))
        selecao = QtWidgets.QTableWidgetItem()
        selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.tabelademan.setItem(conta_linha, 0, selecao)
        self.copiadora()
        self.atualiza_tabela_demandas('tabela_internações_e_transf_externas')

    def add_dados_hemodinamica(self, data_hora_procd, name, data_nasc, data_int_str, formatted_date_time, leito_atual, clinica_pac, procedimento, prioridade, tipo_leito):
        conta_linha = self.tabelademan.rowCount()
        self.tabelademan.insertRow(conta_linha)
        self.tabelademan.setItem(conta_linha, 1, QtWidgets.QTableWidgetItem(data_hora_procd))
        self.tabelademan.setItem(conta_linha, 2, QtWidgets.QTableWidgetItem(name))
        self.tabelademan.setItem(conta_linha, 3, QtWidgets.QTableWidgetItem(data_nasc))
        self.tabelademan.setItem(conta_linha, 4, QtWidgets.QTableWidgetItem(data_int_str))
        self.tabelademan.setItem(conta_linha, 5, QtWidgets.QTableWidgetItem(formatted_date_time))
        self.tabelademan.setItem(conta_linha, 6, QtWidgets.QTableWidgetItem(leito_atual))
        self.tabelademan.setItem(conta_linha, 7, QtWidgets.QTableWidgetItem(clinica_pac))
        self.tabelademan.setItem(conta_linha, 8, QtWidgets.QTableWidgetItem(procedimento))
        self.tabelademan.setItem(conta_linha, 9, QtWidgets.QTableWidgetItem(prioridade))
        self.tabelademan.setItem(conta_linha, 10, QtWidgets.QTableWidgetItem(tipo_leito))
        selecao = QtWidgets.QTableWidgetItem()
        selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.tabelademan.setItem(conta_linha, 0, selecao)
        self.copiadora()
        self.atualiza_tabela_demandas('tabela_hemodinamica')

    def add_dados_agenda(self, data_procd_str, name, data_nasc, leito_atual, clinica_pac, procedimento, medico, tipo_leito, enfermaria, prioridade):
        conta_linha = self.tabelademan.rowCount()
        self.tabelademan.insertRow(conta_linha)
        self.tabelademan.setItem(conta_linha, 1, QtWidgets.QTableWidgetItem(data_procd_str))
        self.tabelademan.setItem(conta_linha, 2, QtWidgets.QTableWidgetItem(name))
        self.tabelademan.setItem(conta_linha, 3, QtWidgets.QTableWidgetItem(data_nasc))
        self.tabelademan.setItem(conta_linha, 4, QtWidgets.QTableWidgetItem(leito_atual))
        self.tabelademan.setItem(conta_linha, 5, QtWidgets.QTableWidgetItem(clinica_pac))
        self.tabelademan.setItem(conta_linha, 6, QtWidgets.QTableWidgetItem(procedimento))
        self.tabelademan.setItem(conta_linha, 7, QtWidgets.QTableWidgetItem(medico))
        self.tabelademan.setItem(conta_linha, 8, QtWidgets.QTableWidgetItem(tipo_leito))
        self.tabelademan.setItem(conta_linha, 9, QtWidgets.QTableWidgetItem(enfermaria))
        self.tabelademan.setItem(conta_linha, 10, QtWidgets.QTableWidgetItem(prioridade))
        selecao = QtWidgets.QTableWidgetItem()
        selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.tabelademan.setItem(conta_linha, 0, selecao)
        self.atualiza_tabela_demandas('tabela_agenda_bloco_demanda')
        self.copiadora()

    def add_dados(self, pronto, npf, name_ps, ponto_score_ps, data_nasc_ps, clinica_pac_ps, obs_ps, tipo_leito_ps, prioridade_solic_ps, nome_contato_sol):
        conta_linha = self.tabelademan.rowCount()
        self.tabelademan.insertRow(conta_linha)
        self.tabelademan.setItem(conta_linha, 4, QtWidgets.QTableWidgetItem(name_ps))
        self.tabelademan.setItem(conta_linha, 5, QtWidgets.QTableWidgetItem(data_nasc_ps))
        self.tabelademan.setItem(conta_linha, 6, QtWidgets.QTableWidgetItem(ponto_score_ps))
        self.tabelademan.setItem(conta_linha, 7, QtWidgets.QTableWidgetItem(clinica_pac_ps))
        self.tabelademan.setItem(conta_linha, 8, QtWidgets.QTableWidgetItem(obs_ps))
        self.tabelademan.setItem(conta_linha, 9, QtWidgets.QTableWidgetItem(tipo_leito_ps))
        self.tabelademan.setItem(conta_linha, 10, QtWidgets.QTableWidgetItem(prioridade_solic_ps))
        self.tabelademan.setItem(conta_linha, 11, QtWidgets.QTableWidgetItem(nome_contato_sol))
        selecao = QtWidgets.QTableWidgetItem()
        selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.tabelademan.setItem(conta_linha, 0, selecao)
        self.copiadora()
        current_datetime = QDateTime.currentDateTime()
        formatted_date = current_datetime.toString('dd/MM/yyyy')
        formatted_time = current_datetime.toString('hh:mm:ss')
        time = formatted_date + ' ' + formatted_time
        self.tabelademan.setItem(conta_linha, 1, QtWidgets.QTableWidgetItem(time))
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        comando = f'''INSERT INTO tabela_demanda_ps (PRONTUARIO,NPF,data_demanda, NOME, DATA_NASC, PONTUAÇÃO, CLÍNICA, OBSERVAÇÕES, TIPO, PRIORIDADE, NOMEECONTATO) VALUES ("{pronto}","{npf}","{formatted_date + ' ' + formatted_time}", "{name_ps}", "{data_nasc_ps}","{ponto_score_ps}","{clinica_pac_ps}","{obs_ps}","{tipo_leito_ps}","{prioridade_solic_ps}","{nome_contato_sol}")'''
        cursor.execute(comando)
        conexao.commit()
        cursor.close()
        conexao.close()
        self.abrir_tabela_Pronto_Socorro(self.mainwindow)

    def avisar_click(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('A tabela está habilitada para edição! Conclua a edição antes!')
        icon = QIcon('warning.ico')
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        reply = msg_box.exec()

    def altera_table(self):
        colum_tipo_de_leito = 0
        colum_prioridade_da_solicitacao = 0
        colum_status_da_solicitacao = 0
        colum_sexo_do_paciente = 0
        colum_unidade_atual = 0
        colum_status_alta = 0
        colum_cirurgia_liberada = 0
        colum_motivo_do_cancelamento = 0
        colum_pos_em_cti = 0
        colum_leito_atual = 0
        colum_clinica = 0
        colum_data_de_confirmacao = 0
        colum_data_rese = 0
        colum_pre_internacao_realizada = 0
        for colum in range(self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum)
            if item_pac.text() == 'LEITO RESERVADO':
                colum_leito_reservado = colum
            if item_pac.text() == 'PRÉ INTERNAÇÃO REALIZADA?':
                colum_pre_internacao_realizada = colum
            if item_pac.text() == 'CLÍNICA':
                colum_clinica = colum
            if item_pac.text() == 'DATA DE CONFIRMAÇÃO DA ALTA':
                colum_data_de_confirmacao = colum
            if item_pac.text() == 'LEITO ATUAL':
                colum_leito_atual = colum
            if item_pac.text() == 'PÓS OPERATÓRIO EM CTI?':
                colum_pos_em_cti = colum
            if item_pac.text() == 'TIPO DE LEITO SOLICITADO':
                colum_tipo_de_leito = colum
            if item_pac.text() == 'PRIORIDADE DA SOLICITAÇÃO':
                colum_prioridade_da_solicitacao = colum
            if item_pac.text() == 'STATUS DA SOLICITAÇÃO':
                colum_status_da_solicitacao = colum
            if item_pac.text() == 'SEXO DO PACIENTE':
                colum_sexo_do_paciente = colum
            if item_pac.text() == 'UNIDADE DE INTERNAÇÃO ATUAL':
                colum_unidade_atual = colum
            if item_pac.text() == 'STATUS DAS ALTAS':
                colum_status_alta = colum
            if item_pac.text() == 'CIRURGIA LIBERADA PARA ENTRAR?':
                colum_cirurgia_liberada = colum
            if item_pac.text() == 'MOTIVO DO CANCELAMENTO':
                colum_motivo_do_cancelamento = colum
            if item_pac.text() ==  'DATA E HORA DA RESERVA':
                colum_data_rese = colum
        if self.tabelademan.rowCount() > 0:
            # Proibindo a edição de colunas para o PS
            if self.dept == 'PS' and self.tabela_atual == 'tabela_demanda_ps':
                for row in range(self.tabelademan.rowCount()):
                    for col in range(colum_status_alta, self.tabelademan.columnCount()):
                        item = self.tabelademan.item(row, col)
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.timer_ps.stop()
            _translate = QtCore.QCoreApplication.translate
            self.btnalterar.setText(_translate('MainWindow', 'CONCLUIR ALTERAÇÃO'))
            self.editable = not self.editable
            self.tabelademan.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers if self.editable else QTableWidget.EditTrigger.NoEditTriggers)
            if self.editable:
                for btn in self.frame.findChildren(QtWidgets.QPushButton):
                    if btn != self.btnalterar:
                        btn.setEnabled(False)
                self.label_icone.setEnabled(False)
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText('A tabela está habilitada para edição!')
                icon = QIcon('warning.ico')
                msg_box.setWindowIcon(icon)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply = msg_box.exec()
                if colum_tipo_de_leito != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box = QComboBox()
                        item = self.tabelademan.item(row, colum_tipo_de_leito)
                        if item is not None:
                            self.combo_box.addItem(item.text())
                            self.combo_box.setItemText(0, item.text())
                            self.combo_box.addItem('ENFERMARIA FEMININA')
                            self.combo_box.addItem('ENFERMARIA MASCULINA')
                            self.combo_box.addItem('PEDIÁTRICO')
                            self.combo_box.addItem('CTI ADULT/UCO')
                            self.combo_box.addItem('CTI NEONATOLOGIA')
                            self.combo_box.addItem('CTI PEDIÁTRICO')
                            self.combo_box.addItem('ISOLAMENTO CONTATO')
                            self.combo_box.addItem('ISOLAMENTO RESPIRATÓRIO')
                            self.combo_box.addItem('MATERNIDADE')
                            self.combo_box.addItem('APARTAMENTO')
                            self.combo_box.addItem('ENFERMARIA COVID')
                            self.combo_box.addItem('CTI COVID')
                            self.combo_box.addItem('INTERNAÇÃO VIRTUAL')
                        self.tabelademan.setCellWidget(row, colum_tipo_de_leito, self.combo_box)
                if colum_pre_internacao_realizada != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_pre_internacao_realizada = QComboBox()
                        item = self.tabelademan.item(row, colum_tipo_de_leito)
                        if item is not None:
                            self.combo_box_pre_internacao_realizada.addItem(item.text())
                            self.combo_box_pre_internacao_realizada.setItemText(0, item.text())
                            self.combo_box_pre_internacao_realizada.addItem('SIM')
                            self.combo_box_pre_internacao_realizada.addItem('NÃO')
                            self.combo_box_pre_internacao_realizada.addItem('NÃO SE APLICA')
                        self.tabelademan.setCellWidget(row, colum_pre_internacao_realizada, self.combo_box_pre_internacao_realizada)
                if colum_clinica != 0 and self.dept == 'PS':
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box = QComboBox()
                        item = self.tabelademan.item(row, colum_clinica)
                        if item is not None:
                            self.combo_box.addItem(item.text())
                            self.combo_box.setItemText(0, item.text())
                            self.combo_box.addItem('CLÍNICA MÉDICA')
                            self.combo_box.addItem('NEUROLOGIA')
                            self.combo_box.addItem('PNEUMOLOGIA')
                            self.combo_box.addItem('HEMATOLOGIA')
                            self.combo_box.addItem('INFECTOLOGIA')
                            self.combo_box.addItem('CARDIOLOGIA')
                            self.combo_box.addItem('NEUROCIRURGIA')
                            self.combo_box.addItem('ORTOPEDIA')
                            self.combo_box.addItem('UROLOGIA')
                            self.combo_box.addItem('CIRURGIA VASCULAR')
                            self.combo_box.addItem('BUCO-MAXILO')
                            self.combo_box.addItem('CIRURGIA TORÁCICA')
                            self.combo_box.addItem('GASTROENTEROLOGIA')
                            self.combo_box.addItem('FÍGADO E VIAS BILIARES')
                            self.combo_box.addItem('ESÓFAGO ESTÔMAGO E DUODENO')
                            self.combo_box.addItem('COLOPROCTOLOGIA')
                            self.combo_box.addItem('CIRURGIA GERAL')
                            self.combo_box.addItem('CIRURGIA DE CABEÇA E PESCOÇO')
                            self.combo_box.addItem('PEDIATRIA')
                            self.combo_box.addItem('CIRURGIA PEDIÁTRICA')
                            self.combo_box.addItem('TRANSPLANTE RENAL')
                            self.combo_box.addItem('TRANSPLANTE HEPÁTICO')
                            self.combo_box.addItem('TRANSPLANTE CARDÍACO')
                            self.combo_box.addItem('TRANSPLANTE DE MEDULA ÓSSEA')
                            self.combo_box.addItem('TRANSPLANTE DE PULMÃO')
                            self.combo_box.addItem('COVID SUSPEITO')
                            self.combo_box.addItem('COVID CONFIRMADO')
                            self.combo_box.addItem('ISOLAMENTO RESPIRATÓRIO')
                            self.combo_box.addItem('ISOLAMENTO DE CONTATO')
                            self.combo_box.addItem('CTI')
                            self.combo_box.addItem('UCO')
                            self.combo_box.addItem('CTI PED')
                        self.tabelademan.setCellWidget(row, colum_clinica, self.combo_box)
                if colum_prioridade_da_solicitacao != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_prioridade = QComboBox()
                        item = self.tabelademan.item(row, colum_prioridade_da_solicitacao)
                        if item is not None:
                            self.combo_box_prioridade.addItem(item.text())
                            self.combo_box_prioridade.setItemText(0, item.text())
                            self.combo_box_prioridade.addItem('BAIXA')
                            self.combo_box_prioridade.addItem('MÉDIA BAIXA')
                            self.combo_box_prioridade.addItem('MÉDIA MÉDIA')
                            self.combo_box_prioridade.addItem('MÉDIA ALTA')
                            self.combo_box_prioridade.addItem('ALTA')
                        self.tabelademan.setCellWidget(row, colum_prioridade_da_solicitacao, self.combo_box_prioridade)
                if colum_status_da_solicitacao != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_status_da_solicitacao = QComboBox()
                        item = self.tabelademan.item(row, colum_status_da_solicitacao)
                        if item is not None:
                            self.combo_box_status_da_solicitacao.addItem(item.text())
                            self.combo_box_status_da_solicitacao.setItemText(0, item.text())
                            self.combo_box_status_da_solicitacao.addItem('ALTA')
                            self.combo_box_status_da_solicitacao.addItem('RESERVADO')
                            self.combo_box_status_da_solicitacao.addItem('EVAZÃO')
                            self.combo_box_status_da_solicitacao.addItem('CANCELADA')
                            self.combo_box_status_da_solicitacao.addItem('AGUARDANDO')
                            self.combo_box_status_da_solicitacao.addItem('OBITO')
                        self.tabelademan.setCellWidget(row, colum_status_da_solicitacao, self.combo_box_status_da_solicitacao)
                if colum_sexo_do_paciente != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_sexo_do_paciente = QComboBox()
                        item = self.tabelademan.item(row, colum_sexo_do_paciente)
                        if item is not None:
                            self.combo_box_sexo_do_paciente.addItem(item.text())
                            self.combo_box_sexo_do_paciente.setItemText(0, item.text())
                            self.combo_box_sexo_do_paciente.addItem('FEMININO')
                            self.combo_box_sexo_do_paciente.addItem('MASCULINO')
                            self.combo_box_sexo_do_paciente.addItem('PEDIÁTRICO')
                        self.tabelademan.setCellWidget(row, colum_sexo_do_paciente, self.combo_box_sexo_do_paciente)
                if colum_unidade_atual != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_unidade_atual = QComboBox()
                        item = self.tabelademan.item(row, colum_unidade_atual)
                        if item is not None:
                            self.combo_box_unidade_atual.addItem(item.text())
                            self.combo_box_unidade_atual.setItemText(0, item.text())
                            self.combo_box_unidade_atual.addItem('CTI 3º LESTE')
                            self.combo_box_unidade_atual.addItem('UCO 3º NORTE')
                            self.combo_box_unidade_atual.addItem('UTI - PS')
                            self.combo_box_unidade_atual.addItem('CTI PEDIÁTRICO 6º NORTE')
                            self.combo_box_unidade_atual.addItem('CTI NEONATOLOGIA')
                        self.tabelademan.setCellWidget(row, colum_unidade_atual, self.combo_box_unidade_atual)
                if colum_status_alta != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_status_alta = QComboBox()
                        item = self.tabelademan.item(row, colum_status_alta)
                        if item is not None:
                            self.combo_box_status_alta.addItem(item.text())
                            self.combo_box_status_alta.setItemText(0, item.text())
                            self.combo_box_status_alta.addItem('PRÉ-ALTA ')
                            self.combo_box_status_alta.addItem('ALTA CONFIRMADA')
                            self.combo_box_status_alta.addItem('ALTA CANCELADA')
                        self.tabelademan.setCellWidget(row, colum_status_alta, self.combo_box_status_alta)
                if colum_cirurgia_liberada != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_cirurgia_liberada = QComboBox()
                        item = self.tabelademan.item(row, colum_cirurgia_liberada)
                        if item is not None:
                            self.combo_box_cirurgia_liberada.addItem(item.text())
                            self.combo_box_cirurgia_liberada.setItemText(0, item.text())
                            self.combo_box_cirurgia_liberada.addItem('SIM')
                            self.combo_box_cirurgia_liberada.addItem('NÃO')
                            self.combo_box_cirurgia_liberada.addItem('CANCELADA')
                        self.tabelademan.setCellWidget(row, colum_cirurgia_liberada, self.combo_box_cirurgia_liberada)
                if colum_pos_em_cti != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_pos_em_cti = QComboBox()
                        item = self.tabelademan.item(row, colum_pos_em_cti)
                        if item is not None:
                            self.combo_box_pos_em_cti.addItem(item.text())
                            self.combo_box_pos_em_cti.setItemText(0, item.text())
                            self.combo_box_pos_em_cti.addItem('SIM')
                            self.combo_box_pos_em_cti.addItem('NÃO')
                        self.tabelademan.setCellWidget(row, colum_pos_em_cti, self.combo_box_pos_em_cti)
                if colum_motivo_do_cancelamento != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_motivo_do_cancelamento = QComboBox()
                        item = self.tabelademan.item(row, colum_motivo_do_cancelamento)
                        if item is not None:
                            self.combo_box_motivo_do_cancelamento.addItem(item.text())
                            self.combo_box_motivo_do_cancelamento.setItemText(0, item.text())
                            self.combo_box_motivo_do_cancelamento.addItem('FALTA DE LEITO')
                            self.combo_box_motivo_do_cancelamento.addItem('EQUIPE MÉDICA')
                            self.combo_box_motivo_do_cancelamento.addItem('INFRAESTRUTURA BLOCO')
                            self.combo_box_motivo_do_cancelamento.addItem('CLINICA DO PACIENTE')
                            self.combo_box_motivo_do_cancelamento.addItem('PACIENTE NÃO COMPARECEU')
                            self.combo_box_motivo_do_cancelamento.addItem('NÃO PRECISOU DO LEITO DE ENFERMARIA')
                            self.combo_box_motivo_do_cancelamento.addItem('FALTA DE MATERIAL')
                            self.combo_box_motivo_do_cancelamento.addItem('PACIENTE SUBSTITUÍDO')
                        self.tabelademan.setCellWidget(row, colum_motivo_do_cancelamento, self.combo_box_motivo_do_cancelamento)
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText('Confirmar Alteração?')
                msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                reply = msg_box.exec()
                self.btnalterar.setText(_translate('MainWindow', 'ALTERAR DEMANDA'))
                if reply == QMessageBox.StandardButton.No:
                    self.refazer_alt()
                if reply == QMessageBox.StandardButton.Yes:
                    self.copiadora()
                    if self.variavel == 0:
                        tabela = 'tabela_demanda_ps'
                    if self.variavel == 1:
                        tabela = 'alta_cti'
                    if self.variavel == 2:
                        tabela = 'tabela_agenda_bloco_demanda'
                    if self.variavel == 3:
                        tabela = 'tabela_hemodinamica'
                    if self.variavel == 4:
                        tabela = 'tabela_internações_e_transf_externas'
                    if self.variavel == 5:
                        tabela = 'tabela_transferencias_internas'
                    if self.variavel == 6:
                        tabela = 'tabela_onco_hemato_ped'
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    cursor.execute(f'SHOW COLUMNS FROM {tabela}')
                    colunas = [coluna[0] for coluna in cursor.fetchall()]
                    for row in range(self.tabelademan.rowCount()):
                        for colum in range(1, self.tabelademan.columnCount()):
                            valor_para_atualizar = self.tabelademan.item(row, colum).text()
                            id = self.tabelademan.verticalHeaderItem(row).text()
                            comando_update = f'UPDATE {tabela} SET {colunas[colum]} = %s WHERE {colunas[0]} = {id} '
                            cursor.execute(comando_update, (valor_para_atualizar,))
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Information)
                    msg_box.setWindowTitle('AVISO')
                    msg_box.setText('Alteração Concluída com Sucesso!')
                    icon = QIcon('warning.ico')
                    msg_box.setWindowIcon(icon)
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                    reply = msg_box.exec()
                if colum_pre_internacao_realizada != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_pre_internacao_realizada = self.tabelademan.cellWidget(row, colum_pre_internacao_realizada)
                        self.combo_box_pre_internacao_realizada.close()
                if colum_tipo_de_leito != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box = self.tabelademan.cellWidget(row, colum_tipo_de_leito)
                        self.combo_box.close()
                if colum_prioridade_da_solicitacao != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_prioridade = self.tabelademan.cellWidget(row, colum_prioridade_da_solicitacao)
                        self.combo_box_prioridade.close()
                if colum_status_da_solicitacao != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_status_da_solicitacao = self.tabelademan.cellWidget(row, colum_status_da_solicitacao)
                        self.combo_box_status_da_solicitacao.close()
                if colum_sexo_do_paciente != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_sexo_do_paciente = self.tabelademan.cellWidget(row, colum_sexo_do_paciente)
                        self.combo_box_sexo_do_paciente.close()
                if colum_unidade_atual != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_unidade_atual = self.tabelademan.cellWidget(row, colum_unidade_atual)
                        self.combo_box_unidade_atual.close()
                if colum_status_alta != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_status_alta = self.tabelademan.cellWidget(row, colum_status_alta)
                        self.leito_reservado = self.tabelademan.item(row, colum_leito_reservado).text()
                        if self.combo_box_status_alta.currentText() == 'ALTA CONFIRMADA' and len(self.leito_reservado) < 2:
                            conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                            cursor = conexao.cursor()
                            current_datetime = QDateTime.currentDateTime()
                            formatted_date = current_datetime.toString('dd/MM/yyyy')
                            formatted_time = current_datetime.toString('hh:mm:ss')
                            pac = self.tabelademan.verticalHeaderItem(row).text()
                            novo_status = 'ALTA CONFIRMADA'
                            comando = 'UPDATE alta_cti SET STATUS_DAS_ALTAS = %s, HORARIO_DA_ALTA = %s, DATA_DE_CONFIRMACAO_DA_ALTA = %s WHERE idnew_table_alta_cti = %s'
                            valor = (novo_status, formatted_time, formatted_date, pac)
                            cursor.execute(comando, valor)
                            conexao.commit()
                            cursor.close()
                            conexao.close()
                            leito = self.tabelademan.item(row, colum_leito_atual)
                            leito = leito.text().replace(' ', '_')
                            conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                            cursor = conexao.cursor()
                            comando = f'SELECT SEXO_DA_ENFERMARIA FROM GRADE WHERE idGRADE = "{leito}"'
                            cursor.execute(comando)
                            leitura = cursor.fetchall()
                            sexo = leitura[0]
                            comando = f'''UPDATE GRADE SET CODIGO_DE_INTERNACAO = "{''}",NPF = "{''}",PRONTUARIO = "{''}",OBSERVACOES = "{''}", STATUS_DO_LEITO = "{'VAGO'}", NOME = "{''}", DATA_DE_NASCIMENTO = "{''}", SEXO_DA_ENFERMARIA = "{sexo}",PREVISÃO_DE_ALTA =  "{''}",DATA_E_HORA_DE_ATUALIZAÇÃO = "{''}", SOLICITANTE = "{''}", RESERVA_COMUNICADA = "{''}", RESERVA_COMUNICADA_QUEM = "{''}"  WHERE idGRADE = "{leito}"'''
                            cursor.execute(comando)
                            comando_verificacao = f"SELECT COUNT(*) FROM GRADE WHERE idGRADE = '{leito}_aguardando'"
                            cursor.execute(comando_verificacao)
                            resultado = cursor.fetchone()
                            if resultado[0] > 0:
                                comando = f'DELETE FROM GRADE WHERE idGRADE = "{leito}"'
                                cursor.execute(comando)
                                conexao.commit()
                                comando = f'UPDATE GRADE SET  idGRADE = "{leito}"  WHERE idGRADE = "{leito}_aguardando"'
                                cursor.execute(comando)
                                conexao.commit()
                            cursor.close()
                            conexao.close()
                        self.combo_box_status_alta.close()
                if colum_cirurgia_liberada != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_cirurgia_liberada = self.tabelademan.cellWidget(row, colum_cirurgia_liberada)
                        self.combo_box_cirurgia_liberada.close()
                if colum_pos_em_cti != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_pos_em_cti = self.tabelademan.cellWidget(row, colum_pos_em_cti)
                        self.combo_box_pos_em_cti.close()
                if colum_motivo_do_cancelamento != 0:
                    for row in range(self.tabelademan.rowCount()):
                        self.combo_box_motivo_do_cancelamento = self.tabelademan.cellWidget(row, colum_motivo_do_cancelamento)
                        self.combo_box_motivo_do_cancelamento.close()
                self.timer_ps.start()
                for btn in self.frame.findChildren(QtWidgets.QPushButton):
                    if btn != self.btnalterar:
                        btn.setEnabled(True)
                self.label_icone.setEnabled(True)

    def pesquisar(self, pesquisa):
        self.timer_ps.stop()
        colum_nome = 4
        for colum in range(self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum)
            if item_pac.text() == 'NOME DO PACIENTE':
                colum_nome = colum
        for row in range(self.tabelademan.rowCount()):
            item = self.tabelademan.item(row, colum_nome)
            if pesquisa.lower() in item.text().lower():
                self.tabelademan.showRow(row)
            else:
                self.tabelademan.hideRow(row)
        self.timer_ps.start()

    def excluir_demanda(self):
        analise = 0
        selecionado = []
        for row in range(self.tabelademan.rowCount()):
            selecao = self.tabelademan.item(row, 0)
            if selecao.checkState() == QtCore.Qt.CheckState.Checked:
                analise = 1
                selecionado.append(row)
        if analise == 1:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('EXCLUIR DEMANDA?')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            reply = msg_box.exec()
            if reply == QMessageBox.StandardButton.Yes:
                if self.variavel == 0:
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    selecionado_copy = selecionado.copy()
                    for row in reversed(selecionado):
                        selecionado.append(row)
                    comando = 'DELETE FROM tabela_demanda_ps WHERE idtabela_demanda_ps = %s'
                    valores = [(self.tabelademan.verticalHeaderItem(row).text(),) for row in selecionado_copy]
                    cursor.executemany(comando, valores)
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    for row in reversed(selecionado):
                        self.tabelademan.removeRow(row)
                if self.variavel == 1:
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    selecionado_copy = selecionado.copy()
                    for row in reversed(selecionado_copy):
                        nome = self.tabelademan.item(row, 3)
                        selecionado.append(row)
                    comando = 'DELETE FROM alta_cti WHERE idnew_table_alta_cti = %s'
                    valores = [(self.tabelademan.verticalHeaderItem(row).text(),) for row in selecionado_copy]
                    cursor.executemany(comando, valores)
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    for row in reversed(selecionado):
                        self.tabelademan.removeRow(row)
                if self.variavel == 2:
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    selecionado_copy = selecionado.copy()
                    for row in reversed(selecionado_copy):
                        nome = self.tabelademan.item(row, 2)
                        selecionado.append(row)
                    comando = 'DELETE FROM tabela_agenda_bloco_demanda WHERE idnew_table = %s'
                    valores = [(self.tabelademan.verticalHeaderItem(row).text(),) for row in selecionado_copy]
                    cursor.executemany(comando, valores)
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    for row in reversed(selecionado):
                        self.tabelademan.removeRow(row)
                if self.variavel == 3:
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    selecionado_copy = selecionado.copy()
                    for row in reversed(selecionado_copy):
                        selecionado.append(row)
                    comando = 'DELETE FROM tabela_hemodinamica WHERE idtabela_hemodinamica = %s'
                    valores = [(self.tabelademan.verticalHeaderItem(row).text(),) for row in selecionado_copy]
                    cursor.executemany(comando, valores)
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    for row in reversed(selecionado):
                        self.tabelademan.removeRow(row)
                if self.variavel == 4:
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    selecionado_copy = selecionado.copy()
                    for row in reversed(selecionado_copy):
                        selecionado.append(row)
                    comando = 'DELETE FROM tabela_internações_e_transf_externas WHERE idtabela_internações_e_transf_externas = %s'
                    valores = [(self.tabelademan.verticalHeaderItem(row).text(),) for row in selecionado_copy]
                    cursor.executemany(comando, valores)
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    for row in reversed(selecionado):
                        self.tabelademan.removeRow(row)
                if self.variavel == 5:
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    selecionado_copy = selecionado.copy()
                    for row in reversed(selecionado_copy):
                        selecionado.append(row)
                    comando = 'DELETE FROM tabela_transferencias_internas WHERE idtabela_transferencias_internas = %s'
                    valores = [(self.tabelademan.verticalHeaderItem(row).text(),) for row in selecionado_copy]
                    cursor.executemany(comando, valores)
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    for row in reversed(selecionado):
                        self.tabelademan.removeRow(row)
                if self.variavel == 6:
                    conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                    cursor = conexao.cursor()
                    selecionado_copy = selecionado.copy()
                    for row in reversed(selecionado_copy):
                        selecionado.append(row)
                    comando = 'DELETE FROM tabela_onco_hemato_ped WHERE idtabela_onco_hemato_ped = %s'
                    valores = [(self.tabelademan.verticalHeaderItem(row).text(),) for row in selecionado_copy]
                    cursor.executemany(comando, valores)
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    for row in reversed(selecionado):
                        self.tabelademan.removeRow(row)
                self.copiadora()

    def retranslateUi_ps(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'Sistema de Gestão de Leitos'))
        self.increase_column_width(0, 5)
        item = self.tabelademan.horizontalHeaderItem(0)
        item.setText(_translate('MainWindow', ' '))
        item = self.tabelademan.horizontalHeaderItem(1)
        item.setText(_translate('MainWindow', 'PRONTUÁRIO'))
        item = self.tabelademan.horizontalHeaderItem(2)
        item.setText(_translate('MainWindow', 'NPF'))
        item = self.tabelademan.horizontalHeaderItem(3)
        item.setText(_translate('MainWindow', 'DATA E HORA DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(4)
        item.setText(_translate('MainWindow', 'NOME DO PACIENTE'))
        item = self.tabelademan.horizontalHeaderItem(5)
        item.setText(_translate('MainWindow', 'DATA DE NASCIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(6)
        item.setText(_translate('MainWindow', 'PONTUAÇÃO SCORE'))
        item = self.tabelademan.horizontalHeaderItem(7)
        item.setText(_translate('MainWindow', 'CLÍNICA'))
        item = self.tabelademan.horizontalHeaderItem(8)
        item.setText(_translate('MainWindow', 'MOTIVO DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(9)
        item.setText(_translate('MainWindow', 'TIPO DE LEITO SOLICITADO'))
        item = self.tabelademan.horizontalHeaderItem(10)
        item.setText(_translate('MainWindow', 'PRIORIDADE DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(11)
        item.setText(_translate('MainWindow', 'NOME/CONTATO DO SOLICITANTE'))
        item = self.tabelademan.horizontalHeaderItem(12)
        item.setText(_translate('MainWindow', 'STATUS DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(13)
        item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
        item = self.tabelademan.horizontalHeaderItem(14)
        item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
        if self.dept != 'Telespectador':
            self.btnregis.setText(_translate('MainWindow', 'REGISTRAR DEMANDA'))
            self.btnalterar.setText(_translate('MainWindow', 'ALTERAR DEMANDA'))
            self.btnexclu.setText(_translate('MainWindow', 'EXCLUIR DEMANDA'))
        self.labeltitulo.setText(_translate('MainWindow', 'SOLICITAÇÃO DE LEITOS PRONTO SOCORRO'))
        self.btndeman.setText(_translate('MainWindow', 'DEMANDA'))
        self.btngraficos.setText(_translate('MainWindow', 'GRÁFICOS'))
        self.btnsair.setText(_translate('MainWindow', 'SAIR'))
        for colum in range(1, self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum).text()
            text_width = self.fontMetrics().boundingRect(item_pac).width()
            self.increase_column_width(colum, text_width + 100)

    def retranslateUi_alta_cti(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'Sistema de Gestão de Leitos'))
        self.increase_column_width(0, 16)
        item = self.tabelademan.horizontalHeaderItem(0)
        item.setText(_translate('MainWindow', ' '))
        item = self.tabelademan.horizontalHeaderItem(1)
        item.setText(_translate('MainWindow', 'PRONTUÁRIO'))
        item = self.tabelademan.horizontalHeaderItem(2)
        item.setText(_translate('MainWindow', 'NPF'))
        item = self.tabelademan.horizontalHeaderItem(3)
        item.setText(_translate('MainWindow', 'DATA DA ALTA'))
        item = self.tabelademan.horizontalHeaderItem(4)
        item.setText(_translate('MainWindow', 'HORA DE SOLICITAÇÃO DA ALTA'))
        item = self.tabelademan.horizontalHeaderItem(5)
        item.setText(_translate('MainWindow', 'NOME DO PACIENTE'))
        item = self.tabelademan.horizontalHeaderItem(6)
        item.setText(_translate('MainWindow', 'DATA DE NASCIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(7)
        item.setText(_translate('MainWindow', 'SEXO DO PACIENTE'))
        item = self.tabelademan.horizontalHeaderItem(8)
        item.setText(_translate('MainWindow', 'ESPECIALIDADE MÉDICA'))
        item = self.tabelademan.horizontalHeaderItem(9)
        item.setText(_translate('MainWindow', 'NECESSIDADES ESPECÍFICAS'))
        item = self.tabelademan.horizontalHeaderItem(10)
        item.setText(_translate('MainWindow', 'UNIDADE DE INTERNAÇÃO ATUAL'))
        item = self.tabelademan.horizontalHeaderItem(11)
        item.setText(_translate('MainWindow', 'STATUS DAS ALTAS'))
        item = self.tabelademan.horizontalHeaderItem(12)
        item.setText(_translate('MainWindow', 'DATA DE CONFIRMAÇÃO DA ALTA'))
        item = self.tabelademan.horizontalHeaderItem(13)
        item.setText(_translate('MainWindow', 'HORÁRIO DE CONFIRMAÇÃO DA ALTA'))
        item = self.tabelademan.horizontalHeaderItem(14)
        item.setText(_translate('MainWindow', 'LEITO ATUAL'))
        item = self.tabelademan.horizontalHeaderItem(15)
        item.setText(_translate('MainWindow', 'STATUS DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(16)
        item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
        item = self.tabelademan.horizontalHeaderItem(17)
        item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
        item = self.tabelademan.horizontalHeaderItem(18)
        item.setText(_translate('MainWindow', 'PRÉ INTERNAÇÃO REALIZADA?'))

        self.labeltitulo.setText(_translate('MainWindow', "SOLICITAÇÃO DE LEITOS ALTA CTI'S"))
        for colum in range(1, self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum).text()
            text_width = self.fontMetrics().boundingRect(item_pac).width()
            self.increase_column_width(colum, text_width + 100)

    def retranslateUi_agenda_bloco(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.increase_column_width(0, 16)
        item = self.tabelademan.horizontalHeaderItem(0)
        item.setText(_translate('MainWindow', ' '))
        item = self.tabelademan.horizontalHeaderItem(1)
        item.setText(_translate('MainWindow', 'PRONTUÁRIO'))
        item = self.tabelademan.horizontalHeaderItem(2)
        item.setText(_translate('MainWindow', 'NPF'))
        item = self.tabelademan.horizontalHeaderItem(3)
        item.setText(_translate('MainWindow', 'DATA E HORA DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(4)
        item.setText(_translate('MainWindow', 'DATA E HORA DO PROCEDIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(5)
        item.setText(_translate('MainWindow', 'NOME DO PACIENTE'))
        item = self.tabelademan.horizontalHeaderItem(6)
        item.setText(_translate('MainWindow', 'DATA DE NASCIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(7)
        item.setText(_translate('MainWindow', 'LEITO DE INTERNAÇÃO ATUAL'))
        item = self.tabelademan.horizontalHeaderItem(8)
        item.setText(_translate('MainWindow', 'CLÍNICA'))
        item = self.tabelademan.horizontalHeaderItem(9)
        item.setText(_translate('MainWindow', 'PROCEDIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(10)
        item.setText(_translate('MainWindow', 'MÉDICO RESPONSÁVEL'))
        item = self.tabelademan.horizontalHeaderItem(11)
        item.setText(_translate('MainWindow', 'TIPO DE LEITO SOLICITADO'))
        item = self.tabelademan.horizontalHeaderItem(12)
        item.setText(_translate('MainWindow', 'ENFERMARIA DE RETAGUARDA?'))
        item = self.tabelademan.horizontalHeaderItem(13)
        item.setText(_translate('MainWindow', 'PRIORIDADE'))
        item = self.tabelademan.horizontalHeaderItem(14)
        item.setText(_translate('MainWindow', 'CIRURGIA LIBERADA PARA ENTRAR?'))
        item = self.tabelademan.horizontalHeaderItem(15)
        item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
        item = self.tabelademan.horizontalHeaderItem(16)
        item.setText(_translate('MainWindow', 'STATUS DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(17)
        item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
        item = self.tabelademan.horizontalHeaderItem(18)
        item.setText(_translate('MainWindow', 'MOTIVO DO CANCELAMENTO'))
        self.labeltitulo.setText(_translate('MainWindow', 'SOLICITAÇÃO DE LEITOS AGENDA BLOCO'))
        for colum in range(1, self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum).text()
            text_width = self.fontMetrics().boundingRect(item_pac).width()
            self.increase_column_width(colum, text_width + 100)

    def retranslateUi_hemodinamica(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.increase_column_width(0, 16)
        item = self.tabelademan.horizontalHeaderItem(0)
        item.setText(_translate('MainWindow', ' '))
        item = self.tabelademan.horizontalHeaderItem(1)
        item.setText(_translate('MainWindow', 'PRONTUÁRIO'))
        item = self.tabelademan.horizontalHeaderItem(2)
        item.setText(_translate('MainWindow', 'NPF'))
        item = self.tabelademan.horizontalHeaderItem(3)
        item.setText(_translate('MainWindow', 'DATA E HORA DO PROCEDIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(4)
        item.setText(_translate('MainWindow', 'NOME DO PACIENTE'))
        item = self.tabelademan.horizontalHeaderItem(5)
        item.setText(_translate('MainWindow', 'DATA DE NASCIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(6)
        item.setText(_translate('MainWindow', 'DATA DA INTERNAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(7)
        item.setText(_translate('MainWindow', 'DATA E HORA DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(8)
        item.setText(_translate('MainWindow', 'LEITO DE INTERNAÇÃO ATUAL'))
        item = self.tabelademan.horizontalHeaderItem(9)
        item.setText(_translate('MainWindow', 'CLÍNICA'))
        item = self.tabelademan.horizontalHeaderItem(10)
        item.setText(_translate('MainWindow', 'PROCEDIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(11)
        item.setText(_translate('MainWindow', 'PRIORIDADE'))
        item = self.tabelademan.horizontalHeaderItem(12)
        item.setText(_translate('MainWindow', 'TIPO DE LEITO SOLICITADO'))
        item = self.tabelademan.horizontalHeaderItem(13)
        item.setText(_translate('MainWindow', 'CIRURGIA LIBERADA PARA ENTRAR?'))
        item = self.tabelademan.horizontalHeaderItem(14)
        item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
        item = self.tabelademan.horizontalHeaderItem(15)
        item.setText(_translate('MainWindow', 'STATUS DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(16)
        item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
        item = self.tabelademan.horizontalHeaderItem(17)
        item.setText(_translate('MainWindow', 'MOTIVO DO CANCELAMENTO'))
        self.labeltitulo.setText(_translate('MainWindow', 'SOLICITAÇÃO DE LEITOS HEMODINÂMICA'))
        for colum in range(1, self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum).text()
            text_width = self.fontMetrics().boundingRect(item_pac).width()
            self.increase_column_width(colum, text_width + 100)

    def retranslateUi_inter_tran_exte(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.increase_column_width(0, 5)
        item = self.tabelademan.horizontalHeaderItem(0)
        item.setText(_translate('MainWindow', ' '))
        item = self.tabelademan.horizontalHeaderItem(1)
        item.setText(_translate('MainWindow', 'PRONTUÁRIO'))
        item = self.tabelademan.horizontalHeaderItem(2)
        item.setText(_translate('MainWindow', 'NPF'))
        item = self.tabelademan.horizontalHeaderItem(3)
        item.setText(_translate('MainWindow', 'DATA E HORA DA INTERNAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(5)
        item.setText(_translate('MainWindow', 'NOME DO PACIENTE'))
        item = self.tabelademan.horizontalHeaderItem(4)
        item.setText(_translate('MainWindow', 'DATA E HORA DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(6)
        item.setText(_translate('MainWindow', 'DATA DE NASCIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(7)
        item.setText(_translate('MainWindow', 'ORIGEM DO PACIENTE'))
        item = self.tabelademan.horizontalHeaderItem(8)
        item.setText(_translate('MainWindow', 'DATA DO PROCEDIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(9)
        item.setText(_translate('MainWindow', 'CLÍNICA'))
        item = self.tabelademan.horizontalHeaderItem(10)
        item.setText(_translate('MainWindow', 'MOTIVO DA INTERNAÇÃO ANTECIPADA/ PROCEDIMENTO A SER REALIZADO'))
        item = self.tabelademan.horizontalHeaderItem(11)
        item.setText(_translate('MainWindow', 'TIPO DE LEITO SOLICITADO'))
        item = self.tabelademan.horizontalHeaderItem(12)
        item.setText(_translate('MainWindow', 'PÓS OPERATÓRIO EM CTI?'))
        item = self.tabelademan.horizontalHeaderItem(13)
        item.setText(_translate('MainWindow', 'NOME E CONTATO DO SOLICITANTE'))
        item = self.tabelademan.horizontalHeaderItem(14)
        item.setText(_translate('MainWindow', 'STATUS DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(15)
        item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
        item = self.tabelademan.horizontalHeaderItem(16)
        item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
        self.labeltitulo.setText(_translate('MainWindow', 'SOLICITAÇÃO DE LEITOS INTERNAÇÕES E TRANSF. EXTERNAS'))
        for colum in range(1, self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum).text()
            text_width = self.fontMetrics().boundingRect(item_pac).width()
            self.increase_column_width(colum, text_width + 100)

    def retranslateUi_tran_inte(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.increase_column_width(0, 5)
        MainWindow.setWindowTitle(_translate('MainWindow', 'Sistema de Gestão de Leitos'))
        item = self.tabelademan.horizontalHeaderItem(0)
        item.setText(_translate('MainWindow', ' '))
        item = self.tabelademan.horizontalHeaderItem(1)
        item.setText(_translate('MainWindow', 'PRONTUÁRIO'))
        item = self.tabelademan.horizontalHeaderItem(2)
        item.setText(_translate('MainWindow', 'NPF'))
        item = self.tabelademan.horizontalHeaderItem(3)
        item.setText(_translate('MainWindow', 'DATA E HORA DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(4)
        item.setText(_translate('MainWindow', 'NOME DO PACIENTE'))
        item = self.tabelademan.horizontalHeaderItem(5)
        item.setText(_translate('MainWindow', 'DATA DE NASCIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(6)
        item.setText(_translate('MainWindow', 'LEITO ATUAL'))
        item = self.tabelademan.horizontalHeaderItem(7)
        item.setText(_translate('MainWindow', 'MOTIVO DA TRANSFERÊNCIA'))
        item = self.tabelademan.horizontalHeaderItem(8)
        item.setText(_translate('MainWindow', 'TIPO DE LEITO SOLICITADO'))
        item = self.tabelademan.horizontalHeaderItem(9)
        item.setText(_translate('MainWindow', 'STATUS DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(10)
        item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
        item = self.tabelademan.horizontalHeaderItem(11)
        item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
        item = self.tabelademan.horizontalHeaderItem(12)
        item.setText(_translate('MainWindow', 'OBERVAÇÕES'))
        self.labeltitulo.setText(_translate('MainWindow', 'SOLICITAÇÃO DE LEITOS TRANSFERÊNCIAS INTERNAS'))
        for colum in range(1, self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum).text()
            text_width = self.fontMetrics().boundingRect(item_pac).width()
            self.increase_column_width(colum, text_width + 100)

    def retranslateUi_onco_hemato_ped(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        item = self.tabelademan.horizontalHeaderItem(0)
        item.setText(_translate('MainWindow', ' '))
        self.increase_column_width(0, 5)
        item = self.tabelademan.horizontalHeaderItem(1)
        item.setText(_translate('MainWindow', 'PRONTUÁRIO'))
        item = self.tabelademan.horizontalHeaderItem(2)
        item.setText(_translate('MainWindow', 'NPF'))
        item = self.tabelademan.horizontalHeaderItem(3)
        item.setText(_translate('MainWindow', 'DATA PREVISTA DA INTERNAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(4)
        item.setText(_translate('MainWindow', 'NOME DO PACIENTE'))
        item = self.tabelademan.horizontalHeaderItem(5)
        item.setText(_translate('MainWindow', 'DATA DE NASCIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(6)
        item.setText(_translate('MainWindow', 'IDADE'))
        item = self.tabelademan.horizontalHeaderItem(7)
        item.setText(_translate('MainWindow', 'PESO E ALTURA DA CRIANÇA'))
        item = self.tabelademan.horizontalHeaderItem(8)
        item.setText(_translate('MainWindow', 'DATA E HORA DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(9)
        item.setText(_translate('MainWindow', 'PACIENTE JA INTERNADO NO PRONTO SOCORRO?'))
        item = self.tabelademan.horizontalHeaderItem(10)
        item.setText(_translate('MainWindow', 'CLÍNICA'))
        item = self.tabelademan.horizontalHeaderItem(11)
        item.setText(_translate('MainWindow', 'PROCEDIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(12)
        item.setText(_translate('MainWindow', 'TIPO DE LEITO SOLICITADO'))
        item = self.tabelademan.horizontalHeaderItem(13)
        item.setText(_translate('MainWindow', 'PÓS OPERATÓRIO EM CTI?'))
        item = self.tabelademan.horizontalHeaderItem(14)
        item.setText(_translate('MainWindow', 'NOME E CONTATO DO SOLICITANTE'))
        item = self.tabelademan.horizontalHeaderItem(15)
        item.setText(_translate('MainWindow', 'STATUS DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(16)
        item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
        item = self.tabelademan.horizontalHeaderItem(17)
        item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
        self.labeltitulo.setText(_translate('MainWindow', 'SOLICITAÇÃO DE LEITOS ONCO-HEMATO PED'))
        for colum in range(1, self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum).text()
            text_width = self.fontMetrics().boundingRect(item_pac).width()
            self.increase_column_width(colum, text_width + 100)

    def increase_column_width(self, column, width):
        self.tabelademan.setColumnWidth(column, width)

    def onIconClick(self):
        self.clicked = not self.clicked
        if self.clicked:
            self.label_icone.setStyleSheet('border-radius: 10px; background-color: #2E3D48;')
            self.sidebar.setVisible(True)
            self.barra = self.tabelademan.horizontalScrollBar().value()
            self.barra_vertical = self.tabelademan.verticalScrollBar().value()
        else:
            self.label_icone.setStyleSheet('border-radius: 10px;')
            self.sidebar.setVisible(False)

    def abrir_procura_pac(self, Form):
        self.timer_ps.stop()
        self.sidebar.hide()
        from procura_paciente import Ui_Form
        self.procura_paciente = Ui_Form()
        self.procura_paciente.setupUi(Form, self)
        self.procurar_Aberta = True
        for btn in self.frame.findChildren(QtWidgets.QPushButton):
            btn.setEnabled(False)

    def abrir_configuracoes(self, Form):
        self.sidebar.close()
        self.timer_ps.stop()
        self.label_icone.setStyleSheet('border-radius: 10px;')
        from config import Ui_Form
        self.config = Ui_Form()
        self.config.setupUi(Form, self)
        self.config_Aberta = True
        for btn in self.frame.findChildren(QtWidgets.QPushButton):
            btn.setEnabled(False)

    def abrir_conta_do_usuario(self, Form):
        self.sidebar.close()
        self.label_icone.setStyleSheet('border-radius: 10px;')
        self.timer_ps.stop()
        from conta_do_usuario import Ui_Form
        self.conta_user = Ui_Form()
        self.conta_user.setupUi(Form, self)
        self.conta_do_usuario_Aberta = True
        for btn in self.frame.findChildren(QtWidgets.QPushButton):
            btn.setEnabled(False)

    def selecionar(self, nome, tipo):
        if tipo == 3:
            texto = 'NOME DO PACIENTE'
        if tipo == 1:
            texto = 'PRONTUÁRIO'
        if tipo == 2:
            texto = 'NPF'
        colum = 2
        for colum in range(self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum)
            if item_pac.text() == texto:
                break
        for row in range(self.tabelademan.rowCount()):
            item = self.tabelademan.item(row, colum)
            item2 = self.tabelademan.verticalHeaderItem(row)
            if item is not None:
                if nome.lower() in item.text().lower() or nome.lower() in item2.text().lower():
                    self.tabelademan.showRow(row)
                else:
                    self.tabelademan.hideRow(row)

    def retornar_main_window(self):
        return self.mainwindow

    def toggle_frame_visibility(self, sidebar):
        if not sidebar.isHidden():
            sidebar.hide()
            self.label_icone.setStyleSheet('border-radius: 10px;')
        if self.config_Aberta == True:
            self.janela_config.close()
            self.config_Aberta = False
            self.timer_ps.start()
        if self.cadastro_Aberta == True:
            self.janela_cadastro.close()
            self.cadastro_Aberta = False
            self.timer_ps.start()
        if self.reserva_Aberta == True:
            self.janela_reserva.close()
            self.reserva_Aberta = False
            self.timer_ps.start()
        if self.procurar_Aberta == True:
            self.janela_procura.close()
            self.procurar_Aberta = False
            self.timer_ps.start()
        if self.conta_do_usuario_Aberta == True:
            self.janela_conta_do_usuario.close()
            self.conta_do_usuario_Aberta = False
            self.timer_ps.start()
        for btn in self.frame.findChildren(QtWidgets.QPushButton):
            btn.setEnabled(True)

    def close_frame(self, row, col):
        if not self.sidebar.isHidden():
            self.sidebar.hide()
            self.label_icone.setStyleSheet('border-radius: 10px;')
        if self.config_Aberta == True:
            self.janela_config.close()
            self.timer_ps.start()
            self.config_Aberta = False
        if self.cadastro_Aberta == True:
            self.janela_cadastro.close()
            self.cadastro_Aberta = False
            self.timer_ps.start()
        if self.reserva_Aberta == True:
            self.janela_reserva.close()
            self.timer_ps.start()
            self.reserva_Aberta = False
        if self.procurar_Aberta == True:
            self.janela_procura.close()
            self.timer_ps.start()
            self.procurar_Aberta = False
        if self.conta_do_usuario_Aberta == True:
            self.janela_conta_do_usuario.close()
            self.timer_ps.start()
            self.conta_do_usuario_Aberta = False
        for btn in self.frame.findChildren(QtWidgets.QPushButton):
            btn.setEnabled(True)

    def check_scrollbar_value(self):
        if self.tabelademan.horizontalScrollBar().value() != self.barra:
            if not self.sidebar.isHidden():
                self.sidebar.hide()
                self.label_icone.setStyleSheet('border-radius: 10px;')
            if self.config_Aberta == True:
                self.janela_config.close()
                self.timer_ps.start()
                self.config_Aberta = False
            if self.cadastro_Aberta == True:
                self.janela_cadastro.close()
                self.timer_ps.start()
                self.cadastro_Aberta = False
            if self.reserva_Aberta == True:
                self.janela_reserva.close()
                self.reserva_Aberta = False
                self.timer_ps.start()
            if self.procurar_Aberta == True:
                self.timer_ps.start()
                self.janela_procura.close()
                self.procurar_Aberta = False
            if self.conta_do_usuario_Aberta == True:
                self.janela_conta_do_usuario.close()
                self.timer_ps.start()
                self.conta_do_usuario_Aberta = False
        if self.tabelademan.verticalScrollBar().value() != self.barra_vertical:
            if not self.sidebar.isHidden():
                self.sidebar.hide()
                self.label_icone.setStyleSheet('border-radius: 10px;')
            if self.config_Aberta == True:
                self.janela_config.close()
                self.timer_ps.start()
                self.config_Aberta = False
            if self.cadastro_Aberta == True:
                self.janela_cadastro.close()
                self.timer_ps.start()
                self.cadastro_Aberta = False
            if self.reserva_Aberta == True:
                self.janela_reserva.close()
                self.reserva_Aberta = False
                self.timer_ps.start()
            if self.procurar_Aberta == True:
                self.janela_procura.close()
                self.timer_ps.start()
                self.procurar_Aberta = False
            if self.conta_do_usuario_Aberta == True:
                self.janela_conta_do_usuario.close()
                self.timer_ps.start()
                self.conta_do_usuario_Aberta = False
        for btn in self.frame.findChildren(QtWidgets.QPushButton):
            btn.setEnabled(True)

    def conf_layout(self):
        if self.settings.contains('tema'):
            font_name = self.settings.value('font', defaultValue='')
            backcolocor = self.settings.value('tema', defaultValue='')
            color = self.settings.value('color', defaultValue='')
            tamanho = int(self.settings.value('tamanho', defaultValue=10))
        else:
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
        self.sidebar.setStyleSheet(f'border: 2px solid #2E3D48;background-color: {backcolocor}; border-radius: 10px;color: {color};font: {font_name} {tamanho}px;')
        for label in self.sidebar.findChildren(QtWidgets.QLabel):
            label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name}; border:none')
        self.labeltitulo.setStyleSheet(f'color: {color}; font:  30 px {font_name};font-weight: bold; border:none;')

    def alterar_cor_tela(self):
        if 'rgb(192, 192, 192)' in self.frame.styleSheet():
            self.frame.setStyleSheet('background-color: #5DADE2')
        else:
            self.frame.setStyleSheet('background-color: rgb(192, 192, 192)')
