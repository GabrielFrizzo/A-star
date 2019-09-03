from collections import deque, defaultdict
from maze import Maze
from sys import stdin

class StateGraph:
    def __init__(self, txt_entry):
        self.root = Maze.from_txt(txt_entry)

    def next_states(maze):
        rotations =  maze.rotations()
        movement = maze.movement()
        return rotations + [movement] if movement else rotations

    def deepening_search(self):
        depth = 0
        path = False
        while not path:
            depth += 1
            path = self._DFS(depth)
        return path

    def _DFS(self, depth):
        visited = set()
        stack = deque([(self.root,0, None)])
        predecessors = {}
        costs = defaultdict(lambda: float("INF"))

        while stack:
            curr_state, curr_cost, pred = stack.pop()
            if curr_cost > depth or curr_cost >= costs[curr_state]:
                continue
            predecessors[curr_state] = pred
            costs[curr_state] = curr_cost

            if StateGraph._DFSUtil(curr_state, curr_cost, visited, stack):
                path = deque([curr_state])
                while predecessors[path[0]]:
                    path.appendleft(predecessors[path[0]])

                return list(path), curr_cost
        return False

    def _DFSUtil(node, cost, visited, stack):
        if node.solved():
            return True

        visited.add(node)
        for nbor in StateGraph.next_states(node):
            stack.append((nbor['maze'], cost+nbor['cost'], node))

if __name__ == '__main__':
    graph = StateGraph(stdin.read())
    path, cost = graph.deepening_search()
    for m in path:
        print(m)
        print(m.agent)
    print(cost)
