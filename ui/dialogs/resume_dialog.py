from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor


def _neon_shadow(r=168, g=85, b=247, blur=40):
    fx = QGraphicsDropShadowEffect()
    fx.setBlurRadius(blur)
    fx.setColor(QColor(r, g, b, 160))
    fx.setOffset(0, 0)
    return fx


class ResumeDialog(QDialog):
    """
    Shown on login when an unfinished game is found.
    Emits resume_game or start_new based on user choice.
    """
    resume_game = Signal()
    start_new   = Signal()

    @staticmethod
    def ask(parent, saved: dict) -> "ResumeDialog":
        dlg = ResumeDialog(parent, saved)
        dlg.exec()
        return dlg

    def __init__(self, parent, saved: dict):
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
                border: 2px solid #A855F7;
                border-radius: 22px;
            }
        """)
        card.setGraphicsEffect(_neon_shadow())

        cl = QVBoxLayout(card)
        cl.setContentsMargins(36, 36, 36, 36)
        cl.setSpacing(18)
        cl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_lbl = QLabel("🎮")
        icon_lbl.setStyleSheet("font-size: 38px; background: transparent;")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Resume Your Game?")
        title.setStyleSheet(
            "font-size: 22px; font-weight: 900; color: #A855F7;"
            " letter-spacing: 1px; background: transparent;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        m, s  = divmod(saved.get("elapsed_time", 0), 60)
        info  = (
            f"Theme: {saved.get('theme','?')}  •  "
            f"{saved.get('difficulty','?')}×{saved.get('difficulty','?')}  •  "
            f"Moves: {saved.get('moves',0)}  •  "
            f"Time: {m:02d}:{s:02d}  •  "
            f"Progress: {saved.get('progress',0)}%"
        )
        info_lbl = QLabel(info)
        info_lbl.setStyleSheet(
            "font-size: 13px; color: #94A3B8; background: transparent;"
        )
        info_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_lbl.setWordWrap(True)

        btn_resume = QPushButton("▶   CONTINUE GAME")
        btn_resume.setObjectName("btnStart")
        btn_resume.setFixedHeight(48)
        btn_resume.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_resume.clicked.connect(self._on_resume)

        btn_new = QPushButton("⊕   START NEW GAME")
        btn_new.setObjectName("btnSecondary")
        btn_new.setFixedHeight(44)
        btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_new.clicked.connect(self._on_new)

        cl.addWidget(icon_lbl)
        cl.addWidget(title)
        cl.addWidget(info_lbl)
        cl.addSpacing(8)
        cl.addWidget(btn_resume)
        cl.addWidget(btn_new)

        root.addWidget(card)

    def _on_resume(self):
        self.resume_game.emit()
        self.accept()

    def _on_new(self):
        self.start_new.emit()
        self.accept()
