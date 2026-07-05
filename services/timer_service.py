from PySide6.QtCore import QTimer, QObject, Signal

class TimerService(QObject):
    """
    Wraps QTimer to provide an isolated time ticking mechanism decoupled from the UI.
    """
    tick = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.tick.emit)

    def start(self) -> None:
        self.timer.start()

    def stop(self) -> None:
        self.timer.stop()
        
    def is_active(self) -> bool:
        return self.timer.isActive()
