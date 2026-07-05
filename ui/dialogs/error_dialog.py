from PySide6.QtWidgets import QMessageBox

class ErrorDialog:
    """
    Standardized dialog for displaying application errors gracefully.
    """
    @staticmethod
    def show(parent, message: str):
        msg = QMessageBox(parent)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.exec()
