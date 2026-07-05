import sys
from PySide6.QtWidgets import QApplication
from ui.app_window import AppWindow


def main():
    """Application entry point — starts with Login page."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = AppWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
