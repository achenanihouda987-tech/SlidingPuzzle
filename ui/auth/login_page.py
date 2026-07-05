from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QFrame, QGraphicsDropShadowEffect, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont

from services.auth_service import AuthService
from models.user_model import UserModel


def _neon_shadow(r=168, g=85, b=247, blur=30) -> QGraphicsDropShadowEffect:
    fx = QGraphicsDropShadowEffect()
    fx.setBlurRadius(blur)
    fx.setColor(QColor(r, g, b, 160))
    fx.setOffset(0, 0)
    return fx


class LoginPage(QWidget):
    """
    Full-screen neon-glass login page shown before the game.
    Emits login_success(UserModel) on valid credentials.
    Emits register_requested to switch to the register page.
    """
    login_success = Signal(object)   # UserModel
    register_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("authPage")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ── Centered glass card ──────────────────────────
        card = QFrame()
        card.setObjectName("authCard")
        card.setFixedWidth(420)
        card.setGraphicsEffect(_neon_shadow())

        lay = QVBoxLayout(card)
        lay.setContentsMargins(44, 44, 44, 44)
        lay.setSpacing(18)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Crown + Title
        crown = QLabel("♛")
        crown.setObjectName("crownLabel")
        crown.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("SLIDPUZZLE")
        title.setObjectName("mainTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub = QLabel("Sign in to your account")
        sub.setObjectName("authSubtitle")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lay.addWidget(crown)
        lay.addWidget(title)
        lay.addWidget(sub)
        lay.addSpacing(8)

        # ── Fields ──────────────────────────────────────
        self._username_input = self._make_field("👤  Username or Email")
        self._password_input = self._make_field("🔒  Password", password=True)

        lay.addWidget(QLabel("Username or Email", objectName="fieldLabel"))
        lay.addWidget(self._username_input)
        lay.addWidget(QLabel("Password", objectName="fieldLabel"))
        lay.addWidget(self._password_input)

        # Remember me
        self._remember = QCheckBox("Remember me")
        self._remember.setObjectName("authCheck")
        lay.addWidget(self._remember)

        # Error label
        self._error_lbl = QLabel("")
        self._error_lbl.setObjectName("errorLabel")
        self._error_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._error_lbl.setWordWrap(True)
        lay.addWidget(self._error_lbl)

        # LOGIN button
        btn_login = QPushButton("▶   LOGIN")
        btn_login.setObjectName("btnStart")
        btn_login.setFixedHeight(50)
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.clicked.connect(self._attempt_login)
        lay.addWidget(btn_login)

        # Register link
        reg_row = QHBoxLayout()
        reg_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        no_account = QLabel("Don't have an account?")
        no_account.setObjectName("authHint")
        btn_register = QPushButton("Create Account")
        btn_register.setObjectName("btnLink")
        btn_register.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_register.clicked.connect(self.register_requested.emit)
        reg_row.addWidget(no_account)
        reg_row.addWidget(btn_register)
        lay.addLayout(reg_row)

        root.addWidget(card)

    def _make_field(self, placeholder: str, password=False) -> QLineEdit:
        field = QLineEdit()
        field.setObjectName("authField")
        field.setPlaceholderText(placeholder)
        field.setFixedHeight(44)
        if password:
            field.setEchoMode(QLineEdit.EchoMode.Password)
        return field

    def _attempt_login(self):
        self._error_lbl.setText("")
        username = self._username_input.text().strip()
        password = self._password_input.text()

        if not username or not password:
            self._error_lbl.setText("Please fill in all fields.")
            return

        user = AuthService.login(username, password)
        if user:
            self.login_success.emit(user)
        else:
            self._error_lbl.setText("Invalid username or password.")

    def clear(self):
        self._username_input.clear()
        self._password_input.clear()
        self._error_lbl.setText("")
