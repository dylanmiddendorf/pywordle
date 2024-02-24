from datetime import datetime
from data import WORDLE_DICTIONARY, WORDLE_SOLUTIONS



class Wordle:
    def __init__(self) -> None:
        self._solution = self._load_solution()
        self.remaining_guesses = 6
        self.is_solved = False
    
    def guess(self, word: str) -> list[int]:
        result = [] # Holds the guess result
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
        
    # TODO Identify NYT's solution algorithm
    @staticmethod
    def _load_solution() -> str:
        epoch = datetime(year=1970, month=1, day=1)  # Linux epoch
        solution = (datetime.now() - epoch).days % len(WORDLE_SOLUTIONS)
        return WORDLE_SOLUTIONS[solution]  # Return the day's solution


def main():
    game = Wordle() # Generate a new Wordle instance
    while game.has_guess() and not game.is_solved:
        result = ['🟩' if x == 2 else ('🟨' if x == 1 else '⬛') for x in game.guess(input('> '))]
        print(''.join(result))
    if game.is_solved:
        print("Congrats!")
    else:
        print("Until next time!")
        
if __name__ == "__main__":
    main()
