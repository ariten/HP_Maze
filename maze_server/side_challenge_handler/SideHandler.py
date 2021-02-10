import os


class SideHandler:

    def __init__(self):
        self.question_1_teams = []
        self.question_2_teams = []
        self.question_3_teams = []
        self.question_4_teams = []
        self.question_1_hints = []
        self.question_2_hints = []
        self.question_3_hints = []
        self.question_4_hints = []
        self.stats = {}

    def hint_handler(self, question, team):
        if question == 1:
            return self.hint_question_1(team)
        elif question == 2:
            return self.hint_question_2(team)
        elif question == 3:
            return self.hint_question_3(team)
        elif question == 4:
            return self.hint_question_4(team)
        else:
            return "Invalid Hint"

    def register_team(self, team):
        self.stats.update({team: 0})

    def handle(self, question, answer, team):
        if question == 1:
            if team in self.question_1_teams:
                return ("Success", '2p8934u5.JPG', 0)
            elif self.question_1(answer):
                self.question_1_teams.append(team)
                self.add_stat(team)
                if team in self.question_1_hints:
                    return "Success", '2p8934u5.JPG', 50
                return ("Success", '2p8934u5.JPG', 100)  # Top Left
        elif question == 2:
            if team in self.question_2_teams:
                return ("Success", '2p8956gc.JPG', 0)
            elif self.question_2(answer):
                self.question_2_teams.append(team)
                self.add_stat(team)
                if team in self.question_2_hints:
                    return ("Success", '2p8956gc.JPG', 50)
                return ("Success", '2p8956gc.JPG', 100)  # Bottom Left
        elif question == 3:
            if team in self.question_3_teams:
                return ("Success", '2p894des.JPG', 0)
            elif self.question_3(answer):
                self.question_3_teams.append(team)
                self.add_stat(team)
                if team in self.question_3_hints:
                    return ("Success", '2p894des.JPG', 50)
                return ("Success", '2p894des.JPG', 100)  # Top Right
        elif question == 4:
            if team in self.question_4_teams:
                return ("Success", '2p89k65c.JPG', 0)
            elif self.question_4(answer):
                self.question_4_teams.append(team)
                self.add_stat(team)
                if team in self.question_4_hints:
                    return ("Success", '2p89k65c.JPG', 50)
                return ("Success", '2p89k65c.JPG', 100)  # Top Right
        return ('Incorrect', '', 0)

    def add_stat(self, team):
        self.stats.update({team: self.stats[team] + 1})

    def get_stats(self):
        return self.stats

    def question_1(self, answer):
        actual_answer = 'rubeus hagrid'
        return answer.lower() == actual_answer

    def question_2(self, answer):
        actual_answer = 'crookshanks'
        return answer.lower() == actual_answer

    def question_3(self, answer):
        actual_answer = 'nymphadora'
        return answer.lower() == actual_answer

    def question_4(self, answer):
        actual_answer = 'lunalovegood'
        return answer.lower() == actual_answer

    def hint_question_1(self, team):
        if team not in self.question_1_hints:
            self.question_1_hints.append(team)
        return "Think back to the roman times, this cipher was inspired by one of the famous Rulers"

    def hint_question_2(self, team):
        if team not in self.question_2_hints:
            self.question_2_hints.append(team)
        return "Think about how letters are represented on computers"

    def hint_question_3(self, team):
        if team not in self.question_3_hints:
            self.question_3_hints.append(team)
        return "Think back to the first question, maybe try from a different elgna"

    def hint_question_4(self, team):
        if team not in self.question_4_hints:
            self.question_4_hints.append(team)
        return "The key to this cracking this cipher is hidden in the house Rowena founded"
