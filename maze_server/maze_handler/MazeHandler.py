import pickle
import re

from datetime import datetime, timedelta
from maze_server.maze_handler.MazeGenerator import Maze
from maze_server.maze_handler.MazeRunner import MazeRunner
from maze_server.maze.models import Team

SECRET_SPELL = "EXIT"


class MazeHandler:
    def __init__(self):
        self.start_time = 0
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
            return "Time left before move " + self.get_remaining_time(team), False, 0
        if input.upper() in ['N', 'S', 'E', 'W']:  # direction
            return self.move_player(input, team)
        elif input == SECRET_SPELL:  # spell
            return self.try_escape(team, input)
        elif self.get_location(team).state == 1:  # answer
            return self.validate_answer(team, input)
        else:
            return "Invalid input", False, 0

    def check_team(self, team):
        if team not in self.escaped_teams:
            if team not in self.teams:
                self.teams.append(team)

    def try_escape(self, team, spell):
        # if not last 1.5 minutes
        ##### TODO: Deduct score
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

    # create_team
    def register_team(self, team):
        self.team_locations.update({team: self.maze.get_start_coords()})
        self.set_score(team, 0)

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
            return "Invalid move, there is a wall in the way.", False, 0

        # TODO: return past moves and current options
        return "Move processed (TODO: details)"

    def set_location(self, location, team):
        self.team_locations.update({team: location})

    def end_node(self):
        # TODO we need to have a method of tell us they want to escape, maybe a command 'escape'?+
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
            self.add_score(team, 50)
            return "Correct answer"
        else:
            ##### TODO: add timeout
            self.set_timeout(team, 9)
            return "Wrong answer, 10 second time penalty", True, 10

    def junction(self, options):
        return {'info': "You have reached a junction. Which way do you want to go?", 'options': options}

    def deadend(self, team):
        return "You have reached a dead end."

    def add_score(self, team, amount):
        score = self.get_score(team)
        score += amount
        self.set_score(team, score)

    def deduct_percentage(self, team, percentage):
        score = self.get_score(team)
        score *= percentage
        self.set_score(team, score)

    def get_score(self, team):
        q = Team.objects.get(team_name=team)
        return q.score

    def set_score(self, team, score):
        team = Team.objects.get(team_name=team)
        team.score = score
        team.save()
