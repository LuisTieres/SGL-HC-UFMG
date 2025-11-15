from PyQt6.QtWidgets import QApplication, QRadioButton, QComboBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import pymysql
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QSettings, QStandardPaths, Qt
import psycopg2

class Ui_Form(QMainWindow):

    def setupUi(self, Form, grade):
        self.grade = grade
        self.form = Form
        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setGeometry(QtCore.QRect(400, 65, 641, 511))
        self.frame.setStyleSheet('background-color: #5DADE2;')
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.Titulo = QtWidgets.QLabel('Criar nova Unidade De Internação', parent=self.frame)
        self.Titulo.setGeometry(QtCore.QRect(160, 15, 330, 38))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.Titulo.setFont(font)
        self.frame.setCursor(Qt.CursorShape.OpenHandCursor)
        self.frame.mousePressEvent = lambda event, frame=self.frame: self.mousePressEvent_2(event, frame)
        self.frame.mouseReleaseEvent = lambda event, frame=self.frame: self.mouseReleaseEvent_2(event, frame)
        self.frame.mouseMoveEvent = lambda event, frame=self.frame: self.mouseMoveEvent_2(event, frame)
        self.grade.janela_cria_unidade = self.frame
        self.table_name_label = QLabel('Nome da Tabela:', self.frame)
        self.table_name_label.setGeometry(QtCore.QRect(20, 100, 100, 30))
        self.lista_table = []
        self.tabelas()
        self.table_name_input = QLineEdit(self.frame)
        self.table_name_input.setGeometry(QtCore.QRect(130, 100, 250, 30))
        self.table_name_input.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        completer = QtWidgets.QCompleter(self.lista_table)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.table_name_input.setCompleter(completer)
        self.columns_layout = QVBoxLayout()
        self.create_table_button = QPushButton('Criar Tabela', self.frame)
        self.create_table_button.clicked.connect(self.create_table)
        self.create_table_button.setGeometry(QtCore.QRect(20, 220, 100, 30))
        self.frame.show()
        for btn in self.frame.findChildren(QtWidgets.QPushButton):
            btn.setStyleSheet('\n                QPushButton {\n                    border: 2px solid #2E3D48;\n                    border-radius: 10px;\n                    background-color: #FFFFFF;\n                    color: #2E3D48;\n                }\n\n                QPushButton:hover {\n                    background-color: #DDDDDD;  /* Change this to your desired hover color */\n                    color: rgb(0, 0, 0);\n                }\n\n                QPushButton:pressed {\n                    background-color: #2E3D48;  /* Change this to your desired pressed color */\n                    color: #FFFFFF;\n                }\n            ')
        for widget in self.frame.findChildren(QtWidgets.QWidget):
            widget.show()
        self.load(Form)

    def tabelas(self):
        connection = psycopg2.connect(user='ugen_integra', password='aghuintegracao', host='10.36.2.35', port='6544', database='dbaghu')
        cursor = connection.cursor()
        cursor.execute('SELECT descricao FROM AGH.AGH_UNIDADES_FUNCIONAIS ')
        rows = cursor.fetchall()
        for row in rows:
            self.lista_table.append(row[0])

    def create_table(self):
        table_name = self.table_name_input.text()
        try:
            conexao = pymysql.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
            cursor = conexao.cursor()
            print(table_name)
            comando = f"INSERT INTO New_GRADES (tabelas) VALUES ('{table_name}')"
            cursor.execute(comando)
            conexao.commit()
            conexao.close()
            self.show_message('Sucesso', 'Tabela criada com sucesso!')
        except pymysql.connector.Error as e:
            self.show_message('Erro', f'Erro ao criar tabela: {e}')

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def mousePressEvent_2(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            centralwidget.setCursor(Qt.CursorShape.ClosedHandCursor)
        centralwidget.mouse_offset = event.pos()

    def mouseReleaseEvent_2(self, event, centralwidget):
        if event.button() == Qt.MouseButton.LeftButton:
            centralwidget.setCursor(Qt.CursorShape.OpenHandCursor)

    def mouseMoveEvent_2(self, event, centralwidget):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = centralwidget.mapToParent(event.pos() - centralwidget.mouse_offset)
            centralwidget.move(new_pos)
            x, y = (new_pos.x(), new_pos.y())

    def load(self, Form):
        if self.settings.contains('tema'):
            font_name = self.settings.value('font', defaultValue='')
            backcolocor = self.settings.value('tema', defaultValue='')
            color = self.settings.value('color', defaultValue='')
            tamanho = int(self.settings.value('tamanho', defaultValue=10))
            self.backcolocor = backcolocor
            self.color = color
            self.frame.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;border: 2px solid #2E3D48;border-radius: 10px;')
            for label in self.frame.findChildren(QtWidgets.QLabel):
                label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name}; border:none')
            self.Titulo.setStyleSheet(f'color: {color}; font:  30 px {font_name}; border:none;')