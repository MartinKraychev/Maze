import copy
import random


class Maze:
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    wall_symbol = '\u25AF'
    cell_symbol = '\u25AE'
    start_symbol = '\u27A4'
    finish_symbol = '\u274C'

    terrain = {
        '\u2162': 3,
        '\u2164': 5,
        '\u2169': 10
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._initial_maze = self.create_initial_maze(self.width, self.height)
        self._current_maze_state = copy.deepcopy(self._initial_maze)
        self.visited_cells = []
        # key = wall, value = the direction that the wall was selected from
        self.walls = {}

    def create_paths(self):
        """
        Starts with random point in the maze and marks it as visited.
        Collects all the walls around that point and picks one randomly if the cell on the other side is not visited.
        Repeats previous step until there is no more walls left.
        """
        r = random.randint(1, len(self._current_maze_state) - 2)
        c = random.randint(1, len(self._current_maze_state[0]) - 2)
        self._current_maze_state[r][c] = Maze.cell_symbol
        self.visited_cells.append((r, c))
        self.get_neighboring_walls(r, c)

        while self.walls:
            wall = random.choice(list(self.walls.keys()))
            direction = self.walls[wall]
            next_cell = wall[0] + direction[0], wall[1] + direction[1]
            if 1 <= next_cell[0] < len(self._current_maze_state) - 1 and 1 <= next_cell[1] < len(
                    self._current_maze_state[0]) - 1:

                if not self.check_if_cell_is_visited(next_cell):
                    self._current_maze_state[wall[0]][wall[1]] = Maze.cell_symbol
                    self._current_maze_state[next_cell[0]][next_cell[1]] = Maze.cell_symbol
                    self.visited_cells.append((next_cell[0], next_cell[1]))
                    self.visited_cells.append(wall)
                    self.get_neighboring_walls(next_cell[0], next_cell[1])
            else:
                self._current_maze_state[wall[0]][wall[1]] = Maze.cell_symbol
                self.visited_cells.append(wall)

            self.walls.pop(wall)

    def check_if_cell_is_visited(self, cell):
        if cell in self.visited_cells:
            return True

    def get_neighboring_walls(self, cell_x, cell_y):
        """
        Returns possible neighbors of the given cell
        """
        for d in Maze.directions:
            current_wall = (cell_x + d[0], cell_y + d[1])
            if 1 <= current_wall[0] < len(self._current_maze_state) - 1 and \
                    1 <= current_wall[1] < len(self._current_maze_state[0]) - 1:

                if self._current_maze_state[current_wall[0]][current_wall[1]] == Maze.wall_symbol and \
                        current_wall not in self.walls:
                    self.walls[current_wall] = d

    def add_details(self):
        """
        Adds starting and finishing points to the maze.
        After that it adds 20 random terrain points with different step count.
        Finally it adds interconnecting points in the maze can have multiple paths to the target.
        """
        self.select_random_position(Maze.start_symbol)
        self.select_random_position(Maze.finish_symbol)

        for t in range(50):
            terrain_symbol = random.choice(list(self.terrain.keys()))
            self.select_random_position(terrain_symbol)

        all_walls = self.get_all_walls()
        for w in range(100):
            wall = random.choice(all_walls)
            self._current_maze_state[wall[0]][wall[1]] = Maze.cell_symbol
            all_walls.remove(wall)

    def get_all_walls(self):
        all_walls = []
        for r in range(1, len(self._current_maze_state) - 1):
            for c in range(1, len(self._current_maze_state[r]) - 1):
                if self._current_maze_state[r][c] == Maze.wall_symbol:
                    all_walls.append((r, c))

        return all_walls

    def select_random_position(self, symbol):
        """
        Selects random position for a symbol and removes it from available positions.
        """
        position = random.choice(self.visited_cells)
        self.visited_cells.remove(position)
        self._current_maze_state[position[0]][position[1]] = symbol

    @staticmethod
    def show_maze(matrix):
        """
        Returns the maze in user friendly way to be shown in the console
        """
        result = ''
        for line in matrix:
            result += ''.join(line)
            result += '\n'

        return result

    @staticmethod
    def create_initial_maze(width, height):
        return [list(width * Maze.wall_symbol) for h in range(height)]

    @property
    def initial_maze(self):
        return self._initial_maze

    @property
    def current_maze_state(self):
        return self._current_maze_state

    def __str__(self):
        return self.show_maze(self._current_maze_state)
