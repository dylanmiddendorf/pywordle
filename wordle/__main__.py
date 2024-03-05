import json, requests
from datetime import date
from backend import Backend


class Wordle:
    def __init__(self) -> None:
        self._solution = self._load_solution()
        self.remaining_guesses = 6
        self.is_solved = False

    def guess(self, word: str) -> list[int]:
        result = []  # Holds the guess result
        for i, c in enumerate(word):
            if c == self._solution[i]:
                result.append(2)
            elif c in self._solution:
                result.append(1)
            else:
                result.append(0)
        self.remaining_guesses -= 1
        if result.count(2) == 5:
            self.is_solved = True
        return result

    def has_guess(self) -> bool:
        return self.remaining_guesses > 0

    @staticmethod
    def _load_solution() -> str:
        endpoint = f"https://www.nytimes.com/svc/wordle/v2/{date.today().strftime('%Y-%m-%d')}.json"
        assert (response := requests.get(endpoint)).ok # Verify the request is valid
        return json.loads(response.text)['solution'] # Return the solution


def main():
    backend = Backend()
    backend.mainloop()

if __name__ == "__main__":
    main()
    