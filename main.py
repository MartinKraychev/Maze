from algorithms.binary_tree_alg import binary_tree_alg
from algorithms.depth_first_search_alg import dfs_alg
from algorithms.randomized_prim_alg import Maze
from functions import show_maze, generate_initial_maze, generate_maze_with_walls_only, place_points

if __name__ == '__main__':
    initial_maze = generate_initial_maze(59, 20)
    maze_with_walls = generate_maze_with_walls_only(60, 20)
    # binary_maze = binary_tree_alg(initial_maze)
    # binary_maze_with_points = place_points(binary_maze)
    # print(show_maze(binary_maze_with_points))
    # dfs_maze = dfs_alg(initial_maze)
    # dfs_maze_with_points = place_points(dfs_maze)
    # print(show_maze(dfs_maze_with_points))
    maze = Maze(60, 20)
    maze.create_paths()
    maze.place_points()
    print(maze)
