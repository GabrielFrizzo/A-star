from copy import deepcopy
from map_parser import parse_entry, build_output

POSITIONS = {
    'v': (0,1),
    '^': (0,-1),
    '>': (1,0),
    '<': (-1,0),
    '\\': (1,1),
    '/': (1,-1),
    '#': (-1,1),
    '%': (-1,-1),
}

ROTATIONS = {
    'v': ('\\', '#'),
    '^': ('/', '%'),
    '>': ('\\', '/'),
    '<': ('#', '%'),
    '\\': ('v', '>'),
    '/': ('^', '>'),
    '#': ('v', '<'),
    '%': ('^', '<'),
}

class Maze:
    def __init__(self, matrix):
        self.matrix = matrix
        self.height = len(matrix)
        self.width = len(matrix[0])
        self.agent = self._find_agent()

    def from_txt(entry):
        return Maze(parse_entry(entry)[2])

    def __repr__(self):
        return build_output(self.matrix)

    def _find_agent(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.pos(x,y) in POSITIONS.keys():
                    return { 'pos': {'x': x, 'y': y}, 'dir': self.pos(x,y)}

    def pos(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return '*'

        return self.matrix[y][x]

    def rotations(self):
        current_dir = self.agent['dir']
        current_pos = self.agent['pos']
        nx_states = []

        for direction in ROTATIONS[current_dir]:
            new_matrix = deepcopy(self.matrix)
            new_matrix[current_pos['y']][current_pos['x']] = direction
            new_maze = Maze(new_matrix)
            nx_states.append({'cost': 1, 'maze': new_maze})

        return nx_states

    def movement(self):
        current_dir = self.agent['dir']
        current_pos = self.agent['pos']

        next_pos = [sum(x) for x in zip(current_pos.values(),POSITIONS[current_dir])]
        if self.pos(next_pos[0], next_pos[1]) != '*':
            new_matrix = deepcopy(self.matrix)
            new_matrix[current_pos['y']][current_pos['x']] = '.'
            new_matrix[next_pos[1]][next_pos[0]] = current_dir

            new_maze = Maze(new_matrix)
            cost = 1.25 if any(POSITIONS[current_dir]) else 1
            return {'cost': cost, 'maze': new_maze} 