from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QProgressBar, QGraphicsDropShadowEffect
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt

class PreviewWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("glassPanel")
        self.setFixedWidth(240)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(168, 85, 247, 50))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        self.title = QLabel("TARGET PREVIEW")
        self.title.setObjectName("statTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.image_label = QLabel()
        self.image_label.setFixedSize(160, 160)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border-radius: 12px; border: 2px solid #D946EF; background-color: #0D0D1A;")
        
        self.badge = QLabel("LVL: 3x3")
        self.badge.setObjectName("previewBadge")
        self.badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        
        prog_title = QLabel("PROGRESS")
        prog_title.setObjectName("statTitle")
        prog_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.title)
        layout.addWidget(self.image_label, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.badge, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
        layout.addWidget(prog_title)
        layout.addWidget(self.progress)
        
    def set_image(self, pixmap: QPixmap, size: int):
        self.badge.setText(f"LVL: {size}x{size}")
        self.image_label.setPixmap(pixmap.scaled(
            160, 160, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        ))
        self.progress.setValue(0)
