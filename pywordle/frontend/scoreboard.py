# Copyright (C) 2024 Dylan Middendorf
# This code is licensed under MIT license (see LICENSE for details)

"""This module provides several classes for building a Wordle scorboard."""
from typing import Sequence
from tkinter import Frame, Label, Misc
from constants import COLOR_MAP, TILE_EMPTY, TILE_UNKNOWN


class ScoreboardTile:
    """
    Represents a tile on the Wordle scoreboard, which can hold a letter and be
    in one of the following states:

    - TILE_EMPTY: Represents an empty tile.
    - TILE_UNKNOWN: Represents a tile with an unknown state.
    - TILE_ABSENT: Represents when the letter is not present.
    - TILE_PRESENT: Represents when the letter is present but not in the correct position.
    - TILE_CORRECT: Represents when the letter is present in the correct position.

    Attributes:
        letter (str): The letter displayed on the tile.
        state (int): The current state of the tile, can be one of the predefined states.

    Methods:
        update(self, letter: int = "", state: int = TILE_EMPTY) -> None: Updates the letter
        and state of the Tile.
    """

    def __init__(self, master: Misc) -> None:
        self._frame = Frame(master, height=52, width=52, borderwidth=2)
        self._label = Label(self._frame, font=("Libre Franklin", 32, "bold"))

        # Force fixed size for tile (52.5 x 52)
        self._frame.pack_propagate(False)

        # Initalize label/frame within master
        self._label.pack(fill="both")  # Fill tile area (48.5 x 48)
        self._frame.grid(column=len(master.children) - 1, row=0)

        self._letter, self._state = "", -1
        self.update()  # Initalize text & color (state)

    def update(self, letter: str = "", state: int = TILE_EMPTY) -> None:
        """
        Updates the letter and state of the tile.

        Args:
            letter (str): The letter to be displayed on the tile.
            state (int): The state to set the tile to. It must be one of the predefined states.
        """
        if letter == self._letter and state == self._state:
            return  # Prevent unecessary updates (when possible)
        if len(letter) > 1 or (len(letter) == 1 and not letter.isalpha()):
            raise ValueError(f"Invalid tile text ({letter})")
        if len(letter) == 0 and state != TILE_EMPTY:
            raise ValueError(f"Invalid tile state ({state})")
        if len(letter) == 1 and state == TILE_EMPTY:
            raise ValueError(f"Invalid tile state ({state})")

        label_config = {
            "text": letter.upper(),
            "bg": "white" if state <= TILE_UNKNOWN else COLOR_MAP[state],
            "fg": "black" if state <= TILE_UNKNOWN else "white",
        }

        self._frame.configure(bg=COLOR_MAP[state])
        self._label.configure(label_config)

    @property
    def letter(self) -> str:
        """
        Returns the letter displayed on the tile.

        Returns:
            str: The letter displayed on the tile.
        """
        return self._letter

    @property
    def state(self) -> int:
        """
        Returns the current state of the tile.

        Returns:
            int: The current state of the tile.
        """
        return self._state


class ScoreboardRow:
    """Represents a row of tiles on the Wordle scoreboard."""

    def __init__(self, master: Misc) -> None:
        self._frame = Frame(master, height=52.5, width=280)
        self._tiles = [ScoreboardTile(self._frame) for _ in range(5)]

        self._frame.grid_propagate(False)
        self._frame.columnconfigure(list(range(5)), weight=1)
        self._frame.grid()

    def update(self, letters: str, states: Sequence[int]) -> None:
        """
        Updates the letters and states of the tiles within the row.

        Args:
            letters (str): The letters to be displayed throughout the row.
            states (Sequence[int]): The states to set the tiles to.
        """

        for idx, (letter, state) in enumerate(zip(letters, states)):
            self._tiles[idx].update(letter, state)

    def __getitem__(self, key: int) -> ScoreboardTile:
        return self._tiles[key]


class Scoreboard:
    """Represents a 6x5 scoreboard used for displaying tiles within a Wordle game."""

    def __init__(self, master: Misc) -> None:
        self._frame = Frame(master, height=340, width=280)
        self._rows = [ScoreboardRow(self._frame) for _ in range(6)]
        self._cursor = [0, 0]  # (x, y)

        self._frame.grid_propagate(False)
        self._frame.rowconfigure(list(range(6)), weight=1)
        self._frame.pack()

    def update_row(self, pattern: tuple[tuple[str, int]]):
        """Updates a row with a specified pattern."""
        for idx, (letter, state) in enumerate(pattern):
            self._rows[self._cursor[1]][idx].update(letter, state)

        self._cursor[0] = 0
        self._cursor[1] += 1

    def query(self, query: str):
        """Processes a single letter, and updates a letter within the current row."""
        if query.isalpha():
            self._rows[self._cursor[1]][self._cursor[0]].update(query, TILE_UNKNOWN)
            self._cursor[0] += 1
        elif query == "\b" and 0 < self._cursor[0]:
            self._cursor[0] -= 1
            self._rows[self._cursor[1]][self._cursor[0]].update()

    def __getitem__(self, key: int) -> ScoreboardRow:
        return self._rows[key]
