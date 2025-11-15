from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFrame, QLabel, QWidget, QScrollArea, QMessageBox, QLineEdit,QComboBox
from PyQt6.QtCore import Qt, QSettings, QStandardPaths
from PyQt6.QtGui import QIcon

import re
import os
import sys
from database_Demandas import Ui_data_Demanda
from PyQt6 import QtCore, QtGui, QtWidgets

def resource_path(relative_path):
    """Resolve path para PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
        icon = QIcon('imagens/silhueta-de-multiplos-usuarios.ico')
        pixmap = icon.pixmap(50, 50)
        self.icone = QtWidgets.QLabel(parent=self.frame)
        self.icone.setPixmap(pixmap)
        self.icone.setGeometry(QtCore.QRect(3, 3, 50, 50))
        self.icone.show()
        self.icone.setStyleSheet('border:none;')
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
        self.lista = self.data_deman.ler_tipos(self)
        self.lista.append("Administrador")
        leitura = self.data_deman.ler_cadastros(self)
        for linha in leitura:
            self.add_frame(linha[0], linha[1], linha[3], linha[2], linha[4])

    def add_frame(self, usu_, Usuario, nivel_acesso, dep, novo):
        frame = QFrame(self.scroll_content)
        frame.setFixedSize(500, 200)
        frame.setStyleSheet('border: 2px solid #2E3D48; background-color: white; border-radius: 10px; color: black;')

        layout_principal = QtWidgets.QVBoxLayout(frame)
        layout_principal.setContentsMargins(10, 10, 10, 10)
        layout_principal.setSpacing(10)

        font_titulo = QtGui.QFont()
        font_titulo.setPointSize(15)

        usu = QLabel(f'Usuário: {Usuario}')
        usu.setFont(font_titulo)
        layout_principal.addWidget(usu)

        if dep == '0':
            departamento = QLabel(f'Perfil Solicitado: {nivel_acesso}')
        elif dep == '2':
            departamento = QLabel(f'Perfil Atual: {nivel_acesso} \nPerfil Solicitado: {novo} ')
        else:
            departamento = QLabel(f'Perfil: {nivel_acesso}')

        departamento.setFont(font_titulo)
        layout_principal.addWidget(departamento)

        btn_alterar_perfil = QtWidgets.QPushButton('Alterar Perfil')
        btn_alterar_perfil.setFixedWidth(150)
        btn_alterar_perfil.setStyleSheet('''
                    QPushButton {
                        border: 2px solid #2E3D48;
                        border-radius: 10px;
                        background-color: #FFFFFF;
                        color: #2E3D48;
                    }
                    QPushButton:hover {
                        background-color: #DDDDDD;
                        color: rgb(0, 0, 0);
                    }
                    QPushButton:pressed {
                        background-color: #2E3D48;
                        color: #FFFFFF;
                    }
                ''')
        btn_alterar_perfil.clicked.connect(lambda: self.abrir_dialog_perfil(nivel_acesso, departamento, usu_))
        layout_principal.addWidget(btn_alterar_perfil)

        btn_excluir = QtWidgets.QPushButton('Excluir Usuário')
        btn_excluir.setFixedWidth(150)
        btn_excluir.setToolTip('Excluir Usuário')
        btn_excluir.setStyleSheet('''
            QPushButton {
                border: 2px solid #2E3D48;
                border-radius: 10px;
                background-color: #FFFFFF;
                color: #2E3D48;
            }
            QPushButton:hover {
                background-color: #DDDDDD;
                color: rgb(0, 0, 0);
            }
            QPushButton:pressed {
                background-color: #2E3D48;
                color: #FFFFFF;
            }
        ''')
        btn_excluir.clicked.connect(lambda: self.excluir(usu_, btn_excluir))
        self.excluir_conta.append((btn_excluir, usu_))
        layout_principal.addWidget(btn_excluir)

        self.scroll_layout.addWidget(frame)
        self.frames.append((frame, Usuario))

    def abrir_dialog_perfil(self, nivel_atual, label_departamento, usu_):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle('Selecionar Perfil')
        dialog.setFixedSize(300, 300)

        layout_dialog = QtWidgets.QVBoxLayout(dialog)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QtWidgets.QWidget()
        layout_checkboxes = QtWidgets.QVBoxLayout(content_widget)

        checkboxes = []
        for perfil in self.lista:
            checkbox = QtWidgets.QCheckBox(perfil)
            if perfil == nivel_atual:
                checkbox.setChecked(True)
            checkbox.stateChanged.connect(lambda state, chk=checkbox: self.desmarcar_outros(checkboxes, chk))
            checkboxes.append(checkbox)
            layout_checkboxes.addWidget(checkbox)

        scroll.setWidget(content_widget)
        layout_dialog.addWidget(scroll)

        # Botões
        layout_botoes = QtWidgets.QHBoxLayout()

        btn_confirmar = QtWidgets.QPushButton('Confirmar')
        btn_confirmar.clicked.connect(lambda: self.definir_novo_perfil(checkboxes, label_departamento, usu_, dialog))
        layout_botoes.addWidget(btn_confirmar)

        btn_limpar = QtWidgets.QPushButton('Limpar Seleção')
        btn_limpar.clicked.connect(lambda: self.limpar_selecao(checkboxes))
        layout_botoes.addWidget(btn_limpar)

        btn_cancelar = QtWidgets.QPushButton('Cancelar')
        btn_cancelar.clicked.connect(dialog.reject)
        layout_botoes.addWidget(btn_cancelar)

        layout_dialog.addLayout(layout_botoes)

        dialog.exec()

    def limpar_selecao(self, checkboxes):
        for chk in checkboxes:
            chk.setChecked(False)

    def desmarcar_outros(self, checkboxes, selecionado):
        if selecionado.isChecked():
            for chk in checkboxes:
                if chk != selecionado:
                    chk.setChecked(False)

    def aceitar_user_(self, user,novo_perfil):
        leitura = self.data_deman.ler_cadastros(self)
        for linha in leitura:
            if len(linha) > 0 and linha[0] == user:
                if linha[2] == '0' or linha[2] == '1':
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Information)
                    msg_box.setWindowTitle('AVISO')
                    msg_box.setText(
                        f'Trocar perfil do usuário com Nome \'{linha[1]}\' e user \'{linha[0]}\' para o perfil \'{novo_perfil}\'. Aceitar?')
                    icon = QIcon(resource_path('imagens/warning.ico'))
                    msg_box.setWindowIcon(icon)
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    reply = msg_box.exec()
                    if reply == QMessageBox.StandardButton.Yes:
                        self.data_deman.update_cadastro('1', user, novo_perfil, '')
                        self._mostrar_mensagem('Alteração Realizada com Sucesso!')
                        break

    def _mostrar_mensagem_yes_no(self, texto):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle('Confirmação')
        msg_box.setText(texto)
        icon = QIcon(resource_path('imagens/warning.ico'))
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg_box.exec()
        return reply

    def _mostrar_mensagem(self, texto):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('AVISO')
        msg_box.setText(texto)
        icon = QIcon(resource_path('imagens/warning.ico'))
        msg_box.setWindowIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def definir_novo_perfil(self, checkboxes, label_departamento, usu_, dialog):
        for chk in checkboxes:
            if chk.isChecked():
                novo_perfil = chk.text()
                label_departamento.setText(f'Perfil: {novo_perfil}')
                self.aceitar_user_(usu_,novo_perfil)
                break
        dialog.accept()

    def excluir(self, usu, btn_excluir):
        for i, (btn_excluir1, usu1) in enumerate(self.excluir_conta):
            print(usu, usu1)
            if btn_excluir1 == btn_excluir and usu == usu1:
                print(usu, usu1, 55)
                leitura = self.data_deman.ler_cadastros(self)
                for linha in leitura:
                    if len(linha) > 0 and linha[0] == usu:
                        msg_box = QMessageBox()
                        msg_box.setIcon(QMessageBox.Icon.Information)
                        msg_box.setWindowTitle('AVISO')
                        msg_box.setText(f"O usuário com Nome '{linha[1]}' e user '{linha[0]}' será excluído do software. Confirmar?")
                        icon = QIcon('imagens/warning.ico')
                        msg_box.setWindowIcon(icon)
                        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                        reply = msg_box.exec()
                        if reply == QMessageBox.StandardButton.Yes:
                            self.data_deman.exluir_conta(usu)
                            self._mostrar_mensagem('Conta Excluída com Sucesso!')


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