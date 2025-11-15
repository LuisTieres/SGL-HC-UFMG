from PyQt6.QtGui import QFont
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QDateTime, Qt, QSettings, QStandardPaths
import pymysql
from PyQt6.QtWidgets import QMessageBox,QSizePolicy
from PyQt6.QtGui import QIcon
import psycopg2
import re
import unicodedata
import sys

class Ui_reserva(QtWidgets.QMainWindow):
    def setupUi(self, Form, variavel, dados_demanda=None):
        self.ala = 'CTI PEDIÁTRICO - 06N'

        self.host = dados_demanda.host
        self.usermysql = dados_demanda.usermysql
        self.password = dados_demanda.password
        self.database = dados_demanda.database

        self.lista_btn = []
        self.lista_titulo = []
        self.lista_ids = []

        self.dados = dados_demanda
        self.variavel = variavel
        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)

        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setStyleSheet('background-color: #2c7f4f;border:none')
        self.frame.setGeometry(QtCore.QRect(350, 80, 729,630))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.dados.janela_reserva = self.frame

        self.frame.mousePressEvent = lambda event, frame=self.frame: self.mousePressEvent_2(event, frame)
        self.frame.mouseReleaseEvent = lambda event, frame=self.frame: self.mouseReleaseEvent_2(event, frame)
        self.frame.mouseMoveEvent = lambda event, frame=self.frame: self.mouseMoveEvent_2(event, frame)
        icon = QIcon('imagens/emergencia.ico')
        pixmap = icon.pixmap(50, 50)
        self.icone = QtWidgets.QLabel(parent=self.frame)
        self.icone.setPixmap(pixmap)
        self.icone.setGeometry(QtCore.QRect(3, 3, 50, 50))
        self.icone.show()
        self.numero_versao_atual = None
        self.tabela_reserva = QtWidgets.QTreeWidget(parent=self.frame)
        self.tabela_reserva.setGeometry(QtCore.QRect(100, 180, 551, 400))
        self.tabela_reserva.setStyleSheet('background-color: rgb(255, 255, 255);border: none;gridline-color: black;')
        self.tabela_reserva.setObjectName('Tabela de reserva')

        scroll_area = QtWidgets.QScrollArea(self.frame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("background: transparent; border: none;")

        self.quantidade_colunas = 0
        self.lista_nomes_das_colunas = []
        self.scroll_area = scroll_area
        scroll_content = QtWidgets.QWidget()
        scroll_content.setStyleSheet("background: transparent; border: none;")
        scroll_area.setWidget(scroll_content)

        scroll_area.move(50, 0)

        grid_layout = QtWidgets.QGridLayout(scroll_content)
        grid_layout.setContentsMargins(5, 5, 5, 5)
        grid_layout.setSpacing(5)

        scroll_area.setFixedHeight(150)
        scroll_area.setFixedWidth(650)

        from database_Grade import Ui_data_Grade
        self.data_grade = Ui_data_Grade()
        self.data_grade.ler_btn_tabela_Grade(self)
        self.lista_btns = []

        btns_por_linha = 6

        for cont, btn_name in enumerate(self.lista_btn):
            btn = QtWidgets.QPushButton(btn_name)
            btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            btn.setFixedHeight(35)
            btn.setFixedWidth(100)

            linha = cont // btns_por_linha
            coluna = cont % btns_por_linha
            grid_layout.addWidget(btn, linha, coluna)

            btn.clicked.connect(lambda _, titulo=self.lista_titulo[cont], btn_=btn, id = self.lista_ids[cont]: self.vagos(titulo, btn_,id))
            self.lista_btns.append(btn)

        self.proc_leito = QtWidgets.QLineEdit(parent=self.frame)
        self.proc_leito.setGeometry(QtCore.QRect(100, 150, 350, 20))
        self.proc_leito.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.proc_leito.setObjectName('Proc Leito')
        self.proc_leito.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        icon = QIcon('imagens/lupa.ico')
        self.proc_leito.addAction(icon, QtWidgets.QLineEdit.ActionPosition.LeadingPosition)
        self.proc_leito.setPlaceholderText('Pesquisar Paciente')

        self.btn_reserva = QtWidgets.QPushButton(parent=self.frame)
        self.btn_reserva.setGeometry(QtCore.QRect(550, 590, 101, 31))
        self.btn_reserva.setObjectName('pushButton')
        self.btn_reserva.clicked.connect(lambda: self.reservar_leito('RESERVADO'))
        self.btn_reserva.setStyleSheet('\n                QPushButton {\n                    border: 2px solid #2E3D48;\n                    border-radius: 10px;\n                    background-color: #FFFFFF;\n                    color: #2E3D48;\n                }\n\n                QPushButton:hover {\n                    background-color: #DDDDDD;  /* Change this to your desired hover color */\n                    color: rgb(0, 0, 0);\n                }\n\n                QPushButton:pressed {\n                    background-color: #2E3D48;  /* Change this to your desired pressed color */\n                    color: #FFFFFF;\n                }\n            ')
        self.btn_reserva.hide()
        self.btn_ocupa = QtWidgets.QPushButton(parent=self.frame)
        self.btn_ocupa.setGeometry(QtCore.QRect(430, 590, 101, 31))
        self.btn_ocupa.setObjectName('pushButton')
        self.btn_ocupa.clicked.connect(lambda: self.reservar_leito('OCUPADO'))
        self.btn_ocupa.setStyleSheet('\n                QPushButton {\n                    border: 2px solid #2E3D48;\n                    border-radius: 10px;\n                    background-color: #FFFFFF;\n                    color: #2E3D48;\n                }\n\n                QPushButton:hover {\n                    background-color: #DDDDDD;  /* Change this to your desired hover color */\n                    color: rgb(0, 0, 0);\n                }\n\n                QPushButton:pressed {\n                    background-color: #2E3D48;  /* Change this to your desired pressed color */\n                    color: #FFFFFF;\n                }\n            ')
        self.btn_ocupa.hide()
        self.proc_leito.textChanged.connect(self.pesquisar)
        for widget in self.frame.findChildren(QtWidgets.QWidget):
            widget.show()
        self.frame.show()
        self.retranslateUi(Form)
        self.vagos(self.lista_titulo[0],self.lista_btns[0],self.lista_ids[0])
        self.conf_layout()

        scroll_area.setStyleSheet("background: transparent; border: none;")

        scroll_content.setStyleSheet("background: transparent; border: none;")

    def pesquisar(self, pesquisa):
        num_linhas = self.tabela_reserva.topLevelItemCount()
        for row in range(num_linhas):
            item = self.tabela_reserva.topLevelItem(row)
            selecao = item.text(1)
            if pesquisa.lower() in selecao.lower():
                item.setHidden(False)
            else:  # inserted
                item.setHidden(True)

    def reservar_leito(self, acao):
        ala = self.ala
        analise = False
        analise2 = False
        selecionado = []
        selecionado2 = []
        selecao_demanda = self.dados.tabela_dem()
        cont = self.dados.conta_linha()
        for row in range(cont):
            selec = selecao_demanda.item(row, 0)
            if selec is not None and selec.checkState() == QtCore.Qt.CheckState.Checked:
                analise = True
                selecionado.append(row)
        num_linhas = self.tabela_reserva.topLevelItemCount()
        for row in range(num_linhas):
            item = self.tabela_reserva.topLevelItem(row)
            selecao = self.tabela_reserva.itemWidget(item, 0)
            if selecao.isChecked():
                analise2 = True
                selecionado2.append(row)

        if analise== False:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText(f'Nenhuma Demanda Selecionada!')
            icon = QIcon('imagens/warning.ico')
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()

        if analise2== False:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText(f'Nenhum Leito Selecionado!')
            icon = QIcon('imagens/warning.ico')
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()

        if analise and analise2:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('Reservar Leito?')
            icon = QIcon('imagens/warning.ico')
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            reply = msg_box.exec()
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                colum_nome = 0
                colum_data_nas = 0
                colum_pronto = 0
                colum_npf = 0
                colum_obs = 0
                for row, raw in zip(selecionado, selecionado2):
                    for colum in range(1, self.dados.tabelademan.columnCount()):
                        item_pac = self.dados.tabelademan.horizontalHeaderItem(colum)
                        if item_pac.text() == 'NOME DO PACIENTE':
                            colum_nome = colum
                        if item_pac.text() == 'DATA DE NASCIMENTO':
                            colum_data_nas = colum
                        if item_pac.text() == 'PRONTUÁRIO':
                            colum_pronto = colum
                        if item_pac.text() == 'NPF':
                            colum_npf = colum
                        if item_pac.text() == 'OBSERVAÇÕES':
                            colum_obs = colum

                    nome = selecao_demanda.item(row, colum_nome)
                    print(nome.text())
                    data_nas = selecao_demanda.item(row, colum_data_nas)
                    pronto = selecao_demanda.item(row, colum_pronto).text()
                    npf = selecao_demanda.item(row, colum_npf).text()
                    print(nome.text(), data_nas, pronto, npf)
                    item = self.tabela_reserva.topLevelItem(raw)
                    leito = item.text(1)
                    status_atual = item.text(2)
                    tipo = item.text(3)
                    obs = selecao_demanda.item(row, colum_obs).text()
                    current_datetime = QDateTime.currentDateTime()
                    formatted_datetime = current_datetime.toString('dd/MM/yyyy hh:mm:ss')
                    status = acao

                    from database_Demandas import Ui_data_Demanda
                    self.data_deman = Ui_data_Demanda()
                    self.data_deman.reservar_leito(self.dados, self.variavel, status, leito, formatted_datetime,nome,row+1)

                    conexao = pymysql.connect(
                        host=self.dados.host,
                        user=self.dados.usermysql,
                        password=self.dados.password,
                        database=self.dados.database
                    )

                    cursor = conexao.cursor()
                    leito = leito.replace(' ', '_')

                    from database_Grade import Ui_data_Grade
                    self.data_grade = Ui_data_Grade()

                    if status_atual!= 'OCUPADO' and 'RESERVA' not in status_atual:
                        print(leito)

                        self.data_grade.reservar_leito_grade_reserva(self.dados, tipo, obs, pronto, npf, nome, status, data_nas, leito,
                                                     self.codigo_ala,
                                                     formatted_datetime)
                    else:
                        self.data_grade.reservar_leito_grade_reserva(self.dados, tipo, obs, pronto, npf, nome, status,
                                                                     data_nas, leito + '_aguardando',
                                                                     self.codigo_ala,
                                                                     formatted_datetime)

                    # conexao = pymysql.connect(
                    #     host=self.dados.host,
                    #     user=self.dados.usermysql,
                    #     password=self.dados.password,
                    #     database=self.dados.database
                    # )
                    #
                    # cursor = conexao.cursor()
                    # current_datetime = QDateTime.currentDateTime()
                    # formatted_date = current_datetime.toString('dd/MM/yyyy')
                    # current_datetime = QDateTime.currentDateTime()
                    # formatted_time = current_datetime.toString('hh:mm')
                    # texto = f'{formatted_time}                LEITO {leito} FOI RESERVADO POR {self.dados.nome_user} PARA {nome.text()} NASCIDO NO DIA {data_nas.text()}'
                    # data = formatted_date
                    # comando = 'INSERT INTO history (data, histo) VALUES (%s, %s)'
                    # valores = (data, texto)
                    # cursor.execute(comando, valores)
                    # conexao.commit()
                    # cursor.close()
                    # conexao.close()

                    current_datetime = QDateTime.currentDateTime()
                    formatted_date = current_datetime.toString('dd/MM/yyyy')
                    current_datetime = QDateTime.currentDateTime()
                    formatted_time = current_datetime.toString('hh:mm')

                    leitox = leito.replace('_', ' ')
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Information)
                    msg_box.setWindowTitle('AVISO')
                    msg_box.setText(f'Rerserva no leito {leitox} Realizda')
                    icon = QIcon('imagens/warning.ico')
                    msg_box.setWindowIcon(icon)
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg_box.exec()

                    item = self.dados.tabelademan.item(row, 0)

                    if item is not None and item.background().style() != QtGui.QBrush().style():
                        adjusted_color = item.background().color()
                    else:
                        adjusted_color = QColor("white")

                    selecao = QtWidgets.QTableWidgetItem()
                    selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                    selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
                    selecao.setBackground(QtGui.QBrush(adjusted_color))
                    self.dados.tabelademan.setItem(row, 0, selecao)
                    self.data_grade.ler_colunas_Grade(self, self.id)

                    texto_historico = (f'{formatted_time}                {self.dados.nome_user} RESERVOU O LEITO {leitox} PARA O PACIENTE \"{nome.text()}\"')
                    print(nome.text(), data_nas, pronto, npf)
                    coluna_alteracao = f'{row}'
                    alteracao = 'RESERVOU'

                    self.data_deman.criar_ou_atualizar_snapshot(self.variavel, self.dados, pronto, data_nas.text(), nome.text(),
                                                                texto_historico, coluna_alteracao, alteracao)

                    alteracao = 'RESERVOU'
                    coluna_alteracao = f"{raw}"

                    lista_leitos = self.data_grade.lista_leitos_filtro_aghu(self)
                    leitura = self.data_grade.ler_database(self, lista_leitos)
                    tabela = self.formatar_nome(self.ala)
                    self.data_grade.criar_ou_atualizar_snapshot(tabela, self, pronto, data_nas.text(), nome.text(),
                                                                texto_historico,
                                                                coluna_alteracao, alteracao, leitura)

        self.vagos(self.ala,self.btn,self.id)
        self.dados.atualiza_tabela_demandas(self.variavel)

    def formatar_nome(self,nome_original):
        # Remove acentos
        nome = unicodedata.normalize('NFKD', nome_original)
        nome = nome.encode('ASCII', 'ignore').decode('utf-8')

        # Coloca tudo em minúsculas
        nome = nome.lower()

        # Remove preposições
        preposicoes = [' de ', ' da ', ' do ']
        for prep in preposicoes:
            nome = nome.replace(prep, ' ')

        # Substitui hífens e múltiplos espaços por underscore
        nome = nome.replace('-', ' ')
        nome = re.sub(r'\s+', '_', nome)  # troca múltiplos espaços por um underscore
        nome = re.sub(r'[^a-z0-9_]', '', nome)  # remove qualquer caractere inválido

        return nome
    def apagar_leito(self):
        analise = False
        selecionado = []
        num_linhas = self.tabela_reserva.topLevelItemCount()
        for row in range(num_linhas):
            item = self.tabela_reserva.topLevelItem(row)
            selecao = item.checkState(0)
            if selecao == QtCore.Qt.CheckState.Checked:
                analise = True
                selecionado.append(row)
        if analise:
            for row in reversed(selecionado):
                self.tabela_reserva.takeTopLevelItem(row)

    def ler_PostgreSQL(self, nome):
        try:
            connection = psycopg2.connect(
                user='ugen_integra',
                password='aghuintegracao',
                host='10.36.2.35',
                port='6544',
                database='dbaghu'
            )
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM AGH.AGH_UNIDADES_FUNCIONAIS')
            rows = cursor.fetchall()

            for row in rows:
                if row[1] == nome:
                    self.codigo_ala = row[0]
                    break

        except psycopg2.Error as e:
            print('Erro ao conectar ao PostgreSQL:', e)

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def vagos(self, ala,btn,id):

        self.ala = ala
        self.btn = btn
        self.id = id

        style_normal = """
                                QPushButton {
                                    background-color: transparent;
                                    color: black;
                                    border: none;
                                    padding: 10px 20px;
                                    font-size: 10px;
                                }
                                QPushButton:hover {
                                    background-color: #555;
                                }
                                QPushButton:pressed {
                                    background-color: #777;
                                }
                            """

        style_clicado = """
                                QPushButton {
                                    background-color: white;
                                    color: black;
                                    font-size: 12px;
                                    font-weight: bold;
                                    border: none;
                                    padding: 10px;
                                    border-radius: 5px;
                                }
                                QPushButton:hover {
                                    background-color: #c1d9f7;
                                }
                                QPushButton:pressed {
                                    background-color: #99c3f4;
                                }
                            """

        for btn_ in self.lista_btns:
            if btn == btn_:
                btn.setStyleSheet(style_clicado)
            else:
                btn_.setStyleSheet(style_normal)

        self.ler_PostgreSQL(ala)
        lista_leitos = []
        connection = psycopg2.connect(user='ugen_integra', password='aghuintegracao', host='10.36.2.35', port='6544', database='dbaghu')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM AGH.ain_leitos WHERE ind_situacao != %s", ('I',))

        rows = cursor.fetchall()
        for row in rows:
            if row[6] == self.codigo_ala:
                sem_hifen = row[0].split('-')[0]
                semzero = row[2].lstrip('0')
                dados = f'{sem_hifen}_{semzero}'
                lista_leitos.append(dados)

        colum1 = self.data_grade.pegar_coluna_Grade(self, id, 'STATUS DO LEITO')
        column_status = "col" if colum1 == 0 else f"col{colum1}"

        colum2 = self.data_grade.pegar_coluna_Grade(self, id, 'SEXO DA ENFERMARIA')
        column_sexo = "col" if colum2 == 0 else f"col{colum2}"

        colunas = ['idGRADE',column_status,column_sexo]

        leitura = self.data_grade.pegar_Dados_das_Colunas_Grade(self,colunas)

        self.tabela_reserva.clear()
        self.tabela_reserva.setColumnCount(4)
        self.tabela_reserva.setHeaderLabels(['', 'LEITOS', 'STATUS', 'SEXO DA ENFERMARIA'])

        i = 0
        coluna_0 = [linha[0] for linha in leitura]
        cont = 0

        for i, linha in enumerate(leitura):
            if i + 1 < len(leitura):
                proxima_linha = leitura[i + 1]
                print(i)
                print(str(linha[0]), 'espaço', str(proxima_linha[0]))
                if (str(linha[0]) + '_aguardando') in coluna_0:
                    continue
                if 'aguardando' in str(linha[0]) or 'aguardando' in str(proxima_linha):
                    continue
            if str(linha[0]) not in lista_leitos:
                continue

            item = str(linha[0]).replace('_', ' ')
            self.addTreeItem(cont, item, str(linha[1]), str(linha[2]))
            cont+=1

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate

        self.btn_reserva.setText(_translate('Form', 'RESERVAR LEITO'))
        self.btn_ocupa.setText(_translate('Form', 'OCUPAR LEITO'))

    def addTreeItem(self, i, leito, status, tipo):
        item = QtWidgets.QTreeWidgetItem(self.tabela_reserva)
        checkbox = QtWidgets.QCheckBox()
        checkbox.setChecked(False)

        item.setText(1, leito)
        item.setText(2, status)
        item.setText(3, tipo)

        print(leito, status, tipo, 'dados')
        self.tabela_reserva.setItemWidget(item, 0, checkbox)
        checkbox.stateChanged.connect(lambda state, row=i: self.checkboxStateChanged(state, row))
        self.apagar_leito()

    def checkboxStateChanged(self, state, row):
        item = self.tabela_reserva.topLevelItem(row)
        status = item.text(2)

        if status == 'OCUPADO' or 'RESERVA' in status:
            self.btn_ocupa.setEnabled(False)
        else:
            self.btn_ocupa.setEnabled(True)

        selected_count = 0
        column = self.tabela_reserva.columnCount()
        quantidade_selecionados_demanda = 0
        selecao_demanda = self.dados.tabela_dem()
        cont = self.dados.conta_linha()

        for row in range(cont):
            selec = selecao_demanda.item(row, 0)
            if selec is not None and selec.checkState() == QtCore.Qt.CheckState.Checked:
                quantidade_selecionados_demanda += 1

        for row in range(self.tabela_reserva.topLevelItemCount()):
            item2 = self.tabela_reserva.topLevelItem(row)
            checkbox = self.tabela_reserva.itemWidget(item2, 0)
            if checkbox is not None and checkbox.isChecked():
                if selected_count < quantidade_selecionados_demanda:
                    selected_count += 1

        if selected_count == quantidade_selecionados_demanda:
            for i in range(self.tabela_reserva.topLevelItemCount()):
                item = self.tabela_reserva.topLevelItem(i)
                checkbox = self.tabela_reserva.itemWidget(item, 0)
                item.setDisabled(not checkbox.isChecked())
                checkbox.setEnabled(checkbox.isChecked())

        else:
            for i in range(0, self.tabela_reserva.topLevelItemCount()):
                item = self.tabela_reserva.topLevelItem(i)
                checkbox = self.tabela_reserva.itemWidget(item, 0)
                if item.checkState(0) != Qt.CheckState.Checked:
                    checkbox.setEnabled(not checkbox.isChecked())

    def conf_layout(self):
        if self.settings.contains('tema'):
            font_name = self.settings.value('font', defaultValue='')
            backcolocor = self.settings.value('tema', defaultValue='')
            color = self.settings.value('color', defaultValue='')
            tamanho = int(self.settings.value('tamanho', defaultValue=10))
        else:
            backcolocor = '#2c7f4f'
            color = 'Black'
            tamanho = 12
            font_name = 'Segoe UI'
        self.backcolocor = backcolocor
        self.color = color
        self.font = font_name
        self.tamanho = tamanho

        for label in self.frame.findChildren(QtWidgets.QLabel):
            label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name}; border:none')

        self.frame.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;border: 2px solid #2E3D48;border-radius: 10px;')

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