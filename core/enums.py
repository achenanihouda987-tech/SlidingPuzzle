from enum import Enum

class Difficulty(Enum):
    EASY = 3    # 3x3
    MEDIUM = 4  # 4x4
    HARD = 5    # 5x5

class ImageStyle(Enum):
    GRADIENT = "Gradient"
    SUNSET = "Sunset"
    FOREST = "Forest"
    CUSTOM = "Custom"
