from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QRadioButton, QDialogButtonBox, QLineEdit,
    QTimeEdit, QDateEdit, QDateTimeEdit, QComboBox, QStackedWidget
)
from PyQt6.QtCore import QDate, QDateTime, pyqtSignal

class CampoDialogWidget(QWidget):
    accepted = pyqtSignal(str, str)
    rejected = pyqtSignal()

    def __init__(self, parent_frame, widget_type=None, dados=None):
        if dados is None:
            dados = {}

        super().__init__()
        self.setWindowTitle("Selecionar Tipo de Campo")
        self.setMinimumWidth(300)
        layout = QVBoxLayout(self)

        # Radio buttons
        self.radio_campo = QRadioButton("CAMPO ABERTO")
        self.radio_tempo = QRadioButton("TEMPORIZADOR")
        self.radio_data = QRadioButton("DATA")
        self.radio_data_tempo = QRadioButton("DATA COM TEMPO")
        self.radio_lista = QRadioButton("LISTA SUSPENSA")
        layout.addWidget(self.radio_campo)
        layout.addWidget(self.radio_tempo)
        layout.addWidget(self.radio_data)
        layout.addWidget(self.radio_data_tempo)
        layout.addWidget(self.radio_lista)

        # Stack
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.line_edit = QLineEdit()
        self.stack.addWidget(self.line_edit)

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.stack.addWidget(self.time_edit)

        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.setDate(QDate.currentDate())
        self.stack.addWidget(self.date_edit)

        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.datetime_edit.setDateTime(QDateTime.currentDateTime())
        self.stack.addWidget(self.datetime_edit)

        self.combo = QComboBox()
        if widget_type == "QComboBox":
            self.combo.addItems(dados.get("itens", ["Item 1", "Item 2"]))
        self.stack.addWidget(self.combo)

        # Conectar os rádios
        self.radio_campo.toggled.connect(lambda: self.stack.setCurrentIndex(0))
        self.radio_tempo.toggled.connect(lambda: self.stack.setCurrentIndex(1))
        self.radio_data.toggled.connect(lambda: self.stack.setCurrentIndex(2))
        self.radio_data_tempo.toggled.connect(lambda: self.stack.setCurrentIndex(3))
        self.radio_lista.toggled.connect(lambda: self.stack.setCurrentIndex(4))

        # Botões
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.on_accept)
        self.buttons.rejected.connect(self.on_reject)
        layout.addWidget(self.buttons)

        # Seleciona inicial
        self.set_widget_type(widget_type)

    def set_widget_type(self, tipo):
        tipo_map = {
            "QLineEdit": (self.radio_campo, 0),
            "QTimeEdit": (self.radio_tempo, 1),
            "QDateEdit": (self.radio_data, 2),
            "QDateTimeEdit": (self.radio_data_tempo, 3),
            "QComboBox": (self.radio_lista, 4)
        }
        if tipo in tipo_map:
            radio, idx = tipo_map[tipo]
            radio.setChecked(True)
            self.stack.setCurrentIndex(idx)

    def on_accept(self):
        tipo, valor = self.get_value()
        self.accepted.emit(tipo, valor)

    def on_reject(self):
        self.rejected.emit()

    def get_value(self):
        if self.radio_campo.isChecked():
            return "CAMPO ABERTO", self.line_edit.text()
        elif self.radio_tempo.isChecked():
            return "TEMPORIZADOR", self.time_edit.time().toString("HH:mm:ss")
        elif self.radio_data.isChecked():
            return "DATA", self.date_edit.date().toString("dd/MM/yyyy")
        elif self.radio_data_tempo.isChecked():
            return "DATA COM TEMPO", self.datetime_edit.dateTime().toString("dd/MM/yyyy HH:mm")
        elif self.radio_lista.isChecked():
            return "LISTA SUSPENSA", self.combo.currentText()
        return "", ""
