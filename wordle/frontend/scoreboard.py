from frontend import *  # General constants
from tkinter import Frame, Label, Misc


class ScoreboardTile:

    def __init__(self, master: Misc) -> None:
        self._frame = Frame(master, height=52.5, width=52, borderwidth=2)
        self._label = Label(self._frame, font=("Libre Franklin", 32, "bold"))

        # Force fixed size for tile (52.5 x 52)
        self._frame.pack_propagate(False)

        # Initalize label/frame within master
        self._label.pack(fill="both")  # Fill tile area (48.5 x 48)
        self._frame.grid(column=len(master.children) - 1, row=0)

        self.update()  # Initalize text & color (state)

    def update(self, text: str = "", state: int = TILE_EMPTY) -> None:
        if len(text) > 1 or (len(text) == 1 and not text.isalpha()):
            raise ValueError(f"Invalid tile text ({text})")
        if len(text) == 0 and state != TILE_EMPTY:
            raise ValueError(f"Invalid tile state ({state})")
        if len(text) == 1 and state == TILE_EMPTY:
            raise ValueError(f"Invalid tile state ({state})")

        label_config = {
            "text": text.upper(),
            "bg": "white" if state <= TILE_UNKNOWN else COLOR_MAP[state],
            "fg": "black" if state == TILE_EMPTY else "white",
        }

        self._frame.configure(bg=COLOR_MAP[state])
        self._label.configure(label_config)


class ScoreboardRow:
    def __init__(self, master: Misc) -> None:
        self._frame = Frame(master, height=52.5, width=280)
        self._tiles = [ScoreboardTile(self._frame) for _ in range(5)]

        self._frame.grid_propagate(False)
        self._frame.columnconfigure(list(range(5)), weight=1)
        self._frame.grid()

    def __getitem__(self, key: int) -> ScoreboardTile:
        return self._tiles[key]


class Scoreboard:
    def __init__(self, master: Misc) -> None:
        self._frame = Frame(master, height=340, width=280)
        self._rows = [ScoreboardRow(self._frame) for _ in range(6)]

        self._frame.grid_propagate(False)
        self._frame.rowconfigure(list(range(6)), weight=1)
        self._frame.pack()

    def __getitem__(self, key: int) -> ScoreboardRow:
        return self._rows[key]
