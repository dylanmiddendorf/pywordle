"""This module provides several classes for building a virtual keyboard."""

from __future__ import annotations

from tkinter import Canvas, Frame, Misc
from typing import Callable, Sequence

from PIL import Image  # Image import/load
from PIL.ImageTk import PhotoImage

from constants import COLOR_MAP, TILE_EMPTY, TILE_UNKNOWN, QUERTY_LAYOUT


class Key:
    """
    Represents a key on a keyboard.

    Attributes:
        - _canvas (Canvas): The canvas widget where the key is drawn.
        - _letter (str): The letter displayed on the key.
        - _state (int): The current state of the key.
        - _width (int): The width of the key button, in pixels.
        - _backspace (PhotoImage): The image for the backspace key.
    """

    def __init__(self, master: Misc, letter: str, handle: Callable[[str], None]) -> None:
        """
        Initializes a Key object.

        Args:
            master (Misc): The parent widget where the key will be placed.
            letter (str): The letter to be displayed on the key.
            handle (Callable[[str], None]): The function to be called when the key is clicked.

        Raises:
            TypeError: If the master widget is not supported.
            ValueError: If the key does not contain a singular alphabetic character.
        """
        if master is None or issubclass(Misc, type(master)):
            raise TypeError(f"{type(master)} is not supported, try using a widget")
        if letter is None or len(letter) != 1:
            raise ValueError("The key must contain a singular alphabetic character")

        self._canvas = Canvas(master, highlightthickness=0)
        self._letter = letter.upper()  # Force letter to uppercase
        self._state = -1  # For updates/upgrades
        self._width = 42 if letter.isalpha() else 65

        height, radius = 57, 4  # height and radius respectively
        self._shape(self._width, height, radius)  # Build the button on the canvas

        if letter.isalpha():
            font = ("Libre Franklin", 20, "bold")
            self._canvas.create_text(0, 0, font=font, text=letter)
        elif letter == "\r":
            font = ("Libre Franklin", 12, "bold")
            self._canvas.create_text(0, 0, font=font, text="ENTER")
        elif letter == "\b":
            # !!! MUST ASSIGN IMAGE AS ATTRIBUTE !!!
            path = "data/backspace.png"  # Filepath for backspace icon
            self._backspace = PhotoImage(Image.open(path).resize((20, 20)))
            self._canvas.create_image(0, 0, image=self._backspace)
        else:
            escaped_letter = self._letter.encode("unicode_escape").decode("utf-8")
            raise ValueError(f"{escaped_letter} is not currently supported")

        self._canvas.move(6, self._width / 2, height / 2)  # Center the media
        self.update()  # Update button color with correct state (empty)
        self._canvas.grid(column=len(master.children) - 1, row=0)
        self._canvas.bind("<Button-1>", lambda _: handle(self._letter))

    def update(self, state: int = TILE_EMPTY) -> None:
        """
        Updates the state of the key.

        Args:
            state (int, optional): The new state of the key. Defaults to TILE_EMPTY.
        """
        if self._state == state:
            return  # Cache previous tile state for performance

        # Key's only contain 4 states (empty, absent, preset, ...)
        state = TILE_EMPTY if state == TILE_UNKNOWN else state
        bg_color = COLOR_MAP[state]  # Based on tile color map
        fg_color = "black" if state == TILE_EMPTY else "white"

        for item in range(1, 6):  # One-based indexing
            self._canvas.itemconfig(item, fill=bg_color, outline=bg_color)
        if self._letter.isalpha() or self._letter == "\n":
            self._canvas.itemconfig(6, fill=fg_color)  # Update text

    @property
    def letter(self) -> str:
        """
        Returns the letter displayed on the key.

        Returns:
            - str: The letter displayed on the key.
        """
        return self._letter

    @property
    def state(self) -> int:
        """
        Returns the state of the key.

        Returns:
            - int: The state of the key.
        """
        return self._state

    @property
    def width(self) -> int:
        """
        Returns the width of the key.

        Returns:
            - int: The width of the key.
        """
        return self._width

    def _shape(self, width: int, height: int, border_radius: int) -> None:
        """
        Shapes the key button on the canvas.

        Args:
            - width (int): The width of the key.
            - height (int): The height of the key.
            - border_radius (int): The radius of the key's borders.
        """
        w, h, r = width, height, border_radius  # Increase readability
        self._canvas.configure(width=w + 1, height=h + 1)

        # Construct polygon w/ chamfered corners
        north_edge, east_edge = (r, 0, w - r, 0), (w, r, w, h - r)
        south_edge, west_edge = (w - r, h, r, h), (0, h - r, 0, r)
        self._canvas.create_polygon(north_edge + east_edge + south_edge + west_edge)

        # Construct remaining corners with arcs
        self._canvas.create_arc((w - (r * 2), 0, w, (r * 2)), start=0, extent=90)
        self._canvas.create_arc((0, (r * 2), (r * 2), 0), start=90, extent=90)
        self._canvas.create_arc((0, h - (r * 2), (r * 2), h), start=180, extent=90)
        self._canvas.create_arc((w, h - (r * 2), w - (r * 2), h), start=270, extent=90)


class KeyboardRow:
    """
    Represents a row of keys on a keyboard.

    Attributes:
        - _frame (Frame): The frame containing the keys of the row.
        - _keys (list[Key]): List of Key objects representing the keys in the row.

    Methods:
        - __init__: Initializes a KeyboardRow object.
        - __getitem__: Retrieves a key from the row by index.
    """

    def __init__(self, master: Misc, keys: str, handle: Callable[[str], None]) -> None:
        """
        Initializes a KeyboardRow object.

        Args:
            - master (Misc): The master widget for the keyboard row.
            - keys (str): The keys to be displayed in the row.
            - handle (Callable[[str], None]): The function to be called when a key is pressed.
        """

        self._frame = Frame(master, height=58)
        self._width = 0  # Used to evenly space keys
        self._keys: list[Key] = []
        for idx, key in enumerate(keys):
            self._keys.append(Key(self._frame, key, handle))
            self._width += self._keys[idx].width + 6  # padding
        self._frame.grid_propagate(False)
        self._frame.config(width=self._width)  # Used for key allignment
        self._frame.columnconfigure(list(range(len(keys))), weight=1)
        self._frame.grid()

    @property
    def width(self) -> int:
        """
        Returns the width of the keyboard row.

        Returns:
            - int: The width of the keyboard.
        """
        return self._width

    def __getitem__(self, key: int) -> Key:
        """
        Retrieves a key from the row by index.

        Args:
        - key (int): The index of the key to retrieve.

        Returns:
        - Key: The Key object at the specified index.
        """
        return self._keys[key]


class Keyboard:
    """
    Represents a virtual keyboard.

    Attributes:
        - _frame (Frame): The frame containing the keyboard.
        - _rows (list[KeyboardRow]): List of KeyboardRow objects representing rows in the keyboard.
        - _mapping (dict): Dictionary containing key-coordinate mappings.

    Methods:
        - __init__: Initializes a Keyboard object.
        - update: Updates the state of a key on the keyboard.
        - upgrade: Upgrades the state of a key on the keyboard.
        - __getitem__: Retrieves a key from the keyboard by coordinates or letter.
        - _load_mapping: Loads key-coordinate mappings for the keyboard layout.
    """

    def __init__(self, master: Misc, handle: Callable[[str], None]) -> None:
        """
        Initializes a Keyboard object.

        Args:
            - master (Misc): The master widget for the keyboard.
            - handle (Callable[[str], None]): The function to handle key press events.
        """
        self._frame = Frame(master, height=198, width=490)
        self._rows = [KeyboardRow(self._frame, r, handle) for r in QUERTY_LAYOUT]
        self._mapping = self._load_mapping(QUERTY_LAYOUT)

        self._frame.grid_propagate(False)
        self._frame.rowconfigure(tuple(range(len(QUERTY_LAYOUT))), weight=1)
        self._frame.pack()  # Render frame within the master widget

    def update(self, letter: str, state: int) -> None:
        """
        Updates the state of a key on the keyboard.

        Args:
            - letter (str): The letter representing the key.
            - state (int): The state to update the key to.
        """
        x, y = self._mapping[letter.upper()]
        self._rows[y][x].update(state)

    def upgrade(self, letter: str, state: int) -> None:
        """
        Upgrades the state of a key on the keyboard if the new state is higher.

        Args:
            - letter (str): The letter representing the key.
            - state (int): The state to upgrade the key to.
        """
        if state > self[letter].state:
            self[letter].update(state)

    def __getitem__(self, key: tuple[int, int] | str) -> Key:
        """
        Retrieves a key from the keyboard by coordinates or letter.

        Args:
            - key (tuple[int, int] | str): The coordinates or letter of the key.

        Returns:
            - Key: The Key object representing the key.
        """
        if not isinstance(key, (tuple, str)):
            raise TypeError(f"{type(key)} is not supported.")
        
        # Unpack the key's coordinates
        x, y = key if isinstance(key, tuple) else self._mapping[key.upper()]
        return self._rows[y][x]
        
        

    @staticmethod
    def _load_mapping(layout: Sequence[str]) -> dict[str, tuple[int, int]]:
        """
        Loads key-coordinate mappings for the keyboard layout.

        Args:
            - layout (Sequence[str]): The layout of the keyboard.

        Returns:
            - dict[str, tuple[int, int]]: The dictionary containing key-coordinate mappings.
        """
        mapping: dict[str, tuple[int, int]] = {}
        for y, row in enumerate(layout):
            mapping.update({k: (x, y) for x, k in enumerate(row)})
        return mapping
