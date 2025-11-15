from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt,QTimer
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QComboBox, QVBoxLayout, QSpacerItem, QSizePolicy,QMenuBar, QMenu
from PyQt6.QtGui import QAction, QIcon
import pymysql
import os
import re
import sys
def resource_path(relative_path):
    """Resolve path para PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
class Front_Grade(QtWidgets.QMainWindow):

    def toggle_table_size(self):
        if self.is_half_size:
            screen = QtGui.QGuiApplication.primaryScreen()
            size = screen.size()
            tabela_height = size.height() - 390
            self.grade.tabela_grade.setFixedHeight(tabela_height)
            self.side_bar.show()
            self.bottom_bar.show()
            self.toggle_button.hide()
            for label in self.grade.frame.findChildren(QtWidgets.QLabel):
                label.show()
            for btn in self.grade.frame.findChildren(QtWidgets.QPushButton):
                btn.show()
            self.grade.BARRADEPESQUISA.show()
            download_icon = QtGui.QIcon('imagens/54638.ico')  # Assuming the download icon file exists
            pixmap = download_icon.pixmap(30, 30)
            self.label_icone.setPixmap(pixmap)
            self.grade.header_frame.show()
            self.grade.btn_dowload_senso.hide()
            self.grade.btnfechar.hide()
            self.grade.btn_filtros.hide()
            self.grade.SGL_label.show()
            self.grade.ebserh_label.show()
        else:
            for label in self.grade.frame.findChildren(QtWidgets.QLabel):
                label.hide()
            for btn in self.grade.frame.findChildren(QtWidgets.QPushButton):
                btn.hide()
            screen = QtGui.QGuiApplication.primaryScreen()
            size = screen.size()
            tabela_height = size.height() - 190
            self.grade.tabela_grade.setFixedHeight(tabela_height)
            self.grade.SGL_label.hide()
            self.grade.ebserh_label.hide()
            self.grade.header_frame.hide()

            download_icon = QtGui.QIcon('imagens/download.ico')
            pixmap = download_icon.pixmap(30, 30)
            self.label_icone.setPixmap(pixmap)
            self.grade.BARRADEPESQUISA.show()
            self.side_bar.show()
            self.bottom_bar.show()
            self.label_icone.show()
        self.is_half_size = not self.is_half_size

    def start_mouse_tracking(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_mouse_position)
        #self.timer.start(100)  # Verifica a cada 100ms

    def check_mouse_position(self):

        self.tamanho_frame = self.grade.frame.width()
        self.tamanho_frame_h = self.grade.frame.height()

        #self.grade.tabela_grade.setFixedHeight(self.grade.frame.height() - 300)

        self.grade.frame.setMaximumWidth(self.tamanho_frame)
        self.grade.frame.setMaximumHeight(self.tamanho_frame_h)

        self.grade.widget_monitora.setMaximumWidth(self.tamanho_frame)
        self.grade.widget_monitora.setMaximumHeight(self.tamanho_frame_h)

        pos = self.mapFromGlobal(QtGui.QCursor.pos())

        tamanho_frame = self.grade.frame.width()
        tamanho_frame_h = self.grade.frame.height()
        print('amg', tamanho_frame, tamanho_frame_h)
        if pos.x() >= self.grade.frame.width() - 20:
            self.show_side_bar()
        elif pos.x() < self.grade.frame.width() - 150:
            self.hide_side_bar()

    def show_side_bar(self):
        self.side_animation.setStartValue(QtCore.QRect(self.side_bar.x(), 300, 220, 300))
        self.side_animation.setEndValue(QtCore.QRect(self.grade.frame.width() - 220, 300, 220, 300))
        self.side_animation.start()

    def hide_side_bar(self):
        self.side_animation.setStartValue(QtCore.QRect(self.side_bar.x(), 300, 200, 300))
        self.side_animation.setEndValue(QtCore.QRect(self.grade.frame.width(), 300, 200, 300))
        self.side_animation.start()

        icon = QtGui.QIcon('imagens/menu_icon_150667.ico')

    def on_botao_clicado(self):
        botao_clicado = self.sender()
        for btn in self.botoes:
            if btn == botao_clicado:
                btn.setStyleSheet("background-color: white; color: black; border: none; padding: 5px;")
            else:
                btn.setStyleSheet("background-color: #ccc; color: black; border: none; padding: 5px;")

    def on_side_btn_clicado(self):
        botao_clicado = self.sender()
        for btn in self.side_buttons:
            if btn == botao_clicado:
                btn.setStyleSheet("background-color: white; color: black; border: none; padding: 5px;")
            else:
                btn.setStyleSheet("background-color: #555; color: white; border: none; padding: 5px;")

    def layout(self, dept, grade):

        self.ativo = 0
        self.grade = grade
        self.dept = dept

        self.grade.frame.setStyleSheet('background-color: #2c7f4f;')
        self.grade.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.grade.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.grade.frame.setObjectName('frame')
        self.grade.frame.setMouseTracking(True)
        self.grade.frame.setVisible(True)
        self.grade.frame.setEnabled(True)
        self.tamanho = self.grade.frame.height()

        self.grade.header_frame= QtWidgets.QFrame( )
        self.grade.header_frame.setStyleSheet("background-color: transparent;")
        header_layout = QtWidgets.QHBoxLayout(self.grade.header_frame)
        self.grade.header_frame.setFixedHeight(175)

        icon = QtGui.QIcon('imagens/sgl.ico')
        pixmap = icon.pixmap(200, 200)
        self.grade.SGL_label.setFixedSize(300, 190)
        self.grade.SGL_label.setPixmap(pixmap)
        self.grade.SGL_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Weight.Bold))
        self.grade.SGL_label.setStyleSheet("background: transparent; color: #2E3D48;")

        self.grade.TITULO_CTI.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Weight.Bold))
        self.grade.TITULO_CTI.setStyleSheet("color: #2E3D48;")
        self.grade.TITULO_CTI.setFixedSize(1000, 150)
        self.grade.TITULO_CTI.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QtGui.QIcon('imagens/ebhseh.ico')
        pixmap = icon.pixmap(300, 230)
        self.grade.ebserh_label.setFixedSize(300, 300)
        self.grade.ebserh_label.setPixmap(pixmap)
        self.grade.ebserh_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Weight.Bold))
        self.grade.ebserh_label.setStyleSheet("background: transparent;color: #2E3D48;")
        self.grade.ebserh_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        header_layout.addWidget(self.grade.SGL_label)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        header_layout.addWidget(self.grade.TITULO_CTI)
        header_layout.addWidget(self.grade.ebserh_label)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.grade.BARRADEPESQUISA)
        header_layout.addLayout(vertical_layout)
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        vertical_layout.addSpacerItem(spacer)

        header_layout.addWidget(self.grade.label_icone)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.grade.header_frame)

        self.grade.tabela_grade.setStyleSheet(
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
        self.grade.tabela_grade.setCornerButtonEnabled(False)

        screen = QtGui.QGuiApplication.primaryScreen()
        size = screen.size()
        tabela_height = size.height() - 390
        self.grade.tabela_grade.setFixedHeight(tabela_height)
        search_layout = QtWidgets.QHBoxLayout()

        self.grade.BARRADEPESQUISA.setFixedSize(150, 30)
        self.grade.BARRADEPESQUISA.setPlaceholderText("Pesquisar Paciente")
        self.grade.BARRADEPESQUISA.setStyleSheet("background-color: white; border: 2px solid #2E3D48; border-radius: 4px; font-size: 12px;")

        self.label_icone = ClickableLabel()
        search_layout.addWidget(self.label_icone)
        self.side_bar = QtWidgets.QWidget(self.grade.frame)

        self.grade.widget_monitora.hide()

        main_layout.addWidget(self.side_bar)
        main_layout.addWidget(self.grade.tabela_grade)
        main_layout.addWidget(self.grade.widget_monitora)

        self.bottom_bar = QtWidgets.QWidget(self.grade.frame)

        main_layout.addWidget(self.bottom_bar)
        self.grade.frame.setLayout(main_layout)

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(self.grade.frame)

        self.bottom_bar.show()

        self.definir_btns()

        self.setLayout(outer_layout)
        self.start_mouse_tracking()

        self.bottom_bar.raise_()

    def definir_btns(self):
        self.layout = QVBoxLayout(self.grade.frame)  # Alterado para usar self.frame

        self.top_layout = QtWidgets.QHBoxLayout()

        icon = QtGui.QIcon('imagens/download.ico')
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

        x = self.grade.frame.width()

        self.bottom_bar.setStyleSheet("background-color: transparent; border: none;")
        self.grade.widget_monitora.setStyleSheet("background-color: transparent; border: none;")

        self.botoes = []

        conexao = pymysql.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        comando = 'SELECT * FROM new_grades '
        cursor.execute(comando)
        rows = cursor.fetchall()
        cursor.close()
        conexao.close()

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
        btn_add.setFixedWidth(50)  # ou outro valor adequado
        btn_add.setFixedHeight(40)
        #btn_add.clicked.connect(lambda _, scrol=scroll_layout: self.grade.abrir_editor_tabela(scrol))
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

        bottom_bar_layout = QtWidgets.QHBoxLayout(self.bottom_bar)
        bottom_bar_layout.setContentsMargins(5, 5, 5, 5)
        bottom_bar_layout.setSpacing(5)
        btn_add.setStyleSheet(style_round)

        self.grade.bottom_bar_layout = bottom_bar_layout
        self.grade.bottom_bar_layout.addWidget(btn_add)

        self.grade.bottom_bar_layout.addWidget(scroll_area)
        scroll_area.setFixedHeight(50)

        from database_Grade import Ui_data_Grade
        self.data_grade = Ui_data_Grade()
        self.data_grade.ler_btn_tabela_Grade(self.grade)

        for cont, btn_name in enumerate(self.grade.lista_btn):
            btn = QtWidgets.QPushButton(btn_name)
            self.grade.lista_dos_btn.append(btn)

            scroll_layout.addWidget(btn)
            btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            btn.setFixedHeight(40)
            btn.setFixedWidth(320)

            self.grade.TITULO_CTI.setText(self.grade.lista_titulo[cont])
            btn.clicked.connect(lambda _, id_=self.grade.lista_ids[cont], titulo=self.grade.lista_titulo[cont],
                                       btn_=btn: self.grade.abri_cti(self.grade.form, id_, titulo, btn_))

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.side_bar.setStyleSheet("background-color: transparent; border: none; border-radius: 5px;")

        side_bar_layout = QtWidgets.QHBoxLayout(self.side_bar)
        side_bar_layout.setContentsMargins(5, 5, 5, 5)
        side_bar_layout.setSpacing(5)

        self.side_buttons = []

        side_bar_layout.addWidget(self.grade.btn_permuta_diferentes_tabelas)
        side_bar_layout.addWidget(self.grade.btn_permuta)
        side_bar_layout.addWidget(self.grade.deixar_vago)
        side_bar_layout.addWidget(self.grade.btn_ocupar_leito)
        side_bar_layout.addWidget(self.grade.btn_alta)

        stilo = """
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

        self.grade.btn_alta.setStyleSheet(stilo)
        self.grade.deixar_vago.setStyleSheet(stilo)
        self.grade.btn_ocupar_leito.setStyleSheet(stilo)
        self.grade.btn_permuta.setStyleSheet(stilo)
        self.grade.btn_permuta_diferentes_tabelas.setStyleSheet(stilo)

        side_bar_layout.addSpacerItem(spacer)

        side_bar_layout.addWidget(self.label_icone)

        self.side_buttons = []

        self.grade.btn_alta.setFixedSize(210, 30)
        self.grade.btn_permuta.setFixedSize(210, 30)
        self.grade.deixar_vago.setFixedSize(210, 30)
        self.grade.btn_ocupar_leito.setFixedSize(210, 30)
        self.grade.btn_alta.hide()

        icon = QtGui.QIcon('imagens/54638.ico')

        pixmap = icon.pixmap(30, 30)

        self.label_icone.setPixmap(pixmap)
        self.label_icone.setFixedSize(30, 30)
        self.label_icone.setStyleSheet("border-radius: 10px;"
                                       "color: white;")

        self.label_icone.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_icone.clicked.connect(self.toggle_table_size)

        self.inicio = 1
        self.inicio2 = 1
        self.setMouseTracking(True)
        self.grade.tabela_grade.setMouseTracking(True)
        self.bottom_bar.setMouseTracking(True)
        self.side_bar.setMouseTracking(True)

        self.is_half_size = False
        self.bottom_bar.setGeometry(300, self.grade.frame.height() - 60, x-500, 60)
        self.side_bar.setGeometry(3000, 300, 100, 300)
        self.side_bar.show()
        self.bottom_bar.show()
