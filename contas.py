# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: contas.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import mysql.connector
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFrame, QLabel, QWidget, QScrollArea, QMessageBox, QLineEdit
from PyQt6.QtCore import Qt, QSettings, QStandardPaths
from PyQt6.QtGui import QIcon

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class Ui_Form(object):

    def setupUi(self, Form, tela):
        self.host_mysql = 'localhost'
        self.user_mysql = ('root',)
        self.password_mysql = 'camileejose'
        self.tela = tela
        self.contas = []
        self.excluir_conta = []
        self.frames = []
        self.settings = QSettings('HC', 'SGL')
        self.form = Form
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setGeometry(QtCore.QRect(400, 50, 543, 600))
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.tela.janela_contas = self.frame
        self.Titulo = QtWidgets.QLabel('Usuários', parent=self.frame)
        self.Titulo.setGeometry(QtCore.QRect(90, 15, 261, 38))
        self.Titulo.setStyleSheet('border:none;')
        font = QtGui.QFont()
        font.setPointSize(30)
        self.Titulo.setFont(font)
        icon = QIcon('silhueta-de-multiplos-usuarios.ico')
        pixmap = icon.pixmap(50, 50)
        self.icone = QtWidgets.QLabel(parent=self.frame)
        self.icone.setPixmap(pixmap)
        self.icone.setGeometry(QtCore.QRect(3, 3, 50, 50))
        self.icone.show()
        self.icone.setStyleSheet('border:none;')
        self.frame.setCursor(Qt.CursorShape.OpenHandCursor)
        self.frame.mousePressEvent = lambda event, frame=self.frame: self.mousePressEvent(event, frame)
        self.frame.mouseReleaseEvent = lambda event, frame=self.frame: self.mouseReleaseEvent(event, frame)
        self.frame.mouseMoveEvent = lambda event, frame=self.frame: self.mouseMoveEvent(event, frame)
        self.scroll_area = QScrollArea(self.frame)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.move(5, 80)
        self.scroll_area.show()
        self.scroll_area.setStyleSheet('border:none;')
        self.scroll_area.setFixedSize(535, 500)
        self.BARRADEPESQUISA = QtWidgets.QLineEdit(parent=self.frame)
        self.BARRADEPESQUISA.setGeometry(QtCore.QRect(5, 55, 360, 21))
        self.BARRADEPESQUISA.setObjectName('BARRADEPESQUISA')
        self.BARRADEPESQUISA.textChanged.connect(self.pesquisar)
        self.BARRADEPESQUISA.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.BARRADEPESQUISA.setPlaceholderText('Pesquisar Usuário')
        self.BARRADEPESQUISA.show()
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_content.setLayout(self.scroll_layout)
        self.add_usuario()
        for widget in self.frame.findChildren(QtWidgets.QWidget):
            widget.show()
        self.frame.show()
        self.load()

    def pesquisar(self, pesquisa):
        for i, (frame, usuarios) in enumerate(self.frames):
            if pesquisa.lower() in usuarios.lower():
                frame.show()
            else:
                frame.hide()

    def add_usuario(self):
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        comando = 'SELECT * FROM cadastros'
        cursor.execute(comando)
        leitura = cursor.fetchall()
        for linha in leitura:
            self.add_frame(linha[0], linha[1], linha[2], linha[3])
        cursor.close()
        conexao.close()

    def add_frame(self, usu_, Usuario, senha, dep):
        frame = QFrame()
        frame.setFixedSize(500, 200)
        usu = QLabel(f'Usuário: {Usuario}', frame)
        font = QtGui.QFont()
        font.setPointSize(15)
        usu.setFont(font)
        usu.setGeometry(5, 5, 450, 30)
        frame.setStyleSheet('border: 2px solid #2E3D48;background-color: white; border-radius: 10px;color: black;')
        senha_label = QtWidgets.QLabel('Senha: ', frame)
        senha_label.setStyleSheet('border:none')
        font = QtGui.QFont()
        font.setPointSize(15)
        senha_label.setFont(font)
        senha_label.setGeometry(5, 50, 100, 30)
        password = QtWidgets.QLineEdit(frame)
        font = QtGui.QFont()
        font.setPointSize(11)
        password.setFont(font)
        password.setGeometry(90, 50, 100, 30)
        password.setStyleSheet('color: black;')
        password.setFrame(True)
        password.setText(senha)
        password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        password.setObjectName('password')
        password.setReadOnly(True)
        icon = QtGui.QIcon('escondido.png')
        pixmap = icon.pixmap(25, 25)
        state = True
        show_password_checkbox = ClickableLabel(parent=frame)
        show_password_checkbox.setPixmap(pixmap)
        show_password_checkbox.setGeometry(QtCore.QRect(200, 50, 50, 31))
        show_password_checkbox.setStyleSheet('border:none;background-color: transparent;')
        self.contas.append((show_password_checkbox, state))
        show_password_checkbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        show_password_checkbox.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        show_password_checkbox.clicked.connect(lambda: self.toggle_password_visibility(password, show_password_checkbox))
        self.scroll_layout.addWidget(frame)
        departamento = QLabel(f'Departamento: {dep}', frame)
        font = QtGui.QFont()
        font.setPointSize(15)
        departamento.setFont(font)
        departamento.setGeometry(5, 100, 450, 30)
        btn_excluir = QtWidgets.QPushButton('Excluir Usuário', parent=frame)
        btn_excluir.setGeometry(QtCore.QRect(5, 150, 150, 23))
        btn_excluir.setToolTip('Excluir Usuário')
        self.excluir_conta.append((btn_excluir, usu_))
        btn_excluir.clicked.connect(lambda: self.excluir(usu_, btn_excluir))
        btn_excluir.setStyleSheet('\n                        QPushButton {\n                            border: 2px solid #2E3D48;\n                            border-radius: 10px;\n                            background-color: #FFFFFF;\n                            color: #2E3D48;\n                        }\n\n                        QPushButton:hover {\n                            background-color: #DDDDDD;  /* Change this to your desired hover color */\n                            color: rgb(0, 0, 0);\n                        }\n\n                        QPushButton:pressed {\n                            background-color: #2E3D48;  /* Change this to your desired pressed color */\n                            color: #FFFFFF;\n                        }\n                    ')
        self.frames.append((frame, Usuario))

    def toggle_password_visibility(self, password_line_edit, show_password_checkbox1):
        for i, (show_checkbox, state) in enumerate(self.contas):
            if show_checkbox == show_password_checkbox1:
                if state:
                    password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
                    icon = QtGui.QIcon('olho.png')
                else:
                    password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
                    icon = QtGui.QIcon('escondido.png')
                pixmap = icon.pixmap(25, 25)
                show_checkbox.setPixmap(pixmap)
                self.contas[i] = (show_checkbox, not state)

    def excluir(self, usu, btn_excluir):
        for i, (btn_excluir1, usu1) in enumerate(self.excluir_conta):
            print(usu, usu1)
            if btn_excluir1 == btn_excluir and usu == usu1:
                print(usu, usu1, 55)
                conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                cursor = conexao.cursor()
                comando = 'SELECT * FROM cadastros'
                cursor.execute(comando)
                leitura = cursor.fetchall()
                for linha in leitura:
                    if len(linha) > 0 and linha[0] == usu:
                        msg_box = QMessageBox()
                        msg_box.setIcon(QMessageBox.Icon.Information)
                        msg_box.setWindowTitle('AVISO')
                        msg_box.setText(f"O usuário com Nome '{linha[1]}' e user '{linha[0]}' será excluído do software. Confirmar?")
                        icon = QIcon('warning.ico')
                        msg_box.setWindowIcon(icon)
                        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                        reply = msg_box.exec()
                        if reply == QMessageBox.StandardButton.Yes:
                            comando = f'DELETE FROM cadastros WHERE user = "{linha[0]}"'
                            cursor.execute(comando)
                            conexao.commit()
                cursor.close()
                conexao.close()

    def mousePressEvent(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            centralwidget.setCursor(Qt.CursorShape.ClosedHandCursor)
        centralwidget.mouse_offset = event.pos()

    def mouseReleaseEvent(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            centralwidget.setCursor(Qt.CursorShape.OpenHandCursor)

    def mouseMoveEvent(self, event, centralwidget):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = centralwidget.mapToParent(event.pos() - centralwidget.mouse_offset)
            centralwidget.move(new_pos)
            x, y = (new_pos.x(), new_pos.y())

    def load(self):
        if self.settings.contains('tema'):
            font_name = self.settings.value('font', defaultValue='')
            backcolocor = self.settings.value('tema', defaultValue='')
            color = self.settings.value('color', defaultValue='')
            tamanho = int(self.settings.value('tamanho', defaultValue=10))
            self.backcolocor = backcolocor
            self.color = color
            self.frame.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;border: 2px solid #2E3D48;border-radius: 10px;')