import numpy as np


class Game:
    def __init__(self, rows: int, cols: int, k: int = 4) -> None:
        self._grid = np.zeros((rows, cols), dtype=np.int8)
        self._k = k

        # TOKENS: 0 - Empty, 1 - Red, 2 - Yellow
        self._players = [1, 2]
        self._active = 0
        self._time = 0

    # PUBLIC METHODS #

    def render(self) -> None:
        print(" -" + "--" * self._grid.shape[1])
        for row in range(self._grid.shape[0]):
            print("|", end=" ")
            for col in range(self._grid.shape[1]):
                print(self._grid[row][col], end=" ")
            print("|")
        print(" -" + "--" * self._grid.shape[1])

    def transition(self, action: int) -> None:
        # def place_token(grid: np.ndarray, token: int, col: int, row: int = None) -> bool:
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
