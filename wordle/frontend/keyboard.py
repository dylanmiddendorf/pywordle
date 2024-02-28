from frontend import *
from tkinter import Canvas, Frame, Misc
from PIL import Image  # Image import/load
from PIL.ImageTk import PhotoImage
class Key:
    # 4px
    def __init__(self, master: Misc, letter: str) -> None:
        self._canvas = Canvas(master, highlightthickness=0)
        w, h, r = 42, 57, 4  # Slightly abstract magic numbers
        letter = letter.upper()  # Force letter to uppercase

        # Build the button and render the specified letter
        self._shape(w, h, r)  # Build the button on the canvas
        self._canvas.create_text(0, 0, font=("Libre Franklin", 20, "bold"), text=letter)
        self._canvas.move(6, w / 2, h / 2)  # Update letter offsets
        self.update()  # Update button color with correct state (empty)
        self._canvas.grid(column=len(master.children) - 1, row=0)

    def _shape(self, width: int, height: int, border_radius: int) -> None:
        w, h, r = width, height, border_radius  # Increase readability
        self._canvas.configure(width=w + 1, height=h + 1)

        # Construct polygon w/ chamfered corners
        north_east = (r, 0, w - r, 0, w, r, w, h - r)
        south_west = (w - r, h, r, h, 0, h - r, 0, r)
        self._canvas.create_polygon(north_east + south_west)

        # Construct remaining corners with arcs
        self._canvas.create_arc((w - (r * 2), 0, w, (r * 2)), start=0, extent=90)
        self._canvas.create_arc((0, (r * 2), (r * 2), 0), start=90, extent=90)
        self._canvas.create_arc((0, h - (r * 2), (r * 2), h), start=180, extent=90)
        self._canvas.create_arc((w, h - (r * 2), w - (r * 2), h), start=270, extent=90)

    def update(self, state: int = TILE_EMPTY) -> None:
        # Key's only contain 4 states (empty, absent, preset, ...)
        state = TILE_EMPTY if state == TILE_UNKNOWN else state
        bg_color = COLOR_MAP[state]  # Based on tile color map
        fg_color = "black" if state == TILE_EMPTY else "white"

        for id in range(1, 6):  # One-based indexing
            self._canvas.itemconfig(id, fill=bg_color, outline=bg_color)
        self._canvas.itemconfig(6, fill=fg_color)  # Update text


class WideKey(Key):
    def __init__(self, master: Misc, media: str | PhotoImage) -> None:
        self._canvas = Canvas(master, highlightthickness=0)
        w, h, r = 65, 57, 4  # Slightly abstract magic numbers

        # Build the button and render the specified text/icon
        self._shape(w, h, r)  # Build the button on the canvas

        if type(media) is str:
            font = ("Libre Franklin", 12, "bold")  # Similar to NYT Franklin
            self._canvas.create_text(0, 0, font=font, text=media.upper())
        elif type(media) is PhotoImage:
            self._canvas.create_image(0, 0, image=media)
        self._canvas.move(6, w / 2, h / 2)  # Update text offsets

        bg_color = COLOR_MAP[TILE_EMPTY]
        for id in range(1, 6):  # One-based indexing
            self._canvas.itemconfig(id, fill=bg_color, outline=bg_color)
        self._canvas.grid(column=len(master.children) - 1, row=0)


class KeyboardRow:
    def __init__(self, master: Misc, keys: str) -> None:
        self._frame = Frame(master, height=58, width=500)
        frame_width = 0 # Used to evenly space keys
        self._keys: list[Key] = []
        for key in keys:
            if key == "\n":
                self._keys.append(WideKey(self._frame, "ENTER"))
                frame_width += 71 # 65 (width) + 6 (padding)
            elif key == "\b":
                # !!! MUST ASSIGN IMAGE AS ATTRIBUTE !!!
                path = 'data/backspace.png' # Filepath for backspace icon
                self._backspace = PhotoImage(Image.open(path).resize((20, 20)))
                self._keys.append(WideKey(self._frame, self._backspace))
                frame_width += 71 # 65 (width) + 6 (padding)
            else:
                self._keys.append(Key(self._frame, key))
                frame_width += 49 # 43 (width) + 6 (padding)

        self._frame.grid_propagate(False)
        self._frame.config(width=frame_width) # Used for key allignment
        self._frame.columnconfigure(list(range(len(keys))), weight=1)
        self._frame.grid()

    def __getitem__(self, key: int) -> Key:
        return self._keys[key]


class Keyboard:
    def __init__(self, master: Misc) -> None:
        self._frame = Frame(master, height=198, width=490)
        self._rows = [KeyboardRow(self._frame, r) for r in QUERTY_LAYOUT]

        self._frame.grid_propagate(False)
        self._frame.rowconfigure(list(range(len(QUERTY_LAYOUT))), weight=1)
        self._frame.pack()

    def __getitem__(self, key: int) -> KeyboardRow:
        return self._rows[key]
