import pymysql
from ldap3 import Server, Connection, ALL, SUBTREE
import ast
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
import sys
import os
from database_Demandas import Ui_data_Demanda

from PyQt6 import QtCore, QtGui, QtWidgets
from conecao_api import Ui_API
def resource_path(relative_path):
    """Resolve path para PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

variaveis = {
    "AUTH_LDAP_SERVER_URI": "ldap://10.36.2.21",
    "AUTH_LDAP_BIND_DN": "CN=TAGS,OU=Servicos,OU=Usuarios,OU=HCMG,OU=EBSERH,DC=ebserhnet,DC=ebserh,DC=gov,DC=br",
    "AUTH_LDAP_BIND_PASSWORD": "T4g5@2022!",
    "AUTH_LDAP_BASE_DN": "OU=Usuarios,OU=HCMG,OU=EBSERH,DC=ebserhnet,DC=ebserh,DC=gov,DC=br"
}

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class Ui_Form(object):

    def setupUi(self, Form, tela):
        self.hostmysql = '127.0.0.1'
        self.usermysql = 'root'
        self.passwordmysql = 'senhasgl'
        self.databasemysql = 'sgl'

        self.data_deman = Ui_data_Demanda()

        self.api = Ui_API()
        print('1')
        self.host_mysql = 'localhost'
        self.user_mysql = ('root',)
        self.password_mysql = 'camileejose'
        self.tela = tela
        self.form = Form
        self.frame = QtWidgets.QFrame(parent=self.form)
        self.frame.setGeometry(QtCore.QRect(30, 40, 451, 361))
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
        self.user.show()

        self.password = QtWidgets.QLineEdit(parent=self.frame)
        self.password.setGeometry(QtCore.QRect(30, 80, 281, 31))

        font = QtGui.QFont()
        font.setPointSize(11)
        print('1')
        self.password.setFont(font)
        self.password.setStyleSheet('color: rgb(255, 255, 255);')
        self.password.setFrame(True)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password.setObjectName('password')
        self.password.show()

        self.login_2 = QtWidgets.QPushButton(parent=self.frame)
        self.login_2.setGeometry(QtCore.QRect(220, 230, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.login_2.setFont(font)
        self.login_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.login_2.setStyleSheet('QPushButton{\nbackground-color: rgb(0, 0, 0);\n    color: rgb(255, 255, 255);\n    border-radius:10px;\n}\nQPushButton:hover{\n    background-color: rgb(255, 255, 255);\n    color: rgb(0, 0, 0);\n}')
        self.login_2.setObjectName('login_2')
        self.login_2.clicked.connect(self.criar_conta)
        self.login_2.show()

        print('1')
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(30, 280, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet('border:none;\nbackground-color: none;')
        self.label.setObjectName('label')

        self.user_2 = QtWidgets.QLineEdit(parent=self.frame)
        self.user_2.setGeometry(QtCore.QRect(30, 150, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.user_2.setFont(font)
        self.user_2.setStyleSheet('color: rgb(255, 255, 255);')
        self.user_2.setText('')
        self.user_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.user_2.setObjectName('user_2')
        self.user_2.textChanged.connect(self.check_space)
        self.user_2.show()

        print('1')
        self.state = True
        self.state_2 = True
        print(3)
        #icon = QIcon(resource_path('imagens/escondido.png'))
        icon = QtGui.QIcon(resource_path('imagens/escondido.png'))

        pixmap = icon.pixmap(25, 25)
        print(3)
        self.show_password_checkbox = ClickableLabel(parent=self.frame)
        self.show_password_checkbox.setPixmap(pixmap)
        self.show_password_checkbox.setGeometry(QtCore.QRect(330, 80, 50, 31))
        self.show_password_checkbox.setStyleSheet('border:none;background-color: transparent;')
        self.show_password_checkbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.show_password_checkbox.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        self.show_password_checkbox.clicked.connect(self.toggle_password_visibility)
        self.show_password_checkbox.show()

        print(3)
        self.retranslateUi(Form)

        print('1')
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

        print('1')
    def voltar(self):
        self.frame.hide()
        self.tela.frame.show()
        self.tela.label.show()
        self.btn_voltar.hide()

    def habilitar_botao_login(self):
        if len(self.user.text()) == 0 or len(self.user_2.text()) == 0 or (len(self.password.text()) == 0) :
            self.login_2.setEnabled(False)
        else:
            self.login_2.setEnabled(True)

    def toggle_password_visibility(self):
        if self.state == True:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            icon = QIcon(resource_path('imagens/olho.png'))
            pixmap = icon.pixmap(25, 25)
            self.show_password_checkbox.setPixmap(pixmap)
            self.state = False
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            icon = QIcon(resource_path('imagens/escondido.png'))
            pixmap = icon.pixmap(25, 25)
            self.show_password_checkbox.setPixmap(pixmap)
            self.state = True


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
        self.user.setPlaceholderText(_translate('Form', 'Login do Usuário Adm'))
        self.password.setPlaceholderText(_translate('Form', 'Senha do Usuário Adm'))
        self.login_2.setText(_translate('Form', 'Registar'))
        self.label.setText(_translate('Form', 'Departamento'))
        self.user_2.setPlaceholderText(_translate('Form', 'Login do novo Usuário'))

    def verificar_adm(self, usuario):
        try:
            leitura = self.data_deman.ler_cadastros(self)

            if len(leitura) == 0:
                self._mostrar_mensagem('Usuário Administrador não existe!')
                return False

            for linha in leitura:
                if linha[0] == usuario and linha[3] == 'Administrador' and linha[2] == '1':
                    return True

            self._mostrar_mensagem('Usuário não é Adm, então não tem permissão para executar essa ação!')
            return False

        finally:
            cursor.close()
            conexao.close()

    def _mostrar_mensagem(self, texto):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText(texto)
        icon = QIcon(resource_path('imagens/warning.ico'))
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def verfificar_user(self):

        leitura = self.data_deman.ler_cadastros(self)

        for linha in leitura:
            if len(linha) > 0 and linha[0] == self.user_2.text() :
                self.nivel_acesso = linha[3]
                analise = linha[2]
                if analise == '1':
                    self._mostrar_mensagem('Usuário já possui acesso!')

                    analise = False
                    self.user.clear()
                    self.user_2.clear()
                    self.password.clear()
                    return False
                elif analise == '0':
                    return True

        self._mostrar_mensagem('Usuário não solicitou acesso ainda!')

        cursor.close()
        conexao.close()
        return False

    def criar_conta(self):
        if self.verfificar_user():
            verificacao = self.api.verificar_usuario_senha(self.user.text(),self.password.text())

            if verificacao:
                if self.verificar_adm(self.user.text()):
                    #print(buscar_usuario)
                    usuario = self.api.buscar_usuario(self.user_2.text())
                    if usuario:

                        name = usuario['nome']
                        msg_box = QMessageBox()
                        msg_box.setIcon(QMessageBox.Icon.Information)
                        msg_box.setWindowTitle('AVISO')
                        msg_box.setText(
                            f'O usuário com Nome \'{usuario['nome']}\' e user \'{self.user_2.text()}\' solicita acesso para logar no software como usuário \'{self.nivel_acesso}\' . Aceitar?')

                        icon = QIcon(resource_path('imagens/warning.ico'))
                        msg_box.setWindowIcon(icon)
                        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                        reply = msg_box.exec()

                        conexao = pymysql.connect(
                            host=self.hostmysql,
                            user=self.usermysql,
                            password=self.passwordmysql,
                            database=self.databasemysql
                        )
                        cursor = conexao.cursor()
                        if reply == QMessageBox.StandardButton.Yes:
                            try:
                                usuario = self.user_2.text()

                                comando = 'UPDATE cadastros SET analise = 1 WHERE user = %s'
                                cursor.execute(comando, (usuario,))
                                conexao.commit()

                                comando = 'INSERT INTO posicao_usuario_tempo_real (usuario, nome) VALUES (%s, %s)'
                                cursor.execute(comando, (usuario, name))
                                conexao.commit()

                                self._mostrar_mensagem('Conta Cadastrada com Sucesso!')

                            finally:
                                cursor.close()
                                conexao.close()

