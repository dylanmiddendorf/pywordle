import itertools
import json
from datetime import date
from typing import Callable, Generator

# Project libraries
from frontend import Frontend, TILE_UNKNOWN, TILE_ABSENT, TILE_PRESENT, TILE_CORRECT

# External libraries
import numpy as np
import requests


class Backend:
    def __init__(self) -> None:
        self._solution = self._load_solution()
        self._buffer, self._cursor = bytearray(b"?????"), 0
        self._guesses = 0  # Current guess count
        self._frontend = Frontend(self.query)

    def set_update_handle(self, func: Callable[[tuple[tuple[str, int]]], None] = None) -> None:
        # Prevent null pointer exceptions by wrapping `func` in a lambda
        self._update_handle = (lambda x: None) if func is None else func
        

    def query(self, request: str) -> None:
        
        if not isinstance(request, str) or len(request) != 1:
            raise ValueError("Requests must be a single character")

        if request.isalpha() and self._cursor < len(self._buffer):
            self._buffer[self._cursor] = ord(request)
            self._cursor += 1  # Update cursor position
            self._frontend.update(key=request)
        elif request == "\b":
            self._cursor -= 1  # Simulate backspace
            self._frontend.update(key=request)
        elif request == "\r":
            self._frontend.update(self._pattern())
            self._cursor = 0  # Simulate `CR LF``
            self._guesses += 1  # Register guess
    
    def mainloop(self) -> None:
        self._frontend.mainloop()

    def _pattern(self) -> tuple[tuple[str, int]]:
        # Shift all strings/results to numpy for faster analysis
        guess = np.array(self._buffer, np.uint8) # bytebuffer
        solution = np.array([ord(c) for c in self._solution], np.uint8)
        print(guess, solution)
        pattern = np.array([TILE_ABSENT] * 5, np.uint8)

        # Update all correct tiles in pattern
        correct_tiles = guess == solution
        pattern[correct_tiles] = TILE_CORRECT

        # Remove correct tiles from future analysis
        equality_grid = np.equal.outer(guess, solution)
        equality_grid[:, correct_tiles] = False
        equality_grid[correct_tiles, :] = False

        # Update all exact matches within the guess
        for i, j in itertools.product(range(5), range(5)):
            if equality_grid[i][j]:
                pattern[i] = TILE_PRESENT  # Found unaligned tile...
                equality_grid[i, :], equality_grid[:, j] = False, False
        
        return tuple(zip(self._buffer.decode(), tuple(pattern.tolist())))

    @staticmethod
    def _load_solution() -> str:
        endpoint = f"https://www.nytimes.com/svc/wordle/v2/{date.today().strftime('%Y-%m-%d')}.json"
        assert (response := requests.get(endpoint, timeout=3)).ok
        return json.loads(response.text)["solution"].upper()  # Return the solution
