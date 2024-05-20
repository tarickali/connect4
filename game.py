from __future__ import annotations
from typing import Any
import pickle
import numpy as np


class Game:
    def __init__(self, config: dict[str, Any] = None) -> None:
        self._config = Game.default_config()
        if config is not None:
            self._config |= config

        self._grid = np.zeros(self._config["shape"], dtype=np.int8)
        self._k = self._config["k"]
        self._players = self._config["players"]

        self._active = 0
        self._time = 0

    # PUBLIC METHODS #
    def start(self, state: dict[str, Any] = None) -> None:
        if state is None:
            self._grid = np.zeros(self._config["shape"], dtype=np.int8)
            self._active = 0
            self._time = 0
        else:
            self._grid = state["grid"]
            self._active = state["active"]
            self._time = state["time"]

    def transition(self, action: int) -> None:
        if action < 0 or action >= self._grid.shape[1]:
            return
        if np.all(self._grid[:, action] != 0):
            return

        col = action
        token = self._players[self._active]

        for row in range(self._grid.shape[0]):
            if self._grid[row][col] != 0:
                self._grid[row - 1][col] = token
                break
        else:
            self._grid[self._grid.shape[0] - 1][col] = token

        self._active = (self._active + 1) % len(self._players)
        self._time += 1
        return

    def generate_actions(self) -> list[int]:
        actions = []
        for col in range(self._grid.shape[1]):
            if np.all(self._grid[:, col] != 0):
                continue
            else:
                actions.append(col)
        return actions

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
            report = {"result": "win", "winner": self._players[self._active]}
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
    def load(cls, filename: str) -> Game:
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
            subgrid = self._grid[row, :]
            assert subgrid.ndim == 1 and subgrid.shape[0] == self._grid.shape[1]
            for col in range(self._grid.shape[1] - self._k + 1):
                line = subgrid[col : col + self._k]
                assert line.shape[0] == self._k
                if line[0] != 0 and np.min(line) == np.max(line):
                    return True
        return False

    def _check_vertical_lines(self) -> bool:
        for col in range(self._grid.shape[1]):
            subgrid = self._grid[:, col]
            assert subgrid.ndim == 1 and subgrid.shape[0] == self._grid.shape[0]
            for row in range(self._grid.shape[0] - self._k + 1):
                line = subgrid[row : row + self._k]
                assert line.shape[0] == self._k
                if line[0] != 0 and np.min(line) == np.max(line):
                    return True
        return False

    def _check_diagonal_lines(self) -> bool:
        for row in range(self._grid.shape[0]):
            if row + self._k > self._grid.shape[0]:
                break
            for col in range(self._grid.shape[1]):
                if col + self._k > self._grid.shape[1]:
                    break

                subgrid = self._grid[row : row + self._k, col : col + self._k]
                assert subgrid.shape[0] == subgrid.shape[1] == self._k

                lr_line = np.diagonal(subgrid)
                if lr_line[0] != 0 and np.min(lr_line) == np.max(lr_line):
                    return True

                rl_line = np.fliplr(subgrid).diagonal()
                if rl_line[0] != 0 and np.min(rl_line) == np.max(rl_line):
                    return True

        return False
