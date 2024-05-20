import random
from game import Game


def main():
    ROWS, COLS, K = 6, 7, 4
    game = Game(ROWS, COLS, K)

    while not game.terminal():
        game.render()
        action = random.choice(game.generate_actions())
        game.transition(action)
        print(f"Action: {action}")
    game.render()
    print(f"Winner: {game._active} after time: {game._time}")


if __name__ == "__main__":
    main()
