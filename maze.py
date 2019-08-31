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

class Maze:
    def __init__(self, matrix=None, height=None, width=None, agent=None):
        if matrix:
            self.matrix = matrix
            self.height = height or len(matrix)
            self.width = width or len(matrix[0])
            self.agent = agent or self._find_agent()

    def from_txt(entry):
        maze = Maze()
        maze.height, maze.width, maze.matrix = parse_entry(entry)
        maze.agent = maze._find_agent()

        return maze

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
