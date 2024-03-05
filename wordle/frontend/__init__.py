from .keyboard import Keyboard
from .scoreboard import Scoreboard

from typing import Callable
from tkinter import Tk

TILE_EMPTY = 0
TILE_UNKNOWN = 1
TILE_ABSENT = 2
TILE_PRESENT = 3
TILE_CORRECT = 4

COLOR_MAP = {
    TILE_EMPTY: "#d3d6da",
    TILE_UNKNOWN: "#878a8c",
    TILE_ABSENT: "#787c7e",
    TILE_PRESENT: "#c9b458",
    TILE_CORRECT: "#6aaa64",
}

QUERTY_LAYOUT = ["QWERTYUIOP", "ASDFGHJKL", "\nZXCVBNM\b"]


class Frontend:
    def __init__(self, query_handel: Callable[[str], None]) -> None:
        self._root = Tk()  # Render frontend
        self._root.geometry("500x550")
        self._scorebord = Scoreboard(self._root)
        self._keybord = Keyboard(self._root, query_handel)
        self._root.bind("<Key>", lambda e: query_handel(e.char.upper()))

    def update(self, pattern: tuple[tuple[str, int], ...] = None, key: str = None) -> None:
        if pattern is None:
            return self._scorebord.query(key)
        elif key is None:
            for key, state in pattern:
                self._keybord.upgrade(key, state)
            self._scorebord.update_row(pattern)
    
    def process_keypress(self, key: str) -> None:
        self._scorebord.query(key)
        

    def mainloop(self) -> None:
        self._root.mainloop()
