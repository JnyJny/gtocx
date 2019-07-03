"""
"""

from pathlib import Path
from .star import Star

Stars = Star.from_csv(Path(__file__).parent /'data'/'stars.txt')

Sol = Stars.pop(0)

__all__ = [
    'Star',
    'Stars',
    'Sol',
]
