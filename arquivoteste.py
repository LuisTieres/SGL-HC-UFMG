from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                             QPushButton, QLabel, QSpacerItem, QSizePolicy,
                             QFrame)
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QColor, QPainter, QLinearGradient, QBrush


class AnimatedTabButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"color")
        self._animation.setDuration(200)
        self._color = QColor("#f8f8f8")
        self.setCheckable(True)

        # Configuração inicial do estilo
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 5px;
                font-weight: bold;
                color: #333333;
                background: transparent;
            }
        """)

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color
        self.update()

    color = property(get_color, set_color)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Configurações de texto
        font = self.font()
        font.setBold(True)
        painter.setFont(font)

        # Cores baseadas no estado
        if self.isChecked():
            bg_color = QColor("#ffffff")
            border_color = QColor("#3a6ab1")
            text_color = QColor("#2b579a")
        elif self.underMouse():
            bg_color = QColor("#e5f1fb")
            border_color = QColor("#aaaaaa")
            text_color = QColor("#333333")
        else:
            bg_color = QColor("#f8f8f8")
            border_color = QColor("#aaaaaa")
            text_color = QColor("#333333")

        # Desenha o fundo
        painter.setBrush(QBrush(bg_color))
        painter.setPen(border_color)
        rect = self.rect().adjusted(1, 1, -1, 0)
        painter.drawRoundedRect(rect, 4, 4, Qt.SizeMode.RelativeSize)

        # Desenha o texto (agora sempre visível)
        painter.setPen(text_color)
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(self.text())
        text_rect = self.rect()
        text_rect.setX((self.width() - text_width) / 2)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self.text())

    def enterEvent(self, event):
        self._animation.stop()
        self._animation.setEndValue(QColor("#e5f1fb"))
        self._animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self._animation.start()
        super().enterEvent(event)
        self.update()

    def leaveEvent(self, event):
        if not self.isChecked():
            self._animation.stop()
            self._animation.setEndValue(QColor("#f8f8f8"))
            self._animation.setEasingCurve(QEasingCurve.Type.OutQuad)
            self._animation.start()
        super().leaveEvent(event)
        self.update()


class CustomTitleBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.mouse_pos = QPoint(0, 0)
        self.is_dragging = False
        self.drag_start_pos = QPoint(0, 0)
        self.drag_timer = QTimer()
        #self.drag_timer.timeout.connect(self.check_drag_to_maximize)

        # Configurações do frame da barra de título
        self.setFixedHeight(36)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("""
            CustomTitleBar {
                background-color: #2b579a;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                border: 1px solid #1a3d6d;
            }
        """)

    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Container das abas (esquerda)
        self.tab_container = QFrame()
        self.tab_container.setFixedHeight(34)
        self.tab_container.setStyleSheet("background: transparent;")
        self.tab_layout = QHBoxLayout(self.tab_container)
        self.tab_layout.setContentsMargins(6, 0, 0, 0)
        self.tab_layout.setSpacing(0)

        # Primeira aba (personalizada)
        self.tab1 = AnimatedTabButton("Arquivo")
        self.tab1.setFixedSize(100, 32)
        self.tab1.setChecked(True)
        self.tab_layout.addWidget(self.tab1)

        # Segunda aba (personalizada)
        self.tab2 = AnimatedTabButton("Editar")
        self.tab2.setFixedSize(100, 32)
        self.tab_layout.addWidget(self.tab2)

        # Conectar sinais
        self.tab1.clicked.connect(lambda: self.set_active_tab(self.tab1))
        self.tab2.clicked.connect(lambda: self.set_active_tab(self.tab2))

        self.layout.addWidget(self.tab_container)

        # Título da janela (centralizado)
        self.title = QLabel("Meu Aplicativo")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 12px;
                background: transparent;
                padding: 0 15px;
            }
        """)
        self.layout.addWidget(self.title)

        # Espaçador
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout.addItem(spacer)

        # Botão adicional com ícone (direita)
        self.custom_button = QPushButton()
        self.custom_button.setFixedSize(34, 34)
        self.custom_button.setIcon(QIcon.fromTheme("document-open"))
        #self.custom_button.setIconSize(QSize(16, 16))
        self.custom_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3a6ab1;
                border-radius: 3px;
            }
        """)
        self.layout.addWidget(self.custom_button)

        # Botões da barra de título (direita)
        self.button_container = QFrame()
        self.button_container.setStyleSheet("background: transparent;")
        self.button_layout = QHBoxLayout(self.button_container)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(0)

        # Botão de minimizar
        self.minimize_button = QPushButton("−")
        self.minimize_button.setFixedSize(46, 34)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3a6ab1;
            }
        """)
        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.button_layout.addWidget(self.minimize_button)

        # Botão de maximizar/restaurar
        self.maximize_button = QPushButton("□")
        self.maximize_button.setFixedSize(46, 34)
        self.maximize_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3a6ab1;
            }
        """)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.button_layout.addWidget(self.maximize_button)

        # Botão de fechar
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(46, 34)
        self.close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 18px;
                border: none;
                border-top-right-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e81123;
            }
        """)
        self.close_button.clicked.connect(self.parent.close)
        self.button_layout.addWidget(self.close_button)

        self.layout.addWidget(self.button_container)

    def set_active_tab(self, active_tab):
        self.tab1.setChecked(active_tab == self.tab1)
        self.tab2.setChecked(active_tab == self.tab2)
        # Atualiza o estilo das abas
        self.tab1.update()
        self.tab2.update()

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.maximize_button.setText("□")
        else:
            self.parent.showMaximized()
            self.maximize_button.setText("❐")

    # ... (restante dos métodos de manipulação da janela permanecem iguais)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicativo com Barra de Título Personalizada")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(800, 600)

        # Configurar barra de título personalizada
        self.title_bar = CustomTitleBar(self)
        self.setMenuWidget(self.title_bar)

        # Área central da janela
        central_widget = QWidget()
        central_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-top: 1px solid #d0d0d0;
            }
        """)
        self.setCentralWidget(central_widget)

        # Estilo da janela principal
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
                border: 1px solid #1a3d6d;
                border-radius: 6px;
            }
        """)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()