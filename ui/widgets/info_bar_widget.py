from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class InfoBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(35)
        
        self.moves_val = QLabel("0")
        self.time_val = QLabel("00:00")
        self.best_val = QLabel("--")
        
        main_layout.addWidget(self._create_card("🕹️ MOVES", self.moves_val))
        main_layout.addWidget(self._create_card("⏱️ TIMER", self.time_val))
        main_layout.addWidget(self._create_card("🏆 BEST SCORE", self.best_val))

    def _create_card(self, title_text, val_label):
        card = QFrame()
        card.setObjectName("statCard")
        card.setFixedSize(180, 100)
        
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(217, 70, 239, 40))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(6)
        
        title = QLabel(title_text)
        title.setObjectName("statTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        val_label.setObjectName("statValue")
        val_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(val_label)
        return card
        
    def update_moves(self, moves: int):
        self.moves_val.setText(str(moves))
        
    def update_time(self, seconds: int):
        mins, secs = divmod(seconds, 60)
        self.time_val.setText(f"{mins:02d}:{secs:02d}")
