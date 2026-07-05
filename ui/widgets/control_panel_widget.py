from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox,
    QLabel, QFileDialog, QSizePolicy
)
from PySide6.QtCore import Signal, Qt


class ControlPanelWidget(QFrame):
    new_game_requested = Signal(int, str, str)   # size, theme, custom_path
    reshuffle_requested = Signal()
    finish_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("controlBar")
        self._custom_path = None

        row = QHBoxLayout(self)
        row.setContentsMargins(24, 16, 24, 16)
        row.setSpacing(20)
        row.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # 🧩 DIFFICULTY dropdown
        row.addLayout(self._labeled_combo(
            "🧩  DIFFICULTY",
            ["3 × 3", "4 × 4", "5 × 5"],
        ))
        self.size_combo = self._last_combo

        # 🎨 THEME dropdown
        row.addLayout(self._labeled_combo(
            "🎨  THEME",
            ["🌲  Forest", "🌇  Sunset", "🎨  Gradient"],
        ))
        self.style_combo = self._last_combo

        # START GAME
        self.btn_new = QPushButton("▶   START GAME")
        self.btn_new.setObjectName("btnStart")
        self.btn_new.setFixedHeight(50)
        self.btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        row.addWidget(self.btn_new)

        # SHUFFLE
        self.btn_shuffle = QPushButton("⇄   SHUFFLE")
        self.btn_shuffle.setObjectName("btnSecondary")
        self.btn_shuffle.setFixedHeight(50)
        self.btn_shuffle.setCursor(Qt.CursorShape.PointingHandCursor)
        row.addWidget(self.btn_shuffle)

        # CUSTOM IMAGE
        self.btn_custom = QPushButton("☁   CUSTOM IMAGE")
        self.btn_custom.setObjectName("btnSecondary")
        self.btn_custom.setFixedHeight(50)
        self.btn_custom.setCursor(Qt.CursorShape.PointingHandCursor)
        row.addWidget(self.btn_custom)

        # FINISH GAME (COMPACT)
        self.btn_finish = QPushButton("✔ Finish")
        self.btn_finish.setObjectName("btnFinishCompact")
        self.btn_finish.setFixedSize(110, 35)
        self.btn_finish.setEnabled(False)
        self.btn_finish.setToolTip("Click when puzzle is complete")
        self.btn_finish.setCursor(Qt.CursorShape.PointingHandCursor)
        row.addWidget(self.btn_finish)

        self.btn_new.clicked.connect(self._on_new_game)
        self.btn_shuffle.clicked.connect(self.reshuffle_requested.emit)
        self.btn_custom.clicked.connect(self._on_custom_image)
        self.btn_finish.clicked.connect(self.finish_clicked.emit)

    def reset_finish_button(self):
        self.btn_finish.setEnabled(False)

    # ── helpers ──────────────────────────────────────
    def _labeled_combo(self, label_text: str, items: list):
        vbox = QVBoxLayout()
        vbox.setSpacing(4)
        vbox.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel(label_text)
        lbl.setObjectName("dropLabel")

        combo = QComboBox()
        combo.addItems(items)
        combo.setFixedHeight(42)
        combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self._last_combo = combo

        vbox.addWidget(lbl)
        vbox.addWidget(combo)
        return vbox

    def _parse_size(self) -> int:
        return int(self.size_combo.currentText()[0])

    def _parse_style(self) -> str:
        return self.style_combo.currentText().split("  ")[-1].strip()

    def _on_new_game(self):
        self.new_game_requested.emit(self._parse_size(), self._parse_style(), "")

    def _on_custom_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "",
            "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.new_game_requested.emit(self._parse_size(), "Custom", path)
