from database_Demandas import Ui_data_Demanda
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFrame, QLabel, QWidget, QScrollArea, QMessageBox, QLineEdit, QFileDialog
from PyQt6.QtCore import Qt, QSettings, QStandardPaths, QFile
from PyQt6.QtGui import QIcon, QPixmap
from pathlib import Path
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QFile
from os.path import expanduser
from PyQt6 import QtCore, QtGui, QtWidgets

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class Ui_Form(object):

    def setupUi(self, Form, tela):

        self.data_deman = Ui_data_Demanda()
        self.tela = tela
        self.contas = []
        self.excluir_conta = []
        self.frames = []
        self.filename = None
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
        self.frame.mousePressEvent = lambda event, frame=self.frame: self.mousePressEvent(event, frame)
        self.frame.mouseReleaseEvent = lambda event, frame=self.frame: self.mouseReleaseEvent(event, frame)
        self.frame.mouseMoveEvent = lambda event, frame=self.frame: self.mouseMoveEvent(event, frame)
        self.label_icone = QtWidgets.QLabel(parent=self.frame)
        self.label_icone.setGeometry(QtCore.QRect(40, 39, 131, 121))
        self.label_icone.setStyleSheet('\nborder: 2px solid #2E3D48;\nborder-radius: 10px;')
        self.label_icone.setText('')
        self.label_icone.setObjectName('label_icone')

        self.frame_2 = QtWidgets.QFrame(parent=self.frame)
        self.frame_2.setGeometry(QtCore.QRect(20, 220, 451, 41))
        self.frame_2.setStyleSheet('background-color: white;\ncolor: black;\nborder: 2px solid #2E3D48;\nborder-radius: 10px;')
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName('frame_2')

        self.label_nome = QtWidgets.QLabel(parent=self.frame_2)
        self.label_nome.setGeometry(QtCore.QRect(20, 14, 341, 16))
        self.label_nome.setStyleSheet('border:none;\n')
        self.label_nome.setObjectName('label_nome')

        self.frame_3 = QtWidgets.QFrame(parent=self.frame)
        self.frame_3.setGeometry(QtCore.QRect(20, 280, 451, 41))
        self.frame_3.setStyleSheet('background-color: white;\ncolor: black;\nborder: 2px solid #2E3D48;\nborder-radius: 10px;')
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName('frame_3')

        self.label_login_2 = QtWidgets.QLabel(parent=self.frame_3)
        self.label_login_2.setGeometry(QtCore.QRect(20, 14, 341, 16))
        self.label_login_2.setStyleSheet('border:none;\n')
        self.label_login_2.setObjectName('label_login_2')


        self.frame_4 = QtWidgets.QFrame(parent=self.frame)
        self.frame_4.setGeometry(QtCore.QRect(20, 340, 100, 41))
        self.frame_4.setStyleSheet('background-color: white;\ncolor: black;\nborder: 2px solid #2E3D48;\nborder-radius: 10px;')
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName('frame_4')

        self.dep = QtWidgets.QLabel(parent=self.frame_4)
        self.dep.setGeometry(QtCore.QRect(20, 14, 70, 16))
        self.dep.setStyleSheet('border:none;\n')
        self.dep.setObjectName('dep')

        self.lista = self.data_deman.ler_tipos(self)

        self.lista.append("Administrador")

        self.combo = QtWidgets.QComboBox(parent=self.frame)
        self.combo.setEditable(True)
        self.combo.setGeometry(QtCore.QRect(140, 340, 161, 41))
        self.combo.addItems(self.lista)
        self.combo.setCurrentText(tela.dept)
        self.combo.setFixedWidth(150)
        self.combo.currentTextChanged.connect(lambda texto: self.ativar_btn(texto))

        self.frame_5 = QtWidgets.QFrame(parent=self.frame)
        self.frame_5.setGeometry(QtCore.QRect(20, 400, 451, 41))
        self.frame_5.setStyleSheet(
            'background-color: white;\ncolor: black;\nborder: 2px solid #2E3D48;\nborder-radius: 10px;')
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName('frame_4')

        self.dep_new = QtWidgets.QLabel(parent=self.frame_5)
        self.dep_new.setGeometry(QtCore.QRect(20, 14, 420, 16))
        self.dep_new.setStyleSheet('border:none;\n')
        self.dep_new.setObjectName('dep_new')
        self.frame_5.hide()

        self.state = True

        self.pushButton = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton.setGeometry(QtCore.QRect(330, 460, 125, 23))
        self.pushButton.setStyleSheet('QPushButton {\n                                border: 2px solid #2E3D48;\n                                border-radius: 10px;\n                                background-color: #FFFFFF;\n                                color: #2E3D48;\n                            }\n\n                            QPushButton:hover {\n                                background-color: #DDDDDD;  /* Change this to your desired hover color */\n                                color: rgb(0, 0, 0);\n                            }\n\n                            QPushButton:pressed {\n                                background-color: #2E3D48;  /* Change this to your desired pressed color */\n                                color: #FFFFFF;\n                            }')
        self.pushButton.setObjectName('pushButton')
        self.pushButton.clicked.connect(self.confirmar_alteracoes)
        self.retranslateUi(Form)
        self.pushButton.hide()

        for widget in self.frame.findChildren(QtWidgets.QWidget):
            widget.show()
        self.frame.show()
        self.load()
        self.atualizar_conta()

    def ativar_btn(self, text):
        if text!= self.tela.dept:
            self.pushButton.show()

    def atualizar_conta(self):
        leitura = self.data_deman.ler_cadastros(self)
        for linha in leitura:
            if self.tela.user == linha[0]:
                if linha[2] == '2':
                    self.dep.setText('Perfil atual: ')
                    self.dep_new.setText(f'Novo Perfil Solicitado: {linha[4]}')
                    self.frame_5.show()
                    break
                else:
                    self.frame_5.hide()

        self.carregar_foto_usuario()

    def carregar_foto_usuario(self):
        pasta_imagens = Path(expanduser("~")) / "Pictures"
        caminho_imagem = pasta_imagens / f"imagem_do_usuario_{self.tela.user}.png"

        if QFile.exists(str(caminho_imagem)):
            pixmap = QPixmap(str(caminho_imagem))
            if not pixmap.isNull():
                self.label_icone.setPixmap(pixmap.scaled(
                    self.label_icone.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
                self.label_icone.setScaledContents(False)
            else:
                print("Imagem encontrada, mas não pôde ser carregada.")
        else:
            print(f"Imagem não encontrada: {caminho_imagem}")

    def confirmar_alteracoes(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText(f'Alterar o Perfil para \'{self.combo.currentText()}\'?')
        icon = QIcon('imagens/warning.ico')
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.No:
            self.combo.setCurrentText(self.tela.dept)

        if reply == QMessageBox.StandardButton.Yes:

            self.data_deman.update_cadastro('2',self.tela.user,self.tela.dept,self.combo.currentText())

            if self.filename:
                caminho_destino = 'imagens/imagem_do_usuario.png'
                QFile.remove(caminho_destino)
                pixmap = QPixmap(self.filename)
                pixmap.save(caminho_destino)
            self.atualizar_conta()
        if reply == QMessageBox.StandardButton.No:
            self.atualizar_conta()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        nome = 'Nome: '+self.tela.nome_user
        login = 'Login: '+self.tela.nome_user
        self.label_nome.setText(_translate('Form', nome))
        self.label_login_2.setText(_translate('Form', login))
        self.dep.setText(_translate('Form', 'Pefil: '))
        self.pushButton.setText(_translate('Form', 'Confirmar Alterações'))

    def mousePressEvent(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            centralwidget.mouse_offset = event.pos()

    def mouseReleaseEvent(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            centralwidget.setCursor(Qt.CursorShape.ArrowCursor)  # Garante que volta para a seta

    def mouseMoveEvent(self, event, centralwidget):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = centralwidget.mapToParent(event.pos() - centralwidget.mouse_offset)
            centralwidget.move(new_pos)

    def load(self):
        if self.settings.contains('tema'):
            font_name = self.settings.value('font', defaultValue='')
            backcolocor = self.settings.value('tema', defaultValue='')
            color = self.settings.value('color', defaultValue='')
            tamanho = int(self.settings.value('tamanho', defaultValue=10))
            self.backcolocor = backcolocor
            self.color = color
            self.frame.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;border: 2px solid #2E3D48;border-radius: 10px;')