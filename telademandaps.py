import pymysql
from PyQt6.QtCore import QEvent, QObject,QDate, QDateTime,QDateTime, QSettings, QStandardPaths, QPoint, Qt,QDate,QTimer
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox,QDialog,QVBoxLayout, QRadioButton, QDialogButtonBox, QStackedWidget,QAbstractItemView,QInputDialog,QStyledItemDelegate,QMenuBar,QMenu,QHeaderView,QColorDialog, QTableWidget, QApplication,QScrollArea,QHBoxLayout,QPushButton,QToolTip, QLabel, QSpacerItem, QSizePolicy,QFrame, QCheckBox, QTableWidgetItem, QLineEdit, QTimeEdit, QDateEdit, QDateTimeEdit, QComboBox, QWidget
from GRADE import Ui_CTI_PED
from criar_nova_tabela import Criartabela
from editor_de_tabela import Editabletabela
from database_Demandas import Ui_data_Demanda
from PyQt6.QtCore import QDateTime, QSettings, QStandardPaths, QPoint, Qt,QDate,QTimer,pyqtSignal
from PyQt6.QtGui import QPalette, QPixmap, QGuiApplication, QStandardItem, QBrush,QIcon, QColor,QPen,QAction,QFont
import datetime
import csv
from pathlib import Path
from os.path import expanduser
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QFile
import ast
from datetime import datetime
from conecao_api import Ui_API
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os
import sys
import unicodedata
import re
from ldap3 import Server, Connection, ALL, SUBTREE
from PyQt6.QtGui import QCloseEvent

variaveis = {
    "AUTH_LDAP_SERVER_URI": "ldap://10.36.2.21",
    "AUTH_LDAP_BIND_DN": "CN=TAGS,OU=Servicos,OU=Usuarios,OU=HCMG,OU=EBSERH,DC=ebserhnet,DC=ebserh,DC=gov,DC=br",
    "AUTH_LDAP_BIND_PASSWORD": "T4g5@2022!",
    "AUTH_LDAP_BASE_DN": "OU=Usuarios,OU=HCMG,OU=EBSERH,DC=ebserhnet,DC=ebserh,DC=gov,DC=br"
}
try:

    def resource_path(relative_path):
        """Resolve path para PyInstaller"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)


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

            for nome, email, departamento,tipo, dept_novo in solicitacoes:
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

    class CustomInputDialog(QDialog):
        def __init__(self, widget_type=None, dados=None):
            if dados is None:
                dados = {}

            super().__init__()
            self.setWindowTitle("Selecionar Tipo de Campo")
            self.setMinimumWidth(300)
            layout = QVBoxLayout(self)

            # Radio buttons
            self.radio_campo = QRadioButton("CAMPO ABERTO")
            self.radio_tempo = QRadioButton("TEMPORIZADOR")
            self.radio_data = QRadioButton("DATA")
            self.radio_data_tempo = QRadioButton("DATA COM TEMPO")
            self.radio_lista = QRadioButton("LISTA SUSPENSA")
            layout.addWidget(self.radio_campo)
            layout.addWidget(self.radio_tempo)
            layout.addWidget(self.radio_data)
            layout.addWidget(self.radio_data_tempo)
            layout.addWidget(self.radio_lista)

            # Stack
            self.stack = QStackedWidget()
            layout.addWidget(self.stack)

            self.line_edit = QLineEdit()
            self.stack.addWidget(self.line_edit)

            self.time_edit = QTimeEdit()
            self.time_edit.setDisplayFormat("HH:mm:ss")
            self.stack.addWidget(self.time_edit)

            self.date_edit = QDateEdit()
            self.date_edit.setDisplayFormat("dd/MM/yyyy")
            self.date_edit.setDate(QDate.currentDate())
            self.stack.addWidget(self.date_edit)

            self.datetime_edit = QDateTimeEdit()
            self.datetime_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
            self.datetime_edit.setDateTime(QDateTime.currentDateTime())
            self.stack.addWidget(self.datetime_edit)

            typo_dado = widget_type
            self.combo = QComboBox()

            if widget_type != "QTimeEdit" and widget_type != "QLineEdit" and widget_type != "QDateTimeEdit" and widget_type != "QDateEdit":

                import ast

                if isinstance(widget_type, str):
                    try:
                        widget_type = ast.literal_eval(widget_type)
                    except Exception as e:
                        print("Erro ao converter string para lista:", e)

                self.combo.addItems(widget_type)
                typo_dado = 'QComboBox'
                if self.combo.findText('') == -1:
                    if '' not in [self.combo.itemText(i) for i in range(self.combo.count())]:
                        self.combo.addItem('')

            self.stack.addWidget(self.combo)
            self.combo.setEditable(True)
            self.combo.currentTextChanged.connect(self.update_item)

            # Conectar os rádios
            self.radio_campo.toggled.connect(lambda: self.stack.setCurrentIndex(0))
            self.radio_tempo.toggled.connect(lambda: self.stack.setCurrentIndex(1))
            self.radio_data.toggled.connect(lambda: self.stack.setCurrentIndex(2))
            self.radio_data_tempo.toggled.connect(lambda: self.stack.setCurrentIndex(3))
            self.radio_lista.toggled.connect(lambda: self.stack.setCurrentIndex(4))

            # Botões
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
            )
            self.buttons.accepted.connect(self.on_accept)
            self.buttons.rejected.connect(self.on_reject)
            layout.addWidget(self.buttons)

            # Seleciona inicial
            self.set_widget_type(typo_dado)

        def update_item(self):
            current_index = self.combo.currentIndex()
            new_text = self.combo.currentText()

            if current_index >= 0:
                self.combo.setItemText(current_index, new_text)

            # Check if '' is already in the combo
            if self.combo.findText('') == -1:
                if '' not in [self.combo.itemText(i) for i in range(self.combo.count())]:
                    self.combo.addItem('')

                self.combo.setEditable(True)

        def set_widget_type(self, tipo):
            tipo_map = {
                "QLineEdit": (self.radio_campo, 0),
                "QTimeEdit": (self.radio_tempo, 1),
                "QDateEdit": (self.radio_data, 2),
                "QDateTimeEdit": (self.radio_data_tempo, 3),
                "QComboBox": (self.radio_lista, 4)
            }
            if tipo in tipo_map:
                radio, idx = tipo_map[tipo]
                radio.setChecked(True)
                self.stack.setCurrentIndex(idx)

        def on_accept(self):
            tipo, valor = self.get_value()
            self.tipo = tipo
            self.valor = valor
            self.accept()

        def on_reject(self):
            self.rejected.emit()

        def get_value(self):
            if self.radio_campo.isChecked():
                return "CAMPO ABERTO", 'QLineEdit'
            elif self.radio_tempo.isChecked():
                return "TEMPORIZADOR", 'QTimeEdit'
            elif self.radio_data.isChecked():
                return "DATA", 'QDateEdit'
            elif self.radio_data_tempo.isChecked():
                return "DATA COM TEMPO", 'QDateTimeEdit'
            elif self.radio_lista.isChecked():
                resposta = [self.combo.itemText(i) for i in range(self.combo.count()) if
                            self.combo.itemText(i) != '']
                return "LISTA SUSPENSA", resposta
            return "", ""

    class ColumnEditDelegate(QStyledItemDelegate):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.editable_column = -1

        def createEditor(self, parent, option, index):
            if index.column() == self.editable_column:
                return super().createEditor(parent, option, index)
            return None

        def set_editable_column(self, col):
            self.editable_column = col

        def createEditor(self, parent, option, index):
            print(f"Editor aberto na linha {index.row()}, coluna {index.column()}")
            return super().createEditor(parent, option, index)


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

    class CustomHeaderView(QHeaderView):
        def __init__(self, orientation, parent=None, cores=None, mudar_cor_vertical_heider = None):
            super().__init__(orientation, parent)
            self.setSectionsClickable(True)  # Permitir clique no cabeçalho
            self.cores = cores if cores else ["#FFFFFF"] * parent.rowCount()  # Lista de cores inicializada com branco
            self.mudar_cor_vertical_heider = mudar_cor_vertical_heider

        def paintSection(self, painter, rect, logicalIndex):
            """Desenha o cabeçalho com a cor definida"""
            # Define a cor do fundo
            cor = QColor(self.cores[logicalIndex]) if logicalIndex < len(self.cores) else QColor("#FFFFFF")
            painter.fillRect(rect, cor)  # Pinta o fundo

            # Define a cor da caneta
            painter.setPen(QColor("#333333"))

            # Tenta obter o texto do cabeçalho
            try:
                model = self.model()
                if model is None:
                    raise ValueError("Model is None")

                header_text = model.headerData(logicalIndex, self.orientation())
                if header_text is None:
                    header_text = ""

                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(header_text))

            except Exception as e:
                # Em caso de erro, apenas evita desenhar texto e pode logar
                print(f"[paintSection] Erro ao desenhar cabeçalho na seção {logicalIndex}: {e}")

        def mousePressEvent(self, event):
            if event.button() == Qt.MouseButton.RightButton:
                index = self.logicalIndexAt(event.pos())
                self.mudar_cor_vertical_heider(index)
            super().mousePressEvent(event)
    class CustomTableWidget(QTableWidget):
        def __init__(self, dept, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.dept = dept
            self.setup_table()

            self.delegate = AlignedLineEditWithBorderDelegate(target_cells=[(1, 2), (2, 3)], border_color=QColor('blue'))
            self.setItemDelegate(self.delegate)

            self.cellClicked.connect(self.on_cell_click)

            self.installEventFilter(self)
            self.itemSelectionChanged.connect(self.aplicar_negrito_nas_selecionadas)

        def aplicar_negrito_nas_selecionadas(self):
            # Primeiro, reseta todas para normal
            for row in range(self.rowCount()):
                for col in range(self.columnCount()):
                    item = self.item(row, col)
                    if item:
                        fonte = item.font()
                        fonte.setBold(False)
                        item.setFont(fonte)

            # Agora aplica bold nas selecionadas
            for index in self.selectedIndexes():
                item = self.item(index.row(), index.column())
                if item:
                    fonte = item.font()
                    fonte.setBold(True)
                    item.setFont(fonte)

        def eventFilter(self, obj, event):
            if obj == self and event.type() == QtCore.QEvent.Type.KeyPress:
                if event.matches(QtGui.QKeySequence.StandardKey.Copy):
                    self.copy_selection()
                    return True
            return super().eventFilter(obj, event)

        def copy_selection(self):
            selection = self.selectedIndexes()
            if not selection:
                return

            selection.sort(key=lambda x: (x.row(), x.column()))
            current_row = -1
            text = ''
            for index in selection:
                if index.row() != current_row:
                    if current_row != -1:
                        text += '\n'
                    current_row = index.row()
                else:
                    text += '\t'

                item = self.item(index.row(), index.column())
                if item:
                    text += item.text()
                else:
                    text += ''  # Evitar erro se não tiver item

            QtWidgets.QApplication.clipboard().setText(text)

        def setup_table(self):
            for row in range(self.rowCount()):
                self.setCellWidget(row, 0, self.create_checkbox(row))
                for col in range(1, self.columnCount()):
                    self.setItem(row, col, QTableWidgetItem(f"Item {row}, {col}"))

        def create_checkbox(self, row):
            checkbox = QCheckBox()
            checkbox.setStyleSheet(
                "QCheckBox::indicator { width: 20px; height: 20px; margin-left: 10px; }"
            )
            checkbox.setTristate(False)
            return checkbox

        def on_cell_click(self, row, column):
            checkbox = self.cellWidget(row, 0)
            if self.verticalHeaderItem(row)is not None:
                if self.verticalHeaderItem(row).text()!='':
                    if isinstance(checkbox, QCheckBox):
                        checkbox.setChecked(True)  # Sempre marca, nunca desmarca

        def edit(self, index, trigger, event):
            if self.dept == 'PS':
                if index.column() in [10, 11, 12]:
                    return False
            return super().edit(index, trigger, event)

        def set_target_cells(self, cells):
            self.delegate.update_target_cells(cells)  # Update the cells with the border
    class ClickableLabel(QtWidgets.QLabel):
        clicked = QtCore.pyqtSignal()
        def mousePressEvent(self, event):
            self.clicked.emit()

    class CustomTitleBar(QFrame):
        def __init__(self, parent, departamento=None, user=None, nome_user=None,deman= None,janela_CTI_PED= None):
            super().__init__(parent)

            self.parent = parent
            self.janela_CTI_PED = janela_CTI_PED
            self.deman = deman
            self.nome_user = nome_user
            self.user = user
            self.departamento = departamento
            self.setup_ui()
            self.mouse_pos = QPoint(0, 0)
            self.is_dragging = False
            self.grade_aberta = False
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

        def abrir_grade(self, MainWindow):
            self.grade_volta(MainWindow)

        def grade_volta(self,MainWindow):
            self.janela_CTI_PED.hide()
            MainWindow.hide()
            MainWindow.show()
            self.janela_CTI_PED.show()

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
                        background-color: white;
                        border: 1px solid #aaaaaa;
                        border-top-right-radius: 3px;
                        border-bottom-right-radius: 0px;
                        padding: 0px;
                        color: #333333;
                        font-weight: bold;
                    }
                    QPushButton:checked {
                        background-color: white;
                        border-bottom: 1px solid #ffffff;
                        color: #333333;
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
            spacer = QSpacerItem(80, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            self.custom_button1 = self.deman.notificao_label
            self.layout.addItem(spacer)
            spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            self.custom_button = self.deman.label_icone
            self.custom_button2 = self.deman.configura
            self.custom_button3 = self.deman.edicao_menu

            self.layout.addWidget(self.custom_button1)
            self.layout.addWidget(self.custom_button2)
            #self.layout.addWidget(self.custom_button3)
            self.layout.addWidget(self.custom_button)
            # Definir um espaçamento global no layout pode ajudar
            self.layout.setSpacing(5)  # Ajuste conforme necessário

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

            self.data_deman = Ui_data_Demanda()
            self.data_deman.definir_posicao_usuario(self.variavel, self, (None,None), 'DEMANDA')

            self.parent.close()
            self.janela_CTI_PED.close()

        def set_active_tab(self, tab_name):
            """Define qual aba está ativa e atualiza a tela correspondente"""
            self.tab_demanda.setChecked(tab_name == 'DEMANDA')
            self.btn_grade.setChecked(tab_name == 'GRADE')

            # Atualiza a variável que indica a tela atual
            self.parent.t = tab_name

            # Aqui você pode adicionar a lógica para mudar o conteúdo da tela
            # Exemplo:
            if tab_name == 'DEMANDA':
                self.deman.atualiza_tabela_demandas(self.deman.tabela_atual)
            elif tab_name == 'GRADE':
                self.abrir_grade(self.parent)
                self.tab_demanda.setChecked(tab_name == 'DEMANDA')
                self.btn_grade.setChecked(tab_name == 'GRADE')

        def toggle_maximize(self):
            if self.parent.isMaximized():
                self.parent.showNormal()
                self.maximize_button.setText("□")
            else:
                self.deman.maximo()
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

            if current_pos.y() <= screen_geometry.y() + 1:
                self.parent.showMaximized()
                self.maximize_button.setText("❐")
                self.drag_timer.stop()

        def mouseDoubleClickEvent(self, event):
            if event.button() == Qt.MouseButton.LeftButton:
                self.toggle_maximize()
                event.accept()

    class Ui_Demanda(QtWidgets.QMainWindow):
        def maximo(self):
            self.mainwindow.showMaximized()

        def closeEvent(self, event: QCloseEvent):
            print('Saiu')
            self.data_deman = Ui_data_Demanda()
            self.data_deman.definir_posicao_usuario(self.variavel, self, (None,None), 'DEMANDA')
            self.remover_widget()
            self.janela_CTI_PED.close()
            event.accept()

        def setupUi(self, MainWindow, departamento=None, user=None, nome_user=None):

            self.host = '10.36.0.32'
            self.usermysql = 'sglHC2024'
            self.password = 'S4g1L81'
            self.database = 'sgl'

            #Define posição inicial na tabela
            self.posicao_inicial_row = 0
            self.posicao_inicial_colum = 0
            self.selection = None

            #Status das Pop-ups

            self.numero_versao_atual = None
            self.cadastro_Aberta = False
            self.reserva_Aberta = False
            self.procurar_Aberta = False
            self.conta_do_usuario_Aberta = False
            self.config_Aberta = False
            self.indexa_pronto = False
            self.indexa_nome = False
            self.action_filtro= ''
            self.action_alterar= ''
            self.analise_corrent_pos = False
            self.alteracao_nome_widget = False
            self.edicao_ativada = False
            self.manter_alteração_atomatica = True
            self.informacao = False
            self.current_editor = None
            self.current_pos = None
            self.tabela_atual = None
            self.scroll_layout = None
            self.bottom_bar_layout = None
            self.frames = []
            self.lista_user_pos = []
            self.lista_btn = []
            self.lista_dos_btn = []
            self.lista_de_leitos = []
            self.lista_titulo = []
            self.lista_ordem_tabelas = []
            self.lista_ids = []
            self.lista_tooltip_label = []
            self.colunas = []
            self.linha_antiga = []
            self.linha_modificada = []
            self.ordem_colunas = []
            self.status_selecao = []
            self.data_deman = Ui_data_Demanda()
            self.api = Ui_API()
            self.columns = []
            self.ordem_linha = []
            self.lista_modificacao = []
            self.lista_econder = []
            self.lista_prioridade_nir = []

            #Nome do Usuário
            self.nome_user = nome_user

            #Tela atual
            self.t = 'Demanda'

            # Login do usuário
            self.user = user

            #Janela Principal
            self.janela_CTI_PED = QtWidgets.QMainWindow()
            script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
            config_file_path = f'{script_directory}/config.ini'
            self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)

            script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
            cliqu = f'{script_directory}/clicado.ini'
            self.settings_clicado = QSettings(cliqu, QSettings.Format.IniFormat)

            MainWindow.setObjectName('MainWindow')
            MainWindow.showMaximized()
            MainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
            self.variavel = 'tabela_demanda_ps'
            self.clicked = False

            # Define o ícone da janela principal
            icon = QIcon(resource_path('imagens/icone_p_eUO_icon.ico'))
            MainWindow.setWindowIcon(icon)
            self.mainwindow = MainWindow
            self.dept = departamento
            self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
            self.centralwidget.setObjectName('centralwidget')

            #Layout da Tela
            self.centralwidget = QWidget(parent=MainWindow)
            self.centralwidget.setObjectName('centralwidget')
            self.horizontalLayout = QHBoxLayout(self.centralwidget)
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout.setSpacing(0)
            self.horizontalLayout.setObjectName('horizontalLayout')

            # Frame principal da tela
            self.frame = QFrame(parent=self.centralwidget)

            self.tamanho_frame = self.width()
            self.tamanho_frame_h = self.height()

            self.frame.setMouseTracking(True)
            self.horizontalLayout.addWidget(self.frame)
            self.SGL_label = QtWidgets.QLabel()
            self.labeltitulo = QtWidgets.QLabel("Hospital das Clínicas")
            self.ebserh_label = QtWidgets.QLabel("EBSERH")
            self.editbarra = QtWidgets.QLineEdit()
            self.btn_filtros = QtWidgets.QPushButton('▼ Selecione uma Data ')
            self.tabelademan = CustomTableWidget(self.dept)
            self.fixed_columns = ["PRONTUÁRIO", "NPF", "NOME DO PACIENTE", "DATA DE NASCIMENTO",
                                  'STATUS DA SOLICITAÇÃO', 'LEITO RESERVADO', 'DATA E HORA DA RESERVA']

            self.tabelademan.horizontalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            #self.tabelademan.horizontalHeader().customContextMenuRequested.connect(self.header_context_menu)
            self.tabela_edicao = CustomTableWidget(self.dept)

            self.tabela_edicao.horizontalHeader().setSectionsMovable(False)
            self.tabelademan.horizontalHeader().setSectionsMovable(False)

            self.preview = QTableWidget(self.mainwindow)
            self.tabelademan.horizontalHeader().sectionMoved.connect(self.on_section_moved)

            delegate = AlignedLineEditWithBorderDelegate(
                target_cells=[],
                border_color=QColor('white'),
                main_window=self  # <-- passe self aqui
            )
            self.tabela_edicao.setItemDelegate(delegate)

            self.delegate = ColumnEditDelegate(self.tabelademan)
            self.tabelademan.setItemDelegate(self.delegate)

            self.header_colors = ["#FFFFFF"] * self.tabelademan.rowCount()

            # Criar e definir o cabeçalho personalizado
            self.custom_header = CustomHeaderView(Qt.Orientation.Vertical, self.tabelademan, self.header_colors,self.mudar_cor_vertical_heider)
            self.tabelademan.setVerticalHeader(self.custom_header)
            self.tabelademan.verticalHeader().sectionClicked.connect(self.ativar_selecao)

            self.confirmar_new_layout = QtWidgets.QPushButton("CONFIRMAR LAYOUT")
            self.confirmar_alt_layout = QtWidgets.QPushButton("CONFIRMAR LAYOUT")
            self.excluir_tabela = QtWidgets.QPushButton("EXCLUIR TABELA")

            self.excluir_tabela.clicked.connect(self.exluir_layout)
            self.confirmar_alt_layout.clicked.connect(self.sincronizar_colunas)
            self.confirmar_new_layout.clicked.connect(self.criar_layout)

            self.voltar_demandas = QtWidgets.QPushButton()
            self.voltar_demandas.setText("VOLTAR PARA A DEMANDA")

            self.voltar_demandas.clicked.connect(self.voltar)

            self.btnsair = QtWidgets.QPushButton('SAIR' )
            self.btnexclu = QtWidgets.QPushButton('EXCLUIR DEMANDA')
            self.btn_reservar_leito = QtWidgets.QPushButton()
            self.procura_pac = QtWidgets.QPushButton()
            self.deslogar_btn = QtWidgets.QPushButton()
            self.config_layout = QtWidgets.QPushButton()
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


            self.edicao_menu = QMenuBar()
            self.edicao_menu.setFixedWidth(50)
            self.label_icone = ClickableLabel()
            self.icone_toke = None

            self.btn_grade = QtWidgets.QPushButton()
            self.btngraficos = QtWidgets.QPushButton('GRÁFICOS')
            self.btndeman = QtWidgets.QPushButton('SOLICITAÇÃO DE LEITOS')

            from font_demandas import Front_Demanda
            self.front_Demanda = Front_Demanda()
            self.front_Demanda.layout(departamento, self)
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

            self.tabelademan.setObjectName('tabelademan')
            self.tabelademan.setColumnCount(13)
            self.tabelademan.setRowCount(0)
            self.tabelademan.cellClicked.connect(self.tabela_clicada)


            # Ativa as funções para bloquear a atualização da tabela.
            self.barra = self.tabelademan.horizontalScrollBar().value()
            self.barra_vertical = self.tabelademan.verticalScrollBar().value()
            self.tabelademan.horizontalScrollBar().valueChanged.connect(self.on_horizontal_scroll)
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

            width = self.frame.width() - 466
            print(width,self.frame.height(),self.frame.height(),'self.frame.height()luis')
            self.email = QtWidgets.QFrame(self.frame)
            self.email.setFrameShape(QtWidgets.QFrame.Shape.Box)
            self.email.setContentsMargins(0, 80, 0, 0)
            self.email.setStyleSheet(
                'QFrame { background-color: white; border: 1px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
            self.email.setVisible(False)


            self.scrool = QScrollArea(self.email)
            self.scrool.setWidgetResizable(True)
            self.scrool.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: none;')

            icon = QtGui.QIcon(resource_path('imagens/notificacao.ico'))
            pixmap = icon.pixmap(25, 25)
            width = size.width() - 99
            self.notificao_label = ClickableLabel(parent=MainWindow)
            self.notificao_label.setPixmap(pixmap)
            self.notificao_label.setGeometry(QtCore.QRect(width, 15, 25, 25))

            self.content_widget = QWidget()
            self.scrool.setWidget(self.content_widget)
            self.main_layout = QVBoxLayout(self.content_widget)

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

            self.notificao_label.clicked.connect(self.abrir_email)
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
            self.fechar.setStyleSheet(
                '\n                QPushButton {\n                    border: 2px solid #2E3D48;\n                    border-radius: 10px;\n                    background-color: #FFFFFF;\n                    color: #2E3D48;\n                }\n\n                QPushButton:hover {\n                    background-color: #DDDDDD;  /* Change this to your desired hover color */\n                    color: rgb(0, 0, 0);\n                }\n\n                QPushButton:pressed {\n                    background-color: #2E3D48;  /* Change this to your desired pressed color */\n                    color: #FFFFFF;\n                }\n            ')

            linha_frame = QtWidgets.QFrame(self.email)
            linha_frame.setFrameShape(QtWidgets.QFrame.Shape.HLine)
            linha_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
            linha_frame.setStyleSheet('margin: 0; padding: 0; ')
            linha_frame.setGeometry(0, 40, 400, 1)

            self.NOME = QtWidgets.QLabel(login, self.sidebar)
            self.NOME.setFont(font)
            sidebar_layout.addWidget(self.NOME)
            self.NOME.setStyleSheet('border: 2px solid transparent; border-radius: 10px;')
            sidebar_layout.addWidget(self.NOME)

            sidebar_width = 40
            sidebar_x = size.width() - sidebar_width
            sidebar_y = 40
            icon = QtGui.QIcon(resource_path('imagens/user.ico'))
            pixmap = icon.pixmap(40, 40)

            icon = QtGui.QIcon(resource_path('imagens/user.ico'))
            pixmap = icon.pixmap(25, 25)
            self.label_icone.setPixmap(pixmap)
            self.label_icone.setFixedSize( 25, 25)
            self.label_icone.setStyleSheet('border-radius: 10px;')
            self.label_icone.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.label_icone.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
            tooltip_text = user
            self.label_icone.setToolTip(tooltip_text)
            self.label_icone.clicked.connect(self.onIconClick)

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

            self.title_bar = CustomTitleBar(MainWindow, departamento, user, nome_user,self,self.janela_CTI_PED)
            MainWindow.setMenuWidget(self.title_bar)
            buttons = [
                ('GRÁFICOS', self.btngraficos),
                ('PROCURAR PACIENTE', self.procura_pac),
                ('ALTERAR O LAYOUT', self.config_layout),
                ('DESLOGAR', self.deslogar_btn),
                ('SAIR', self.btnsair)
            ]

            for text, btn in buttons:
                btn.setText(text)
                btn.setFixedSize(180, 30)
                btn.setStyleSheet(LAYOUT_BTN)
                sidebar_layout.addWidget(btn)


            if self.dept == 'NIR' or self.dept == 'Administrador':
                buttons = [
                    ('GRÁFICOS', self.btngraficos),
                    ('PROCURAR PACIENTE', self.procura_pac),
                    ('ALTERAR O LAYOUT', self.config_layout),
                    ('DESLOGAR', self.deslogar_btn),
                    ('SAIR', self.btnsair)
                ]

            self.usuario = QtWidgets.QPushButton('USUÁRIO', self.sidebar)
            self.usuario.setFixedSize(180, 30)
            self.usuario.setStyleSheet(LAYOUT_BTN)
            self.usuario.clicked.connect(lambda: self.abrir_conta_do_usuario(MainWindow))
            sidebar_layout.addWidget(self.usuario)

            for text, btn in buttons:
                btn.setText(text)
                btn.setFixedSize(180, 30)
                btn.setStyleSheet(LAYOUT_BTN)
                sidebar_layout.addWidget(btn)



            self.usuario.setGeometry(10, 200, 180, 30)

            self.procura_pac.setGeometry(10, 250, 180, 30)

            self.config_layout.setGeometry(10, 250, 180, 30)
            self.deslogar_btn.setGeometry(10, 250, 180, 30)

            #Tabela alternativa para analise de dados
            self.tabela_alt = QtWidgets.QTableWidget()
            self.tabela_alt2 = QtWidgets.QTableWidget()
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
            self.tabelademan.horizontalHeader().setDefaultSectionSize(140)
            #self.tabelademan.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)

            self.inactivity_timer= QtCore.QTimer()
            self.timer_ps = QtCore.QTimer()
            self.timer_posicao = QtCore.QTimer()
            self.timer_email = QtCore.QTimer()
            self.time_user = QtCore.QTimer()

            #Line edit para pesquisa de pasciente

            self.editbarra.setPlaceholderText('Pesquisar Paciente')
            self.editbarra.textChanged.connect(self.pesquisar)
            icon = QIcon(resource_path('imagens/lupa.ico'))
            self.editbarra.addAction(icon, QtWidgets.QLineEdit.ActionPosition.LeadingPosition)

            font = QtGui.QFont()
            font.setPointSize(15)
            self.labeltitulo.setFont(font)
            self.labeltitulo.setObjectName('labeltitulo')
            self.btndeman.setGeometry(QtCore.QRect(0, 0, 100, 23))
            self.btndeman.setObjectName('btndeman')
            self.btndeman.setStyleSheet('\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }F\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

            self.btngraficos.setObjectName('btngraficos')
            self.btngraficos.setStyleSheet(LAYOUT_BTN)
            self.btnsair.setObjectName('btnsair')
            self.btnsair.clicked.connect(self.finalizar_operacao)
            self.horizontalLayout.addWidget(self.frame)
            MainWindow.setCentralWidget(self.centralwidget)


            self.tabelademan.setCurrentCell(self.tabelademan.rowCount() - 1, 0)
            self.frame.mousePressEvent = lambda event: self.toggle_frame_visibility(self.sidebar)
            _translate = QtCore.QCoreApplication.translate


            if self.dept == 'NIR' or self.dept == 'Administrador':
                self.editable = False

                self.btnexclu.setObjectName('btnexclu')
                self.btnexclu.clicked.connect(self.excluir_demanda)

                self.btn_reservar_leito.setObjectName('btn_reservar_leito')
                self.btn_reservar_leito.setText(_translate('MainWindow', 'RESERVAR LEITO'))
                self.btn_reservar_leito.clicked.connect(lambda: self.reservar_leito(MainWindow))

                self.btn_grade.setObjectName('btn_reservar_leito')
                self.btn_grade.setText(_translate('MainWindow', 'GRADE'))
                self.btn_grade.clicked.connect(lambda: self.abrir_grade(MainWindow))
                print(121)
                self.CTI_PED = Ui_CTI_PED()
                print(2)
                self.CTI_PED.setupUi_grade(self.janela_CTI_PED, self, self.dept, self.user, self.nome_user,
                                           MainWindow)
                print(3)
                self.janela_CTI_PED.show()
                print(4)
                self.frame_personalisa = QtWidgets.QFrame(parent=self.frame)
                self.frame_personalisa.setStyleSheet('\n                                QFrame  {\n                                    background-color: #FFFFFF;\n                                    border-top-right-radius: 20px;\n                                    border-bottom-right-radius: 20px;\n                                    border-left: 1px solid black;\n                                }\n                            ')
                self.frame_personalisa.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
                self.frame_personalisa.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
                self.frame_personalisa.setObjectName('frame_box')
                self.frame_personalisa.hide()


                self.btn_filtros.setFocus()
                self.btnfechar = QtWidgets.QPushButton("X",self.frame)
                self.btnfechar.setStyleSheet('QPushButton {    border-top-right-radius: 0px;    border-bottom-right-radius: 0px;    border-top-left-radius: 10px;    border-bottom-left-radius: 10px;    background-color: #FFFFFF;    color: #2E3D48;    border: 2px solid #2E3D48;}QPushButton:pressed {    background-color: #2E3D48;    color: #FFFFFF;}')

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
                x = self.btn_filtros.width()
                self.btn_personalisa.setGeometry(QtCore.QRect(0, 100, 150, 20))

                self.day = 'ONTEM'
                self.btnfechar.hide()
                self.frame_box.hide()
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

                pos = self.btn_filtros.pos()  # Retorna um QPoint com (x, y)
                # Obter a posição do widget (x0, y0) no canto superior esquerdo
                posicao = self.tabelademan.pos()
                x = posicao.x()
                y = posicao.y()

                self.frame_personalisa.setGeometry(QtCore.QRect(x+150, y, 270, 125))
                self.frame_box.setGeometry(QtCore.QRect(x, y, 150, 125))
                self.btngraficos.setGeometry(QtCore.QRect(210, 0, 100, 23))
                self.btngraficos.clicked.connect(lambda: self.abrir_gráficos(MainWindow))
                #self.retranslateUi_ps(MainWindow)
                self.abrir_tabela(MainWindow,self.lista_ids[0],self.lista_titulo[0],self.lista_dos_btn[0])
                #self.atualiza_tabela_demandas('tabela_demanda_ps')
                self.temporizador(MainWindow)

            elif self.dept == 'Telespectador':
                self.labeltitulo.setGeometry(QtCore.QRect(540, 29, 400, 31))
                self.btngraficos.setGeometry(QtCore.QRect(210, 0, 100, 23))
                self.btnsair.setGeometry(QtCore.QRect(320, 0, 100, 23))

                self.btn_grade.setObjectName('Grade')
                self.btn_grade.setText(_translate('MainWindow', 'GRADE'))
                self.btn_grade.clicked.connect(lambda: self.abrir_grade(MainWindow))

                self.CTI_PED = Ui_CTI_PED()
                self.CTI_PED.setupUi_grade(self.janela_CTI_PED, self, self.dept, self.user, self.nome_user,
                                           MainWindow)
                self.janela_CTI_PED.show()

                self.frame.mousePressEvent = lambda event: self.toggle_frame_visibility(self.sidebar)

                self.frame_personalisa = QtWidgets.QFrame(parent=self.frame)
                self.frame_personalisa.setStyleSheet('\n                                            QFrame  {\n                                                background-color: #FFFFFF;\n                                                border-top-right-radius: 20px;\n                                                border-bottom-right-radius: 20px;\n                                                border-left: 1px solid black;\n                                            }\n                                        ')
                self.frame_personalisa.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
                self.frame_personalisa.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
                self.frame_personalisa.setObjectName('frame_box')
                self.frame_personalisa.hide()

                self.btn_filtros.setFocus()

                self.btnfechar = QtWidgets.QPushButton("X",self.frame)
                self.btnfechar.setStyleSheet('QPushButton {    border-top-right-radius: 0px;    border-bottom-right-radius: 0px;    border-top-left-radius: 10px;    border-bottom-left-radius: 10px;    background-color: #FFFFFF;    color: #2E3D48;    border: 2px solid #2E3D48;}QPushButton:pressed {    background-color: #2E3D48;    color: #FFFFFF;}')
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

                self.sidebar = QtWidgets.QFrame(parent=MainWindow)
                self.sidebar.setGeometry(sidebar_x, sidebar_y, sidebar_width, sidebar_height)

                self.labeltitulo.setGeometry(QtCore.QRect(540, 29, 400, 31))
                self.editbarra.setGeometry(QtCore.QRect(30, 65, 360, 21))

                sizetabela = self.tabelademan.size()
                x = sizetabela.width()
                y = sizetabela.height()
                self.frame_personalisa.setGeometry(QtCore.QRect(x+150, y, 270, 125))
                self.frame_box.setGeometry(QtCore.QRect(x, y, 150, 125))
                self.btngraficos.setGeometry(QtCore.QRect(210, 0, 100, 23))
                self.btngraficos.clicked.connect(lambda: self.abrir_gráficos(MainWindow))

                self.retranslateUi_ps(MainWindow)
                self.abrir_tabela(MainWindow,self.lista_ids[0],self.lista_titulo[0],self.lista_dos_btn[0])

                self.temporizador(MainWindow)
            else:
                for cont, id in enumerate(self.lista_btn):
                    if id == self.dept:
                        self.abrir_tabela(self.mainwindow, self.lista_ids[cont], self.lista_titulo[cont],
                                          self.lista_dos_btn[cont])
                        break
            self.conf_layout()
            self.temporizador(MainWindow)
            if not self.frame_do_grafico.isHidden():
                self.canvas.show()
                self.plot_pie_chart()
                self.timer.stop()
            self.delegate = AlignedLineEditWithBorderDelegate(
                target_cells=[],
                border_color=QColor('white'),
                main_window=self  # <-- passe self aqui
            )

            self.tabelademan.setItemDelegate(delegate)

            for colum in range(self.tabelademan.columnCount()):
                self.tabelademan.setItemDelegateForColumn(colum, delegate)

            self.header_colors = ["#FFFFFF"] * self.tabelademan.rowCount()
            self.configura.clicked.connect(lambda :self.abrir_configuracoes(MainWindow))
            self.procura_pac.clicked.connect(lambda :self.abrir_procura_pac(MainWindow))
            self.deslogar_btn.clicked.connect(lambda :self.deslogar(MainWindow))
            self.config_layout.clicked.connect( self.habilitar_config)
            item = self.tabelademan.item(0, 0)
            self.tabelademan.scrollToItem(item)
            self.procurar_paciente()

        def _mostrar_MENSAGEM_YES_NO(self, texto):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setWindowTitle('Confirmação')
            msg_box.setText(texto)
            icon = QIcon(resource_path('imagens/warning.ico'))
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            reply = msg_box.exec()

            return reply

        def habilitar_config(self):
            if self.edicao_ativada == False:
                resposta = self._mostrar_MENSAGEM_YES_NO('Alterar Layout ?')
                if resposta == QMessageBox.StandardButton.Yes:
                    self.remover_widget()
                    for btn in self.frame.findChildren(QtWidgets.QPushButton):
                        btn.setEnabled(False)
                    self.travar_operacoes()
                    self.edicao_ativada = True
                    self.tabelademan.horizontalHeader().setSectionsMovable(True)

                    header = self.tabelademan.horizontalHeader()
                    header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                    header.customContextMenuRequested.connect(self.header_context_menu)
                    self.tabelademan.horizontalHeader().sectionDoubleClicked.connect(self.change_headers)
                if resposta == QMessageBox.StandardButton.No:
                    return
            else:
                for btn in self.frame.findChildren(QtWidgets.QPushButton):
                    btn.setEnabled(True)

                header = self.tabelademan.horizontalHeader()
                header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                header.customContextMenuRequested.connect(self.header_context_menu)
                self.tabelademan.horizontalHeader().sectionDoubleClicked.disconnect(self.change_headers)
                self.edicao_ativada = False
                self.tabelademan.horizontalHeader().setSectionsMovable(False)
                self.voltar_operacoes()

        def finalizar_operacao(self):
            resposta = self._mostrar_MENSAGEM_YES_NO('Sair do Sistema de Gestão de Leitos ?')
            if resposta == QMessageBox.StandardButton.Yes:
                self.remover_widget()
                self.mainwindow.close()
                self.janela_CTI_PED.close()

        def abrir_items(self):
            if self.frame_box.isHidden():
                #self.action_filtro.setText("▲ Ocultar Filtro")
                #self.btn_filtros.click()
                #self.action_filtro.setVisible(True)
                self.frame_box.show()
                posicao = self.tabelademan.pos()
                x = posicao.x()
                y = posicao.y()
                self.btnfechar.setGeometry(QtCore.QRect(x , y, 20, 20))
                self.frame_personalisa.setGeometry(QtCore.QRect(x + 170, y, 270, 125))
                self.frame_box.setGeometry(QtCore.QRect(x + 20, y, 150, 125))
                return
            self.frame_box.hide()
            if not self.frame_personalisa.isHidden():
                #self.action_filtro.setText("▼ Selecione uma Data")
                self.frame_personalisa.hide()

        def filtros(self, index):

            if index == 1:
                self.day = 'HOJE'
                self.btn_filtros.setText('Hoje')
                self.btnfechar.show()
            elif index == 2:
                self.day = 'SEMANA'
                self.btn_filtros.setText('Ultimos 7 dias')
                self.btnfechar.show()
            elif index == 3:
                self.day = 'MES'
                self.btn_filtros.setText('Ultimos 30 dias')
                self.btnfechar.show()
            elif index == 4:
                self.day = 'ANO'
                current_datetime = QDateTime.currentDateTime()
                formatted_date = current_datetime.toString('yyyy')
                self.btn_filtros.setText(f'{formatted_date}')
                self.btnfechar.show()
            elif index == 5:
                self.day = '2ANO'
                current_datetime = QDateTime.currentDateTime()
                formatted_date = current_datetime.addYears(-1).toString('yyyy')
                self.btn_filtros.setText(f'{formatted_date}')
                self.btnfechar.show()
            elif index == 6:
                self.day = 'PERSONALIZADO'
                self.data_i = self.data_inicio.date()
                self.data_f = self.data_final.date()
                self.btn_filtros.setText('Período personalizado')
                self.btnfechar.show()
            elif index == 0:
                self.day = 'ONTEM'
                self.btn_filtros.setText('▼ Selecione uma Data ')
                self.btn_filtros.setStyleSheet(
                    'QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')
                self.btnfechar.hide()
                self.frame_box.hide()
                if not self.frame_personalisa.isHidden():
                    self.frame_personalisa.hide()
            if self.day != 'ONTEM':
                self.filtrar_data()
                return
            for row in range(self.tabelademan.rowCount()):
                self.tabelademan.showRow(row)
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
                    self.btn_reservar_leito.hide()
                    self.btnexclu.hide()
                self.tabelademan.hide()
                self.editbarra.hide()
                self.canvas.show()
                self.plot_pie_chart()
                self.timer_ps.stop()
                self.icone_toke.hide()
                self.btn_filtros.hide()

                self.SGL_label.hide()
                self.labeltitulo.hide()
                self.ebserh_label.hide()
            else:
                self.frame_do_grafico.hide()
                self.tabelademan.show()
                self.editbarra.show()
                self.btn_filtros.show()
                self.icone_toke.show()
                if self.dept != 'Telespectador':
                    self.btn_reservar_leito.show()
                    self.btnexclu.show()
                self.timer_ps.start()

                self.SGL_label.show()
                self.labeltitulo.show()
                self.ebserh_label.show()

        def plot_pie_chart(self):
            lista = ['ENFERMARIA FEMININA RESERVADA', 'ENFERMARIA FEMININA AGUARDANDO', 'ENFERMARIA MASCULINA RESERVADA', 'ENFERMARIA MASCULINA AGUARDANDO', 'LEITO PEDIÁTRICO RESERVADO', 'LEITO PEDIÁTRICO AGUARDANDO', 'CTI ADULT/UCO RESERVADO', 'CTI ADULT/UCO AGUARDANDO', 'LEITO OBSTETRICO/ MATERNIDADE ', 'ISOLAMENTO CONTATO RESERVADO', 'ISOLAMENTO CONTATO AGUARDANDO', 'ISOLAMENTO RESPIRATÓRIO RESERVADO', 'ISOLAMENTO RESPIRATÓRIO AGUARDANDO', 'APARTAMENTO RESERVADO', 'APARTAMENTO AGUARDANDO', 'CTI PEDIÁTRICO RESERVADO', 'CTI PEDIÁTRICO AGUARDANDO', 'CTI NEONATOLOGIA RESERVADO', 'LEITO VIRTUAL', 'SOLICITAÇÃO CANCELADA', 'ALTA PARA CASA', 'RERSERVADO', 'OCUPADO']
            qt = 0
            self.concluida = 0
            self.nao_concluida = 0
            colum=0
            for colum in range(self.tabelademan.columnCount()):
                item_pac = self.tabelademan.horizontalHeaderItem(colum)
                if item_pac.text() == 'STATUS DA SOLICITAÇÃO':
                    break
            for row in range(self.tabelademan.rowCount()):
                item = self.tabelademan.verticalHeaderItem(row)
                if item is not None and item.text() != '':
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
            cont = self.conta_linha()
            analise = False
            for row in range(cont):
                selec = self.tabelademan.item(row, 0)
                if selec.checkState() == QtCore.Qt.CheckState.Checked:
                    analise = True
            if analise == True:
                colum_leito_atual = 0
                for colum in range(self.tabelademan.columnCount()):
                    item_pac = self.tabelademan.horizontalHeaderItem(colum)
                    if item_pac.text() == 'LEITO ATUAL':
                        colum_leito_atual = colum
                conexao = pymysql.connect(
                    host=self.host,
                    user=self.usermysql,
                    password=self.password,
                    database=self.database
                )
                cursor = conexao.cursor()
                analise = 0
                selecionado = []
                resposta = self._mostrar_MENSAGEM_YES_NO('Confirmar Alta?')
                if resposta == QMessageBox.StandardButton.Yes:
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
                            conexao = pymysql.connect(
                                host=self.host,
                                user=self.usermysql,
                                password=self.password,
                                database=self.database
                            )
                            cursor = conexao.cursor()
                            comando = 'UPDATE alta_cti SET STATUS_DAS_ALTAS = %s, HORARIO_DA_ALTA = %s, DATA_DE_CONFIRMACAO_DA_ALTA = %s WHERE id = %s'
                            valor = (novo_status, formatted_time, formatted_date, pac)
                            cursor.execute(comando, valor)
                            conexao.commit()
                            leito = self.tabelademan.item(row, colum_leito_atual)
                            leito = leito.text().replace(' ', '_')
                            conexao = pymysql.connect(
                                host=self.host,
                                user=self.usermysql,
                                password=self.password,
                                database=self.database
                            )
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

            else:
                self._mostrar_mensagem('Nenhum paciente selecionado!')

        def _mostrar_mensagem(self, texto):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText(texto)
            icon = QIcon(resource_path('imagens/warning.ico'))
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()

        def temporizador(self, MainWindow):
            #self.timer_ps.setInterval(18000)
            self.tabelademan.cellChanged.connect(self.checkboxStateChanged)

            self.timer_posicao.setInterval(500)

            # Desconecta antes de conectar para evitar múltiplas conexões
            try:
                self.timer_posicao.timeout.disconnect()
            except Exception:
                pass
            self.timer_posicao.timeout.connect(self.atualizar_posicao)

            self.timer_email.setInterval(100)
            self.indices = []
            # self.timer_email.timeout.connect(self.adicionar_email)
            # self.timer_email.start()

            if self.dept == 'Administrador':
                self.time_user.setInterval(2000)
                try:
                    self.time_user.timeout.disconnect()
                except Exception:
                    pass
                #self.time_user.timeout.connect(self.aceitar_user)
                self.time_user.start()

            try:
                self.timer_ps.timeout.disconnect()
            except Exception:
                pass
            #self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas(self.variavel))

            #self.timer_ps.start()
            self.timer_posicao.start()
            self.increase_column_width(0, 16)

        def atualiza_tabela_demandas(self, tabela):
            try:
                cell_list = []
                lista_clear = []
                for row in range(self.tabelademan.rowCount()):
                    for col in range(self.tabelademan.columnCount()):
                        lista_clear.append((row, col))
                delegate = AlignedLineEditWithBorderDelegate(
                    target_cells=lista_clear,
                    border_color=QColor('white'),
                    main_window=self
                )
                self.tabelademan.setItemDelegate(delegate)
                if self.current_pos is not None:
                    old_row, old_col = self.current_pos
                    for col in range(self.tabelademan.columnCount()):
                        cell_list.append((old_row, col))

                delegate = AlignedLineEditWithBorderDelegate(
                    target_cells=cell_list,
                    border_color=QColor(0, 100, 0),  # dark green
                    main_window=self
                )
                self.tabelademan.setItemDelegate(delegate)
                delegate = AlignedLineEditWithBorderDelegate(
                    target_cells=self.lista_user_pos,
                    border_color=QColor('purple'),
                    main_window=self
                )
                self.tabelademan.setItemDelegate(delegate)

                for colum in range(self.tabelademan.columnCount()):
                    self.tabelademan.setItemDelegateForColumn(colum, delegate)
                    item_pac = self.tabelademan.horizontalHeaderItem(colum)

                if self.tabelademan.currentItem():
                    self.selection = (self.tabelademan.currentRow(), self.tabelademan.currentColumn())

                self.tabelademan.setEditTriggers(
                    QTableWidget.EditTrigger.DoubleClicked |
                    QTableWidget.EditTrigger.SelectedClicked |
                    QTableWidget.EditTrigger.EditKeyPressed
                )
                lista_leitos = []
                lista_de_ids = []
                leitura = self.data_deman.ler_dabatabase_demandas(self, tabela)

                inicio = False
                if tabela != self.tabela_atual:
                    self.tabelademan.clearContents()
                    self.tabelademan.setRowCount(0)
                    self.tabela_atual = tabela
                    inicio = True
                contador = 0
                if self.tabelademan.rowCount() == 0:
                    inicio = True
                for r,linha in enumerate(leitura):
                    for column, valor in enumerate(linha):
                        if column == 0:
                            contador = int(valor) -1
                            lista_de_ids.append(str(valor))
                            if inicio == True:
                                self.tabelademan.setRowCount(int(valor))

                                item = QtWidgets.QTableWidgetItem('')
                                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                                self.tabelademan.setItem(contador, column, item)
                                item = self.tabelademan.item(contador, column)
                                if item is not None:
                                    fonte = item.font()
                                    fonte.setBold(False)
                                    item.setFont(fonte)

                        item = self.tabelademan.item(contador, column)
                        if item is not None:
                            print(str(valor).upper(),item.text(),'dado fim')
                        if inicio != True:
                            if item is not None:
                                if str(valor).upper()== item.text():
                                    continue

                        if item is not None:
                            print(str(valor).upper(),item.text(), 'saiu')
                        item = QtWidgets.QTableWidgetItem(str(valor).upper())
                        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        if self.current_pos:
                            if self.current_editor:
                                old_row, old_col = self.current_pos
                                if old_row == contador and old_col == column:
                                    continue
                        if column != 0:
                            if item is None or item.text() == 'None' or item.text() == 'NONE':
                                item = QtWidgets.QTableWidgetItem(str(''))
                                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                            self.tabelademan.setItem(contador, column, item)

                        if column == 0:
                            self.tabelademan.setVerticalHeaderItem(contador, item)
                            _translate = QtCore.QCoreApplication.translate
                            self.increase_column_width(0, 16)
                            item_pac = self.tabelademan.verticalHeaderItem(contador)
                            item_pac.setText(_translate('MainWindow', item.text()))
                            pessoa = item.text()
                            pessoa += '_'
                            pessoa += self.variavel
                            lista_leitos.append(pessoa)

                self.posicao_inicial_row = contador
                for row in range(self.tabelademan.rowCount()):
                     if inicio != True and self.tabelademan.verticalHeaderItem(row) is not None :
                         if self.tabelademan.verticalHeaderItem(row).text()!='':
                             for colum in range(self.tabelademan.columnCount()):
                                 if self.tabelademan.item(row, colum) is not None:
                                     if self.tabelademan.item(row, colum).text() != '':
                                         if self.tabelademan.verticalHeaderItem(row).text() not in lista_de_ids:
                                            self.tabelademan.removeRow(row)

                for row in range(self.tabelademan.rowCount()):
                    tem = False
                    for column in range(1, self.tabelademan.columnCount()):
                        item = self.tabelademan.item(row, column)
                        if item is not None:
                            if item.isSelected():
                                tem = True
                                break
                    if tem == True:
                        continue

                    coluna_data_reserva = None
                    for column in range(1, self.tabelademan.columnCount()):
                        header = self.tabelademan.horizontalHeaderItem(column)
                        if header and header.text() == 'DATA E HORA DA RESERVA':
                            coluna_data_reserva = column
                            break

                    if coluna_data_reserva is None:
                        continue

                    item_data_reserva = self.tabelademan.item(row, coluna_data_reserva)
                    data_reserva = ''
                    if item_data_reserva is None:
                        item_data_reserva = QtWidgets.QTableWidgetItem('')
                        item_data_reserva.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        self.tabelademan.setItem(row, coluna_data_reserva, item_data_reserva)
                    else:
                        data_reserva = item_data_reserva.text()

                    current_datetime = QDateTime.currentDateTime()
                    formatted_date = current_datetime.toString('dd/MM/yyyy')
                    data_celula = data_reserva.split()[0] if data_reserva and ' ' in data_reserva else ''

                    self.increase_column_width(0, 16)

                    for column in range(1, self.tabelademan.columnCount()):
                        item = self.tabelademan.item(row, column)
                        if item is None:
                            item = QtWidgets.QTableWidgetItem('')
                            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                            self.tabelademan.setItem(row, column, item)

                        # Pular se o item está selecionado
                        if item.isSelected():
                            continue

                        cor = None

                        if data_reserva == '':
                            cor = QtGui.QColor(255, 255, 255)
                        elif data_celula == formatted_date:
                            cor = QtGui.QColor(31, 73, 125).lighter(140)
                        elif data_celula < formatted_date:
                            cor = QtGui.QColor(255, 148, 74).lighter(140)

                        if cor:
                            item.setBackground(cor)
                            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    # Verificar SIM/NÃO
                    for colum in range(1, self.tabelademan.columnCount()):
                        item = self.tabelademan.item(row, colum)
                        if item is None:
                            item = QtWidgets.QTableWidgetItem('')
                            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                            self.tabelademan.setItem(row, colum, item)

                        # Pular se o item está selecionado
                        if item.isSelected():
                            continue

                        dados = item.text()
                        if dados == 'SIM':
                            cor = QtGui.QColor(0, 255, 127).lighter(140)
                            item.setBackground(cor)
                            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        elif dados == 'NÃO':
                            cor = QtGui.QColor(250, 128, 114).lighter(140)
                            item.setBackground(cor)
                            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                if self.selection:
                    row, col = self.selection
                    self.tabelademan.setCurrentCell(row, col)
                self.atualizar_color_vertical_heider(lista_leitos)
                self.lista_de_leitos = lista_leitos
                self.status_selecao = []
                row = self.posicao_inicial_row
                if row < 300:
                    self.tabelademan.setRowCount(row+300)
                for linha in range(self.posicao_inicial_row+1, self.tabelademan.rowCount()-1):
                    for column in range(1,self.tabelademan.columnCount()):
                        item = QtWidgets.QTableWidgetItem('')
                        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        self.tabelademan.setItem(linha, column, item)

                    header_item = QtWidgets.QTableWidgetItem("")
                    header_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setVerticalHeaderItem(linha, header_item)

                for linha in range( self.tabelademan.rowCount() - 1):
                    self.tabelademan.setRowHeight(linha, 30)
                    if self.preview.isVisible():
                        self.preview.setRowHeight(linha, 30)
                    if self.tabelademan.verticalHeaderItem(linha) is not None:
                        if self.tabelademan.verticalHeaderItem(linha).text() not in lista_de_ids:
                            header_item = QtWidgets.QTableWidgetItem("")
                            header_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                            self.tabelademan.setVerticalHeaderItem(linha, header_item)
                    else:
                        header_item = QtWidgets.QTableWidgetItem("")
                        header_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        self.tabelademan.setVerticalHeaderItem(linha, header_item)
                for row in range(self.tabelademan.rowCount()):
                    header = self.tabelademan.verticalHeaderItem(row)
                    if header is not None and header.text() != '':
                        item = self.tabelademan.item(row, 0)
                        if item is None:
                            item = QtWidgets.QTableWidgetItem()
                            item.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                            item.setCheckState(QtCore.Qt.CheckState.Unchecked)
                            item.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                            self.tabelademan.setItem(row, 0, item)

                        elif item.checkState() != QtCore.Qt.CheckState.Checked:
                            item.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                            item.setCheckState(QtCore.Qt.CheckState.Unchecked)
                            item.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                        else:
                            self.status_selecao.append(row)

                self.copiadora()
                if self.current_pos:
                    if self.current_editor:
                        old_row, old_col = self.current_pos
                        self.atualizar_cor_linha("#D4EDDA", old_row)

                        for j in range(self.tabelademan.columnCount()):
                            delegate = AlignedLineEditWithBorderDelegate(
                                target_cells=[(old_row, j)],
                                border_color=QColor('purple'),
                                main_window=self
                            )
                            self.tabelademan.setItemDelegate(delegate)

                            # Update cells and force repaint

                            delegate.update_target_cells([(old_row, j)])
                            self.tabelademan.viewport().update()
                            item = self.tabelademan.item(old_row, j)
                            if item is not None:
                                fonte = item.font()
                                fonte.setBold(True)
                                fonte.setPointSize(10)
                                item.setFont(fonte)

                                self.tabelademan.setRowHeight(old_row, 35)

                                if self.preview.isVisible():
                                    item = self.preview.item(old_row, j)
                                    if item is not None:
                                        fonte = item.font()
                                        fonte.setBold(True)
                                        fonte.setPointSize(10)
                                        item.setFont(fonte)

                                        self.preview.setRowHeight(old_row, 35)

                        if (self.tabelademan.verticalHeaderItem(old_row) is not None and self.tabelademan.verticalHeaderItem(old_row).text() != ''):
                            item = self.tabelademan.verticalHeaderItem(old_row)
                            fonte = item.font()
                            fonte.setBold(True)
                            fonte.setPointSize(10)
                            item.setFont(fonte)

                if len(self.status_selecao) != 0:
                    for row in self.status_selecao:
                        for j in range(self.tabelademan.columnCount()):
                            item = self.tabelademan.item(row, j)
                            if item is not None:
                                fonte = item.font()
                                fonte.setBold(True)
                                fonte.setPointSize(10)
                                item.setFont(fonte)

                                self.tabelademan.setRowHeight(row, 35)
                            if self.preview.isVisible():
                                item = self.preview.item(old_row, j)
                                if item is not None:
                                    fonte = item.font()
                                    fonte.setBold(True)
                                    fonte.setPointSize(10)
                                    item.setFont(fonte)

                                    self.preview.setRowHeight(old_row, 35)

                        if (self.tabelademan.verticalHeaderItem(
                                row) is not None and self.tabelademan.verticalHeaderItem(row).text() != ''):
                            item = self.tabelademan.verticalHeaderItem(row)
                            fonte = item.font()
                            fonte.setBold(True)
                            fonte.setPointSize(10)
                            item.setFont(fonte)

            except Exception as e:
                print(f"Error: {e}")

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
                import datetime

                for colum in range(self.tabelademan.columnCount()):
                    item_pac = self.tabelademan.horizontalHeaderItem(colum)
                    if item_pac and item_pac.text() in ['DATA E HORA DA SOLICITAÇÃO', 'DATA DA ALTA']:
                        colum_data_da_demanda = colum
                        break

                for row in range(self.tabelademan.rowCount()):
                    item = self.tabelademan.item(row, colum_data_da_demanda)
                    data_celula = ''
                    if item is not None:
                        texto = item.text()
                        try:
                            data_celula = datetime.datetime.strptime(texto, '%d/%m/%Y %H:%M').date()
                        except ValueError:
                            try:
                                data_celula = datetime.datetime.strptime(texto, '%d/%m/%Y').date()
                            except ValueError:
                                data_celula = None
                    if data_celula is None:
                        self.tabelademan.hideRow(row)
                    else:
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
                for analisa_coluna in range(conta_coluna):
                    item = self.tabelademan.item(analisa_linha, analisa_coluna)
                    if item is not None:
                        item_text = item.text()
                        item_copy = QtWidgets.QTableWidgetItem(item_text)
                        self.tabela_alt.setItem(analisa_linha, analisa_coluna, item_copy)
                leitos = self.tabelademan.verticalHeaderItem(analisa_linha)
                if leitos is not None:
                    leitos = QtWidgets.QTableWidgetItem(leitos.text())
                    self.tabela_alt.setVerticalHeaderItem(analisa_linha, leitos)
            for analisa_coluna in range(conta_coluna):
                item = self.tabelademan.horizontalHeaderItem(analisa_coluna)
                if item is not None:
                    item = QtWidgets.QTableWidgetItem(item.text())
                    self.tabela_alt.setHorizontalHeaderItem(analisa_coluna, item)

        def copiadora2(self):
            conta_linha = self.tabelademan.rowCount()
            conta_coluna = self.tabelademan.columnCount()

            self.tabela_alt2.setColumnCount(conta_coluna)
            self.tabela_alt2.setRowCount(conta_linha)

            for analisa_linha in range(conta_linha):
                for analisa_coluna in range(conta_coluna):
                    item = self.tabelademan.item(analisa_linha, analisa_coluna)
                    if item is not None:
                        item_text = item.text()
                        item_copy = QtWidgets.QTableWidgetItem(item_text)
                        self.tabela_alt2.setItem(analisa_linha, analisa_coluna, item_copy)

                header_item = self.tabelademan.verticalHeaderItem(analisa_linha)
                if header_item is not None:
                    header_text = header_item.text()
                    header_copy = QtWidgets.QTableWidgetItem(header_text)
                    self.tabela_alt2.setVerticalHeaderItem(analisa_linha, header_copy)

        def reservar_leito(self, MainWindow):
            cont = self.conta_linha()
            analise = False
            for row in range(cont):
                selec = self.tabelademan.item(row, 0)
                if selec is not None and selec.checkState() == QtCore.Qt.CheckState.Checked:
                    if self.tabelademan.verticalHeaderItem(row) is None or self.tabelademan.verticalHeaderItem(
                            row).text() == '':
                        self._mostrar_mensagem('Demanda Inexistente!')
                        return
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
                self._mostrar_mensagem('Nenhum paciente selecionado!')

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

        def procurar_paciente(self):
            pesquisa = ' '
            if pesquisa != '':
                try:
                    rows = self.data_deman.ler_pacientes_aghu()
                    self.lista_npf = [[] for _ in range(10)]
                    self.lista_prontuario = [[] for _ in range(10)]
                    self.lista_nome = [[] for _ in range(10)]
                    self.lista_data_nascimento = [[] for _ in range(10)]

                    self.lista_npf_nome = [[] for _ in range(26)]
                    self.lista_prontuario_nome = [[] for _ in range(26)]
                    self.lista_nome_nome = [[] for _ in range(26)]
                    self.lista_data_nascimento_nome = [[] for _ in range(26)]
                    self.index_prontuario = {}
                    self.index_nome = {}

                    for row in rows:
                        prontuario = row[1]
                        if prontuario is None:
                            continue

                        nome = row[2]
                        if not nome:
                            continue

                        indice = int(str(prontuario)[0])
                        indice_name_char = nome[0].upper()

                        if 'A' <= indice_name_char <= 'Z':
                            indice_name = ord(indice_name_char) - ord('A')
                        else:
                            continue
                        self.lista_npf[indice].append(row[0])
                        self.lista_prontuario[indice].append(prontuario)
                        self.lista_nome[indice].append(nome)
                        self.lista_data_nascimento[indice].append(row[3])

                        self.lista_npf_nome[indice_name].append(row[0])
                        self.lista_prontuario_nome[indice_name].append(prontuario)
                        self.lista_nome_nome[indice_name].append(nome)
                        self.lista_data_nascimento_nome[indice_name].append(row[3])

                        self.index_prontuario[str(prontuario)] = (indice, len(self.lista_prontuario[indice]) - 1)
                        self.index_nome[str(nome)] = (indice_name, len(self.lista_nome_nome[indice_name]) - 1)

                    # Converte prontuários para strings
                    self.lista_prontuario = [[str(item) for item in sublist] for sublist in self.lista_prontuario]
                    self.lista_nome = [[str(item) for item in sublist] for sublist in self.lista_nome]
                    self.lista_npf = [[str(item) for item in sublist] for sublist in self.lista_npf]
                except Exception as e:

                    print(f"Error: {e}")

        def name_text(self, text, cdata, row,line_edit):
            try:
                if len(text) < 2:
                    return

                primeira_letra = str(text)[0].upper()

                if self.indexa_nome != primeira_letra:
                    self.indexa_nome = primeira_letra
                    idx = ord(primeira_letra) - ord('A')
                    if 0 <= idx < len(self.lista_nome_nome):
                        todos_nomes = self.lista_nome_nome[idx]
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
                if text in self.index_nome:
                    indice, i = self.index_nome[text]
                    prontuario = self.lista_prontuario_nome[indice][i] or 'N/A'
                    npf = self.lista_npf_nome[indice][i] or 'N/A'
                    data_nasc = self.lista_data_nascimento_nome[indice][i]

                    item = QtWidgets.QTableWidgetItem(text)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setItem(row, colum_paciente, QTableWidgetItem(item))

                    item = QtWidgets.QTableWidgetItem(prontuario)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setItem(row, colum_prontuario, QTableWidgetItem(item))

                    item = QtWidgets.QTableWidgetItem(npf)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setItem(row, colum_npf, QTableWidgetItem(item))

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
                    self.tabelademan.setItem(row, cdata, QTableWidgetItem(item))

                    self.current_pos = (row, colum_prontuario)
                    self.aterar_dados_database(prontuario, 'QLineEdit')
                    self.current_pos = (row, colum_npf)
                    self.aterar_dados_database(npf, 'QLineEdit')
                    self.current_pos = (row, cdata)
                    self.aterar_dados_database(datanas, 'QDateEdit')
            except Exception as e:
                print(f"Error: {e}")
        def prontu_text(self, text, cdata, row,line_edit):

            try:
                if self.indexa_pronto != int(str(text)[0]):
                    if len(text) < 2:
                        return
                    self.indexa_pronto = int(str(text)[0])
                    index = self.indexa_pronto
                    if 0 <= index < len(self.lista_prontuario):
                        todos_prontuarios = self.lista_prontuario[index]
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
                if text in self.index_prontuario:
                    indice, i = self.index_prontuario[text]
                    nome = self.lista_nome[indice][i] or 'N/A'
                    npf = self.lista_npf[indice][i] or 'N/A'
                    data_nasc = self.lista_data_nascimento[indice][i]

                    item = QtWidgets.QTableWidgetItem(text)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setItem(row, colum_prontuario, QTableWidgetItem(item))

                    item = QtWidgets.QTableWidgetItem(nome)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setItem(row, colum_paciente, QTableWidgetItem(item))

                    item = QtWidgets.QTableWidgetItem(npf)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setItem(row, colum_npf, QTableWidgetItem(item))

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
                    self.tabelademan.setItem(row, cdata, QTableWidgetItem(item))

                    self.current_pos = (row, colum_paciente)
                    self.aterar_dados_database(nome, 'QLineEdit')
                    self.current_pos = (row, colum_npf)
                    self.aterar_dados_database(npf, 'QLineEdit')
                    self.current_pos = (row, cdata)
                    self.aterar_dados_database(datanas, 'QDateEdit')
            except Exception as e:
                print(f"Error: {e}")

        def conta_linha(self):
            conta_linha = self.tabelademan.rowCount()
            return conta_linha

        def conta_coluna(self):
            conta_coluna = self.tabela_alt.columnCount()
            return conta_coluna

        def tabela_dem(self):
            return self.tabelademan

        def aceitar_user(self):
            self.time_user.stop()

            solicitacoes = []
            users= []
            leitura = self.data_deman.ler_cadastros(self)

            for linha in leitura:
                if len(linha) > 0:
                    if (linha[2] == '0'):

                        usuario = self.api.buscar_usuario(linha[0])
                        solicitacoes.append((linha[1], usuario['email'], linha[3],'0',''))
                        users.append(linha[0])
                    if (linha[2] == '2'):
                        usuario = self.api.buscar_usuario(linha[0])
                        solicitacoes.append((linha[1], usuario['email'], linha[3],'2',linha[4]))
                        users.append(linha[0])

            if len(solicitacoes)>0:
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
                            print(solicitacoes[i][0],users[i])
                            self.data_deman.update_cadastro('1', users[i], solicitacoes[i][2], '')

                        self._mostrar_mensagem('Conta Cadastrada com Sucesso!')
                if reply == QMessageBox.StandardButton.No:
                    return

        def abrir_grade(self, MainWindow):
            self.btn_volta_grade = QtWidgets.QPushButton("GRADE",self.frame)
            self.btn_volta_grade.setStyleSheet(
                '\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        ')

            self.btn_volta_grade.setGeometry(QtCore.QRect(0, 0, 150, 20))
            self.btn_volta_grade.show()

            self.CTI_PED = Ui_CTI_PED()
            self.btn_volta_grade.clicked.connect( self.grade_volta)
            self.CTI_PED.setupUi_grade(self.janela_CTI_PED, self, self.dept, self.user, self.nome_user, MainWindow)
            self.janela_CTI_PED.show()

        def grade_volta(self):
            self.janela_CTI_PED.hide()
            self.janela_CTI_PED.show()

        def is_cell_editable(self,table_widget, row, column):
            item = table_widget.item(row, column)
            if item is None:
                return False
            return bool(item.flags() & Qt.ItemFlag.ItemIsEditable)

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
                if selecao:
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
                    self.timer_posicao.stop()

                    self.numero_versao_atual = None

                    selecionado_copy = selecionado.copy()
                    for row in reversed(selecionado_copy):
                        selecionado.append(row)


                    for row in reversed(selecionado):

                        colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE', None)
                        colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', None)
                        colum_data_nace = self.descobrir_nome_coluna('DATA DE NASCIMENTO', None)

                        pront = self.tabelademan.item(row, colum_prontuario)
                        data = self.tabelademan.item(row, colum_data_nace)
                        nome = self.tabelademan.item(row, colum_paciente)

                        if self.tabelademan.item(row, colum_paciente) is None:
                            nome = ''
                        else:
                            nome = self.tabelademan.item(row, colum_paciente).text()

                        if self.tabelademan.item(row, colum_prontuario) is None:
                            pront = ''
                        else:
                            pront = self.tabelademan.item(row, colum_prontuario).text()

                        if self.tabelademan.item(row, colum_data_nace) is None:
                            data = ''
                        else:
                            data = self.tabelademan.item(row, colum_data_nace).text()

                        valores = self.tabelademan.verticalHeaderItem(row).text()

                        self.data_deman.excluir_na_tabela(self, self.variavel, valores)

                        current_datetime = QDateTime.currentDateTime()
                        formatted_time = current_datetime.toString('hh:mm')

                        #self.tabelademan.removeRow(row)

                        texto_historico = (f'{formatted_time}                {self.nome_user} EXCLUIU A DEMANDA DO PACIENTE \"{nome}\"')
                        alteracao = 'EXCLUIU'
                        print('excl', pront, data, nome, texto_historico,f'{row}' , alteracao)

                        self.data_deman.criar_ou_atualizar_snapshot(self.variavel, self, pront, data, nome, texto_historico,f'{row}' , alteracao)

                    self.timer_posicao.start()
                    self.copiadora()
                    for cont, id in enumerate(self.lista_ids):
                        if id == self.variavel:
                            self.abrir_tabela(self.mainwindow, self.lista_ids[cont], self.lista_titulo[cont],
                                              self.lista_dos_btn[cont])
                            break
                    colum = -100

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
            item.setText(_translate('MainWindow', 'ESPECIALIDADE'))
            item = self.tabelademan.horizontalHeaderItem(7)
            item.setText(_translate('MainWindow', 'OBSERVAÇÃO'))
            item = self.tabelademan.horizontalHeaderItem(8)
            item.setText(_translate('MainWindow', 'TIPO DE LEITO SOLICITADO'))
            item = self.tabelademan.horizontalHeaderItem(9)
            item.setText(_translate('MainWindow', 'MOTIVO DA SOLICITAÇÃO'))
            item = self.tabelademan.horizontalHeaderItem(10)
            item.setText(_translate('MainWindow', 'STATUS DA SOLICITAÇÃO'))
            item = self.tabelademan.horizontalHeaderItem(11)
            item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
            item = self.tabelademan.horizontalHeaderItem(12)
            item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
            if self.dept != 'Telespectador':
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
            item.setText(_translate('MainWindow', 'DATA E HORA DA ALTA'))
            item = self.tabelademan.horizontalHeaderItem(4)
            item.setText(_translate('MainWindow', 'NOME DO PACIENTE'))
            item = self.tabelademan.horizontalHeaderItem(5)
            item.setText(_translate('MainWindow', 'DATA DE NASCIMENTO'))
            item = self.tabelademan.horizontalHeaderItem(6)
            item.setText(_translate('MainWindow', 'SEXO DO PACIENTE'))
            item = self.tabelademan.horizontalHeaderItem(7)
            item.setText(_translate('MainWindow', 'ESPECIALIDADE MÉDICA'))
            item = self.tabelademan.horizontalHeaderItem(8)
            item.setText(_translate('MainWindow', 'NECESSIDADES ESPECÍFICAS'))
            item = self.tabelademan.horizontalHeaderItem(9)
            item.setText(_translate('MainWindow', 'UNIDADE DE INTERNAÇÃO ATUAL'))
            item = self.tabelademan.horizontalHeaderItem(10)
            item.setText(_translate('MainWindow', 'STATUS DAS ALTAS'))
            item = self.tabelademan.horizontalHeaderItem(11)
            item.setText(_translate('MainWindow', 'DATA DE CONFIRMAÇÃO DA ALTA'))
            item = self.tabelademan.horizontalHeaderItem(12)
            item.setText(_translate('MainWindow', 'HORÁRIO DE CONFIRMAÇÃO DA ALTA'))
            item = self.tabelademan.horizontalHeaderItem(13)
            item.setText(_translate('MainWindow', 'LEITO ATUAL'))
            item = self.tabelademan.horizontalHeaderItem(14)
            item.setText(_translate('MainWindow', 'STATUS DA SOLICITAÇÃO'))
            item = self.tabelademan.horizontalHeaderItem(15)
            item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
            item = self.tabelademan.horizontalHeaderItem(16)
            item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
            item = self.tabelademan.horizontalHeaderItem(17)
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
            item.setText(_translate('MainWindow', 'HORARIO DA CHEGADA DO PACIENTE'))
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
            item.setText(_translate('MainWindow', 'MÉDICO RESPONSÁVEL E CONTATO'))
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
            item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
            item = self.tabelademan.horizontalHeaderItem(17)
            item.setText(_translate('MainWindow', 'MOTIVO DO CANCELAMENTO'))
            item = self.tabelademan.horizontalHeaderItem(18)
            item.setText(_translate('MainWindow', 'PRÉ INTERNAÇÃO REALIZADA?'))
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
            item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
            item = self.tabelademan.horizontalHeaderItem(16)
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
            item.setText(_translate('MainWindow', 'HORÁRIO DE CHEGADA DA INTERNAÇÃO'))
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
            item.setText(_translate('MainWindow', 'AUTORIZADOR'))
            item = self.tabelademan.horizontalHeaderItem(15)
            item.setText(_translate('MainWindow', 'PRÉ INTERNAÇÃO REALIZADA?'))
            item = self.tabelademan.horizontalHeaderItem(16)
            item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
            item = self.tabelademan.horizontalHeaderItem(17)
            item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
            self.labeltitulo.setText(_translate('MainWindow', 'SOLICITAÇÃO DE LEITOS INTERNAÇÕES E TRANSF. EXTERNAS'))
            for colum in range(1, self.tabelademan.columnCount()):
                item_pac = self.tabelademan.horizontalHeaderItem(colum).text()
                text_width = self.fontMetrics().boundingRect(item_pac).width()
                self.increase_column_width(colum, text_width + 100)
        def retranslateUi_endoscopia(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            item = self.tabelademan.horizontalHeaderItem(0)
            item.setText(_translate('MainWindow', ' '))
            self.increase_column_width(0, 5)
            item = self.tabelademan.horizontalHeaderItem(1)
            item.setText(_translate('MainWindow', 'PRONTUÁRIO'))
            item = self.tabelademan.horizontalHeaderItem(2)
            item.setText(_translate('MainWindow', 'NPF'))
            item = self.tabelademan.horizontalHeaderItem(3)
            item.setText(_translate('MainWindow', 'DATA E HORA DO PROCEDIMENTO'))
            item = self.tabelademan.horizontalHeaderItem(4)
            item.setText(_translate('MainWindow', 'HORÁRIO DE CHEGADA DO PACIENTE NA URA'))
            item = self.tabelademan.horizontalHeaderItem(5)
            item.setText(_translate('MainWindow', 'NOME DO PACIENTE'))
            item = self.tabelademan.horizontalHeaderItem(6)
            item.setText(_translate('MainWindow', 'DATA DE NASCIMENTO'))
            item = self.tabelademan.horizontalHeaderItem(7)
            item.setText(_translate('MainWindow', 'ORIGEM DO PACIENTE'))
            item = self.tabelademan.horizontalHeaderItem(8)
            item.setText(_translate('MainWindow', 'CLÍNICA'))
            item = self.tabelademan.horizontalHeaderItem(9)
            item.setText(_translate('MainWindow', 'PROCEDIMENTO'))
            item = self.tabelademan.horizontalHeaderItem(10)
            item.setText(_translate('MainWindow', 'MÉDICO RESPONSÁVEL'))
            item = self.tabelademan.horizontalHeaderItem(11)
            item.setText(_translate('MainWindow', 'TIPO DE LEITO SOLICITADO'))
            item = self.tabelademan.horizontalHeaderItem(12)
            item.setText(_translate('MainWindow', 'PRIORIDADE'))
            item = self.tabelademan.horizontalHeaderItem(13)
            item.setText(_translate('MainWindow', 'STATUS DA SOLICITAÇÃO'))
            item = self.tabelademan.horizontalHeaderItem(14)
            item.setText(_translate('MainWindow', 'CIRURGIA LIBERADA PARA ENTRAR?'))
            item = self.tabelademan.horizontalHeaderItem(15)
            item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
            item = self.tabelademan.horizontalHeaderItem(16)
            item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
            item = self.tabelademan.horizontalHeaderItem(17)
            item.setText(_translate('MainWindow', 'MOTIVO DO CANCELAMENTO'))
            self.labeltitulo.setText(_translate('MainWindow', 'SOLICITAÇÃO DE LEITOS ENDOSCOPIA'))
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
            item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
            item = self.tabelademan.horizontalHeaderItem(10)
            item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
            item = self.tabelademan.horizontalHeaderItem(11)
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
            item.setText(_translate('MainWindow', 'DATA E HORÁRIO DE CHEGADA NA INTERNAÇÃO'))
            item = self.tabelademan.horizontalHeaderItem(10)
            item.setText(_translate('MainWindow', 'CLÍNICA'))
            item = self.tabelademan.horizontalHeaderItem(11)
            item.setText(_translate('MainWindow', 'PROCEDIMENTO'))
            item = self.tabelademan.horizontalHeaderItem(12)
            item.setText(_translate('MainWindow', 'TIPO DE LEITO SOLICITADO'))
            item = self.tabelademan.horizontalHeaderItem(13)
            item.setText(_translate('MainWindow', 'NOME E CONTATO DO SOLICITANTE'))
            item = self.tabelademan.horizontalHeaderItem(14)
            item.setText(_translate('MainWindow', 'STATUS DA SOLICITAÇÃO'))
            item = self.tabelademan.horizontalHeaderItem(15)
            item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
            item = self.tabelademan.horizontalHeaderItem(16)
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
        def modificao(self, row, col):
            self.antigo = ''
            self.copiadora2()
            current_datetime = QDateTime.currentDateTime()
            formatted_time = current_datetime.toString('hh:mm')

            NOME = ''

            colum_paciente = 4
            colum_prontuario = 1

            colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE', colum_paciente)
            colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', colum_prontuario)

            NOME = self.tabela_alt2.item(row, colum_paciente)
            texto = ''
            if col == -100:
                texto = (f'{formatted_time}                {self.nome_user} EXCLUIU A DEMANDA DO PACIENTE \"{NOME.text()}\"')
            else:
                item = self.tabela_alt2.item(row, col)
                item2 = self.tabela_alt.item(row, col)
                heider = self.tabela_alt.verticalHeaderItem(row)
                if item is not None and item2 is not None and item.text()!= item2.text():
                    col_label = self.tabela_alt.horizontalHeaderItem(col).text()
                    texto = f'{formatted_time}                {self.nome_user} ALTEROU O \"{col_label}\" DE \"{item2.text()}\" PARA \"{item.text()}\" NO PACIENTE \"{NOME.text()}\"'
            if texto!= self.antigo and texto != '':
                self.lista_modificacao.append(texto)
                self.antigo = texto
                for col in range(1,self.tabelademan.columnCount()):
                    coluna = self.tabelademan.horizontalHeaderItem(col)

                    item = self.tabela_alt2.item(row, col)
                    item2 = self.tabela_alt.item(row, col)

                    self.colunas.append(coluna)
                    if item is not None:
                        self.linha_modificada.append(item.text())
                    if item2 is not None:
                        self.linha_antiga.append(item2.text())

        def moficacao_inserir(self, row, col):
            self.antigo = ''
            self.copiadora2()
            current_datetime = QDateTime.currentDateTime()
            formatted_time = current_datetime.toString('hh:mm')

            NOME = ''

            colum_paciente = 4
            colum_prontuario = 1

            colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE', colum_paciente)
            colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', colum_prontuario)

            NOME = self.tabela_alt2.item(row, colum_paciente)


            texto = (f'{formatted_time}                {self.nome_user} INSERIU A DEMANDA DO PACIENTE \"{NOME.text()}\"')

            if texto!= self.antigo:
                self.lista_modificacao.append(texto)
                self.antigo = texto
                for col in range(self.tabelademan.columnCount()):
                    coluna = self.tabelademan.horizontalHeaderItem(col)
                    self.colunas.append(coluna)

                    item = self.tabela_alt2.item(row, colum_paciente)
                    if item is not None:
                        self.linha_modificada.append(item.text())

        def abrir_configuracoes(self, Form):
            self.sidebar.close()
            self.timer_ps.stop()
            self.label_icone.setStyleSheet('border-radius: 10px;')

            if self.config_Aberta == True:
                self.janela_config.close()
                self.timer_ps.start()
                self.config_Aberta = False
            else:
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
                if item2 is not None and item2 !='':
                    if item is not None:
                        if nome.lower() in item.text().lower() or nome.lower() in item2.text().lower():
                            self.tabelademan.showRow(row)
                        else:
                            self.tabelademan.hideRow(row)

            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                btn.setEnabled(True)

        def retornar_main_window(self):
            return self.mainwindow

        def toggle_frame_visibility(self, sidebar):
            self.remover_widget()


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
            if col > 0:
                self.delegate.set_editable_column(col)
                self.tabelademan.editItem(self.tabelademan.item(row, col))
                self.colocar_widget(row, col)


        def on_horizontal_scroll(self, value):

            self.ativar_shadow(value)
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

        def check_scrollbar_value(self,value):
            self.preview.verticalScrollBar().setValue(value)
            if self.tabelademan.verticalScrollBar().value() != self.barra_vertical:

                #self.remover_widget()

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
                backcolocor = '#C0C0C0'
                color = 'Black'
                tamanho = 12
                font_name = 'Segoe UI'
            self.backcolocor = backcolocor
            self.color = color
            self.font = font_name
            self.tamanho = tamanho
            for label in self.frame.findChildren(QtWidgets.QLabel):
                if label != self.SGL_label and label!= self.ebserh_label:
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
            self.conf_layout()

        def abrir_email(self):
            self.clicked = not self.clicked
            if self.clicked:
                print('abrir_email')
                self.barra = self.tabelademan.horizontalScrollBar().value()
                self.barra_vertical = self.tabelademan.verticalScrollBar().value()
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
            for texto,id in data:
                frame = QPushButton(texto)
                frame.setContentsMargins(0, 80, 0, 0)
                if not self.settings.value(f'clicados/{texto}', False, type=bool):
                    frame.setStyleSheet("QPushButton { background-color: white;font-weight: bold; border: 2px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; text-align: left; padding-left: 10px;}")
                    icon = QIcon(resource_path('imagens/novo-email.ico'))
                    frame.setIcon(icon)
                else:
                    frame.setStyleSheet(
                        "QPushButton { background-color: white; border: 2px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; text-align: left; padding-left: 10px;}")
                frame.setFixedSize(370, 50)
                frame.clicked.connect(lambda _, user = id,text=texto, btn=frame: self.clicar_botao(text, btn,user))
                self.main_layout.addWidget(frame)
                self.frames.append(frame)

        def clicar_botao(self, texto, botao,user):
            if not self.settings_clicado.value(f'clicados/{texto}', False, type=bool):
                self.settings_clicado.setValue(f'clicados/{texto}', True)
                botao.setStyleSheet(
                    "QPushButton { background-color: white; border: 2px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; text-align: left; padding-left: 10px;}")

            self.abrir_notificao(texto,user)

        def abrir_notificao(self, text,user):
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
            btnfechar.clicked.connect(self.fechar_correio )

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

        def mudar_cor_vertical_heider(self, index):
            color = QColorDialog.getColor()
            if color.isValid():
                color_name = color.name()
                self.header_colors[index] = color.name()
                self.custom_header.cores = self.header_colors
                self.custom_header.viewport().update()

                conexao = pymysql.connect(
                    host=self.host,
                    user=self.usermysql,
                    password=self.password,
                    database=self.database
                )
                cursor = conexao.cursor()

                leitos = self.tabelademan.verticalHeaderItem(index)
                LEITOS = leitos.text()
                LEITOS = LEITOS.replace(' ', '_')
                LEITOS += '_'
                LEITOS += self.variavel
                nome_mysql = self.normalizar_nome_mysql(LEITOS)
                # Verifica se o leito já existe na tabela
                cursor.execute('SELECT leito FROM color_table_demandas WHERE leito = %s', (nome_mysql,))
                resultado = cursor.fetchone()

                if resultado:
                    # Se o leito existir, atualiza a cor
                    comando = 'UPDATE color_table_demandas SET cor = %s WHERE leito = %s'
                else:
                    # Se o leito não existir, insere um novo registro
                    comando = 'INSERT INTO color_table_demandas (cor, leito) VALUES (%s, %s)'

                valores = (color_name, nome_mysql)  # Usa a cor no formato hexadecimal
                cursor.execute(comando, valores)
                conexao.commit()
                cursor.close()
                conexao.close()

        def atualizar_color_vertical_heider(self, lista_leitos):
            if len(lista_leitos) > 0:
                conexao = None
                cursor = None
                try:
                    self.header_colors = ["#FFFFFF"] * self.tabelademan.rowCount()
                    conexao = pymysql.connect(
                        host=self.host,
                        user=self.usermysql,
                        password=self.password,
                        database=self.database,
                        charset='utf8mb4'
                    )
                    cursor = conexao.cursor()

                    leitos_str = ', '.join([f'"{self.normalizar_nome_mysql(leito)}"' for leito in lista_leitos])

                    # Executa a consulta
                    comando = f'SELECT * FROM color_table_demandas WHERE leito IN ({leitos_str})'
                    cursor.execute(comando)
                    leitura = cursor.fetchall()

                    # Itera sobre os resultados da consulta
                    for linha in leitura:
                        leito_db = linha[0].decode() if isinstance(linha[0], (bytes, bytearray)) else linha[0]  # Valor do leito no banco de dados
                        cor = linha[1].decode() if isinstance(linha[1], (bytes, bytearray)) else linha[1]
                        # Itera sobre as linhas do cabeçalho vertical da tabela
                        for linha_analisa in range(self.tabelademan.rowCount()):
                            leitos = self.tabelademan.verticalHeaderItem(linha_analisa)
                            if leitos is not None:
                                LEITOS = leito_db.replace(f'_{self.normalizar_nome_mysql(self.variavel)}', '')

                                if LEITOS == leitos.text():
                                    if cor == '#550000':
                                        self.tabelademan.setRowHidden(linha_analisa, True)
                                    else:
                                        self.atualizar_cor_linha(cor,linha_analisa)
                finally:
                    if cursor:
                        cursor.close()
                    if conexao:
                        conexao.close()

        def atualizar_cor_linha(self,cor,linha_analisa):
            self.header_colors[linha_analisa] = cor
            for coluna in range(self.tabelademan.columnCount()):
                item = self.tabelademan.item(linha_analisa, coluna)
                if item is None:
                    item = QTableWidgetItem()
                    self.tabelademan.setItem(linha_analisa, coluna, item)
                item.setBackground(QBrush(QColor(cor)))
            self.custom_header.cores = self.header_colors  # Aplica as novas cores ao cabeçalho
            self.custom_header.viewport().update()
        def analisar_widget(self, row, colum, colum_data_nace):

            widget = self.tabelademan.cellWidget(row, colum)
            valor_para_atualizar = ''
            item = self.tabelademan.item(row, colum)
            if item is not None:
                valor_para_atualizar = item.text()
            else:
                valor_para_atualizar = ''

            if isinstance(widget, QComboBox):
                combo_box = self.tabelademan.cellWidget(row, colum)
                valor_para_atualizar = combo_box.currentText()
            elif isinstance(widget, QtWidgets.QTimeEdit):
                time_edit = self.tabelademan.cellWidget(row, colum)
                valor_para_atualizar = time_edit.time().toString(
                    "HH:mm:ss")  # Captura a hora no formato desejado
                if valor_para_atualizar == "01/01/2000 00:00" or valor_para_atualizar == "00:00" or valor_para_atualizar == "01/01/2000" or valor_para_atualizar == "00:00:00":
                    valor_para_atualizar = ''
            elif isinstance(widget, QtWidgets.QDateTimeEdit):
                datetime_edit = self.tabelademan.cellWidget(row, colum)
                valor_para_atualizar = datetime_edit.dateTime().toString(
                        "dd/MM/yyyy HH:mm")
                if valor_para_atualizar == "01/01/2000 00:00" or valor_para_atualizar == "00:00" or valor_para_atualizar == "01/01/2000" or valor_para_atualizar == "00:00:00":
                    valor_para_atualizar = ''
            elif isinstance(widget, QtWidgets.QLineEdit):
                lineedit = self.tabelademan.cellWidget(row, colum)
                valor_para_atualizar = lineedit.text()
            if (colum == colum_data_nace and colum_data_nace != 0):
                datetime_edit = self.tabelademan.cellWidget(row, colum)
                if datetime_edit is not None:
                    valor_para_atualizar = datetime_edit.date().toString("dd/MM/yyyy")
                    if valor_para_atualizar == "01/01/2000":
                        valor_para_atualizar = ''
                else:
                    valor_para_atualizar = ''
            return valor_para_atualizar
        def ativar_selecao(self, row):

            item = self.tabelademan.item(row, 0)  # Pegamos a checkbox que está na coluna 0
            linhas = self.tabelademan.rowCount()
            colunas = self.tabelademan.columnCount()
            if item is not None:
                # Alterna entre marcado e desmarcado
                if item.checkState() == Qt.CheckState.Checked:
                    item.setCheckState(Qt.CheckState.Unchecked)
                    self.status_selecao.remove(row)

                else:
                    item.setCheckState(Qt.CheckState.Checked)
                    item = self.tabelademan.verticalHeaderItem(row)
                    fonte = item.font()
                    fonte.setBold(True)
                    fonte.setPointSize(10)
                    item.setFont(fonte)

                    for j in range(colunas):
                        item = self.tabelademan.item(row, j)
                        if item is not None:
                            fonte = item.font()
                            fonte.setBold(True)
                            item.setFont(fonte)
                    self.tabelademan.setRowHeight(row, 35)
                    self.status_selecao.append(row)
        def abrir_tabela(self, MainWindow, demanda, titulo, btn):
            self.labeltitulo.setText(titulo)
            self.variavel = demanda

            # Definição dos estilos
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

            if self.dept == 'NIR' or self.dept == 'Administrador':
                self.alterar_cor_tela()
            self.btn_atual = btn
            self.quantidade_colunas = 0
            self.lista_nomes_das_colunas = []
            self.lista_widgets = []

            self.data_deman.ler_colunas_demanda(self, demanda)
            self.data_deman.ler_Widgets_deman(self, demanda)

            self.tabelademan.setColumnCount(self.quantidade_colunas+1)

            self.ordem_original_colunas = []
            self.colunas_visuais_atuais = []
            for col in range(self.tabelademan.columnCount()):
                item = QtWidgets.QTableWidgetItem()
                font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
                font.setPointSize(8)
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                self.tabelademan.setHorizontalHeaderItem(col, item)

                if col == 0:
                    continue
                if col == 1:
                    column_field = 'col'
                else:
                    column_field = f'col{col - 1}'
                self.ordem_original_colunas.append(column_field)
                self.colunas_visuais_atuais.append(column_field)

            self.retranslateUi(MainWindow)
            self.atualiza_tabela_demandas(demanda)
            if not self.frame_do_grafico.isHidden():
                self.canvas.show()
                self.plot_pie_chart()
                self.timer.stop()
            self.inserir_linha()

            if len(self.lista_tooltip_label) > 0:
                for usue, tool, line_edit in self.lista_tooltip_label:
                    if tool:
                        tool.deleteLater()
                    if line_edit:
                        line_edit.deleteLater()
            self.lista_tooltip_label = []
            self.remover_widget()

        def inserir_linha(self):
            colum_paciente = 4
            colum_prontuario = 1

            colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE', colum_paciente)
            colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', colum_prontuario)

            row = self.tabelademan.rowCount() - 1
            conta_linha = self.tabelademan.rowCount()

            if self.tabelademan.item(row, colum_prontuario) is None:
                item = QtWidgets.QTableWidgetItem(str(''))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabelademan.setItem(row, colum_prontuario, item)

            if self.tabelademan.item( row, colum_paciente) is None:
                item = QtWidgets.QTableWidgetItem(str(''))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabelademan.setItem(row, colum_paciente, item)

            id = QtWidgets.QTableWidgetItem('')
            self.tabelademan.setVerticalHeaderItem(row, id)
            if self.tabelademan.rowCount() > 0 and self.tabelademan.item(row, colum_prontuario).text() != '' or self.tabelademan.item( row, colum_paciente).text() != '':

                self.tabelademan.insertRow(conta_linha)
                item = QtWidgets.QTableWidgetItem(str(conta_linha + 1))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabelademan.setVerticalHeaderItem(conta_linha, item)
                _translate = QtCore.QCoreApplication.translate
                self.increase_column_width(0, 16)
                item_pac = self.tabelademan.verticalHeaderItem(conta_linha)
                #item_pac.setText(_translate('MainWindow', item.text()))

                excel_color = QtGui.QColor(255, 255, 255)
                adjusted_color = excel_color.lighter(100)
                self.tabelademan.verticalHeaderItem(row)
                for colum in range(self.tabelademan.columnCount()):
                    item = QtWidgets.QTableWidgetItem(str(''))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setItem(conta_linha, colum, item)
                if (self.tabelademan.verticalHeaderItem(row) is not None and self.tabelademan.verticalHeaderItem(
                        row).text() != ''):

                    selecao = QtWidgets.QTableWidgetItem()
                    selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                    selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
                    selecao.setBackground(QtGui.QBrush(adjusted_color))
                    #self.tabelademan.setItem(row, 0, selecao)

            elif self.tabelademan.rowCount() == 0:
                self.tabelademan.insertRow(conta_linha)
                item = QtWidgets.QTableWidgetItem(str(conta_linha + 1))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabelademan.setVerticalHeaderItem(conta_linha, item)
                _translate = QtCore.QCoreApplication.translate
                self.increase_column_width(0, 16)
                item_pac = self.tabelademan.verticalHeaderItem(conta_linha)
                item_pac.setText(_translate('MainWindow', item.text()))

                excel_color = QtGui.QColor(255, 255, 255)
                adjusted_color = excel_color.lighter(100)

                for colum in range(self.tabelademan.columnCount()):
                    item = QtWidgets.QTableWidgetItem(str(''))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tabelademan.setItem(conta_linha, colum, item)

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate('MainWindow', 'Sistema de Gestão de Leitos'))
            self.increase_column_width(0, 5)
            item = self.tabelademan.horizontalHeaderItem(0)
            item.setText(_translate('MainWindow', ' '))

            self.nomes_colunas = {}
            self.widgets_colunas = {}

            for idx in range(1, self.tabelademan.columnCount()):
                if idx == 1:
                    column_field = 'col'
                else:
                    column_field = f'col{idx - 1}'

                nome = self.lista_nomes_das_colunas[idx - 1]
                widg = self.lista_widgets[idx ]

                self.nomes_colunas[column_field] = nome
                self.widgets_colunas[column_field] = widg


                item = self.tabelademan.horizontalHeaderItem(idx)
                item.setText(_translate('MainWindow', nome))
                hide, priority = self.data_deman.descobrir_escondidos(self, self.variavel, nome)
                if hide == 'TRUE':
                    self.tabelademan.hideColumn(idx)
            self.btndeman.setText(_translate('MainWindow', 'DEMANDA'))
            self.btngraficos.setText(_translate('MainWindow', 'GRÁFICOS'))
            self.btnsair.setText(_translate('MainWindow', 'SAIR'))
            for colum in range(1, self.tabelademan.columnCount()):
                item_pac = self.tabelademan.horizontalHeaderItem(colum).text()
                text_width = self.fontMetrics().boundingRect(item_pac).width()
                self.increase_column_width(colum, text_width + 100)

        def tabela_clicada(self, row, column):


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
            if column != 0:
                self.remover_widget()
                self.colocar_widget(row, column)

            linhas = self.tabelademan.rowCount()
            colunas = self.tabelademan.columnCount()

            for i in range(linhas):
                for j in range(colunas):
                    item = self.tabelademan.item(i, j)
                    if item is not None:
                        fonte = item.font()
                        fonte.setBold(False)
                        item.setFont(fonte)
                    if self.preview.isVisible():
                        item = self.preview.item(i, j)
                        if item is not None:
                            fonte = item.font()
                            fonte.setBold(False)
                            item.setFont(fonte)

                        self.preview.setRowHeight(i, 30)

                    self.tabelademan.setRowHeight(i, 30)

            for j in range(colunas):
                item = self.tabelademan.item(row, j)
                if item is not None:
                    fonte = item.font()
                    fonte.setBold(True)
                    item.setFont(fonte)
                if self.preview.isVisible():
                    item = self.preview.item(row, j)
                    if item is not None:
                        fonte = item.font()
                        fonte.setBold(True)
                        fonte.setPointSize(10)
                        item.setFont(fonte)

                    self.preview.setRowHeight(row, 35)

                self.tabelademan.setRowHeight(row, 35)


            widget = self.tabelademan.cellWidget(row, column)

        def iniciar_timer_inatividade(self, timeout_ms=15000):
            if self.inactivity_timer is not None:
                self.inactivity_timer.stop()

            self.inactivity_timer.setSingleShot(True)
            self.inactivity_timer.timeout.connect(self.remover_widget)
            self.inactivity_timer.start(timeout_ms)

        def colocar_widget(self, row, column):
            self.remover_widget()
            self.numero_versao_atual = None
            if self.edicao_ativada:
                return
            for col in range(self.tabelademan.columnCount()):
                self.atualizar_cor_linha("#D4EDDA", row)

            self.current_pos = (row, column)
            item_pac = self.tabelademan.horizontalHeaderItem(column).text()
            hide, priority = self.data_deman.descobrir_escondidos(self, self.variavel, item_pac)
            if priority == 'TRUE' and self.dept != 'NIR':
                return
            widget = self.lista_widgets[column]

            if (self.tabelademan.verticalHeaderItem(row) is not None and self.tabelademan.verticalHeaderItem(
                    row).text() != ''):
                item = self.tabelademan.verticalHeaderItem(row)
                fonte = item.font()
                fonte.setBold(True)
                fonte.setPointSize(10)
                item.setFont(fonte)
            self.tabelademan.setRowHeight(row, 35)

            if widget == 'QDateEdit':
                item = self.tabelademan.item(row, column)
                if item is not None:
                    if self.is_cell_editable(self.tabelademan, row, column):
                        dado = item.text()

                        qtwidget = QtWidgets.QDateEdit()
                        bg_color = item.background().color().name()
                        if bg_color == '#000000':
                            bg_color = 'white'

                        qtwidget.setStyleSheet(f' background-color: {bg_color};')
                        qtwidget.setFixedSize(self.tabelademan.columnWidth(column), self.tabelademan.rowHeight(row))
                        qtwidget.setCalendarPopup(True)
                        qtwidget.setDate(QDate.fromString(dado, 'dd/MM/yyyy'))

                        qtwidget.setStyleSheet(f"""
                                              background-color: {bg_color};
                                              font-weight: bold;
                                              font-size: 10pt;
                                              qproperty-alignment: AlignCenter;
                                              """)
                        qtwidget.setAlignment(Qt.AlignmentFlag.AlignCenter)

                        self.key_filter = KeyFilter(self.on_tab_pressed)
                        qtwidget.installEventFilter(self.key_filter)

                        self.tabelademan.setCellWidget(row, column, qtwidget)
                        self.current_editor = qtwidget
                        self.current_pos = (row, column)
                        qtwidget.dateChanged.connect(
                            lambda date: self.aterar_dados_database(date.toString("dd/MM/yyyy"), 'QDateEdit'))
                        qtwidget.setFocus()

            elif widget == 'QDateTimeEdit':
                item = self.tabelademan.item(row, column)
                if item is not None:
                    if self.is_cell_editable(self.tabelademan, row, column):

                        dado = item.text()
                        qtwidget = QtWidgets.QDateTimeEdit()

                        bg_color = item.background().color().name()
                        if bg_color == '#000000':
                            bg_color = 'white'
                        qtwidget.setStyleSheet(f'background-color: {bg_color};')
                        qtwidget.setFixedSize(
                            self.tabelademan.columnWidth(column),
                            self.tabelademan.rowHeight(row)
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

                        self.tabelademan.setCellWidget(row, column, qtwidget)

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

                        self.current_editor = qtwidget
                        self.current_pos = (row, column)
                        qtwidget.dateTimeChanged.connect(
                            lambda dt: self.aterar_dados_database(dt.toString("dd/MM/yyyy HH:mm"), 'QDateTimeEdit'))

            elif widget == 'QTimeEdit':
                item = self.tabelademan.item(row, column)
                if item is not None:
                    if self.is_cell_editable(self.tabelademan, row, column):

                        dado = item.text()
                        qtwidget = QtWidgets.QTimeEdit()

                        time = QtCore.QTime.fromString(dado, "HH:mm")  # Ajuste o formato conforme necessário
                        if time.isValid():
                            qtwidget.setTime(time)

                        # Cor de fundo
                        bg_color = item.background().color().name()
                        if bg_color == '#000000':
                            bg_color = 'white'
                        qtwidget.setStyleSheet(f' background-color: {bg_color}; ')
                        qtwidget.setFixedSize(self.tabelademan.columnWidth(column),
                                              self.tabelademan.rowHeight(row))
                        self.tabelademan.setCellWidget(row, column, qtwidget)

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

                        self.current_editor = qtwidget
                        self.current_pos = (row, column)
                        qtwidget.timeChanged.connect(
                            lambda time: self.aterar_dados_database(time.toString("HH:mm"), 'QTimeEdit'))

            elif widget == 'QLineEdit':
                item = self.tabelademan.item(row, column)
                if item == None:
                    item = QtWidgets.QTableWidgetItem('')
                text = item.text() if item else ""
                line_edit = QLineEdit(text)

                bg_color = item.background().color().name()
                if bg_color == '#000000':
                    bg_color = 'white'
                line_edit.setStyleSheet(f'background-color: {bg_color}; border: none;')
                self.tabelademan.setCellWidget(row, column, line_edit)
                line_edit.setFocus()

                self.key_filter = KeyFilter(self.on_tab_pressed)
                line_edit.installEventFilter(self.key_filter)
                line_edit.setFocus()
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

                if column == colum_prontuario:
                    line_edit.textChanged.connect(
                        lambda text, datanasce=colum_data_nace, r=row, line=line_edit: self.prontu_text(text, datanasce,
                                                                                                        r, line))
                elif column == colum_paciente:
                    line_edit.textChanged.connect(
                        lambda text, datanasce=colum_data_nace, r=row, line=line_edit: self.name_text(text, datanasce,
                                                                                                      r, line))
                else:
                    line_edit.textChanged.connect(lambda texto: self.aterar_dados_database(texto, 'QLineEdit'))

            elif widget is not None:

                combo_box = QComboBox()
                item = self.tabelademan.item(row, column)
                bg_color = item.background().color().name() if item else '#FFFFFF'
                if bg_color == '#000000':
                    bg_color = 'white'
                combo_box.setStyleSheet(f'background-color: {bg_color};')
                combo_box.setFixedSize(self.tabelademan.columnWidth(column), self.tabelademan.rowHeight(row))

                if item is not None and self.is_cell_editable(self.tabelademan, row, column):

                    especialidades = ast.literal_eval(widget)
                    if isinstance(especialidades, list):

                        texto = item.text()
                        combo_box.addItems(especialidades)
                        combo_box.setCurrentText(texto)
                        self.tabelademan.setCellWidget(row, column, combo_box)
                    else:
                        print("Conteúdo não é uma lista válida.")

                font = combo_box.font()
                font.setBold(True)
                font.setPointSize(10)
                combo_box.setFont(font)

                self.key_filter = KeyFilter(self.on_tab_pressed)
                combo_box.installEventFilter(self.key_filter)

                self.current_editor = combo_box
                self.current_pos = (row, column)

                combo_box.currentTextChanged.connect(lambda texto: self.aterar_dados_database(texto, 'QComboBox'))
                combo_box.setFocus()
            self.iniciar_timer_inatividade()

        def finalizar_historico(self):
            print("Finalizando histórico...")

        def on_tab_pressed(self, widget):
            row, column = self.current_pos
            max_row = self.tabelademan.rowCount() - 1
            max_col = self.tabelademan.columnCount() - 1

            if column < max_col:
                column += 1
            else:
                column = 1
                if row < max_row:
                    row += 1
                else:
                    row = 0

            self.tabela_clicada(row, column)

            widget = self.tabelademan.cellWidget(row, column)

        def aterar_dados_database(self, texto, tipo):

            try:


                if self.edicao_ativada:
                    return

                row, colum = self.current_pos
                current_datetime = QDateTime.currentDateTime()
                formatted_time = current_datetime.toString('hh:mm')

                colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE', None)
                colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', None)
                colum_data_nace = self.descobrir_nome_coluna('DATA DE NASCIMENTO', None)

                pront = self.tabelademan.item(row, colum_prontuario)
                data = self.tabelademan.item(row, colum_data_nace)
                nome = self.tabelademan.item(row, colum_paciente)

                item = QtWidgets.QTableWidgetItem(texto)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabelademan.setItem(row, colum, QTableWidgetItem(item))

                if (self.tabelademan.verticalHeaderItem(row) is not None and self.tabelademan.verticalHeaderItem(
                        row).text() != ''):
                    id_valor = self.tabelademan.verticalHeaderItem(row).text()

                else:
                    id_valor = 0
                print('id_valor', id_valor)
                if row == self.tabelademan.rowCount() - 1 or id_valor == 0:
                    if self.analisar_requisitos_tabela_paciente(texto, id_valor, row, colum):
                        if id_valor == 0:
                            id_valor = str(row + 1)
                        print('PASSOU inserir', id_valor)
                        if self.tabelademan.item(row, colum_paciente) is None:
                            nome = ''
                        else:
                            nome = self.tabelademan.item(row, colum_paciente).text()
                        texto_historico = (f'{formatted_time}                {self.nome_user} INSERIU A DEMANDA DO PACIENTE \"{nome}\"')

                        self.data_deman.inserir_na_tabela(self, self.variavel, texto, id_valor, colum)

                        item = QtWidgets.QTableWidgetItem('')
                        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        self.tabelademan.setItem(row, colum, item)

                        # if colum == colum_prontuario or colum:
                        #     # self.moficacao_inserir(row, colum)
                        #     #
                        #     # self.data_deman.salvar_historico(self, self.lista_modificacao, self.linha_modificada,
                        #     #                                  self.linha_antiga, self.lista_nomes_das_colunas)
                        #     # self.lista_modificacao = []
                        item = QtWidgets.QTableWidgetItem('')
                        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        self.tabelademan.setItem(row, 0, item)
                        self.analise_corrent_pos = True
                else:
                    if self.analisar_requisitos_tabela_paciente(texto, id_valor, row, colum):
                        print('passou moddigica', id_valor)
                        self.data_deman.modificar_tabela(self, self.variavel, texto, id_valor, colum)
                        # self.modificao(row, colum)
                        #
                        # self.data_deman.salvar_historico(self, self.lista_modificacao, self.linha_modificada,
                        #                                  self.linha_antiga, self.lista_nomes_das_colunas)
                        # self.lista_modificacao = []
                        print(self.tabelademan.item(row, colum_paciente).text())
                        if self.tabelademan.item(row, colum_paciente) is None:
                            nome= ''
                        else:
                            nome = self.tabelademan.item(row, colum_paciente).text()

                        col_label = self.tabela_alt.horizontalHeaderItem(colum).text()
                        texto_historico = f'{formatted_time}                {self.nome_user} ALTEROU O \"{col_label}\"  NO PACIENTE \"{nome}\"'

                # self.atualiza_tabela_demandas(self.variavel)
                self.copiadora()
                print('Atualizando tabela de demandas...')

                if self.tabelademan.item(row, colum_paciente) is None:
                    nome = ''
                else:
                    nome = self.tabelademan.item(row, colum_paciente).text()

                if self.tabelademan.item(row, colum_prontuario) is None:
                    pront = ''
                else:
                    pront = self.tabelademan.item(row, colum_prontuario).text()

                if self.tabelademan.item(row, colum_data_nace) is None:
                    data_nascimento = ''
                else:
                    data_nascimento = self.tabelademan.item(row, colum_data_nace).text()

                if self.analise_corrent_pos == True:
                    texto_historico = (f'{formatted_time}                {self.nome_user} INSERIU A DEMANDA DO PACIENTE \"{nome}\"')
                    alteracao = 'INSERIU'
                    coluna_alteracao = f'{row}'
                else:
                    alteracao = 'EDITOU'
                    coluna_alteracao =f"{row, colum}"

                self.data_deman.criar_ou_atualizar_snapshot(self.variavel, self,pront, data_nascimento, nome,texto_historico,coluna_alteracao , alteracao)
                self.iniciar_timer_inatividade()

            except Exception as e:
                print(f"Error: {e}")

        def analisar_requisitos_tabela_paciente(self, valor_para_inserir, id_valor,row, colum):
            colum_paciente = 4
            colum_prontuario = 1

            colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE',colum_paciente)
            colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO',colum_prontuario)
            if self.tabelademan.item(row, colum_prontuario) is not None and self.tabelademan.item(row,
                                                                                                  colum_paciente) is not None:
                if self.tabelademan.item(row, colum_prontuario).text() != '' and self.tabelademan.item(row, colum_paciente).text() != '':
                    return True
                elif self.tabelademan.item(row, colum_prontuario).text() == '':
                    if self.tabelademan.item(row, colum_paciente).text() == '':
                        self._mostrar_mensagem('O campo \"PRONTUÁRIO\" é obrigatório!')
                        return False
                    return True
                else:
                    if self.tabelademan.item(row, colum_prontuario).text() == '':
                        self._mostrar_mensagem('O campo \"NOME DO PACIENTE\" é obrigatório!')
                        return False
                    return True


        def descobrir_nome_coluna(self, nome, coluna):
            for col in range(self.tabelademan.columnCount()):
                item_pac = self.tabelademan.horizontalHeaderItem(col)
                if item_pac is not None:
                    if item_pac.text() == nome:
                        return col
            return coluna

        def remover_widget(self):
            # Se há uma posição atual definida
            self.analise_corrent_pos = False
            if self.current_pos and self.current_editor:
                old_row, old_col = self.current_pos
                # Remove o widget da célula atual
                self.tabelademan.removeCellWidget(old_row, old_col)
                self.current_editor = None
            # Verifica e remove widgets de outras células que não sejam os esperados
            for row in range(self.tabelademan.rowCount()):
                for col in range(self.tabelademan.columnCount()):
                    widget = self.tabelademan.cellWidget(row, col)
                    if widget:
                        # Verifica se o widget pertence à lista de widgets válidos
                        is_valid = any(widget == line_edit for _, _, line_edit in self.lista_tooltip_label)
                        if not is_valid:
                            self.tabelademan.removeCellWidget(row, col)
            self.data_deman.definir_posicao_usuario(self.variavel, self, (None,None), 'DEMANDA')

        def atualizar_posicao(self):
            if self.current_editor:
                self.data_deman.definir_posicao_usuario(self.variavel, self, self.current_pos, 'DEMANDA')
            self.identificar_usuarios()

        def identificar_usuarios(self):
            self.atualiza_tabela_demandas(self.variavel)
            try:
                leitura = self.data_deman.ler_posicoes_usuarios(self,'DEMANDA', self.variavel)

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
                                index = self.tabelademan.indexAt(antigo_lineedit.pos())
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
                                item = self.tabelademan.item(row, col)
                                text = item.text() if item else ""
                                line_edit = ClickableLabel(text)

                                self.lista_user_pos.append((row, col))

                                bg_color = item.background().color().name() if item else 'white'
                                if bg_color == '#000000':
                                    bg_color = 'white'
                                line_edit.setStyleSheet(f'background-color: {bg_color}; border: 2px solid purple;')
                                line_edit.setFocus()

                                tooltip_label = QLabel(self.tabelademan)
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
                                self.tabelademan.setItemDelegate(delegate)
                                # Update cells and force repaint
                                delegate.update_target_cells([(row, col)])
                                self.tabelademan.viewport().update()
                                index = self.tabelademan.model().index(row, col)
                                rect = self.tabelademan.visualRect(index)

                                if not rect.isValid():
                                    tooltip_label.hide()
                                    continue

                                pos_viewport = rect.topRight() + QPoint(10, 0)
                                pos_viewport.setX(pos_viewport.x() - 15)
                                pos_viewport.setY(pos_viewport.y() - 5)

                                tooltip_label.setParent(self.tabelademan.viewport())
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

        def chamar_tabela_click(self,row, column, line):
            line.deleteLater()
            self.tabela_clicada(row, column)

        def inialisador_lauout_Edicao(self,scrol):
            self.line_nome_btn = QtWidgets.QLineEdit('Escreva o nome do Botão')
            # line_nome_btn.setToolTip('Tabela')
            scrol.addWidget(self.line_nome_btn)
            self.line_nome_btn.show()
            style_normal = """
                                        QLineEdit {
                                            background-color: white;
                                            color: black;
                                            border: none;
                                            padding: 10px 20px;
                                            font-size: 14px;
                                        }
                                        QLineEdit:hover {
                                            background-color: #555;
                                        }
                                        QLineEdit:pressed {
                                            background-color: #777;
                                        }
                                    """
            self.line_nome_btn.setStyleSheet(style_normal)
            self.line_nome_btn.setFixedHeight(40)
            self.line_nome_btn.setFixedWidth(320)

            self.line_nome_tabela = QtWidgets.QLineEdit(self.frame)
            self.line_nome_tabela.setToolTip('Nome da Tabela')
            self.line_nome_tabela.setGeometry(self.labeltitulo.geometry())
            self.line_nome_tabela.show()
            self.line_nome_tabela.setFixedHeight(60)
            self.line_nome_tabela.setFixedWidth(1000)
            self.line_nome_tabela.setStyleSheet(style_normal)

            for btn in self.frame.findChildren(QtWidgets.QPushButton):
                btn.hide()
            self.tabelademan.hide()
            self.tabela_edicao.show()
            self.timer_posicao.stop()

        def abrir_editor_tabela(self,scrol,acao):
            if self.preview.isVisible():
                self.preview.hide()
            self.inialisador_lauout_Edicao(scrol)

            self.line_nome_tabela.setText(self.labeltitulo.text())
            self.line_nome_btn.setText(self.btn_atual.text())
            self.editor_Tabela = Editabletabela(self.frame, self.tabela_edicao,self, acao,self.tabelademan)
            self.confirmar_alt_layout.show()
            self.excluir_tabela.show()

        def abrir_criar_tabela(self,scrol, acao):
            self.edicao_ativada = True
            self.inialisador_lauout_Edicao(scrol)
            if self.preview.isVisible():
                self.preview.hide()

            self.tabela_edicao.setColumnCount(len(self.fixed_columns))

            for col, nome in enumerate(self.fixed_columns):
                item = QtWidgets.QTableWidgetItem()
                font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
                font.setPointSize(8)
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                self.tabela_edicao.setHorizontalHeaderItem(col, item)
                item = self.tabela_edicao.horizontalHeaderItem(col)
                item.setText(nome)

            self.editor_Tabela = Criartabela(self.frame, self.tabela_edicao, self, acao, self.tabelademan)
            self.line_nome_tabela.setText('Escreva o nome da Tabela')
            self.line_nome_btn.setText('Escreva o nome do Botão')
            self.confirmar_new_layout.show()
            self.voltar_demandas.show()

        def criar_layout(self):
            if self.line_nome_tabela.text().strip().replace(' ', '') == '' or self.line_nome_tabela.text() == 'Escreva o nome da Tabela':
                self._mostrar_mensagem('Escreva o nome da Tabela.')
                return

            if self.line_nome_btn.text().strip().replace(' ', '') == '' or self.line_nome_btn.text() == 'Escreva o nome do Botão':
                self._mostrar_mensagem('Escreva o nome do Botão da Tabela.')
                return

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('Atenção')
            msg_box.setText('Criar Nova Tabela?')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            reply = msg_box.exec()
            if reply == QMessageBox.StandardButton.Yes:
                table_name = 'tabela_' + self.line_nome_tabela.text().strip().replace(' ', '')
                variavel = self.variavel
                self.variavel = table_name
                self.data_deman.criar_nova_tabela_demandas(self, self.tabela_edicao, table_name,self.line_nome_tabela.text(),self.line_nome_btn.text())
                self.atualizar_layout()
                self.variavel = variavel
                self.voltar()
                self._mostrar_mensagem('Tabela Criada!!!')

                self.line_nome_btn.hide()
                self.line_nome_tabela.hide()
                self.bottom_bar_layout.show()

                for btn in self.bottom_bar_layout.findChildren(QtWidgets.QPushButton):
                    btn.show()

        def voltar(self):
            self.lista_ids = []
            self.lista_titulo = []
            self.lista_dos_btn = []

            self.voltar_demandas.hide()
            self.confirmar_new_layout.hide()
            self.confirmar_alt_layout.hide()
            self.excluir_tabela.hide()

            self.habilitar_config()

            self.timer_posicao.start()

            self.tabelademan.show()
            self.tabela_edicao.hide()

            self.data_deman.ler_btn_tabela_demanda(self)

            zipped = zip(self.lista_ordem_tabelas,
                         self.lista_btn,
                         self.lista_titulo,
                         self.lista_ids)

            # Sort by the order value
            sorted_data = sorted(zipped, key=lambda x: x[0])

            (self.lista_ordem_tabelas,
             self.lista_btn,
             self.lista_titulo,
             self.lista_ids) = map(list, zip(*sorted_data))

            for btn in self.scroll_layout.findChildren(QtWidgets.QPushButton):
                btn.deleteLater()

            self.front_Demanda.acdicionar_btn_demanda(self.scroll_layout, sorted_data)

        def descobrir_widget(self,widget):
            if isinstance(widget, QLineEdit):
                return 'QLineEdit'
            elif isinstance(widget, QTimeEdit):
                return 'QTimeEdit'
            elif isinstance(widget, QDateEdit):
                return 'QDateEdit'
            elif isinstance(widget, QDateTimeEdit):
                return 'QDateTimeEdit'
            elif isinstance(widget, QComboBox):
                return 'QComboBox'

        def deslogar(self, main):
            self.Logando_tela = QtWidgets.QMainWindow()
            from Login import Ui_Form
            self.logando = Ui_Form()
            self.logando.setupUi(self.Logando_tela)

            self.mainwindow.close()
            self.janela_CTI_PED.close()
            self.Logando_tela.show()

        def pegar_dados_para_atualizar_widget(self, tabela, col):
            item = tabela.cellWidget(0, col)

            column_field = 'col' if col == 0 else f'col{col}'

            if item is not None:
                resposta = self.descobrir_widget(item)

                if resposta == 'QComboBox':
                    resposta = [item.itemText(i) for i in range(item.count()) if
                                item.itemText(i) != '']

            else:
                resposta = ''
            return resposta

        def ativar_shadow(self, value):

            colum_paciente = 4
            colum_prontuario = 1
            colum_data_nace = 5

            colum_paciente = self.descobrir_nome_coluna('NOME DO PACIENTE', colum_paciente)
            colum_prontuario = self.descobrir_nome_coluna('PRONTUÁRIO', colum_prontuario)
            colum_data_nace = self.descobrir_nome_coluna('DATA DE NASCIMENTO', colum_data_nace)

            maior = max(colum_paciente, colum_prontuario, colum_data_nace)

            if value < maior:
                self.preview.hide()
                palette = self.tabelademan.palette()
                palette.setColor(QPalette.ColorRole.Base, QColor("#d0f0c0"))  # green
                self.tabelademan.setPalette(palette)
            else:

                self.tabelademan.setPalette(self.style().standardPalette())
                self.preview.setRowCount(self.tabelademan.rowCount())

                # Determine visible columns (start with 0)
                start_col = 0
                visible_columns = []

                visible_columns.append(colum_prontuario)
                visible_columns.append(colum_paciente)
                visible_columns.append(colum_data_nace)

                for row in range(self.tabelademan.rowCount()):
                    for i, col in enumerate(visible_columns):
                        heightrow = self.preview.rowHeight(row)
                        item = self.tabelademan.item(row, col)
                        text = item.text() if item else ""
                        new_item = QTableWidgetItem(text)
                        new_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        self.preview.setItem(row, i, new_item)
                        self.preview.setRowHeight(row, heightrow)

                tamanh_col = 0
                for i, col in enumerate(visible_columns):
                    header_item = self.tabelademan.horizontalHeaderItem(col)
                    if header_item:
                        self.preview.setHorizontalHeaderItem(i, QTableWidgetItem(header_item.text()))
                        text_width = self.fontMetrics().boundingRect(header_item.text()).width()
                        self.preview.setColumnWidth(i, text_width + 100)
                        tamanh_col+=text_width + 100


                main_geom = self.tabelademan.geometry()
                viewport_height = self.tabelademan.viewport().height()

                width = self.tabelademan.verticalHeader().width()
                header_height = self.tabelademan.horizontalHeader().height()-1

                # Apply it to the horizontal header of table2
                self.preview.horizontalHeader().setFixedHeight(header_height)

                self.preview.setGeometry(
                    main_geom.left() + width,
                    main_geom.top()  + self.tabelademan.horizontalHeader().height(),
                    tamanh_col,
                    viewport_height + self.tabelademan.horizontalHeader().height()
                )
                self.preview.show()
                self.preview.cellClicked.connect(self.previw_clicado)

        def previw_clicado(self, row, column):
            self.preview.hide()
            colum = 0
            header_item = self.preview.horizontalHeaderItem(column)
            if header_item is not None:
                header_item.text()

                colum = self.descobrir_nome_coluna(header_item.text(), colum)
                self.tabelademan.setCurrentCell(row, colum-1)
                self.tabela_clicada(row, colum)

        def exluir_layout(self):

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('Atenção')
            msg_box.setText('Excluir Tabela?')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            reply = msg_box.exec()

            if reply == QMessageBox.StandardButton.Yes:
                self.data_deman.excluir_tabela_mysql(self, self.variavel)
                self.abrir_tabela(self.mainwindow,self.lista_ids[0],self.lista_titulo[0],self.lista_dos_btn[0])
                self.voltar()

        def normalizar_nome_mysql(self, nome):
            nome_sem_acentos = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')

            nome_limpo = re.sub(r'[^a-zA-Z0-9_]', '_', nome_sem_acentos)

            nome_final = re.sub(r'_+', '_', nome_limpo).strip('_')

            return nome_final

        def header_context_menu(self, position: QPoint):
            if self.edicao_ativada != True:
                return
            logical_index = self.tabelademan.horizontalHeader().logicalIndexAt(position)

            from database_Demandas import Ui_data_Demanda
            self.data_deman = Ui_data_Demanda()

            header = self.tabelademan.horizontalHeader()

            nome = (self.tabelademan.horizontalHeaderItem(header.logicalIndex(logical_index)).text())

            hide, priority = self.data_deman.descobrir_escondidos(self,self.variavel, nome)
            nan = (self.tabelademan.horizontalHeaderItem(logical_index).text())

            if nan in self.fixed_columns:
                menu = QMenu()

                prioridade_action = QAction("🔏 Definir Edição para somente o Nir", self.tabelademan)
                adicionar_column_acction = QAction("➕ Adicionar Coluna", self.tabelademan)
                esconder_action = QAction("🙈 Esconder Coluna", self.tabelademan)
                editar_action = QAction("✏️ Editar Tipo da Celula", self.tabelademan)

                if hide == 'TRUE':
                    esconder_action = QAction("👁️ Mostrar Coluna", self.tabelademan)

                if priority == 'TRUE':
                    prioridade_action = QAction("🔓 Definir Edição para todos", self.tabelademan)

                menu.addAction(adicionar_column_acction)
                menu.addAction(prioridade_action)
                menu.addAction(esconder_action)
                menu.addAction(editar_action)

                # esconder_action.triggered.connect(lambda: self.definir_escondido(logical_index))
                # prioridade_action.triggered.connect(lambda: self.definir_prioridade(logical_index))
                editar_action.triggered.connect(lambda: self.chamar_Edicao(logical_index, fixed=False))
                adicionar_column_acction.triggered.connect(lambda: self.adicionar_coluna(logical_index, fixed=False))
                menu.exec(self.tabelademan.horizontalHeader().mapToGlobal(position))

            else:

                menu = QMenu()
                prioridade_action = QAction("🔏 Definir Edição para somente o Nir", self.tabelademan)
                esconder_action = QAction("🙈 Esconder Coluna", self.tabelademan)
                adicionar_column_acction = QAction("➕ Adicionar Coluna", self.tabelademan)

                if hide == 'TRUE':
                    esconder_action = QAction("👁️ Mostrar Coluna", self.tabelademan)

                if priority == 'TRUE':
                    prioridade_action = QAction("🔓 Definir Edição para todos", self.tabelademan)

                rename_action = QAction("📝 Renomear Coluna", self.tabelademan)
                editar_action = QAction("✏️ Editar Tipo da Celula", self.tabelademan)
                delete_action = QAction("❌ Deletar Coluna", self.tabelademan)

                menu.addAction(adicionar_column_acction)
                menu.addAction(rename_action)
                menu.addAction(editar_action)
                menu.addAction(prioridade_action)
                menu.addAction(esconder_action)
                menu.addAction(delete_action)

                rename_action.triggered.connect(lambda: self.change_headers(logical_index))
                delete_action.triggered.connect(lambda: self.delete_column(logical_index))
                # esconder_action.triggered.connect(lambda: self.definir_escondido(logical_index))
                # prioridade_action.triggered.connect(lambda: self.definir_prioridade(logical_index))
                editar_action.triggered.connect(lambda: self.chamar_Edicao(logical_index, fixed=False))
                adicionar_column_acction.triggered.connect(lambda: self.adicionar_coluna(logical_index, fixed=False))
                menu.exec(self.tabelademan.horizontalHeader().mapToGlobal(position))

        def extrair_indice_coluna(self,nome):
            if nome == 'col':
                return 0
            match = re.search(r'\d+', nome)
            return int(match.group()) if match else None
        def adicionar_coluna(self, logical_index, fixed=False):
            num = 0
            for col in self.colunas_visuais_atuais:
                number = self.extrair_indice_coluna(col)
                if number> num :
                    num = number
            quantidade = num

            new_text, ok = QInputDialog.getText(
                self,
                "Escreva o nome da Coluna",
                "Nome da nova coluna:"
            )

            if ok and new_text:
                dialog = CustomInputDialog('QLineEdit', '')
                if dialog.exec():
                    tipo, valor = dialog.tipo, dialog.valor
                    print("Tipo escolhido:", tipo)
                    print("Valor inserido:", valor)

                    column_field = 'col' if quantidade == 0 else f'col{quantidade + 1}'
                    self.nomes_colunas[column_field] = new_text
                    self.widgets_colunas[column_field] = valor

                    # Adiciona a nova coluna
                    self.tabelademan.insertColumn(self.tabelademan.columnCount())
                    new_column_index = self.tabelademan.columnCount() - 1

                    # Atualiza o cabeçalho da nova coluna
                    self.tabelademan.setHorizontalHeaderItem(new_column_index, QTableWidgetItem(new_text))

                    # Atualiza a lista de controle
                    self.colunas_visuais_atuais.append(column_field)

                    # Força o layout/scroll a ser recalculado antes do moveSection
                    self.tabelademan.viewport().update()
                    QApplication.processEvents()

                    # Move visualmente a coluna se necessário
                    if 0 <= logical_index < self.tabelademan.columnCount() and new_column_index != logical_index:
                        print(f"✅ Movendo coluna {new_column_index} para {logical_index}")
                        self.tabelademan.horizontalHeader().moveSection(new_column_index, logical_index)
                    else:
                        print(f"⚠ Posição inválida ou movimento desnecessário: {new_column_index} -> {logical_index}")

                    self.alteracao_nome_widget = True
                    print("Nomes das colunas:", self.nomes_colunas)
                    print("Widgets das colunas:", self.widgets_colunas)
                    print("Ordem visual atual:", self.colunas_visuais_atuais)
                    print("Índice da nova coluna:", new_column_index)
                    print("Índice lógico desejado:", logical_index)

        def chamar_Edicao(self, logical_index, fixed=False):
            column_field = 'col' if logical_index == 1 else f'col{logical_index - 1}'
            widget_info = self.widgets_colunas.get(column_field)

            nome = self.nomes_colunas.get(column_field)
            if widget_info is None:
                tipo_widget = "QComboBox"
                dados = {}
            else:
                try:
                    dados = ast.literal_eval(widget_info)
                    tipo_widget = dados.get("tipo", "QComboBox")
                except Exception as e:
                    print(f"Erro ao interpretar widget_info: {e}")
                    tipo_widget = "QComboBox"
                    dados = {}

            dialog = CustomInputDialog(widget_info,dados)
            if dialog.exec():

                tipo, valor = dialog.tipo , dialog.valor
                print("Tipo escolhido:", tipo)
                print("Valor inserido:", valor)
                self.alteracao_nome_widget = True
                self.widgets_colunas[column_field] = valor
            print(self.widgets_colunas, 'widgets_colunas')


        def delete_column(self, column_index):
            print(column_index)
            self.tabelademan.removeColumn(column_index)

            header = self.tabelademan.horizontalHeader()
            logical_index = header.logicalIndex(column_index)

            if column_index == 1:
                column_field = 'col'
            else:
                column_field = f'col{column_index - 1}'
            self.colunas_visuais_atuais.remove(column_field)


        def change_headers(self, column_index: int):
            if self.edicao_ativada == True:
                self.tabelademan.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
                self.tabelademan.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
                self.tabelademan.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)


                current_header = self.tabelademan.horizontalHeaderItem(column_index).text()
                new_text, ok = QInputDialog.getText(
                    self,
                    "Altera nome da Coluna",
                    f"(Nome atual: {current_header})",
                    text=current_header
                )

                if ok and new_text:
                    column_field = 'col' if column_index == 1 else f'col{column_index - 1}'
                    self.nomes_colunas[column_field] = new_text
                    self.tabelademan.setHorizontalHeaderItem(column_index, QTableWidgetItem(new_text))
                    self.alteracao_nome_widget = True

        def travar_operacoes(self):
            self.edicao_ativada = True
            self.tabelademan.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.tabelademan.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
            self.tabelademan.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.timer_posicao.stop()

            self.confirmar_alt_layout.show()
            self.voltar_demandas.show()

        def voltar_operacoes(self):
            self.edicao_ativada = False
            self.tabelademan.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked | QAbstractItemView.EditTrigger.SelectedClicked)
            self.tabelademan.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
            self.tabelademan.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
            self.timer_posicao.start()

            self.confirmar_alt_layout.hide()
            self.voltar_demandas.hide()
            if self.current_editor:
                self.current_editor.setEnabled(True)

            for cont, id in enumerate(self.lista_ids):
                if id == self.variavel:
                    self.abrir_tabela(self.mainwindow, self.lista_ids[cont], self.lista_titulo[cont], self.lista_dos_btn[cont])
                    break


        def on_section_moved(self, logicalIndex, oldVisualIndex, newVisualIndex):
            print('Movendo colunas...')
            print(logicalIndex, oldVisualIndex, newVisualIndex)

            if logicalIndex == 0 or oldVisualIndex == 0:
                return

            header = self.tabelademan.horizontalHeader()
            item = self.colunas_visuais_atuais.pop(oldVisualIndex - 1)
            self.colunas_visuais_atuais.insert(newVisualIndex - 1, item)


        def sincronizar_colunas(self):
            print("Verificando alterações nas colunas...")
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('Confirmar Alterações ?')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            reply = msg_box.exec()
            if reply == QMessageBox.StandardButton.Yes:
                self.atualizar_layout()
                self.voltar()
                self._mostrar_mensagem('Tabela Alterada!!!')
                for cont, id in enumerate(self.lista_ids):
                    if id == self.variavel:
                        self.abrir_tabela(self.mainwindow, self.lista_ids[cont], self.lista_titulo[cont],
                                          self.lista_dos_btn[cont])
                        break

        def atualizar_layout(self):
            header = self.tabelademan.horizontalHeader()

            print('colunas_visuais_atuais', self.colunas_visuais_atuais, self.ordem_original_colunas)
            ordem_mudou = False
            colunas_deletadas = [col for col in self.ordem_original_colunas if
                                 col not in self.colunas_visuais_atuais]
            for col in self.ordem_original_colunas:
                if col not in self.colunas_visuais_atuais:
                    ordem_mudou = True
                    break
                if self.colunas_visuais_atuais.index(col) != self.ordem_original_colunas.index(col):
                    ordem_mudou = True
                    break

            if len(self.colunas_visuais_atuais) > len(self.ordem_original_colunas):
                print("Colunas visuais atuais excedem a ordem original.")
                self.data_deman.add_columns(self, self.colunas_visuais_atuais, self.ordem_original_colunas,
                                            self.variavel)
            if ordem_mudou:
                print("Ordem de colunas mudou.")
                self.data_deman.alterar_ordem_tabela(self, self.variavel, self.colunas_visuais_atuais,
                                                     self.ordem_original_colunas)
                self.alteracao_nome_widget = False
            if len(self.colunas_visuais_atuais) < len(self.ordem_original_colunas):
                print("Colunas deletadas:", colunas_deletadas)
                quantidade = len(colunas_deletadas)
                quantidade_inicio = len(self.ordem_original_colunas) - 1
                print("Quantidade de colunas deletadas:", quantidade, quantidade_inicio)
                for col in range(quantidade):
                    print(f"Deletando coluna: {self.ordem_original_colunas[quantidade_inicio - col]}")
                    self.data_deman.deletar_coluna(self, self.variavel,
                                                   self.ordem_original_colunas[quantidade_inicio - col])

            if self.alteracao_nome_widget == True:
                self.data_deman.alterar_widget_name(self, self.variavel, self.colunas_visuais_atuais,
                                                     self.ordem_original_colunas)


except Exception as e:
    print(f"Error: {e}")
