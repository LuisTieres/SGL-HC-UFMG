import pymysql
from PyQt6.QtGui import QIcon, QPalette, QColor, QPixmap, QGuiApplication
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QCompleter,QStyledItemDelegate, QLineEdit, QMessageBox, QHeaderView, QColorDialog, QComboBox, QLabel, QToolTip, QTableWidgetItem, QVBoxLayout, QScrollArea, QFrame, QWidget, QPushButton
from PyQt6.QtCore import QDateTime, Qt, QSettings, QStandardPaths, QFile, QDate
from PyQt6.QtWidgets import QMessageBox,QDialog,QVBoxLayout, QRadioButton, QDialogButtonBox, QStackedWidget,QAbstractItemView,QInputDialog,QStyledItemDelegate,QMenuBar,QMenu,QHeaderView,QColorDialog, QTableWidget, QApplication,QScrollArea,QHBoxLayout,QPushButton,QToolTip, QLabel, QSpacerItem, QSizePolicy,QFrame, QCheckBox, QTableWidgetItem, QLineEdit, QTimeEdit, QDateEdit, QDateTimeEdit, QComboBox, QWidget
from PyQt6.QtCore import QDateTime, QSettings, QStandardPaths, QPoint, Qt, QObject,QDate,QTimer, QEvent
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication, QStandardItem
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QComboBox, QApplication,QMainWindow, QWidget,QHBoxLayout,QPushButton, QLabel, QSpacerItem, QSizePolicy,QFrame, QCheckBox, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import datetime
from pathlib import Path
from os.path import expanduser
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QFile
from database_Demandas import Ui_data_Demanda
from conecao_api import Ui_API
import pyqtgraph as pg
import numpy as np
from openpyxl import Workbook
import os
from PyQt6 import QtCore, QtGui, QtWidgets
import re
import sys
import csv
import ast
from database_Grade import Ui_data_Grade
import psycopg2
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QCloseEvent
import sys
import unicodedata
import re
class AlignedLineEditWithBorderDelegate(QStyledItemDelegate):
    def __init__(self, target_cells=None, border_color=QColor('purple'), main_window=None, parent=None):
        super().__init__(parent)
        self.target_cells = target_cells or []
        self.border_color = border_color
        self.main_window = main_window

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.installEventFilter(self)
        editor.index = index
        return editor

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.ItemDataRole.EditRole)
        editor.setText(str(text))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        if (index.row(), index.column()) in self.target_cells:
            pen = QPen(self.border_color)
            pen.setWidth(3)
            painter.setPen(pen)
            rect = option.rect
            painter.drawRect(rect)

    def update_target_cells(self, target_cells):
        self.target_cells = target_cells  # Update the target cells dynamically

class KeyFilter(QObject):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab:
                self.callback(obj)  # Pass the widget that triggered it
                return True  # Block tab default behavior (optional)
        return super().eventFilter(obj, event)

class SolicitacaoDialog(QDialog):
    def __init__(self, solicitacoes):
        super().__init__()
        self.setWindowTitle('Solicitações de Acesso')
        self.setMinimumWidth(500)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 12pt;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        main_layout = QVBoxLayout(self)

        title = QLabel('Usuários Solicitantes')
        title.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        self.checkboxes = []

        # Área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(300)  # Altura máxima para caber ~3 solicitações

        container = QWidget()
        container_layout = QVBoxLayout(container)

        for nome, email, departamento, tipo, dept_novo in solicitacoes:
            frame = QFrame()
            frame.setFrameShape(QFrame.Shape.Box)
            frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #dcdcdc;
                    border-radius: 8px;
                    padding: 8px;
                }
            """)
            frame_layout = QHBoxLayout(frame)
            if tipo == '0':
                info_label = QLabel(
                    f"<b>Nome:</b> {nome} &nbsp; | &nbsp; <b>Email:</b> {email} &nbsp; | &nbsp; <b>Perfil Solicitado:</b> {departamento}"
                )
            if tipo == '2':
                info_label = QLabel(
                    f"<b>Nome:</b> {nome} &nbsp; | &nbsp; <b>Email:</b> {email} &nbsp; | &nbsp; <b>Novo Perfil Solicitado:</b> {dept_novo}; | &nbsp; <b> Perfil Atual:</b> {departamento}"
                )
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.verificar_selecao)
            frame_layout.addWidget(checkbox)

            frame_layout.addWidget(checkbox)
            frame_layout.addWidget(info_label)
            frame_layout.addStretch()

            container_layout.addWidget(frame)
            self.checkboxes.append(checkbox)

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

        self.btn_aceitar = QPushButton('  Aceitar Solicitação   ')
        self.btn_aceitar.setVisible(False)
        self.btn_aceitar.clicked.connect(self.aceitar_solicitacao)
        main_layout.addWidget(self.btn_aceitar, alignment=Qt.AlignmentFlag.AlignCenter)

    def verificar_selecao(self):
        selecionado = any(cb.isChecked() for cb in self.checkboxes)
        self.btn_aceitar.setVisible(selecionado)

    def aceitar_solicitacao(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Aceitar Solicitações?')

        icon = QtGui.QIcon(resource_path('imagens/escondido.ico'))
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.selecionados = [i for i, cb in enumerate(self.checkboxes) if cb.isChecked()]
            print(f'Solicitações aceitas: {self.selecionados}')
            self.accept()
def resource_path(relative_path):
    """Resolve path para PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class TabTimerEventFilter(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.tab_timer = QTimer()
        self.tab_timer.setInterval(50)  # 500ms para considerar "Tab pressionado"
        self.tab_timer.setSingleShot(True)
        self.tab_timer.timeout.connect(self.on_tab_timeout)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab:
                print("🔵 TAB detectado, iniciando temporizador...")
                self.tab_timer.start()
                return True
            elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                print("🟢 ENTER pressionado")
                self.parent.set_and_move()
                return True
        return False

    def on_tab_timeout(self):
        print("🔴 TAB confirmado após timeout!")
        self.parent.set_and_move()
class AlignedLineEditDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setAutoFillBackground(True)
        return editor

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.ItemDataRole.EditRole)
        editor.setText(str(text))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class CustomHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None, cores=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)  # Permitir clique no cabeçalho
        self.cores = cores if cores else ["#FFFFFF"] * parent.rowCount()  # Lista de cores inicializada com branco

    def paintSection(self, painter, rect, logicalIndex):
        """Desenha o cabeçalho com a cor definida"""
        cor = QColor(self.cores[logicalIndex]) if logicalIndex < len(self.cores) else QColor("#FFFFFF")  # Cor definida ou branco
        painter.fillRect(rect, cor)  # Pinta o fundo
        painter.setPen(QColor("#333333"))  # Cor do texto (cinza escuro)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.model().headerData(logicalIndex, self.orientation()))
class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class CustomTitleBar(QFrame):
    def __init__(self, parent, departamento=None, user=None, nome_user=None,deman= None,janela_CTI_PED= None):
        super().__init__(parent)
        self.parent = janela_CTI_PED
        self.janela_CTI_PED = janela_CTI_PED
        self.deman = deman
        self.demanda = parent
        self.nome_user = nome_user
        self.user = user
        self.departamento = departamento
        self.setup_ui()
        self.mouse_pos = QPoint(0, 0)
        self.is_dragging = False
        self.drag_start_pos = QPoint(0, 0)
        self.drag_timer = QTimer()
        self.drag_timer.timeout.connect(self.check_drag_to_maximize)

        # Configurações do frame da barra de título
        self.setFixedHeight(40)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("""
            CustomTitleBar {
                background-color: #2E3D48;
                border: 1px solid #1a3d6d;
            }
        """)
    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Container das abas (esquerda)
        self.tab_container = QFrame()
        self.tab_container.setFixedHeight(36)
        self.tab_container.setStyleSheet("background: transparent;")
        self.tab_layout = QHBoxLayout(self.tab_container)
        self.tab_layout.setContentsMargins(5, 0, 0, 0)
        self.tab_layout.setSpacing(0)

        # Aba Demanda (selecionada por padrão)
        self.tab_demanda = QPushButton("DEMANDA")
        self.tab_demanda.setFixedSize(90, 36)
        self.tab_demanda.setCheckable(True)
        self.tab_demanda.setChecked(True)
        self.tab_demanda.setStyleSheet("""
            QPushButton {
                    background-color: #2E3D48;
                    border: 1px solid #aaaaaa;
                    border-top-right-radius: 3px;
                    border-bottom-right-radius: 0px;
                    padding: 0px;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:checked {
                    background-color: #2E3D48;
                    border-bottom: 1px solid #ffffff;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #e5f1fb;
                }
        """)
        self.tab_layout.addWidget(self.tab_demanda)

        # Aba Outra (exemplo)
        if self.departamento == 'NIR' or self.departamento == 'Administrador':
            self.btn_grade = QPushButton("GRADE")
            self.btn_grade.setFixedSize(90, 36)
            self.btn_grade.setCheckable(True)
            self.btn_grade.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #aaaaaa;
                    border-top-right-radius: 3px;
                    border-bottom-right-radius: 0px;
                    padding: 0px;
                    color: black;
                    font-weight: bold;
                }
                QPushButton:checked {
                    background-color: white;
                    border-bottom: 1px solid #ffffff;
                    color: black;
                }
                QPushButton:hover {
                    background-color: #e5f1fb;
                }
            """)
            self.tab_layout.addWidget(self.btn_grade)
            self.btn_grade.clicked.connect(lambda: self.set_active_tab('GRADE'))

            # Conectar sinais
        self.tab_demanda.clicked.connect(lambda: self.set_active_tab('DEMANDA'))

        self.layout.addWidget(self.tab_container)

        # Título da janela (centralizado)
        self.title = QLabel(f" {self.departamento} - {self.nome_user}")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                color: white;
                font-weight: bold;
                background: transparent;
                padding: 0 10px;
            }
        """)
        self.layout.addWidget(self.title)

        # Espaçador
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.custom_button1 = self.deman.notificao_label
        self.layout.addItem(spacer)
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.custom_button = self.deman.label_icone
        self.custom_button2 = self.deman.configura
        self.layout.addWidget(self.custom_button1)
        self.layout.addItem(spacer)
        self.layout.addWidget(self.custom_button2)
        self.layout.addItem(spacer)

        self.layout.addWidget(self.custom_button)

        # Botões da barra de título (direita)
        self.button_container = QFrame()
        self.button_container.setStyleSheet("background: transparent;")
        self.button_layout = QHBoxLayout(self.button_container)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(0)

        # Botão de minimizar
        self.minimize_button = QPushButton("−")
        self.minimize_button.setFixedSize(46, 38)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3a6ab1;
            }
        """)
        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.button_layout.addWidget(self.minimize_button)

        # Botão de maximizar/restaurar
        self.maximize_button = QPushButton("□")
        self.maximize_button.setFixedSize(46, 38)
        self.maximize_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3a6ab1;
            }
        """)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.button_layout.addWidget(self.maximize_button)

        # Botão de fechar
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(46, 38)
        self.close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 18px;
                border: none;
                border-top-right-radius: 3px;
            }
            QPushButton:hover {
                background-color: #e81123;
            }
        """)

        self.close_button.clicked.connect(self.fechar_tudo)
        self.button_layout.addWidget(self.close_button)

        self.layout.addWidget(self.button_container)
    def fechar_tudo(self):
        self.deman.remover_widget()
        self.demanda.close()
        self.deman.form.close()
    def set_active_tab(self, tab_name):
        """Define qual aba está ativa e atualiza a tela correspondente"""
        self.tab_demanda.setChecked(tab_name == 'DEMANDA')
        self.btn_grade.setChecked(tab_name == 'GRADE')

        # Atualiza a variável que indica a tela atual
        self.parent.t = tab_name

        if tab_name == 'GRADE':
            self.deman.atualiza_cti()
        elif tab_name == 'DEMANDA':
            self.deman.demanda_volta(self.demanda )
            self.tab_demanda.setChecked(tab_name == 'DEMANDA')
            self.btn_grade.setChecked(tab_name == 'GRADE')

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.maximize_button.setText("□")
        else:
            self.parent.showMaximized()
            self.maximize_button.setText("❐")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.globalPosition().toPoint()
            self.is_dragging = True

            if self.parent.isMaximized():
                self.parent.showNormal()
                self.maximize_button.setText("□")

                screen_geometry = QApplication.primaryScreen().availableGeometry()
                relative_x = self.drag_start_pos.x() / screen_geometry.width()

                normal_width = min(800, screen_geometry.width() - 100)
                normal_height = min(600, screen_geometry.height() - 100)
                #self.parent.resize(normal_width, normal_height)

                new_x = self.drag_start_pos.x() - int(relative_x * normal_width)
                new_y = self.drag_start_pos.y() - 10

                new_x = max(screen_geometry.left(),
                            min(new_x, screen_geometry.right() - normal_width))
                new_y = max(screen_geometry.top(),
                            min(new_y, screen_geometry.bottom() - normal_height))

                self.parent.move(new_x, new_y)
                self.mouse_pos = QPoint(int(relative_x * normal_width), event.pos().y())
            else:
                self.mouse_pos = event.globalPosition().toPoint() - self.parent.frameGeometry().topLeft()

            self.drag_timer.start(50)
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            if not self.parent.isMaximized():
                self.parent.move(event.globalPosition().toPoint() - self.mouse_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        self.drag_timer.stop()
        event.accept()

    def check_drag_to_maximize(self):
        if not self.is_dragging or self.parent.isMaximized():
            return

        current_pos = self.parent.pos()
        screen_geometry = QApplication.primaryScreen().availableGeometry()

        if current_pos.y() <= screen_geometry.y() + 5:
            self.parent.showMaximized()
            self.maximize_button.setText("❐")
            self.drag_timer.stop()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize()
            event.accept()
class Ui_CTI_PED(QtWidgets.QMainWindow):
    def closeEvent(self, event: QCloseEvent):
        print('Saiu')
        self.data_grade = Ui_data_Grade()
        self.data_grade.definir_posicao_usuario(self.variavel, self, (None,None), 'DEMANDA')
        self.remover_widget()
        self.teladem.remover_widget()
        self.teladem.mainwindow.close()
        event.accept()

    def setupUi_grade(self, Form, para_teladem=None, dept=None, user=None, nome_user=None, MainWindow=None):
        #Dados Bancos Mysql:
        self.numero_versao_atual = None
        print(21221 )
        self.host = '10.36.0.32'
        self.usermysql = 'sglHC2024'
        self.password = 'S4g1L81'
        self.database = 'sgl'

        self.codigo_ala = 29
        print(self.codigo_ala )
        # self.host = para_teladem.host
        # self.usermysql = para_teladem.usermysql
        # self.password = para_teladem.password
        # self.database = para_teladem.database

        self.data_grade = Ui_data_Grade()

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
        self.permuta_Aberta = False
        self.contas_Aberta = False
        self.conta_do_usuario_Aberta = False
        self.cria_unidade_Aberta = False
        self.current_editor = None
        self.current_pos = None
        self.tabela_atual = None
        self.action_alterar= ''

        self.indexa_pronto = False
        self.indexa_nome = False
        self.scroll_layout = None
        self.bottom_bar_layout = None

        self.lista_tooltip_label = []
        self.lista_user_pos = []
        self.lista_btn = []
        self.lista_permuta = []
        self.lista_permuta_tabela_diferente = []
        self.lista_dos_btn = []
        self.lista_titulo = []
        self.lista_ids = []

        #Dados de layout
        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)

        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        cliqu = f'{script_directory}/clicado.ini'
        self.settings_clicado = QSettings(cliqu, QSettings.Format.IniFormat)

        self.clicked = False
        self.teladem = para_teladem
        self.monitora = False

        #Form tela principal
        Form.setObjectName('Form')
        Form.showMaximized()
        Form.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        icon = QIcon(resource_path('imagens/icone_p_eUO_icon.ico'))
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
        self.frame.setMouseTracking(True)

        self.btn_dowload_senso = QtWidgets.QPushButton('Baixar Senso', parent=self.frame)
        self.btn_filtros = QtWidgets.QPushButton('▼ Selecione uma Data ', parent=self.frame)

        self.tabela_grade = QtWidgets.QTableWidget()
        header = self.tabela_grade.horizontalHeader()
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self.edit_tabela)

        self.header_colors = ["#FFFFFF"] * self.tabela_grade.rowCount()

        # Criar e definir o cabeçalho personalizado
        self.custom_header = CustomHeaderView(Qt.Orientation.Vertical, self.tabela_grade, self.header_colors)
        self.tabela_grade.setVerticalHeader(self.custom_header)

        self.tabela_grade.verticalHeader().sectionClicked.connect(self.mudar_cor_vertical_heider)
        self.tabela_grade.setColumnCount(13)
        self.tabela_grade.setRowCount(11)

        self.TITULO_CTI = QtWidgets.QLabel()
        self.SGL_label = QtWidgets.QLabel()
        self.ebserh_label = QtWidgets.QLabel("EBSERH")

        self.btn_realocar = QtWidgets.QPushButton()
        self.btn_alterar = QtWidgets.QPushButton()
        self.MONITORAMENTO = QtWidgets.QPushButton()
        self.DEMANDAS = QtWidgets.QPushButton()
        self.GRAFICOS = QtWidgets.QPushButton()
        self.GRADE = QtWidgets.QPushButton()
        self.btn_alta = QtWidgets.QPushButton()
        self.btn_permuta = QtWidgets.QPushButton()
        self.btn_permuta_diferentes_tabelas = QtWidgets.QPushButton()
        self.deixar_vago = QtWidgets.QPushButton()
        self.btn_ocupar_leito = QtWidgets.QPushButton()
        self.historio = QtWidgets.QPushButton()
        self.BARRADEPESQUISA = QtWidgets.QLineEdit()
        self.btn_relatorio = QtWidgets.QPushButton()
        self.SAIR = QtWidgets.QPushButton()
        self.list_tabela = []
        self.label_icone = ClickableLabel(parent=Form)
        self.BARRADEPESQUISA.setObjectName('BARRADEPESQUISA')

        self.widget_monitora =  QtWidgets.QScrollArea(self.frame)
        self.lista_modificacao = []

        from front_grade import Front_Grade
        self.Front_Grade = Front_Grade()
        self.Front_Grade.layout(dept, self)

        self.data_deman = Ui_data_Demanda()

        self.api = Ui_API()
        screen = QGuiApplication.primaryScreen()
        size = screen.size()
        width = size.width() - 10
        height = size.height() - 35
        self.BARRADEPESQUISA.hide()

        #Frame do relátorio
        self.frame_relatorio = QtWidgets.QFrame(parent=self.frame)
        self.frame_relatorio.setStyleSheet('background-color: #2c7f4f;')
        self.frame_relatorio.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_relatorio.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_relatorio.setObjectName('frame')
        self.frame_relatorio.setVisible(False)
        self.frame_relatorio.setGeometry(0, 25, width, height)

        #COMPOSIÇAO DO SENSO
        self.frame_senso = QtWidgets.QFrame(parent=self.frame)
        self.frame_senso.setStyleSheet('background-color: #2c7f4f;')
        self.frame_senso.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_senso.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_senso.setObjectName('frame')
        self.frame_senso.setVisible(False)
        self.frame_senso.setGeometry(0, 25, width, height)

        self.btn_dowload_senso.setGeometry(QtCore.QRect(230, 0, 150, 23))
        self.btn_dowload_senso.hide()
        self.btn_dowload_senso.setToolTip('Baixar Senso')

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
        sidebar_y = 0
        sidebar_height = self.height() + 200
        self.sidebar = QtWidgets.QFrame(parent=Form)
        self.sidebar.setGeometry(sidebar_x, 40, sidebar_width, sidebar_height)
        self.sidebar.setStyleSheet('border: 2px solid #2E3D48;background-color: #2c7f4f; border-radius: 10px;')
        self.sidebar.setVisible(False)

        sidebar_layout = QtWidgets.QVBoxLayout()
        self.sidebar.setLayout(sidebar_layout)

        self.foto_do_usuario = QtWidgets.QLabel()
        self.foto_do_usuario.setFixedSize(145, 121)
        self.foto_do_usuario.setStyleSheet('border: 2px solid #2E3D48; border-radius: 10px;')
        self.foto_do_usuario.setText('')
        sidebar_layout.addWidget(self.foto_do_usuario, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        pasta_imagens = Path(expanduser("~")) / "Pictures"
        caminho_imagem = pasta_imagens / f"imagem_do_usuario_{self.user}.png"

        if QFile.exists(str(caminho_imagem)):
            pixmap = QPixmap(str(caminho_imagem))
            if not pixmap.isNull():
                self.foto_do_usuario.setPixmap(pixmap.scaled(
                    self.foto_do_usuario.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
                self.foto_do_usuario.setScaledContents(False)
            else:
                print("Imagem encontrada, mas não pôde ser carregada.")
        else:
            print(f"Imagem não encontrada: {caminho_imagem}")

        icon = QtGui.QIcon(resource_path('imagens/user.ico'))
        pixmap = icon.pixmap(25, 25)
        sidebar_width = 40
        sidebar_x = size.width() - sidebar_width
        sidebar_y = 40

        self.label_icone.setPixmap(pixmap)
        self.label_icone.setFixedSize( 25, 25)
        self.label_icone.setStyleSheet('border-radius: 10px;color: black;')
        self.label_icone.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_icone.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)

        tooltip_text = self.nome_user
        self.label_icone.setToolTip(tooltip_text)
        self.label_icone.show()
        self.label_icone.clicked.connect(self.onIconClick)

        icon = QtGui.QIcon(resource_path('imagens/notificacao.ico'))
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

        print(self.codigo_ala )
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
        self.NOME.setFixedSize(180, 30)
        self.painel = QtWidgets.QPushButton()
        self.painel_voltar = QtWidgets.QPushButton(self.frame)
        self.painel_voltar.hide()
        self.senso = QtWidgets.QPushButton()

        self.procura_pac.setToolTip(tooltip_text)

        self.configura  = ClickableLabel()

        icon = QtGui.QIcon(resource_path('imagens/configuracoes-_1_.ico'))
        pixmap = icon.pixmap(25, 25)
        self.configura.setPixmap(pixmap)
        self.configura.setFixedSize( 25, 25)
        self.configura.setStyleSheet('border-radius: 10px;')
        self.configura.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.configura.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)

        tooltip_text = user
        self.configura.setToolTip(tooltip_text)
        self.configura.clicked.connect(lambda: self.abrir_configuracoes(Form))

        buttons = [
            ('USUÁRIO', self.usuario),
            ('GRÁFICOS', self.GRAFICOS),
            ('MONITORAMENTO', self.MONITORAMENTO),
            ('PAINEL', self.painel),
            ('CENSO', self.senso),
            ('RELATÓRIO', self.btn_relatorio),
            ('HISTORICO', self.historio),
            ('PROCURAR PACIENTE', self.procura_pac),
            ('SAIR', self.SAIR)
        ]
        #Tipo Admin administra Usuários
        if self.dept == 'Administrador':
            self.usuarios_contas = QtWidgets.QPushButton('USUÁRIOS', self.sidebar)
            self.usuarios_contas.clicked.connect(lambda: self.abrir_contas(Form))

            #self.criar_nova_unidade = QtWidgets.QPushButton('CRIAR NOVA UNIDADE', self.sidebar)
            #self.criar_nova_unidade.clicked.connect(lambda: self.abrir_novas_unidades(Form))
            buttons = [
            ('USUÁRIO', self.usuario),
            ('GRÁFICOS', self.GRAFICOS),
            ('MONITORAMENTO', self.MONITORAMENTO),
            ('PAINEL', self.painel),
            ('CENSO', self.senso),
            ('RELATÓRIO', self.btn_relatorio),
            ('HISTORICO', self.historio),
            ('PROCURAR PACIENTE', self.procura_pac),
            ('USUÁRIOS', self.usuarios_contas),
            ('SAIR', self.SAIR)
            ]

        sidebar_layout.addWidget(self.NOME)
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
        for text, btn in buttons:
            btn.setText(text)
            btn.setFixedSize(180, 30)
            btn.setStyleSheet(LAYOUT_BTN)
            
            self.painel_voltar.setStyleSheet('''
                            QPushButton {
                                border: 2px solid #2E3D48;
                                border-radius: 10px;
                                background-color: #FFFFFF;
                                color: #2E3D48;
                            }
                            QPushButton:pressed {
                                background-color: #2E3D48;
                                color: #FFFFFF;
                            }
                        ''')
            sidebar_layout.addWidget(btn)
        self.t = 'Grade'


        self.NOME.setFont(font)

        self.NOME.setStyleSheet('border: 2px solid transparent; border-radius: 10px;')

        self.configura.setGeometry(10, 300, 180, 30)
        self.usuario.setGeometry(10, 200, 180, 30)
        self.procura_pac.setGeometry(10, 250, 180, 30)

        print(self.codigo_ala )
        self.tabela_grade.cellClicked.connect(self.tabela_clicada)

        self.barra = self.tabela_grade.horizontalScrollBar().value()
        self.barra_vertical = self.tabela_grade.verticalScrollBar().value()

        self.tabela_grade.horizontalScrollBar().valueChanged.connect(self.check_scrollbar_value)
        self.tabela_grade.verticalScrollBar().valueChanged.connect(self.check_scrollbar_value)
        self.tabela_alt = QtWidgets.QTableWidget()
        self.tabela_alt2 = QtWidgets.QTableWidget()

        self.delegate = AlignedLineEditWithBorderDelegate(
            target_cells=[],
            border_color=QColor('white'),
            main_window=self  # <-- passe self aqui
        )

        self.tabela_grade.setItemDelegate( self.delegate)

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

        self.tabela_grade.show()
        screen = QGuiApplication.primaryScreen()
        size = screen.size()

        print(self.codigo_ala )
        self.btn_width = size.width() - 216
        conta_linha = self.tabela_grade.rowCount()

        for conta in range(conta_linha):

            item = self.tabela_grade.item(conta, 0)
            if item is not None and item.background().style() != QtGui.QBrush().style():
                adjusted_color = item.background().color()
            else:
                adjusted_color = QColor("white")
            self.colocar_caixa_selecao(conta, adjusted_color)

        self.btn_realocar.setObjectName('btn_realocar')

        self.btn_alterar.setObjectName('btn_alterar')

        self.editable = False

        # Abrir Monitoramento
        self.MONITORAMENTO.setObjectName('MONITORAMENTO')
        self.MONITORAMENTO.clicked.connect(lambda: self.monitoramento(Form))

        # Abrir demandas
        self.DEMANDAS.setObjectName('DEMANDAS')
        self.DEMANDAS.clicked.connect(lambda: self.abrir_demanda(Form))

        #Abrir GRADE
        self.GRADE.setObjectName('GRADE')
        self.GRADE.clicked.connect(lambda: self.voltar_grade(Form))

        #Abrir Gráficos
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

        print(self.codigo_ala )
        #Dar alta
        self.btn_alta.setGeometry(QtCore.QRect(self.btn_width, 320, 210, 31))
        self.btn_alta.setObjectName('btn_alta')
        self.btn_alta.clicked.connect(lambda: self.alta(Form, self.teladem))

        self.btn_permuta.setGeometry(QtCore.QRect(self.btn_width, 360, 210, 31))
        self.btn_permuta.setObjectName('btn_permuta')
        self.btn_permuta.clicked.connect( self.trocando_pacientes_mesma_tabela)
        self.btn_permuta.hide()
        self.deixar_vago.hide()
        self.btn_ocupar_leito.hide()
        self.btn_permuta_diferentes_tabelas.hide()
        self.btn_permuta_diferentes_tabelas.clicked.connect( self.trocar_pacientes_diferente_tabela)

        self.deixar_vago.clicked.connect( self.leito_vago)
        self.btn_ocupar_leito.clicked.connect( self.ocupar_leito)

        # Pesquisa de pacientes
        self.BARRADEPESQUISA.textChanged.connect(self.pesquisar)
        self.BARRADEPESQUISA.setPlaceholderText('Pesquisar Paciente')

        icon = QIcon(resource_path('imagens/lupa.ico'))
        self.BARRADEPESQUISA.addAction(icon, QtWidgets.QLineEdit.ActionPosition.LeadingPosition)
        btn_width = size.width() - 236

        #Abrir historico
        self.historio.setObjectName('historio')
        self.historio.clicked.connect(lambda: self.abrir_historico(Form))

        #Abrir painel
        self.painel.setObjectName('painel')
        self.painel.clicked.connect(lambda: self.abrir_painel(Form))
        self.painel_voltar.clicked.connect(lambda: self.abrir_painel(Form))

        #Abrir senso
        self.senso_Aberta = False
        self.senso.setObjectName('SENSO')
        self.senso.clicked.connect(lambda: self.abrir_senso(Form))

        #Abrir relatorio
        self.btn_relatorio.setObjectName('RELATORIO')
        self.btn_relatorio.clicked.connect(lambda: self.abri_relatorio(Form))

        #Fechar sgl

        self.SAIR.setObjectName('SAIR')
        self.SAIR.clicked.connect(lambda: self.finalizar_operacao(MainWindow))

        self.widget_monitora.setWidgetResizable(True)
        self.widget_monitora.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.widget_monitora.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        scroll_contentmonitora = QtWidgets.QWidget()
        self.widget_monitora.setWidget(scroll_contentmonitora)

        scroll_layoutmonitora = QtWidgets.QHBoxLayout(scroll_contentmonitora)
        scroll_layoutmonitora.setContentsMargins(0, 0, 0, 0)
        scroll_layoutmonitora.setSpacing(0)

        self.frame_do_monitoramento = QtWidgets.QFrame()
        self.frame_do_monitoramento.setStyleSheet(
            'background-color: transparent; border: 2px solid black; border-radius: 10px;')
        self.frame_do_monitoramento.setFixedSize(1500, 800)# Optional: define the scroll area geometry

        self.frame_do_monitoramento.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_do_monitoramento.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_do_monitoramento.setObjectName('frame')

        scroll_layoutmonitora.addWidget(self.frame_do_monitoramento)

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
        height = size.height() - 130

        self.help_sccrol_painel = False
        self.scroll_painel = QScrollArea(self.frame)
        self.scroll_painel.setWidgetResizable(True)
        self.scroll_painel.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_painel.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
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

        self.frame_permuta = QtWidgets.QFrame(parent=self.frame)
        self.frame_permuta.hide()

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
        self.header_colors = ["#FFFFFF"] * self.tabela_grade.rowCount()
        #self.abri_cti(Form, 'CTI PEDIÁTRICO - 06N')

        self.abri_cti(Form, self.lista_ids[0], self.lista_titulo[0], self.lista_dos_btn[0])
        for row in range(self.tabela_grade.rowCount()):
            selecao = self.tabela_grade.item(row, 0)
            item = self.tabela_grade.verticalHeaderItem(row)
            if 'aguardando' not in item.text() and selecao.checkState() == QtCore.Qt.CheckState.Checked:
                self.timer.stop()
                self.timer_post.stop()
                self.timer_mysql.stop()

        self.tela = 'Grade'
        self.horizontalLayout.addWidget(self.frame)


        self.title_bar = CustomTitleBar(MainWindow, dept, user, nome_user,self,Form)
        Form.setMenuWidget(self.title_bar)
        Form.setCentralWidget(self.centralwidget)
        self.frame.raise_()

        for btn in self.sidebar.findChildren(QtWidgets.QPushButton):
            #btn.setStyleSheet('\n                QPushButton {\n                    border: 2px solid #2E3D48;\n                    border-radius: 10px;\n                    background-color: #FFFFFF;\n                    color: #2E3D48;\n                }\n\n                QPushButton:hover {\n                    background-color: #DDDDDD;  /* Change this to your desired hover color */\n                    color: rgb(0, 0, 0);\n                }\n\n                QPushButton:pressed {\n                    background-color: #2E3D48;  /* Change this to your desired pressed color */\n                    color: #FFFFFF;\n                }\n            ')
            tooltip_text = btn.text()
            if btn.text() == 'X':
                tooltip_text = 'Fechar'
            btn.setToolTip(tooltip_text)
        print(1)
        self.bloqueado_senso= 0

        self.ocupado_senso =0
        self.total=0
        self.data_grade.atualizar_senso(self)
        print(11)
        self.atualizar_painel()

        #Configurções para telespectador
        if self.dept == 'Telespectador':
            self.btn_realocar.hide()
            self.btn_alterar.hide()
            self.btn_alta.hide()
            self.btn_permuta.hide()
            self.senso.hide()
            self.btn_relatorio.hide()
            self.SAIR.setGeometry(QtCore.QRect(540, 0, 75, 23))

    # Função ligada ao temporizador para que novo usuário seja aceito pelo admin
    def aceitar_user(self):
        self.time_user.stop()

        solicitacoes = []
        users = []
        leitura = self.data_deman.ler_cadastros(self)

        for linha in leitura:
            if len(linha) > 0:
                if (linha[2] == '0'):
                    usuario = self.api.buscar_usuario(linha[0])
                    solicitacoes.append((linha[1], usuario['email'], linha[3], '0', ''))
                    users.append(linha[0])
                if (linha[2] == '2'):
                    usuario = self.api.buscar_usuario(linha[0])
                    solicitacoes.append((linha[1], usuario['email'], linha[3], '2', linha[4]))
                    users.append(linha[0])

        if len(solicitacoes) > 0:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('Existem Usuários que Solicitam permissão para acessar o software!')

            icon = QtGui.QIcon(resource_path('imagens/escondido.ico'))
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            yes_button = msg_box.button(QMessageBox.StandardButton.Yes)
            yes_button.setText('Abrir Tela de Usuários')

            no_button = msg_box.button(QMessageBox.StandardButton.No)
            no_button.setText('Esperar')

            reply = msg_box.exec()
            if reply == QMessageBox.StandardButton.Yes:
                dialog = SolicitacaoDialog(solicitacoes)
                if dialog.exec():
                    for i in dialog.selecionados:
                        print(solicitacoes[i][0], users[i])
                        self.data_deman.update_cadastro('1', users[i], solicitacoes[i][2], '')

                    self._mostrar_mensagem('Conta Cadastrada com Sucesso!')
            if reply == QMessageBox.StandardButton.No:
                return

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
        #     self.btn_alterar.show()
        #     self.btn_alta.show()
        #     self.btn_permuta.show()
        #     self.btn_realocar.show()
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

            tamanho_frame = self.frame.width()
            tamanho_frame_h = self.frame.height()

            self.frame.setMaximumWidth(tamanho_frame)
            self.frame.setMaximumHeight(tamanho_frame_h)

            #self.grade.widget_monitora.setMaximumWidth(self.tamanho_frame)
            #self.grade.widget_monitora.setMaximumHeight(self.tamanho_frame_h)
            if self.codigo_ala == 29:
                self.monitora_cti_ped(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 23:
                self.uco(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 30:
                self.monitora_6_leste(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 36:
                self.monitora_10_norte(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 169:
                self.monitora_cti_ps(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 22:
                self.monitora_2_leste(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 21:
                self.monitora_2_sul(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 32:
                self.monitora_7_leste(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 31:
                self.monitora_7_norte(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 33:
                self.monitora_8_sul(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 34:
                self.monitora_8_leste(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 193:
                self.monitora_8_norte(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 35:
                self.monitora_9_leste(Form, self.frame_do_monitoramento)
            elif self.codigo_ala == 24:
                self.monitora_3_leste(Form, self.frame_do_monitoramento)
            else:
                return

            self.widget_monitora.show()
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
            self.frame_do_monitoramento.show()
        else:  # inserted
            self.monitora = False
            self.frame_do_monitoramento.hide()
            self.TITULO_CTI.show()
            if self.dept!= 'Telespectador':
                # self.btn_alterar.show()
                # self.btn_alta.show()
                # self.btn_permuta.show()
                # self.btn_realocar.show()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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
            self.btn_permuta.hide()
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

        tamanho_frame = self.frame.width()
        tamanho_frame_h = self.frame.height()

        self.frame.setMaximumWidth(tamanho_frame)
        self.frame.setMaximumHeight(tamanho_frame_h)
        if self.frame_do_monitoramento.isVisible():
            self.frame_do_monitoramento.hide()
        if self.frame_do_grafico.isHidden():
            self.frame_do_grafico.show()
            if self.dept!= 'Telespectador':
                self.btn_alterar.hide()
                self.btn_alta.hide()
                self.btn_permuta.hide()
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
                # self.btn_alterar.show()
                # self.btn_alta.show()
                # self.btn_permuta.show()
                # self.btn_realocar.show()
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
            icon = QIcon(resource_path('imagens/warning.ico'))
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
        connection = None
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
                #print('esses mesmo', dados)

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

            #print('caminho 1')
        except psycopg2.Error as e:
            print('Erro ao conectar ao PostgreSQL:', e)

        finally:
            if connection:
                cursor.close()
                connection.close()

            #print('caminho 2')
            conexao = pymysql.connect(host=self.host, user=self.usermysql, password=self.password, database='sgl')
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM tabelas_grade_names WHERE id = %s", (self.codigo_ala,))
            leitura = cursor.fetchone()

            nome_tabela = leitura[1]
            coluna_bd = None
            for idx, valor in enumerate(leitura[3:], start=3):

                match str(valor).strip().upper():
                    case "SEXO DA ENFERMARIA":
                        coluna_bd = "col" if idx - 3 == 0 else f"col{idx - 3}"

            for leitos, sexo_leito in lista_leitos:
                comando = f'SELECT idGRADE FROM grade WHERE idGRADE = \'{leitos}\''
                cursor.execute(comando)
                resultado = cursor.fetchone()

                if not resultado:
                    comando = f'INSERT INTO grade (idGRADE) VALUES (\'{leitos}\')'
                    cursor.execute(comando)
                    conexao.commit()
                    leitura = cursor.fetchone()
                if coluna_bd is not None:
                    comando = f'UPDATE grade SET {coluna_bd} = \"{sexo_leito}\" WHERE idGRADE = \"{leitos}\"'
                    cursor.execute(comando)
                    conexao.commit()

            cursor.close()
            conexao.close()
        #print('caminho 1')

    #abrir os cti's e enfermarias
    def abri_cti(self, Form, variavel, nome, btn):
        self.codigo_ala == variavel
        #print('cti')
        self.inicio = True
        self.quantidade_colunas = 0
        self.lista_nomes_das_colunas = []
        self.lista_widgets = []
        self.lista_permuta = []
        self.data_grade.ler_colunas_Grade(self, variavel)
        self.data_grade.ler_Widgets_Grade(self, variavel)

        self.deixar_vago.hide()
        self.btn_ocupar_leito.hide()

        self.tabela_grade.setColumnCount(self.quantidade_colunas + 1)
        for col in range(self.tabela_grade.columnCount()):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
            font.setPointSize(8)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tabela_grade.setHorizontalHeaderItem(col, item)
        style_normal = """
                        QPushButton {
                            background-color: transparent;
                            color: black;
                            border: none;
                            padding: 10px 20px;
                            font-size: 14px;
                        }
                        QPushButton:hover {
                            background-color: #555;
                        }
                        QPushButton:pressed {
                            background-color: #777;
                        }
                    """

        style_clicado = """
                        QPushButton {
                            background-color: white;
                            color: black;
                            font-size: 16px;
                            font-weight: bold;
                            border: none;
                            padding: 10px;
                            border-radius: 5px;
                        }
                        QPushButton:hover {
                            background-color: #c1d9f7;
                        }
                        QPushButton:pressed {
                            background-color: #99c3f4;
                        }
                    """

        # Aplicando estilos
        for btn_ in self.lista_dos_btn:
            if btn == btn_:
                btn.setStyleSheet(style_clicado)
            else:
                btn_.setStyleSheet(style_normal)
            tooltip_text = btn.text()
            btn_.setToolTip(tooltip_text)

        self.retranslateUi_CTI(Form)
        self.nome_tabela_post = nome
        self.ler_PostgreSQL(nome)
        self.timer.stop()
        self.timer_post.stop()
        self.timer_mysql.stop()
        self.atualiza_mysql()
        self.atualiza_cti()
        self.TITULO_CTI.setText(f'{nome}')
        self.temporizador()
        self.modificador_cor_cell()
        #self.ler_movimentacao_post()
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
        print('nam')


    #função get_corrent usada para pegar a posicao na tabela
    def get_current_position(self):
        current_item = self.tabela_grade.currentItem()
        if current_item:
            self.posicao_inicial_row = current_item.row()
            self.posicao_inicial_colum = current_item.column()

    #Identifica a movimentação de Leitos
    def ler_movimentacao_post(self):
        print('mov post')
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
            limite_inferior = data_atual - timedelta(hours=24)

            data_tres_dias_atras = data_atual - timedelta(days=10)
            #print(rows)
            for row in rows:
                sem_hifen = row[0].split('-')[0]
                semzero = row[2].lstrip('0')
                dados = f'{sem_hifen}_{semzero}'
                data_fornecida = row[3]
               # print(data_fornecida,data_atual)
                if limite_inferior <= data_fornecida <= data_atual:
                   # print('entrada')
                    lista_leitos_alta.append((dados, row[4]))

               # print(lista_leitos_alta)
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
                      #  print(str(codigo), item.text(), 'alçta')
                        if item is not None and item.text() == str(codigo):
                            self.alta_automatica(row)

            # if status is not None and status.text() == 'RESERVADO':
            #     for leito, codigo, codigo_npf in lista_leitos_internacao:
            #         leito = leito.replace('_', ' ')
            #         if leito == self.tabela_grade.verticalHeaderItem(row).text():
            #             item = self.tabela_grade.item(row, colum_npf)
            #             if item is not None and item.text() == str(codigo_npf):
            #                 self.ocupacao_automatica(row, codigo)

        #self.atualiza_cti()

    def atualizar_color_vertical_heider(self, lista_leitos):
        try:
            self.header_colors = ["#FFFFFF"] * self.tabela_grade.rowCount()
            # Conecta ao banco de dados
            conexao = pymysql.connect(host=self.host, user=self.usermysql, password=self.password, database='sgl')
            cursor = conexao.cursor()

            # Constrói a string de leitos para a consulta SQL
            leitos_str = ', '.join([f'"{leito}"' for leito in lista_leitos])

            # Executa a consulta
            comando = f'SELECT * FROM color_table WHERE leito IN ({leitos_str})'
            cursor.execute(comando)
            leitura = cursor.fetchall()

            # Itera sobre os resultados da consulta
            for linha in leitura:
                leito_db = linha[0]  # Valor do leito no banco de dados
                cor = linha[1]  # Cor correspondente

                # Itera sobre as linhas do cabeçalho vertical da tabela
                for linha_analisa in range(self.tabela_grade.rowCount()):
                    leitos = self.tabela_grade.verticalHeaderItem(linha_analisa)
                    if leitos is not None:
                        LEITOS = leitos.text().replace(' ', '_')
                        if leito_db == LEITOS:
                            if cor == '#550000':
                                self.tabela_grade.setRowHidden(linha_analisa, True)
                            else:
                                self.header_colors[linha_analisa] = cor

            # Aplica as novas cores ao cabeçalho
            self.custom_header.cores = self.header_colors
            self.custom_header.viewport().update()

        finally:
            # Fecha o cursor e a conexão
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    # funcao atualiza_cti atualiza as tabelas
    def atualiza_cti(self):
        lista_clear = []
        for row in range(self.tabela_grade.rowCount()):
            for col in range(self.tabela_grade.columnCount()):
                lista_clear.append((row, col))
        delegate = AlignedLineEditWithBorderDelegate(
            target_cells=lista_clear,
            border_color=QColor('white'),
            main_window=self
        )
        self.tabela_grade.setItemDelegate(delegate)
        cell_list= []
        if self.current_pos is not None:
            old_row, old_col = self.current_pos
            for col in range(self.tabela_grade.columnCount()):
                cell_list.append((old_row, col))

        delegate = AlignedLineEditWithBorderDelegate(
            target_cells=cell_list,
            border_color=QColor(0, 100, 0),  # dark green
            main_window=self
        )
        self.tabela_grade.setItemDelegate(delegate)
        delegate = AlignedLineEditWithBorderDelegate(
            target_cells=self.lista_user_pos,
            border_color=QColor('purple'),
            main_window=self
        )
        self.tabela_grade.setItemDelegate(delegate)

       # self.ler_movimentacao_post()
        print('dentro')
        delegate = AlignedLineEditDelegate(self.tabela_grade)
        for colum in range(self.tabela_grade.columnCount()):
            self.tabela_grade.setItemDelegateForColumn(colum, delegate)
            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == 'NPF':
                self.tabela_grade.hideColumn(colum)

        lista_leitos = self.data_grade.lista_leitos_filtro_aghu(self)

        if self.tabela_grade.currentItem():
            self.selection = (self.tabela_grade.currentRow(), self.tabela_grade.currentColumn())
        incio = self.inicio
        leitura = self.data_grade.ler_database(self, lista_leitos)
       # print('ana', len(leitura))

        if self.inicio == True:
            self.tabela_grade.clearContents()
            self.tabela_grade.setRowCount(0)
            self.inicio = False

        row = -1
        for linha in leitura:
            row += 1
            for column, valor in enumerate(linha):
                if column == 0:
                    texto_item = str(valor)
                    if texto_item not in lista_leitos:
                        parts = texto_item.split('_')
                        new_string = '_'.join(parts[:2])
                        if new_string not in lista_leitos:
                            continue

                    if incio:
                        self.tabela_grade.insertRow(row)
                    elif self.tabela_grade.verticalHeaderItem(row) is None or self.tabela_grade.verticalHeaderItem(
                            row).text() != texto_item.replace('_', ' '):
                       # print(self.tabela_grade.rowCount(),'espacao', len(leitura))
                        if texto_item not in lista_leitos:
                            parts = texto_item.split('_')
                            new_string = '_'.join(parts[:2])
                            if new_string not in lista_leitos:
                                continue
                        while self.tabela_grade.rowCount() < len(leitura):
                            self.tabela_grade.insertRow(self.tabela_grade.rowCount())
                        while self.tabela_grade.rowCount() > len(leitura):
                            self.tabela_grade.removeRow(self.tabela_grade.rowCount()-1)
                    else:
                        continue
                    item_texto = texto_item.replace('_', ' ')
                    item = QtWidgets.QTableWidgetItem(item_texto)
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
        self.modificador_cor_cell()
        for colum in range(1, self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum).text()
            text_width = self.fontMetrics().boundingRect(item_pac).width()
            self.increase_column_width(colum, text_width + 100)
        item = self.tabela_grade.item(self.posicao_inicial_row, self.posicao_inicial_colum)
        #self.tabela_grade.scrollToItem(item)
        if self.selection:
            row, col = self.selection
            self.tabela_grade.setCurrentCell(row, col)
        self.atualizar_color_vertical_heider(lista_leitos)
        for j in range(self.tabela_grade.columnCount()):
            old_row =1
            delegate = AlignedLineEditWithBorderDelegate(
                target_cells=[(old_row, j)],
                border_color=QColor('purple'),
                main_window=self
            )
            self.tabela_grade.setItemDelegate(delegate)
            delegate.update_target_cells([(old_row, j)])
            self.tabela_grade.viewport().update()

    def modificador_cor_cell(self):
        contador = 0
        for row in range(self.tabela_grade.rowCount()):
            item = self.tabela_grade.verticalHeaderItem(row)
            excel_blue = QtGui.QColor(255, 255, 255)
            adjusted_color = excel_blue.lighter(100)
            if 'aguardando' in item.text():
                self.tabela_grade.setItem(row, 0, None)

                btn_excluir = QtWidgets.QPushButton('X')
                btn_excluir.setStyleSheet('\n                                           QPushButton {\n                                               border: 2px solid #2E3D48;\n                                               border-radius: 10px;\n                                               background-color: transparent;\n                                               color: black;\n                                           }\n                                           QPushButton:pressed {\n                                               background-color: #black;\n                                               color: #FFFFFF;\n                                           }\n                                       ')
                btn_excluir.clicked.connect(lambda _, r=row: (self.apagar_linha(r)))
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
                        for coluna_bloqueia in range(self.tabela_grade.columnCount()):
                            if coluna_bloqueia!= 0:
                                item_bloqueia = self.tabela_grade.item(row, coluna_bloqueia)
                                new_item_bloqueia = QtWidgets.QTableWidgetItem(item_bloqueia.text())
                                new_item_bloqueia.setBackground(QtGui.QColor(200, 200, 200))
                                new_item_bloqueia.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                                self.tabela_grade.setItem(row, coluna_bloqueia, new_item_bloqueia)

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
                selecao = self.tabela_grade.item(row, 0)
                if selecao:
                    if selecao.checkState() != QtCore.Qt.CheckState.Checked:
                        self.tabela_grade.setItem(row, 0, None)
                        selecao = QtWidgets.QTableWidgetItem()
                        selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                        selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
                        selecao.setBackground(QtGui.QBrush(adjusted_color))
                        self.tabela_grade.setItem(row, 0, selecao)

                    else:
                        contador+=1

                        self.ativar_btn_permutas()

                else:
                    self.tabela_grade.setItem(row, 0, None)
                    selecao = QtWidgets.QTableWidgetItem()
                    selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                    selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
                    selecao.setBackground(QtGui.QBrush(adjusted_color))
                    id_valor = self.tabela_grade.verticalHeaderItem(row).text()

                    if any(id_valor == tupla[1] for tupla in self.lista_permuta_tabela_diferente):

                        selecao.setCheckState(QtCore.Qt.CheckState.Checked)
                    self.tabela_grade.setItem(row, 0, selecao)

            for colum in range(self.tabela_grade.columnCount()):
                dados = self.tabela_grade.item(row, colum)
                if dados is None:
                    dados = ''
                    item = QtWidgets.QTableWidgetItem(str(''))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabela_grade.setItem(row, colum, item)
                else:
                    dados = dados.text()
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
        if contador == 0:
            self.deixar_vago.hide()
            self.btn_ocupar_leito.hide()
            self.btn_alta.hide()
            self.btn_permuta.hide()
        if contador > 0:
            self.deixar_vago.show()
            #self.chamar_btn_alta()
            coluna = self.descobrir_nome_coluna('STATUS DO LEITO', None)

        if contador == 2:
            self.btn_permuta.show()
        else:
            self.btn_permuta.hide()
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
        conexao = pymysql.connect(host=self.host, user=self.usermysql, password=self.password, database='sgl')
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
        conexao = pymysql.connect(host=self.host, user=self.usermysql, password=self.password, database='sgl')
        cursor = conexao.cursor()
        cursor.execute('SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'grade\' ORDER BY ORDINAL_POSITION')
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
            Comando = f'UPDATE grade SET {colunas[colum]} = \"{valor_para_atualizar}\" WHERE idGRADE = \"{leito}\"'
            cursor.execute(Comando)
        conexao.commit()
        cursor.close()
        conexao.close()

        self.data_grade.retirar_aguardando(row, self)
        self.atualiza_cti()

    def ocupacao_automatica(self, row, codigo):
        colum_status = 0
        for colum in range(self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == 'STATUS DO LEITO':
                colum_status = colum
        conexao = pymysql.connect(host=self.host, user=self.usermysql, password=self.password, database='sgl')
        cursor = conexao.cursor()
        leito = self.tabela_grade.verticalHeaderItem(row)
        leito = leito.text().replace(' ', '_')
        Comando = f'UPDATE grade SET STATUS_DO_LEITO = \"OCUPADO\", CODIGO_DE_INTERNACAO = {codigo} WHERE idGRADE = \"{leito}\"'
        cursor.execute(Comando)
        item_ocupado = QTableWidgetItem('OCUPADO')
        self.tabela_grade.setItem(row, colum_status, item_ocupado)
        conexao.commit()
        cursor.close()
        conexao.close()
        self.atualiza_cti()

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
        conexao = pymysql.connect(host=self.host, user=self.usermysql, password=self.password, database='sgl')
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
            msg_box.setText('Dar Alta?')
            icon = QIcon(resource_path('imagens/warning.ico'))
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            reply = msg_box.exec()
            if reply == QMessageBox.StandardButton.Yes:

                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText('Alta Confirmada!')
                icon = QIcon(resource_path('imagens/warning.ico'))
                msg_box.setWindowIcon(icon)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.exec()

                for row in reversed(selecionado):
                    for idx, id in enumerate(para_teladem.lista_ids):
                        if id == 'alta_cti':
                            para_teladem.abrir_tabela(para_teladem.mainwindow, para_teladem.lista_ids[idx], para_teladem.lista_titulo[idx],
                                              para_teladem.lista_dos_btn[idx])
                            for i in range(para_teladem.tabelademan.rowCount()):
                                id_valor = para_teladem.tabelademan.verticalHeaderItem(i)
                                if id_valor is not None and id_valor.text() != '':
                                    continue

                                colum_paciente = para_teladem.descobrir_nome_coluna('NOME DO PACIENTE', None)
                                colum_data_nace = para_teladem.descobrir_nome_coluna('DATA DE NASCIMENTO', None)
                                colum_prontuario = para_teladem.descobrir_nome_coluna('PRONTUÁRIO', None)
                                colum_npf = para_teladem.descobrir_nome_coluna('NPF', None)

                                nome = self.tabela_grade.item(row, colum_nome)
                                data_nasc = self.tabela_grade.item(row, colum_data_nas)
                                pronto = self.tabela_grade.item(row, colum_prontuario).text()
                                npf = self.tabela_grade.item(row, colum_npf).text()

                           #     print('analisando dados alta', pronto,nome.text(),data_nasc.text(),npf)
                                if colum_prontuario is not None:

                                    self.data_deman.inserir_na_tabela(para_teladem, 'alta_cti', pronto, str(i + 1),
                                                                      colum_prontuario)
                                    if colum_paciente is not None:
                                        self.data_deman.modificar_tabela(para_teladem, 'alta_cti', nome.text(), str(i + 1),
                                                                         colum_paciente)
                                    if colum_data_nace is not None:
                                        self.data_deman.modificar_tabela(para_teladem, 'alta_cti', data_nasc.text(), str(i + 1),
                                                                         colum_data_nace)
                                    if colum_npf is not None:
                                        self.data_deman.modificar_tabela(para_teladem, 'alta_cti', npf, str(i + 1), colum_npf)

                                elif colum_paciente is not None:
                                    # self.data_deman.inserir_na_tabela(para_teladem, 'alta_cti', texto, str(i + 1), colum)
                                    if colum_data_nace is not None:
                                        self.data_deman.modificar_tabela(para_teladem, 'alta_cti', data_nasc.text(), str(i + 1),
                                                                         colum_data_nace)
                                    if colum_npf is not None:
                                        self.data_deman.modificar_tabela(para_teladem, 'alta_cti', npf, str(i + 1), colum_npf)
                                else:
                                    continue
                                self.leito_vago()
                                break
                            break

    def temporizador(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.atualiza_cti)
        self.timer.start()
        self.timer_email = QtCore.QTimer()
        self.timer_email.setInterval(2000)
        self.indices = []

        self.timer_posicao = QtCore.QTimer()
        self.timer_posicao.setInterval(500)

        # Desconecta antes de conectar para evitar múltiplas conexões
        try:
            self.timer_posicao.timeout.disconnect()
        except Exception:
            pass
        self.timer_posicao.timeout.connect(self.atualizar_posicao)
        #self.timer_email.timeout.connect(self.adicionar_email)
        #self.timer_email.start()
        if self.dept == 'Administrador':
            self.time_user = QtCore.QTimer()
            self.time_user.setInterval(2000)
            #self.time_user.timeout.connect(self.aceitar_user)
            self.time_user.start()
        self.timer_post = QtCore.QTimer()
        self.timer_post.setInterval(300000)
        #self.timer_post.timeout.connect(self.ler_movimentacao_post)
        self.timer_post.start()
        self.timer_mysql = QtCore.QTimer()
        self.timer_mysql.setInterval(300000)
        self.timer_mysql.timeout.connect(self.atualiza_mysql)
        self.timer_mysql.start()
        self.timer_posicao.start()

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
    def name_text(self, text, cdata, row, line_edit):
        try:
            if len(text) < 4:
                return

            primeira_letra = str(text)[0].upper()

            if self.indexa_nome != primeira_letra:
                self.indexa_nome = primeira_letra
                idx = ord(primeira_letra) - ord('A')
                if 0 <= idx < len(self.teladem.lista_nome_nome):
                    todos_nomes = self.teladem.lista_nome_nome[idx]
                else:
                    todos_nomes = []
                completer = QtWidgets.QCompleter(todos_nomes)
                completer.setFilterMode(Qt.MatchFlag.MatchStartsWith)
                completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                line_edit.setCompleter(completer)

            colum_prontuario = 1
            colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', colum_prontuario)

            colum_paciente = 4
            colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE', colum_paciente)

            colum_npf = 2
            colum_npf = self.descobrir_nome_coluna('NPF', colum_npf)

            self.aterar_dados_database(text, 'QLineEdit')
            if text in self.teladem.index_nome:
                indice, i = self.teladem.index_nome[text]
                prontuario = self.teladem.lista_prontuario_nome[indice][i] or 'N/A'
                npf = self.teladem.lista_npf_nome[indice][i] or 'N/A'
                data_nasc = self.teladem.lista_data_nascimento_nome[indice][i]

                item = QtWidgets.QTableWidgetItem(text)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabela_grade.setItem(row, colum_paciente, QTableWidgetItem(item))

                item = QtWidgets.QTableWidgetItem(prontuario)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabela_grade.setItem(row, colum_prontuario, QTableWidgetItem(item))

                item = QtWidgets.QTableWidgetItem(npf)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabela_grade.setItem(row, colum_npf, QTableWidgetItem(item))

                if data_nasc is not None:
                    ano = data_nasc.year
                    mes = data_nasc.month
                    dia = data_nasc.day
                    datanas = f'{dia:02d}/{mes:02d}/{ano}'
                else:
                    ccurrent_datetime = QtCore.QDateTime.currentDateTime()
                    future_datetime = ccurrent_datetime.addDays(30000)
                    datanas = future_datetime.toString("dd/MM/yyyy")

                item = QtWidgets.QTableWidgetItem(datanas)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabela_grade.setItem(row, cdata, QTableWidgetItem(item))

                self.current_pos = (row, colum_prontuario)
                self.aterar_dados_database(prontuario, 'QLineEdit')
                self.current_pos = (row, colum_npf)
                self.aterar_dados_database(npf, 'QLineEdit')
                self.current_pos = (row, cdata)
                self.aterar_dados_database(datanas, 'QDateEdit')
        except Exception as e:
            print(f"Error: {e}")

    def prontu_text(self, text, cdata, row, line_edit):
        try:
            if self.indexa_pronto != int(str(text)[0]):
                if len(text) < 4:
                    return
                self.indexa_pronto = int(str(text)[0])
                index = self.indexa_pronto
                if 0 <= index < len(self.teladem.lista_prontuario):
                    todos_prontuarios = self.teladem.lista_prontuario[index]
                else:
                    todos_prontuarios = []

                completer = QtWidgets.QCompleter(todos_prontuarios)
                completer.setFilterMode(Qt.MatchFlag.MatchStartsWith)
                completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                line_edit.setCompleter(completer)

            colum_paciente = 4
            colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE', colum_paciente)
            colum_prontuario = 1
            colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', colum_prontuario)
            colum_npf = 2
            colum_npf = self.descobrir_nome_coluna('NPF', colum_npf)

            self.aterar_dados_database(text, 'QLineEdit')

            if text in self.teladem.index_prontuario:
                indice, i = self.teladem.index_prontuario[text]
                nome = self.teladem.lista_nome[indice][i] or 'N/A'
                npf = self.teladem.lista_npf[indice][i] or 'N/A'
                data_nasc = self.teladem.lista_data_nascimento[indice][i]

                item = QtWidgets.QTableWidgetItem(text)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabela_grade.setItem(row, colum_prontuario, QTableWidgetItem(item))

                item = QtWidgets.QTableWidgetItem(nome)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabela_grade.setItem(row, colum_paciente, QTableWidgetItem(item))

                item = QtWidgets.QTableWidgetItem(npf)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabela_grade.setItem(row, colum_npf, QTableWidgetItem(item))

                if data_nasc is not None:
                    ano = data_nasc.year
                    mes = data_nasc.month
                    dia = data_nasc.day
                    datanas = f'{dia:02d}/{mes:02d}/{ano}'
                else:
                    ccurrent_datetime = QtCore.QDateTime.currentDateTime()
                    future_datetime = ccurrent_datetime.addDays(30000)
                    datanas = future_datetime.toString("dd/MM/yyyy")

                item = QtWidgets.QTableWidgetItem(datanas)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabela_grade.setItem(row, cdata, QTableWidgetItem(item))

                self.current_pos = (row, colum_paciente)
                self.aterar_dados_database(nome, 'QLineEdit')
                self.current_pos = (row, colum_npf)
                self.aterar_dados_database(npf, 'QLineEdit')
                self.current_pos = (row, cdata)
                self.aterar_dados_database(datanas, 'QDateEdit')

        except Exception as e:
            print(f"Error: {e}")

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
            conexao = pymysql.connect(host=self.host, user=self.usermysql, password=self.password, database='sgl')
            cursor = conexao.cursor()
            for coluna, valor, LEITO in lista:
                comando = f'UPDATE grade SET {coluna} = \"{valor}\" WHERE idGRADE = \"{LEITO}\"'
                cursor.execute(comando)
                conexao.commit()
            conexao.close()
        except pymysql.connector.Error as error:
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
            self.btn_alterar.setText(_translate('Form', 'ALTERAR A GRADE DE LEITOS'))
            self.btn_alta.setText(_translate('Form', 'SOLICITAR ALTA'))
            self.btn_permuta.setText(_translate('Form', 'TROCAR PACIENTE'))
        self.usuario.setText(_translate('Form', 'USUÁRIO'))
        self.procura_pac.setText(_translate('Form', 'PROCURAR PACIENTE'))
        self.MONITORAMENTO.setText(_translate('Form', 'MONITORAMENTO'))
        self.GRADE.setText(_translate('Form', 'GRADE'))
        self.GRAFICOS.setText(_translate('Form', 'GRÁFICOS'))

        self.SAIR.setText(_translate('Form', 'SAIR'))
        self.historio.setText(_translate('Form', 'HISTÓRICO'))

    def retranslateUi_CTI(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'Sistema de Gestão de Leitos'))
        self.increase_column_width(0, 5)
        item = self.tabela_grade.horizontalHeaderItem(0)
        item.setText(_translate('Form', ' '))

        for col in range(1, self.tabela_grade.columnCount()):
            nome = self.lista_nomes_das_colunas[col - 1]
            item = self.tabela_grade.horizontalHeaderItem(col)
            item.setText(_translate('Form', nome))

        for colum in range(1, self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum).text()
            text_width = self.fontMetrics().boundingRect(item_pac).width()
            self.increase_column_width(colum, text_width + 100)

        if self.dept!= 'Telespectador':
            self.btn_alterar.setText(_translate('Form', 'ALTERAR A GRADE DE LEITOS'))
            self.btn_alta.setText(_translate('Form', 'SOLICITAR ALTA'))
            self.btn_permuta.setText(_translate('Form', 'TROCAR PACIENTES DE LEITO'))
            self.deixar_vago.setText(_translate('Form', 'DEIXAR LEITO VAGO'))
            self.btn_ocupar_leito.setText(_translate('Form', 'DEIXAR LEITO OCUPADO'))
        self.usuario.setText(_translate('Form', 'USUÁRIO'))
        self.procura_pac.setText(_translate('Form', 'PROCURAR PACIENTE'))
        self.MONITORAMENTO.setText(_translate('Form', 'MONITORAMENTO'))
        self.GRADE.setText(_translate('Form', 'GRADE'))
        self.GRAFICOS.setText(_translate('Form', 'GRÁFICOS'))

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
            print('abrir_email')
            self.barra = self.tabela_grade.horizontalScrollBar().value()
            self.barra_vertical = self.tabela_grade.verticalScrollBar().value()
            self.email.setVisible(True)
            self.email.setGeometry(self.frame.width() - 500, 0, 400, 600)
            self.scrool.setGeometry(3, 42, 394, self.email.height() - 50)

            self.atualizar_email()
            if self.sidebar.isVisible():
                self.sidebar.close()
                self.label_icone.setStyleSheet('border-radius: 10px;')
        else:  # inserted
            self.email.setVisible(False)
            for frame in self.frames:
                frame.deleteLater()
                self.frames = []

    def user_s_new(self):
        data = []

        leitura = self.data_deman.ler_cadastros(self)
        for linha in leitura:
            if linha[0] == self.user:
                continue
            if len(linha) > 0:
                if linha[2] == '0':
                    data.append((
                        f'O usuário com Nome \'{linha[1]}\' e user \'{linha[0]}\' solicita acesso para logar no software com o perfil \'{linha[3]}\'.',
                        linha[0]
                    ))
                elif linha[2] == '2':
                    data.append((
                        f'O usuário com Nome \'{linha[1]}\' e user \'{linha[0]}\' solicita alteração do perfil \'{linha[3]}\' para o perfil \'{linha[4]}\'.',
                        linha[0]
                    ))
        return data

    def atualizar_email(self):
        for frame in self.frames:
            frame.deleteLater()
        for label in self.msm.findChildren(QtWidgets.QWidget):
            label.deleteLater()
        self.msm.hide()
        self.frames = []
        data = self.user_s_new()
        print(data)
        for texto, id in data:
            frame = QPushButton(texto)
            frame.setContentsMargins(0, 80, 0, 0)
            if not self.settings.value(f'clicados/{texto}', False, type=bool):
                frame.setStyleSheet(
                    "QPushButton { background-color: white;font-weight: bold; border: 2px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; text-align: left; padding-left: 10px;}")
                icon = QIcon(resource_path('imagens/novo-email.ico'))
                frame.setIcon(icon)
            else:
                frame.setStyleSheet(
                    "QPushButton { background-color: white; border: 2px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; text-align: left; padding-left: 10px;}")
            frame.setFixedSize(370, 50)
            frame.clicked.connect(lambda _, user=id, text=texto, btn=frame: self.clicar_botao(text, btn, user))
            self.main_layout.addWidget(frame)
            self.frames.append(frame)

    def clicar_botao(self, texto, botao, user):
        if not self.settings_clicado.value(f'clicados/{texto}', False, type=bool):
            self.settings_clicado.setValue(f'clicados/{texto}', True)
            botao.setStyleSheet(
                "QPushButton { background-color: white; border: 2px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; text-align: left; padding-left: 10px;}")

        self.abrir_notificao(texto, user)

    def abrir_notificao(self, text, user):
        sender = self.sender()
        pos = sender.geometry().topLeft()
        self.indices = []

        self.atualizar_email()

        btnfechar = QtWidgets.QPushButton(" X ", self.msm)
        btnfechar.setToolTip('Fechar')
        btnfechar.setGeometry(200, 5, 40, 20)
        btnfechar.setStyleSheet("""
                                           QPushButton {
                                               border: 2px solid #2E3D48;
                                               border-radius: 10px;
                                               background-color: balck;
                                               color: #FFFFFF;
                                           }
                                           QPushButton:pressed {
                                               background-color: #FFFFFF;
                                               color: black;
                                           }
                                       """)
        tooltip_text = f'Fechar'''
        btnfechar.setToolTip(tooltip_text)
        btnfechar.clicked.connect(self.fechar_correio)

        for frame in self.frames:
            frame.setFixedSize(80, 50)

        self.label_msm = QtWidgets.QLabel(self.msm)
        self.label_msm.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_msm.setGeometry(10, 30, 230, 200)
        self.label_msm.setWordWrap(True)
        self.label_msm.setText(text)
        #
        # text = f"Clique <span style='color: blue;'>aqui</span> para aceitar a solicitação."
        # label_link = QtWidgets.QLabel(text,self.msm)
        # label_link.mousePressEvent = self.aceitar_user_
        # label_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # label_link.setStyleSheet(
        #     "font-size: 12px; margin: 0; padding: 0;border: none;")
        # label_link.setGeometry(3, 300, 230, 30)
        # label_link.setWordWrap(True)

        btnAceitar = QtWidgets.QPushButton("Aceitar a Solicitação", self.msm)
        btnAceitar.setToolTip('Aceitar')
        btnAceitar.setGeometry(3, 300, 110, 20)
        btnAceitar.setStyleSheet("""
                                                       QPushButton {
                                                           border: 2px solid #2E3D48;
                                                           border-radius: 10px;
                                                           background-color: balck;
                                                           color: #FFFFFF;
                                                       }
                                                       QPushButton:pressed {
                                                           background-color: #FFFFFF;
                                                           color: black;
                                                       }
                                                   """)
        tooltip_text = f'Aceitar'''
        btnAceitar.setToolTip(tooltip_text)
        btnAceitar.clicked.connect(lambda: self.aceitar_user_(user))

        btncancelar = QtWidgets.QPushButton("Negar a Solicitação", self.msm)
        btncancelar.setToolTip('Negar')
        btncancelar.setGeometry(120, 300, 110, 20)
        btncancelar.setStyleSheet("""
                                                                   QPushButton {
                                                                       border: 2px solid #2E3D48;
                                                                       border-radius: 10px;
                                                                       background-color: balck;
                                                                       color: #FFFFFF;
                                                                   }
                                                                   QPushButton:pressed {
                                                                       background-color: #FFFFFF;
                                                                       color: black;
                                                                   }
                                                               """)
        tooltip_text = f'Negar'''
        btncancelar.setToolTip(tooltip_text)
        btncancelar.clicked.connect(lambda: self.cancelar(user))

        self.msm.setGeometry(100, 3, 250, 400)
        self.msm.show()
        self.label_msm.show()

    def fechar_correio(self):
        self.msm.close()
        for frame in self.frames:
            frame.setFixedSize(370, 50)

    def aceitar_user_(self, user):
        leitura = self.data_deman.ler_cadastros(self)
        for linha in leitura:
            if len(linha) > 0 and linha[0] == user and linha[2] != '1':
                if linha[2] == '0':
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Information)
                    msg_box.setWindowTitle('AVISO')
                    msg_box.setText(
                        f'O usuário com Nome \'{linha[1]}\' e user \'{linha[0]}\' solicita acesso para logar no software com o perfil \'{linha[3]}\'. Aceitar?')
                    icon = QIcon(resource_path('imagens/warning.ico'))
                    msg_box.setWindowIcon(icon)
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    reply = msg_box.exec()
                    if reply == QMessageBox.StandardButton.Yes:
                        self.data_deman.update_cadastro('1', linha[0], linha[3], '')
                        self._mostrar_mensagem('Conta Cadastrada com Sucesso!')
                        break

                elif linha[2] == '2':
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Information)
                    msg_box.setWindowTitle('AVISO')
                    msg_box.setText(
                        f'O usuário com Nome \'{linha[1]}\' e user \'{linha[0]}\' solicita acesso para logar no software com o perfil \'{linha[4]}\'. Aceitar?')
                    icon = QIcon(resource_path('imagens/warning.ico'))
                    msg_box.setWindowIcon(icon)
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    reply = msg_box.exec()
                    if reply == QMessageBox.StandardButton.Yes:
                        self.data_deman.update_cadastro('1', linha[0], linha[4], '')
                        self._mostrar_mensagem('Alteração Realizada com Sucesso!')
                        break

                self.abrir_email()

    def cancelar(self, user):

        leitura = self.data_deman.ler_cadastros(self)
        for linha in leitura:
            if len(linha) > 0 and linha[0] == user:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText(
                    f'Excluir Solicitação do usuário com Nome \'{linha[1]}\' e user \'{linha[0]}\' ?')
                icon = QIcon(resource_path('imagens/warning.ico'))
                msg_box.setWindowIcon(icon)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                reply = msg_box.exec()

                if reply == QMessageBox.StandardButton.Yes:
                    self.data_deman.exluir_conta(user)
                self._mostrar_mensagem('Solicitação Excluída com Sucesso!')
                break

                self.abrir_email()

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


    def apagar_linha(self, row):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Apagar Reserva?')
        icon = QIcon(resource_path('imagens/warning.ico'))
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            conexao = pymysql.connect(host=self.host, user=self.usermysql, password=self.password, database='sgl')
            leito = self.tabela_grade.verticalHeaderItem(row)
            cursor = conexao.cursor()
            leito = leito.text().replace(' ', '_')
            comando = f'DELETE FROM grade WHERE idGRADE = \"{leito}\"'
            cursor.execute(comando)
            conexao.commit()
            cursor.close()
            conexao.close()
            #self.abri_cti(self.form, self.nome_tabela_post)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('Solicitação apagada.')
            icon = QIcon(resource_path('imagens/warning.ico'))
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply = msg_box.exec()
            self.tabela_grade.removeRow(row)
            self.atualiza_cti()

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
        if self.config_Aberta == True:
            self.janela_config.close()
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
            self.config_Aberta = False
        else:
            from config import Ui_Form
            self.config = Ui_Form()
            self.config.setupUi(Form, self)
            self.config_Aberta = True
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()


        self.remover_widget()

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
            backcolocor = '#C0C0C0'
            color = 'Black'
            tamanho = 12
            font_name = 'Segoe UI'
        self.backcolocor = backcolocor
        self.color = color
        self.font = font_name
        self.tamanho = tamanho
        for label in self.frame.findChildren(QtWidgets.QLabel):
            if label != self.SGL_label and label != self.ebserh_label and label!=self.TITULO_CTI:
                label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name}; border:none')
        self.frame.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;')
        self.frame_senso.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;')
        self.frame_relatorio.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;')
        self.frame_permuta.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;border: 2px solid #2E3D48;border-radius: 10px;')
        self.sidebar.setStyleSheet(f'border: 2px solid #2E3D48;background-color: {backcolocor}; border-radius: 10px;color: {color};font: {font_name} {tamanho}px;')
        for label in self.sidebar.findChildren(QtWidgets.QLabel):
            if label != self.SGL_label and label != self.ebserh_label and label!=self.TITULO_CTI:
                label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name}; border:none')
        self.qt_notificao.setStyleSheet('background-color: red; color: #FFFFFF; border: 2px solid white; border-radius: 10px;')
        self.TITULO_CTI.setStyleSheet(f'color: {color}; font:  30 px {font_name};font-weight: bold; border:none;')

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
        if self.permuta_Aberta  == True:
            self.frame_permuta.close()
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
            self.permuta_Aberta = False

        self.remover_widget()
    def tabela_clicada(self, row, column):
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
        if self.permuta_Aberta == True:
            self.frame_permuta.close()
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
            self.permuta_Aberta = False
        for btn in self.frame.findChildren(QtWidgets.QPushButton):
            btn.setEnabled(True)
        if column != 0:
            self.remover_widget()
            self.colocar_widget(row, column)
        rowcont = row
        item = self.tabela_grade.item(row, column)
        contador = 0
        self.lista_permuta = []
        if item.column() == 0 and item.flags() & QtCore.Qt.ItemFlag.ItemIsUserCheckable:
            for row in range(self.tabela_grade.rowCount()):
                selecao = self.tabela_grade.item(row, 0)
                if selecao:
                    if selecao.checkState() == QtCore.Qt.CheckState.Checked:
                        contador += 1
                        id_valor = self.tabela_grade.verticalHeaderItem(row).text()
                        self.lista_permuta.append(id_valor)
                        if not any(id_valor == valor[1] for valor in self.lista_permuta_tabela_diferente):
                            id_valor = self.tabela_grade.verticalHeaderItem(row).text()
                            self.lista_permuta_tabela_diferente.append((self.codigo_ala,id_valor))
                    if selecao.checkState() != QtCore.Qt.CheckState.Checked:
                        id_valor = self.tabela_grade.verticalHeaderItem(row).text()
                        for tupla in self.lista_permuta_tabela_diferente:
                            if id_valor == tupla[1]:
                                self.lista_permuta_tabela_diferente.remove(tupla)
                                break

            self.ativar_btn_permutas()

            #print(self.lista_permuta_tabela_diferente, 'analisa')
            if contador == 0:
                self.deixar_vago.hide()
                self.btn_alta.hide()
                self.btn_permuta.hide()
            if contador > 0:
                self.deixar_vago.show()
                coluna = self.descobrir_nome_coluna('STATUS DO LEITO', None)
                print(self.tabela_grade.item(rowcont, coluna).text())
                if self.tabela_grade.item(rowcont, coluna) is not  None and self.tabela_grade.item(rowcont, coluna).text() != 'OCUPADO':
                    self.btn_ocupar_leito.show()
                #self.chamar_btn_alta()
            if contador == 2:
                self.btn_permuta.show()
            else:
                self.btn_permuta.hide()

      #  print(self.lista_permuta)
    def chamar_btn_alta(self):
        if self.codigo_cti:
            self.btn_alta.show()
        else:
            self.btn_alta.hide()
    def ativar_btn_permutas(self):
        print('permutar1')
        lista = self.lista_permuta_tabela_diferente

        # Passo 1: verificar quantas alas diferentes existem
        alas = [tupla[0] for tupla in lista]
        alas_unicas = list(dict.fromkeys(alas))  # remove duplicatas preservando a ordem

        if len(alas_unicas) > 2:
            primeira_ala = alas_unicas[0]
            # Remove todos os itens da primeira ala
            lista = [tupla for tupla in lista if tupla[0] != primeira_ala]

        # Atualiza a lista após possível remoção
        self.lista_permuta_tabela_diferente = lista

        # Verifica se agora temos exatamente 2 alas
        alas_restantes = [tupla[0] for tupla in lista]
        alas_unicas_restantes = list(set(alas_restantes))

        if len(alas_unicas_restantes) == 2:
            # Conta quantos leitos tem em cada ala
            contagem = {}
            for ala in alas_unicas_restantes:
                contagem[ala] = sum(1 for tupla in lista if tupla[0] == ala)

            # Verifica se ambas têm a mesma quantidade
            valores = list(contagem.values())
            dado2 = 0
            dado1 = 0
            if valores[0] == valores[1]:
                area1, area2 = alas_unicas_restantes
                for idx, id, in enumerate(self.lista_ids):
                    print('olha iso',id, area1)
                    if int(id) == int(area1):
                        print('dentro pai')
                        dado1 = self.lista_btn[idx]
                    elif int(id) == int(area2):
                        print('dentro pai')
                        dado2 = self.lista_btn[idx]
                self.btn_permuta_diferentes_tabelas.setText(
                    f'TROCAR PACIENTES ENTRE {dado1} E {dado2}'
                )
                self.btn_permuta_diferentes_tabelas.show()
                return
        # Se não atender aos critérios
        self.btn_permuta_diferentes_tabelas.hide()
        self.btn_permuta_diferentes_tabelas.adjustSize()

    def remover_widget(self):
        # Se há uma posição atual definida
        if self.current_pos and self.current_editor:
            old_row, old_col = self.current_pos
            # Remove o widget da célula atual
            self.tabela_grade.removeCellWidget(old_row, old_col)
            self.current_editor = None
        # Verifica e remove widgets de outras células que não sejam os esperados
        for row in range(self.tabela_grade.rowCount()):
            for col in range(self.tabela_grade.columnCount()):
                widget = self.tabela_grade.cellWidget(row, col)
                if widget:
                    # Verifica se o widget pertence à lista de widgets válidos
                    is_valid = any(widget == line_edit for _, _, line_edit in self.lista_tooltip_label)
                    if not is_valid:
                        self.tabela_grade.removeCellWidget(row, col)
        self.data_grade.definir_posicao_usuario('_grade'+str(self.codigo_ala), self, (None, None), 'GRADE')

    def atualizar_posicao(self):
        tamanho_frame = self.frame.width()
        tamanho_frame_h = self.frame.height()

        self.frame.setMaximumWidth(tamanho_frame)
        self.frame.setMaximumHeight(tamanho_frame_h)

        if self.current_editor:
            self.data_grade.definir_posicao_usuario('_grade'+str(self.codigo_ala), self, self.current_pos, 'GRADE')
        self.identificar_usuarios()

    def identificar_usuarios(self):
        try:
            leitura = self.data_grade.ler_posicoes_usuarios(self, 'GRADE', '_grade'+str(self.codigo_ala))

            # Dicionário para mapear usuário -> (row, col, tooltip, line_edit)
            mapa_usuarios = {usue: (tooltip, line_edit) for usue, tooltip, line_edit in self.lista_tooltip_label}

            nova_lista_tooltip_label = []

            self.lista_user_pos = []
            if leitura:
                for valor2 in leitura:
                    usuario = valor2[0]
                    posicao_str = valor2[1]
                    nome_usuario = valor2[2]

                    if posicao_str and posicao_str != 'None' and ',' in posicao_str and usuario != self.user:
                        try:
                            row_str, col_str = posicao_str.split(',')
                            if row_str.strip().isdigit() and col_str.strip().isdigit():
                                row, col = int(row_str), int(col_str)

                            else:
                                continue
                        except Exception as e:
                            print(f"Erro ao processar posição {posicao_str}: {e}")
                            continue

                        # Verifica se o usuário já tinha um tooltip e line_edit
                        antigo = mapa_usuarios.get(usuario)
                        precisa_atualizar = True
                        if antigo:
                            antigo_tooltip, antigo_lineedit = antigo
                            index = self.tabela_grade.indexAt(antigo_lineedit.pos())
                            if index.row() == row and index.column() == col:
                                precisa_atualizar = False
                                nova_lista_tooltip_label.append((usuario, antigo_tooltip, antigo_lineedit))
                            else:

                                # Posição mudou -> remove os antigos
                                if antigo_tooltip:
                                    antigo_tooltip.deleteLater()
                                if antigo_lineedit:
                                    antigo_lineedit.deleteLater()
                                if (index.row(), index.column()) in self.lista_user_pos:
                                    self.lista_user_pos.remove((index.row(), index.column()))

                        if precisa_atualizar:
                            item = self.tabela_grade.item(row, col)
                            text = item.text() if item else ""
                            line_edit = ClickableLabel(text)

                            self.lista_user_pos.append((row, col))

                            bg_color = item.background().color().name() if item else 'white'
                            if bg_color == '#000000':
                                bg_color = 'white'
                            line_edit.setStyleSheet(f'background-color: {bg_color}; border: 2px solid purple;')
                            line_edit.setFocus()

                            tooltip_label = QLabel(self.tabela_grade)
                            tooltip_label.setText(f"{nome_usuario} Editando a célula")
                            tooltip_label.setStyleSheet(
                                "background-color: purple; border: 1px solid white; padding: 3px; "
                                "border-radius: 10px; color: white;"
                            )
                            tooltip_label.adjustSize()

                            delegate = AlignedLineEditWithBorderDelegate(
                                target_cells=[(row, col)],
                                border_color=QColor('purple'),
                                main_window=self
                            )
                            self.tabela_grade.setItemDelegate(delegate)
                            # Update cells and force repaint
                            delegate.update_target_cells([(row, col)])
                            self.tabela_grade.viewport().update()
                            index = self.tabela_grade.model().index(row, col)
                            rect = self.tabela_grade.visualRect(index)

                            if not rect.isValid():
                                tooltip_label.hide()
                                continue

                            pos_viewport = rect.topRight() + QPoint(10, 0)
                            pos_viewport.setX(pos_viewport.x() - 15)
                            pos_viewport.setY(pos_viewport.y() - 5)

                            tooltip_label.setParent(self.tabela_grade.viewport())
                            tooltip_label.move(pos_viewport)
                            tooltip_label.show()

                            nova_lista_tooltip_label.append((usuario, tooltip_label, line_edit))
                            if self.current_editor is not None:
                                self.current_editor.raise_()
                                self.current_editor.setFocus()

            # Remove tooltips de usuários que não estão mais na leitura
            usuarios_novos = set([u[0] for u in nova_lista_tooltip_label])
            usuarios_antigos = set(mapa_usuarios.keys())

            usuarios_removidos = usuarios_antigos - usuarios_novos
            for usuario in usuarios_removidos:
                tooltip, lineedit = mapa_usuarios[usuario]
                if tooltip:
                    tooltip.deleteLater()
                if lineedit:
                    lineedit.deleteLater()

            self.lista_tooltip_label = nova_lista_tooltip_label

        except Exception as e:
            print(f"Error: {e}")

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
            if self.permuta_Aberta  == True:
                self.frame_permuta.close()
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                self.permuta_Aberta = False

            self.remover_widget()
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
            if self.permuta_Aberta  == True:
                self.frame_permuta.close()
                self.timer.start()
                self.timer_post.start()
                self.timer_mysql.start()
                self.permuta_Aberta = False
            self.remover_widget()

    def abrir_senso(self, Form):
        if self.frame_do_grafico.isVisible():
            self.frame_do_grafico.hide()
        if self.frame_do_monitoramento.isVisible():
            self.frame_do_monitoramento.hide()
        if self.senso_Aberta == False:
            #self.senso.move(3, 0)
            self.senso.setText('VOLTAR')
            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                if btn!= self.senso:
                    if self.dept!= 'Telespectador':
                        btn.hide()
                    else:
                        if btn!= self.btn_alta and btn!= self.btn_permuta and btn!= self.btn_alterar and (btn!= self.btn_realocar) and (btn!= self.btn_relatorio) and (btn!= self.senso):
                            btn.hide()
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
        else:
            self.frame_senso.hide()
            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                if self.dept!= 'Telespectador':
                    btn.show()
                else:  # inserted
                    if btn!= self.btn_alta and btn!= self.btn_alterar and btn!= self.btn_permuta and (btn!= self.btn_realocar) and (btn!= self.btn_relatorio) and (btn!= self.senso):
                        btn.show()
            self.senso.setText('SENSO')
            self.tabela_grade.show()
            self.BARRADEPESQUISA.show()
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

    def dados_senso(self, ala):
        mapa_aghu = {
            'PS|UTI - AGHU': 169,
            '2º SUL - GRADE': 21,
            '2º LESTE - GRADE': 22,
            '3º NORTE/UCO - GRADE': 23,
            '3º LESTE/CTI - GRADE': 24,
            '6º NORTE/CTI PEDIATRICO - GRADE': 29,
            '6º LESTE - GRADE': 30,
            '7º NORTE - GRADE': 31,
            '7º LESTE - GRADE': 32,
            '8º SUL - GRADE': 33,
            '8º LESTE - GRADE': 34,
            '8º NORTE - GRADE': 193,
            '9º LESTE - GRADE': 35,
            '10º NORTE - GRADE': 36,
            'PS|UDC - AGHU': 171,
            'PS|CORREDOR - AGHU': 173,
            'PS|PEDIATRIA - AGHU': 170,
            'HOSPITAL SÃO GERALDO - AGHU': 47,
            'OBSTÉTRICO': 93,
            'PEDIATRICO': [141, 170, 29],
            'CLÍNICO ADULTO': 194,  # se necessário
            'CIRÚRGICO ADULTO': 195,  # se necessário
            'CTI - ADULTO': 24,
            'CTI - PEDIATRICO': 29
        }

        # Caso a ala esteja no dicionário, usa pegar_senso_aghu
        codigo_ala = mapa_aghu.get(ala)
        if codigo_ala is not None:
            if isinstance(codigo_ala, list):
                for cod in codigo_ala:
                    self.pegar_senso_aghu(cod)
            else:
                self.pegar_senso_aghu(codigo_ala)
            return  # já preencheu os dados, não precisa continuar

        # Se não está no mapa_aghu, assume que está na tabela_grade (GRADE)
        colum_status = 0
        for colum in range(self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(colum)
            if item_pac.text() == 'STATUS DO LEITO':
                colum_status = colum
                break

        for row in range(self.conta_linha()):
            self.total += 1
            selecao = self.item(row, colum_status)
            if selecao is None:
                continue
            texto = selecao.text().strip().upper()
            if texto == 'OCUPADO':
                self.ocupado_senso += 1
            elif texto in {
                'BLOQUEADO',
                'BLOQUEADO POR FALTA DE FUNCIONÁRIOS',
                'PONTUAL - BLOQUEADO POR FALTA DE FUNCIONÁRIOS',
                'BLOQUEADO POR MANUTENÇÃO',
                'BLOQUEADO POR VM/VNI',
                'BLOQUEADO POR OUTROS MOTIVOS'
            }:
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
            cursor.execute(f'SELECT unf_seq, int_seq, ind_situacao FROM agh.ain_leitos WHERE unf_seq = {codigo_ala}')
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
    def voltar_normal(self):
        self.frame_relatorio.hide()
        self.frame_do_grafico.hide()
        self.frame_do_monitoramento.hide()
    def abri_relatorio(self, Form):
        if self.frame_do_grafico.isVisible():
            self.frame_do_grafico.hide()
        if self.frame_do_monitoramento.isVisible():
            self.frame_do_monitoramento.hide()
        if not self.frame_relatorio.isVisible():
            # self.timer_post.stop()
            # self.timer_mysql.stop()
            # self.timer.stop()
            # for btn in self.frame.findChildren(QtWidgets.QPushButton):
            #     if btn!= self.btn_relatorio:
            #         btn.hide()
            # # self.tabela_grade.hide()
            # # self.BARRADEPESQUISA.hide()
            # # self.label_icone.hide()
            # # self.notificao_label.hide()
            # # self.TITULO_CTI.hide()
            from relatorio import Ui_Form
            self.relatorio = Ui_Form()
            self.frame_relatorio.show()
            self.relatorio.setupUi(Form, self.frame_relatorio, self)
            # self.timer.stop()
            # self.timer_post.stop()
            # self.timer_mysql.stop()
        else:  # inserted
            self.timer_post.start()
            self.timer_mysql.start()
            self.timer.start()
            self.timer_post.start()
            self.timer_mysql.start()
            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                if self.dept!= 'Telespectador':
                    btn.show()
                else:  # inserted
                    if btn!= self.btn_alta and btn!= self.btn_alterar and btn!= self.btn_permuta and (btn!= self.btn_realocar) and (btn!= self.btn_relatorio) and (btn!= self.senso):
                        btn.show()
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
        tamanho_frame = self.frame.width()
        tamanho_frame_h = self.frame.height()

        self.frame.setMaximumWidth(tamanho_frame)
        self.frame.setMaximumHeight(tamanho_frame_h)

        self.scroll_painel.setGeometry(QtCore.QRect(0, 25, tamanho_frame - 10, tamanho_frame_h-10))

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
            self.painel_voltar.setText('VOLTAR')
            self.painel_voltar.setToolTip('VOLTAR')
            self.painel_voltar.move(0, 0)
            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                if btn!= self.painel_voltar:
                    btn.hide()
            self.tabela_grade.hide()
            self.BARRADEPESQUISA.hide()
            self.label_icone.hide()
            self.notificao_label.hide()
            self.TITULO_CTI.hide()
            self.scroll_painel.show()
            self.timer.stop()
            self.timer_post.stop()
            self.timer_mysql.stop()
            self.painel_voltar.show()
        else:  # inserted
            self.painel_voltar.hide()
            for widget in self.list_painel:
                widget.deleteLater()
            self.frame_terapia_intensiva.deleteLater()
            self.frame_unidades_internacao_1.deleteLater()
            self.scroll_painel.hide()
            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                if self.dept!= 'Telespectador':
                    btn.show()
                else:  # inserted
                    if btn!= self.btn_alta and btn!= self.btn_permuta and btn!= self.btn_alterar and (btn!= self.btn_realocar) and (btn!= self.btn_relatorio) and (btn!= self.senso):
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
    def atualizar_painel(self):
        self.help_sccrol_painel = True
        self.qt_int_adulto = 1
        self.qt_int_ped = 1
        self.qt_int_adulto_total = 1
        self.qt_int_neo = 1
        self.qt_int_ped_total = 1
        self.qt_int_adulto2 = 1
        self.qt_int_adulto_total2 = 1
        self.qt_int_ped2 = 1
        self.qt_int_ped_total2 = 1
        self.total_bloq = 1
        self.total_vago = 1
        self.total_rese = 1
        self.total_ocup = 1
        self.qt_bl_manu = 1
        self.qt_bl_VM_VNI = 1
        self.qt_se_fun = 1
        self.qt_pront = 1
        self.qt_vagos_2leste = 1
        self.qt_vagos_2sul = 1
        self.qt_vagos_7norte = 1
        self.qt_vagos_10norte = 1
        self.qt_vagos_8leste = 1
        self.qt_vagos_6leste = 1
        self.qt_vagos_8norte = 1
        self.qt_vagos_uco = 1
        self.qt_vagos_uti_ps = 1
        self.qt_vagos_9leste = 1
        self.qt_vagos_7leste = 1
        self.qt_vagos_8sul = 1
        self.qt_vagos_3leste = 1
        self.qt_vagos_cti_ped = 1
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
        print('AQUI2')
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
        print('AQUI1')
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
        print('AQUI3')
        self.monitora_8_sul(Form, frame_8_sul)
        frame_10_sul = QFrame(frame_2_leste)
        frame_10_sul.setFrameShape(QFrame.Shape.Box)
        frame_10_sul.setContentsMargins(0, 80, 0, 0)
        frame_10_sul.setStyleSheet('QFrame { background-color: white; border: 1px solid black; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
        frame_10_sul.setGeometry(0, 845, 1091, 435)
        self.list_painel.append(frame_10_sul)
        print('AQUI4')
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
        #self.abri_cti(self.form, 'CTI PEDIÁTRICO - 06N')
        # if self.dept!= 'Telespectador':
        #     self.btn_alterar.show()
        #     self.btn_alta.show()
        #     self.btn_realocar.show()
        #     self.btn_permuta.show()
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
            #self.abri_cti(Form, funcao)
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
            #self.abri_cti(Form, funcao)
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
        # if self.codigo_ala == 29:
        #     #self.abri_cti(Form, 'CTI PEDIÁTRICO - 06N')
        # if self.codigo_ala == 23:
        #     #self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO CORONARIANA - 03N')
        # if self.codigo_ala == 30:
        #     #self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 06L')
        # if self.codigo_ala == 36:
        #     #self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 10N')
        # if self.codigo_ala == 169:
        #     #self.abri_cti(Form, 'UTI - PRONTO SOCORRO')
        # if self.codigo_ala == 22:
        #     #self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 02L')
        # if self.codigo_ala == 21:
        #     #self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 02S')
        # if self.codigo_ala == 32:
        #     #self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 07L')
        # if self.codigo_ala == 31:
        #     #self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 07N')
        # if self.codigo_ala == 33:
        #     #self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08S')
        # if self.codigo_ala == 34:
        #     #self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08L')
        # if self.codigo_ala == 193:
        #     #self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 08N')
        # if self.codigo_ala == 35:
        #     #self.abri_cti(Form, 'UNIDADE DE INTERNAÇÃO - 09L')
        # if self.codigo_ala == 24:
        #     #self.abri_cti(Form, 'CTI ADULTO - 03L')
        return valor

    def novas_unidades(self):
        list = ['tabela_2_sul', 'tabela_6_leste', 'tabela_10°_norte', 'tabela_cti_ps', 'tabela_2_leste', 'tabela_cti_ped', 'tabela_7_leste', 'tabela_8_sul', 'tabela_7_norte', 'tabela_8_leste', 'tabela_8_norte', 'tabela_uco', 'tabela_9_leste', 'tabela_3_leste']
        try:
            connection = pymysql.connect(host='localhost', user='root', password='camileejose', database='grade')
            cursor = connection.cursor()
            cursor.execute('SHOW TABLES')
            tables = cursor.fetchall()
            for i, table in enumerate(tables):
                if table[0] not in list:
                    button = QtWidgets.QPushButton(f'{table[0].upper()}')
                    button.setFixedSize(71, 21)
                    self.bottom_bar_layout.addWidget(button)
                    button.clicked.connect(lambda checked, text=table[0]: self.abrir_nova_unidade(text))
                    button.setStyleSheet('\n                                    QPushButton {\n                                        border: 2px solid #2E3D48;\n                                        border-radius: 10px;\n                                        background-color: #FFFFFF;\n                                        color: #2E3D48;\n                                    }\n\n                                    QPushButton:hover {\n                                        background-color: #DDDDDD;  /* Change this to your desired hover color */\n                                        color: rgb(0, 0, 0);\n                                    }\n\n                                    QPushButton:pressed {\n                                        background-color: #2E3D48;  /* Change this to your desired pressed color */\n                                        color: #FFFFFF;\n                                    }\n                                ')
            connection.close()
        except pymysql.connector.Error as error:
            print('Erro ao conectar ao MySQL:', error)

    def abrir_nova_unidade(self, tabela):
        conexao = pymysql.connect(host='localhost', user='root', password='camileejose', database='grade')
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
                    self.atualiza_cti()
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

    def trocar_paciente(self,tabela_grade):
        analise = 0
        for row in range(self.tabela_grade.rowCount()):
            selecao = self.tabela_grade.item(row, 0)
            item = self.tabela_grade.verticalHeaderItem(row)
            if 'aguardando' not in item.text():
                if selecao.checkState() == QtCore.Qt.CheckState.Checked:
                    self.timer.stop()
                    self.timer_post.stop()
                    self.timer_mysql.stop()
                    analise += 1
        # if analise >1:
        #     msg_box = QMessageBox()
        #     msg_box.setIcon(QMessageBox.Icon.Information)
        #     msg_box.setWindowTitle('AVISO')
        #     msg_box.setText('SOMENTE É PERMITIDO UMA TROCA POR VEZ. SELECIONE APENAS UM PACIENTE.')
        #     msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        #     reply = msg_box.exec()
        #     icon = QIcon(resource_path('imagens/warning.ico'))
        #     msg_box.setWindowIcon(icon)
        if analise == 0:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('É OBRIGATÓRIO A SELEÇÃO DE AO MENOS UM LEITO.')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply = msg_box.exec()
            icon = QIcon(resource_path('imagens/warning.ico'))
            msg_box.setWindowIcon(icon)
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('PROSSEGUIR')
            icon = QIcon(resource_path('imagens/warning.ico'))
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            reply = msg_box.exec()
            if reply == QMessageBox.StandardButton.Yes:
                self.definir_unidade_permuta(tabela_grade)

    def definir_unidade_permuta(self,tabela_grade):
        self.permuta_Aberta = True
        self.copiadora()
        self.frame_permuta.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_permuta.setGeometry(QtCore.QRect(270, 50, 790, 538))
        self.frame_permuta.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_permuta.setObjectName('frame_permuta')
        self.frame_permuta.show()

        self.frame_permuta.mousePressEvent = lambda event, frame=self.frame_permuta: self.PressEvent_2(event, frame)
        self.frame_permuta.mouseReleaseEvent = lambda event, frame=self.frame_permuta: self.ReleaseEvent_2(event, frame)
        self.frame_permuta.mouseMoveEvent = lambda event, frame=self.frame_permuta: self.MoveEvent_2(event, frame)

        self.table_copy = self.copy_table(self.tabela_alt)
        self.table_copy.setStyleSheet('background-color: rgb(255, 255, 255);border: none;gridline-color: black;')
        self.table_copy.show()
        self.table_copy.setGeometry(QtCore.QRect(10, 110, 751, 351))

        self._criar_btn_permutas(self.tabela_alt)

        self.btn_2leste_3.setText('2º LESTE')
        self.btn_6leste_3.setText('6º LESTE')
        self.btn_UCO_3.setText('UCO')
        self.btn_CTI_3leste_3.setText('CTI 3º LESTE')
        self.btn_2sul_3.setText( '2º SUL')
        self.btn_8sul_3.setText('8º SUL')
        self.btn_8norte_3.setText('8º NORTE')
        self.btn_CTI_PS_3.setText('CTI PS')
        self.btn_10norte_3.setText( '10º NORTE')
        self.btn_8leste_3.setText('8º LESTE')
        self.btn_7norte_3.setText('7º NORTE')
        self.btn_9leste_3.setText('9º LESTE')
        self.btn_cti_ped_3.setText('CTI PED')
        self.btn_7leste_3.setText('7º LESTE')
        self.btn_reserva.setText('TROCAR')

        for btn in self.frame_permuta.findChildren(QtWidgets.QPushButton):
            btn.show()

        self.atualizar_permuta()
        self.checkboxes = []
        for row in range(self.table_copy.rowCount()):
            checkbox = QtWidgets.QCheckBox()
            checkbox.stateChanged.connect(lambda state, r=row: self.checkboxStateChanged(state, r))
            self.checkboxes.append(checkbox)

            # Adicionando checkbox à célula da tabela
            cell_widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(cell_widget)
            layout.addWidget(checkbox)
            layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Centralizar checkbox
            layout.setContentsMargins(0, 0, 0, 0)  # Remover margens
            cell_widget.setLayout(layout)
            self.table_copy.setCellWidget(row, 0, cell_widget)

        self.selecionado_pemuta = -1

    def copy_table(self, table):
        num_rows = table.rowCount()
        num_cols = table.columnCount()

        new_table = QtWidgets.QTableWidget(parent=self.frame_permuta)
        new_table.setGeometry(QtCore.QRect(10, 110, 751, 351))
        new_table.setMinimumSize(QtCore.QSize(681, 0))
        new_table.setStyleSheet('background-color: rgb(255, 255, 255);gridline-color: black;')
        new_table.setObjectName('tabela_grade')
        new_table.setColumnCount(num_cols)
        new_table.setRowCount(num_rows)

        new_table.setHorizontalHeaderLabels(table.horizontalHeaderItem(i).text() for i in range(num_cols))

        for row in range(num_rows):
            for col in range(num_cols):
                item = table.item(row, col)
                if item:
                    new_item = QTableWidgetItem(item.text())
                    new_table.setItem(row, col, new_item)

        return new_table

    def atualizar_permuta(self):
        lista_leitos = []
        connection = psycopg2.connect(user='ugen_integra', password='aghuintegracao', host='10.36.2.35', port='6544',
                                      database='dbaghu')
        cursor = connection.cursor()
        cursor.execute(f'SELECT lto_id, leito FROM AGH.ain_leitos WHERE unf_seq = {self.codigo_ala}')
        rows = cursor.fetchall()
        self.codigo_permuta = self.codigo_ala
        for row in rows:
            sem_hifen = row[0].split('-')[0]
            semzero = row[1].lstrip('0')
            dados = f'{sem_hifen}_{semzero}'
            lista_leitos.append(dados)
            dados = dados + '_aguardando'
            lista_leitos.append(dados)

        conexao = pymysql.connect(host=self.host, user=self.usermysql, password=self.password, database='sgl')
        cursor = conexao.cursor()
        leitos_str = ', '.join([f'\"{leito}\"' for leito in lista_leitos])
        comando = f'SELECT * FROM grade WHERE idGRADE IN ({leitos_str})'
        cursor.execute(comando)
        leitura = cursor.fetchall()
        self.table_copy.clearContents()
        self.table_copy.setRowCount(0)
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
                    row = self.table_copy.rowCount()
                    self.table_copy.insertRow(row)
                    item = item.text().replace('_', ' ')
                    item = QtWidgets.QTableWidgetItem(item)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.table_copy.setVerticalHeaderItem(row, item)
                    _translate = QtCore.QCoreApplication.translate
                    self.increase_column_width(0, 16)
                    item_pac = self.table_copy.verticalHeaderItem(row)
                    item_pac.setText(_translate('MainWindow', item.text()))
                if column != 0:
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    if item is None or item.text() == 'None':
                        item = QtWidgets.QTableWidgetItem(str(''))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.table_copy.setItem(row, column, item)

    def PressEvent_2(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            # centralwidget.setCursor(Qt.CursorShape.ClosedHandCursor)  # Removido
            centralwidget.mouse_offset = event.pos()

    def ReleaseEvent_2(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            # centralwidget.setCursor(Qt.CursorShape.OpenHandCursor)  # Removido
            centralwidget.setCursor(Qt.CursorShape.ArrowCursor)  # Garante que volta para a seta

    def MoveEvent_2(self, event, centralwidget):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = centralwidget.mapToParent(event.pos() - centralwidget.mouse_offset)
            centralwidget.move(new_pos)
    def trocar_unidade_permuta(self,codigo_ala):
        self.codigo_permuta = codigo_ala
        lista_leitos = []
        connection = psycopg2.connect(user='ugen_integra', password='aghuintegracao', host='10.36.2.35', port='6544',
                                      database='dbaghu')
        cursor = connection.cursor()
        cursor.execute(f'SELECT lto_id, leito FROM AGH.ain_leitos WHERE unf_seq = {codigo_ala}')
        rows = cursor.fetchall()
        for row in rows:
            sem_hifen = row[0].split('-')[0]
            semzero = row[1].lstrip('0')
            dados = f'{sem_hifen}_{semzero}'
            lista_leitos.append(dados)
            dados = dados + '_aguardando'
            lista_leitos.append(dados)

        conexao = pymysql.connect(host=self.host, user=self.usermysql, password=self.password, database='sgl')
        cursor = conexao.cursor()
        leitos_str = ', '.join([f'\"{leito}\"' for leito in lista_leitos])
        comando = f'SELECT * FROM grade WHERE idGRADE IN ({leitos_str})'
        cursor.execute(comando)
        leitura = cursor.fetchall()
        self.table_copy.clearContents()
        self.table_copy.setRowCount(0)
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
                    row = self.table_copy.rowCount()
                    self.table_copy.insertRow(row)
                    item = item.text().replace('_', ' ')
                    item = QtWidgets.QTableWidgetItem(item)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.table_copy.setVerticalHeaderItem(row, item)
                    _translate = QtCore.QCoreApplication.translate
                    self.increase_column_width(0, 16)
                    item_pac = self.table_copy.verticalHeaderItem(row)
                    item_pac.setText(_translate('MainWindow', item.text()))
                if column != 0:
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    if item is None or item.text() == 'None':
                        item = QtWidgets.QTableWidgetItem(str(''))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.table_copy.setItem(row, column, item)

        self.checkboxes = []
        for row in range(self.table_copy.rowCount()):
            checkbox = QtWidgets.QCheckBox()
            checkbox.stateChanged.connect(lambda state, r=row: self.checkboxStateChanged(state, r))
            self.checkboxes.append(checkbox)

            # Adicionando checkbox à célula da tabela
            cell_widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(cell_widget)
            layout.addWidget(checkbox)
            layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Centralizar checkbox
            layout.setContentsMargins(0, 0, 0, 0)  # Remover margens
            cell_widget.setLayout(layout)
            self.table_copy.setCellWidget(row, 0, cell_widget)

        self.selecionado_pemuta = -1
    def _criar_btn_permutas(self,tabela_grade):

        self.btn_2leste_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_2leste_3.setGeometry(QtCore.QRect(100, 60, 71, 21))
        self.btn_2leste_3.setObjectName('btn_2leste_3')
        self.btn_2leste_3.clicked.connect(lambda: self.trocar_unidade_permuta(22))
        self.btn_2leste_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_6leste_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_6leste_3.setGeometry(QtCore.QRect(180, 30, 71, 21))
        self.btn_6leste_3.setObjectName('btn_6leste_3')
        self.btn_6leste_3.clicked.connect(lambda: self.trocar_unidade_permuta(30))
        self.btn_6leste_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_UCO_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_UCO_3.setGeometry(QtCore.QRect(340, 60, 71, 21))
        self.btn_UCO_3.setObjectName('btn_UCO_3')
        self.btn_UCO_3.clicked.connect(lambda: self.trocar_unidade_permuta(23))
        self.btn_UCO_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_CTI_3leste_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_CTI_3leste_3.setGeometry(QtCore.QRect(260, 60, 71, 21))
        self.btn_CTI_3leste_3.setObjectName('btn_CTI_3leste_3')
        self.btn_CTI_3leste_3.clicked.connect(lambda: self.trocar_unidade_permuta(24))
        self.btn_CTI_3leste_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_2sul_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_2sul_3.setGeometry(QtCore.QRect(500, 60, 71, 21))
        self.btn_2sul_3.setObjectName('btn_2sul_3')
        self.btn_2sul_3.clicked.connect(lambda: self.trocar_unidade_permuta(21))
        self.btn_2sul_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_8sul_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_8sul_3.setGeometry(QtCore.QRect(420, 30, 71, 21))
        self.btn_8sul_3.setObjectName('btn_8sul_3')
        self.btn_8sul_3.clicked.connect(lambda: self.trocar_unidade_permuta(33))
        self.btn_8sul_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_8norte_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_8norte_3.setGeometry(QtCore.QRect(580, 60, 71, 21))
        self.btn_8norte_3.setObjectName('btn_8norte_3')
        self.btn_8norte_3.clicked.connect(lambda: self.trocar_unidade_permuta(193))
        self.btn_8norte_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_CTI_PS_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_CTI_PS_3.setGeometry(QtCore.QRect(180, 60, 71, 21))
        self.btn_CTI_PS_3.setObjectName('btn_CTI_PS_3')
        self.btn_CTI_PS_3.clicked.connect(lambda: self.trocar_unidade_permuta(169))
        self.btn_CTI_PS_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.final = False
        self.btn_10norte_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_10norte_3.setGeometry(QtCore.QRect(260, 30, 71, 21))
        self.btn_10norte_3.setObjectName('btn_10norte_3')
        self.btn_10norte_3.clicked.connect(lambda: self.trocar_unidade_permuta(36))
        self.btn_10norte_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_8leste_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_8leste_3.setGeometry(QtCore.QRect(500, 30, 71, 21))
        self.btn_8leste_3.setObjectName('btn_8leste_3')
        self.btn_8leste_3.clicked.connect(lambda: self.trocar_unidade_permuta(34))
        self.btn_8leste_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_7norte_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_7norte_3.setGeometry(QtCore.QRect(420, 60, 71, 21))
        self.btn_7norte_3.setObjectName('btn_7norte_3')
        self.btn_7norte_3.clicked.connect(lambda: self.trocar_unidade_permuta(31))
        self.btn_7norte_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_9leste_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_9leste_3.setGeometry(QtCore.QRect(580, 30, 71, 21))
        self.btn_9leste_3.setObjectName('btn_9leste_3')
        self.btn_9leste_3.clicked.connect(lambda: self.trocar_unidade_permuta(35))
        self.btn_9leste_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_cti_ped_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_cti_ped_3.setGeometry(QtCore.QRect(100, 30, 71, 21))
        self.btn_cti_ped_3.setObjectName('btn_cti_ped_3')
        self.btn_cti_ped_3.clicked.connect(lambda: self.trocar_unidade_permuta(29))
        self.btn_cti_ped_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_7leste_3 = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_7leste_3.setGeometry(QtCore.QRect(340, 30, 71, 21))
        self.btn_7leste_3.setObjectName('btn_7leste_3')
        self.btn_7leste_3.clicked.connect(lambda: self.trocar_unidade_permuta(32))
        self.btn_7leste_3.setStyleSheet(
            '\n                    QPushButton {\n                        border: 2px solid #2E3D48;\n                        border-radius: 10px;\n                        background-color: #FFFFFF;\n                        color: #2E3D48;\n                    }\n                    QPushButton:pressed {\n                        background-color: #2E3D48;\n                        color: #FFFFFF;\n                    }\n                ')
        self.btn_reserva = QtWidgets.QPushButton(parent=self.frame_permuta)
        self.btn_reserva.setGeometry(QtCore.QRect(600, 500, 101, 31))
        self.btn_reserva.setObjectName('pushButton')
        self.btn_reserva.clicked.connect(lambda: self.finalizar_troca(tabela_grade))
        self.btn_reserva.setStyleSheet(
            '\n                QPushButton {\n                    border: 2px solid #2E3D48;\n                    border-radius: 10px;\n                    background-color: #FFFFFF;\n                    color: #2E3D48;\n                }\n\n                QPushButton:hover {\n                    background-color: #DDDDDD;  /* Change this to your desired hover color */\n                    color: rgb(0, 0, 0);\n                }\n\n                QPushButton:pressed {\n                    background-color: #2E3D48;  /* Change this to your desired pressed color */\n                    color: #FFFFFF;\n                }\n            ')

    def finalizar_troca(self,tabela_grade):
        selecionado = []
        selecionado_per = []
        analise = 0
        analise2 = 0
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
        if(analise == 1 and self.selecionado_pemuta != -1):
            for row in reversed(selecionado):
                leitos = tabela_grade.verticalHeaderItem(row)
                LEITOS = leitos.text()
                nome_item = tabela_grade.item(row, colum_nome)
                data_nasc =tabela_grade.item(row, colum_data_nas)
                obs = tabela_grade.item(row, colum_obs)
                npf = tabela_grade.item(row, colum_npf)
                prontuario = tabela_grade.item(row, colum_prontuario)
                tipo_leito = tabela_grade.item(row, colum_tipo_leito)
                previsao_alta = tabela_grade.item(row, colum_previsao_alta)
                data_atualizao_status = tabela_grade.item(row, colum_data_atualizao_status)
                solicitante = tabela_grade.item(row, colum_solicitante)
                pergunta_reserva_comunicada = tabela_grade.item(row, colum_pergunta_reserva_comunicada)
                reserva_comunicada_a_quem = tabela_grade.item(row, colum_reserva_comunicada_a_quem)
                if tipo_leito is None:
                    TIPO = ''
                else:
                    TIPO = tipo_leito.text()

                codigo = tabela_grade.item(row, colum_codigo)
                sexo = tabela_grade.item(row, colum_status)
                if sexo is None:
                    sexo = ''
                else:
                    sexo = sexo.text()

                status = tabela_grade.item(row, colum_sexo)
                if status is None:
                    status = ''
                else:
                    status = status.text()

            row = self.selecionado_pemuta
            leitos_perm = self.table_copy.verticalHeaderItem(row)
            LEITOS_perm = leitos_perm.text()
            nome_item_perm = self.table_copy.item(row, colum_nome)
            data_nasc_perm = self.table_copy.item(row, colum_data_nas)
            obs_perm = self.table_copy.item(row, colum_obs)
            npf_perm = self.table_copy.item(row, colum_npf)
            prontuario_perm = self.table_copy.item(row, colum_prontuario)
            tipo_leito_perm = self.table_copy.item(row, colum_tipo_leito)
            previsao_alta_perm = self.table_copy.item(row, colum_previsao_alta)
            data_atualizao_status_perm = self.table_copy.item(row, colum_data_atualizao_status)
            solicitante_perm = self.table_copy.item(row, colum_solicitante)
            pergunta_reserva_comunicada_perm = self.table_copy.item(row, colum_pergunta_reserva_comunicada)
            reserva_comunicada_a_quem_perm = self.table_copy.item(row, colum_reserva_comunicada_a_quem)
            if tipo_leito_perm is None:
                TIPO_perm = ''
            else:
                TIPO_perm = tipo_leito_perm.text()
            codigo_perm = self.table_copy.item(row, colum_codigo)

            sexo_perm = self.table_copy.item(row, colum_status)
            if sexo_perm is None:
                sexo_perm = ''
            else:
                sexo_perm = sexo_perm.text()

            status_perm = self.table_copy.item(row, colum_sexo)
            if status_perm is None:
                status_perm = ''
            else:
                status_perm = status_perm.text()
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('CONFIRMAR?')
            icon = QIcon(resource_path('imagens/warning.ico'))
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            reply = msg_box.exec()
            
            if reply == QMessageBox.StandardButton.Yes:
                if (self.codigo_permuta == self.codigo_ala):
                    self.alt_banco(codigo, prontuario, npf, obs, status, nome_item, data_nasc, sexo, LEITOS_perm,
                                   previsao_alta,
                                   data_atualizao_status, solicitante, pergunta_reserva_comunicada,
                                   reserva_comunicada_a_quem, TIPO)

                    self.alt_banco(codigo_perm, prontuario_perm, npf_perm, obs_perm, status_perm, nome_item_perm,
                                   data_nasc_perm, sexo_perm, LEITOS, previsao_alta_perm,
                                   data_atualizao_status_perm, solicitante_perm, pergunta_reserva_comunicada_perm,
                                   reserva_comunicada_a_quem_perm, TIPO_perm)
                    self.atualiza_cti()
                else:

                    item = QtWidgets.QTableWidgetItem(str(''))
                    self.alt_banco(codigo, prontuario, npf, obs, status, nome_item, data_nasc, sexo_perm, LEITOS_perm,item,item, item, item,item, TIPO_perm)
                    self.alt_banco(codigo_perm, prontuario_perm, npf_perm, obs_perm, status_perm, nome_item_perm, data_nasc_perm, sexo, LEITOS,item,item, item, item,item, TIPO)
                    self.atualiza_cti()

                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText('TROCA REALIZADA.')
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply = msg_box.exec()
                icon = QIcon(resource_path('imagens/warning.ico'))
                msg_box.setWindowIcon(icon)
                self.frame_permuta.close()

    def checkboxStateChanged(self, state, row):
        """ Habilita ou desabilita outros checkboxes baseado no estado atual """
        if state == QtCore.Qt.CheckState.Checked.value:
            # Se um for marcado, desabilita os outros
            self.selecionado_pemuta = row
            for i, checkbox in enumerate(self.checkboxes):
                if i != row:
                    checkbox.setEnabled(False)
        else:
            # Se nenhum estiver marcado, reabilita todos
            for checkbox in self.checkboxes:
                checkbox.setEnabled(True)

    def mudar_cor_vertical_heider(self, index):
        """Abre um diálogo para escolher a cor e altera o fundo do cabeçalho vertical"""
        color = QColorDialog.getColor()
        if color.isValid():
            color_name = color.name()  # Obtém a cor no formato hexadecimal (#RRGGBB)
            self.header_colors[index] = color.name()  # Atualiza a cor da linha clicada
            self.custom_header.cores = self.header_colors  # Aplica as novas cores ao cabeçalho
            self.custom_header.viewport().update()  # Atualiza a exibição

            conexao = pymysql.connect(host=self.host, user=self.usermysql, password=self.password, database='sgl')
            cursor = conexao.cursor()

            leitos = self.tabela_grade.verticalHeaderItem(index)
            LEITOS = leitos.text()
            LEITOS = LEITOS.replace(' ', '_')

            # Verifica se o leito já existe na tabela
            cursor.execute('SELECT leito FROM color_table WHERE leito = %s', (LEITOS,))
            resultado = cursor.fetchone()

            if resultado:
                # Se o leito existir, atualiza a cor
                comando = 'UPDATE color_table SET cor = %s WHERE leito = %s'
            else:
                # Se o leito não existir, insere um novo registro
                comando = 'INSERT INTO color_table (cor, leito) VALUES (%s, %s)'

            valores = (color_name, LEITOS)  # Usa a cor no formato hexadecimal
            cursor.execute(comando, valores)
            conexao.commit()
            cursor.close()
            conexao.close()

    def is_cell_editable(self, table_widget, row, column):
        item = table_widget.item(row, column)
        if item is None:
            return False
        return bool(item.flags() & Qt.ItemFlag.ItemIsEditable)
    def demanda_volta(self, Main):
        Main.hide()
        self.form.hide()
        self.form.show()
        self.teladem.grade_aberta = False
        Main.show()

    def ativar_selecao(self, row):

        item = self.tabela_grade.item(row, 0)  # Pegamos a checkbox que está na coluna 0
        linhas = self.tabela_grade.rowCount()
        colunas = self.tabela_grade.columnCount()
        if item is not None:
            # Alterna entre marcado e desmarcado
            if item.checkState() == Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Unchecked)

            else:
                item.setCheckState(Qt.CheckState.Checked)
                item = self.tabela_grade.verticalHeaderItem(row)
                fonte = item.font()
                fonte.setBold(True)
                fonte.setPointSize(10)
                item.setFont(fonte)

                for j in range(colunas):
                    item = self.tabela_grade.item(row, j)
                    if item is not None:
                        fonte = item.font()
                        fonte.setBold(True)
                        item.setFont(fonte)
                self.tabela_grade.setRowHeight(row, 35)
    def colocar_widget(self, row, column):
        self.numero_versao_atual = None

        widget = self.lista_widgets[column]
        for col in range(self.tabela_grade.columnCount()):
            self.tabela_grade.item(row, col).setBackground(QColor("#D4EDDA"))

        if widget == 'QDateEdit':
            item = self.tabela_grade.item(row, column)
            if item is not None:
                if self.is_cell_editable(self.tabela_grade, row, column):
                    dado = item.text()

                    qtwidget = QtWidgets.QDateEdit()
                    bg_color = item.background().color().name()
                    if bg_color == '#000000':
                        bg_color = 'white'

                    qtwidget.setStyleSheet(f' background-color: {bg_color};')
                    qtwidget.setFixedSize(self.tabela_grade.columnWidth(column), self.tabela_grade.rowHeight(row))
                    qtwidget.setCalendarPopup(True)
                    qtwidget.setDate(QDate.fromString(dado, 'dd/MM/yyyy'))

                    self.tabela_grade.setCellWidget(row, column, qtwidget)
                    self.current_editor = qtwidget
                    self.current_pos = (row, column)
                    qtwidget.dateChanged.connect(
                        lambda date: self.aterar_dados_database(date.toString("dd/MM/yyyy"), 'QDateEdit'))

                    qtwidget.setStyleSheet(f"""
                                                                                          background-color: {bg_color};
                                                                                          font-weight: bold;
                                                                                          font-size: 10pt;
                                                                                          qproperty-alignment: AlignCenter;
                                                                                          """)
                    qtwidget.setAlignment(Qt.AlignmentFlag.AlignCenter)

                    self.key_filter = KeyFilter(self.on_tab_pressed)
                    qtwidget.installEventFilter(self.key_filter)
                    qtwidget.setFocus()

        elif widget == 'QDateTimeEdit':
            item = self.tabela_grade.item(row, column)
            if item is not None:
                if self.is_cell_editable(self.tabela_grade, row, column):

                    dado = item.text()
                    qtwidget = QtWidgets.QDateTimeEdit()

                    bg_color = item.background().color().name()
                    if bg_color == '#000000':
                        bg_color = 'white'
                    qtwidget.setStyleSheet(f'background-color: {bg_color};')
                    qtwidget.setFixedSize(
                        self.tabela_grade.columnWidth(column),
                        self.tabela_grade.rowHeight(row)
                    )
                    qtwidget.setCalendarPopup(True)
                    for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M'):
                        try:
                            dt = datetime.strptime(dado, fmt)
                            qdatetime = QDateTime(dt)
                            qtwidget.setDateTime(qdatetime)
                            break
                        except ValueError:
                            continue
                    else:
                        print(f"Formato de data inválido: {dado}")
                    self.tabela_grade.setCellWidget(row, column, qtwidget)

                    self.current_editor = qtwidget
                    self.current_pos = (row, column)
                    qtwidget.dateTimeChanged.connect(
                        lambda dt: self.aterar_dados_database(dt.toString("dd/MM/yyyy HH:mm"), 'QDateTimeEdit'))

                    qtwidget.setStyleSheet(f"""
                                                                                          background-color: {bg_color};
                                                                                          font-weight: bold;
                                                                                          font-size: 10pt;
                                                                                          qproperty-alignment: AlignCenter;
                                                                                          """)
                    qtwidget.setAlignment(Qt.AlignmentFlag.AlignCenter)

                    self.key_filter = KeyFilter(self.on_tab_pressed)
                    qtwidget.installEventFilter(self.key_filter)
                    qtwidget.setFocus()

        elif widget == 'QTimeEdit':
            item = self.tabela_grade.item(row, column)
            if item is not None:
                if self.is_cell_editable(self.tabela_grade, row, column):

                    dado = item.text()
                    qtwidget = QtWidgets.QTimeEdit()

                    time = QtCore.QTime.fromString(dado, "HH:mm")  # Ajuste o formato conforme necessário
                    if time.isValid():
                        qtwidget.setTime(time)

                    # Cor de fundo
                    bg_color = item.background().color().name()
                    if bg_color == '#000000':
                        bg_color = 'white'

                    qtwidget.setStyleSheet(f"""
                                                                                          background-color: {bg_color};
                                                                                          font-weight: bold;
                                                                                          font-size: 10pt;
                                                                                          qproperty-alignment: AlignCenter;
                                                                                          """)
                    qtwidget.setAlignment(Qt.AlignmentFlag.AlignCenter)

                    self.key_filter = KeyFilter(self.on_tab_pressed)
                    qtwidget.installEventFilter(self.key_filter)
                    qtwidget.setFocus()

                    qtwidget.setFixedSize(self.tabela_grade.columnWidth(column),
                                          self.tabela_grade.rowHeight(row))
                    self.tabela_grade.setCellWidget(row, column, qtwidget)

                    self.current_editor = qtwidget
                    self.current_pos = (row, column)
                    qtwidget.timeChanged.connect(
                        lambda time: self.aterar_dados_database(time.toString("HH:mm"), 'QTimeEdit'))

                    self.event_filter = TabTimerEventFilter(self)
                    qtwidget.installEventFilter(self.event_filter)
        elif widget == 'QLineEdit':
            item = self.tabela_grade.item(row, column)
            text = item.text() if item else ""
            line_edit = QLineEdit(text)

            bg_color = item.background().color().name()
            if bg_color == '#000000':
                bg_color = 'white'
            line_edit.setStyleSheet(f'background-color: {bg_color}; border: none;')
            self.tabela_grade.setCellWidget(row, column, line_edit)
            line_edit.setFocus()

            # Atualiza estado
            self.current_editor = line_edit
            self.current_pos = (row, column)

            colum_paciente = 4
            colum_prontuario = 1
            colum_data_nace = 5

            colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE', colum_paciente)
            colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', colum_prontuario)
            colum_data_nace = self.descobrir_nome_coluna('DATA DE NASCIMENTO', colum_data_nace)

            line_edit.setStyleSheet(f"""
                                background-color: {bg_color};
                                font-weight: bold;
                                font-size: 10pt;
                                qproperty-alignment: AlignCenter;
                            """)

            line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

            line_edit.setFocus()

            self.key_filter = KeyFilter(self.on_tab_pressed)
            line_edit.installEventFilter(self.key_filter)
            line_edit.setFocus()

            if column == colum_prontuario:
                line_edit.textChanged.connect(
                    lambda text, datanasce=colum_data_nace, r=row, line=line_edit: self.prontu_text(text, datanasce, r,
                                                                                                    line))
            elif column == colum_paciente:
                line_edit.textChanged.connect(
                    lambda text, datanasce=colum_data_nace, r=row, line=line_edit: self.name_text(text, datanasce, r,
                                                                                                  line))
            else:
                line_edit.textChanged.connect(lambda texto: self.aterar_dados_database(texto, 'QLineEdit'))

        elif widget is not None:

            combo_box = QComboBox()
            item = self.tabela_grade.item(row, column)
            bg_color = item.background().color().name() if item else '#FFFFFF'
            if bg_color == '#000000':
                bg_color = 'white'
            combo_box.setStyleSheet(f'background-color: {bg_color};')
            combo_box.setFixedSize(self.tabela_grade.columnWidth(column), self.tabela_grade.rowHeight(row))

            if item is not None and self.is_cell_editable(self.tabela_grade, row, column):
                especialidades = ast.literal_eval(widget)
                if isinstance(especialidades, list):
                    texto = item.text()
                    combo_box.addItem(item.text())
                    combo_box.addItems(especialidades)
                    combo_box.setCurrentText(texto)
                    self.tabela_grade.setCellWidget(row, column, combo_box)
                else:
                    print("Conteúdo não é uma lista válida.")

            self.current_editor = combo_box
            self.current_pos = (row, column)
            combo_box.currentTextChanged.connect(lambda texto: self.aterar_dados_database(texto, 'QComboBox'))

            self.key_filter = KeyFilter(self.on_tab_pressed)
            combo_box.installEventFilter(self.key_filter)

    def on_tab_pressed(self, widget):
        row, column = self.current_pos
        max_row = self.tabela_grade.rowCount() - 1
        max_col = self.tabela_grade.columnCount() - 1

        if column < max_col:
            column += 1
        else:
            column = 1
            if row < max_row:
                row += 1
            else:
                row = 0

        self.tabela_clicada(row, column)

        widget = self.tabela_grade.cellWidget(row, column)
    def aterar_dados_database(self, texto, tipo):
        try:
            row, colum = self.current_pos

            colum_prontuario = 1

            colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', colum_prontuario)

            item = QtWidgets.QTableWidgetItem(texto)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.tabela_grade.setItem(row, colum, QTableWidgetItem(item))
            id_valor = self.tabela_grade.verticalHeaderItem(row).text()

            if self.analisar_requisitos_tabela_paciente(texto, id_valor, row, colum):
                print('passou moddigica', id_valor)
                self.data_grade.modificar_tabela(self, texto, id_valor, colum)

                self.lista_modificacao = []

                colum_sexo = 5
                print('pai', texto)
                if self.descobrir_nome_coluna('STATUS DO LEITO', 5) == colum and texto == 'VAGO':
                    print('pai3')
                    for j in range(1, self.tabela_grade.columnCount()):
                        if j == self.descobrir_nome_coluna('SEXO DA ENFERMARIA', 5):
                            continue
                        print(id_valor)
                        if j == colum:
                            continue
                        self.data_grade.modificar_tabela(self, '', id_valor, j)

                    self.data_grade.modificar_tabela(self, '', id_valor, self.descobrir_nome_coluna('STATUS DO LEITO', 5))

                    self.data_grade.retirar_aguardando(row, self)
                    self.atualiza_cti()

                self.add_historico(id_valor)

                if self.descobrir_nome_coluna('STATUS DO LEITO', 5) == colum and texto != 'VAGO':
                    colum = self.descobrir_nome_coluna('DATA E HORA DE ATUALIZAÇÃO DO STATUS', None)
                    if colum is not None:
                        current_datetime = QDateTime.currentDateTime()
                        formatted_datetime = current_datetime.toString('dd/MM/yyyy hh:mm:ss')
                        self.data_grade.modificar_tabela(self, formatted_datetime, id_valor, colum)

                    self.colocar_vago_ocupado_historico(row, texto)

            self.copiadora()
        except Exception as e:
            print(f"Error: {e}")

    def add_historico(self,col_label):

        row, colum = self.current_pos

        current_datetime = QDateTime.currentDateTime()
        formatted_time = current_datetime.toString('hh:mm')

        colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE', None)
        colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', None)
        colum_data_nace = self.descobrir_nome_coluna('DATA DE NASCIMENTO', None)

        if self.tabela_grade.item(row, colum_paciente) is None:
            nome = ''
        else:
            nome = self.tabela_grade.item(row, colum_paciente).text()

        if self.tabela_grade.item(row, colum_prontuario) is None:
            pront = ''
        else:
            pront = self.tabela_grade.item(row, colum_prontuario).text()

        if self.tabela_grade.item(row, colum_data_nace) is None:
            data_nascimento = ''
        else:
            data_nascimento = self.tabela_grade.item(row, colum_data_nace).text()

        texto_historico = f'{formatted_time}                {self.nome_user} ALTEROU O \"{col_label}\"  NO PACIENTE \"{nome}\"'

        alteracao = 'EDITOU'
        coluna_alteracao = f"{row, colum}"

        lista_leitos = self.data_grade.lista_leitos_filtro_aghu(self)
        leitura = self.data_grade.ler_database(self, lista_leitos)
        tabela = self.formatar_nome(self.nome_tabela_post)
        self.data_grade.criar_ou_atualizar_snapshot(tabela, self, pront, data_nascimento, nome, texto_historico,
                                                    coluna_alteracao, alteracao,leitura)

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

        return nome
    def colocar_vago_ocupado_historico(self,row,alteracao):

        colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE', None)
        colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', None)
        colum_data_nace = self.descobrir_nome_coluna('DATA DE NASCIMENTO', None)

        pront = self.tabela_grade.item(row, colum_prontuario)
        data = self.tabela_grade.item(row, colum_data_nace)
        nome = self.tabela_grade.item(row, colum_paciente)

        if self.tabela_grade.item(row, colum_paciente) is None:
            nome = ''
        else:
            nome = self.tabela_grade.item(row, colum_paciente).text()

        if self.tabela_grade.item(row, colum_prontuario) is None:
            pront = ''
        else:
            pront = self.tabela_grade.item(row, colum_prontuario).text()

        if self.tabela_grade.item(row, colum_data_nace) is None:
            data = ''
        else:
            data = self.tabela_grade.item(row, colum_data_nace).text()

        valores = self.tabela_grade.verticalHeaderItem(row).text()


        current_datetime = QDateTime.currentDateTime()
        formatted_time = current_datetime.toString('hh:mm')

        texto_historico = (f'{formatted_time}                {self.nome_user} DEIXOU O LEITO \"{valores}\" {alteracao} ')

        print('excl', pront, data, nome, texto_historico, f'{row}', alteracao)

        lista_leitos = self.data_grade.lista_leitos_filtro_aghu(self)
        leitura = self.data_grade.ler_database(self, lista_leitos)

        tabela = self.formatar_nome(self.nome_tabela_post)
        self.data_grade.criar_ou_atualizar_snapshot(tabela, self, pront, data, nome, texto_historico, f'{row}',
                                                    alteracao,leitura)
    def analisar_requisitos_tabela_paciente(self, valor_para_inserir, id_valor, row, colum):
        colum_paciente = 4
        colum_prontuario = 1

        colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE', colum_paciente)
        colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', colum_prontuario)
        print(colum_prontuario, colum_paciente)
        if self.tabela_grade.item(row, colum_prontuario) is not None and self.tabela_grade.item(row,
                                                                                              colum_paciente) is not None:
            if self.tabela_grade.item(row, colum_prontuario).text() != '' and self.tabela_grade.item(row,
                                                                                                   colum_paciente).text() != '':
                return True
            elif self.tabela_grade.item(row, colum_prontuario).text() == '':
                if self.tabela_grade.item(row, colum_paciente).text() == '':
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Information)
                    msg_box.setWindowTitle('AVISO')
                    msg_box.setText('O campo \"PRONTUÁRIO\" é obrigatório!')

                    icon = QtGui.QIcon(resource_path('imagens/escondido.ico'))
                    msg_box.setWindowIcon(icon)
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                    reply = msg_box.exec()
                    return False
                return True
            else:
                if self.tabela_grade.item(row, colum_prontuario).text() == '':
                    self.message_box_ok('O campo \"NOME DO PACIENTE\" é obrigatório!')

                    return False
                return True

    def descobrir_nome_coluna(self, nome, coluna):
        for col in range(self.tabela_grade.columnCount()):
            item_pac = self.tabela_grade.horizontalHeaderItem(col)
            if item_pac is not None:
                if item_pac.text() == nome:
                    return col
        return coluna

    def set_and_move(self):
        if not self.current_editor:
            return

        row, col = self.current_pos
        self.tabela_grade.removeCellWidget(row, col)
        print('remove', col, row)
        next_row, next_col = self.get_next_cell(row, col)

        if next_row is not None:
            self.tabela_grade.selectRow(next_row)
            self.tabela_clicada(next_row, next_col)
        else:
            self.current_editor = None  # Acabou

    def get_next_cell(self, row, col):
        col += 1
        print('coluna pf2',col,row)
        if col >= self.tabela_grade.columnCount():
            col = 0
            row += 1

        print('coluna pf1',col,row)
        if row >= self.tabela_grade.rowCount():
            return None, None
        print('coluna pf',col,row)
        return row, col

    def edit_tabela(self, pos: QPoint):
        print(21)
        # header = self.tabela_grade.horizontalHeader()
        # logical_index = header.logicalIndexAt(pos)
        # if logical_index < 0:
        #     return
        #
        # menu = QMenu(self)
        # action1 = QAction("Editar Layout da Tabela", self)
        # action1.triggered.connect(self.sua_funcao_de_edicao)
        # menu.addAction(action1)
        # menu.exec(header.mapToGlobal(pos))

    def ocupar_leito(self):
        analise = 0
        selecionado = []
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Deixar Leito Ocupado?')

        icon = QtGui.QIcon(resource_path('imagens/escondido.ico'))
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            for row in range(self.tabela_grade.rowCount()):
                selecao = self.tabela_grade.item(row, 0)
                if selecao:
                    if selecao.checkState() == QtCore.Qt.CheckState.Checked:
                        analise = 1
                        selecionado.append(row)

            for i in selecionado:
                id_valor = self.tabela_grade.verticalHeaderItem(i).text()
                for j in range(1, self.tabela_grade.columnCount()):
                    if j == self.descobrir_nome_coluna('STATUS DO LEITO', None):
                        dado = 'OCUPADO'
                        self.data_grade.modificar_tabela(self, dado, id_valor, j)
                        break
                    else:
                        return

                self.data_grade.retirar_aguardando(i, self)


                item = self.tabela_grade.item(i, 0)
                if item is not None and item.background().style() != QtGui.QBrush().style():
                    adjusted_color = item.background().color()
                else:
                    adjusted_color = QColor("white")
                self.colocar_caixa_selecao(i, adjusted_color)

                self.colocar_vago_ocupado_historico(i,'OCUPADO')

            self.message_box_ok('Alteração Concluida Com Sucesso')

            self.atualiza_cti()
            self.btn_permuta.hide()
            self.deixar_vago.hide()
            self.btn_alta.hide()

    def leito_vago(self):
        analise = 0
        selecionado = []
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Deixar Leito Vago?')

        icon = QtGui.QIcon(resource_path('imagens/escondido.ico'))
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            for row in range(self.tabela_grade.rowCount()):
                selecao = self.tabela_grade.item(row, 0)
                if selecao:
                    if selecao.checkState() == QtCore.Qt.CheckState.Checked:
                        analise = 1
                        selecionado.append(row)

            for i in selecionado:
                id_valor = self.tabela_grade.verticalHeaderItem(i).text()
                for j in range(1, self.tabela_grade.columnCount()):
                    dado = ''
                    if j == self.descobrir_nome_coluna('SEXO DA ENFERMARIA', None) or j == self.descobrir_nome_coluna('TIPO DE LEITO', None):
                        continue
                    print(id_valor)
                    if j == self.descobrir_nome_coluna('STATUS DO LEITO', None):
                        dado = 'VAGO'
                    self.data_grade.modificar_tabela(self, dado, id_valor, j)

                self.data_grade.retirar_aguardando(i, self)

                item = self.tabela_grade.item(i, 0)
                if item is not None and item.background().style() != QtGui.QBrush().style():
                    adjusted_color = item.background().color()
                else:
                    adjusted_color = QColor("white")
                self.colocar_caixa_selecao(i, adjusted_color)
                self.colocar_vago_ocupado_historico(i,'VAGO')

            self.message_box_ok('Alteração Concluida Com Sucesso')

            self.atualiza_cti()
            self.btn_permuta.hide()
            self.deixar_vago.hide()
            self.btn_alta.hide()

    def trocando_pacientes_mesma_tabela(self):

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Concluir Troca?')

        icon = QtGui.QIcon(resource_path('imagens/escondido.ico'))
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:

            print(2121,self.lista_permuta,'analisa')
            linha1 = 0
            linha2 = 0
            for id_valor in self.lista_permuta:
                id1 = self.lista_permuta[0]
                id2 = self.lista_permuta[1]
            print(id2,id1)
            for i in range(self.tabela_grade.rowCount()):
                print(self.tabela_grade.verticalHeaderItem(i).text())
                if self.tabela_grade.verticalHeaderItem(i).text() == id1:
                    linha1 = i

                if self.tabela_grade.verticalHeaderItem(i).text() == id2:
                    linha2 = i

            LEITOUNO = self.tabela_grade.verticalHeaderItem(linha1).text()
            LEITODONO = self.tabela_grade.verticalHeaderItem(linha2).text()
            print(linha1,linha2)
            for j in range(1, self.tabela_grade.columnCount()):
                if j == self.descobrir_nome_coluna('SEXO DA ENFERMARIA', 5):
                    continue
                dado1 = self.tabela_grade.item(linha1, j)
                dado2 = self.tabela_grade.item(linha2, j)

                if dado1 is None:
                    dado1 = ''
                else:
                    dado1= dado1.text()


                if dado2 is None:
                    dado2 = ''
                else:
                    dado2= dado2.text()
                print(dado1,dado2, 'analisa')
                self.data_grade.modificar_tabela(self, dado2, id1, j)
                self.data_grade.modificar_tabela(self, dado1, id2, j)

            item = self.tabela_grade.item(linha2, 0)
            if item is not None and item.background().style() != QtGui.QBrush().style():
                adjusted_color = item.background().color()
            else:
                adjusted_color = QColor("white")

            self.colocar_caixa_selecao(linha2,adjusted_color)

            item = self.tabela_grade.item(linha1, 0)
            if item is not None and item.background().style() != QtGui.QBrush().style():
                adjusted_color = item.background().color()
            else:
                adjusted_color = QColor("white")
            self.colocar_caixa_selecao(linha1,adjusted_color)

            self.message_box_ok('Alteração Concluida Com Sucesso')


            current_datetime = QDateTime.currentDateTime()
            formatted_time = current_datetime.toString('hh:mm')

            texto_historico = (
                f'{formatted_time}                {self.nome_user} REALIZOU PERMUTA ENTRE OS LEITOS \"{LEITOUNO}\" E \"{LEITODONO}\"')
            alteracao = 'PERMUTA'
            print('excl', pront, data, nome, texto_historico, f'{row}', alteracao)

            lista_leitos = self.data_grade.lista_leitos_filtro_aghu(self)
            leitura = self.data_grade.ler_database(self, lista_leitos)

            tabela = self.formatar_nome(self.nome_tabela_post)
            self.data_grade.criar_ou_atualizar_snapshot(tabela, self, pront, data, nome, texto_historico, f'{linha1}',
                                                        alteracao, leitura)

            self.atualiza_cti()
            self.btn_permuta.hide()
            self.deixar_vago.hide()
            self.btn_alta.hide()

    def trocar_pacientes_diferente_tabela(self):

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Concluir Troca?')

        icon = QtGui.QIcon(resource_path('imagens/escondido.ico'))
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            lista_colunas = ['NPF','CÓDIGO DE INTERNACAO','STATUS DO LEITO','SEXO DA ENFERMARIA','PRONTUÁRIO','OBSERVAÇÕES','NOME DO PACIENTE','DATA DE NASCIMENTO','SOLICITANTE']

            pares = self.comparar_pares()
            if pares:
                for p1, p2 in pares:
                    for coluna in lista_colunas:
                        print(p1[0], coluna, p1[1])
                        print(p2[0], coluna, p2[1])
                        colum1 = self.data_grade.pegar_coluna_Grade(self, p1[0], coluna)
                        if colum1 is None:
                            continue
                        print(colum1)
                        coluna_bd = "col" if colum1 == 0 else f"col{colum1}"
                        dadop1 = self.data_grade.pegar_Dados_Grade(self, p1[1], coluna_bd)

                        colum2 = self.data_grade.pegar_coluna_Grade(self, p2[0], coluna)
                        if colum2 is None:
                            continue
                        coluna_bd = "col" if colum2 == 0 else f"col{colum2}"
                        dadop2 = self.data_grade.pegar_Dados_Grade(self, p2[1], coluna_bd)

                        print(dadop1, dadop2)

                        self.data_grade.modificar_tabela(self, dadop2, p1[1], colum1+1)
                        self.data_grade.modificar_tabela(self, dadop1, p2[1], colum2+1)

                        for row in range(self.tabela_grade.rowCount()):
                            id_valor = self.tabela_grade.verticalHeaderItem(row).text()

                            if id_valor == p1[1] or id_valor == p2[1]:
                                item = self.tabela_grade.item(row, 0)
                                if item is not None and item.background().style() != QtGui.QBrush().style():
                                    adjusted_color = item.background().color()
                                else:
                                    adjusted_color = QColor("white")
                                self.colocar_caixa_selecao(row, adjusted_color)

            self.message_box_ok('Alteração Concluida Com Sucesso')
            self.atualiza_cti()
            self.btn_permuta.hide()
            self.deixar_vago.hide()
            self.btn_alta.hide()
            self.btn_permuta_diferentes_tabelas.hide()
            self.lista_permuta_tabela_diferente = []

            # for area, leito in self.lista_permuta_tabela_diferente:
            #     print(area, leito)
            #
            #     colum = self.data_grade.pegar_coluna_Grade(self, area,'NPF')
            #
            #     self.data_grade.modificar_tabela(self, texto, id_valor, colum)

    def comparar_pares(self):
        grupo1 = []
        grupo2 = []

        if not self.lista_permuta_tabela_diferente:
            return

        alas = list(set(ala for ala, _ in self.lista_permuta_tabela_diferente))
        if len(alas) != 2:
            return

        ala1, ala2 = alas

        for ala, leito in self.lista_permuta_tabela_diferente:
            if ala == ala1:
                grupo1.append((ala, leito))
            elif ala == ala2:
                grupo2.append((ala, leito))

        grupo1.sort(key=lambda x: x[1])
        grupo2.sort(key=lambda x: x[1])

        tamanho = min(len(grupo1), len(grupo2))

        pares = []
        for i in range(tamanho):
            pares.append((grupo1[i], grupo2[i]))

        return pares

    def colocar_caixa_selecao(self,row,adjusted_color):

        selecao = QtWidgets.QTableWidgetItem()
        selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
        selecao.setBackground(QtGui.QBrush(adjusted_color))
        self.tabela_grade.setItem(row, 0, selecao)

    def message_box_ok(self, text):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText(text)

        icon = QtGui.QIcon(resource_path('imagens/escondido.ico'))
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        reply = msg_box.exec()
