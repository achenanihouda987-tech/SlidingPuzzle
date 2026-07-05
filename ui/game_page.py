import os
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer

from models.user_model import UserModel
from services.session_service import SessionService
from services.best_score_service import BestScoreService
from database import saved_game_repository

from ui.widgets.control_panel_widget import ControlPanelWidget
from ui.widgets.stats_panel_widget import StatsPanelWidget
from ui.widgets.board_widget import BoardWidget
from ui.widgets.preview_panel_widget import PreviewPanelWidget
from ui.widgets.bottom_bar_widget import BottomBarWidget
from ui.widgets.profile_widget import ProfileWidget
from ui.layouts.main_layout import MainLayout
from controllers.game_controller import GameController
from controllers.ui_controller import UIController


class GamePage(QWidget):
    """
    The main game screen. Contains the profile bar at the top and
    the full game layout below. Manages save/resume lifecycle.
    """

    def __init__(self, app_window, parent=None):
        super().__init__(parent)
        self._app_window = app_window
        self._ui_ctrl: UIController = None
        self._auto_save_timer = QTimer(self)
        self._auto_save_timer.setInterval(30_000)   # auto-save every 30 s
        self._auto_save_timer.timeout.connect(self._auto_save)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Profile bar ───────────────────────────────────
        self.profile_bar = ProfileWidget()
        self.profile_bar.logout_requested.connect(self._on_logout)
        self.profile_bar.history_requested.connect(self._on_history)
        root.addWidget(self.profile_bar)

        # ── Game area root widget ─────────────────────────
        self._game_root = QWidget()
        self._game_root.setObjectName("rootBg")
        root.addWidget(self._game_root, 1)

        self._load_styles()

        # Build widgets
        self.control_panel  = ControlPanelWidget()
        self.stats_panel    = StatsPanelWidget()
        self.board_widget   = BoardWidget()
        self.preview_widget = PreviewPanelWidget()
        self.bottom_bar     = BottomBarWidget()

        self.main_layout = MainLayout(
            self._game_root,
            self.control_panel,
            self.stats_panel,
            self.board_widget,
            self.preview_widget,
            self.bottom_bar,
        )

        # Game controller
        self.game_controller = GameController()
        self._ui_ctrl = UIController(self, self.game_controller)

        # Bottom bar help
        self.bottom_bar.help_clicked.connect(self._ui_ctrl._show_help)

    # ── Public lifecycle API ──────────────────────────────
    def activate(self, user: UserModel):
        """Called when the user logs in. Checks for saved game."""
        self.profile_bar.refresh(user)
        self._refresh_best_score()

        saved = saved_game_repository.find_by_user(user.id)
        if saved:
            from ui.dialogs.resume_dialog import ResumeDialog
            dlg = ResumeDialog(self, saved)
            dlg.resume_game.connect(lambda: self._resume_game(saved))
            dlg.start_new.connect(self._start_fresh)
            dlg.exec()
        else:
            self._start_fresh()

        self._auto_save_timer.start()

    def deactivate(self):
        """Called when the user logs out."""
        self._auto_save()
        self._auto_save_timer.stop()

    def _start_fresh(self):
        user = SessionService.instance().get_user()
        if user:
            saved_game_repository.delete(user.id)
        self.game_controller.start_new_game(3, "Forest")

    def _resume_game(self, saved: dict):
        """Restores board state from DB save."""
        self.game_controller.restore_game(
            size=saved["difficulty"],
            theme=saved["theme"],
            board_state=saved["board_state"],
            moves=saved["moves"],
            elapsed_time=saved["elapsed_time"],
        )

    def _auto_save(self):
        user = SessionService.instance().get_user()
        gc = self.game_controller
        if not user or not gc.board_model or not gc.state.is_playing:
            return

        board_state = [t.id for t in gc.board_model.grid]
        total = gc.board_model.size ** 2 - 1
        correct = sum(
            1 for i, t in enumerate(gc.board_model.grid)
            if not t.is_empty and t.id == i
        )
        progress = int(correct / total * 100) if total else 0

        saved_game_repository.upsert(
            user_id=user.id,
            theme=self._ui_ctrl._current_theme,
            difficulty=self._ui_ctrl._current_size,
            moves=gc.state.moves_count,
            elapsed_time=gc.state.time_seconds,
            board_state=board_state,
            progress=progress,
        )

    def _refresh_best_score(self):
        user = SessionService.instance().get_user()
        if user and hasattr(self, '_ui_ctrl') and self._ui_ctrl:
            best = BestScoreService.get_best(
                user.id, self._ui_ctrl._current_size)
            self.stats_panel.update_best_score(best)

    def _on_logout(self):
        self.deactivate()
        SessionService.instance().logout()
        self._app_window.show_login()

    def _on_history(self):
        user = SessionService.instance().get_user()
        if user:
            from ui.dialogs.score_history_dialog import ScoreHistoryDialog
            ScoreHistoryDialog.show(self, user)

    # ── Expose alias for UIController ────────────────────
    @property
    def info_bar(self):
        return self.stats_panel

    def _load_styles(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "styles", "dark_theme.qss")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self._game_root.setStyleSheet(f.read())
