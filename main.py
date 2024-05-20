import random
import numpy as np


def create_grid(rows: int = 6, cols: int = 7):
    return np.zeros((rows, cols), dtype=int)


def display_grid(grid: np.ndarray):
    print(" -" + "--" * grid.shape[1])
    for row in range(grid.shape[0]):
        print("|", end=" ")
        for col in range(grid.shape[1]):
            print(grid[row][col], end=" ")
        print("|")
    print(" -" + "--" * grid.shape[1])


def generate_moves(grid: np.ndarray) -> list[int]:
    moves = []
    for col in range(grid.shape[1]):
        if np.all(grid[:, col] != 0):
            continue
        else:
            moves.append(col)
    return moves


def place_token(grid: np.ndarray, token: int, col: int, row: int = None) -> bool:
    if col < 0 or col >= grid.shape[1]:
        return False

    if np.all(grid[:, col] != 0):
        return False

    if row is not None:
        grid[row][col] = token
    else:
        for row in range(grid.shape[0]):
            if grid[row][col] != 0:
                grid[row - 1][col] = token
                break
        else:
            grid[grid.shape[0] - 1][col] = token

    return True


def check_horizontal_lines(grid: np.ndarray, k: int) -> bool:
    for row in range(grid.shape[0]):
        subgrid = grid[row, :]
        assert subgrid.ndim == 1 and subgrid.shape[0] == grid.shape[1]
        for col in range(grid.shape[1] - k + 1):
            line = subgrid[col : col + k]
            assert line.shape[0] == k
            if line[0] != 0 and np.min(line) == np.max(line):
                return True
    return False


def check_vertical_lines(grid: np.ndarray, k: int) -> bool:
    for col in range(grid.shape[1]):
        subgrid = grid[:, col]
        assert subgrid.ndim == 1 and subgrid.shape[0] == grid.shape[0]
        for row in range(grid.shape[0] - k + 1):
            line = subgrid[row : row + k]
            assert line.shape[0] == k
            if line[0] != 0 and np.min(line) == np.max(line):
                return True
    return False


def check_diagonal_lines(grid: np.ndarray, k: int) -> bool:
    for row in range(grid.shape[0]):
        if row + k > grid.shape[0]:
            break
        for col in range(grid.shape[1]):
            if col + k > grid.shape[1]:
                break

            subgrid = grid[row : row + k, col : col + k]
            assert subgrid.shape[0] == subgrid.shape[1] == k

            lr_line = np.diagonal(subgrid)
            if lr_line[0] != 0 and np.min(lr_line) == np.max(lr_line):
                return True

            rl_line = np.fliplr(subgrid).diagonal()
            if rl_line[0] != 0 and np.min(rl_line) == np.max(rl_line):
                return True

    return False


def terminal(grid: np.ndarray, k: int) -> bool:
    return (
        check_horizontal_lines(grid, k)
        or check_vertical_lines(grid, k)
        or check_diagonal_lines(grid, k)
        or np.all(grid != 0)
    )


def main():
    ROWS, COLS, K = 6, 7, 4
    grid = create_grid(ROWS, COLS)

    # TOKENS:
    # 0 - Empty, 1 - Red, 2 - Yellow
    players = [1, 2]
    active = 0
    time = 0

    grid = np.random.randint(1, 10, (ROWS, COLS))

    while not terminal(grid, K):
        display_grid(grid)
        token = players[active]
        action = random.choice(generate_moves(grid))
        print(f"Action: {action}")
        place_token(grid, token, action)
        active = (active + 1) % len(players)
        time += 1
    display_grid(grid)
    print(f"Winner: {active} after time: {time}")


if __name__ == "__main__":
    main()
