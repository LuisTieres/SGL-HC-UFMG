from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableView, QWidget
)
from PyQt6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex, QTimer
)
from PyQt6.QtGui import QColor, QPalette
import sys

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self._data[0])

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

class ProxyModel(QAbstractTableModel):
    def __init__(self, source_model):
        super().__init__()
        self.source_model = source_model
        self.columns = [0, 1, 2]

    def set_columns(self, columns):
        self.columns = columns
        self.layoutChanged.emit()

    def rowCount(self, index=QModelIndex()):
        return self.source_model.rowCount()

    def columnCount(self, index=QModelIndex()):
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            source_index = self.source_model.index(index.row(), self.columns[index.column()])
            return self.source_model.data(source_index, role)
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return f"Col {self.columns[section]}"
            else:
                return str(section)
        return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Horizontal Scroll with Floating Table")
        self.resize(1000, 600)

        data = [[f"Item {r}-{c}" for c in range(100)] for r in range(50)]

        self.table = QTableView()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

        self.preview = QTableView(self)
        self.preview.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.SubWindow)
        self.preview.setStyleSheet("background-color:black; color: white;")
        self.preview.verticalHeader().setVisible(False)
        self.preview.horizontalHeader().setVisible(False)
        self.preview.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.preview.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.proxy = ProxyModel(self.model)
        self.preview.setModel(self.proxy)

        self.preview.hide()

        self.table.horizontalScrollBar().valueChanged.connect(self.on_horizontal_scroll)

        self.table.verticalScrollBar().valueChanged.connect(
            self.preview.verticalScrollBar().setValue
        )

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.preview.hide)

    def on_horizontal_scroll(self, value):
        if value == 0:
            self.preview.hide()
            palette = self.table.palette()
            palette.setColor(QPalette.ColorRole.Base, QColor("#d0f0c0"))  # light green
            self.table.setPalette(palette)
        else:
            self.table.setPalette(self.style().standardPalette())

            # Update visible columns
            index_left = self.table.indexAt(self.table.viewport().rect().topLeft())
            start_col = index_left.column() if index_left.isValid() else 0

            visible_columns = list(range(start_col, min(start_col + 3, self.model.columnCount())))
            self.proxy.set_columns(visible_columns)

            # Dynamically set the preview table height to match main table
            main_geom = self.table.geometry()
            viewport_height = self.table.viewport().height()

            preview_width = 400
            preview_height = viewport_height

            self.preview.setGeometry(
                main_geom.left() + 20,
                main_geom.top() + self.table.horizontalHeader().height(),
                preview_width,
                preview_height
            )

            self.preview.show()


# Run the app
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
