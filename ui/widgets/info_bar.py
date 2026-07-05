from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

class InfoBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.moves_label = QLabel("Coups: 0")
        self.moves_label.setObjectName("infoLabel")
        
        self.time_label = QLabel("00:00")
        self.time_label.setObjectName("infoLabel")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        layout.addWidget(self.moves_label)
        layout.addWidget(self.time_label)
        
    def update_moves(self, moves: int):
        self.moves_label.setText(f"Coups: {moves}")
        
    def update_time(self, seconds: int):
        mins, secs = divmod(seconds, 60)
        self.time_label.setText(f"{mins:02d}:{secs:02d}")
