from math import sqrt
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
    def __init__(self, matrix, agent=None, obj_pos=None):
        self.matrix = matrix
        self.height = len(matrix)
        self.width = len(matrix[0])

        self.obj_pos = obj_pos or self._find_objective()

        self.agent = agent or self._find_agent()
        self.matrix[self.agent['pos']['y']][self.agent['pos']['x']] = '.'

    def from_txt(entry):
        return Maze(parse_entry(entry)[2])

    def copy(self, agent_pos = None, agent_dir = None):
        agent = {'pos': agent_pos or self.agent['pos'],
                 'dir': agent_dir or self.agent['dir']
                 }

        return Maze(self.matrix, agent, self.obj_pos)

    def __repr__(self):
        return build_output(self.matrix, self.agent, self.obj_pos)

    def _find_agent(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.pos(x,y) in POSITIONS.keys():
                    return { 'pos': {'x': x, 'y': y}, 'dir': self.pos(x,y) }

    def _find_objective(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.pos(x,y) == 'x':
                    return {'x': x, 'y': y}

    def pos(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return '*'

        return self.matrix[y][x]

    def rotations(self):
        current_dir = self.agent['dir']
        current_pos = self.agent['pos']
        nx_states = []

        for direction in ROTATIONS[current_dir]:
            new_maze = self.copy(agent_dir=direction)
            nx_states.append({'cost': 1, 'maze': new_maze})

        return nx_states

    def movement(self):
        current_dir = self.agent['dir']
        current_pos = self.agent['pos']

        next_pos = {'x': current_pos['x'] + POSITIONS[current_dir][0],
                    'y': current_pos['y'] + POSITIONS[current_dir][1]
                    }
        if self.pos(next_pos['x'], next_pos['y']) != '*':
            new_maze = self.copy(next_pos)
            cost = 1 if 0 in POSITIONS[current_dir] else 1.5
            return {'cost': cost, 'maze': new_maze}

    def solved(self):
        if self.agent['pos'] == self.obj_pos:
            return True
        return False

    def euclid_dist(self):
        agent_pos = self.agent['pos']
        obj_pos = self.obj_pos
        return sqrt((agent_pos['x']**2 -obj_pos['x'])**2 + \
                    (agent_pos['y']**2 -obj_pos['y'])**2)

    def __hash__(self):
        return hash((self.agent['pos']['x'], self.agent['pos']['y'], self.agent['dir']))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __lt__(self, other):
        return True