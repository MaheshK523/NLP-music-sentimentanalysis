class MusicEmotionError(Exception):
    """Base exception for expected, user-facing failures."""


class DataValidationError(MusicEmotionError):
    """Raised when an input or result dataset violates the documented schema."""


class BackendUnavailableError(MusicEmotionError):
    """Raised when an explicitly requested optional backend cannot be loaded."""
