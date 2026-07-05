from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal


class BottomBarWidget(QFrame):
    """Footer bar with HOW TO PLAY button, motto text, and sparkle decoration."""
    help_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("bottomBar")
        self.setFixedHeight(54)

        row = QHBoxLayout(self)
        row.setContentsMargins(24, 0, 24, 0)
        row.setSpacing(16)

        # Left: HOW TO PLAY
        self.btn_help = QPushButton("ⓘ  HOW TO PLAY")
        self.btn_help.setObjectName("btnHowTo")
        self.btn_help.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_help.setFixedHeight(36)
        self.btn_help.clicked.connect(self.help_clicked.emit)

        # Center: motto
        motto = QLabel("✦  Every move brings you closer to the complete picture  ✦")
        motto.setObjectName("mottoText")
        motto.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Right: glowing star decoration (matches reference image)
        star = QLabel("✦")
        star.setObjectName("starDecoration")
        star.setFixedWidth(36)
        star.setAlignment(Qt.AlignmentFlag.AlignCenter)

        row.addWidget(self.btn_help)
        row.addWidget(motto, 1)
        row.addWidget(star)
