from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem

class CircuitBoardProblem(ConstraintSatisfactionProblem):
    def __init__(self, variables, board, mrv=False, lcv=False, mac=False):
        self.variables = variables
        self.domains = self.build_domains(board)
        self.constraints = self.build_constraints(board)
        self.mrv = mrv
        self.lcv = lcv
        self.mac = mac
        self.nodes_visited = 0
        self.BOARD = board
        self.nodes_explored = 0
        self.num_of_inconsistency = 0

    # The domain for each component would be a set of possible coordinates of the component's bottom-left corner.
    def build_domains(self, board):
        domains = {}
        for v in range(len(self.variables)):
            domains[v] = set()

            x = len(board) - len(self.variables[v])
            y = len(board[0]) - len(self.variables[v][0])

            for i in range(x + 1):
                for j in range(y + 1):
                    domains[v].add((i, j))

        return domains

    # The constraint for each pair of component pieces is a set of possible coordinates of the two pieces
    # within each's domain where the two pieces do not overlap.
    def build_constraints(self, board):
        constraints = {}

        for i in range(len(self.variables)):
            for j in range(len(self.variables)):
                constraints[(i, j)] = set()
                v_1 = self.variables[i]
                v_2 = self.variables[j]

                if v_1 == v_2: continue

                for d_1 in self.domains[i]:
                    for d_2 in self.domains[j]:
                        upperbound_x = max(d_1[0] + len(v_1), d_2[0] + len(v_2))
                        upperbound_y = max(d_1[1] + len(v_1[0]), d_2[1] + len(v_2[0]))

                        lowerbound_x = min(d_1[0], d_2[0])
                        lowerbound_y = min(d_1[1], d_2[1])

                        if (upperbound_x - lowerbound_x >= len(v_1) + len(v_2)) or (upperbound_y - lowerbound_y >= len(v_1[0]) + len(v_2[0])):

                            if upperbound_x <= len(board) and upperbound_y <= len(board[0]):
                                constraints[(i, j)].add((d_1, d_2))

        return constraints

    def solve(self):
        solution = self.backtrack_search()
        return solution

    def __str__(self):
        solution = self.solve()

        if solution is None:
            return "No solution exists"

        board = [['.' for i in range    (len(self.BOARD[0]))] for j in range((len(self.BOARD)))]

        for key in solution.keys():
            for x in range(len(self.variables[key])):
                for y in range(len(self.variables[key][0])):
                    x_index = x + solution[key][0]
                    y_index = y + solution[key][1]

                    board[x_index][y_index] = self.variables[key][x][y]

        res = "MRV=" + str(self.mrv) + " LCV=" + str(self.lcv) + " MAC-3=" + str(self.mac) + "\n"
        res += "Number of nodes visited : " + str(self.nodes_visited) + "\n"
        res += "Number of nodes explored : " + str(self.nodes_explored) + "\n"
        res += "Number of Inconsistencies Encountered : " + str(self.num_of_inconsistency) + "\n"
        for j in range(len(board[0]) - 1, -1, -1):
            for i in range(len(board)):
                res += board[i][j]
            res += '\n'

        return res
