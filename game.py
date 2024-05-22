from __future__ import annotations
from typing import Any
import pickle
import numpy as np

__all__ = ["Connect4"]


class Connect4:
    """Classic Connect-4 Game.

    Configuration:
        shape: tuple[int, int]
        k: int
        players: list[int]

    State:
        grid: np.ndarray
        action: int
        time: int

    Action:
        int

    """

    def __init__(self, config: dict[str, Any] = None) -> None:
        # Set the config dict, using default values if any are not given
        self._config = Connect4.default_config()
        if config is not None:
            self._config |= config

        # Initialize the config-related members
        self._shape = self._config["shape"]
        self._k = self._config["k"]
        self._players = self._config["players"]

        # Check if the configuration setup is valid
        assert self._k <= min(
            *self._shape
        ), "Invalid config: the line length is > min(row, col), can't create game."

        # Set all state-related members to their "zero" values
        # NOTE: this implicitly enforces game.start() to be called
        self._grid = None
        self._active = -1
        self._time = -1

        # Additional computed members for faster runtime
        # The generated actions at a timestamp
        self._actions = (-1, [])

    # PUBLIC METHODS #

    def start(self, state: dict[str, Any] = None) -> dict[str, Any]:
        """Start the game from the zero or (optional) state.

        Parameters
        ----------
        state : dict[str, Any] = None
            An optional dictionary for the game state to start from.

        Returns
        -------
        state : dict[str, Any]

        """

        if state is None:
            self._grid = np.zeros(self._shape, dtype=np.int8)
            self._active = 0
            self._time = 0
        else:
            self._grid = state["grid"]
            self._active = state["active"]
            self._time = state["time"]
        # Generate actions (optional to place to here)
        self.generate_actions()
        return self.state

    def transition(self, action: int) -> dict[str, Any]:
        """Transition the game state based on the given action

        Parameters
        ----------
        action : int
            The column to place the token

        Returns
        -------
        state : dict[str, Any]

        """

        assert action in self._actions[1], "Invalid action"

        # Get the token to place
        col = action
        token = self._players[self._active]

        # Find the row to place the token at
        for row in range(self._grid.shape[0]):
            if self._grid[row][col] != 0:
                self._grid[row - 1][col] = token
                break
        else:
            self._grid[self._grid.shape[0] - 1][col] = token

        # Update the active player and time
        self._active = (self._active + 1) % len(self._players)
        self._time += 1

        # Generate actions (optional to place to here)
        self.generate_actions()

        return self.state

    def generate_actions(self) -> list[int]:
        if self._actions[0] < self._time:
            actions = []
            for col in range(self._grid.shape[1]):
                if np.all(self._grid[:, col] != 0):
                    continue
                else:
                    actions.append(col)
            self._actions = (self._time, actions)
        return self._actions[1]

    def terminal(self) -> bool:
        return (
            self._check_horizontal_lines()
            or self._check_vertical_lines()
            or self._check_diagonal_lines()
            or np.all(self._grid != 0)
        )

    def report(self) -> dict[str, Any]:
        report = {}
        if np.all(self._grid != 0):
            report = {"result": "draw", "winner": None}
        else:
            report = {
                "result": "win",
                "winner": self._players[(self._active - 1) % len(self._players)],
            }
        return report

    def render(self) -> None:
        print("===" * self._grid.shape[1])
        print(f"Time: {self._time} - Active: {self._players[self._active]}")
        print(" -" + "--" * self._grid.shape[1])
        for row in range(self._grid.shape[0]):
            print("|", end=" ")
            for col in range(self._grid.shape[1]):
                print(self._grid[row][col], end=" ")
            print("|")
        print(" -" + "--" * self._grid.shape[1])
        print("===" * self._grid.shape[1])

    def save(self, filename: str) -> None:
        instance = {
            "grid": self._grid,
            "active": self._active,
            "time": self._time,
            "config": self._config,
        }

        with open(filename, "wb+") as f:
            pickle.dump(instance, f)

    @classmethod
    def load(cls, filename: str) -> Connect4:
        with open(filename, "rb") as f:
            instance = pickle.load(f)

        game = cls(instance["config"])
        game._grid = instance["grid"]
        game._active = instance["active"]
        game._time = instance["time"]

        return game

    @classmethod
    def default_config(cls) -> dict[str, Any]:
        return {"shape": (6, 7), "k": 4, "players": [1, 2]}

    @property
    def state(self) -> dict[str, Any]:
        return {"grid": np.copy(self._grid), "active": self._active, "time": self._time}

    # PRIVATE METHODS #

    def _check_horizontal_lines(self) -> bool:
        for row in range(self._grid.shape[0]):
            # Get the columns from row
            subgrid = self._grid[row, :]
            assert subgrid.ndim == 1 and subgrid.shape[0] == self._grid.shape[1]
            # Loop for all valid k length lines of row
            for col in range(self._grid.shape[1] - self._k + 1):
                # Get the k length line starting from col
                line = subgrid[col : col + self._k]
                assert line.shape[0] == self._k
                # Check if the line is full
                if check_line(line):
                    return True
        return False

    def _check_vertical_lines(self) -> bool:
        for col in range(self._grid.shape[1]):
            # Get the rows from col
            subgrid = self._grid[:, col]
            assert subgrid.ndim == 1 and subgrid.shape[0] == self._grid.shape[0]
            # Loop for all valid k length lines of col
            for row in range(self._grid.shape[0] - self._k + 1):
                # Get the k length line starting from row
                line = subgrid[row : row + self._k]
                assert line.shape[0] == self._k
                # Check if the line is full
                if check_line(line):
                    return True
        return False

    def _check_diagonal_lines(self) -> bool:
        for row in range(self._grid.shape[0]):
            # Check if row + k goes out of bounds of the grid
            if row + self._k > self._grid.shape[0]:
                break
            for col in range(self._grid.shape[1]):
                # Check if col + k goes out of bounds of the grid
                if col + self._k > self._grid.shape[1]:
                    break
                # Get the k x k subgrid to check diagonals
                subgrid = self._grid[row : row + self._k, col : col + self._k]
                assert subgrid.shape[0] == subgrid.shape[1] == self._k
                # Get the main and anti diagonals of the subgrid
                lr_line = np.diagonal(subgrid)
                rl_line = np.fliplr(subgrid).diagonal()
                # Check if either of the lines are full
                if check_line(lr_line) or check_line(rl_line):
                    return True
        return False


# HELPER FUNCTIONS #


def check_line(line: np.ndarray) -> bool:
    return line[0] != 0 and np.min(line) == np.max(line)
