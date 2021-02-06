
class MazeRunner:
    def __init__(self, maze):
        self.maze = maze

    def run_direction(self, location, direction):
        print(direction)
        sx, sy = location.get_coordinates()
        direction_moves = 0
        movements = []
        flag = True
        delta = {'W': (-1, 0),
                 'E': (1, 0),
                 'S': (0, 1),
                 'N': (0, -1)}
        if location.has_wall(direction):
            # if the option provided is not possible
            code = [0, location, movements]
            return code
        while flag:
            dx, dy = delta[direction]
            x, y = location.get_coordinates()
            location = self.maze.cell_at(x + dx, y + dy)
            direction_moves += 1
            if location.state == 1:
                return self.question_node(location, movements)
            if location.state == 2:
                return self.end_node(location, movements)
            walls = self.count_walls(location)
            if walls == 3:
                movements.append([direction, direction_moves])
                return self.deadend(sx, sy, movements)
            elif walls <= 1:
                movements.append([direction, direction_moves])
                return self.junction(direction, location, movements)
            else:
                print("HERE")
                path_direction = self.direction(location, direction)
                print(path_direction)
                if path_direction != direction:
                    movements.append([direction, direction_moves])
                    direction = path_direction
                    direction_moves = 0

    def direction(self, cell, direction):
        inverse = {
            'N': 'S',
            'S': 'N',
            'E': 'W',
            'W': 'E'
        }
        backwards = inverse[direction]
        direction_combos = ['N', 'S', 'E', 'W']
        direction_combos.remove(backwards)
        for i in direction_combos:
            if not cell.has_wall(i):
                return i

    def count_walls(self, cell):
        count = 0
        if cell.has_wall('N'):
            count += 1
        if cell.has_wall('S'):
            count += 1
        if cell.has_wall('E'):
            count += 1
        if cell.has_wall('W'):
            count += 1
        return count

    def end_node(self, location, movements):
        code = [4, location, movements]
        return code

    def question_node(self, location, movements):
        code = [3, location, movements]
        return code

    def deadend(self, sx, sy, movements):
        location = self.maze.cell_at(sx, sy)
        code = [2, location, movements]
        return code

    def junction(self, direction, location, movements):
        inverse = {
            'N': 'S',
            'S': 'N',
            'E': 'W',
            'W': 'E'
        }
        backwards = inverse[direction]
        direction_combos = ['N', 'S', 'E', 'W']
        direction_combos.remove(backwards)
        possible_moves = [backwards]
        for i in direction_combos:
            if not location.has_wall(i):
                possible_moves.append(i)
        code = [1, location, movements, possible_moves]
        return code
