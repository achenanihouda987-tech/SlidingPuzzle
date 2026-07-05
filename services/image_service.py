import os
from PySide6.QtGui import QPixmap, QImageReader
from PySide6.QtCore import Qt
from core.exceptions import ImageLoadError

class ImageService:
    """
    Handles robust image loading, scaling, and processing for both
    built-in themes and custom user images.
    """
    
    IMAGE_MAP = {
        "Gradient": "assets/images/gradient.jpg",
        "Sunset": "assets/images/sunset.jpg",
        "Forest": "assets/images/forest.jpg"
    }

    @staticmethod
    def load_builtin_image(theme_name: str, size: int) -> QPixmap:
        """
        Loads a default local image based on the selected theme.
        Falls back safely if the image is missing.
        """
        if theme_name not in ImageService.IMAGE_MAP:
            raise ImageLoadError(f"Unknown theme: {theme_name}")
            
        filepath = ImageService.IMAGE_MAP[theme_name]
        
        if not os.path.exists(filepath):
            raise ImageLoadError(f"Missing default image file: {filepath}")
            
        return ImageService.load_image(filepath, size)

    @staticmethod
    def load_image(filepath: str, size: int) -> QPixmap:
        """
        Loads and scales any image to the exact square size needed.
        """
        if not os.path.exists(filepath):
            raise ImageLoadError(f"File not found: {filepath}")
            
        reader = QImageReader(filepath)
        if not reader.canRead():
            raise ImageLoadError(f"Cannot read image file format: {filepath}")
            
        reader.setAutoTransform(True)
        img = reader.read()
        if img.isNull():
            raise ImageLoadError(f"Failed to decode valid image data from {filepath}")
            
        pixmap = QPixmap.fromImage(img)
        
        # Scale to ensure the shortest side fits the requested size, keeping aspect ratio
        scaled = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        
        # Crop to center square
        x = max(0, (scaled.width() - size) // 2)
        y = max(0, (scaled.height() - size) // 2)
        
        return scaled.copy(x, y, size, size)
