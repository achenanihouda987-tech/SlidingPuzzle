from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor


def _neon_shadow(r=217, g=70, b=239, blur=50):
    fx = QGraphicsDropShadowEffect()
    fx.setBlurRadius(blur)
    fx.setColor(QColor(r, g, b, 160))
    fx.setOffset(0, 0)
    return fx


class VictoryDialog(QDialog):
    """
    Auto-shown when the puzzle is solved.
    save_score_requested is emitted when user clicks Save Best Score.
    play_again_requested is emitted on Play Again.
    """
    save_score_requested = Signal()
    play_again_requested = Signal()

    @staticmethod
    def show(parent, moves: int, seconds: int, difficulty: int, theme: str, 
             is_record: bool = False, score: int = 0):
        dlg = VictoryDialog(parent, moves, seconds, difficulty, theme, is_record, score)
        dlg.exec()

    def __init__(self, parent, moves: int, seconds: int, difficulty: int, theme: str,
                 is_record: bool = False, score: int = 0):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumWidth(420)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)

        card = QFrame()
        card.setObjectName("glassPanel")
        card.setStyleSheet("""
            QFrame#glassPanel {
                background-color: rgba(20,20,42,0.97);
                border: 2px solid #D946EF;
                border-radius: 22px;
            }
        """)
        card.setGraphicsEffect(_neon_shadow())

        cl = QVBoxLayout(card)
        cl.setContentsMargins(40, 44, 40, 44)
        cl.setSpacing(16)
        cl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Trophy
        trophy = QLabel("🏆")
        trophy.setStyleSheet("font-size: 48px; background: transparent;")
        trophy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("🎉 CONGRATULATIONS!\nPuzzle Completed Successfully")
        title.setStyleSheet(
            "font-size: 22px; font-weight: 900; color: #D946EF;"
            " letter-spacing: 2px; background: transparent;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if is_record:
            rec_lbl = QLabel("🎉  New Record!")
            rec_lbl.setStyleSheet(
                "font-size: 15px; color: #FBBF24; font-weight: 800;"
                " background: transparent;"
            )
            rec_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            rec_lbl = None

        m, s = divmod(seconds, 60)
        stats = QLabel(
            f"Moves: {moves}   •   Time: {m:02d}:{s:02d}\n"
            f"Difficulty: {difficulty} × {difficulty}   •   Theme: {theme}"
        )
        stats.setStyleSheet(
            "font-size: 14px; color: #94A3B8; background: transparent;"
        )
        stats.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Success message (hidden by default)
        self.success_msg = QLabel("✅ Best Score Saved Successfully!")
        self.success_msg.setStyleSheet("font-size: 14px; color: #34D399; font-weight: bold; background: transparent;")
        self.success_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_msg.hide()

        # Buttons
        self.btn_save = QPushButton("🏆 SAVE MY BEST SCORE")
        self.btn_save.setObjectName("btnStart")
        self.btn_save.setFixedHeight(48)
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.clicked.connect(self.save_score_requested.emit)

        btn_again = QPushButton("🔄 PLAY AGAIN")
        btn_again.setObjectName("btnSecondary")
        btn_again.setFixedHeight(44)
        btn_again.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_again.clicked.connect(lambda: (self.play_again_requested.emit(), self.accept()))

        btn_close = QPushButton("❌ CLOSE")
        btn_close.setObjectName("btnLink")
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.accept)

        cl.addWidget(trophy)
        cl.addWidget(title)
        if rec_lbl:
            cl.addWidget(rec_lbl)
        cl.addWidget(stats)
        cl.addWidget(self.success_msg)
        cl.addSpacing(10)
        cl.addWidget(self.btn_save)
        cl.addWidget(btn_again)
        cl.addWidget(btn_close, 0, Qt.AlignmentFlag.AlignHCenter)

        root.addWidget(card)

    def show_success(self):
        self.btn_save.setDisabled(True)
        self.btn_save.setText("🏆 SCORE ALREADY SAVED")
        self.success_msg.show()
