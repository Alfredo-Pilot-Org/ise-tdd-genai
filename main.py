# Re-export so callers can use: from main import make_change
from src.change_maker import make_change

__all__ = ["make_change"]
