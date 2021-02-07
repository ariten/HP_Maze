import os


class SideHandler:

    def __init__(self):
        pass

    def handle(self, question, answer):
        if question == 1:
            return self.question_1(answer)
        elif question == 2:
            return self.question_2(answer)
        elif question == 3:
            return self.question_3(answer)
        elif question == 4:
            return self.question_4(answer)

    def question_1(self, answer):
        actual_answer = 'rubeus hagrid'
        if answer.lower() == actual_answer:
            return ["Success", '2p8934u5', 100]
        else:
            return ['Incorrect', '', 0]

    def question_2(self, answer):
        actual_answer = 'crookshanks'
        if answer.lower() == actual_answer:
            return ["Success", '2p8956gc', 100]
        else:
            return ['Incorrect', '', 0]

    def question_3(self, answer):
        actual_answer = 'nymphadora'
        if answer.lower() == actual_answer:
            return ["Success", '2p894des', 100]
        else:
            return ['Incorrect', '', 0]

    def question_4(self, answer):
        actual_answer = 'lunalovegood'
        if answer.lower() == actual_answer:
            return ["Success", '2p89k65c', 100]
        else:
            return ['Incorrect', '', 0]
