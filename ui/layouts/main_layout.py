from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt


class MainLayout(QVBoxLayout):
    """
    Assembles the full window layout matching the reference image:
      Header → Control Bar → [Left Stats | Board | Right Preview] → Footer
    """
    def __init__(self, parent, control_bar, stats_panel,
                 board_panel, right_panel, bottom_bar):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        # ── 1. Header ──────────────────────────────
        self.addWidget(self._build_header())

        # ── 2. Control Bar ─────────────────────────
        ctrl_wrap = QFrame()
        ctrl_wrap.setObjectName("rootBg")
        cw_l = QHBoxLayout(ctrl_wrap)
        cw_l.setContentsMargins(28, 0, 28, 18)
        cw_l.addWidget(control_bar, 0, Qt.AlignmentFlag.AlignHCenter)
        self.addWidget(ctrl_wrap)

        # ── 3. Three-column game area ───────────────
        game_wrap = QFrame()
        game_wrap.setObjectName("rootBg")
        game_l = QHBoxLayout(game_wrap)
        game_l.setContentsMargins(20, 0, 20, 12)
        game_l.setSpacing(16)

        # Left fixed width, board stretches, right fixed width
        stats_panel.setFixedWidth(190)
        right_panel.setFixedWidth(230)

        game_l.addWidget(stats_panel, 0, Qt.AlignmentFlag.AlignTop)
        game_l.addWidget(board_panel, 1)
        game_l.addWidget(right_panel, 0, Qt.AlignmentFlag.AlignTop)

        self.addWidget(game_wrap, 1)

        # ── 4. Footer ───────────────────────────────
        self.addWidget(bottom_bar)

    # ─────────────────────────────────────────────
    def _build_header(self) -> QFrame:
        hdr = QFrame()
        hdr.setObjectName("rootBg")
        lay = QVBoxLayout(hdr)
        lay.setContentsMargins(20, 28, 20, 18)
        lay.setSpacing(4)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        crown = QLabel("♛")
        crown.setObjectName("crownLabel")
        crown.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("SLIDING PUZZLE")
        title.setObjectName("mainTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtitle row with arrow decorations
        sub_row = QHBoxLayout()
        sub_row.setSpacing(14)
        sub_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        def _arrow(direction="right"):
            a = QLabel("→" if direction == "right" else "←")
            a.setStyleSheet("color: rgba(168,85,247,0.7); font-size:14px; background:transparent;")
            return a

        sub = QLabel("Rebuild the image piece by piece")
        sub.setObjectName("subTitle")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub_row.addWidget(_arrow("left"))
        sub_row.addWidget(sub)
        sub_row.addWidget(_arrow("right"))

        lay.addWidget(crown)
        lay.addWidget(title)
        lay.addLayout(sub_row)
        return hdr
