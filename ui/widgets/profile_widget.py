from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from database import score_repository
from models.user_model import UserModel


class ProfileWidget(QFrame):
    """
    Top-right horizontal strip showing the logged-in user's name,
    win stats, and Logout / Score History buttons.
    """
    logout_requested = Signal()
    history_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("profileBar")

        row = QHBoxLayout(self)
        row.setContentsMargins(14, 8, 14, 8)
        row.setSpacing(16)

        # User avatar + name
        self._avatar = QLabel("👤")
        self._avatar.setObjectName("profileAvatar")

        self._name_lbl = QLabel("—")
        self._name_lbl.setObjectName("profileName")

        # Stats strip
        self._stats_lbl = QLabel("")
        self._stats_lbl.setObjectName("profileStats")

        # Buttons
        self._btn_history = QPushButton("🏆  SCORE HISTORY")
        self._btn_history.setObjectName("btnScoreHistory")
        self._btn_history.setFixedHeight(34)
        self._btn_history.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_history.clicked.connect(self.history_requested.emit)

        self._btn_logout = QPushButton("Logout")
        self._btn_logout.setObjectName("btnLink")
        self._btn_logout.setFixedHeight(34)
        self._btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_logout.clicked.connect(self.logout_requested.emit)

        row.addWidget(self._avatar)
        row.addWidget(self._name_lbl)
        row.addWidget(self._stats_lbl)
        row.addStretch()
        row.addWidget(self._btn_history)
        row.addWidget(self._btn_logout)

    def refresh(self, user: UserModel) -> None:
        """Populate widget with current user data."""
        self._name_lbl.setText(user.username)
        stats = score_repository.get_user_stats(user.id)
        wins  = stats["total_wins"]
        best  = stats["best_score"]
        self._stats_lbl.setText(
            f"  Wins: {wins}   Best: {best if best else '—'}"
        )
