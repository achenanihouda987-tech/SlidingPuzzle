from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


def _glow(r, g, b, blur=18):
    fx = QGraphicsDropShadowEffect()
    fx.setBlurRadius(blur)
    fx.setColor(QColor(r, g, b, 110))
    fx.setOffset(0, 0)
    return fx


class StatsPanelWidget(QFrame):
    """Left panel — compact GAME STATS with 3 glowing cards (~25% smaller)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statsPanel")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 14, 10, 14)
        lay.setSpacing(8)

        # Panel title
        title = QLabel("🧩  GAME STATS")
        title.setObjectName("panelTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(title)
        lay.addSpacing(2)

        # Moves — purple
        self._moves_val = QLabel("0")
        self._moves_val.setObjectName("statValPurple")
        lay.addWidget(self._make_card(
            "cardPurple", "❗", "MOVES",
            self._moves_val, _glow(168, 85, 247)
        ))

        # Timer — blue
        self._time_val = QLabel("00:00")
        self._time_val.setObjectName("statValBlue")
        lay.addWidget(self._make_card(
            "cardBlue", "🕒", "TIMER",
            self._time_val, _glow(59, 130, 246)
        ))

        # Best Score — gold
        self._best_val = QLabel("- - -")
        self._best_val.setObjectName("statValGold")
        lay.addWidget(self._make_card(
            "cardGold", "🏆", "BEST SCORE",
            self._best_val, _glow(234, 179, 8)
        ))

        lay.addStretch()

    # ── public API ────────────────────────────────
    def update_moves(self, moves: int):
        self._moves_val.setText(str(moves))

    def update_time(self, seconds: int):
        m, s = divmod(seconds, 60)
        self._time_val.setText(f"{m:02d}:{s:02d}")

    def update_best_score(self, score):
        self._best_val.setText(str(score) if score is not None else "- - -")

    # ── private ───────────────────────────────────
    def _make_card(self, obj_name, icon, label, val_lbl, shadow):
        card = QFrame()
        card.setObjectName(obj_name)
        card.setGraphicsEffect(shadow)

        cl = QVBoxLayout(card)
        cl.setContentsMargins(8, 8, 8, 8)   # compact: was 14
        cl.setSpacing(2)
        cl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ico = QLabel(icon)
        ico.setObjectName("statIconCircle")
        ico.setStyleSheet("font-size: 16px; background: transparent;")  # compact
        ico.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl = QLabel(label)
        lbl.setObjectName("statName")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cl.addWidget(ico)
        cl.addWidget(lbl)
        cl.addWidget(val_lbl)
        return card
