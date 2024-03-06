from __future__ import annotations

from tkinter import Canvas, Frame, Misc
from typing import Callable, Sequence

from PIL import Image  # Image import/load
from PIL.ImageTk import PhotoImage

from constants import COLOR_MAP, TILE_EMPTY, TILE_UNKNOWN, QUERTY_LAYOUT


class Key:
    def __init__(self, master: Misc, letter: str, func: Callable[[str], None]) -> None:
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

        self._canvas.move(
            6, self._width / 2, height / 2
        )  # Center the media on the canvas
        self.update()  # Update button color with correct state (empty)
        self._canvas.grid(column=len(master.children) - 1, row=0)
        self._canvas.bind("<Button-1>", lambda _: func(self._letter))

    def _shape(self, width: int, height: int, border_radius: int) -> None:
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

    def update(self, state: int = TILE_EMPTY) -> None:
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
        return self._letter

    @property
    def width(self) -> int:
        return self._width

    def upgrade(self, state: int = TILE_EMPTY) -> None:
        if self._state < state:
            self.update(state)


class KeyboardRow:
    def __init__(self, master: Misc, keys: str, func: Callable[[str], None]) -> None:
        self._frame = Frame(master, height=58, width=500)
        frame_width = 0  # Used to evenly space keys
        self._keys: list[Key] = []
        for idx, key in enumerate(keys):
            self._keys.append(Key(self._frame, key, func))
            frame_width += self._keys[idx].width + 6  # padding
        self._frame.grid_propagate(False)
        self._frame.config(width=frame_width)  # Used for key allignment
        self._frame.columnconfigure(list(range(len(keys))), weight=1)
        self._frame.grid()

    def __getitem__(self, key: int) -> Key:
        return self._keys[key]


class Keyboard:
    def __init__(self, master: Misc, handle: Callable[[str], None]) -> None:
        self._frame = Frame(master, height=198, width=490)
        self._rows = [KeyboardRow(self._frame, r, handle) for r in QUERTY_LAYOUT]
        self._mapping = self._load_mapping(QUERTY_LAYOUT)

        self._frame.grid_propagate(False)
        self._frame.rowconfigure(tuple(range(len(QUERTY_LAYOUT))), weight=1)
        self._frame.pack()  # Render frame within the master widget

    def update(self, letter: str, state: int) -> None:
        x, y = self._mapping[letter.upper()]
        self._rows[y][x].update(state)

    def __getitem__(self, key: int) -> KeyboardRow:
        return self._rows[key]

    @staticmethod
    def _load_mapping(layout: Sequence[str]) -> dict[str, tuple[int, int]]:
        """Returns a dictionary containing key-coordiante mappings."""
        mapping: dict[str, tuple[int, int]] = {}
        for y, row in enumerate(layout):
            mapping.update({k: (x, y) for x, k in enumerate(row)})
        return mapping
