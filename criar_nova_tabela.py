from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QComboBox, QLineEdit, QTimeEdit, QDateEdit, QDateTimeEdit,
    QInputDialog, QMenu, QMessageBox,QStackedWidget,QAbstractItemView
)
from PyQt6 import  QtWidgets
from PyQt6.QtGui import QColor, QAction
from PyQt6.QtCore import Qt, QDate, QDateTime, QPoint
import sys
import sqlite3
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtCore import QTimer
from database_Demandas import Ui_data_Demanda
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QRadioButton, QStackedWidget
from PyQt6.QtGui import QIcon
import re
import ast
import os
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QFontMetrics

def resource_path(relative_path):
    """Resolve path para PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class CustomInputDialog(QDialog):
    def __init__(self, widget_type=None, dados=None):
        if dados is None:
            dados = {}

        super().__init__()
        self.setWindowTitle("Selecionar Tipo de Campo")
        self.setMinimumWidth(300)
        layout = QVBoxLayout(self)

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
        print(widget_type)

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

        self.radio_campo.toggled.connect(lambda: self.stack.setCurrentIndex(0))
        self.radio_tempo.toggled.connect(lambda: self.stack.setCurrentIndex(1))
        self.radio_data.toggled.connect(lambda: self.stack.setCurrentIndex(2))
        self.radio_data_tempo.toggled.connect(lambda: self.stack.setCurrentIndex(3))
        self.radio_lista.toggled.connect(lambda: self.stack.setCurrentIndex(4))

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.on_accept)
        self.buttons.rejected.connect(self.on_reject)
        layout.addWidget(self.buttons)

        self.set_widget_type(typo_dado)

    def update_item(self):
        current_index = self.combo.currentIndex()
        new_text = self.combo.currentText()

        if current_index >= 0:
            self.combo.setItemText(current_index, new_text)

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
        self.reject()

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

class Criartabela(QtWidgets.QWidget):
    def __init__(self, frame, tabela_edicao, deman, acao, tabelademan):
        super().__init__(deman)

        fm = QFontMetrics(self.font())

        self.frame = frame
        self.table = tabela_edicao
        self.edit = False
        self.fixed_columns = ["PRONTUÁRIO", "NPF", "NOME DO PACIENTE", "DATA DE NASCIMENTO",
                              'STATUS DA SOLICITAÇÃO', 'LEITO RESERVADO', 'DATA E HORA DA RESERVA']

        self.table.horizontalHeader().setSectionsMovable(False)
        self.table.horizontalHeader().sectionMoved.connect(self.on_section_moved)
        self.data_deman = Ui_data_Demanda()
        self.deman = deman

        self.deman.nomes_colunas = {}
        self.deman.widgets_colunas = {}
        self.deman.ordem_original_colunas = []
        self.deman.colunas_visuais_atuais = []

        self.table.setRowCount(1)

        self.table.horizontalHeader().setSectionsMovable(True)

        header = self.table.horizontalHeader()
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self.header_context_menu)
        self.table.horizontalHeader().sectionDoubleClicked.connect(self.change_headers)

        for idx,value in enumerate(self.fixed_columns):
            if idx == 0:
                column_field = 'col'
            else:
                column_field = f'col{idx}'

            self.deman.ordem_original_colunas.append(column_field)
            self.deman.colunas_visuais_atuais.append(column_field)

            if value == "DATA DE NASCIMENTO":
                widg = 'QDateEdit'
            elif value == 'DATA E HORA DA RESERVA':
                widg = 'QDateTimeEdit'
            else:
                widg = 'QLineEdit'

            self.deman.nomes_colunas[column_field] = value
            self.deman.widgets_colunas[column_field] = widg

        for colum in range(self.table.columnCount()):
            item_pac = self.table.horizontalHeaderItem(colum).text()
            text_width = fm.boundingRect(item_pac).width()
            self.increase_column_width(colum, text_width + 100)

        print(self.deman.widgets_colunas,'valor analise')
        print(self.deman.nomes_colunas,'nome analise')
    def increase_column_width(self, column, width):
        self.table.setColumnWidth(column, width)

    def header_context_menu(self, position: QPoint):
        logical_index = self.table.horizontalHeader().logicalIndexAt(position)

        header = self.table.horizontalHeader()

        nome = (self.table.horizontalHeaderItem(header.logicalIndex(logical_index)).text())

        hide, priority = self.data_deman.descobrir_escondidos(self.deman, self.deman.variavel, nome)
        nan = (self.table.horizontalHeaderItem(logical_index).text())

        if nan in self.fixed_columns:
            menu = QMenu()

            prioridade_action = QAction("🔏 Definir Edição para somente o Nir", self.table)
            adicionar_column_acction = QAction("➕ Adicionar Coluna", self.table)
            esconder_action = QAction("🙈 Esconder Coluna", self.table)
            editar_action = QAction("✏️ Editar Tipo da Celula", self.table)

            if hide == 'TRUE':
                esconder_action = QAction("👁️ Mostrar Coluna", self.table)

            if priority == 'TRUE':
                prioridade_action = QAction("🔓 Definir Edição para todos", self.table)

            menu.addAction(adicionar_column_acction)
            menu.addAction(prioridade_action)
            menu.addAction(esconder_action)
            menu.addAction(editar_action)

            # esconder_action.triggered.connect(lambda: self.definir_escondido(logical_index))
            # prioridade_action.triggered.connect(lambda: self.definir_prioridade(logical_index))
            editar_action.triggered.connect(lambda: self.chamar_Edicao(logical_index, fixed=False))
            adicionar_column_acction.triggered.connect(lambda: self.adicionar_coluna(logical_index, fixed=False))
            menu.exec(self.table.horizontalHeader().mapToGlobal(position))

        else:
            menu = QMenu()
            prioridade_action = QAction("🔏 Definir Edição para somente o Nir", self.table)
            esconder_action = QAction("🙈 Esconder Coluna", self.table)
            adicionar_column_acction = QAction("➕ Adicionar Coluna", self.table)

            if hide == 'TRUE':
                esconder_action = QAction("👁️ Mostrar Coluna", self.table)

            if priority == 'TRUE':
                prioridade_action = QAction("🔓 Definir Edição para todos", self.table)

            rename_action = QAction("📝 Renomear Coluna", self.table)
            editar_action = QAction("✏️ Editar Tipo da Celula", self.table)
            delete_action = QAction("❌ Deletar Coluna", self.table)

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
            menu.exec(self.table.horizontalHeader().mapToGlobal(position))

    def extrair_indice_coluna(self, nome):
        if nome == 'col':
            return 0
        match = re.search(r'\d+', nome)
        return int(match.group()) if match else None

    def adicionar_coluna(self, logical_index, fixed=False):
        num = 0
        for col in self.deman.colunas_visuais_atuais:
            number = self.extrair_indice_coluna(col)
            if number > num:
                num = number
        quantidade = num

        new_text, ok = QInputDialog.getText(
            None,
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
                self.deman.nomes_colunas[column_field] = new_text
                self.deman.widgets_colunas[column_field] = valor

                # Adiciona a nova coluna
                self.table.insertColumn(self.table.columnCount())
                new_column_index = self.table.columnCount() - 1

                # Atualiza o cabeçalho da nova coluna
                self.table.setHorizontalHeaderItem(new_column_index, QTableWidgetItem(new_text))

                # Atualiza a lista de controle
                self.deman.colunas_visuais_atuais.append(column_field)

                # Força o layout/scroll a ser recalculado antes do moveSection
                self.table.viewport().update()
                QApplication.processEvents()

                # Move visualmente a coluna se necessário
                if 0 <= logical_index < self.table.columnCount() and new_column_index != logical_index:
                    print(f"✅ Movendo coluna {new_column_index} para {logical_index}")
                    self.table.horizontalHeader().moveSection(new_column_index, logical_index)
                else:
                    print(f"⚠ Posição inválida ou movimento desnecessário: {new_column_index} -> {logical_index}")

                print("Nomes das colunas:", self.deman.nomes_colunas)
                print("Widgets das colunas:", self.deman.widgets_colunas)
                print("Ordem visual atual:", self.deman.colunas_visuais_atuais)
                print("Índice da nova coluna:", new_column_index)
                print("Índice lógico desejado:", logical_index)
                fm = QFontMetrics(self.font())

                item_pac = self.table.horizontalHeaderItem(new_column_index).text()
                text_width = fm.boundingRect(item_pac).width()
                self.increase_column_width(new_column_index, text_width + 100)

                #self._mostrar_mensagem('Coluna Adicionada!')

    def chamar_Edicao(self, logical_index, fixed=False):
        column_field = 'col' if logical_index == 0 else f'col{logical_index}'
        widget_info = self.deman.widgets_colunas.get(column_field)

        print(self.deman.widgets_colunas,'valor analise')
        nome = self.deman.nomes_colunas.get(column_field)
        if widget_info is None:
            tipo_widget = "QComboBox"
            dados = {}
        else:
            try:
                if isinstance(widget_info, str):
                    try:
                        dados = ast.literal_eval(widget_info)
                    except:
                        dados = widget_info
                tipo_widget = dados.get("tipo", "QComboBox")
            except Exception as e:
                print(f"Erro ao interpretar widget_info: {e}")
                tipo_widget = "QComboBox"
                dados = {}

        dialog = CustomInputDialog(widget_info, dados)
        if dialog.exec():
            tipo, valor = dialog.tipo, dialog.valor
            print("Tipo escolhido:", tipo)
            print("Valor inserido:", valor)
            self.deman.widgets_colunas[column_field] = valor
            print(self.deman.widgets_colunas, 'widgets_colunas')
            self.atualizar_metricas()
            self._mostrar_mensagem('Alteração Realizada!')

    def delete_column(self, column_index):
        resposta = self._mostrar_mensagem_yes_no('Deletar Coluna?')
        if resposta == QMessageBox.StandardButton.Yes:
            print(column_index)
            self.table.removeColumn(column_index)

            header = self.table.horizontalHeader()
            logical_index = header.logicalIndex(column_index)

            if column_index == 0:
                column_field = 'col'
            else:
                column_field = f'col{column_index }'
            self.deman.colunas_visuais_atuais.remove(column_field)
            self.atualizar_metricas()
            self._mostrar_mensagem('Alteração Realizada!')


    def change_headers(self, column_index: int):
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        current_header = self.table.horizontalHeaderItem(column_index).text()
        new_text, ok = QInputDialog.getText(
            self,
            "Altera nome da Coluna",
            f"(Nome atual: {current_header})",
            text=current_header
        )

        if ok and new_text:


            fm = QFontMetrics(self.font())
            column_field = 'col' if column_index == 0 else f'col{column_index }'
            self.deman.nomes_colunas[column_field] = new_text
            self.table.setHorizontalHeaderItem(column_index, QTableWidgetItem(new_text))

            item_pac = self.table.horizontalHeaderItem(column_index).text()
            text_width = fm.boundingRect(item_pac).width()
            self.increase_column_width(column_index, text_width + 100)
            self.atualizar_metricas()
            self._mostrar_mensagem('Alteração Realizada!')

    def on_section_moved(self, logicalIndex, oldVisualIndex, newVisualIndex):
        print('Movendo colunas...')
        print(logicalIndex, oldVisualIndex, newVisualIndex)

        if logicalIndex == 0 or oldVisualIndex == 0:
            return

        header = self.table.horizontalHeader()
        item = self.deman.colunas_visuais_atuais.pop(oldVisualIndex)
        self.deman.colunas_visuais_atuais.insert(newVisualIndex, item)
        self.atualizar_metricas()

    def atualizar_metricas(self):
        print("Nomes das colunas:", self.deman.nomes_colunas)
        print("Widgets das colunas:", self.deman.widgets_colunas)
        print("Ordem visual atual:", self.deman.colunas_visuais_atuais)

    def _mostrar_mensagem_yes_no(self, texto):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle('Confirmação')
        msg_box.setText(texto)
        icon = QIcon(resource_path('imagens/warning.ico'))
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()
        return reply

    def _mostrar_mensagem(self, texto):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText(texto)
        icon = QIcon(resource_path('imagens/warning.ico'))
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()