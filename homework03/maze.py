from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """
    Убирает стену между выбранной клеткой и соседней (вверх или вправо) для алгоритма Binary Tree.

    :param grid: текущая сетка
    :param coord: координаты клетки (y, x)
    :return: обновлённая сетка
    """

    y, x = coord
    y_remove, x_remove = y, x
    cols = len(grid[0])

    decision = choice(("up", "right"))
    if decision == "up" and 0 <= y - 2:
        y_remove, x_remove = y - 1, x
    else:
        decision = "right"

    if decision == "right" and x + 2 < cols - 1:
        y_remove, x_remove = y, x + 1
    elif 0 <= y - 2 and x < cols - 1:
        y_remove, x_remove = y - 1, x

    grid[y_remove][x_remove] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """
    Генерирует лабиринт по алгоритму Binary Tree.

    :param rows: число строк
    :param cols: число столбцов
    :param random_exit: True — случайные вход и выход, False — фиксированные
    :return: сетка лабиринта с входом и выходом, отмеченными "X"
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for cell in empty_cells:
        grid = remove_wall(grid, cell)

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
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """ "
    Находит все клетки входа/выхода ("X") в лабиринте.

    :param grid: сетка лабиринта
    :return: список координат выходов [(y, x), ...]
    """

    return [(y, x) for y, row in enumerate(grid) for x, s in enumerate(row) if s == "X"]


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    Выполняет один шаг распространения чисел для поиска пути через лабиринт.

    :param grid: сетка лабиринта с заполненными числами и пустыми клетками
    :param k: текущее число, которое распространяется
    :return: обновлённая сетка с увеличенными числами
    """
    rows = len(grid)
    cols = len(grid[0])
    for y, row in enumerate(grid):
        for x, s in enumerate(row):
            if s == k:
                k += 1
                for fill_x, fill_y in [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]:
                    if fill_x in range(0, cols) and fill_y in range(0, rows):
                        if grid[fill_y][fill_x] == 0:
                            grid[fill_y][fill_x] = k
                k -= 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    Восстанавливает кратчайший путь от выхода до входа по пронумерованным клеткам.

    :param grid: сетка с пронумерованными шагами
    :param exit_coord: координаты выхода (y, x)
    :return: список координат пути или кортеж, если путь одной клетки
    """
    rows = len(grid)
    cols = len(grid[0])

    y, x = exit_coord
    k = int(grid[y][x])
    path = [(y, x)]
    while grid[y][x] != 1:
        for check_x, check_y in [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]:
            if check_x in range(0, cols) and check_y in range(0, rows):
                if grid[check_y][check_x] == k - 1:
                    path.append((check_y, check_x))
                    k -= 1
                    x, y = check_x, check_y
                    break

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    Проверяет, окружён ли указанный выход стенами или находится в углу.

    :param grid: сетка лабиринта
    :param coord: координаты клетки выхода (y, x)
    :return: True если выход окружён стенами, иначе False
    """

    rows = len(grid)
    cols = len(grid[0])
    y, x = coord

    if (x, y) in [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]:
        return True

    if (
        (y == 0 and grid[y + 1][x] != " ")
        or (x == cols - 1 and grid[y][x - 1] != " ")
        or (y == rows - 1 and grid[y - 1][x] != " ")
        or (x == 0 and grid[y][x + 1] != " ")
    ):
        return True

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    Находит путь через лабиринт от входа до выхода.

    :param grid: сетка лабиринта с входом и выходом
    :return: обновлённая сетка и список координат пути, либо None если путь невозможен
    """

    exits = get_exits(grid)

    if len(set(exits)) == 1:
        return grid, exits[0]

    for exit_pos in exits:
        if encircled_exit(grid, exit_pos):
            return grid, None

    (y_in, x_in), (y_out, x_out) = exits

    grid[y_in][x_in] = 1
    grid[y_out][x_out] = 0

    for y, row in enumerate(grid):
        for x, s in enumerate(row):
            if s == " ":
                grid[y][x] = 0

    k = 0
    while grid[y_out][x_out] == 0:
        k += 1
        grid = make_step(grid, k)

    path = shortest_path(grid, (y_out, x_out))
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """
    Отмечает путь в лабиринте, заменяя клетки на "X".

    :param grid: сетка лабиринта
    :param path: список координат пути
    :return: сетка с отмеченным путем
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
