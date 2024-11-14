import mysql.connector
import datetime
from PyQt6.QtCore import QDateTime, QSettings, QStandardPaths, QDate
from PyQt6.QtGui import QKeyEvent, QGuiApplication
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QScrollArea, QFrame, QWidget, QVBoxLayout, QLabel, QRadioButton
from PyQt6.QtCore import Qt

class Ui_Form(object):
    def __init__(self):
        super().__init__()

    def setupUi(self, Form, tela):

        colo = """
                            QPushButton {

                            background-color: #FFFFFF;
                            color: #2E3D48;
                            border-radius: 10px;
                            border-color: transparent;
                            }
                            QPushButton:hover {
                            background-color: #c0c0c0;
                            color: #000000;
                            }
                            QPushButton:pressed {
                                background-color: #2E3D48;
                                color: #FFFFFF;
                            }
                        """

        self.host_mysql = 'localhost'
        self.user_mysql = ('root',)
        self.password_mysql = 'camileejose'
        self.tela = tela
        Form.setObjectName('Form')
        Form.showMaximized()
        icon = QIcon('documentario.ico')
        Form.setWindowIcon(icon)
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)
        screen = QGuiApplication.primaryScreen()
        size = screen.size()
        width = size.width()
        height = size.height() - 10
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setStyleSheet('background-color: #5DADE2;')
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.frame.show()
        self.frame.setGeometry(QtCore.QRect(0, 0, width, height))
        self.pesquisa_historico = QtWidgets.QLineEdit(parent=self.frame)
        self.pesquisa_historico.setGeometry(QtCore.QRect(40, 25, 741, 31))
        self.pesquisa_historico.setAccessibleName('')
        self.pesquisa_historico.setAccessibleDescription('')
        self.pesquisa_historico.setAutoFillBackground(False)
        self.pesquisa_historico.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.pesquisa_historico.setInputMask('')
        self.pesquisa_historico.setText('')
        self.pesquisa_historico.setObjectName('pesquisa_historico')
        self.pesquisa_historico.setPlaceholderText('Pesquisar no Historico')
        self.pesquisa_historico.textChanged.connect(self.pesquisar)
        icon = QIcon('lupa.ico')
        self.pesquisa_historico.addAction(icon, QtWidgets.QLineEdit.ActionPosition.LeadingPosition)
        width = size.width() - 100
        height = size.height() - 200
        self.scroll = QScrollArea(self.frame)
        self.scroll.setWidgetResizable(True)
        self.scroll.setGeometry(QtCore.QRect(39, 130, width, height))
        self.scroll.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: none;')
        self.content_widget = QWidget()
        self.scroll.setWidget(self.content_widget)
        self.radio_recente = QRadioButton('Modificação mais Recente', parent=self.frame)
        self.radio_recente.setChecked(True)
        self.radio_antigo = QRadioButton('Modificação mais  Antiga', parent=self.frame)
        self.radio_antigo.setChecked(False)
        self.radio_recente.toggled.connect(self.atualiza_historico)
        self.radio_antigo.toggled.connect(self.atualiza_historico)
        self.radio_recente.setGeometry(QtCore.QRect(950, 100, 160, 20))
        self.radio_antigo.setGeometry(QtCore.QRect(1120, 100, 160, 20))
        self.label_ordenar = QtWidgets.QLabel(parent=self.frame)
        self.label_ordenar.setGeometry(QtCore.QRect(900, 70, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_ordenar.setFont(font)
        self.label_ordenar.setObjectName('label_grupo')
        self.btn_filtros = QtWidgets.QPushButton('▼ Selecione uma Data ', parent=self.frame)
        self.btn_filtros.setGeometry(QtCore.QRect(790, 20, 150, 23))
        self.btnfechar = QtWidgets.QPushButton(' X ', parent=self.frame)
        self.btn_filtros.setFocus()
        self.btnfechar.setStyleSheet('QPushButton {    border-top-right-radius: 10px;    border-bottom-right-radius: 10px;    border-top-left-radius: 0px;    border-bottom-left-radius: 0px;    background-color: #FFFFFF;    color: #2E3D48;    border: 2px solid #2E3D48;}QPushButton:pressed {    background-color: #2E3D48;    color: #FFFFFF;}')
        current_datetime = QDateTime.currentDateTime()
        formatted_date = current_datetime.toString('yyyy')
        formatted_date2 = current_datetime.addYears((-1)).toString('yyyy')
        self.frame_box = QtWidgets.QFrame(parent=self.frame)
        self.frame_box.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.frame_box.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_box.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_box.setGeometry(QtCore.QRect(790, 43, 150, 125))
        self.frame_personalisa = QtWidgets.QFrame(parent=self.frame)
        self.frame_personalisa.setStyleSheet('\n            QFrame  {\n                background-color: #FFFFFF;\n                border-top-right-radius: 20px;\n                border-bottom-right-radius: 20px;\n                border-left: 1px solid black;\n            }\n        ')
        self.frame_personalisa.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_personalisa.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_personalisa.setObjectName('frame_box')
        self.frame_personalisa.setGeometry(QtCore.QRect(939, 43, 270, 125))
        ccurrent_datetime = QtCore.QDateTime.currentDateTime()

        # Correção da criação e configuração de frames e widgets
        self.borda_inicio = QtWidgets.QFrame(parent=self.frame_personalisa)
        self.borda_inicio.setStyleSheet('border: 2px solid black; border-radius: 10px; background-color: #FFFFFF;')
        self.borda_inicio.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.borda_inicio.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.borda_inicio.setObjectName('frame')
        self.borda_inicio.setGeometry(QtCore.QRect(25, 140, 29, 29))

        self.data_inicio = QtWidgets.QDateEdit(parent=self.frame_personalisa)
        self.data_inicio.setGeometry(QtCore.QRect(30, 130, 120, 20))
        self.data_inicio.setDateTime(QtCore.QDateTime.currentDateTime())
        self.data_inicio.setCalendarPopup(True)
        self.data_inicio.setStyleSheet('border-color: #FFFFFF; border-radius: 10px; background-color: #FFFFFF;')
        self.data_inicio.setObjectName('data_inicio')

        self.inicio = QtWidgets.QLabel('Depois de ', self.frame_personalisa)
        self.inicio.setStyleSheet('font-size: 13px; margin: 0; padding: 0; border: none; background-color: #FFFFFF')
        self.inicio.setGeometry(15, 20, 63, 13)

        self.borda_fim = QtWidgets.QFrame(parent=self.frame_personalisa)
        self.borda_fim.setStyleSheet('border: 2px solid black; border-radius: 10px; background-color: #FFFFFF;')
        self.borda_fim.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.borda_fim.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.borda_fim.setObjectName('frame')
        self.borda_fim.setGeometry(QtCore.QRect(80, 140, 29, 29))

        self.data_final = QtWidgets.QDateEdit(parent=self.frame_personalisa)
        self.data_final.setGeometry(QtCore.QRect(85, 130, 120, 20))
        self.data_final.setStyleSheet('border-color: #FFFFFF; border-radius: 10px; background-color: #FFFFFF;')
        self.data_final.setDateTime(QtCore.QDateTime.currentDateTime())
        self.data_final.setCalendarPopup(True)
        self.data_final.setObjectName('data_final')

        self.fim = QtWidgets.QLabel('Antes de ', self.frame_personalisa)
        self.fim.setStyleSheet('font-size: 13px; margin: 0; padding: 0; border: none; background-color: #FFFFFF')
        self.fim.setGeometry(15, 75, 57, 13)

        self.aplicar = QtWidgets.QPushButton('Aplicar', self.frame_personalisa)
        self.aplicar.setGeometry(QtCore.QRect(100, 101, 23, 23))
        self.aplicar.clicked.connect(lambda: self.filtros(6))
        self.aplicar.setStyleSheet(
            'QPushButton {border: 2px solid #000000; border-radius: 10px; background-color: #FFFFFF; color: #2E3D48;} QPushButton:pressed {background-color: #2E3D48; color: #FFFFFF;}')

        self.btn_hoje = QtWidgets.QPushButton('Hoje', self.frame_box)
        self.btn_hoje.setGeometry(QtCore.QRect(0, 150, 60, 20))
        self.btn_hoje.setStyleSheet(colo)

        self.btn_7 = QtWidgets.QPushButton('Últimos 7 dias', self.frame_box)
        self.btn_7.setGeometry(QtCore.QRect(20, 150, 100, 20))
        self.btn_7.setStyleSheet(colo)

        self.btn_30 = QtWidgets.QPushButton('Últimos 30 dias', self.frame_box)
        self.btn_30.setGeometry(QtCore.QRect(40, 150, 120, 20))
        self.btn_30.setStyleSheet(colo)

        self.btn_ano = QtWidgets.QPushButton('Ano', self.frame_box)
        self.btn_ano.setGeometry(QtCore.QRect(60, 150, 60, 20))
        self.btn_ano.setStyleSheet(colo)

        self.btn_2ano = QtWidgets.QPushButton('2 Anos', self.frame_box)
        self.btn_2ano.setGeometry(QtCore.QRect(80, 150, 70, 20))
        self.btn_2ano.setStyleSheet(colo)

        self.btn_personalisa = QtWidgets.QPushButton('Período personalizado >', self.frame_box)
        self.btn_personalisa.setGeometry(QtCore.QRect(0, 100, 150, 20))

        self.btn_filtros.clicked.connect(self.abrir_items)

        self.btnfechar.setGeometry(QtCore.QRect(910, 20, 30, 23))
        self.btnfechar.setGeometry(QtCore.QRect(910, 20, 30, 23))
        self.btn_7.clicked.connect(lambda: self.filtros(2))
        self.btn_30.clicked.connect(lambda: self.filtros(3))
        self.btn_ano.clicked.connect(lambda: self.filtros(4))
        self.btn_2ano.clicked.connect(lambda: self.filtros(5))
        self.btn_hoje.clicked.connect(lambda: self.filtros(1))
        self.btnfechar.clicked.connect(lambda: self.filtros(0))
        self.btn_personalisa.clicked.connect(self.abrir_personalisa)
        self.btn_filtros.setStyleSheet("QPushButton {\n"
                                       "                border: 2px solid #2E3D48;\n"
                                       "                border-radius: 10px;\n"
                                       "                background-color: #FFFFFF;\n"
                                       "                color: #2E3D48;\n"
                                       "            }\n"
                                       "            QPushButton:pressed {\n"
                                       "                background-color: #2E3D48;\n"
                                       "                color: #FFFFFF;\n"
                                       "            }")

        self.retranslateUi(Form)
        self.main_layout = QVBoxLayout(self.content_widget)
        self.guia = 1
        self.day = "ONTEM"
        self.atualiza_historico()
        for widget in self.frame.findChildren(QtWidgets.QWidget):
            widget.show()
        self.btnfechar.hide()
        self.frame_personalisa.hide()
        self.frame_box.hide()
        self.btn_voltar = QtWidgets.QPushButton('Voltar', parent=Form)
        self.btn_voltar.setGeometry(QtCore.QRect(1, 3, 50, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_voltar.setFont(font)
        self.btn_voltar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_voltar.setStyleSheet("QPushButton{\n"
                                      "background-color: rgb(0, 0, 0);\n"
                                      "    color: rgb(255, 255, 255);\n"
                                      "    border-radius:10px;\n"
                                      "}\n"
                                      "QPushButton:hover{\n"
                                      "    background-color: rgb(255, 255, 255);\n"
                                      "    color: rgb(0, 0, 0);\n"
                                      "}")
        self.btn_voltar.setObjectName("login_2")
        self.btn_voltar.clicked.connect(lambda: self.voltar(Form))
        self.btn_voltar.show()
        self.conf_layout()

    def voltar(self, Form):
        self.tela.frame.show()
        self.frame.hide()
        self.btn_voltar.hide()
        self.tela.timer.start()
        _translate = QtCore.QCoreApplication.translate
        icon = QIcon('C:\\Users\\luist\\OneDrive\\Área de Trabalho\\Ti\\Nova pasta\\HC-UFMG\\SGL\\icone_p_eUO_icon.ico')
        Form.setWindowIcon(icon)
        Form.setWindowTitle(_translate('Form', 'Sistema de Gestão de Leitos'))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'HISTÓRICO'))
        self.label_ordenar.setText(_translate('Form', 'ORDENAR POR: '))

    def obter_dia_semana(self, data):
        dias_da_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
        dia_da_semana = data.weekday()
        return dias_da_semana[dia_da_semana]

    def atualiza_historico(self):
        self.frames = []
        self.labels = []
        self.labels_Data = []
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        analise = ''
        cursor = conexao.cursor()
        comando = 'SELECT * FROM history'
        cursor.execute(comando)
        leitura = cursor.fetchall()
        self.onRadioButtonToggled(leitura)
        leitura = self.leitura
        for linha in leitura:
            for column, valor in enumerate(linha):
                item = QtWidgets.QTableWidgetItem(str(valor))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                if analise!= item.text() and item.text()!= 'None' and (item is None) or (column == 1):
                    texto = item.text()
                    data_celula = datetime.datetime.strptime(texto, '%d/%m/%Y').date()
                    partes_data = texto.split('/')
                    data_ano_celula = partes_data[(-1)]
                    data_atual = datetime.datetime.now().date()
                    data_atual_ano = str(data_atual.year)
                    data_atual_2ano = str((data_atual - datetime.timedelta(days=365)).year)
                    if self.day == 'HOJE' and data_celula!= data_atual:
                        break
                    if self.day == 'SEMANA' and data_celula < data_atual - datetime.timedelta(days=7):
                        break
                    if self.day == 'MES' and data_celula < data_atual - datetime.timedelta(days=30):
                        break
                    if self.day == 'ANO' and data_ano_celula!= data_atual_ano:
                        break
                    if self.day == '2ANO' and data_ano_celula!= data_atual_2ano:
                        break
                    self.data_inicio1 = datetime.datetime.strptime(self.data_inicio.date().toString('dd/MM/yyyy'), '%d/%m/%Y').date()
                    self.data_final1 = datetime.datetime.strptime(self.data_final.date().toString('dd/MM/yyyy'), '%d/%m/%Y').date()
                    if self.day == 'PERSONALIZADO' and (not self.data_inicio1 <= data_celula <= self.data_final1):
                        frame = QFrame()
                        layout = QVBoxLayout(frame)
                        labels = []
                        continue
                    labels = []
                    frame = QFrame()
                    frame.setFrameShape(QFrame.Shape.Box)
                    frame.setContentsMargins(0, 80, 0, 0)
                    frame.setStyleSheet('QFrame { background-color: white; border: 1px solid #C0C0C0; border-radius: 10px; box-shadow: 5px 5px 5px grey; }')
                    x = 61
                    self.main_layout.addWidget(frame)
                    if data_celula == data_atual:
                        dia_da_semana = self.obter_dia_semana(data_celula)
                        texto_formatado = f"Hoje - {dia_da_semana}, {data_celula.strftime('%d/%m/%Y')}"
                    else:  # inserted
                        if data_celula == data_atual - datetime.timedelta(days=1):
                            dia_da_semana = self.obter_dia_semana(data_celula)
                            texto_formatado = f"Ontem - {dia_da_semana}, {data_celula.strftime('%d/%m/%Y')}"
                        else:  # inserted
                            dia_da_semana = self.obter_dia_semana(data_celula)
                            texto_formatado = f" {dia_da_semana}, {data_celula.strftime('%d/%m/%Y')}"
                    layout = QVBoxLayout(frame)
                    titulo_label = QtWidgets.QLabel(texto_formatado, frame)
                    titulo_label.setStyleSheet('font-size: 30px; font-weight: bold; margin: 0; padding: 0;border: none;')
                    titulo_label.setGeometry(5, 10, 1000, 40)
                    linha_frame = QFrame(frame)
                    linha_frame.setFrameShape(QFrame.Shape.HLine)
                    linha_frame.setFrameShadow(QFrame.Shadow.Sunken)
                    linha_frame.setStyleSheet('margin: 0; padding: 0; ')
                    linha_frame.setGeometry(0, 60, 3000, 1)
                    self.frames.append((frame, titulo_label))
                    self.labels_Data.append(titulo_label)
                    analise = item.text()
                if column == 2 and item.text()!= 'None' and (item is not None):
                    label = QtWidgets.QLabel(item.text(), frame)
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    label.setFont(font)
                    label.setStyleSheet(' background-color: none; border: none; border-radius: none; box-shadow: none; ')
                    self.labels.append(label)
                    labels.append(label)
                    label.setGeometry(3, x, 3000, 20)
                    x += 20

                    frame.setFixedSize(3000, x)
                if analise == item.text():
                    if column == 2:
                        if item.text()!= 'None':
                            if item is not None:
                                label = QtWidgets.QLabel(item.text(), frame)
                                font = QtGui.QFont()
                                label.setFont(font)
                                label.setStyleSheet(' background-color: none; border: none; border-radius: none; box-shadow: none; ')
                                label
                                label()
                                label.setGeometry(3, x, 3000, 20)
                                x += 20

    def onRadioButtonToggled(self, leitura):
        if self.guia!= 0:
            self.leitura = reversed(leitura)
        self.radio_recente.toggled.connect(lambda checked: self.onRadioRecenteToggled(checked, leitura))
        self.radio_antigo.toggled.connect(lambda checked: self.onRadioAntigoToggled(checked, leitura))

    def onRadioRecenteToggled(self, checked, leitura):
        if checked:
            self.leitura = reversed(leitura)
            for i in reversed(range(self.main_layout.count())):
                widget = self.main_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
            self.guia = 0
            self.atualiza_historico()

    def onRadioAntigoToggled(self, checked, leitura):
        if checked:
            self.leitura = leitura
            for i in reversed(range(self.main_layout.count())):
                widget = self.main_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
            self.guia = 0
            self.atualiza_historico()

    def filtros(self, index):
        self.btn_filtros.setStyleSheet('QPushButton {    border-top-right-radius: 0px;    border-bottom-right-radius: 0px;    border-top-left-radius: 10px;    border-bottom-left-radius: 10px;    background-color: #FFFFFF;    color: #2E3D48;    border: 2px solid black;}QPushButton:pressed {    background-color: #2E3D48;    color: #FFFFFF;}')
        if index == 1:
            self.day = 'HOJE'
            for i in reversed(range(self.main_layout.count())):
                widget = self.main_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
            self.btn_filtros.setText('Hoje')
            self.btn_filtros.setGeometry(QtCore.QRect(790, 20, 120, 23))
            self.btnfechar.show()
            self.atualiza_historico()
        else:  # inserted
            if index == 2:
                self.day = 'SEMANA'
                for i in reversed(range(self.main_layout.count())):
                    widget = self.main_layout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()
                self.btn_filtros.setText('Ultimos 7 dias')
                self.btn_filtros.setGeometry(QtCore.QRect(790, 20, 120, 23))
                self.btnfechar.show()
                self.atualiza_historico()
            else:  # inserted
                if index == 3:
                    self.day = 'MES'
                    for i in reversed(range(self.main_layout.count())):
                        widget = self.main_layout.itemAt(i).widget()
                        if widget is not None:
                            widget.deleteLater()
                    self.btn_filtros.setText('Ultimos 30 dias')
                    self.btn_filtros.setGeometry(QtCore.QRect(790, 20, 120, 23))
                    self.btnfechar.show()
                    self.atualiza_historico()
                else:  # inserted
                    if index == 4:
                        self.day = 'ANO'
                        for i in reversed(range(self.main_layout.count())):
                            widget = self.main_layout.itemAt(i).widget()
                            if widget is not None:
                                widget.deleteLater()
                        current_datetime = QDateTime.currentDateTime()
                        formatted_date = current_datetime.toString('yyyy')
                        self.btn_filtros.setGeometry(QtCore.QRect(790, 20, 120, 23))
                        self.btn_filtros.setText(f'{formatted_date}')
                        self.btnfechar.show()
                        self.atualiza_historico()
                    else:  # inserted
                        if index == 5:
                            self.day = '2ANO'
                            for i in reversed(range(self.main_layout.count())):
                                widget = self.main_layout.itemAt(i).widget()
                                if widget is None:
                                    continue
                                widget.deleteLater()
                            current_datetime = QDateTime.currentDateTime()
                            formatted_date = current_datetime.addYears((-1)).toString('yyyy')
                            self.btn_filtros.setGeometry(QtCore.QRect(790, 20, 120, 23))
                            self.btn_filtros.setText(f'{formatted_date}')
                            self.btnfechar.show()
                            self.atualiza_historico()
                        else:  # inserted
                            if index == 6:
                                self.day = 'PERSONALIZADO'
                                self.data_i = self.data_inicio.date()
                                self.data_f = self.data_final.date()
                                for i in reversed(range(self.main_layout.count())):
                                    widget = self.main_layout.itemAt(i).widget()
                                    if widget is not None:
                                        widget.deleteLater()
                                self.btn_filtros.setText('Período personalizado')
                                self.btn_filtros.setGeometry(QtCore.QRect(790, 20, 120, 23))
                                self.btnfechar.show()
                                self.atualiza_historico()
                            else:  # inserted
                                if index == 0:
                                    self.day = 'ONTEM'
                                    for i in reversed(range(self.main_layout.count())):
                                        widget = self.main_layout.itemAt(i).widget()
                                        if widget is not None:
                                            widget.deleteLater()
                                    self.btn_filtros.setGeometry(QtCore.QRect(790, 20, 150, 23))
                                    self.btn_filtros.setText('▼ Selecione uma Data ')
                                    self.btn_filtros.setStyleSheet('QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')
                                    self.btnfechar.hide()
                                    self.atualiza_historico()

    def abrir_personalisa(self):
        if self.frame_personalisa.isHidden():
            self.frame_personalisa.show()
            self.frame_box.setStyleSheet('background-color: #FFFFFF; border-top-left-radius: 20px; border-bottom: 1px solid black;')
            self.frame_personalisa.setStyleSheet('\n                        QFrame  {\n                            background-color: #FFFFFF;\n                            border-top-right-radius: 20px;\n                            border-bottom: 1px solid black;\n                            border-left: 1px solid black;\n                        }\n                    ')
        else:  # inserted
            self.frame_personalisa.hide()
            self.frame_box.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
            self.frame_personalisa.setStyleSheet('\n                        QFrame  {\n                            background-color: #FFFFFF;\n                            border-top-right-radius: 20px;\n                            border-bottom-right-radius: 20px;\n                            border-left: 1px solid black;\n                        }\n                    ')

    def abrir_items(self):
        if self.frame_box.isHidden():
            self.frame_box.show()
        else:  # inserted
            self.frame_box.hide()
            if not self.frame_personalisa.isHidden():
                self.frame_personalisa.hide()

    def pesquisar(self):
        text = self.pesquisa_historico.text().lower()
        for frame, titulo in self.frames:
            frame_visible = any((text in label.text().lower() and label.text()!= titulo.text() for label in frame.findChildren(QtWidgets.QLabel)))
            frame.setVisible(frame_visible)
            titulo.setVisible(frame_visible)
            labels = []
            i = 61
            for label in frame.findChildren(QtWidgets.QLabel):
                labels.append(label)
                if text not in label.text().lower() and label.text()!= titulo.text():
                    label.setVisible(False)
                    labels.append(label)
                else:  # inserted
                    label.setVisible(True)
                    if label.text()!= titulo.text():
                        label.move(0, i)
                        i += 20
            frame.setFixedSize(3000, i)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.btn_filtros.click()

    def conf_layout(self):
        if self.settings.contains('tema'):
            font_name = self.settings.value('font', defaultValue='')
            backcolocor = self.settings.value('tema', defaultValue='')
            color = self.settings.value('color', defaultValue='')
            tamanho = int(self.settings.value('tamanho', defaultValue=10))
        else:  # inserted
            backcolocor = '#5DADE2'
            color = 'Black'
            tamanho = 12
            font_name = 'Segoe UI'
        self.backcolocor = backcolocor
        self.color = color
        self.font = font_name
        self.tamanho = tamanho
        for label in self.frame.findChildren(QtWidgets.QLabel):
            if label not in self.labels_Data:
                label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name};border-top: 0.2px solid white;border-bottom: 0.2px solid white;border-right: 0.2px solid white;border-left: none;')
        self.frame.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;')