import os


class SideHandler:

    def __init__(self):
        self.question_1_teams = []
        self.question_2_teams = []
        self.question_3_teams = []
        self.question_4_teams = []

    def handle(self, question, answer, team):
        if question == 1:
            if team in self.question_1_teams:
                return ['You have answered Question 1', '', 0]
            elif self.question_1(answer):
                self.question_1_teams.append(team)
                return ["Success", '2p8934u5.JPG', 100]  # Top Left
        elif question == 2:
            if team in self.question_2_teams:
                return ['You have answered Question 2', '', 0]
            elif self.question_2(answer):
                self.question_2_teams.append(team)
                return ["Success", '2p8956gc.JPG', 100]  # Bottom Left
        elif question == 3:
            if team in self.question_2_teams:
                return ['You have answered Question 3', '', 0]
            elif self.question_3(answer):
                self.question_3_teams.append(team)
                return ["Success", '2p894des.JPG', 100]  # Top Right
        elif question == 4:
            if team in self.question_2_teams:
                return ['You have answered Question 4', '', 0]
            elif self.question_4(answer):
                self.question_4_teams.append(team)
                return ["Success", '2p894des.JPG', 100]  # Top Right
        else:
            return ['Incorrect', '', 0]

    def question_1(self, answer):
        actual_answer = 'rubeus hagrid'
        return answer.lower() == actual_answer

    def question_2(self, answer):
        actual_answer = 'crookshanks'
        if answer.lower() == actual_answer:
            return ["Success", '2p89k65c.JPG', 100]  # Bottom Right
        else:
            return ['Incorrect', '', 0]

    def question_3(self, answer):
        actual_answer = 'nymphadora'
        return answer.lower() == actual_answer

    def question_4(self, answer):
        actual_answer = 'lunalovegood'
        return answer.lower() == actual_answer
