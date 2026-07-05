from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


def _neon_shadow(r=236, g=72, b=153, blur=50):
    fx = QGraphicsDropShadowEffect()
    fx.setBlurRadius(blur)
    fx.setColor(QColor(r, g, b, 150))
    fx.setOffset(0, 0)
    return fx


class ScoreDialog(QDialog):
    """Detailed score modal shown when VIEW SCORE is clicked."""

    @staticmethod
    def show(parent, moves: int, seconds: int, difficulty: int, score: int):
        dlg = ScoreDialog(parent, moves, seconds, difficulty, score)
        dlg.exec()

    def __init__(self, parent, moves: int, seconds: int,
                 difficulty: int, score: int):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumWidth(400)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)

        card = QFrame()
        card.setObjectName("glassPanel")
        card.setStyleSheet("""
            QFrame#glassPanel {
                background-color: rgba(20,20,42,0.97);
                border: 2px solid #EC4899;
                border-radius: 22px;
            }
        """)
        card.setGraphicsEffect(_neon_shadow())

        cl = QVBoxLayout(card)
        cl.setContentsMargins(40, 44, 40, 44)
        cl.setSpacing(18)
        cl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("PERFORMANCE SCORE")
        title.setStyleSheet(
            "font-size: 22px; font-weight: 900; color: #EC4899;"
            " letter-spacing: 2px; background: transparent;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Rating
        if moves < 30:
            rating, stars, color = "Excellent", "⭐", "#34D399"
        elif moves < 60:
            rating, stars, color = "Good", "⭐⭐", "#60A5FA"
        else:
            rating, stars, color = "Average", "⭐⭐⭐", "#FBBF24"

        m, s = divmod(seconds, 60)
        diff_label = f"{difficulty} × {difficulty}"

        for label, value, val_color in [
            ("Difficulty",   diff_label,      "#E2E8F0"),
            ("Total Moves",  str(moves),      "#E2E8F0"),
            ("Total Time",   f"{m:02d}:{s:02d}", "#E2E8F0"),
            ("Score",        str(score),      "#FBBF24"),
            ("Rating",       f"{rating}  {stars}", color),
        ]:
            row = QHBoxLayout()
            lbl = QLabel(label + ":")
            lbl.setStyleSheet(
                "font-size: 14px; color: #94A3B8; font-weight: 600;"
                " background: transparent;"
            )
            val = QLabel(value)
            val.setStyleSheet(
                f"font-size: 16px; color: {val_color}; font-weight: 800;"
                " background: transparent;"
            )
            val.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(val)
            cl.addLayout(row)

        btn_close = QPushButton("CLOSE")
        btn_close.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #EC4899, stop:1 #8B5CF6);
                color: white; border: none; border-radius: 10px;
                padding: 10px 35px; font-weight: 800; font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #F472B6, stop:1 #A78BFA);
            }
        """)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.accept)

        cl.addSpacing(12)
        cl.addWidget(btn_close, 0, Qt.AlignmentFlag.AlignHCenter)

        root.addWidget(card)
