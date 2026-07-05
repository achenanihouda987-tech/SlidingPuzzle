from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class HelpDialog(QDialog):
    @staticmethod
    def show(parent):
        dialog = HelpDialog(parent)
        dialog.exec()

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        card = QFrame()
        card.setObjectName("glassPanel")
        card.setStyleSheet("""
            QFrame#glassPanel {
                background-color: rgba(20, 20, 42, 0.96);
                border: 2px solid #A855F7;
                border-radius: 20px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(50)
        shadow.setColor(QColor(168, 85, 247, 150))
        shadow.setOffset(0, 0)
        card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 40, 36, 40)
        card_layout.setSpacing(18)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("HOW TO PLAY")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: 900;
            color: #A855F7;
            letter-spacing: 2px;
            background: transparent;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        rules_text = (
            "Slide tiles into the empty space to reconstruct the image.\n\n"
            "Only adjacent tiles can move.\n\n"
            "Complete the puzzle in the least moves and time."
        )
        body = QLabel(rules_text)
        body.setStyleSheet("""
            font-size: 15px;
            line-height: 1.6;
            color: #E2E8F0;
            background: transparent;
        """)
        body.setWordWrap(True)
        body.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_close = QPushButton("GOT IT")
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.accept)
        btn_close.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9333EA, stop:1 #C026D3);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 30px;
                font-weight: 800;
                font-size: 14px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #A855F7, stop:1 #DB2777);
            }
        """)
        
        card_layout.addWidget(title)
        card_layout.addWidget(body)
        card_layout.addSpacing(10)
        card_layout.addWidget(btn_close, 0, Qt.AlignmentFlag.AlignHCenter)
        
        layout.addWidget(card)
