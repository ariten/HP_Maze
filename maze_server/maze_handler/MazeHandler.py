import pickle
import re

from datetime import datetime, timedelta
from maze_handler.MazeGenerator import Maze
from maze_handler.MazeRunner import MazeRunner

SECRET_SPELL = "PERICULUM"


class MazeHandler:
    def __init__(self, nx=50, ny=50, load_maze_file=None, save_maze_file=None):
        ix, iy = 0, 0  # Maze entry position

        if not load_maze_file==None:  # load pre-generated maze
            self.maze = pickle.load(open(load_maze_file, "rb"))
        else:  # generate maze
            self.maze = Maze(nx, ny, ix, iy)
            self.maze.make_maze()

        if not save_maze_file==None:  # save maze
            pickle.dump(self.maze, open(save_maze_file, "wb"))

        self.maze_runner = MazeRunner(self.get_maze())
        self.team_locations = {}  # assume no duplicates
        self.timeouts = {}
        self.escaped_teams = []
        self.team_answered_questions = {}

        print(self.maze)
        self.maze.write_svg("output_maze.svg")


    def game_over(self):
        trapped_teams = []
        for i in self.team_locations.keys():
            if i not in self.escaped_teams:
                trapped_teams.append(i)
        return trapped_teams

    def process_input(self, team, input):
        input_formatted = re.sub('[\W_]', '', input.upper())

        self.check_team(team)
        if team in self.escaped_teams:
            return {"info": "You have escaped, you can no longer move.", "score": 0, "timeout": 0}

        if input_formatted == 'EXIT':
            return self.try_exit(team)

        # if self.check_timeout(team):
        #     return "Time left before move " + self.get_remaining_time(team)

        if input_formatted.upper() in ['N', 'S', 'E', 'W']:  # direction
            return self.move_player(input_formatted, team)

        elif input_formatted == SECRET_SPELL:  # spell
            return self.try_spell_escape(team, input_formatted)

        elif self.get_location(team).state == 1:  # question node answer
            return self.validate_answer(team, input_formatted)

        else:
            return {"info": "Invalid input", "score": 0, "timeout": 0}

    def check_team(self, team):
        if team not in self.escaped_teams:
            if team not in self.team_locations.keys():
                self.register_team(team)

    def try_exit(self, team):
        if self.get_location(team).state == 2:  # end node
            self.escaped_teams.append(team)
            return {"info": "You have safely escaped the maze!", "score": 150, "timeout": 0}
        else:
            return {"info": "Naughty, you're not at the exit node.", "score": -1, "timeout": 0}

    def try_spell_escape(self, team, spell):
        # TODO: if not last 1.5 minutes
        self.escaped_teams.append(team)
        return {"info": "You have used a spell to escape!", "score": -0.25, "timeout": 0}

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

    # def get_remaining_time(self, team):
    #     if team in self.timeouts:
    #         event_time = self.timeouts[team]['set']
    #         delta = self.timeouts[team]['delta']
    #         return delta - (datetime.now() - event_time)
    #     else:
    #         return 0.0

    def register_team(self, team):
        self.team_locations.update({team: self.maze.get_start_coords()})
        self.team_answered_questions[team] = set()
        return {"info": "Team "+team+" registered.", "score": 0, "timeout": 0}

    def move_player(self, direction, team):
        location = self.get_location(team)
        response = self.maze_runner.run_direction(location, direction)

        if location.state == 1 and not location.get_coordinates() in self.team_answered_questions[team]:  # unanswered question node
            return {"info": "You have to answer the question before moving.", "score": -1, "timeout": 0}

        code = response[0]
        self.set_location(response[1].get_coordinates(), team)
        movements = response[2]
        if code == 4:
            return self.end_node(*response[2:])
        if code == 3:
            print("*****", self.team_answered_questions)
            return self.question(team, *response[1:])
        if code == 2:
            return self.deadend(*response[2:])
        if code == 1:
            return self.junction(*response[2:])

        # code == 0
        return {"info": "Invalid move, there is a wall in the way.", "score": 0, "timeout": 0}

    def set_location(self, location, team):
        self.team_locations.update({team: location})

    def end_node(self, prev_path, options):
        return {"info": "You have found the end of the maze! This is the path you followed:<br>"+str(prev_path)+"<br>Would you like to leave with 'Exit', or keep exploring?<br>"+str(['Exit']+options), "score": 0, "timeout": 0}

    def question(self, team, location, prev_path, options):
        if location.get_coordinates() in self.team_answered_questions[team]:
            info = "You have reached a question node that you have already answered by this path:<br>"+str(prev_path)+"<br>Where would you like to go next? "+str(options)
        else:
            info = "Taking these steps along a corridor have brought you to a question node. To continue, answer this question:<br>"+str(prev_path)+"<br>"+self.maze.get_cell_question(location)

        return {"info": info, "score": 0, "timeout": 0}

    def validate_answer(self, team, answer):
        location = self.get_location(team)
        coordinates = location.get_coordinates()
        options = location.no_wall_directions()

        if coordinates in self.team_answered_questions[team]:
            info = "You have already answered this question.<br>Where would you like to go next? "+str(options)
            return {"info": info, "score": 0, "timeout": 0}
        else:
            self.team_answered_questions[team].add(location.get_coordinates())
            answer_formatted = re.sub('[\W_]', '', answer.lower())

            if answer_formatted in self.maze.get_cell_answer(location):
                return {"info": "Correct answer. Which way do you want to go next?<br>"+str(options), "score": 50, "timeout": 0}
            else:
                return {"info": "Wrong answer, 10 second time penalty. Which way do you want to go next?<br>"+str(options), "score": 0, "timeout": 10}

    def junction(self, prev_path, options):
        info = "Taking these steps along a corridor have brought you to a junction:<br>"+str(prev_path)+"<br>Which way do you want to go?<br>"+str(options)
        return {"info": info, "score": 0, "timeout": 0}

    def deadend(self, prev_path, options):
        return {"info": "Following this path, you have reached a dead end:<br>"+str(prev_path)+"<br>Turn back: "+str(options), "score": 0, "timeout": 0}
