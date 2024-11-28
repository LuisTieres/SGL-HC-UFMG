from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QComboBox
import mysql.connector
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QDateTime, Qt, QRect, QSettings, QStandardPaths, QPoint

class Ui_Form(object):

    def setupUi(self, Form, alta, grade=None):
        self.host_mysql = 'localhost'
        self.user_mysql = ('root',)
        self.password_mysql = 'camileejose'
        self.alta = alta
        self.grade = grade

        self.settings = QSettings('HC', 'SGL')
        script_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = f'{script_directory}/config.ini'
        self.settings = QSettings(config_file_path, QSettings.Format.IniFormat)

        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setGeometry(QtCore.QRect(270, 50, 790, 538))
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName('frame')
        self.grade.janela_realocar = self.frame

        self.tabela_demanda = QtWidgets.QTableWidget(parent=self.frame)
        self.tabela_demanda.setGeometry(QtCore.QRect(10, 110, 751, 251))
        self.tabela_demanda.setStyleSheet('background-color: rgb(255, 255, 255);border: none;gridline-color: black;')
        self.tabela_demanda.setObjectName('tabela_demanda')
        self.tabela_demanda.setColumnCount(11)
        self.tabela_demanda.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()

        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabela_demanda.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabela_demanda.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabela_demanda.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabela_demanda.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabela_demanda.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabela_demanda.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabela_demanda.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabela_demanda.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabela_demanda.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabela_demanda.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabela_demanda.setHorizontalHeaderItem(10, item)

        colo = '\n            QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }\n        '

        self.BARRADEPESQUISA = QtWidgets.QLineEdit(parent=self.frame)
        self.BARRADEPESQUISA.setGeometry(QtCore.QRect(130, 80, 301, 21))
        self.BARRADEPESQUISA.setObjectName('BARRADEPESQUISA')
        self.BARRADEPESQUISA.setStyleSheet('border: 2px solid white; border-radius: 10px; background-color: white;')
        self.BARRADEPESQUISA.textChanged.connect(self.pesquisar)

        self.procurar = QtWidgets.QLabel(parent=self.frame)
        self.procurar.setGeometry(QtCore.QRect(10, 83, 115, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.procurar.setFont(font)
        self.procurar.setObjectName('label')

        self.tabela_demanda.setHorizontalHeaderItem(8, item)
        self.tabela_demanda.horizontalHeader().setDefaultSectionSize(140)
        self.tabela_demanda.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)

        self.ps = QtWidgets.QPushButton(parent=self.frame)
        self.ps.setGeometry(QtCore.QRect(10, 55, 111, 21))
        self.ps.setObjectName('ps')
        self.ps.setStyleSheet(colo)
        self.ps.clicked.connect(lambda: self.atualiza_tela('PS', Form))

        self.onco_hemato_ped = QtWidgets.QPushButton(parent=self.frame)
        self.onco_hemato_ped.setGeometry(QtCore.QRect(673, 55, 116, 21))
        self.onco_hemato_ped.setObjectName('onco_hemato_ped')
        self.onco_hemato_ped.clicked.connect(lambda: self.atualiza_tela('ONCO_HEMATO_PED', Form))
        self.onco_hemato_ped.setStyleSheet(colo)

        self.tran_inte = QtWidgets.QPushButton(parent=self.frame)
        self.tran_inte.setGeometry(QtCore.QRect(563, 55, 101, 21))
        self.tran_inte.setObjectName('tran_inte')
        self.tran_inte.clicked.connect(lambda: self.atualiza_tela('TRA_INTER', Form))
        self.tran_inte.setStyleSheet(colo)

        self.agenda_bloco = QtWidgets.QPushButton(parent=self.frame)
        self.agenda_bloco.setGeometry(QtCore.QRect(200, 55, 98, 21))
        self.agenda_bloco.setObjectName('agenda_bloco')
        self.agenda_bloco.clicked.connect(lambda: self.atualiza_tela('AGENDA_BLOCO', Form))
        self.agenda_bloco.setStyleSheet(colo)

        self.inter_tran_exte = QtWidgets.QPushButton(parent=self.frame)
        self.inter_tran_exte.setGeometry(QtCore.QRect(416, 55, 137, 21))
        self.inter_tran_exte.setObjectName('inter_tran_exte')
        self.inter_tran_exte.clicked.connect(lambda: self.atualiza_tela('INTER_TRAN_EXTER', Form))
        self.inter_tran_exte.setStyleSheet(colo)

        self.hemodinamica = QtWidgets.QPushButton(parent=self.frame)
        self.hemodinamica.setGeometry(QtCore.QRect(307, 55, 100, 21))
        self.hemodinamica.setObjectName('hemodinamica')
        self.hemodinamica.clicked.connect(lambda: self.atualiza_tela('HEMODINAMICA', Form))
        self.hemodinamica.setStyleSheet(colo)

        self.alta_cti = QtWidgets.QPushButton(parent=self.frame)
        self.alta_cti.setGeometry(QtCore.QRect(130, 55, 61, 21))
        self.alta_cti.setObjectName('alta_cti')
        self.alta_cti.clicked.connect(lambda: self.atualiza_tela('ALTA_CTI', Form))
        self.alta_cti.setStyleSheet(colo)

        self.titulo = QtWidgets.QLabel(parent=self.frame)
        self.titulo.setGeometry(QtCore.QRect(170, 23, 398, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.titulo.setFont(font)
        self.titulo.setStyleSheet('alternate-background-color: rgb(255, 255, 255);')
        self.titulo.setObjectName('titulo')

        self.confirmar = QtWidgets.QPushButton(parent=self.frame)
        self.confirmar.setGeometry(QtCore.QRect(615, 420, 120, 30))
        self.confirmar.setObjectName('confirmar')
        self.confirmar.clicked.connect(self.realocar)
        self.confirmar.setStyleSheet(colo)

        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(590, 390, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName('label')
        self.atualiza_tela('PS', Form)
        self.retranslateUi_ps(Form)
        self.load(Form)
        for widget in self.frame.findChildren(QtWidgets.QWidget):
            widget.show()
        self.frame.show()

    def realocar(self):
        analise = False
        analise2 = False
        selecionado = []
        selecionado2 = []
        cont = self.grade.conta_linha()
        selecao_grade = self.grade.tabela_grade1()
        for row in range(cont):
            selec = selecao_grade.item(row, 0)
            if selec.checkState() == QtCore.Qt.CheckState.Checked:
                analise = True
                selecionado2.append(row)
        num_linhas = self.tabela_demanda.rowCount()
        for row in range(num_linhas):
            item = self.tabela_demanda.item(row, 0)
            selecao = item.checkState()
            if selecao == QtCore.Qt.CheckState.Checked:
                analise2 = True
                selecionado.append(row)
        if analise and analise2:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg_box.setWindowTitle('AVISO')
            msg_box.setText('Reservar Leito?')
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            reply = msg_box.exec()
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                for row in reversed(selecionado):
                    if self.dep == 'PS':
                        nome = self.tabela_demanda.item(row, 4)
                        data_nas = self.tabela_demanda.item(row, 3)
                    if self.dep == 'ALTA_CTI':
                        nome = self.tabela_demanda.item(row, 5)
                        data_nas = self.tabela_demanda.item(row, 4)
                    if self.dep == 'AGENDA_BLOCO':
                        nome = self.tabela_demanda.item(row, 2)
                        data_nas = self.tabela_demanda.item(row, 3)
                    if self.dep == 'HEMODINAMICA':
                        nome = self.tabela_demanda.item(row, 2)
                        data_nas = self.tabela_demanda.item(row, 3)
                    if self.dep == 'INTER_TRAN_EXTER':
                        nome = self.tabela_demanda.item(row, 3)
                        data_nas = self.tabela_demanda.item(row, 4)
                    if self.dep == 'TRA_INTER':
                        nome = self.tabela_demanda.item(row, 2)
                        data_nas = self.tabela_demanda.item(row, 3)
                    if self.dep == 'ONCO_HEMATO_PED':
                        nome = self.tabela_demanda.item(row, 2)
                        data_nas = self.tabela_demanda.item(row, 3)
                    for row2 in reversed(selecionado2):
                        leito = self.grade.leito(row2)
                        current_datetime = QDateTime.currentDateTime()
                        formatted_datetime = current_datetime.toString('dd/MM/yyyy hh:mm:ss')
                        status = 'RESERVADO'
                        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                        if self.dep == 'PS':
                            cursor = conexao.cursor()
                            comando = f'UPDATE tabela_demanda_ps SET STATUS_SOLICITACAO = "{status}", LEITO_RESERVADO = "{leito.text()}", DATA_HORA_RESERVA = "{formatted_datetime}" WHERE NOME = "{nome.text()}"'
                            cursor.execute(comando)
                            conexao.commit()
                        if self.dep == 'ALTA_CTI':
                            cursor = conexao.cursor()
                            comando = f'UPDATE alta_cti SET STATUS_SOLICITACAO = "{status}", LEITO_RESERVADO = "{leito.text()}", DATA_HORÁRIO_DA_RESERVA = "{formatted_datetime}" WHERE NOME_DO_PACIENTE = "{nome.text()}"'
                            cursor.execute(comando)
                            conexao.commit()
                        if self.dep == 'AGENDA_BLOCO':
                            cursor = conexao.cursor()
                            comando = f'UPDATE tabela_agenda_bloco_demanda SET STATUS_SOLICITACAO = "{status}", LEITO_RESERVADO = "{leito.text()}", DATA_HORÁRIO_DA_RESERVA = "{formatted_datetime}" WHERE NOME_DO_PACIENTE = "{nome.text()}"'
                            cursor.execute(comando)
                            conexao.commit()
                        if self.dep == 'HEMODINAMICA':
                            cursor = conexao.cursor()
                            comando = f'UPDATE tabela_hemodinamica SET STATUS_SOLICITACAO = "{status}", LEITO_RESERVADO = "{leito.text()}", DATA_HORÁRIO_DA_RESERVA = "{formatted_datetime}" WHERE NOME_DO_PACIENTE = "{nome.text()}"'
                            cursor.execute(comando)
                            conexao.commit()
                        if self.dep == 'INTER_TRAN_EXTER':
                            cursor = conexao.cursor()
                            comando = f'UPDATE tabela_internações_e_transf_externas SET STATUS_DA_SOLICITAÇÃO = "{status}", LEITO_RESERVADO = "{leito.text()}", DATA_HORÁRIO_RESERVA = "{formatted_datetime}" WHERE NOME_DO_PACIENTE = "{nome.text()}"'
                            cursor.execute(comando)
                            conexao.commit()
                        if self.dep == 'TRA_INTER':
                            cursor = conexao.cursor()
                            comando = f'UPDATE tabela_transferencias_internas SET STATUS_DA_SOLICITAÇÃO = "{status}", LEITO_RESERVADO = "{leito.text()}", DATA_E_HORÁRIO_RESERVA = "{formatted_datetime}" WHERE NOME_DO_PACIENTE = "{nome.text()}"'
                            cursor.execute(comando)
                            conexao.commit()
                        if self.dep == 'ONCO_HEMATO_PED':
                            cursor = conexao.cursor()
                            comando = f'UPDATE tabela_onco_hemato_ped SET STATUS_SOLICITACAO = "{status}", LEITO_RESERVADO = "{leito.text()}", DATA_HORÁRIO_RESERVA = "{formatted_datetime}" WHERE NOME_DO_PACIENTE = "{nome.text()}"'
                            cursor.execute(comando)
                            conexao.commit()
                        cursor.close()
                        conexao.close()
                        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
                        cursor = conexao.cursor()
                        comando = f'UPDATE GRADE SET NOME = "{nome.text()}", STATUS_DO_LEITO = "{status}", DATA_DE_NASCIMENTO = "{data_nas.text()}" WHERE LEITO = "{leito.text()}"'
                        cursor.execute(comando)
                        conexao.commit()
                        cursor.close()
                        conexao.close()

    def pesquisar(self, pesquisa):
        for row in range(self.tabela_demanda.rowCount()):
            item = self.tabela_demanda.item(row, 2)
            item2 = self.tabela_demanda.verticalHeaderItem(row)
            if item is None:
                continue
            if pesquisa.lower() in item.text().lower() or pesquisa.lower() in item2.text().lower():
                self.tabela_demanda.showRow(row)
            else:
                self.tabela_demanda.hideRow(row)

    def atualiza_tela(self, dep, Form):
        self.dep = dep
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        if dep == 'PS':
            cursor = conexao.cursor()
            comando = 'SELECT * FROM tabela_demanda_ps'
            self.retranslateUi_ps(Form)
        if dep == 'ONCO_HEMATO_PED':
            cursor = conexao.cursor()
            comando = 'SELECT * FROM tabela_onco_hemato_ped'
            self.retranslateUi_onco_hemato_ped(Form)
        if dep == 'TRA_INTER':
            cursor = conexao.cursor()
            comando = 'SELECT * FROM tabela_transferencias_internas'
            self.retranslateUi_tran_inte(Form)
        if dep == 'AGENDA_BLOCO':
            cursor = conexao.cursor()
            comando = 'SELECT * FROM tabela_agenda_bloco_demanda'
            self.retranslateUi_agenda_bloco(Form)
        if dep == 'INTER_TRAN_EXTER':
            cursor = conexao.cursor()
            comando = 'SELECT * FROM tabela_internações_e_transf_externas'
            self.retranslateUi_inter_tran_exte(Form)
        if dep == 'HEMODINAMICA':
            cursor = conexao.cursor()
            comando = 'SELECT * FROM tabela_hemodinamica'
            self.retranslateUi_hemodinamica(Form)
        if dep == 'ALTA_CTI':
            cursor = conexao.cursor()
            comando = 'SELECT * FROM alta_cti'
            self.retranslateUi_alta_cti(Form)
        cursor.execute(comando)
        leitura = cursor.fetchall()
        self.tabela_demanda.clearContents()
        self.tabela_demanda.setRowCount(0)
        for linha in leitura:
            row = self.tabela_demanda.rowCount()
            self.tabela_demanda.insertRow(row)
            selecao = QtWidgets.QTableWidgetItem()
            selecao.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            selecao.setCheckState(QtCore.Qt.CheckState.Unchecked)
            for column, valor in enumerate(linha):
                item = QtWidgets.QTableWidgetItem(str(valor))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                if column != 0 and item.text() != 'None':
                    self.tabela_demanda.setItem(row, 0, selecao)
                    self.increase_column_width(0, 16)
                    self.tabela_demanda.setItem(row, column, item)
                if column == 0:
                    self.tabela_demanda.setVerticalHeaderItem(row, item)
                    _translate = QtCore.QCoreApplication.translate
                    self.increase_column_width(0, row)
                    item_pac = self.tabela_demanda.verticalHeaderItem(row)
                    item_pac.setText(_translate('MainWindow', item.text()))
        cursor.close()
        conexao.close()

    def retranslateUi_ps(self, Form):
        _translate = QtCore.QCoreApplication.translate
        item = self.tabela_demanda.horizontalHeaderItem(0)
        item.setText(_translate('Form', ' '))
        item = self.tabela_demanda.horizontalHeaderItem(1)
        item.setText(_translate('Form', 'PRONTUÁRIO'))
        item = self.tabela_demanda.horizontalHeaderItem(2)
        item.setText(_translate('Form', 'NPF'))
        item = self.tabela_demanda.horizontalHeaderItem(3)
        item.setText(_translate('Form', 'DATA DA DEMANDA'))
        item = self.tabela_demanda.horizontalHeaderItem(4)
        item.setText(_translate('Form', 'NOME DO PACIENTE '))
        item = self.tabela_demanda.horizontalHeaderItem(5)
        item.setText(_translate('Form', 'DATA DE NASCIMENTO'))
        item = self.tabela_demanda.horizontalHeaderItem(6)
        item.setText(_translate('Form', 'PONTUAÇÃO SCORE'))
        item = self.tabela_demanda.horizontalHeaderItem(7)
        item.setText(_translate('Form', 'CLÍNICA'))
        item = self.tabela_demanda.horizontalHeaderItem(8)
        item.setText(_translate('Form', 'OBSERVAÇÕES'))
        item = self.tabela_demanda.horizontalHeaderItem(9)
        item.setText(_translate('Form', 'TIPO DE LEITO SOLICITADO'))
        item = self.tabela_demanda.horizontalHeaderItem(10)
        item.setText(_translate('Form', 'PRIORIDADE DA SOLICITAÇÃO'))
        self.ps.setText(_translate('Form', 'PRONTO SOCORRO'))
        self.onco_hemato_ped.setText(_translate('Form', 'ONCO HEMATO PED'))
        self.tran_inte.setText(_translate('Form', 'TRANS INTERNAS'))
        self.agenda_bloco.setText(_translate('Form', 'AGENDA BLOCO'))
        self.inter_tran_exte.setText(_translate('Form', 'INTER TRANS EXTERNAS'))
        self.hemodinamica.setText(_translate('Form', 'HEMODINÂMICA'))
        self.alta_cti.setText(_translate('Form', 'ALTA CTI'))
        self.titulo.setText(_translate('Form', 'REALOCAR PACIENTE DO PRONTO SOCORRO'))
        self.confirmar.setText(_translate('Form', 'REALOCAR PACIENTE'))
        self.label.setText(_translate('Form', 'REALOCAR PACIENTE ?'))
        self.procurar.setText(_translate('Form', 'PROCURAR PACIENTE'))
        for colum in range(1, self.tabela_demanda.columnCount()):
            self.increase_column_width(colum, 250)

    def retranslateUi_alta_cti(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'REALOCAR'))
        item = self.tabela_demanda.horizontalHeaderItem(0)
        item.setText(_translate('Form', ' '))
        item = self.tabela_demanda.horizontalHeaderItem(1)
        item.setText(_translate('Form', 'PRONTUÁRIO'))
        item = self.tabela_demanda.horizontalHeaderItem(2)
        item.setText(_translate('Form', 'NPF'))
        item = self.tabela_demanda.horizontalHeaderItem(3)
        item.setText(_translate('Form', 'DATA DA ALTA'))
        item = self.tabela_demanda.horizontalHeaderItem(4)
        item.setText(_translate('Form', 'HORA DE SOLICITAÇÃO DA ALTA'))
        item = self.tabela_demanda.horizontalHeaderItem(5)
        item.setText(_translate('Form', 'NOME DO PACIENTE'))
        item = self.tabela_demanda.horizontalHeaderItem(6)
        item.setText(_translate('Form', 'DATA DE NASCIMENTO'))
        item = self.tabela_demanda.horizontalHeaderItem(7)
        item.setText(_translate('Form', 'SEXO DO PACIENTE'))
        item = self.tabela_demanda.horizontalHeaderItem(8)
        item.setText(_translate('Form', 'ESPECIALIDADE MÉDICA'))
        item = self.tabela_demanda.horizontalHeaderItem(9)
        item.setText(_translate('Form', 'OBSERVAÇÃO'))
        item = self.tabela_demanda.horizontalHeaderItem(10)
        item.setText(_translate('Form', 'UNIDADE DE INTERNAÇÃO ATUAL'))
        self.titulo.setText(_translate('Form', 'REALOCAR PACIENTE DA ALTA CTI'))
        for colum in range(1, self.tabela_demanda.columnCount()):
            self.increase_column_width(colum, 250)

    def retranslateUi_agenda_bloco(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'REALOCAR'))
        item = self.tabela_demanda.horizontalHeaderItem(0)
        item.setText(_translate('Form', ' '))
        item = self.tabela_demanda.horizontalHeaderItem(1)
        item.setText(_translate('Form', 'PRONTUÁRIO'))
        item = self.tabela_demanda.horizontalHeaderItem(2)
        item.setText(_translate('Form', 'NPF'))
        item = self.tabela_demanda.horizontalHeaderItem(3)
        item.setText(_translate('Form', 'DATA E HORA DO PROCEDIMENTO'))
        item = self.tabela_demanda.horizontalHeaderItem(4)
        item.setText(_translate('Form', 'NOME DO PACIENTE'))
        item = self.tabela_demanda.horizontalHeaderItem(5)
        item.setText(_translate('Form', 'DATA DE NASCIMENTO'))
        item = self.tabela_demanda.horizontalHeaderItem(6)
        item.setText(_translate('Form', 'LEITO DE INTERNAÇÃO ATUAL'))
        item = self.tabela_demanda.horizontalHeaderItem(7)
        item.setText(_translate('Form', 'CLÍNICA'))
        item = self.tabela_demanda.horizontalHeaderItem(8)
        item.setText(_translate('Form', 'PROCEDIMENTO'))
        item = self.tabela_demanda.horizontalHeaderItem(9)
        item.setText(_translate('Form', 'MÉDICO RESPONSÁVEL'))
        item = self.tabela_demanda.horizontalHeaderItem(10)
        item.setText(_translate('Form', 'TIPO DE LEITO SOLICITADO'))
        self.titulo.setText(_translate('Form', 'REALOCAR PACIENTE DA AGENDA BLOCO'))
        for colum in range(1, self.tabela_demanda.columnCount()):
            self.increase_column_width(colum, 250)

    def retranslateUi_hemodinamica(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'REALOCAR'))
        item = self.tabela_demanda.horizontalHeaderItem(0)
        item.setText(_translate('Form', ' '))
        item = self.tabela_demanda.horizontalHeaderItem(1)
        item.setText(_translate('Form', 'PRONTUÁRIO'))
        item = self.tabela_demanda.horizontalHeaderItem(2)
        item.setText(_translate('Form', 'NPF'))
        item = self.tabela_demanda.horizontalHeaderItem(3)
        item.setText(_translate('Form', 'DATA E HORA DO PROCEDIMENTO'))
        item = self.tabela_demanda.horizontalHeaderItem(4)
        item.setText(_translate('Form', 'NOME DO PACIENTE'))
        item = self.tabela_demanda.horizontalHeaderItem(5)
        item.setText(_translate('Form', 'DATA DE NASCIMENTO'))
        item = self.tabela_demanda.horizontalHeaderItem(6)
        item.setText(_translate('Form', 'DATA DA INTERNAÇÃO'))
        item = self.tabela_demanda.horizontalHeaderItem(7)
        item.setText(_translate('Form', 'DATA E HORA DA SOLICITAÇÃO'))
        item = self.tabela_demanda.horizontalHeaderItem(8)
        item.setText(_translate('Form', 'LEITO DE INTERNAÇÃO ATUAL'))
        item = self.tabela_demanda.horizontalHeaderItem(9)
        item.setText(_translate('Form', 'CLÍNICA'))
        item = self.tabela_demanda.horizontalHeaderItem(10)
        item.setText(_translate('Form', 'PROCEDIMENTO'))
        self.titulo.setText(_translate('Form', 'REALOCAR PACIENTE DA HEMODINÂMICA'))
        for colum in range(1, self.tabela_demanda.columnCount()):
            self.increase_column_width(colum, 250)

    def retranslateUi_inter_tran_exte(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'REALOCAR'))
        item = self.tabela_demanda.horizontalHeaderItem(0)
        item.setText(_translate('Form', ' '))
        item = self.tabela_demanda.horizontalHeaderItem(1)
        item.setText(_translate('Form', 'PRONTUÁRIO'))
        item = self.tabela_demanda.horizontalHeaderItem(2)
        item.setText(_translate('Form', 'NPF'))
        item = self.tabela_demanda.horizontalHeaderItem(3)
        item.setText(_translate('Form', 'DATA E HORA DA INTERNAÇÃO'))
        item = self.tabela_demanda.horizontalHeaderItem(4)
        item.setText(_translate('Form', 'NOME DO PACIENTE'))
        item = self.tabela_demanda.horizontalHeaderItem(5)
        item.setText(_translate('Form', 'DATA E HORA DA SOLICITAÇÃO'))
        item = self.tabela_demanda.horizontalHeaderItem(6)
        item.setText(_translate('Form', 'DATA DE NASCIMENTO'))
        item = self.tabela_demanda.horizontalHeaderItem(7)
        item.setText(_translate('Form', 'ORIGEM DO PACIENTE'))
        item = self.tabela_demanda.horizontalHeaderItem(8)
        item.setText(_translate('Form', 'DATA DO PROCEDIMENTO'))
        item = self.tabela_demanda.horizontalHeaderItem(9)
        item.setText(_translate('Form', 'CLÍNICA'))
        item = self.tabela_demanda.horizontalHeaderItem(10)
        item.setText(_translate('Form', 'MOTIVO DA INTERNAÇÃO ANTECIPADA/ PROCEDIMENTO A SER REALIZADO'))
        self.titulo.setText(_translate('Form', 'REALOCAR PACIENTE DAS INTERNAÇÕES E TRANFERÊNCIAS EXTERNAS'))
        for colum in range(1, self.tabela_demanda.columnCount()):
            self.increase_column_width(colum, 250)

    def retranslateUi_tran_inte(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'REALOCAR'))
        item = self.tabela_demanda.horizontalHeaderItem(0)
        item.setText(_translate('Form', ' '))
        item = self.tabela_demanda.horizontalHeaderItem(1)
        item.setText(_translate('Form', 'PRONTUÁRIO'))
        item = self.tabela_demanda.horizontalHeaderItem(2)
        item.setText(_translate('Form', 'NPF'))
        item = self.tabela_demanda.horizontalHeaderItem(3)
        item.setText(_translate('Form', 'DATA E HORA DA SOLICITAÇÃO'))
        item = self.tabela_demanda.horizontalHeaderItem(4)
        item.setText(_translate('Form', 'NOME DO PACIENTE'))
        item = self.tabela_demanda.horizontalHeaderItem(5)
        item.setText(_translate('Form', 'DATA DE NASCIMENTO'))
        item = self.tabela_demanda.horizontalHeaderItem(6)
        item.setText(_translate('Form', 'LEITO ATUAL'))
        item = self.tabela_demanda.horizontalHeaderItem(7)
        item.setText(_translate('Form', 'MOTIVO DA TRANSFERÊNCIA'))
        item = self.tabela_demanda.horizontalHeaderItem(8)
        item.setText(_translate('Form', 'TIPO DE LEITO SOLICITADO'))
        item = self.tabela_demanda.horizontalHeaderItem(9)
        item.setText(_translate('Form', 'STATUS DA SOLICITAÇÃO'))
        item = self.tabela_demanda.horizontalHeaderItem(10)
        item.setText(_translate('Form', 'LEITO RESERVADO'))
        self.titulo.setText(_translate('Form', 'REALOCAR PACIENTE DAS TRANSFERÊNCIAS INTERNAS'))
        for colum in range(1, self.tabela_demanda.columnCount()):
            self.increase_column_width(colum, 250)

    def retranslateUi_onco_hemato_ped(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'REALOCAR'))
        item = self.tabela_demanda.horizontalHeaderItem(0)
        item.setText(_translate('Form', ' '))
        item = self.tabela_demanda.horizontalHeaderItem(1)
        item.setText(_translate('Form', 'PRONTUÁRIO'))
        item = self.tabela_demanda.horizontalHeaderItem(2)
        item.setText(_translate('Form', 'NPF'))
        item = self.tabela_demanda.horizontalHeaderItem(3)
        item.setText(_translate('Form', 'DATA PREVISTA DA INTERNAÇÃO'))
        item = self.tabela_demanda.horizontalHeaderItem(4)
        item.setText(_translate('Form', 'NOME DO PACIENTE'))
        item = self.tabela_demanda.horizontalHeaderItem(5)
        item.setText(_translate('Form', 'DATA DE NASCIMENTO'))
        item = self.tabela_demanda.horizontalHeaderItem(6)
        item.setText(_translate('Form', 'IDADE'))
        item = self.tabela_demanda.horizontalHeaderItem(7)
        item.setText(_translate('Form', 'PESO E ALTURA DA CRIANÇA'))
        item = self.tabela_demanda.horizontalHeaderItem(8)
        item.setText(_translate('Form', 'DATA E HORA DA SOLICITAÇÃO'))
        item = self.tabela_demanda.horizontalHeaderItem(9)
        item.setText(_translate('Form', 'PACIENTE JA INTERNADO NO PRONTO SOCORRO?'))
        item = self.tabela_demanda.horizontalHeaderItem(10)
        item.setText(_translate('Form', 'CLÍNICA'))
        self.titulo.setText(_translate('Form', 'REALOCAR PACIENTE DA ONCO-HEMATO PED'))
        for colum in range(1, self.tabela_demanda.columnCount()):
            self.increase_column_width(colum, 250)

    def increase_column_width(self, column, width):
        self.tabela_demanda.setColumnWidth(column, width)

    def load(self, Form):
        if self.settings.contains('tema'):
            font_name = self.settings.value('font', defaultValue='')
            backcolocor = self.settings.value('tema', defaultValue='')
            color = self.settings.value('color', defaultValue='')
            tamanho = int(self.settings.value('tamanho', defaultValue=10))
            self.frame.setStyleSheet(f'background-color: {backcolocor};color: {color};font: {font_name} {tamanho}px;border: 2px solid #2E3D48;border-radius: 10px;')
            for label in self.frame.findChildren(QtWidgets.QLabel):
                label.setStyleSheet(f'color: {color}; font:  {tamanho}px {font_name}; border:none')
            self.titulo.setStyleSheet(f'color: {color}; font:  15 px {font_name}; border:none')