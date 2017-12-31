from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem


class MapColoringProblem(ConstraintSatisfactionProblem):
    def __init__(self, variables, colors, adjacency_list, mrv=False, lcv=False, mac=False):
        self.variables = variables
        self.domains = self.build_domains(len(colors))
        self.constraints = self.build_constraints(adjacency_list)
        self.mrv = mrv
        self.lcv = lcv
        self.mac = mac
        self.nodes_visited = 0
        self.nodes_explored = 0
        self.num_of_inconsistency = 0
        self.colors = colors

    # Every variable will have as its domain an integer value from 0 to the number of colors provided.
    def build_domains(self, colors):
        domains = {}

        for var in range(len(self.variables)):
            domains[var] = set()

            for i in range(colors):
                domains[var].add(i)

        return domains

    # Loop through v_1's domain and v_2's domain, if v_1 and v_2 are adjacents, have their constrains include only the
    # combinations of colors where the two colors do not match, if not include every possible combination of colors.
    def build_constraints(self, adjacency_list):
        constraints = {}
        for i in range(len(self.variables)):
            for j in range(len(self.variables)):
                constraints[(i, j)] = set()
                for color_1 in self.domains[i]:
                    for color_2 in self.domains[j]:
                        if adjacency_list[i][j] and color_1 == color_2:
                            continue
                        constraints[(i, j)].add((color_1, color_2))

        return constraints

    # For debugging purposes, to test if the map coloring problem has been initialized properly.
    def print_tree(self):
        for i in range(len(self.variables)):
            print(self.variables[i] + " : ")
            for j in range(len(self.variables)):
                print(self.variables[j] + " " + str((self.variables[i], self.variables[j]) not in self.constraints[self.variables[i]]) + ", ")
            print("\n")

    def solve(self):
        solution = self.backtrack_search()
        return solution

    def __str__(self):
        solution = self.solve()

        res = "MRV=" + str(self.mrv) + " LCV=" + str(self.lcv) + " MAC-3=" + str(self.mac) + "\n"
        res += "Number of nodes visited : " + str(self.nodes_visited) + "\n"
        res += "Number of nodes explored : " + str(self.nodes_explored) + "\n"
        res += "Number of Inconsistencies Encountered : " + str(self.num_of_inconsistency) + "\n"

        if solution is None:
            return res + "No solution was found"

        for var in range(len(self.variables)):
            color = self.colors[solution[var]]
            res += self.variables[var] + " : " + color + "\n"

        return res


