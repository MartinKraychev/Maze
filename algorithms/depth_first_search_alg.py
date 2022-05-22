import copy
import random

wall_symbol = '\u25AF'
cell_symbol = '\u25AE'
directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
visited_cells = []


def recursive_path(item, copy_maze):
    """
    Calls recursively until there is available moves
    """
    d = get_directions(item, copy_maze)
    if not d:
        return

    new_coord_x = item[0] + d[0]
    new_coord_y = item[1] + d[1]
    copy_maze[new_coord_x][new_coord_y] = cell_symbol
    new_cell = (item[0] + d[0] * 2, item[1] + d[1] * 2)
    visited_cells.append(new_cell)
    recursive_path(new_cell, copy_maze)


def get_possible_moves(coords, copy_maze):
    """
    Returns all possible moves
    """
    result = []
    for d in directions:
        pos_x, pos_y = coords
        dir_x, dir_y = d
        next_cell = (pos_x + dir_x * 2, pos_y + dir_y * 2)
        if 1 <= next_cell[0] < len(copy_maze) - 1 and 1 <= next_cell[1] < len(copy_maze[0]) - 1:
            if next_cell not in visited_cells:
                direction = (dir_x, dir_y)
                result.append(direction)

    return result


def get_directions(coordinates, copy_maze):
    """
    Selects random direction
    """
    try:

        direction = random.choice(get_possible_moves(coordinates, copy_maze))
        return direction
    except IndexError:
        return None


def dfs_alg(maze):
    """
    Creating maze with recursive dfs algorithm
    """
    copy_maze = copy.deepcopy(maze)

    for r in range(len(maze)):
        for c in range(len(maze[r])):
            tile = maze[r][c]
            if tile == cell_symbol:
                cell = r, c
                visited_cells.append(cell)
                recursive_path(cell, copy_maze)

    return copy_maze
