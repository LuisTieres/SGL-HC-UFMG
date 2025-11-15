import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QDateEdit, QTableWidget, QTableWidgetItem,
    QScrollArea, QFrame, QFileDialog
)
from PyQt6.QtCore import Qt, QDate
import pymysql
import pandas as pd
from datetime import datetime

# Configurações do banco
DB_CONFIG = {
    'host': '10.36.0.32',
    'user': 'sglHC2024',
    'password': 'S4g1L81',
    'database': 'sgl'
}


class SensoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Senso Diário")
        self.resize(1200, 600)

        # Frame principal
        self.frame_principal = QFrame(self)
        self.frame_principal.setFrameShape(QFrame.Shape.StyledPanel)

        layout_principal = QVBoxLayout(self)
        layout_frame = QVBoxLayout(self.frame_principal)

        # Seletores de datas
        date_layout = QHBoxLayout()

        self.date_mesano = QDateEdit()
        self.date_mesano.setDisplayFormat("MM/yyyy")
        self.date_mesano.setCalendarPopup(True)
        self.date_mesano.setDate(QDate.currentDate())

        self.date_dia = QDateEdit()
        self.date_dia.setDisplayFormat("dd/MM/yyyy")
        self.date_dia.setCalendarPopup(True)
        self.date_dia.setDate(QDate.currentDate())

        btn_filtrar = QPushButton("Filtrar")
        btn_filtrar.clicked.connect(self.filtrar_dados)

        btn_exportar = QPushButton("Exportar Excel")
        btn_exportar.clicked.connect(self.exportar_excel)

        date_layout.addWidget(self.date_mesano)
        date_layout.addWidget(self.date_dia)
        date_layout.addWidget(btn_filtrar)
        date_layout.addWidget(btn_exportar)

        layout_frame.addLayout(date_layout)

        # Área de scroll para tabelas
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.frame_tabelas = QFrame()
        self.hbox_tabelas = QHBoxLayout(self.frame_tabelas)
        self.scroll.setWidget(self.frame_tabelas)

        layout_frame.addWidget(self.scroll)

        layout_principal.addWidget(self.frame_principal)

        # Guardar referência às tabelas
        self.tabelas = {}

    def filtrar_dados(self):
        # Limpar tabelas antigas
        for i in reversed(range(self.hbox_tabelas.count())):
            widget = self.hbox_tabelas.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.tabelas.clear()

        mesano = self.date_mesano.date()
        dia_selecionado = self.date_dia.date()

        mes = mesano.month()
        ano = mesano.year()

        if not mes or not ano:
            return  # sem mês/ano não mostra nada

        conexao = pymysql.connect(**DB_CONFIG)
        cursor = conexao.cursor()

        # Buscar dados por mês/ano
        cursor.execute("""
            SELECT data, ala, ocupacao, bloqueios, cnes, ocupacao_percentual, leitos_disponiveis
            FROM senso_diario
            WHERE MONTH(data) = %s AND YEAR(data) = %s
            ORDER BY data
        """, (mes, ano))
        resultados = cursor.fetchall()
        conexao.close()

        # Organizar por dia
        dados_por_dia = {}
        for row in resultados:
            data = row[0]
            if data not in dados_por_dia:
                dados_por_dia[data] = []
            dados_por_dia[data].append(row)

        # Criar uma tabela para cada dia
        for data, linhas in dados_por_dia.items():
            tabela = QTableWidget()
            tabela.setColumnCount(7)
            tabela.setHorizontalHeaderLabels([
                "Data", "Ala", "Ocupação", "Bloqueios", "CNES", "% Ocupação", "Leitos Disp."
            ])
            tabela.setRowCount(len(linhas))

            for r, row in enumerate(linhas):
                for c, value in enumerate(row):
                    tabela.setItem(r, c, QTableWidgetItem(str(value)))

            self.hbox_tabelas.addWidget(tabela)
            self.tabelas[data] = tabela

        # Scroll até o dia selecionado (se existir)
        dia_dt = dia_selecionado.toPyDate()
        if dia_dt in self.tabelas:
            tabela_widget = self.tabelas[dia_dt]
            self.scroll.ensureWidgetVisible(tabela_widget)

    def exportar_excel(self):
        if not self.tabelas:
            return

        # Caminho padrão sugerido
        default_dir = "senso_exportado.xlsx"

        # Abre o diálogo
        filename, _ = QFileDialog.getSaveFileName(
            self.frame_principal,
            "Salvar Relatório",
            default_dir,
            "Arquivos Excel (*.xlsx)"
        )

        if not filename:  # Usuário cancelou
            return

        with pd.ExcelWriter(filename) as writer:
            for data, tabela in self.tabelas.items():
                df = self._tabela_para_df(tabela)
                aba = data.strftime("%d-%m-%Y")
                df.to_excel(writer, sheet_name=aba, index=False)

        print(f"Arquivo Excel salvo em: {filename}")

    def _tabela_para_df(self, tabela: QTableWidget):
        colunas = [tabela.horizontalHeaderItem(c).text() for c in range(tabela.columnCount())]
        dados = []
        for r in range(tabela.rowCount()):
            linha = []
            for c in range(tabela.columnCount()):
                item = tabela.item(r, c)
                linha.append(item.text() if item else "")
            dados.append(linha)
        return pd.DataFrame(dados, columns=colunas)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SensoApp()
    win.show()
    sys.exit(app.exec())
