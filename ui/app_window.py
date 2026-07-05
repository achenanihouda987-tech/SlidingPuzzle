import os
from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtCore import Qt

from models.user_model import UserModel
from services.session_service import SessionService
from database import db_manager


class AppWindow(QMainWindow):
    """
    Root application window. Holds a QStackedWidget with three pages:
      0 — LoginPage
      1 — RegisterPage
      2 — GamePage
    Applies the global stylesheet to the main window.
    """

    PAGE_LOGIN    = 0
    PAGE_REGISTER = 1
    PAGE_GAME     = 2

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sliding Puzzle")
        self.setMinimumSize(1100, 820)

        # Ensure DB is initialized
        db_manager.initialize()

        # Apply global stylesheet
        self._load_styles()

        # Build pages
        from ui.auth.login_page    import LoginPage
        from ui.auth.register_page import RegisterPage
        from ui.game_page          import GamePage

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self._login_page    = LoginPage()
        self._register_page = RegisterPage()
        self._game_page     = GamePage(self)

        self._stack.addWidget(self._login_page)     # 0
        self._stack.addWidget(self._register_page)  # 1
        self._stack.addWidget(self._game_page)      # 2

        # Wire auth signals
        self._login_page.login_success.connect(self._on_login)
        self._login_page.register_requested.connect(self.show_register)

        self._register_page.register_success.connect(self._on_register)
        self._register_page.login_requested.connect(self.show_login)

        self.show_login()

    # ── Navigation ────────────────────────────────────────
    def show_login(self):
        self._login_page.clear()
        self._stack.setCurrentIndex(self.PAGE_LOGIN)

    def show_register(self):
        self._register_page.clear()
        self._stack.setCurrentIndex(self.PAGE_REGISTER)

    def show_game(self, user: UserModel):
        SessionService.instance().login(user)
        self._game_page.activate(user)
        self._stack.setCurrentIndex(self.PAGE_GAME)

    # ── Auth callbacks ────────────────────────────────────
    def _on_login(self, user: UserModel):
        self.show_game(user)

    def _on_register(self, user: UserModel):
        """After registration, immediately log in."""
        self.show_game(user)

    # ── Stylesheet ────────────────────────────────────────
    def _load_styles(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "styles", "dark_theme.qss")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def closeEvent(self, event):
        """Auto-save on window close."""
        if hasattr(self, "_game_page"):
            self._game_page.deactivate()
        super().closeEvent(event)
