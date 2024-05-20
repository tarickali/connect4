import random
from game import Game


def driver():
    config = {"shape": (6, 7), "k": 4}
    game = Game(config)

    game.start()
    while not game.terminal():
        game.render()
        action = random.choice(game.generate_actions())
        game.transition(action)
        print(f"Action: {action}")
    game.render()

    print(game.report())


if __name__ == "__main__":
    driver()
