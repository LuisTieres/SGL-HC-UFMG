# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: conta_do_usuario.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import mysql.connector
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFrame, QLabel, QWidget, QScrollArea, QMessageBox, QLineEdit, QFileDialog
from PyQt6.QtCore import Qt, QSettings, QStandardPaths, QFile
from PyQt6.QtGui import QIcon, QPixmap

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
        self.frame.setGeometry(QtCore.QRect(400, 50, 506, 501))
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.tela.janela_conta_do_usuario = self.frame
        self.frame.setCursor(Qt.CursorShape.OpenHandCursor)
        self.frame.mousePressEvent = lambda event, frame=self.frame: self.mousePressEvent(event, frame)
        self.frame.mouseReleaseEvent = lambda event, frame=self.frame: self.mouseReleaseEvent(event, frame)
        self.frame.mouseMoveEvent = lambda event, frame=self.frame: self.mouseMoveEvent(event, frame)
        self.label_icone = QtWidgets.QLabel(parent=self.frame)
        self.label_icone.setGeometry(QtCore.QRect(40, 39, 131, 121))
        self.label_icone.setStyleSheet('\nborder: 2px solid #2E3D48;\nborder-radius: 10px;')
        self.label_icone.setText('')
        self.label_icone.setObjectName('label_icone')
        self.btn_altera_foto = QtWidgets.QPushButton(parent=self.frame)
        self.btn_altera_foto.setGeometry(QtCore.QRect(40, 170, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_altera_foto.setFont(font)
        self.btn_altera_foto.setStyleSheet('QPushButton {\n                                border: 2px solid #2E3D48;\n                                border-radius: 10px;\n                                background-color: #FFFFFF;\n                                color: #2E3D48;\n                            }\n\n                            QPushButton:hover {\n                                background-color: #DDDDDD;  /* Change this to your desired hover color */\n                                color: rgb(0, 0, 0);\n                            }\n\n                            QPushButton:pressed {\n                                background-color: #2E3D48;  /* Change this to your desired pressed color */\n                                color: #FFFFFF;\n                            }')
        self.btn_altera_foto.setObjectName('btn_altera_foto')
        self.btn_altera_foto.clicked.connect(self.abrir_dialogo_imagem)
        self.frame_2 = QtWidgets.QFrame(parent=self.frame)
        self.frame_2.setGeometry(QtCore.QRect(20, 220, 451, 41))
        self.frame_2.setStyleSheet('background-color: white;\ncolor: black;\nborder: 2px solid #2E3D48;\nborder-radius: 10px;')
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName('frame_2')
        self.label_nome = QtWidgets.QLabel(parent=self.frame_2)
        self.label_nome.setGeometry(QtCore.QRect(20, 14, 37, 16))
        self.label_nome.setStyleSheet('border:none;\n')
        self.label_nome.setObjectName('label_nome')
        self.label_name = QtWidgets.QLineEdit(parent=self.frame_2)
        self.label_name.setGeometry(QtCore.QRect(60, 10, 341, 21))
        self.label_name.setStyleSheet('border: none;\n')
        self.label_name.setReadOnly(True)
        self.label_name.setText('')
        self.label_name.setObjectName('label_name')
        self.btn_altera_name = ClickableLabel(parent=self.frame_2)
        self.btn_altera_name.setGeometry(QtCore.QRect(410, 10, 31, 23))
        self.btn_altera_name.setText('')
        self.btn_altera_name.setStyleSheet('ClickableLabel {\nborder: 2px solid #2E3D48;\nborder-radius: 10px;\nbackground-color: #FFFFFF;\ncolor: #2E3D48;\n}\n\nClickableLabel:hover {\nbackground-color: #DDDDDD;  /* Change this to your desired hover color */\ncolor: rgb(0, 0, 0);\n}\n\nClickableLabel:pressed {\nbackground-color: #2E3D48;  /* Change this to your desired pressed color */\ncolor: #FFFFFF;\n}')
        icon = QIcon('ferramenta-lapis.ico')
        pixmap = icon.pixmap(16, 16)
        self.btn_altera_name.setPixmap(pixmap)
        self.btn_altera_name.setObjectName('btn_altera_name')
        self.frame_3 = QtWidgets.QFrame(parent=self.frame)
        self.frame_3.setGeometry(QtCore.QRect(20, 280, 451, 41))
        self.frame_3.setStyleSheet('background-color: white;\ncolor: black;\nborder: 2px solid #2E3D48;\nborder-radius: 10px;')
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName('frame_3')
        self.label_login_2 = QtWidgets.QLabel(parent=self.frame_3)
        self.label_login_2.setGeometry(QtCore.QRect(20, 14, 37, 16))
        self.label_login_2.setStyleSheet('border:none;\n')
        self.label_login_2.setObjectName('label_login_2')
        self.label_login = QtWidgets.QLineEdit(parent=self.frame_3)
        self.label_login.setGeometry(QtCore.QRect(60, 10, 341, 21))
        self.label_login.setStyleSheet('border: none;\n')
        self.label_login.setReadOnly(True)
        self.label_login.setText('')
        self.label_login.setObjectName('label_login')
        self.btn_altera_login = ClickableLabel(parent=self.frame_3)
        self.btn_altera_login.setGeometry(QtCore.QRect(410, 10, 31, 23))
        self.btn_altera_login.setText('')
        self.btn_altera_login.setStyleSheet('ClickableLabel {\nborder: 2px solid #2E3D48;\nborder-radius: 10px;\nbackground-color: #FFFFFF;\ncolor: #2E3D48;\n}\n\nClickableLabel:hover {\nbackground-color: #DDDDDD;  /* Change this to your desired hover color */\ncolor: rgb(0, 0, 0);\n}\n\nClickableLabel:pressed {\nbackground-color: #2E3D48;  /* Change this to your desired pressed color */\ncolor: #FFFFFF;\n}')
        icon = QIcon('ferramenta-lapis.ico')
        pixmap = icon.pixmap(20, 20)
        self.btn_altera_login.setPixmap(pixmap)
        self.btn_altera_login.setObjectName('btn_altera_login')
        self.frame_4 = QtWidgets.QFrame(parent=self.frame)
        self.frame_4.setGeometry(QtCore.QRect(20, 340, 451, 41))
        self.frame_4.setStyleSheet('background-color: white;\ncolor: black;\nborder: 2px solid #2E3D48;\nborder-radius: 10px;')
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName('frame_4')
        self.label_senha_2 = QtWidgets.QLabel(parent=self.frame_4)
        self.label_senha_2.setGeometry(QtCore.QRect(20, 14, 37, 16))
        self.label_senha_2.setStyleSheet('border:none;\n')
        self.label_senha_2.setObjectName('label_senha_2')
        self.password = QtWidgets.QLineEdit(parent=self.frame_4)
        self.password.setGeometry(QtCore.QRect(60, 10, 161, 21))
        self.password.setStyleSheet('border: none;\n')
        self.password.setFrame(True)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password.setObjectName('password')
        self.password.setReadOnly(True)
        self.password.setText('')
        self.password.setObjectName('password')
        self.state = True
        icon = QtGui.QIcon('escondido.png')
        pixmap = icon.pixmap(25, 25)
        self.show_password_checkbox = ClickableLabel(parent=self.frame_4)
        self.show_password_checkbox.setPixmap(pixmap)
        self.show_password_checkbox.setGeometry(QtCore.QRect(350, 7, 50, 31))
        self.show_password_checkbox.setStyleSheet('border:none;background-color: transparent;')
        self.show_password_checkbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.show_password_checkbox.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        self.show_password_checkbox.clicked.connect(self.toggle_password_visibility)
        self.btn_altera_senha = ClickableLabel(parent=self.frame_4)
        self.btn_altera_senha.setGeometry(QtCore.QRect(410, 10, 31, 23))
        self.btn_altera_senha.setStyleSheet('ClickableLabel {\nborder: 2px solid #2E3D48;\nborder-radius: 10px;\nbackground-color: #FFFFFF;\ncolor: #2E3D48;\n}\n\nClickableLabel:hover {\nbackground-color: #DDDDDD;  /* Change this to your desired hover color */\ncolor: rgb(0, 0, 0);\n}\n\nClickableLabel:pressed {\nbackground-color: #2E3D48;  /* Change this to your desired pressed color */\ncolor: #FFFFFF;\n}')
        icon = QIcon('ferramenta-lapis.ico')
        pixmap = icon.pixmap(20, 20)
        self.btn_altera_senha.setPixmap(pixmap)
        self.btn_altera_senha.setText('')
        self.btn_altera_senha.setObjectName('btn_altera_senha')
        self.btn_altera_senha.clicked.connect(lambda: self.habilitar(self.password))
        self.btn_altera_login.clicked.connect(lambda: self.habilitar(self.label_login))
        self.btn_altera_name.clicked.connect(lambda: self.habilitar(self.label_name))
        self.pushButton = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton.setGeometry(QtCore.QRect(390, 420, 75, 23))
        self.pushButton.setStyleSheet('QPushButton {\n                                border: 2px solid #2E3D48;\n                                border-radius: 10px;\n                                background-color: #FFFFFF;\n                                color: #2E3D48;\n                            }\n\n                            QPushButton:hover {\n                                background-color: #DDDDDD;  /* Change this to your desired hover color */\n                                color: rgb(0, 0, 0);\n                            }\n\n                            QPushButton:pressed {\n                                background-color: #2E3D48;  /* Change this to your desired pressed color */\n                                color: #FFFFFF;\n                            }')
        self.pushButton.setObjectName('pushButton')
        self.pushButton.clicked.connect(self.confirmar_alteracoes)
        self.retranslateUi(Form)
        for widget in self.frame.findChildren(QtWidgets.QWidget):
            widget.show()
        self.frame.show()
        self.load()
        self.atualizar_conta()

    def abrir_dialogo_imagem(self):
        self.filename, _ = QFileDialog.getOpenFileName(self.form, 'Selecionar Imagem', '', 'Arquivos de Imagem (*.jpg *.png *.bmp *.jpeg)')
        if self.filename:
            pixmap = QPixmap(self.filename)
            self.label_icone.setPixmap(pixmap)
            self.label_icone.setScaledContents(True)

    def habilitar(self, line_edit):
        analise = line_edit.isReadOnly()
        line_edit.setReadOnly(not analise)

    def atualizar_conta(self):
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        comando = 'SELECT * FROM cadastros'
        cursor.execute(comando)
        leitura = cursor.fetchall()
        for linha in leitura:
            if self.tela.user == linha[0]:
                self.label_name.setText(linha[1])
                self.label_login.setText(linha[0])
                self.password.setText(linha[2])
                break
        cursor.close()
        conexao.close()
        caminho_imagem = 'imagem_do_usuario.png'
        if QFile.exists(caminho_imagem):
            pixmap = QPixmap(caminho_imagem)
            self.label_icone.setPixmap(pixmap)
            self.label_icone.setScaledContents(True)

    def confirmar_alteracoes(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText('Confirmar Alterações?')
        icon = QIcon('warning.ico')
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
            cursor = conexao.cursor()
            comando = 'UPDATE cadastros SET senha = %s, Nome = %s, user = %s WHERE user = %s'
            valores = (self.password.text(), self.label_name.text(), self.label_login.text(), self.tela.user)
            cursor.execute(comando, valores)
            cursor.close()
            conexao.close()
            if self.filename:
                caminho_destino = 'imagem_do_usuario.png'
                QFile.remove(caminho_destino)
                pixmap = QPixmap(self.filename)
                pixmap.save(caminho_destino)
            self.atualizar_conta()
        if reply == QMessageBox.StandardButton.No:
            self.atualizar_conta()

    def toggle_password_visibility(self):
        if self.state == True:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            icon = QtGui.QIcon('olho.png')
            pixmap = icon.pixmap(25, 25)
            self.show_password_checkbox.setPixmap(pixmap)
            self.state = False
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            icon = QtGui.QIcon('escondido.png')
            pixmap = icon.pixmap(25, 25)
            self.show_password_checkbox.setPixmap(pixmap)
            self.state = True

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.btn_altera_foto.setText(_translate('Form', 'Carregar foto:'))
        self.label_nome.setText(_translate('Form', 'Nome: '))
        self.label_login_2.setText(_translate('Form', 'Login: '))
        self.label_senha_2.setText(_translate('Form', 'Senha: '))
        self.pushButton.setText(_translate('Form', 'Confirmar'))

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