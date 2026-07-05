class GameError(Exception):
    """Base class for game exceptions"""
    pass

class InvalidMoveError(GameError):
    """Raised when an illegal move is attempted"""
    pass

class ImageLoadError(GameError):
    """Raised when an image fails to load"""
    pass
