from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt,QTimer
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QSizePolicy, QVBoxLayout, QSpacerItem, QSizePolicy,QMenuBar, QMenu
from PyQt6.QtGui import QAction, QIcon
import os
import re
import sys
from database_Demandas import Ui_data_Demanda

def resource_path(relative_path):
    """Resolve path para PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

from PyQt6 import QtWidgets, QtCore, QtGui

class DraggableButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setFixedWidth(320)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.drag_start_pos = None
        self.parent = parent
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.position()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_start_pos is not None:
            distance = (event.position() - self.drag_start_pos).manhattanLength()
            if distance > QtWidgets.QApplication.startDragDistance():
                drag = QtGui.QDrag(self)
                mime_data = QtCore.QMimeData()
                mime_data.setText(self.text())
                drag.setMimeData(mime_data)
                pixmap = self.grab()
                drag.setPixmap(pixmap)
                drag.setHotSpot(event.position().toPoint())
                drag.exec(QtCore.Qt.DropAction.MoveAction)
                self.drag_start_pos = None
        super().mouseMoveEvent(event)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent):
        source_text = event.mimeData().text()
        source_btn = None
        source_index = None
        target_index = None
        target_btn = self
        print(99)
        # if not hasattr(self.parent, "scroll_layout"):
        #     return
        print(22)

        for i in range(self.parent.deman.scroll_layout.count()):
            w = self.parent.deman.scroll_layout.itemAt(i).widget()
            print('analise',w.text(),source_text)
            if isinstance(w, DraggableButton) and w.text() == source_text:
                source_btn = w
        print('analise1',source_btn.text())
        if source_btn and source_btn != target_btn:
            layout = self.parent.deman.scroll_layout
            source_index = layout.indexOf(source_btn)
            target_index = layout.indexOf(target_btn)
            print(source_index,'fifa',layout.indexOf(source_btn))
            layout.takeAt(source_index)
            layout.insertWidget(target_index, source_btn)

            self.update_order_list(source_index, target_index)

        event.acceptProposedAction()

    def update_order_list(self, source_index, target_index):
        print(f"update_order_list chamado com: source_index={source_index}, target_index={target_index}")
        order_list = self.parent.deman.lista_ordem_tabelas[:]
        btn_list = self.parent.deman.lista_btn[:]
        titulo_list = self.parent.deman.lista_titulo[:]
        id_list = self.parent.deman.lista_ids[:]

        print("Tamanhos das listas:")
        print("order_list:", len(order_list))
        print("btn_list:", len(btn_list))
        print("titulo_list:", len(titulo_list))
        print("id_list:", len(id_list))

        # Verifique se source_index está dentro do intervalo de todas as listas
        for name, lst in [("order_list", order_list), ("btn_list", btn_list),
                          ("titulo_list", titulo_list), ("id_list", id_list)]:
            if not (0 <= source_index < len(lst)):
                print(f"Índice inválido para {name}: {source_index}")
                return

        # Agora pode fazer os pops e inserts em segurança
        for lst in [order_list, btn_list, titulo_list, id_list]:
            item = lst.pop(source_index)
            lst.insert(target_index, item)
        print('lista apos insert',btn_list)

        # Continua o resto da função...

        # Update (though lists are modified in-place)
        self.parent.deman.lista_ordem_tabelas = order_list
        self.parent.deman.lista_btn = btn_list
        self.parent.deman.lista_titulo = titulo_list
        self.parent.deman.lista_ids = id_list

        self.data_deman = Ui_data_Demanda()
        self.data_deman.atualizar_posicao_tabela(self.parent.deman)


class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
class Front_Demanda(QtWidgets.QMainWindow):

    def toggle_table_size(self):
        if self.is_half_size:
            self.deman.frame.setMaximumWidth(self.tamanho_frame)
            self.deman.frame.setMaximumHeight(self.tamanho_frame_h)
            self.deman.frame.move(0,0)
            self.side_bar.show()
            self.bottom_bar.show()
            for label in self.deman.frame.findChildren(QtWidgets.QLabel):
                label.show()
            for btn in self.deman.frame.findChildren(QtWidgets.QPushButton):
                if btn != self.deman.btnfechar:
                    btn.show()
            self.deman.editbarra.show()
            download_icon = QtGui.QIcon(resource_path('imagens/54638.ico'))  # Assuming the download icon file exists
            pixmap = download_icon.pixmap(30, 30)
            self.label_icone.setPixmap(pixmap)
            self.deman.header_frame.show()
            self.deman.tabelademan.setFixedHeight(self.deman.frame.height() - 300)
            self.deman.tabela_edicao.setFixedHeight(self.deman.frame.height() - 300)
            self.toggle_button.hide()
            self.tabela_maxima = False

            if self.dept != 'NIR' and self.dept != 'Administrador'and  self.deman.dept!= 'Telespectador':
                self.bottom_bar.hide()
        else:
            self.deman.frame.setMaximumWidth(self.deman.frame.width())
            for label in self.deman.frame.findChildren(QtWidgets.QLabel):
                is_valid = any(label == label_edit for _, label_edit, _ in self.deman.lista_tooltip_label)
                if not is_valid:
                    label.hide()
            for btn in self.deman.frame.findChildren(QtWidgets.QPushButton):
                btn.hide()
            self.tamanho_frame = self.deman.frame.width()
            self.tamanho_frame_h = self.deman.frame.height()
            self.deman.header_frame.hide()
            self.side_bar.show()
            self.deman.tabela_edicao.setFixedHeight(self.deman.frame.height() - 150)
            self.deman.tabelademan.setFixedHeight(self.deman.frame.height() - 150)
            self.tabela_maxima = True
            download_icon = QtGui.QIcon(resource_path('imagens/download.ico'))  # Assuming the download icon file exists
            pixmap = download_icon.pixmap(30, 30)
            self.label_icone.setPixmap(pixmap)
            self.deman.editbarra.show()
            self.side_bar.show()
            self.bottom_bar.show()
            self.label_icone.show()
            self.deman.btn_filtros.show()
            self.deman.btn_reservar_leito.show()
            self.deman.btnexclu.show()
            if self.dept != 'NIR' and self.dept != 'Administrador'and  self.deman.dept!= 'Telespectador':
                self.bottom_bar.hide()
        self.is_half_size = not self.is_half_size

    def start_mouse_tracking(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_mouse_position)
        self.timer.start(100)
        if (self.deman.dept!= 'NIR' and  self.deman.dept!= 'Telespectador' and self.deman.dept!= 'Administrador'):
            self.bottom_bar.hide()
            self.deman.btn_reservar_leito.hide()

    def check_mouse_position(self):
        if (self.deman.dept!= 'NIR' and  self.deman.dept!= 'Telespectador' and self.deman.dept!= 'Administrador'):
            self.bottom_bar.hide()
            self.deman.btn_reservar_leito.hide()

        self.tamanho_frame = self.deman.frame.width()
        self.tamanho_frame_h = self.deman.frame.height()

        if self.tabela_maxima == False:
            self.deman.tabelademan.setFixedHeight(self.deman.frame.height() - 300)
            self.deman.tabela_edicao.setFixedHeight(self.deman.frame.height() - 300)

        self.deman.frame.setMaximumWidth(self.tamanho_frame)
        self.deman.frame.setMaximumHeight(self.tamanho_frame_h)

    def layout(self, dept, deman):
        self.ativo = 0
        self.deman = deman
        self.dept = dept
        self.deman.frame.setStyleSheet('background-color: #2c7f4f;')
        self.deman.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.deman.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.deman.frame.setObjectName('frame')
        self.deman.frame.setMouseTracking(True)
        self.deman.frame.setVisible(True)
        self.deman.frame.setEnabled(True)
        self.tamanho = self.deman.frame.height()

        self.tabela_maxima = False

        # Criando um frame separado para os labels
        self.deman.header_frame= QtWidgets.QFrame( )
        self.deman.header_frame.setStyleSheet("background-color: transparent;")
        header_layout = QtWidgets.QHBoxLayout(self.deman.header_frame)
        self.deman.header_frame.setFixedHeight(160)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        header_layout.setContentsMargins(0, 0, 0, 0)  # Remove margens
        header_layout.setSpacing(0)  # Remove espaçamento entre widgets
        self.deman.header_frame.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                              QtWidgets.QSizePolicy.Policy.Fixed)
        self.deman.labeltitulo.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        icon = QtGui.QIcon(resource_path('imagens/sgl.ico'))
        pixmap = icon.pixmap(200, 200)
        self.deman.SGL_label.setFixedSize(200, 190)
        self.deman.SGL_label.setPixmap(pixmap)
        self.deman.SGL_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Weight.Bold))
        self.deman.SGL_label.setStyleSheet("background: transparent; color: #2E3D48;")

        self.deman.labeltitulo.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Weight.Bold))
        self.deman.labeltitulo.setStyleSheet("color: #2E3D48;")
        self.deman.labeltitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajustando automaticamente o tamanho do QLabel com base no texto
        self.deman.labeltitulo.adjustSize()

        icon = QtGui.QIcon(resource_path('imagens/ebhseh.ico'))
        pixmap = icon.pixmap(300, 230)
        self.deman.ebserh_label.setFixedSize(300, 300)
        self.deman.ebserh_label.setPixmap(pixmap)
        self.deman.ebserh_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Weight.Bold))
        self.deman.ebserh_label.setStyleSheet("background: transparent;color: #2E3D48;")
        self.deman.ebserh_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        header_layout.addWidget(self.deman.SGL_label)
        header_layout.addWidget(self.deman.labeltitulo)
        header_layout.addWidget(self.deman.ebserh_label)
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.deman.editbarra)
        vertical_layout.addWidget(self.deman.voltar_demandas)
        vertical_layout.addWidget(self.deman.confirmar_new_layout)
        vertical_layout.addWidget(self.deman.confirmar_alt_layout)
        vertical_layout.addWidget(self.deman.excluir_tabela)

        header_layout.addLayout(vertical_layout)
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        vertical_layout.addSpacerItem(spacer)

        header_layout.addWidget(self.deman.label_icone)

        self.deman.confirmar_new_layout.hide()
        self.deman.confirmar_alt_layout.hide()
        self.deman.excluir_tabela.hide()

        self.deman.voltar_demandas.hide()
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.deman.header_frame)  # Adicionando o novo frame

        estilo_tabela = (
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
        self.deman.tabelademan.setStyleSheet(estilo_tabela)

        self.deman.tabelademan.setCornerButtonEnabled(False)  # Desabilita o botão do canto

        self.deman.tabela_edicao.setStyleSheet(estilo_tabela)

        self.deman.tabela_edicao.setCornerButtonEnabled(False)  # Desabilita o botão do canto

        self.deman.btn_filtros.setFixedSize(150,20)
        self.deman.btn_filtros.setStyleSheet(
            'QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')
        search_layout = QtWidgets.QHBoxLayout()
        self.deman.editbarra.setFixedSize(180, 30 )
        self.deman.editbarra.setPlaceholderText("Pesquisar Paciente")
        self.deman.editbarra.setStyleSheet(
            "background-color: white; border: 2px solid #2E3D48; border-radius: 4px; font-size: 12px;"
        )
        self.label_icone = ClickableLabel()

        self.side_bar = QtWidgets.QWidget(self.deman.frame)  # Alterado para usar self.frame
        main_layout.addWidget(self.side_bar)

        self.deman.icone_toke = self.label_icone
        main_layout.addWidget(self.deman.tabelademan)
        main_layout.addWidget(self.deman.tabela_edicao)

        self.deman.preview.setColumnCount(3)
        self.deman.preview.verticalHeader().setVisible(False)
        self.deman.preview.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.deman.preview.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.deman.preview.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.deman.preview.setStyleSheet(
            """
            QTableWidget {
                background-color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: black;
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
                background: black;
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
                background: black;
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
        self.deman.preview.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.deman.preview.hide()

        self.deman.tabela_edicao.hide()
        self.bottom_bar = QtWidgets.QWidget(self.deman.frame)  # Alterado para usar self.frame
        main_layout.addWidget(self.bottom_bar)

        self.deman.frame.setLayout(main_layout)

        # Outer layout
        outer_layout = QVBoxLayout()
        outer_layout.addWidget(self.deman.frame)

        # Definir os botões dentro do frame
        self.definir_btns()

        self.setLayout(outer_layout)
        self.start_mouse_tracking()

    def definir_btns(self):
        self.layout = QVBoxLayout(self.deman.frame)  # Alterado para usar self.frame

        self.top_layout = QtWidgets.QHBoxLayout()

        icon = QtGui.QIcon(resource_path('imagens/download.ico'))
        pixmap = icon.pixmap(30, 30)

        self.toggle_button = ClickableLabel()
        self.toggle_button.setPixmap(pixmap)
        self.toggle_button.setFixedSize(30, 30)
        self.toggle_button.setStyleSheet("border-radius: 10px;"
                                         "color: white;")

        self.toggle_button.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.toggle_button.clicked.connect(self.toggle_table_size)
        self.top_layout.addWidget(self.toggle_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addLayout(self.top_layout)
        self.toggle_button.hide()

        x = self.deman.frame.width()  # Alterado para usar self.frame

        self.bottom_bar.setStyleSheet("background-color: transparent; border: none;")

        bottom_bar_layout = QtWidgets.QHBoxLayout(self.bottom_bar)
        bottom_bar_layout.setContentsMargins(5, 5, 5, 5)
        bottom_bar_layout.setSpacing(5)

        self.data_deman = Ui_data_Demanda()
        self.data_deman.ler_btn_tabela_demanda(self.deman)

        scroll_area = QtWidgets.QScrollArea(self.bottom_bar)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(
            """
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

        scroll_content = QtWidgets.QWidget()
        scroll_area.setWidget(scroll_content)

        scroll_layout = QtWidgets.QHBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)

        btn_add = QtWidgets.QPushButton(" + ")
        btn_add.setFixedWidth(50)
        btn_add.setFixedHeight(40)
        btn_add.clicked.connect(lambda _, scrol=scroll_layout : self.deman.abrir_criar_tabela(scrol, 'criar'))
        style_round = """
            QPushButton {
                background-color: #2E3D48;
                color: white;
                border: 2px solid #2E3D48;
                min-width: 30px;
                min-height: 30px;
                max-width: 30px;
                max-height: 30px;
                font-size: 12px;
                border-radius: 15px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #777;
                border: 2px solid #777;
            }
            QPushButton:pressed {
                background-color: #555;
                border: 2px solid #555;
            }
        """

        btn_add.setStyleSheet(style_round)
        bottom_bar_layout.addWidget(btn_add)

        bottom_bar_layout.addWidget(scroll_area)
        scroll_area.setFixedHeight(50)

        self.deman.scroll_layout = scroll_layout
        self.deman.bottom_bar_layout = bottom_bar_layout

        zipped = zip(self.deman.lista_ordem_tabelas,
                     self.deman.lista_btn,
                     self.deman.lista_titulo,
                     self.deman.lista_ids)

        sorted_data = sorted(zipped, key=lambda x: x[0])

        (self.deman.lista_ordem_tabelas,
         self.deman.lista_btn,
         self.deman.lista_titulo,
         self.deman.lista_ids) = map(list, zip(*sorted_data))

        # Now iterate through the sorted data

        self.acdicionar_btn_demanda(scroll_layout, sorted_data)

        self.bottom_animation = QtCore.QPropertyAnimation(self.bottom_bar, b"geometry")
        self.bottom_animation.setDuration(500)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.side_bar.setStyleSheet("background-color: transparent; border: none; border-radius: 5px;")

        side_bar_layout = QtWidgets.QHBoxLayout(self.side_bar)
        side_bar_layout.setContentsMargins(5, 5, 5, 5)
        side_bar_layout.setSpacing(5)

        self.side_buttons = []

        side_bar_layout.addWidget(self.deman.btn_filtros)
        side_bar_layout.addWidget(self.deman.btn_reservar_leito)
        side_bar_layout.addWidget(self.deman.btnexclu)

        side_bar_layout.addSpacerItem(spacer)

        side_bar_layout.addWidget(self.label_icone)
        side_bar_layout.setContentsMargins(0, 0, 0, 0)  # Remover margens extras
        side_bar_layout.setSpacing(5)  # Ajustar espaçamento entre os widgets


        self.deman.btnexclu.setFixedSize(160, 30)
        self.deman.btn_reservar_leito.setFixedSize(160, 30)
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
        self.deman.btn_reservar_leito.setIcon(QIcon(resource_path("imagens/reservar.ico")))
        self.deman.btn_reservar_leito.setStyleSheet(LAYOUT_BTN)
        self.deman.btnexclu.setIcon(QIcon(resource_path("imagens/excluir.ico")))
        self.deman.btnexclu.setStyleSheet(LAYOUT_BTN)

        icon = QtGui.QIcon(resource_path('imagens/54638.ico'))

        pixmap = icon.pixmap(30, 30)


        self.deman.voltar_demandas.setStyleSheet(LAYOUT_BTN)
        self.deman.confirmar_alt_layout.setStyleSheet(LAYOUT_BTN)
        self.deman.excluir_tabela.setStyleSheet(LAYOUT_BTN)
        self.deman.confirmar_new_layout.setStyleSheet(LAYOUT_BTN)

        self.label_icone.setPixmap(pixmap)
        self.label_icone.setFixedSize(30, 30)
        self.label_icone.setStyleSheet("border-radius: 10px;"
                                       "color: white;")

        self.label_icone.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_icone.clicked.connect(self.toggle_table_size)

        icon = QtGui.QIcon(resource_path('imagens/menu_icon_150667.ico'))

        self.setMouseTracking(True)
        self.deman.tabelademan.setMouseTracking(True)
        self.bottom_bar.setMouseTracking(True)
        self.side_bar.setMouseTracking(True)

        self.is_half_size = False
        self.bottom_bar.setFixedHeight(55)
        self.side_bar.setGeometry(3000, 300, 100, 300)
        self.bottom_bar.show()
        if self.dept != 'NIR' and self.dept != 'Administrador':
            self.bottom_bar.hide()

        self.deman.edicao_menu.setStyleSheet("""
                                                        QMenuBar {
                                                            background-color: transparent;
                                                            color: white;
                                                            spacing: 5px;
                                                        }
                                                        QMenuBar::item {
                                                            background:#2E3D48;
                                                            padding: 15px 15px;
                                                            border: 2px solid transparent;
                                                        }
                                                        QMenuBar::item:selected {
                                                            background: #555;
                                                        }
                                                        QMenu {
                                                            background-color: white;
                                                            color: #444;
                                                        }
                                                    """)
        menus = [
            ("", 2),
        ]

        for title, number in menus:
            # side_bar_layout.addWidget(self.grade.btn_realocar)
            if number == 2:
                menu = QMenu(title, self)
                icon = QIcon("imagens/menu_icon_150667.ico")
                icon = icon.pixmap(30, 30)  # opcional, controle de tamanho
                menu.setIcon(QIcon(icon))

                action_alterar = QAction(QIcon("imagens/alterar.ico"), "Editar Layout da Tabela", self)
                # action_alterar.triggered.connect(self.grade.btn_alterar.click)

                action_excluir = QAction(QIcon("imagens/deletar.ico"), "Deletar Tabela", self)
                # action_excluir.triggered.connect(self.grade.btn_alta.click)

                action_reservar = QAction(QIcon("imagens/configuracoes-_1_.ico"), "Salvar Configurações", self)
                # action_reservar.triggered.connect(self.grade.btn_permuta.click)

                menu.addAction(action_alterar)
                menu.addAction(action_excluir)
                menu.addAction(action_reservar)

            self.deman.edicao_menu.addMenu(menu)

    def acdicionar_btn_demanda(self, scroll_layout,sorted_data):
        print('sorted',sorted_data)
        for order, btn_name, tit, id in sorted_data:
            print(order, btn_name, tit, id)
            btn = DraggableButton(btn_name, self)
            self.deman.lista_dos_btn.append(btn)

            scroll_layout.addWidget(btn)
            btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            btn.setFixedHeight(40)
            btn.setFixedWidth(320)

            self.deman.labeltitulo.setText(tit)
            btn.clicked.connect(lambda _, id_=id, titulo=tit,
                                       btn_=btn: self.deman.abrir_tabela(self.deman.mainwindow,
                                                                         id_, titulo, btn_))
        print('analisa', self.deman.lista_dos_btn)
