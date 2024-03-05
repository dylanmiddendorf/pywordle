# wordle

Welcome to PyWordle, a fun and challenging word game inspired by the web-based Wordle. PyWordle is written in Python, using tkinter for the graphical user interface. PyWordle is not affiliated with or endorsed by The New York Times Company, the owner of the original Wordle game, which can be played here: https://www.nytimes.com/puzzles/wordle.

## How to play

The goal of the game is to guess a randomly chosen five-letter word in six attempts or less. You can enter any five-letter word in the input box and press enter or click the submit button. You will receive feedback for each guess in the form of colored tiles:

- Green: The letter is in the correct position in the word.
- Yellow: The letter is in the word, but not in the correct position.
- Gray: The letter is not in the word.

You can use the feedback to narrow down your guesses and find the word. If you guess the word correctly, you win the game. If you run out of attempts, you lose the game and the word is revealed.

## How to run

To run the project, you need to have Python 3 and required dependencies installed on your system. You can download Python from [here](https://www.python.org/downloads/) and tkinter from [here](https://tkdocs.com/tutorial/install.html).

To run the project, navigate to the project directory and execute the following command:

```bash
python pywordle/__main__.py
```

This will launch the game window where you can start playing.

## How to contribute

If you want to contribute to this project, you can fork the repository and make changes as you wish. You can also submit issues or pull requests if you find any bugs or have any suggestions for improvement.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- `data/backspace.png` was obtained from https://svgrepo.com.
- `data/dictionary.json` was obtained from https://www.nytimes.com.