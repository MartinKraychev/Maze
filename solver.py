import copy
from dataclasses import dataclass
from operator import attrgetter

from functions import show_maze


@dataclass(frozen=True)
class Tile:
    """
    Data class used to for storing data for better performance.
    Alternative is commented below.
    """
    x: int
    y: int
    goal: tuple
    # g = steps taken so far
    g: int
    prev_tile_coord: tuple

    def __post_init__(self):
        # We set the heuristic score of Tile. It is the sum of the steps(g) and the manhattan distance.
        object.__setattr__(self, 'f', self.g + abs(self.goal[0] - self.x) + abs(self.goal[1] - self.y))


# class Tile:
#
#     def __init__(self, x, y, goal, step, prev_tile_coord=None):
#         self.x = x
#         self.y = y
#         self.goal = goal
#         self.g = step
#         self.h = self.calculate_heuristic()
#         self.f = self.g + self.h
#         self.prev_tile_coord = prev_tile_coord
#
#     def calculate_heuristic(self):
#         return abs(self.goal[0] - self.x) + abs(self.goal[1] - self.y)


class Solver:
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    wall_symbol = '\u25AF'
    start_symbol = '\u27A4'
    finish_symbol = '\u274C'

    terrain = {
        '\u2162': 3,
        '\u2164': 5,
        '\u2169': 10,
        '\u25AE': 1,
        '\u274C': 1
    }

    def __init__(self, maze):
        self._initial_state = copy.deepcopy(maze)
        self.start = self.find_position(Solver.start_symbol)
        self.finish = self.find_position(Solver.finish_symbol)
        self.closed_tiles = []
        self.open_tiles = []
        self.step = 1
        self.cache = {}

    def find_position(self, symbol):
        for r in range(len(self._initial_state)):
            if symbol in self._initial_state[r]:
                c = self._initial_state[r].index(symbol)
                return r, c

    def get_directions(self, pos_x, pos_y):
        all_directions = []
        for d in Solver.directions:
            new_pos_x = pos_x + d[0]
            new_pos_y = pos_y + d[1]

            if 1 <= new_pos_x < len(self._initial_state) - 1 and 1 <= new_pos_y < len(self._initial_state[0]) - 1:
                if self._initial_state[new_pos_x][new_pos_y] != Solver.wall_symbol:
                    if (new_pos_x, new_pos_y) not in self.closed_tiles:
                        all_directions.append(d)

        return all_directions

    def solve(self):
        # Starts with the starting tile and adds to the open tiles list
        start_tile = Tile(self.start[0], self.start[1], self.finish, 0, (self.start[0], self.start[1]))
        self.open_tiles.append(start_tile)

        while self.open_tiles:

            best_score_tile = self.find_best_score_tile()
            # self._initial_state[best_score_tile.x][best_score_tile.y] = Solver.start_symbol
            # print(show_maze(self._initial_state))

            # Saves the previous move to get to the current tile in the cache
            self.cache[(best_score_tile.x, best_score_tile.y)] = \
                best_score_tile.prev_tile_coord[0], best_score_tile.prev_tile_coord[1]

            # If we reach the finish symbol we return and we backtrack
            # from the cache to find the path to the starting symbol
            if best_score_tile.x == self.finish[0] and best_score_tile.y == self.finish[1]:
                return self.backtracking()

            moves = self.get_directions(best_score_tile.x, best_score_tile.y)

            for move in moves:
                next_tile_x = best_score_tile.x + move[0]
                next_tile_y = best_score_tile.y + move[1]
                symbol = self._initial_state[next_tile_x][next_tile_y]
                tile = Tile(next_tile_x, next_tile_y, self.finish, best_score_tile.g + self.terrain[symbol],
                            (best_score_tile.x, best_score_tile.y))

                self.open_tiles.append(tile)

            self.open_tiles.remove(best_score_tile)
            self.closed_tiles.append((best_score_tile.x, best_score_tile.y))

    def find_best_score_tile(self):
        """
        Returns the tile with the minimum score from the tiles list
        """
        return min(self.open_tiles, key=attrgetter('f'))

    def backtracking(self):
        """
        Backtracks the movement from the cache in reverse order(Starting from the finish symbol)
        """
        last_move = self.finish
        self._initial_state[last_move[0]][last_move[1]] = Solver.start_symbol
        prev_move = self.cache[last_move]

        while True:
            if prev_move == self.start:
                print(show_maze(self._initial_state))
                return
            self._initial_state[prev_move[0]][prev_move[1]] = Solver.start_symbol
            prev_move = self.cache[prev_move]
