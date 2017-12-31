from SearchSolution import SearchSolution
from heapq import heappush, heappop


class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost

    def priority(self):
        return self.heuristic + self.transition_cost
        # you write this part


    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result

def find_cost(solution):
    path = solution.path
    prev_state = path[0]
    solution.cost = 0

    for cur_state in path:
        if prev_state[1:] != cur_state[1:]:
            solution.cost += 1

        prev_state = cur_state

def astar_search(search_problem, heuristic_fn):
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[tuple(start_node.state)] = 0

    while len(pqueue) != 0:
        current_node = heappop(pqueue)

        if current_node != start_node and current_node.state in visited_cost.keys():
            continue

        visited_cost[tuple(current_node.state)] = current_node.transition_cost

        # print("queue length is " + str(len(pqueue)))
        # print("popped " + str(current_node.state))
        visited_cost[tuple(current_node.state)] = current_node.transition_cost
        search_problem.update_loc(current_node.state)
        # search_problem.maze.robotloc = current_node.state[1:]
        solution.nodes_visited += 1

        # if search_problem.is_goal(current_node.state):
        #     path = backchain(current_node)
        #     solution.path = path
        #     return solution

        if search_problem.is_goal(current_node.state):
            print("found")
            path = backchain(current_node)
            solution.path = path
            find_cost(solution)
            return solution

        successors = search_problem.get_successors(current_node.state)
        # print("this is your successor list " + str(successors))

        for successor in successors:
            # cost = current_node.transition_cost
            # cost += 1 if successor[1:] != current_node.state[1:] else 0
            #
            # if successor[1:] != current_node.state[1:]:
            #     cost = current_node.transition_cost + 1
            # else:
            #     cost = current_node.transition_cost

            cost = current_node.transition_cost + 1

            new_node = AstarNode(successor, heuristic_fn(successor), current_node, cost)

            if tuple(successor) in visited_cost.keys():
                if visited_cost[tuple(successor)] > cost:
                    visited_cost[tuple(successor)] = cost
                    heappush(pqueue, new_node)

            else:
                # visited_cost[successor] = cost
                heappush(pqueue, new_node)

    return solution

    # you write the rest:
