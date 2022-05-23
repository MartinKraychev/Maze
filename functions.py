import random

from constrains import *


def show_maze(maze):
    """
    returns the maze in user friendly way to be shown in the console
    """
    result = ''
    for line in maze:
        result += ''.join(line)
        result += '\n'

    return result


def generate_initial_maze(width, height):
    """
    Creates a maze from width and height.
    There is wall frame around it and cells surrounded by walls
    """

    matrix = []
    for h in range(height):
        if h % 2 == 0:
            line = list(width * wall_symbol)
        else:
            line = list(int(width / 2) * f'{wall_symbol}{cell_symbol}')
            line.append(wall_symbol)
        matrix.append(line)

    matrix.append(list(width * wall_symbol))
    return matrix


def generate_maze_with_walls_only(width, height):
    """
    Creates a maze from width and height. It contains wall symbols only
    """
    return [list(width * wall_symbol) for h in range(height)]


def place_points(maze):
    """
    Places start and finish points on the maze
    """
    all_cells = []
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == cell_symbol:
                all_cells.append((r, c))

    start = random.choice(all_cells)
    all_cells.remove(start)
    maze[start[0]][start[1]] = start_symbol
    finish = random.choice(all_cells)
    maze[finish[0]][finish[1]] = finish_symbol

    return maze
