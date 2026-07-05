from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox
from PySide6.QtCore import Signal

class ControlPanel(QWidget):
    new_game_requested = Signal(int, str) # size, style
    shuffle_requested = Signal()
    load_image_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.size_combo = QComboBox()
        self.size_combo.addItems(["3x3", "4x4", "5x5"])
        
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Gradient", "Sunset", "Forest"])
        
        self.btn_new = QPushButton("Nouvelle")
        self.btn_shuffle = QPushButton("Mélanger")
        self.btn_load = QPushButton("Image...")
        
        layout.addWidget(self.size_combo)
        layout.addWidget(self.style_combo)
        layout.addWidget(self.btn_new)
        layout.addWidget(self.btn_shuffle)
        layout.addWidget(self.btn_load)
        
        self.btn_new.clicked.connect(self._on_new_game)
        self.btn_shuffle.clicked.connect(self.shuffle_requested.emit)
        self.btn_load.clicked.connect(self.load_image_requested.emit)

    def _on_new_game(self):
        size_str = self.size_combo.currentText()
        size = int(size_str[0])
        style = self.style_combo.currentText()
        self.new_game_requested.emit(size, style)
