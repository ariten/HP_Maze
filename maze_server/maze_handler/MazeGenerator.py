import json
import random
import re


"""
credit too Christian, github username:xnx, link to code https://github.com/scipython/scipython-maths/tree/master/maze
"""


class Cell:
    """
    A cell in the maze
    """
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """
        Initialize the cell at (x,y). At first it is surrounded by walls.
        States;
        0: path
        1: Question point
        2: End Point
        3: Start Point
        """
        self.x = x
        self.y = y
        self.state = 0
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}


    def __str__(self):
        cell_states_dict = {0: 'path', 1: 'question', 2: 'end', 3: 'start'}
        return "CELL ("+str(self.x)+","+str(self.y)+")  |  TYPE: "+cell_states_dict[self.state]+"  |  WALLS: "+json.dumps(self.walls)


    def has_wall(self, direction):
        return self.walls[direction]


    def get_wall_count(self):
        return sum(self.walls.values())


    def change_state(self, state):
        self.state = state


    def get_coordinates(self):
        return self.x, self.y


    def has_all_walls(self):
        return all(self.walls.values())


    def knock_down_wall(self, other, wall):
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False



class Maze:
    """
    The overarching Maze
    """
    def __init__(self, nx, ny, ix=0, iy=0):
        """
        initialise the maze grid. The maze consists of nx x ny cells,
        starts will all walls true and no paths

        ix & iy  are the start point in the maze
        """
        self.nx = nx
        self.ny = ny
        self.ix = ix
        self.iy = iy

        self.qa_lookup = dict()  # e.g. {qnode_id: {'coord': 5, 29, 'question': question, 'answer': answer}}

        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]


    def cell_at(self, x, y):
        return self.maze_map[x][y]


    def get_start_coords(self):
        return (self.ix, self.iy)


    def __str__(self):
        """
        return a crude string version of the maze
        """
        maze_rows = ['-' * self.nx * 2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E'] and self.maze_map[x][y].state == 1:
                    maze_row.append('Q|')
                elif self.maze_map[x][y].walls['E'] and self.maze_map[x][y].state == 2:
                    maze_row.append('C|')
                elif self.maze_map[x][y].walls['E'] and self.maze_map[x][y].state == 3:
                    maze_row.append('S|')
                elif self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                elif self.maze_map[x][y].state == 1:
                    maze_row.append('Q ')
                elif self.maze_map[x][y].state == 2:
                    maze_row.append('C ')
                elif self.maze_map[x][y].state == 3:
                    maze_row.append('S ')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)


    def write_svg (self, filename):
        """
        Write the maze into a SVG file
        :param filename: The file name of the SVG file
        """
        aspect_ratio = self.nx / self.ny
        # Pad the maze all ar+ound by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 1000
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ny, width / self.nx

        def write_wall(ww_f, ww_x1, ww_y1, ww_x2, ww_y2):
            """Write a single wall to the SVG image file handle f."""

            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'
                  .format(ww_x1, ww_y1, ww_x2, ww_y2), file=ww_f)

        # Write the SVG image file for maze
        with open(filename, 'w') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                  .format(width + 2 * padding, height + 2 * padding,
                          -padding, -padding, width + 2 * padding, height + 2 * padding),
                  file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 5;\n}', file=f)
            print(']]></style>\n</defs>', file=f)
            # Draw the "South" and "East" walls of each cell, if present (these
            # are the "North" and "West" walls of a neighbouring cell in
            # general, of course).
            for x in range(self.nx):
                for y in range(self.ny):
                    if self.cell_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
            print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height), file=f)
            print('</svg>', file=f)


    def find_valid_neighbours(self, cell):
        """
        return a list of unvisited neighbouring cells
        :param cell: instance of cell
        """
        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours


    def make_maze(self):
        """
        algorithm that creates the maze and adds the path using unvisited nodes to create the maze
        """
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                current_cell = cell_stack.pop()
                continue

            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1
        self.cell_at(random.randint(self.nx%10, self.nx-1), random.randint(self.ny%10, self.ny-1)).change_state(2)

        nr_qas = 5
        question_and_answers = self.get_question_selection(nr_qas)

        for x in range(nr_qas):
            question_cell = self.cell_at(random.randint(1, self.nx - 1), random.randint(1, self.ny - 1))
            question_cell.change_state(1)

            self.qa_lookup[(question_cell.x, question_cell.y)] = question_and_answers[x]

        self.cell_at(self.ix, self.iy).change_state(3)


    def get_cell_question(self, coordinates):
        try: return self.qa_lookup[coordinates]['Q']
        except KeyError: return "ERROR: Incorrect coordinates, not a question node."


    def get_cell_answer(self, coordinates):
        try: return self.qa_lookup[coordinates]['A']
        except KeyError: return "ERROR: Incorrect coordinates, not a question node."


    def get_question_selection(self, n=5, qa_filename="questions_and_answers.csv"):
        """n: number of question nodes"""
        with open(qa_filename, 'r') as f:
            nr_qas = len(f.readlines())
            f.seek(0)

            sample_ids = random.sample(range(nr_qas), n)

            qas = list()
            for i, qa in enumerate(f):
                if i in sample_ids:
                    qas.append(qa)

        qas_formatted = [{'Q': qa.split('","')[0].replace('"', ''), \
                          'A': [re.sub('[\W_]', '', a.lower()) for a in qa.split('","')[1].split(",")]} \
                          for qa in qas]

        return qas_formatted