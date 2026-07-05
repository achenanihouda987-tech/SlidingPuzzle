from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from database import score_repository
from models.user_model import UserModel


def _neon_shadow(r=168, g=85, b=247, blur=40):
    fx = QGraphicsDropShadowEffect()
    fx.setBlurRadius(blur)
    fx.setColor(QColor(r, g, b, 160))
    fx.setOffset(0, 0)
    return fx


class ScoreHistoryDialog(QDialog):
    """Ranked score history table for the current user."""

    @staticmethod
    def show(parent, user: UserModel):
        dlg = ScoreHistoryDialog(parent, user)
        dlg.exec()

    def __init__(self, parent, user: UserModel):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumWidth(680)
        self.setMinimumHeight(520)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)

        card = QFrame()
        card.setObjectName("glassPanel")
        card.setStyleSheet("""
            QFrame#glassPanel {
                background-color: rgba(13,13,26,0.97);
                border: 2px solid #A855F7;
                border-radius: 22px;
            }
        """)
        card.setGraphicsEffect(_neon_shadow())

        cl = QVBoxLayout(card)
        cl.setContentsMargins(30, 30, 30, 30)
        cl.setSpacing(16)

        # Header
        hdr_row = QHBoxLayout()
        icon = QLabel("🏆")
        icon.setStyleSheet("font-size: 28px; background: transparent;")
        title = QLabel("SCORE HISTORY")
        title.setStyleSheet(
            "font-size: 22px; font-weight: 900; color: #A855F7;"
            " letter-spacing: 2px; background: transparent;"
        )
        hdr_row.addWidget(icon)
        hdr_row.addWidget(title)
        hdr_row.addStretch()
        cl.addLayout(hdr_row)

        # User stats cards
        stats = score_repository.get_user_stats(user.id)
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)

        def _make_stat_card(icon, title, value, color):
            c = QFrame()
            c.setObjectName("statCardHistory")
            c.setStyleSheet(f"""
                QFrame#statCardHistory {{
                    background-color: rgba(15,12,40,0.85);
                    border: 1px solid {color};
                    border-radius: 12px;
                }}
            """)
            cl = QVBoxLayout(c)
            cl.setContentsMargins(16, 12, 16, 12)
            cl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            lbl_title = QLabel(f"{icon} {title}")
            lbl_title.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; background: transparent; letter-spacing: 1px;")
            lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            lbl_val = QLabel(str(value))
            lbl_val.setStyleSheet(f"font-size: 20px; font-weight: 900; color: {color}; background: transparent;")
            lbl_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            cl.addWidget(lbl_title)
            cl.addWidget(lbl_val)
            return c

        stats_row.addWidget(_make_stat_card("🏆", "Personal Best", stats['best_score'] or '—', "#FBBF24"))
        stats_row.addWidget(_make_stat_card("🎮", "Total Games Played", stats.get('total_games', stats['total_wins']), "#3B82F6"))
        stats_row.addWidget(_make_stat_card("✅", "Total Wins", stats['total_wins'], "#34D399"))
        
        cl.addLayout(stats_row)

        # Table
        history = score_repository.get_history_for_user(user.id)
        cols = ["Rank", "Theme", "Difficulty", "Moves", "Time", "Score", "Date"]
        table = QTableWidget(len(history), len(cols))
        table.setHorizontalHeaderLabels(cols)
        table.setObjectName("scoreTable")
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setStyleSheet("""
            QTableWidget {
                background-color: rgba(10, 8, 28, 0.90);
                color: #E2E8F0;
                border: 1px solid rgba(139,92,246,0.4);
                border-radius: 10px;
                gridline-color: rgba(139,92,246,0.2);
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: rgba(88,28,135,0.4);
                color: #A855F7;
                font-weight: 800;
                font-size: 12px;
                letter-spacing: 1px;
                border: none;
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: rgba(139,92,246,0.25);
            }
        """)

        for rank, row in enumerate(history, 1):
            m, s   = divmod(row["time_seconds"], 60)
            diff   = row["difficulty"]
            values = [
                str(rank),
                row["theme"],
                f"{diff} × {diff}",
                str(row["moves"]),
                f"{m:02d}:{s:02d}",
                str(row["score"]),
                row["date_created"][:10],
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 5:  # score column — highlight top
                    item.setForeground(QColor("#FBBF24"))
                table.setItem(rank - 1, col, item)

        cl.addWidget(table)

        # Close button
        btn_close = QPushButton("CLOSE")
        btn_close.setObjectName("btnSecondary")
        btn_close.setFixedHeight(44)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.accept)
        cl.addWidget(btn_close, 0, Qt.AlignmentFlag.AlignHCenter)

        root.addWidget(card)
