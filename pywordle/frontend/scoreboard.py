# Copyright (C) 2024 Dylan Middendorf
# This code is licensed under MIT license (see LICENSE for details)

"""This module provides several classes for building a Wordle scorboard."""
from typing import Sequence
from tkinter import Frame, Label, Misc
from constants import COLOR_MAP, TILE_EMPTY, TILE_UNKNOWN


class ScoreboardTile:
    """
    Represents a scoreboard tile for the Wordle game. Each tile holds a letter and associated
    state. The state must be one of the five recognized states (found in pywordle.constants):
        - TILE_EMPTY: Represents an empty tile.
        - TILE_UNKNOWN: Represents a tile with an unknown state.
        - TILE_ABSENT: Represents when the letter is not present.
        - TILE_PRESENT: Represents when the letter is present but not in the correct position.
        - TILE_CORRECT: Represents when the letter is present in the correct position.

    Attributes:
        - _frame (Frame): The frame containing the label for the tile.
        - _label (Label): The label displaying the letter on the tile.
        - _letter (str): The letter displayed on the tile.
        - _state (int): The state of the tile (e.g., empty, unknown, absent, etc.).

    Methods:
        - __init__(self, master): Initializes the ScoreboardTile instance.
        - update(self, letter, state): Updates the tile's letter and state.
        - letter(self): Returns the letter displayed on the tile.
        - state(self): Returns the state of the tile.
    """

    def __init__(self, master: Misc) -> None:
        """
        Initializes a ScoreboardTile instance.

        Parameters:
            - master (Misc): The parent widget where the tile will be placed.
        """
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
        Updates the tile's letter and state.

        Parameters:
            - letter (str): The letter to be displayed on the tile.
            - state (int): The state of the tile.

        Raises:
            - ValueError: If the letter or state is invalid.
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
            - str: The letter displayed on the tile.
        """
        return self._letter

    @property
    def state(self) -> int:
        """
        Returns the state of the tile.

        Returns:
            - int: The state of the tile.
        """
        return self._state


class ScoreboardRow:
    """
    Represents a row of scoreboard tiles for the Wordle game.

    Attributes:
        - _frame (Frame): The frame used to position the scoreboard tiles.
        - _tiles (list[ScoreboardTile]): A list containing the scoreboard tiles.

    Methods:
        - __init__(self, master): Initializes the ScoreboardTile instance.
        - update(self, letter, state): Updates the row's tiles with letters and their states.
        - letter(self): Returns the letter displayed on the tile.
        - state(self): Returns the state of the tile.
    """

    def __init__(self, master: Misc) -> None:
        """
        Initialize the ScoreboardRow.

        Parameters:
        - master (Misc): The parent widget where the scoreboard row will be placed.
        """
        self._frame = Frame(master, height=52.5, width=280)
        self._tiles = [ScoreboardTile(self._frame) for _ in range(5)]

        self._frame.grid_propagate(False)
        self._frame.columnconfigure(list(range(5)), weight=1)
        self._frame.grid()

    def update(self, letters: str, states: Sequence[int]) -> None:
        """
        Update the scoreboard row with letters and their states.

        Parameters:
        - letters (str): The letters to be displayed in the scoreboard row.
        - states (Sequence[int]): The states corresponding to the letters.
        """

        for idx, (letter, state) in enumerate(zip(letters, states)):
            self._tiles[idx].update(letter, state)

    def __getitem__(self, key: int) -> ScoreboardTile:
        """
        Retrieve a scoreboard tile by index.

        Parameters:
        - key (int): The index of the scoreboard tile to retrieve.

        Returns:
        - ScoreboardTile: The scoreboard tile at the specified index.
        """
        return self._tiles[key]


class Scoreboard:
    """
    Represents a 6x5 scoreboard used for displaying tiles within a Wordle game.

    Attributes:
        _frame (Frame): The frame containing the scoreboard.
        _rows (List[ScoreboardRow]): A list containing the scoreboard rows.
        _cursor (List[int]): Current cursor position represented as (x, y).
    """

    def __init__(self, master: Misc) -> None:
        """
        Initialize the Scoreboard.

        Parameters:
            master (Misc): The master widget (typically a Tkinter root or frame).
        """
        self._frame = Frame(master, height=340, width=280)
        self._rows = [ScoreboardRow(self._frame) for _ in range(6)]
        self._cursor = [0, 0]  # (x, y)

        self._frame.grid_propagate(False)
        self._frame.rowconfigure(list(range(6)), weight=1)
        self._frame.pack()

    def update_row(self, pattern: tuple[tuple[str, int]]) -> None:
        """
        Update the current scoreboard row with letters and their states.

        Parameters:
            - pattern (tuple[tuple[str, int]]): Pattern to update the row with. Each tuple contains
                a letter and an associated state.
        """
        for idx, (letter, state) in enumerate(pattern):
            self._rows[self._cursor[1]][idx].update(letter, state)

        self._cursor[0] = 0
        self._cursor[1] += 1

    def query(self, query: str):
        """
        Processes a single letter and updates a letter within the current row.

        Parameters:
            query (str): The letter to be processed.
        """
        if query.isalpha():
            self._rows[self._cursor[1]][self._cursor[0]].update(query, TILE_UNKNOWN)
            self._cursor[0] += 1
        elif query == "\b" and 0 < self._cursor[0]:
            self._cursor[0] -= 1
            self._rows[self._cursor[1]][self._cursor[0]].update()

    def __getitem__(self, key: int) -> ScoreboardRow:
        """
        Get the specified scoreboard row.

        Args:
            key (int): Index of the row to retrieve.

        Returns:
            ScoreboardRow: The specified scoreboard row.
        """
        return self._rows[key]
