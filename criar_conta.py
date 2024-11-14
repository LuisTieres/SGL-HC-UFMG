# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: criar_conta.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import mysql.connector
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
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
        self.form = Form
        self.frame = QtWidgets.QFrame(parent=self.form)
        self.frame.setGeometry(QtCore.QRect(30, 40, 511, 421))
        self.frame.setStyleSheet('background-color: rgba(0, 0, 0,0.2);\nborder: 2px solid while;\n                               border-radius: 10px;')
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.frame.show()
        self.user = QtWidgets.QLineEdit(parent=self.frame)
        self.user.setGeometry(QtCore.QRect(30, 20, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.user.setFont(font)
        self.user.setStyleSheet('color: rgb(255, 255, 255);')
        self.user.setText('')
        self.user.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.user.setObjectName('user')
        self.password = QtWidgets.QLineEdit(parent=self.frame)
        self.password.setGeometry(QtCore.QRect(30, 150, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.password.setFont(font)
        self.password.setStyleSheet('color: rgb(255, 255, 255);')
        self.password.setFrame(True)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password.setObjectName('password')
        self.login_2 = QtWidgets.QPushButton(parent=self.frame)
        self.login_2.setGeometry(QtCore.QRect(220, 330, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.login_2.setFont(font)
        self.login_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.login_2.setStyleSheet('QPushButton{\nbackground-color: rgb(0, 0, 0);\n    color: rgb(255, 255, 255);\n    border-radius:10px;\n}\nQPushButton:hover{\n    background-color: rgb(255, 255, 255);\n    color: rgb(0, 0, 0);\n}')
        self.login_2.setObjectName('login_2')
        self.login_2.clicked.connect(self.criar_conta)
        self.password_2 = QtWidgets.QLineEdit(parent=self.frame)
        self.password_2.setGeometry(QtCore.QRect(30, 210, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.password_2.setFont(font)
        self.password_2.setStyleSheet('color: rgb(255, 255, 255);')
        self.password_2.setText('')
        self.password_2.setFrame(True)
        self.password_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password_2.setObjectName('password_2')
        self.password_2.textChanged.connect(self.habilitar_botao_login)
        self.password.textChanged.connect(self.habilitar_botao_login)
        self.comboBox = QtWidgets.QComboBox(parent=self.frame)
        self.comboBox.setGeometry(QtCore.QRect(150, 280, 161, 22))
        self.comboBox.setStyleSheet('background-color: rgb(0, 0, 0);\n    color: rgb(255, 255, 255);\n    border-radius:10px;')
        self.comboBox.setObjectName('comboBox')
        self.comboBox.addItem('')
        self.comboBox.setItemText(0, '')
        self.comboBox.addItem('')
        self.comboBox.addItem('')
        self.comboBox.addItem('')
        self.comboBox.addItem('')
        self.comboBox.addItem('')
        self.comboBox.addItem('')
        self.comboBox.addItem('')
        self.comboBox.addItem('')
        self.comboBox.currentIndexChanged.connect(self.habilitar_botao_login)
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(30, 280, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet('border:none;\nbackground-color: none;')
        self.label.setObjectName('label')
        self.user_2 = QtWidgets.QLineEdit(parent=self.frame)
        self.user_2.setGeometry(QtCore.QRect(30, 80, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.user_2.setFont(font)
        self.user_2.setStyleSheet('color: rgb(255, 255, 255);')
        self.user_2.setText('')
        self.user_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.user_2.setObjectName('user_2')
        self.user_2.textChanged.connect(self.check_space)
        self.state = True
        self.state_2 = True
        icon = QtGui.QIcon('escondido.png')
        pixmap = icon.pixmap(25, 25)
        self.show_password_checkbox = ClickableLabel(parent=self.frame)
        self.show_password_checkbox.setPixmap(pixmap)
        self.show_password_checkbox.setGeometry(QtCore.QRect(330, 150, 50, 31))
        self.show_password_checkbox.setStyleSheet('border:none;background-color: transparent;')
        self.show_password_checkbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.show_password_checkbox.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        self.show_password_checkbox.clicked.connect(self.toggle_password_visibility)
        self.show_password_checkbox_2 = ClickableLabel(parent=self.frame)
        self.show_password_checkbox_2.setPixmap(pixmap)
        self.show_password_checkbox_2.setGeometry(QtCore.QRect(330, 210, 50, 31))
        self.show_password_checkbox_2.setStyleSheet('border:none;background-color: transparent;')
        self.show_password_checkbox_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.show_password_checkbox_2.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        self.show_password_checkbox_2.clicked.connect(self.toggle_password_visibility_2)
        self.retranslateUi(Form)
        for widget in self.frame.findChildren(QtWidgets.QWidget):
            widget.show()
        self.warning_label = QtWidgets.QLabel(self.frame)
        self.warning_label.setStyleSheet('color: red;border:none;background-color: transparent;')
        self.habilitar_botao_login()
        self.warning_label.setGeometry(QtCore.QRect(30, 115, 281, 31))
        self.user.textChanged.connect(self.habilitar_botao_login)
        self.user_2.textChanged.connect(self.habilitar_botao_login)
        self.btn_voltar = QtWidgets.QPushButton('Voltar', parent=Form)
        self.btn_voltar.setGeometry(QtCore.QRect(3, 10, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_voltar.setFont(font)
        self.btn_voltar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_voltar.setStyleSheet('QPushButton{\nbackground-color: rgb(0, 0, 0);\n    color: rgb(255, 255, 255);\n    border-radius:10px;\n}\nQPushButton:hover{\n    background-color: rgb(255, 255, 255);\n    color: rgb(0, 0, 0);\n}')
        self.btn_voltar.setObjectName('login_2')
        self.btn_voltar.clicked.connect(self.voltar)
        self.btn_voltar.show()

    def voltar(self):
        self.frame.hide()
        self.tela.frame.show()
        self.tela.label.show()
        self.btn_voltar.hide()

    def habilitar_botao_login(self):
        if self.comboBox.currentText() == '' or len(self.user.text()) == 0 or len(self.user_2.text()) == 0 or (len(self.password.text()) == 0) or (len(self.password_2.text()) == 0):
            self.login_2.setEnabled(False)
        else:
            self.login_2.setEnabled(True)

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

    def toggle_password_visibility_2(self):
        if self.state_2 == True:
            self.password_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            icon = QtGui.QIcon('olho.png')
            pixmap = icon.pixmap(25, 25)
            self.show_password_checkbox_2.setPixmap(pixmap)
            self.state_2 = False
        else:
            self.password_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            icon = QtGui.QIcon('escondido.png')
            pixmap = icon.pixmap(25, 25)
            self.show_password_checkbox_2.setPixmap(pixmap)
            self.state_2 = True

    def check_space(self, text):
        if ' ' in text:
            self.warning_label.show()
            self.warning_label.setText('O login não pode conter espaços.')
            self.login_2.setEnabled(False)
        else:
            self.warning_label.hide()
            self.warning_label.clear()
            self.login_2.setEnabled(True)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.user.setPlaceholderText(_translate('Form', 'Nome Completo'))
        self.password.setPlaceholderText(_translate('Form', 'Senha'))
        self.login_2.setText(_translate('Form', 'Criar Conta'))
        self.password_2.setPlaceholderText(_translate('Form', 'Repita a Senha'))
        self.comboBox.setItemText(1, _translate('Form', 'NIR'))
        self.comboBox.setItemText(2, _translate('Form', 'Pronto Socorro'))
        self.comboBox.setItemText(3, _translate('Form', 'Administrador'))
        self.comboBox.setItemText(4, _translate('Form', 'Telespectador'))
        self.comboBox.setItemText(5, _translate('Form', 'Bloco Cirúrgico'))
        self.comboBox.setItemText(6, _translate('Form', 'Terapía Intensiva'))
        self.comboBox.setItemText(7, _translate('Form', 'Hemodinâmica'))
        self.label.setText(_translate('Form', 'Departamento'))
        self.user_2.setPlaceholderText(_translate('Form', 'Usuário'))

    def criar_conta(self):
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        cursor = conexao.cursor()
        comando = 'SELECT * FROM cadastros'
        cursor.execute(comando)
        leitura = cursor.fetchall()
        analise = True
        for linha in leitura:
            if len(linha) > 0 and linha[0] == self.user_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText('Usuário já existe!')
                icon = QIcon('warning.ico')
                msg_box.setWindowIcon(icon)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply = msg_box.exec()
                analise = False
                self.user.clear()
                self.user_2.clear()
                self.password.clear()
                self.password_2.clear()
                self.comboBox.setCurrentIndex(0)
        cursor.close()
        conexao.close()
        if analise == True:
            conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
            cursor = conexao.cursor()
            usuario = self.user_2.text()
            name = self.user.text()
            senha = self.password.text()
            dep = self.comboBox.currentText()
            comando = f'INSERT INTO cadastros (user,Nome, senha, departamento,analise) VALUES ("{usuario}","{name}", "{senha}", "{dep}",False)'
            cursor.execute(comando)
            conexao.commit()
            cursor.close()
            conexao.close()
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('Conta Cadastrada com Sucesso! Aguarde o Administrador confirmar o acesso.')
            icon = QIcon('warning.ico')
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply = msg_box.exec()