from heapq import heappush, heappop
from collections import deque, defaultdict
from maze import Maze

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
        costs = defaultdict(lambda: float("INF"))

        while not path and depth < self.root.height*self.root.width*8:
            depth += 1
            path = self._DLS(depth, costs)
        return path

    def _DLS(self, depth, costs):
        stack = deque([(self.root,0, None, 0)])
        predecessors = {}

        while stack:
            curr_state, curr_cost, pred, curr_depth = stack.pop()
            if curr_cost > costs[curr_state] or curr_depth > depth:
                continue
            predecessors[curr_state] = pred
            costs[curr_state] = curr_cost

            if curr_state.solved():
                return StateGraph.reconstruct_path(curr_state, predecessors), curr_cost

            for nbor in StateGraph.next_states(curr_state):
                stack.append((nbor['maze'], curr_cost+nbor['cost'], curr_state, curr_depth+1))
        return False

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
