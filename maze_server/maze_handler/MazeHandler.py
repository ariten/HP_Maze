import pickle

from maze_server.maze_handler.MazeGenerator import Maze
from maze_server.maze_handler.MazeRunner import MazeRunner


class MazeHandler:
    def __init__(self):
        nx, ny = 10,10  # Maze dimensions (ncols, nrows)
        ix, iy = 0, 0  # Maze entry position
        self.maze = Maze(nx, ny, ix, iy)
        self.maze.make_maze()
        self.maze_runner = MazeRunner(self.get_maze())
        # # pickle.dump(self.maze, open("testMaze.pickle", "wb"))
        # self.maze = pickle.load(open("testMaze.pickle", "rb"))
        self.team_locations = {}  # assume no duplicates

    def create_maze(self):
        self.maze.make_maze()

    def create_team(self, team):
        self.team_locations.update({team: (0, 0)})

    def get_location(self, team):
        return self.maze.cell_at(*self.team_locations[team])

    def get_maze(self):
        return self.maze

    def get_timeout(self, team, node):
        pass

    # create_team
    def register_team(self, team):
        self.team_locations.update({team: self.maze.get_start_coords()})

    def move_player(self, direction, team):
        location = self.get_location(team)
        response = self.maze_runner.run_direction(location, direction)
        code = response[0]
        self.set_location(response[1].get_coordinates(), team)
        movements = response[2]
        if code == 4:
            self.end_node()
        if code == 3:
            self.question()
        if code == 2:
            self.deadend()
        if code == 1:
            self.junction(response[3])
        if code == 0:
            print("Invalid Move")

    def set_location(self, location, team):
        self.team_locations.update({team: location})


    def end_node(self):
        print("END NODE")

    def question(self):
        print("Question")

    def junction(self, possible_moves):
        print("Junction")
        print(possible_moves)

    def deadend(self):
        print("Deadend")

mh = MazeHandler()
