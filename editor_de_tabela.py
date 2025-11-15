from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QComboBox, QLineEdit, QTimeEdit, QDateEdit, QDateTimeEdit,
    QInputDialog, QMenu, QMessageBox, QPushButton, QMainWindow
)
from PyQt6.QtGui import QColor, QAction,QColor, QAction, QFontMetrics, QFont

from PyQt6.QtCore import Qt, QDate, QDateTime, QPoint
import sys
import sqlite3
from PyQt6.QtGui import QFontMetrics
import ast


class Editabletabela:
    def __init__(self, frame: QFrame, tabela: QTableWidget,deman,acao,tabela_Atual):
        self.frame = frame
        self.deman = deman
        self.table = tabela
        self.fixed_columns = ["PRONTUÁRIO", "NPF","NOME DO PACIENTE", "DATA DE NASCIMENTO",'STATUS DA SOLICITAÇÃO','LEITO RESERVADO','DATA E HORA DA RESERVA']
        self.type_selector = []
        self.table.setRowCount(1)
        self.table.setColumnCount(tabela_Atual.columnCount())
        self.edit = False
        self.colunas_dados_fixos = []
        deman.ordem_colunas = []
        self.ordem_colunas = deman.ordem_colunas
        self.ordem_colunas_indices = []
        self.cont = 0
        self.iniciar_tabela(deman)
        deman.lista_econder = []
        deman.lista_prioridade_nir = []
        deman.voltar_demandas.show()

        self.edit = True
        self.table.setHorizontalHeaderLabels(deman.lista_nomes_das_colunas + ["Click duas vezes para salvar a coluna."])
        self.setup_column(self.cont+1, fixed=False)

        #self.table.resizeColumnsToContents()

        for col in range(self.table.columnCount()):
            header_item = self.table.horizontalHeaderItem(col)
            if header_item is not None:
                item_pac = header_item.text()
                font = self.table.font()
                metrics = QFontMetrics(font)
                text_width = metrics.boundingRect(item_pac).width()
                width = text_width + 100
                self.table.setColumnWidth(col, width)

        layout = QVBoxLayout(self.frame)
        self.table.horizontalHeader().setSectionsMovable(True)
        layout.addWidget(self.table)
        self.table.horizontalHeader().sectionDoubleClicked.connect(self.set_header_name)
        self.table.horizontalHeader().sectionMoved.connect(self.on_section_moved)

        self.table.horizontalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.horizontalHeader().customContextMenuRequested.connect(self.header_context_menu)

        self.conn = sqlite3.connect('data.db')
        header = self.table.horizontalHeader()

        deman.columns = [
            self.table.horizontalHeaderItem(header.logicalIndex(i)).text()
            for i in range(self.table.columnCount() - 1)
            if self.table.horizontalHeaderItem(header.logicalIndex(i))
               and self.table.horizontalHeaderItem(
                header.logicalIndex(i)).text() != "Click duas vezes para salvar a coluna."
        ]

    def setup_fixed_column(self, column_index, name):
        if name == "DATA DE NASCIMENTO":
            widget = QDateEdit()
            widget.setDisplayFormat("dd/MM/yyyy")
            widget.setDate(QDate.currentDate())
        elif name == 'DATA E HORA DA RESERVA':
            widget = QDateTimeEdit()
            widget.setDisplayFormat("dd/MM/yyyy HH:mm")
            widget.setDateTime(QDateTime.currentDateTime())
        else:
            widget = QLineEdit()

        self.table.setCellWidget(0, column_index, widget)
        self.type_selector.append(None)

    def setup_column(self, column_index, fixed=False):

        if fixed:
            widget = QLineEdit()
            self.table.setCellWidget(0, column_index, widget)
            self.type_selector.append(None)

        if self.dados == 'QLineEdit':
            campo = 'CAMPO ABERTO'

        elif self.dados == 'QDateEdit':
            campo = 'DATA'

        elif self.dados == 'QDateTimeEdit':
            campo = 'DATA COM TEMPO'

        elif self.dados == 'QTimeEdit':
            campo = 'TEMPORIZADOR'
        else:
            campo = 'LISTA SUSPENSA'

        print(self.dados, campo)
        combo = QComboBox()
        combo.addItems(["Escolher...","CAMPO ABERTO", "TEMPORIZADOR", "DATA", "DATA COM TEMPO", "LISTA SUSPENSA"])
        combo.currentTextChanged.connect(lambda val, combox=combo: self.handle_combo_change(val, combox))

        combo.setItemText(0, 'Escolher...')

        self.type_selector.append(combo)
        self.table.setCellWidget(0, column_index, combo)
        if self.edit == False:
            self.set_cell_widget(column_index, campo)
        self.table.resizeColumnsToContents()

    def handle_combo_change(self, value, combo):
        index = self.table.indexAt(combo.pos())
        row = index.row()
        col = index.column()

        print(f"Changed combo at row {row}, column {col} to {value}")
        if self.edit == True:
            self.set_cell_widget(col, value)

    def set_cell_widget(self, column_index, type_choice):
        if type_choice == "CAMPO ABERTO":
            widget = QLineEdit()

        elif type_choice == "TEMPORIZADOR":
            widget = QTimeEdit()
            widget.setDisplayFormat("HH:mm:ss")

        elif type_choice == "DATA":
            widget = QDateEdit()
            widget.setDisplayFormat("dd/MM/yyyy")
            widget.setDate(QDate.currentDate())

        elif type_choice == "DATA COM TEMPO":
            widget = QDateTimeEdit()
            widget.setDisplayFormat("dd/MM/yyyy HH:mm")
            widget.setDateTime(QDateTime.currentDateTime())

        elif type_choice == "LISTA SUSPENSA":
            def update_item():
                current_index = combo.currentIndex()
                new_text = combo.currentText()

                if current_index >= 0:
                    combo.setItemText(current_index, new_text)

                # Check if '' is already in the combo
                if combo.findText('') == -1:
                    if '' not in [combo.itemText(i) for i in range(combo.count())]:
                        combo.addItem('')

                    combo.setEditable(True)

            combo = QComboBox()
            combo.setEditable(True)

            combo.currentTextChanged.connect(update_item)

            combo_items =  ['',"+ Adicionar Item"]
            if self.edit == False:

                especialidades = ast.literal_eval(self.dados)
                if isinstance(especialidades, list):
                    texto = ''

                    combo.setCurrentText(texto)
                    combo.addItems(especialidades)

            def handle_selection(index):
                if combo.itemText(index) == "+ Adicionar Item":
                    text, ok = QInputDialog.getText(
                        self.frame, "Adicionar Item", "Novo Item:"
                    )
                    if ok and text.strip():
                        combo.insertItem(combo.count() - 1, text.strip())

            combo.activated.connect(handle_selection)
            if '' not in [combo.itemText(i) for i in range(combo.count())]:
                combo.addItem('')

            combo.setEditable(True)

            widget = combo

        self.table.removeCellWidget(0, column_index)
        self.table.setCellWidget(0, column_index, widget)
        self.deman.ordem_linha = self.get_row_values(0, True)

        widget.setFixedHeight(30)
        widget.setStyleSheet(f'background-color: white; color: black;')

    def set_header_name(self, column_index):
        if column_index in self.colunas_dados_fixos:
            return

        widget = self.table.cellWidget(0, column_index)
        if isinstance(widget, QComboBox):
            print(widget.currentText())
            if widget.currentText() == "Escolher...":
                print('grade')
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('Atenção')
                msg_box.setText('Por favor, selecione o Tipo de Atributo antes de salvar a coluna.')
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply = msg_box.exec()
                return
        current_text = self.table.horizontalHeaderItem(column_index).text()

        text, ok = QInputDialog.getText(
            self.frame,
            "Defina o nome da Coluna",
            "Nome da Coluna:",
            text=current_text
        )

        if ok and text.strip() != "":
            header = self.table.horizontalHeader()

            if column_index != self.table.columnCount():
                if self.table.horizontalHeaderItem(header.logicalIndex(column_index)).text() in self.deman.lista_econder:
                    from database_Demandas import Ui_data_Demanda
                    self.data_deman = Ui_data_Demanda()

                    nome = (self.table.horizontalHeaderItem(header.logicalIndex(column_index)).text())

                    hide, priority = self.data_deman.descobrir_escondidos(self.deman,self.deman.variavel, nome)
                    if hide == 'TRUE':
                        self.deman.lista_econder.append((
                            self.table.horizontalHeaderItem(column_index).text(),
                            'FALSE'
                        ))
                    else:
                        self.deman.lista_econder.append((
                            self.table.horizontalHeaderItem(column_index).text(),
                            'TRUE'
                        ))

                if self.table.horizontalHeaderItem(header.logicalIndex(column_index)).text() in self.deman.lista_prioridade_nir:

                    from database_Demandas import Ui_data_Demanda
                    self.data_deman = Ui_data_Demanda()
                    nome = (self.table.horizontalHeaderItem(header.logicalIndex(column_index)).text())
                    hide, priority = self.data_deman.descobrir_escondidos(self.deman,self.deman.variavel, nome)
                    if priority == 'TRUE':
                        self.deman.lista_prioridade_nir.append((
                            self.table.horizontalHeaderItem(column_index).text(),
                            'FALSE'
                        ))
                    else:
                        self.deman.lista_prioridade_nir.append((
                            self.table.horizontalHeaderItem(column_index).text(),
                            'TRUE'
                        ))

            self.table.setHorizontalHeaderItem(column_index, QTableWidgetItem(text.strip()))
            self.add_column_if_last(column_index)
            header = self.table.horizontalHeader()

            num_colunas = self.table.columnCount() - 1
            if self.table.columnCount() == len(self.fixed_columns):
                self.add_column_if_last(self.table.columnCount() - 1)
            self.deman.columns = [
            self.table.horizontalHeaderItem(header.logicalIndex(i)).text()
            for i in range(self.table.columnCount() - 1)
            if self.table.horizontalHeaderItem(header.logicalIndex(i))
            and self.table.horizontalHeaderItem(header.logicalIndex(i)).text() != "Click duas vezes para salvar a coluna."
          ]

            self.deman.ordem_linha = self.get_row_values(0, True)

            current_col = self.table.columnCount()
            print(self.ordem_colunas)

    def add_column_if_last(self, column_index):
        if column_index == self.table.columnCount() - 1:

            current_col = self.table.columnCount()
            self.table.setColumnCount(current_col + 1)
            self.table.setHorizontalHeaderItem(current_col, QTableWidgetItem("Click duas vezes para salvar a coluna."))

            self.setup_column(current_col)
            self.ordem_colunas.append(current_col-1)

    def header_context_menu(self, position: QPoint):
        logical_index = self.table.horizontalHeader().logicalIndexAt(position)

        from database_Demandas import Ui_data_Demanda
        self.data_deman = Ui_data_Demanda()

        header = self.table.horizontalHeader()

        nome = (self.table.horizontalHeaderItem(header.logicalIndex(logical_index)).text())

        hide, priority = self.data_deman.descobrir_escondidos(self.deman,self.deman.variavel, nome)
        nan = (self.table.horizontalHeaderItem(logical_index).text())

        print(nan,self.fixed_columns)
        if nan in self.fixed_columns:
            menu = QMenu()

            prioridade_action = QAction("🔏 Definir Edição para somente o Nir", self.table)
            esconder_action = QAction("🙈 Esconder Coluna", self.table)
            editar_action = QAction("✏️ Editar Tipo da Celula", self.table)

            if hide == 'TRUE':
                esconder_action = QAction("👁️ Mostrar Coluna", self.table)

            if priority == 'TRUE':
                prioridade_action = QAction("🔓 Definir Edição para todos", self.table)

            menu.addAction(prioridade_action)
            menu.addAction(esconder_action)
            menu.addAction(editar_action)

            esconder_action.triggered.connect(lambda: self.definir_escondido(logical_index))
            prioridade_action.triggered.connect(lambda: self.definir_prioridade(logical_index))
            editar_action.triggered.connect(lambda: self.chamar_Edicao(logical_index, fixed=False))
            menu.exec(self.table.horizontalHeader().mapToGlobal(position))

        else:

            menu = QMenu()
            prioridade_action = QAction("🔏 Definir Edição para somente o Nir", self.table)
            esconder_action = QAction("🙈 Esconder Coluna", self.table)

            if hide == 'TRUE':
                esconder_action = QAction("👁️ Mostrar Coluna", self.table)

            if priority == 'TRUE':
                prioridade_action = QAction("🔓 Definir Edição para todos", self.table)

            rename_action = QAction("📝 Renomear Coluna", self.table)
            editar_action = QAction("✏️ Editar Tipo da Celula", self.table)
            delete_action = QAction("❌ Deletar Coluna", self.table)

            menu.addAction(rename_action)
            menu.addAction(editar_action)
            menu.addAction(prioridade_action)
            menu.addAction(esconder_action)
            menu.addAction(delete_action)

            rename_action.triggered.connect(lambda: self.set_header_name(logical_index))
            delete_action.triggered.connect(lambda: self.delete_column(logical_index))
            esconder_action.triggered.connect(lambda: self.definir_escondido(logical_index))
            prioridade_action.triggered.connect(lambda: self.definir_prioridade(logical_index))
            editar_action.triggered.connect(lambda: self.chamar_Edicao(logical_index, fixed=False))
            menu.exec(self.table.horizontalHeader().mapToGlobal(position))

    def delete_column(self, column_index):
        if column_index in self.colunas_dados_fixos:
            QMessageBox.warning(
                self.frame, "Warning", "Essa coluna não pode ser deletada."
            )
            return
        self.table.removeColumn(column_index)

        print('analise delete')


        print('rapaz2',self.ordem_colunas)
        for i in range(len(self.ordem_colunas_indices)):
            header_text = self.table.horizontalHeaderItem(column_index).text()
            print('a', header_text, self.ordem_colunas_indices[i])

            if header_text == self.ordem_colunas_indices[i]:
                self.ordem_colunas.remove(self.ordem_colunas[i])
                self.ordem_colunas_indices.remove(self.ordem_colunas_indices[i])
                break

        print('rapaz',self.ordem_colunas, self.table.horizontalHeaderItem(column_index).text())
        if self.table.horizontalHeaderItem(column_index).text() == "Click duas vezes para salvar a coluna.":
            print(122112)
            self.add_column_if_last(self.table.columnCount()-1)
        self.table.removeColumn(column_index)

        header = self.table.horizontalHeader()

        num_colunas = self.table.columnCount() - 1

        self.deman.columns = [
            self.table.horizontalHeaderItem(header.logicalIndex(i)).text()
            for i in range(num_colunas)
        ]

        print('analise delete',self.deman.columns)

        self.deman.ordem_linha = self.get_row_values(0, True)
    def chamar_Edicao(self,logical_index, fixed=False):
        self.edit = True
        self.dados = ''
        self.setup_column(logical_index, fixed=False)
        #self.edit = False

    def on_section_moved(self, logicalIndex, oldVisualIndex, newVisualIndex):

        column_count = self.table.columnCount()

        header = self.table.horizontalHeader()
        print(1)
        if self.table.horizontalHeaderItem(oldVisualIndex).text() != "Click duas vezes para salvar a coluna.":
            print(12)
            item = self.ordem_colunas.pop(oldVisualIndex)
            self.ordem_colunas.insert(newVisualIndex, item)

            num_colunas = column_count - 1

            # Update deman.columns ignoring the last column
            self.deman.columns = [
            self.table.horizontalHeaderItem(header.logicalIndex(i)).text()
            for i in range(self.table.columnCount() - 1)
            if self.table.horizontalHeaderItem(header.logicalIndex(i))
            and self.table.horizontalHeaderItem(header.logicalIndex(i)).text() != "Click duas vezes para salvar a coluna."
            ]


            self.deman.ordem_linha = self.get_row_values(0, True)

            print(f"Coluna movida: índice lógico {logicalIndex}, de posição {oldVisualIndex} para {newVisualIndex}")
            print(self.deman.columns)

    def get_row_values(self, row=0, ignore_last=True):
        header = self.table.horizontalHeader()
        count = self.table.columnCount() - 1 if ignore_last else self.table.columnCount()

        valores = []
        for i in range(count):
            col_index = header.logicalIndex(i)
            item = self.table.cellWidget(0, col_index)

            column_field = 'col' if col_index == 0 else f'col{col_index}'

            if item is not None:
                resposta = self.deman.descobrir_widget(item)

                if resposta == 'QComboBox':
                    resposta = [item.itemText(i) for i in range(item.count()) if
                                item.itemText(i) != '+ Adicionar Item']
                    print(resposta)
            else:
                resposta = ''
            valores.append(resposta)
        print(valores)
        return valores
    def iniciar_tabela(self,deman):
        print('tabela inciadad')

        for cont, coluna in enumerate(deman.lista_nomes_das_colunas):
            self.dados = deman.lista_widgets[cont+1]
            if coluna in self.fixed_columns:
                self.setup_column(cont, fixed=True)
                self.colunas_dados_fixos.append(cont)
                item = QTableWidgetItem(deman.lista_widgets[cont])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(0, cont, item)
            else:
                self.table.setHorizontalHeaderItem(cont, QTableWidgetItem(coluna))
                self.setup_column(cont, fixed=False)

            item = QTableWidgetItem(deman.lista_widgets[cont])
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(0, cont, item)
            self.ordem_colunas.append(cont)
            self.ordem_colunas_indices.append(coluna)
        self.cont = cont

    def definir_escondido(self, coluna):

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Confirmar Alteração ?')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            header = self.table.horizontalHeader()

            num_colunas = self.table.columnCount() - 1
            from database_Demandas import Ui_data_Demanda
            self.data_deman = Ui_data_Demanda()

            header = self.table.horizontalHeader()

            nome = (self.table.horizontalHeaderItem(header.logicalIndex(coluna)).text())

            hide, priority = self.data_deman.descobrir_escondidos(self.deman,self.deman.variavel, nome)
            if hide == 'TRUE':
                self.deman.lista_econder.append((
                    self.table.horizontalHeaderItem(coluna).text(),
                    'FALSE'
                ))
            else:
                self.deman.lista_econder.append((
                    self.table.horizontalHeaderItem(coluna).text(),
                    'TRUE'
                ))

            from database_Demandas import Ui_data_Demanda
            self.data_deman = Ui_data_Demanda()
            self.data_deman.atualizar_escondidos(self.deman, self.deman.variavel)

    def definir_prioridade(self, coluna):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Confirmar Alteração ?')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            header = self.table.horizontalHeader()

            num_colunas = self.table.columnCount() - 1
            from database_Demandas import Ui_data_Demanda
            self.data_deman = Ui_data_Demanda()

            header = self.table.horizontalHeader()

            nome = (self.table.horizontalHeaderItem(header.logicalIndex(coluna)).text())

            hide, priority = self.data_deman.descobrir_escondidos(self.deman,self.deman.variavel, nome)
            if priority == 'TRUE':
                self.deman.lista_prioridade_nir.append((
                    self.table.horizontalHeaderItem(coluna).text(),
                    'FALSE'
                ))
            else:
                self.deman.lista_prioridade_nir.append((
                    self.table.horizontalHeaderItem(coluna).text(),
                    'TRUE'
                ))


