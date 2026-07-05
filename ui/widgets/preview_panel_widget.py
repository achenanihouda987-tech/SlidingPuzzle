from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QProgressBar, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt


class PreviewPanelWidget(QFrame):
    """Right panel — TARGET IMAGE + progress + theme info card."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("rightPanel")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(139, 92, 246, 50))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 18, 14, 18)
        lay.setSpacing(14)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Panel title
        title = QLabel("⊕  TARGET IMAGE")
        title.setObjectName("panelTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(title)

        # Preview image
        self._img = QLabel()
        self._img.setFixedSize(200, 180)
        self._img.setObjectName("previewLabel")
        self._img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self._img, 0, Qt.AlignmentFlag.AlignHCenter)

        # Progress row
        prog_row = QHBoxLayout()
        prog_row.setSpacing(8)
        prog_lbl = QLabel("PROGRESS")
        prog_lbl.setObjectName("progressLabel")
        self._pct_lbl = QLabel("0%")
        self._pct_lbl.setObjectName("progressPct")
        prog_row.addWidget(prog_lbl)
        prog_row.addStretch()
        prog_row.addWidget(self._pct_lbl)
        lay.addLayout(prog_row)

        self._bar = QProgressBar()
        self._bar.setValue(0)
        self._bar.setTextVisible(False)
        self._bar.setFixedHeight(10)
        lay.addWidget(self._bar)

        # Theme info card
        self._theme_card = QFrame()
        self._theme_card.setObjectName("themeCard")
        tc_lay = QVBoxLayout(self._theme_card)
        tc_lay.setContentsMargins(14, 12, 14, 12)
        tc_lay.setSpacing(8)
        tc_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._theme_lbl = QLabel("🌲  Forest")
        self._theme_lbl.setObjectName("themeText")
        self._theme_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._diff_badge = QLabel("3 × 3")
        self._diff_badge.setObjectName("diffBadge")
        self._diff_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tc_lay.addWidget(self._theme_lbl)
        tc_lay.addWidget(self._diff_badge, 0, Qt.AlignmentFlag.AlignHCenter)

        lay.addWidget(self._theme_card)
        lay.addStretch()

    # ── public API ────────────────────────────────
    def set_image(self, pixmap: QPixmap, size: int, theme: str):
        icons = {"Forest": "🌲", "Sunset": "🌅", "Gradient": "🎨", "Custom": "🖼"}
        icon = icons.get(theme, "🖼")
        self._theme_lbl.setText(f"{icon}  {theme}")
        self._diff_badge.setText(f"{size} × {size}")
        self._img.setPixmap(pixmap.scaled(
            200, 180,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self._bar.setValue(0)
        self._pct_lbl.setText("0%")

    def set_progress(self, pct: int):
        self._bar.setValue(pct)
        self._pct_lbl.setText(f"{pct}%")
