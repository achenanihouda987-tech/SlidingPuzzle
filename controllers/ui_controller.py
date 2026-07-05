from PySide6.QtCore import QObject

from controllers.game_controller import GameController
from services.session_service import SessionService
from services.best_score_service import BestScoreService
from database import saved_game_repository


class UIController(QObject):
    """
    Bridges the UI events to game logic and back.
    Handles the full victory flow: auto-save score, show Victory dialog,
    update best score card, show VIEW SCORE button.
    """

    def __init__(self, game_page, game_controller: GameController):
        super().__init__()
        self._page = game_page
        self.game  = game_controller

        # Track current game metadata
        self._current_size  = 3
        self._current_theme = "Forest"

        # UI → Game
        self._page.control_panel.new_game_requested.connect(self._handle_new_game)
        self._page.control_panel.reshuffle_requested.connect(self._handle_reshuffle)
        self._page.board_widget.tile_clicked.connect(self.game.handle_tile_click)

        # Game → UI
        self.game.state_changed.connect(self._on_state_changed)
        self.game.board_updated.connect(self._on_board_updated)
        self.game.image_updated.connect(self._on_image_updated)
        self.game.puzzle_solved.connect(self._on_puzzle_solved)
        self.game.victory_achieved.connect(self._on_victory)

        # Board Widget buttons
        self._page.board_widget.view_score_clicked.connect(self._show_score)
        
        # Control Panel buttons
        self._page.control_panel.finish_clicked.connect(self._on_finish_clicked)

        # Store victory stats for score dialog
        self._last_moves   = 0
        self._last_seconds = 0
        self._last_score   = 0

    # ── Handlers: UI → Game ───────────────────────────────
    def _handle_new_game(self, size: int, theme: str, custom_path: str):
        self._current_size  = size
        self._current_theme = theme
        self._page.board_widget.show_score_button(False)
        self._page.control_panel.reset_finish_button()

        # Delete any existing save when starting fresh
        user = SessionService.instance().get_user()
        if user:
            saved_game_repository.delete(user.id)

        try:
            self.game.start_new_game(size, theme, custom_path or None)
        except Exception as e:
            from ui.dialogs.error_dialog import ErrorDialog
            ErrorDialog.show(self._page, str(e))

    def _handle_reshuffle(self):
        self._page.board_widget.show_score_button(False)
        self._page.control_panel.reset_finish_button()
        user = SessionService.instance().get_user()
        if user:
            saved_game_repository.delete(user.id)
        self.game.reshuffle_current()

    # ── Handlers: Game → UI ───────────────────────────────
    def _on_state_changed(self, state):
        self._page.stats_panel.update_moves(state.moves_count)
        self._page.stats_panel.update_time(state.time_seconds)

        if state.is_playing:
            self._page.board_widget.show_score_button(False)

        if self.game.board_model:
            total   = self.game.board_model.size ** 2 - 1
            correct = sum(
                1 for i, t in enumerate(self.game.board_model.grid)
                if not t.is_empty and t.id == i
            )
            pct = int(correct / total * 100) if total else 0
            self._page.preview_widget.set_progress(pct)

    def _on_board_updated(self):
        if self.game.board_model and self.game.current_pixmap:
            self._page.board_widget.render_board(
                self.game.board_model, self.game.current_pixmap)

    def _on_image_updated(self, pixmap):
        self._page.preview_widget.set_image(
            pixmap, self._current_size, self._current_theme)

    def _on_puzzle_solved(self):
        self._page.control_panel.btn_finish.setEnabled(True)

    def _on_finish_clicked(self):
        self._page.control_panel.btn_finish.setEnabled(False)
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self._page, "Success", "🎉 Puzzle Completed!")
        self.game.finish_game()

    def _on_victory(self, moves: int, seconds: int):
        """Full victory flow: show dialog → wait for save click."""
        user = SessionService.instance().get_user()
        if user:
            # Delete auto-save (game is finished)
            saved_game_repository.delete(user.id)

        self._last_moves   = moves
        self._last_seconds = seconds
        self._last_score   = BestScoreService.calculate_score(moves, seconds, self._current_size)

        # Show victory popup automatically
        from ui.dialogs.victory_dialog import VictoryDialog
        dlg = VictoryDialog(self._page, moves, seconds, self._current_size, self._current_theme)
        
        dlg.save_score_requested.connect(lambda: self._handle_save_score(dlg))
        
        dlg.play_again_requested.connect(
            lambda: self._handle_new_game(
                self._current_size, self._current_theme, ""))
        dlg.exec()

        # Show VIEW SCORE button below board
        self._page.board_widget.show_score_button(True)

    def _handle_save_score(self, dlg):
        """Called when user clicks SAVE AS BEST SCORE in victory dialog."""
        user = SessionService.instance().get_user()
        if user:
            score, is_record = BestScoreService.save_if_record(
                user.id, self._current_theme, self._current_size, self._last_moves, self._last_seconds)
            
            # Update best score card
            best = BestScoreService.get_best(user.id, self._current_size)
            self._page.stats_panel.update_best_score(best)
            
            # Refresh profile bar stats
            self._page.profile_bar.refresh(user)
            
            dlg.show_success()

    def _show_score(self):
        from ui.dialogs.score_dialog import ScoreDialog
        ScoreDialog.show(
            self._page,
            self._last_moves,
            self._last_seconds,
            self._current_size,
            self._last_score,
        )

    def _show_help(self):
        from ui.dialogs.help_dialog import HelpDialog
        HelpDialog.show(self._page)
