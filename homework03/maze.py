"""Module for maze generation and solving algorithms."""

from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    """Create a grid filled with wall characters.

    :param rows: Number of rows in the grid
    :param cols: Number of columns in the grid
    :return: Grid filled with wall characters
    """
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """Remove wall at specified coordinate.

    :param grid: The maze grid
    :param coord: Coordinate tuple (row, col)
    :return: Modified grid with wall removed
    """
    # TODO: Implement wall removal logic
    _ = coord  # Will be used in implementation
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """Generate a maze using binary tree algorithm.

    :param rows: Number of rows in the maze
    :param cols: Number of columns in the maze
    :param random_exit: Whether to use random entrance/exit positions
    :return: Generated maze grid
    """
    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = (
            randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
        )
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """Get all exit coordinates from the maze.

    :param grid: The maze grid
    :return: List of exit coordinates
    """
    # TODO: Implement exit detection logic
    _ = grid  # Will be used in implementation
    return []


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """Perform one step of wave propagation algorithm.

    :param grid: The maze grid with wave numbers
    :param k: Current wave number
    :return: Modified grid after one step
    """
    # TODO: Implement wave propagation step logic
    _, _ = grid, k  # Will be used in implementation
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """Find shortest path to exit coordinate.

    :param grid: The maze grid with wave numbers
    :param exit_coord: Target exit coordinate
    :return: Shortest path as list of coordinates or None if no path exists
    """
    # TODO: Implement shortest path finding logic
    _, _ = grid, exit_coord  # Will be used in implementation
    return None  # pylint: disable=useless-return


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """Check if exit is completely surrounded by walls.

    :param grid: The maze grid
    :param coord: Coordinate to check
    :return: True if exit is encircled, False otherwise
    """
    # TODO: Implement encircled exit check logic
    _, _ = grid, coord  # Will be used in implementation
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[
    List[List[Union[str, int]]],
    Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
]:
    """Solve the maze and find path between exits.

    :param grid: The maze grid
    :return: Tuple of (modified grid, path) or (grid, None) if no solution
    """
    # TODO: Implement maze solving logic
    _ = grid  # Will be used in implementation
    return grid, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """Add path markers to the grid.

    :param grid: The maze grid
    :param path: Path as single coordinate or list of coordinates
    :return: Grid with path marked
    """
    if path:
        path_list: List[Tuple[int, int]] = [path] if isinstance(path, tuple) else path
        for coord in path_list:
            i, j = coord
            if 0 <= i < len(grid) and 0 <= j < len(grid[i]):
                grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
