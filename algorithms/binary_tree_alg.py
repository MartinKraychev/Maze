import random

directions = [(0, 1), (1, 0)]
cell_symbol = '\u25AE'


def binary_tree_alg(maze):
    """
    For every cell in the maze chooses a random direction
    - either down or right and builds a path in the wall to connect two cells
    """
    for r in range(1, len(maze) - 1, 2):
        for c in range(1, len(maze[r]) - 1, 2):
            random_path_x, random_path_y = random.choice(directions)
            # Edge cases for leaving the wall frame
            if (r + random_path_x) > len(maze) - 2:
                random_path_x = 0
                random_path_y += 1

            if (c + random_path_y) > len(maze[0]) - 2:
                if c == len(maze[0]) - 2 and r == len(maze) - 2:
                    random_path_x = 0
                else:
                    random_path_x += 1
                random_path_y = 0
            # End of edge cases

            maze[r + random_path_x][c + random_path_y] = cell_symbol

    return maze
