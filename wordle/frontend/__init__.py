from typing import Callable
from tkinter import Tk

from constants import *
from .keyboard import Keyboard
from .scoreboard import Scoreboard


class Frontend:
    def __init__(self, query_handel: Callable[[str], None]) -> None:
        self._root = Tk()  # Render frontend
        self._root.geometry("500x550")
        self._scorebord = Scoreboard(self._root)
        self._keybord = Keyboard(self._root, query_handel)
        self._root.bind("<Key>", lambda e: query_handel(e.char.upper()))

    def update(
        self, pattern: tuple[tuple[str, int], ...] = None, key: str = None
    ) -> None:
        if pattern is None:
            self._scorebord.query(key)
        elif key is None:
            for k, s in pattern:
                self._keybord.upgrade(k, s)
            self._scorebord.update_row(pattern)

    def process_keypress(self, key: str) -> None:
        self._scorebord.query(key)

    def mainloop(self) -> None:
        self._root.mainloop()
