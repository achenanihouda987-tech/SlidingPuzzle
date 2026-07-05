import os
from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import Qt

from ui.widgets.control_panel_widget import ControlPanelWidget
from ui.widgets.stats_panel_widget import StatsPanelWidget
from ui.widgets.board_widget import BoardWidget
from ui.widgets.preview_panel_widget import PreviewPanelWidget
from ui.widgets.bottom_bar_widget import BottomBarWidget
from ui.layouts.main_layout import MainLayout
from controllers.game_controller import GameController
from controllers.ui_controller import UIController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sliding Puzzle")
        self.setMinimumSize(1100, 800)

        self._load_styles()
        self._setup_widgets()

        self.game_controller = GameController()
        self.ui_controller = UIController(self, self.game_controller)
        self.game_controller.start_new_game(3, "Forest")

    def _setup_widgets(self):
        root = QWidget(self)
        root.setObjectName("rootBg")
        self.setCentralWidget(root)

        self.control_panel  = ControlPanelWidget()
        self.stats_panel    = StatsPanelWidget()
        self.board_widget   = BoardWidget()
        self.preview_widget = PreviewPanelWidget()
        self.bottom_bar     = BottomBarWidget()

        self.main_layout = MainLayout(
            root,
            self.control_panel,
            self.stats_panel,
            self.board_widget,
            self.preview_widget,
            self.bottom_bar,
        )

    @property
    def info_bar(self):
        """Alias used by UIController for stat updates."""
        return self.stats_panel

    def _load_styles(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "styles", "dark_theme.qss")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
