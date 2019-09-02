from maze import Maze
from sys import stdin

class StateGraph:
    def __init__(self, txt_entry):
        self.root = Maze.from_txt(txt_entry)

    def next_states(maze):
        rotations =  maze.rotations()
        movement = maze.movement()
        return rotations + [movement] if movement else rotations

graph = StateGraph(stdin.read())
for state in StateGraph.next_states(graph.root):
    print(state['cost'])
    print(state['maze'])
