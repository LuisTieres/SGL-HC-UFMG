from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QCheckBox, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

class CustomTableWidget(QTableWidget):
    def __init__(self, dept, rows, cols):
        super().__init__(rows, cols)
        self.dept = dept
        self.setup_table()
        self.cellClicked.connect(self.on_cell_click)

    def setup_table(self):
        for row in range(self.rowCount()):
            self.setCellWidget(row, 0, self.create_checkbox(row))
            for col in range(1, self.columnCount()):
                self.setItem(row, col, QTableWidgetItem(f"Item {row}, {col}"))

    def create_checkbox(self, row):
        checkbox = QCheckBox()
        checkbox.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px; margin-left: 10px; }")  # Ajuste do tamanho
        checkbox.setTristate(False)  # Apenas marcado ou desmarcado
        return checkbox

    def on_cell_click(self, row, column):
        if column == 0:  # Apenas na coluna do checkbox
            widget = self.cellWidget(row, column)
            if isinstance(widget, QCheckBox):
                widget.setChecked(not widget.isChecked())

    def edit(self, index, trigger, event):
        if self.dept == 'PS':
            if index.column() in [10, 11, 12]:
                return False
        return super().edit(index, trigger, event)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.table = CustomTableWidget("PS", 5, 3)  # Tabela com 5 linhas e 3 colunas
        layout.addWidget(self.table)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
