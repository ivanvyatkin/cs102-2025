"""GUI module for maze visualization and solving."""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import List

from maze import add_path_to_grid, bin_tree_maze, solve_maze


def draw_cell(
    x: int, y: int, color: str, size: int = 10, canvas_obj: tk.Canvas = None
) -> None:
    """Draw a single cell on the canvas.

    :param x: X coordinate
    :param y: Y coordinate
    :param color: Color of the cell
    :param size: Size of the cell in pixels
    :param canvas_obj: Canvas to draw on
    """
    if canvas_obj is None:
        return
    x *= size
    y *= size
    x1 = x + size
    y1 = y + size
    canvas_obj.create_rectangle(x, y, x1, y1, fill=color)


def draw_maze(
    grid: List[List[str]], size: int = 10, canvas_obj: tk.Canvas = None
) -> None:
    """Draw the entire maze on the canvas.

    :param grid: The maze grid
    :param size: Size of each cell in pixels
    :param canvas_obj: Canvas to draw on
    """
    if canvas_obj is None:
        return
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == " ":
                color = "White"
            elif cell == "■":
                color = "black"
            elif cell == "X":
                color = "red"
            else:
                color = "White"
            draw_cell(x=y, y=x, color=color, size=size, canvas_obj=canvas_obj)


def show_solution(grid: List[List[str]], cell_size: int, canvas_obj: tk.Canvas) -> None:
    """Show the solution path on the maze.

    :param grid: The maze grid
    :param cell_size: Size of each cell in pixels
    :param canvas_obj: Canvas to draw on
    """
    _, path = solve_maze(grid)
    maze = add_path_to_grid(grid, path)
    if path:
        draw_maze(maze, cell_size, canvas_obj)
    else:
        messagebox.showinfo("Message", "No solutions")


if __name__ == "__main__":
    N, M = 51, 77

    CELL_SIZE = 10
    GRID = bin_tree_maze(N, M)

    window = tk.Tk()
    window.title("Maze")
    window.geometry(f"{M * CELL_SIZE + 100}x{N * CELL_SIZE + 100}")

    canvas = tk.Canvas(window, width=M * CELL_SIZE, height=N * CELL_SIZE)
    canvas.pack()

    draw_maze(GRID, CELL_SIZE, canvas)
    ttk.Button(
        window,
        text="Solve",
        command=lambda: show_solution(GRID, CELL_SIZE, canvas),
    ).pack(pady=20)

    window.mainloop()
