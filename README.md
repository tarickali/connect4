# Connect-4

A lightweight implementation of Connect-4 to train AI agents.

## Introduction

As childhood classic, Connect-4 won the hearts of millions for its fun and entertaining gameplay. The mix of its low barrier of entry and rich strategies creates a unique competitive experience for players of all ages. However, if you are anything like me, you may have wondered what optimal play looks like. To answer that question, we have really have three choices: 1. have a group of humans analyze the game space, 2. have a group of computers analyze the entire game space, or 3. have a computer learn the game and analyze the game space. The first two options are a no go for obvious reasons (time is limited at the end of the day). So we are left we option 3. To that end, this project is meant to be a simple implementation of the game that can be used to train various AI agents by using its "API" (more on this in the Usages section).

## Installation

All requirements can be found in `requirements.txt` but you won't be surprised to find that you only need `numpy` to run this project.

To install this project, follow these setups:

1. Clone github repo to your local environment:
   `git clone https://github.com/tarickali/connect4.git`
2. Change directory into project folder and install project requirements:
    `cd connect4 && pip install -r requirements.txt`

And that's it.

## Usage

The interface design for `connect4` is meant to be straight-forward and intuitive to use.
The high-level steps are:

```{python}
# 1. Define a config dictionary and a create a game
config = {"shape": (6, 7), "k": 4, "players": [1, 2]} # look at Connect4.default_config
game = Connect4(config)
# 2. Start the game
game.start()
# 3. Loop until the game is over
while not game.terminal():
    # 4. Render the game in terminal (optional)
    game.render()
    # 5. Generate actions
    actions = game.generate_actions()
    # 6. Select action
    action = random.choice(actions) # <- agent code goes here (can use game.state)
    # 7. Transition the game based on the action
    game.transition(action)
# 8. Get the end-game report
report = game.report()
```

The game implementation also comes with a few extra features that may prove to be useful while training an agent. In particular:

- `start(state: dict[str, Any])`: The `start` method accepts an optional `state` dictionary to start from any game state.
- `save(filename: str)`: Saves an instance of the complete game into a `pickle` file. This instance includes everything needed to create and start the game, i.e. the config and state information.
- `load(filename: str)`: A classmethod that loads a saved instance and returns a ready to run game. Note that you do not need to `start` a loaded game.

## Customizability

This implementation of Connect-4 gives users the ability to customize the game's structure. Namely, one can change the following:

- The grid's shape: by default the shape is 6 rows and 7 columns, but this can be changed to any shape, even 100x100 but that's kind of crazy...
- The line length: by default the line length, k, to win is 4, but this can be changed to anything that is k <= min(row, col). If k > min(row, col), then no one can win.
- The players: by default there are two players and they are represented by the integers 1 and 2. Although it is very non-standard, this implementation supports any number of players that play in the sequential order given in `config["players"]`. Note that there is no restriction that the same integer is used more than once, so technically teams of agents can played against each other.

N.B. that the default values here are based on the classic game of Connect-4.

Although you can mix and match these customizations as much as you like, some game configurations make more sense than others, so take this a note of caution.

## Extendability

If the play and flow of Connect-4 does not seem rich enough for your AI training needs, you can take the base game and modify the `start`, `transition`, and `terminal` methods to create different games entirely. This requires more effort and writing different logic to deal with each of these methods, however similar principles from the base game should still hold. For example, one can implement these [variants of Connect-4](https://en.wikipedia.org/wiki/Connect_Four#Rule_variations).
