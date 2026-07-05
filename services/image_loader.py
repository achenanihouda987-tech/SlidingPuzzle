from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class ImageLoader:
    @staticmethod
    def load_custom_image(path: str, size: int) -> QPixmap:
        pixmap = QPixmap(path)
        if pixmap.isNull():
            raise ValueError("Failed to load image")
        # Scaled to square
        return pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation).copy(0, 0, size, size)
