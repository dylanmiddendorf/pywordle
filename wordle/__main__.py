import itertools
import json
from datetime import date
from typing import cast

# Project/External libraries
from frontend import Frontend, TILE_ABSENT, TILE_PRESENT, TILE_CORRECT
import numpy as np
import requests


class Wordle:
    def __init__(self) -> None:
        self._solution = self._load_solution()
        self._buffer = bytearray(b"?????")
        self._index, self._guesses = 0, 0
        self._frontend = Frontend(self.query)
        self._dictionary = self._load_dictionary()
        self.has_won = False

    def query(self, request: str) -> None:
        if not isinstance(request, str) or len(request) != 1:
            raise ValueError("Requests must be a single character")
        if self._guesses == 6 or self.has_won:
            print("Please come back tommorow!")
            return  # Don't allow player to continue playing

        if request.isalpha() and self._index < len(self._buffer):
            self._buffer[self._index] = ord(request)
            self._frontend.update(key=request)
            self._index += 1
        elif request == "\b" and 0 < self._index:
            self._frontend.update(key=request)
            self._index -= 1
        elif request == "\r" and self._index == len(self._buffer):
            # Check if user has beaten the game
            if self._buffer.decode() == self._solution:
                print("Congratulations, you won!")
                self.has_won = True

            if self._buffer.decode().lower() not in self._dictionary:
                print("Not in word list.")
            else:
                self._frontend.update(self._pattern())
                self._index, self._guesses = 0, self._guesses + 1

    def mainloop(self) -> None:
        self._frontend.mainloop()

    def _pattern(self) -> tuple[tuple[str, int], ...]:
        """Inspired by: https://github.com/3b1b/videos/blob/master/_2022/wordle/simulations.py"""
        # Shift all strings/results to numpy for faster analysis
        n = len(self._buffer)  # Reduce magic numbers
        guess = np.array(self._buffer, np.uint8)
        solution = np.array([ord(c) for c in self._solution], np.uint8)
        pattern = np.array([TILE_ABSENT] * n, np.uint8)
        equality_grid = np.equal.outer(guess, solution)

        # Update all correct tiles in pattern
        # Remove correct tiles from future analysis
        correct_tiles = guess == solution
        pattern[correct_tiles] = TILE_CORRECT
        equality_grid[:, correct_tiles] = False
        equality_grid[correct_tiles, :] = False

        # Update all exact matches within the guess
        for i, j in itertools.product(range(n), range(n)):
            if equality_grid[i][j]:
                pattern[i] = TILE_PRESENT  # Found present tile...
                equality_grid[i, :], equality_grid[:, j] = False, False
        return tuple(zip(self._buffer.decode(), pattern.tolist()))

    @staticmethod
    def _load_dictionary() -> list[str]:
        with open("data/dictionary.json", "rt", encoding="utf-8") as fp:
            return json.load(fp)

    @staticmethod
    def _load_solution() -> str:
        endpoint = f"https://www.nytimes.com/svc/wordle/v2/{date.today().strftime('%Y-%m-%d')}.json"
        assert (response := requests.get(endpoint, timeout=3)).ok
        return cast(str, json.loads(response.text)["solution"]).upper()


if __name__ == "__main__":
    wordle = Wordle()
    wordle.mainloop()
