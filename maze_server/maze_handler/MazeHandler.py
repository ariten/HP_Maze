import pickle

from generator import Maze


class MazeHandler:
    def __init__(self):
        nx, ny = 10,10  # Maze dimensions (ncols, nrows)
        ix, iy = 0, 0  # Maze entry position
        self.maze = Maze(nx, ny, ix, iy)
        self.maze.make_maze()

        self.team_locations = {'team1': (ix, iy), 'team2': (ix, iy)}  # populate team names from django

    def get_challenge(self, node):
        pass

    def get_location(self, team):
        return self.maze.cell_at(*self.team_locations[team])

    def get_maze(self):
        return self.maze

    def get_timeout(self, team, node):
        pass

    def move_player(self, team, direction):
        pass
