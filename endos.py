    def abrir_tabela_Endoscopia(self, MainWindow):
        if self.dept != 'Telespectador' and self.dept != 'Bloco Cirúrgico' and (self.dept != 'Pronto Socorro') and (
                self.dept != 'Hemodinâmica' and self.dept != 'Endoscopia'):
            self.btn_confirm_alta.hide()

        if self.dept == 'NIR':
            self.alterar_cor_tela()
        self.tabelademan.setColumnCount(18)
        self.tabelademan.setRowCount(0)
        self.variavel = 7
        self.timer_ps.stop()
        self.temporizador(MainWindow)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont('Arial', 15, weight=QtGui.QFont.Weight.Bold)
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tabelademan.setHorizontalHeaderItem(17, item)
        self.retranslateUi_endoscopia(MainWindow)
        self.atualiza_tabela_demandas('tabela_endoscopia')
        self.tabelademan.setCurrentCell(self.tabelademan.rowCount() - 1, 0)
        if not self.frame_do_grafico.isHidden():
            self.canvas.show()
            self.plot_pie_chart()
            self.timer.stop()
    def filtros(self, index):
        self.btn_filtros.setStyleSheet('QPushButton {    border-top-right-radius: 0px;    border-bottom-right-radius: 0px;    border-top-left-radius: 10px;    border-bottom-left-radius: 10px;    background-color: #FFFFFF;    color: #2E3D48;    border: 2px solid black;}QPushButton:pressed {    background-color: #2E3D48;    color: #FFFFFF;}')
        if index == 1:
            self.day = 'HOJE'
            self.btn_filtros.setText('Hoje')
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 120, 23))
            self.btnfechar.show()
        elif index == 2:
            self.day = 'SEMANA'
            self.btn_filtros.setText('Ultimos 7 dias')
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 120, 23))
            self.btnfechar.show()
        elif index == 3:
            self.day = 'MES'
            self.btn_filtros.setText('Ultimos 30 dias')
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 120, 23))
            self.btnfechar.show()
        elif index == 4:
            self.day = 'ANO'
            current_datetime = QDateTime.currentDateTime()
            formatted_date = current_datetime.toString('yyyy')
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 120, 23))
            self.btn_filtros.setText(f'{formatted_date}')
            self.btnfechar.show()
        elif index == 5:
            self.day = '2ANO'
            current_datetime = QDateTime.currentDateTime()
            formatted_date = current_datetime.addYears(-1).toString('yyyy')
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 120, 23))
            self.btn_filtros.setText(f'{formatted_date}')
            self.btnfechar.show()
        elif index == 6:
            self.day = 'PERSONALIZADO'
            self.data_i = self.data_inicio.date()
            self.data_f = self.data_final.date()
            self.btn_filtros.setText('Período personalizado')
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 120, 23))
            self.btnfechar.show()
        elif index == 0:
            self.day = 'ONTEM'
            self.btn_filtros.setGeometry(QtCore.QRect(420, 65, 150, 23))
            self.btn_filtros.setText('▼ Selecione uma Data ')
            self.btn_filtros.setStyleSheet('QPushButton {\n                border: 2px solid #2E3D48;\n                border-radius: 10px;\n                background-color: #FFFFFF;\n                color: #2E3D48;\n            }\n            QPushButton:pressed {\n                background-color: #2E3D48;\n                color: #FFFFFF;\n            }')
            self.btnfechar.hide()
            if not self.frame_personalisa.isHidden():
                self.frame_personalisa.hide()
        if self.day != 'ONTEM':
            self.filtrar_data()
            return

        if self.variavel == 0:
            self.atualiza_tabela_demandas('tabela_demanda_ps')
        if self.variavel == 1:
            self.atualiza_tabela_demandas('alta_cti')
        if self.variavel == 2:
            self.atualiza_tabela_demandas('tabela_agenda_bloco_demanda')
        if self.variavel == 3:
            self.atualiza_tabela_demandas('tabela_hemodinamica')
        if self.variavel == 4:
            self.atualiza_tabela_demandas('tabela_internações_e_transf_externas')
        if self.variavel == 5:
            self.atualiza_tabela_demandas('tabela_transferencias_internas')
        if self.variavel == 6:
            self.atualiza_tabela_demandas('tabela_onco_hemato_ped')
        if self.variavel == 7:
            self.atualiza_tabela_demandas('tabela_endoscopia')
        self.timer_ps.start()
    def temporizador(self, MainWindow):
        self.timer_ps = QtCore.QTimer()
        self.timer_ps.setInterval(60000)
        self.tabelademan.cellChanged.connect(self.checkboxStateChanged)
        if self.variavel == 0:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_demanda_ps'))
        if self.variavel == 1:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('alta_cti'))
        if self.variavel == 2:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_agenda_bloco_demanda'))
        if self.variavel == 3:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_hemodinamica'))
        if self.variavel == 4:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_internações_e_transf_externas'))
        if self.variavel == 5:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_transferencias_internas'))
        if self.variavel == 6:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_onco_hemato_ped'))
        if self.variavel == 7:
            self.timer_ps.timeout.connect(lambda: self.atualiza_tabela_demandas('tabela_endoscopia'))

        self.timer_ps.start()
        self.increase_column_width(0, 16)
    def retranslateUi_endoscopia(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        item = self.tabelademan.horizontalHeaderItem(0)
        item.setText(_translate('MainWindow', ' '))
        self.increase_column_width(0, 5)
        item = self.tabelademan.horizontalHeaderItem(1)
        item.setText(_translate('MainWindow', 'PRONTUÁRIO'))
        item = self.tabelademan.horizontalHeaderItem(2)
        item.setText(_translate('MainWindow', 'NPF'))
        item = self.tabelademan.horizontalHeaderItem(3)
        item.setText(_translate('MainWindow', 'DATA E HORA DO PROCEDIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(4)
        item.setText(_translate('MainWindow', 'HORÁRIO DE CHEGADA DO PACIENTE NA URA'))
        item = self.tabelademan.horizontalHeaderItem(5)
        item.setText(_translate('MainWindow', 'NOME DO PACIENTE'))
        item = self.tabelademan.horizontalHeaderItem(6)
        item.setText(_translate('MainWindow', 'DATA DE NASCIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(7)
        item.setText(_translate('MainWindow', 'ORIGEM DO PACIENTE'))
        item = self.tabelademan.horizontalHeaderItem(8)
        item.setText(_translate('MainWindow', 'CLÍNICA'))
        item = self.tabelademan.horizontalHeaderItem(9)
        item.setText(_translate('MainWindow', 'PROCEDIMENTO'))
        item = self.tabelademan.horizontalHeaderItem(10)
        item.setText(_translate('MainWindow', 'MÉDICO RESPONSÁVEL'))
        item = self.tabelademan.horizontalHeaderItem(11)
        item.setText(_translate('MainWindow', 'TIPO DE LEITO SOLICITADO'))
        item = self.tabelademan.horizontalHeaderItem(12)
        item.setText(_translate('MainWindow', 'PRIORIDADE'))
        item = self.tabelademan.horizontalHeaderItem(13)
        item.setText(_translate('MainWindow', 'STATUS DA SOLICITAÇÃO'))
        item = self.tabelademan.horizontalHeaderItem(14)
        item.setText(_translate('MainWindow', 'CIRURGIA LIBERADA PARA ENTRAR?'))
        item = self.tabelademan.horizontalHeaderItem(15)
        item.setText(_translate('MainWindow', 'LEITO RESERVADO'))
        item = self.tabelademan.horizontalHeaderItem(16)
        item.setText(_translate('MainWindow', 'DATA E HORA DA RESERVA'))
        item = self.tabelademan.horizontalHeaderItem(17)
        item.setText(_translate('MainWindow', 'MOTIVO DO CANCELAMENTO'))
        self.labeltitulo.setText(_translate('MainWindow', 'SOLICITAÇÃO DE LEITOS ENDOSCOPIA'))
        for colum in range(1, self.tabelademan.columnCount()):
            item_pac = self.tabelademan.horizontalHeaderItem(colum).text()
            text_width = self.fontMetrics().boundingRect(item_pac).width()
            self.increase_column_width(colum, text_width + 100)