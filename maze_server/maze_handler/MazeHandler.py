import pickle

from MazeGenerator import Maze


class MazeHandler:
    def __init__(self):
        nx, ny = 10,10  # Maze dimensions (ncols, nrows)
        ix, iy = 0, 0  # Maze entry position
        self.maze = Maze(nx, ny, ix, iy)
        self.maze.make_maze()
        # # pickle.dump(self.maze, open("testMaze.pickle", "wb"))
        # self.maze = pickle.load(open("testMaze.pickle", "rb"))
        self.team_locations = {}  # assume no duplicates

    def get_challenge(self, node):
        pass

    def get_location(self, team):
        return self.maze.cell_at(*self.team_locations[team])

    def get_maze(self):
        return self.maze

    def get_timeout(self, team, node):
        pass

    def register_team(self, team):
        self.team_locations[team] = self.maze.get_start_coords()
