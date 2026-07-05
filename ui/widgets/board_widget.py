from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy,
    QGraphicsDropShadowEffect, QPushButton
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QColor

from models.board_model import BoardModel
from ui.widgets.tile_widget import TileWidget


class BoardWidget(QFrame):
    tile_clicked = Signal(int)
    view_score_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("boardPanel")
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # Outer glow matching reference
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(45)
        shadow.setColor(QColor(139, 92, 246, 110))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(10)

        # Board title
        title_row = QHBoxLayout()
        title_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl = QLabel("🧩   PUZZLE BOARD   🧩")
        lbl.setObjectName("panelTitle")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_row.addWidget(lbl)
        outer.addLayout(title_row)

        # Inner grid container
        self._inner = QFrame()
        self._inner.setObjectName("boardInner")
        from PySide6.QtWidgets import QGridLayout
        self._grid = QGridLayout(self._inner)
        self._grid.setSpacing(8)
        self._grid.setContentsMargins(14, 14, 14, 14)
        self._grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(self._inner, 1)

        # Glowing VIEW SCORE button
        self.btn_view_score = QPushButton("🏆   VIEW SCORE")
        self.btn_view_score.setObjectName("btnViewScore")
        self.btn_view_score.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_view_score.setVisible(False)
        self.btn_view_score.clicked.connect(self.view_score_clicked.emit)

        glow_view = QGraphicsDropShadowEffect(self.btn_view_score)
        glow_view.setBlurRadius(25)
        glow_view.setColor(QColor(236, 72, 153, 200)) # Pink neon glow
        glow_view.setOffset(0, 0)
        self.btn_view_score.setGraphicsEffect(glow_view)

        # Container for bottom buttons
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_view_score)
        outer.addLayout(btn_layout)

    def show_score_button(self, visible: bool):
        self.btn_view_score.setVisible(visible)

    def render_board(self, board_model: BoardModel, full_pixmap: QPixmap):
        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        size = board_model.size
        tile_px = full_pixmap.width() // size

        for index, tile in enumerate(board_model.grid):
            if not tile.is_empty:
                r, c = divmod(tile.id, size)
                crop = full_pixmap.copy(c * tile_px, r * tile_px, tile_px, tile_px)
            else:
                crop = None

            widget = TileWidget(tile.id, index, crop, tile.is_empty)
            widget.clicked.connect(self.tile_clicked.emit)
            r_curr, c_curr = divmod(index, size)
            self._grid.addWidget(widget, r_curr, c_curr)
