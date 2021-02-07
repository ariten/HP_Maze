import pickle
import re

from datetime import datetime, timedelta
from maze_server.maze_handler.MazeGenerator import Maze
from maze_server.maze_handler.MazeRunner import MazeRunner
from maze_server.maze.models import Team

SECRET_SPELL = "EXIT"


class MazeHandler:
    def __init__(self):
        nx, ny = 10, 10  # Maze dimensions (ncols, nrows)
        ix, iy = 0, 0  # Maze entry position
        self.maze = Maze(nx, ny, ix, iy)
        self.maze.make_maze()
        self.maze_runner = MazeRunner(self.get_maze())
        self.team_locations = {}  # assume no duplicates
        self.timeouts = {}
        self.teams = []
        self.escaped_teams = []

    def game_over(self):
        trapped_teams = []
        for i in self.teams:
            if i not in self.escaped_teams:
                trapped_teams.append(i)
        return trapped_teams

    def process_input(self, team, input):
        self.check_team(team)
        if team in self.escaped_teams:
            return "You have escaped, you can no longer move", False, 0
        if self.check_timeout(team):
            return "Time left before move " + self.get_remaining_time(team)
        if input.upper() in ['N', 'S', 'E', 'W']:  # direction
            return self.move_player(input, team)
        elif input == SECRET_SPELL:  # spell
            return self.try_escape(team, input)
        elif self.get_location(team).state == 1:  # answer
            return self.validate_answer(team, input)
        else:
            return {"info": "Invalid input", "score": 0, "timeout": 0}

    def check_team(self, team):
        if team not in self.escaped_teams:
            if team not in self.teams:
                self.teams.append(team)

    def try_escape(self, team, spell):
        # if not last 1.5 minutes
        # TODO: Deduct score
        self.deduct_percentage(team, 0.25)
        return "You have escaped!", False, 0

    def get_location(self, team):
        return self.maze.cell_at(*self.team_locations[team])

    def get_maze(self):
        return self.maze

    def set_timeout(self, team, amount):
        self.timeouts.update({team: {'set': datetime.now(), 'delta': timedelta(seconds=amount)}})

    def check_timeout(self, team):
        if team in self.timeouts:
            event_time = self.timeouts[team]['set']
            delta = self.timeouts[team]['delta']
            gap = datetime.now() - event_time
            if gap > delta:
                # if timeout has passed
                self.timeouts.pop(team)
                return False
            else:
                # if still in a time penalty
                return True
        else:
            # if there are no time penalty's against the team
            return False

    def get_remaining_time(self, team):
        if team in self.timeouts:
            event_time = self.timeouts[team]['set']
            delta = self.timeouts[team]['delta']
            return delta - (datetime.now() - event_time)
        else:
            return 0.0

    def register_team(self, team):
        self.team_locations.update({team: self.maze.get_start_coords()})

        return {"info": "Team "+team+" registered.", "score": 0, "timeout": 0}

    def move_player(self, direction, team):
        # TODO: don't let team move if on unanswered question node
        location = self.get_location(team)
        response = self.maze_runner.run_direction(location, direction)
        print(self.team_locations)

        code = response[0]
        self.set_location(response[1].get_coordinates(), team)
        movements = response[2]
        if code == 4:
            info_string = self.end_node(team)
            return info_string # TODO: add options if not exiting
        if code == 3:
            # TODO: check if team has answered question
            return self.question(*response[1:3])
        if code == 2:
            return self.deadend(*response[2:])
        if code == 1:
            return self.junction(*response[2:])

        # code == 0
        return {"info": "Invalid move, there is a wall in the way.", "score": 0, "timeout": 0}

    def set_location(self, location, team):
        self.team_locations.update({team: location})

    def end_node(self):
        # TODO: add options
        return {"info": "You have found the end of the maze! Would you like to leave, or keep exploring?", "score": 0, "timout": 0}

    def question(self, location, prev_path):
        # TODO: Track which questions have already been answered
        info = "Taking these steps along a corridor have brought you to a question node. To continue, answer this question:<br>"+str(prev_path)+"<br>"+self.maze.get_cell_question(location)
        return {"info": info, "score": 0, "timeout": 0}

    def validate_answer(self, team, answer):
        answer_formatted = re.sub('[\W_]', '', answer.lower())
        location = self.get_location(team)
        options = location.no_wall_directions()

        if answer_formatted in self.maze.get_cell_answer(location):
            return {"info": "Correct answer. Which way do you want to go next?<br>"+str(options), "score": 50, "timeout": 0}
        else:
            return {"info": "Wrong answer, 10 second time penalty. Which way do you want to go next?<br>"+str(options), "score": 0, "timeout": 10}

    def junction(self, prev_path, options):
        info = "Taking these steps along a corridor have brought you to a junction:<br>"+str(prev_path)+"<br>Which way do you want to go?<br>"+str(options)
        return {"info": info, "score": 0, "timeout": 0}

    def deadend(self, prev_path, options):
        return {"info": "Following this path, you have reached a dead end:<br>"+str(prev_path)+"<br>Turn back: "+str(options), "score": 0, "timeout": 0}

