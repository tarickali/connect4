import random
from game import Connect4


def driver():
    config = {"shape": (6, 7), "k": 4}
    game = Connect4(config)

    state = game.start()
    while not game.terminal():
        game.render()
        action = random.choice(game.generate_actions())
        print(f"Action: {action}")
        state = game.transition(action)
    game.render()

    print(game.report())


if __name__ == "__main__":
    driver()
