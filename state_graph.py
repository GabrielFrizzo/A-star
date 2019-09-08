from heapq import heappush, heappop
from collections import deque, defaultdict
from maze import Maze
from sys import stdin, argv
from os import system

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
                return StateGraph.reconstruct_path(curr_state, predecessors), curr_cost
        return False

    def _DFSUtil(node, cost, visited, stack):
        if node.solved():
            return True

        visited.add(node)
        for nbor in StateGraph.next_states(node):
            stack.append((nbor['maze'], cost+nbor['cost'], node))

    def astar(self, heuristic=Maze.euclid_dist):
        predecessors = {self.root: None}
        costs = defaultdict(lambda: float("INF"))
        costs[self.root] = 0
        heap = [(0, self.root)]

        while heap:
            curr_cost, curr_node = heappop(heap)
            if curr_node.solved():
                return StateGraph.reconstruct_path(curr_node, predecessors), costs[curr_node]

            for nbor in StateGraph.next_states(curr_node):
                nx_node, cost = nbor['maze'], nbor['cost']
                next_cost = costs[curr_node] + cost
                if next_cost < costs[nx_node]:
                    predecessors[nx_node] = curr_node
                    costs[nx_node] = next_cost
                    heappush(heap, (next_cost+heuristic(nx_node), nx_node))

        return False


    def reconstruct_path(last_state, predecessors):
        path = deque([last_state])
        while predecessors[path[0]]:
            path.appendleft(predecessors[path[0]])
        return list(path)

if __name__ == '__main__':
    with open(argv[1], 'r') as file:
        graph = StateGraph(file.read())
    path, cost = graph.astar()
    for m in path:
        system("clear")
        print(m)
        input("Aperte ENTER para o próximo estado")
    print("Custo total:", cost)
