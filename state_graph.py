import networkx as nx
from maze import Maze, POSITIONS
from sys import stdin
from copy import deepcopy

class StateGraph:
    def __init__(self):
        self.root = Maze.from_txt(stdin.read())

    def next_states(maze):
        current_dir = maze.agent['dir']
        current_pos = maze.agent['pos']
        h = maze.height
        w = maze.width
        nx_states = []

        #rotations
        for direction in POSITIONS.keys():
            if direction != current_dir:
                new_matrix = deepcopy(maze.matrix)
                new_matrix[current_pos['y']][current_pos['x']] = direction
                new_maze = Maze(new_matrix, height=h, width=w)
                nx_states.append({'cost': 1, 'maze': new_maze})

        #movement
        next_pos = list(current_pos.values()) + list(POSITIONS[current_dir])
        if maze.pos(next_pos[0], next_pos[1]) != '*':
            new_matrix = deepcopy(maze.matrix)
            new_matrix[current_pos['y']][current_pos['x']] = '.'
            new_matrix[next_pos[1]][next_pos[0]] = current_dir

            new_maze = Maze(new_matrix, height=h, width=w)
            cost = 1.25 if any(POSITIONS[current_dir]) else 1
            nx_states.append({'cost': cost, 'maze': new_maze})

        return nx_states

graph = StateGraph()
for state in StateGraph.next_states(graph.root):
    print(state['cost'])
    print(state['maze'])