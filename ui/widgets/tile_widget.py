from PySide6.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QCursor, QColor


class TileWidget(QLabel):
    clicked = Signal(int)

    # Fixed pixel size per tile for a clean uniform grid
    TILE_SIZE = 128

    def __init__(self, tile_id: int, current_idx: int,
                 pixmap: QPixmap, is_empty: bool):
        super().__init__()
        self.tile_id = tile_id
        self.current_idx = current_idx
        self.is_empty = is_empty

        self.setFixedSize(self.TILE_SIZE, self.TILE_SIZE)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if not self.is_empty and pixmap:
            scaled = pixmap.scaled(
                self.TILE_SIZE, self.TILE_SIZE,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.setPixmap(scaled)
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.setStyleSheet("""
                TileWidget {
                    border: 2px solid rgba(139, 92, 246, 0.65);
                    border-radius: 10px;
                }
                TileWidget:hover {
                    border: 2px solid #A855F7;
                    background-color: rgba(139, 92, 246, 0.15);
                }
            """)
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(10)
            shadow.setColor(QColor(0, 0, 0, 180))
            shadow.setOffset(0, 3)
            self.setGraphicsEffect(shadow)
        else:
            # Empty slot — dark, no border
            self.setStyleSheet("""
                TileWidget {
                    background-color: #07071A;
                    border-radius: 10px;
                    border: none;
                }
            """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.is_empty:
            self.clicked.emit(self.current_idx)
