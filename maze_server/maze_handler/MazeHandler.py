import pickle
import re

from maze_server.maze_handler.MazeGenerator import Maze
from maze_server.maze_handler.MazeRunner import MazeRunner


SECRET_SPELL = "EXIT"


class MazeHandler:
    def __init__(self):
        nx, ny = 10,10  # Maze dimensions (ncols, nrows)
        ix, iy = 0, 0  # Maze entry position
        self.maze = Maze(nx, ny, ix, iy)
        self.maze.make_maze()
        self.maze_runner = MazeRunner(self.get_maze())
        self.team_locations = {}  # assume no duplicates


    def process_input(self, team, input):
        if input.upper() in ['N', 'S', 'E', 'W']:  # direction
            return self.move_player(input, team)
        elif input == SECRET_SPELL:  # spell
            return self.try_escape(team, input)
        elif self.get_location(team).state == 1:  # answer
            return self.validate_answer(team, answer)
        else:
            return "Invalid input"


    def try_escape(self, team, spell):
        # if not last 1.5 minutes
        # TODO: Deduct score
        return "You have escaped!"


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
            info_string = self.end_node(team)
            return info_string # TODO: add options if not exiting
        if code == 3:
            info_string = self.question(team, self.get_location(team))
            return info_string # TODO: options for after the question is answered
        if code == 2:
            info_string = self.deadend(team) ### returns current position instead of deadend?
            return info_string # TODO: options for turning back
        if code == 1:
            return self.junction(response[3])
        if code == 0:
            return "Invalid move, there is a wall in the way."

        # TODO: return past moves and current options
        return "Move processed (TODO: details)"


    def set_location(self, location, team):
        self.team_locations.update({team: location})


    def end_node(self):
        return "You have found the end of the maze! Would you like to leave, or keep exploring?"


    def question(self, team, location):
        # TODO: Track which questions have already been answered
        """Returns the question as a string."""
        return self.maze.get_cell_question(location)


    def validate_answer(self, team, answer):
        answer_formatted = re.sub('[\W_]', '', answer.lower())
        location = self.get_location(team).get_coordinates()

        if answer_formatted in self.maze.get_cell_answer(location):
            # TODO: add score
            return "Correct answer"
        else:
            # TODO: add timeout
            return "Wrong answer"


    def junction(self, options):
        return {'info': "You have reached a junction. Which way do you want to go?", 'options': options}


    def deadend(self, team):
        return "You have reached a dead end."
