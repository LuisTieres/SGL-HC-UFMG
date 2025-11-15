import pymysql
from PyQt6.QtGui import QIcon,QPixmap
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QVBoxLayout, QWidget,QDialog,QComboBox,QPushButton,QLabel
from PyQt6.QtCore import Qt, QTimer
import sys
import os
from PyQt6 import QtGui
from ldap3 import Server, Connection, ALL, SUBTREE
import ast
from PyQt6.QtCore import Qt,QObject, QEvent, Qt
from PyQt6.QtGui import QFont
import base64
from database_Demandas import Ui_data_Demanda
from conecao_api import Ui_API
import base64
from pathlib import Path
from os.path import expanduser
DB_CONFIG = {
    'host': '10.36.0.32',
    'user': 'sglHC2024',
    'password': 'S4g1L81',
    'database': 'sgl'
}

def resource_path(relative_path):
    """Resolve path para PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class KeyFilter(QObject):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self.callback(obj)
                return True
        return super().eventFilter(obj, event)

class ComboDialog(QDialog):
    def __init__(self,login):
        super().__init__()
        self.setWindowTitle("Selecione o Tipo de Usuário que você Deseja Solicitar")
        self.valor_selecionado = None

        self.data_deman = Ui_data_Demanda()
        self.lista = self.data_deman.ler_tipos(self)

        layout = QVBoxLayout()

        label = QLabel("Escolha o Usuário:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Segoe UI", 12))
        layout.addWidget(label)

        self.combo = QComboBox()
        self.combo.setStyleSheet("""
                    QComboBox {
                        padding: 6px;
                        font-size: 14px;
                        border: 1px solid #ccc;
                        border-radius: 6px;
                    }
                    QComboBox::drop-down {
                        border: none;
                    }
                """)
        layout.addWidget(self.combo)
        self.combo.addItems(self.lista)

        btn = QPushButton("Confirmar")
        btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        padding: 8px;
                        border-radius: 8px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
        btn.clicked.connect(self.retorna_valor)
        layout.addWidget(btn)

        self.setLayout(layout)

    def retorna_valor(self):
        self.valor_selecionado = self.combo.currentText()
        self.accept()

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()


class Ui_Form(object):

    def setupUi(self, Form):

        # if self.user.text() != 'luis.tieres':
        # self.hostmysql = '10.36.0.32'
        # self.usermysql = 'sglHC2024'
        # self.passwordmysql = 'S4g1L81'
        # self.databasemysql = 'sgl'

        # self.hostmysql = '127.0.0.1'
        # self.usermysql = 'root'
        # self.passwordmysql = 'senhasgl'
        # self.databasemysql = 'sgl'

        self.data_deman = Ui_data_Demanda()
        self.api = Ui_API()

        # Configuração do Form para ficar sem bordas e com fundo translúcido
        Form.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        Form.setFixedSize(612, 567)

        icon = QIcon(resource_path('imagens/icone_p_eUO_icon.ico'))
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: rgb(0, 74, 112);")

        self.frame_Form = QtWidgets.QFrame(parent=Form)
        self.frame_Form.setGeometry(QtCore.QRect(0, 0, 612, 567))
        self.frame_Form.setStyleSheet("background-color: rgb(0, 74, 112);\n"
                                 "border: 2px solid while;\n"
                                 "border-radius: 10px;")
        self.frame_Form.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_Form.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_Form.setObjectName("frame")

        self.frame = QtWidgets.QFrame(parent=self.frame_Form)
        self.frame.setGeometry(QtCore.QRect(80, 190, 461, 341))
        self.frame.setStyleSheet("background-color: rgba(0, 0, 0,0.2);\n"
"border: 2px solid while;\n"
"                               border-radius: 10px;")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        self.user = QtWidgets.QLineEdit(parent=self.frame)
        self.user.setGeometry(QtCore.QRect(100, 70, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.user.setFont(font)
        self.user.setStyleSheet("color: rgb(255, 255, 255);")
        self.user.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.user.setObjectName("user")

        self.key_filter = KeyFilter(self.on_tab_pressed)
        self.user.installEventFilter(self.key_filter)

        self.password = QtWidgets.QLineEdit(parent=self.frame)
        self.password.setGeometry(QtCore.QRect(100, 160, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.password.setFont(font)
        self.password.setStyleSheet("color: rgb(255, 255, 255);")
        self.password.setFrame(True)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password.setObjectName("password")

        self.password.installEventFilter(self.key_filter)
        self.state = True

        icon = QtGui.QIcon(resource_path('imagens/escondido.ico'))
        pixmap = icon.pixmap(25, 25)
        self.show_password_checkbox = ClickableLabel(parent=self.frame)
        self.show_password_checkbox.setPixmap(pixmap)
        self.show_password_checkbox.setGeometry(QtCore.QRect(350, 160, 50, 31))
        self.show_password_checkbox.setStyleSheet('border:none;'
                                                  'background-color: transparent;')
        self.show_password_checkbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.show_password_checkbox.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)

        icon = QtGui.QIcon(resource_path('imagens/escondido.png'))
        pixmap = icon.pixmap(25, 25)
        self.show_password_checkbox.setPixmap(pixmap)
        self.show_password_checkbox.clicked.connect(self.toggle_password_visibility)

        self.login = QtWidgets.QPushButton(parent=self.frame)
        self.login.setGeometry(QtCore.QRect(150, 230, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.login.setFont(font)
        self.login.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.login.setStyleSheet("QPushButton{\n"
        "    background-color: rgb(0, 0, 0);\n"
        "    color: rgb(255, 255, 255);\n"
        "    border-radius:10px;\n"
        "}\n"
        "QPushButton:hover{\n"
        "    background-color: rgb(255, 255, 255);\n"
        "    color: rgb(0, 0, 0);\n"
        "}")
        self.login.setObjectName("login")


        self.login_2 = QtWidgets.QPushButton(parent=self.frame)
        self.login_2.setGeometry(QtCore.QRect(150, 280, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.login_2.setFont(font)
        self.login_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.login_2.setStyleSheet("QPushButton{\n"
            "    background-color:transparent;\n"
            "    color: rgb(255, 255, 255);\n"
            "    border-radius:10px;\n"
            "   border:  transparent;\n"
            "}\n"
            "QPushButton:hover{\n"
            "    background-color: rgba(255, 255, 255,0.2);\n"
            "    color: rgb(0, 0, 0);\n"
            "   border:  transparent;\n"
            "\n"
            "}")
        self.login_2.setObjectName("login_2")
        self.login_2.clicked.connect(lambda :self.criar_conta(self.frame_Form))
        self.form = Form
        self.login.clicked.connect(self.logar)

        self.bnt_sair = QtWidgets.QPushButton('X',parent=self.frame_Form)
        self.bnt_sair.setGeometry(QtCore.QRect(580, 5, 25, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bnt_sair.setFont(font)
        self.bnt_sair.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.bnt_sair.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgb(0, 0, 0);
                border-radius: 10px;
                border: transparent;
                font-weight: bold; /* Deixa o texto mais grosso */
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                color: rgb(0, 0, 0);
                border: transparent;
                border-radius: 10px;
                font-weight: bold; /* Deixa o texto mais grosso ao passar o mouse */
            }
        """)

        self.bnt_sair.setObjectName("bnt_sair")
        self.bnt_sair.clicked.connect(Form.close)

        self.label_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_2.setGeometry(QtCore.QRect(50, 160, 41, 31))
        self.label_2.setStyleSheet("background-color:none;")
        self.label_2.setText("")

        pixmap = QtGui.QPixmap(resource_path('imagens/cadeado-desbloqueado.png'))

        self.label_2.setPixmap(pixmap)

        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.frame)
        self.label_3.setGeometry(QtCore.QRect(50, 70, 41, 31))
        self.label_3.setStyleSheet("background-color:none;")
        self.label_3.setText("")

        pixmap = QtGui.QPixmap(resource_path('imagens/sombra-de-usuario-masculino.png'))

        self.label_3.setPixmap(pixmap)

        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(parent=self.frame_Form)
        self.label.setGeometry(QtCore.QRect(190, 40, 221, 171))
        self.label.setText("")

        pixmap = QtGui.QPixmap(resource_path('imagens/icon_title.png'))

        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label.raise_()
        self.frame.raise_()
        self.user_label = QtWidgets.QLabel('Usuário não Encotrado!',self.frame)
        self.user_label.setStyleSheet('color: red;'
                                         'border:none;'
                                         'background-color: transparent;')
        self.user_label.setGeometry(QtCore.QRect(100, 105, 281, 31))
        self.user_label.hide()

        self.senha_label = QtWidgets.QLabel('Senha Incorreta!', self.frame)
        self.senha_label.setStyleSheet('color: red;'
                                      'border:none;'
                                      'background-color: transparent;')
        self.senha_label.setGeometry(QtCore.QRect(100, 196, 281, 31))
        self.senha_label.hide()

        self.user.textChanged.connect(self.ocultar_user_label)
        self.password.textChanged.connect(self.ocultar_user_label)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(self.frame_Form)
        Form.setTabOrder(self.user, self.password)
        Form.setTabOrder(self.password, self.login)
        Form.setTabOrder(self.login, self.login_2)
        self.show_password_checkbox.show()
        self.inicio = True


    def toggle_password_visibility(self):
        if self.state == True:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            icon = QtGui.QIcon(resource_path('imagens/olho.png'))
            pixmap = icon.pixmap(25, 25)
            self.show_password_checkbox.setPixmap(pixmap)
            self.state = False

        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            icon = QtGui.QIcon(resource_path('imagens/escondido.png'))
            pixmap = icon.pixmap(25, 25)
            self.show_password_checkbox.setPixmap(pixmap)
            self.state = True

    def on_tab_pressed(self, widget):
        self.logar()

    def ocultar_user_label(self):
        self.user_label.hide()
        self.senha_label.hide()


    def logar(self):
        try:
            #verificacao = self.api.verificar_usuario_senha(self.user.text(),self.password.text())
            verificacao = True
            if verificacao:

                print("Tentando conectar...")

                leitura = self.data_deman.ler_cadastros(self)

                analise = False
                cont = 0
                for linha in leitura:
                    if len(linha) > 0:
                        cont += 1
                        print(cont, len(leitura),linha[0], self.user.text())
                        if linha[0] == self.user.text():
                            analise = True
                            if linha[2] == '0':
                                msg_box = QMessageBox()
                                msg_box.setIcon(QMessageBox.Icon.Information)
                                msg_box.setWindowTitle("AVISO")
                                msg_box.setText("Aguarde o Administrador confirmar o acesso!")

                                icon = QtGui.QIcon(resource_path('imagens/escondido.png'))
                                msg_box.setWindowIcon(icon)
                                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                                reply = msg_box.exec()

                            else:
                                from telademandaps import Ui_Demanda
                                self.linha3 = linha[3]
                                self.linha1 = linha[0]
                                self.linha2 = linha[1]

                                self.janela_demanda = QtWidgets.QMainWindow()
                                self.demanda = Ui_Demanda()
                                self.tela_espera()
                                break

                if analise == False:
                    self.criar_user()


        except Exception as e:
            print(f"Error: {e}")

    def criar_user(self):

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText(f'Você {self.nome} não possui acesso ao software!')

        icon = QIcon('imagens/warning.ico')
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Ok:
            dialog = ComboDialog(self)
            if dialog.exec():

                usuario = self.user.text()
                name = self.nome
                self.data_deman. criar_user_(self,usuario,name,dialog)

                print("Valor selecionado:", dialog.valor_selecionado)
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle('AVISO')
                msg_box.setText(f'Cadastro feito!\nAguarde o Administrador confirmar o acesso!')

                icon = QIcon('imagens/warning.ico')
                msg_box.setWindowIcon(icon)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply = msg_box.exec()


    def tela_espera(self):
        Form = self.frame_Form
        for widget in Form.findChildren(QtWidgets.QWidget):
            widget.hide()
        self.frame.show()
        self.frame.setGeometry(QtCore.QRect(0, 0, 612, 567))
        self.loading_label = QtWidgets.QLabel(self.frame)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame.setStyleSheet("border: none;")
        caminho_imagem = "imagens/tela_espera.png"
        pixmap = QPixmap(caminho_imagem)
        self.loading_label.setPixmap(pixmap)
        self.loading_label.setGeometry(QtCore.QRect(0, 0, 612, 567))
        self.loading_label.setScaledContents(True)
        self.loading_label.show()

        self.timer = QtCore.QTimer()
        self.show_main_window()
        #self.timer.start(5000)

    def show_main_window(self):
        self.timer.stop()
        Form = self.form
        Form.close()
        print(2)
        self.demanda.setupUi(self.janela_demanda, self.linha3, self.linha1,self.linha2)
        self.janela_demanda.show()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Sistema de Gestão de Leitos"))
        self.user.setPlaceholderText(_translate("Form", "Usuário"))
        self.password.setPlaceholderText(_translate("Form", "Senha"))
        self.login.setText(_translate("Form", "Login"))
        self.login_2.setText(_translate("Form", "Conceder Acesso!"))

    def criar_conta(self,Form):
        self.frame.hide()
        self.label.hide()
        from  criar_conta import Ui_Form
        self.criar_cont = Ui_Form()
        self.criar_cont.setupUi(Form,self)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())