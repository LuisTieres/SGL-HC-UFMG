from PyQt6.QtGui import QIcon,QPixmap
from PyQt6 import QtCore, QtGui, QtWidgets
import mysql.connector
from PyQt6.QtWidgets import QMessageBox, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
class Ui_Form(object):
    def setupUi(self, Form):
        # Dados Bancos Mysql:
        self.host_mysql = 'localhost'
        self.user_mysql = 'root',
        self.password_mysql = 'camileejose'

        Form.setObjectName("Form")
        Form.setFixedSize(612, 567)

        icon = QIcon('icone_p_eUO_icon.ico')
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: rgb(0, 74, 112);")
        self.frame = QtWidgets.QFrame(parent=Form)
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
        self.state = True

        icon = QtGui.QIcon(
            'escondido.png')
        pixmap = icon.pixmap(25, 25)
        self.show_password_checkbox = ClickableLabel(parent=self.frame)
        self.show_password_checkbox.setPixmap(pixmap)
        self.show_password_checkbox.setGeometry(QtCore.QRect(350, 160, 50, 31))
        self.show_password_checkbox.setStyleSheet('border:none;'
                                                  'background-color: transparent;')
        self.show_password_checkbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.show_password_checkbox.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
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
        self.login_2.setGeometry(QtCore.QRect(180, 280, 91, 21))
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
        self.login_2.clicked.connect(lambda :self.criar_conta(Form))
        self.login.clicked.connect(lambda :self.logar(Form))

        self.label_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_2.setGeometry(QtCore.QRect(50, 160, 41, 31))
        self.label_2.setStyleSheet("background-color:none;")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("cadeado-desbloqueado.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.frame)
        self.label_3.setGeometry(QtCore.QRect(50, 70, 41, 31))
        self.label_3.setStyleSheet("background-color:none;")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("sombra-de-usuario-masculino.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(190, 40, 221, 171))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("icon_title.png"))
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
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.user, self.password)
        Form.setTabOrder(self.password, self.login)
        Form.setTabOrder(self.login, self.login_2)
    def toggle_password_visibility(self):
        if self.state == True:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            icon = QtGui.QIcon(
                'olho.png')
            pixmap = icon.pixmap(25, 25)
            self.show_password_checkbox.setPixmap(pixmap)
            self.state = False

        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            icon = QtGui.QIcon(
                'escondido.png')
            pixmap = icon.pixmap(25, 25)
            self.show_password_checkbox.setPixmap(pixmap)
            self.state = True
    def ocultar_user_label(self):
        self.user_label.hide()
        self.senha_label.hide()
    def logar(self,Form):
        conexao = mysql.connector.connect(
            host=f'10.36.0.32',
            user=f'sglHC2024',
            password=f'S4g1L81',
            database='sgl'
        )
        cursor = conexao.cursor()

        comando = 'SELECT * FROM cadastros'
        cursor.execute(comando)
        leitura = cursor.fetchall()

        analise = True
        cont = 0
        reply = None
        for linha in leitura:
            if len(linha)>0:
                cont+=1
                print(cont,len(leitura))
                if linha[0] == self.user.text():
                    if linha[4] == '0':
                        msg_box = QMessageBox()
                        msg_box.setIcon(QMessageBox.Icon.Information)
                        msg_box.setWindowTitle("AVISO")
                        msg_box.setText("Aguarde o Administrador confirmar o acesso!")
                        icon = QIcon(
                            'warning.ico')
                        msg_box.setWindowIcon(icon)
                        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                        reply = msg_box.exec()
                    else:
                        if linha[2] == self.password.text():
                            from telademandaps import Ui_Demanda
                            self.janela_demanda = QtWidgets.QMainWindow()
                            self.demanda = Ui_Demanda()
                            self.linha3 = linha[3]
                            self.linha1 = linha[1]
                            self.linha2 = linha[2]
                            self.tela_espera(Form)
                            break
                        else:
                            print(reply)
                            self.password.clear()
                            if reply == None:
                                print(reply,1)
                                self.senha_label.show()
                            break
                if linha[0] != self.user.text() and cont == len(leitura):
                    self.password.clear()
                    self.user.clear()
                    if reply == None:
                        self.user_label.show()
        cursor.close()
        conexao.close()
    def tela_espera(self,Form):
        for widget in Form.findChildren(QtWidgets.QWidget):
            widget.hide()
        self.frame.show()
        self.frame.setGeometry(QtCore.QRect(0, 0, 612, 567))
        self.loading_label = QtWidgets.QLabel(self.frame)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame.setStyleSheet("border: none;")
        caminho_imagem = "tela_espera.png"
        pixmap = QPixmap(caminho_imagem)
        self.loading_label.setPixmap(pixmap)
        self.loading_label.setGeometry(QtCore.QRect(0, 0, 612, 567))
        self.loading_label.setScaledContents(True)
        self.loading_label.show()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda :self.show_main_window(Form))
        self.timer.start(5000)

    def show_main_window(self,Form):
        self.timer.stop()
        Form.close()
        self.demanda.setupUi(self.janela_demanda, self.linha3, self.linha1,self.linha2)
        self.janela_demanda.show()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Sistema de Gestão de Leitos"))
        self.user.setPlaceholderText(_translate("Form", "Usuário"))
        self.password.setPlaceholderText(_translate("Form", "Senha"))
        self.login.setText(_translate("Form", "Login"))
        self.login_2.setText(_translate("Form", "Criar Conta"))
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