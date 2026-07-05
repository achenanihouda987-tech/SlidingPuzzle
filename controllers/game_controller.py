from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap

from models.game_state import GameState
from models.board_model import BoardModel
from models.tile_model import TileModel
from services.board_service import BoardService
from services.movement_service import MovementService
from services.shuffle_service import ShuffleService
from services.victory_service import VictoryService
from services.timer_service import TimerService
from services.image_service import ImageService


class GameController(QObject):
    """
    Orchestrates the entire game flow.
    Supports fresh starts and board-state restoration from a saved game.
    """
    state_changed   = Signal(object)   # GameState
    board_updated   = Signal()
    puzzle_solved   = Signal()         # Emitted when board is in correct order
    victory_achieved = Signal(int, int) # Emitted when user clicks Finish Game
    image_updated   = Signal(QPixmap)

    def __init__(self):
        super().__init__()
        self.state          = GameState()
        self.board_model    = None
        self.current_pixmap = None
        self.tile_size      = 120

        self.timer_service = TimerService(self)
        self.timer_service.tick.connect(self._on_timer_tick)

    # ── New game ──────────────────────────────────────────
    def start_new_game(self, size: int, style: str, custom_path: str = None):
        total_size = size * self.tile_size
        try:
            if custom_path:
                self.current_pixmap = ImageService.load_image(custom_path, total_size)
            else:
                self.current_pixmap = ImageService.load_builtin_image(style, total_size)

            self.image_updated.emit(self.current_pixmap)

            self.board_model = BoardService.create_board(size)
            ShuffleService.shuffle(self.board_model, num_moves=400 + size * 50)

            self.state.reset()
            self.timer_service.start()

            from database.user_repository import increment_games_played
            from services.session_service import SessionService
            user = SessionService.instance().get_user()
            if user:
                increment_games_played(user.id)

            self.state_changed.emit(self.state)
            self.board_updated.emit()
        except Exception:
            raise

    # ── Restore from saved game ───────────────────────────
    def restore_game(self, size: int, theme: str, board_state: list,
                     moves: int, elapsed_time: int, custom_path: str = None):
        """Re-creates board from a persisted tile-ID list."""
        total_size = size * self.tile_size
        try:
            if custom_path:
                self.current_pixmap = ImageService.load_image(custom_path, total_size)
            else:
                self.current_pixmap = ImageService.load_builtin_image(theme, total_size)
            self.image_updated.emit(self.current_pixmap)
        except Exception:
            # Fallback: start fresh if image is unavailable
            self.start_new_game(size, theme)
            return

        # Rebuild board from state list
        self.board_model = BoardModel(size)
        self.board_model.grid.clear()
        self.board_model.tile_positions = [0] * (size * size)

        for pos_idx, tile_id in enumerate(board_state):
            is_empty = (tile_id == self.board_model.empty_tile_id)
            tile = TileModel(id=tile_id, is_empty=is_empty)
            self.board_model.grid.append(tile)
            self.board_model.tile_positions[tile_id] = pos_idx

        # Restore state
        self.state.reset()
        self.state.moves_count  = moves
        self.state.time_seconds = elapsed_time
        self.timer_service.start()

        self.state_changed.emit(self.state)
        self.board_updated.emit()

    # ── Reshuffle ─────────────────────────────────────────
    def reshuffle_current(self):
        if not self.board_model:
            return
        ShuffleService.shuffle(self.board_model,
                               num_moves=400 + self.board_model.size * 50)
        self.state.reset()
        self.timer_service.start()
        self.state_changed.emit(self.state)
        self.board_updated.emit()

    # ── Tile click ────────────────────────────────────────
    def handle_tile_click(self, board_idx: int):
        if not self.state.is_playing:
            return

        move = MovementService.move(self.board_model, board_idx)
        if move:
            self.state.add_move(move)
            self.state_changed.emit(self.state)
            self.board_updated.emit()

            if VictoryService.check_victory(self.board_model):
                self.state.stop()
                self.timer_service.stop()
                self.state_changed.emit(self.state)
                self.puzzle_solved.emit()

    def finish_game(self):
        """Called when user clicks the Finish Game button."""
        self.victory_achieved.emit(self.state.moves_count, self.state.time_seconds)

    def _on_timer_tick(self):
        self.state.tick_time()
        self.state_changed.emit(self.state)
