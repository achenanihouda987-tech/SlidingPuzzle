from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from services.auth_service import AuthService
from models.user_model import UserModel


def _neon_shadow(r=168, g=85, b=247, blur=30) -> QGraphicsDropShadowEffect:
    fx = QGraphicsDropShadowEffect()
    fx.setBlurRadius(blur)
    fx.setColor(QColor(r, g, b, 160))
    fx.setOffset(0, 0)
    return fx


class RegisterPage(QWidget):
    """
    Neon-glass registration form.
    Emits register_success(UserModel) and login_requested.
    """
    register_success = Signal(object)  # UserModel
    login_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("authPage")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("authCard")
        card.setFixedWidth(420)
        card.setGraphicsEffect(_neon_shadow())

        lay = QVBoxLayout(card)
        lay.setContentsMargins(44, 44, 44, 44)
        lay.setSpacing(14)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header
        crown = QLabel("♛")
        crown.setObjectName("crownLabel")
        crown.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("SLIDPUZZLE")
        title.setObjectName("mainTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub = QLabel("Join the puzzle community")
        sub.setObjectName("authSubtitle")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lay.addWidget(crown)
        lay.addWidget(title)
        lay.addWidget(sub)
        lay.addSpacing(6)

        # Fields
        self._username_input = self._make_field("👤  Username")
        self._email_input    = self._make_field("✉   Email")
        self._password_input = self._make_field("🔒  Password", password=True)
        self._confirm_input  = self._make_field("🔒  Confirm Password", password=True)

        for label, widget in [
            ("Username", self._username_input),
            ("Email", self._email_input),
            ("Password", self._password_input),
            ("Confirm Password", self._confirm_input),
        ]:
            lay.addWidget(QLabel(label, objectName="fieldLabel"))
            lay.addWidget(widget)

        # Error label
        self._error_lbl = QLabel("")
        self._error_lbl.setObjectName("errorLabel")
        self._error_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._error_lbl.setWordWrap(True)
        lay.addWidget(self._error_lbl)

        # CREATE ACCOUNT button
        btn_create = QPushButton("✦   CREATE ACCOUNT")
        btn_create.setObjectName("btnStart")
        btn_create.setFixedHeight(50)
        btn_create.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_create.clicked.connect(self._attempt_register)
        lay.addWidget(btn_create)

        # Back to login
        back_row = QHBoxLayout()
        back_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_row.addWidget(QLabel("Already have an account?", objectName="authHint"))
        btn_login = QPushButton("Sign In")
        btn_login.setObjectName("btnLink")
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.clicked.connect(self.login_requested.emit)
        back_row.addWidget(btn_login)
        lay.addLayout(back_row)

        root.addWidget(card)

    def _make_field(self, placeholder: str, password=False) -> QLineEdit:
        field = QLineEdit()
        field.setObjectName("authField")
        field.setPlaceholderText(placeholder)
        field.setFixedHeight(44)
        if password:
            field.setEchoMode(QLineEdit.EchoMode.Password)
        return field

    def _attempt_register(self):
        self._error_lbl.setText("")
        username = self._username_input.text().strip()
        email    = self._email_input.text().strip()
        password = self._password_input.text()
        confirm  = self._confirm_input.text()

        if not username or not email or not password or not confirm:
            self._error_lbl.setText("Please fill in all fields.")
            return
        if password != confirm:
            self._error_lbl.setText("Passwords do not match.")
            return

        try:
            user = AuthService.register(username, email, password)
            self.register_success.emit(user)
        except ValueError as e:
            self._error_lbl.setText(str(e))

    def clear(self):
        for f in [self._username_input, self._email_input,
                  self._password_input, self._confirm_input]:
            f.clear()
        self._error_lbl.setText("")
