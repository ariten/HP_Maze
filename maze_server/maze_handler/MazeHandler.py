from maze_server.maze_handler.MazeGenerator import Maze
from maze_server.maze_handler.MazeRunner import MazeRunner


class MazeHandler:
    def __init__(self):
        self.maze = Maze(10, 10, 0, 0)
        self.maze_runner = MazeRunner(self.get_maze())
        self.team_location = {}

    def create_maze(self):
        self.maze.make_maze()
        print(self.maze)

    def create_team(self, team):
        self.team_location.update({team: (0, 0)})

    def get_location(self, team):
        return self.maze.cell_at(*self.team_location[team])

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
        self.team_location.update({team: location})

    def get_maze(self):
        return self.maze

    def end_node(self):
        print("END NODE")

    def question(self):
        print("Question")

    def junction(self, possible_moves):
        print("Junction")
        print(possible_moves)

    def deadend(self):
        print("Deadend")
