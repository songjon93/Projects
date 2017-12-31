class ConstraintSatisfactionProblem:

    def __init__(self, variables, domains, constraints, mrv, lcv, mac):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.removed = {}
        self.mrv = mrv
        self.lcv = lcv
        self.mac = mac
        self.nodes_visited = 0
        self.nodes_explored = 0
        self.num_of_inconsistency = 0

    # Backtrack caller function
    def backtrack_search(self):
        sol = self.backtrack({})
        return sol

    # Backtrack helper function: assigns a value to a variable at every recursive call made to the function.
    # If the assignment turns out to be a failure (no legal value can be assigned to a variable),
    # the function returns None, recurs to its parent node, and tries out a different value assignment.
    def backtrack(self, assignment):
        if self.is_complete(assignment):
            return assignment

        self.nodes_visited += 1

        var = self.select_unassigned_var(assignment)
        self.order_domain(assignment, var)

        for val in self.order_domain(assignment, var):
            self.nodes_explored += 1

            if self.is_consistent(assignment, var, val):
                domains_reserve = {}
                assignment[var] = val
                self.set_domain(domains_reserve, var, val)

                if self.test_inference(assignment, var, domains_reserve):
                    result = self.backtrack(assignment)

                    if result is not None:
                        return result

                del assignment[var]

                self.restore_domain(domains_reserve)

        self.num_of_inconsistency += 1
        return None

    # When a value is assigned to the variable, remove every other value from its domain and add it to the domain
    # reserve so that the domain can be restored when desired.
    def set_domain(self, domains_reserve, var, val):
        domains_reserve[var] = set()
        domains_reserve[var] = domains_reserve[var].union(self.domains[var])
        domains_reserve[var].remove(val)

        self.domains[var].clear()
        self.domains[var].add(val)

    # Restore the variables' domain as noted above.
    def restore_domain(self, domains_reserve):
        for key in domains_reserve:
            self.domains[key] = self.domains[key].union(domains_reserve[key])

    # The assignment is complete when the dictionary has an assigned value for every variable.
    def is_complete(self, assignment):
        return len(assignment.keys()) == len(self.variables)

    # If MCV flag is on, search through the variable list, and return the most constrained variable, and if MCV flag is
    # off, just return the first variable you come across that has not been assigned a value yet.
    def select_unassigned_var(self, assignment):
        min_count = float("inf")
        mcv_index = None

        for var in range(len(self.variables)):

            if var in assignment.keys():
                continue
            
            if not self.mrv:
                return var

            count = 0
            for key in assignment.keys():
                for constraint in self.constraints[(var, key)]:
                    if constraint[1] == assignment[key]:
                        count += len(self.constraints[(var, key)])

            mcv_index = var if count < min_count else mcv_index
            min_count = min(min_count, count)

        return mcv_index

    # If LCV flag is on, sort your domain according to the number of legal moves it leaves for its neighboring variable.
    # If not, return a listified default domain
    def order_domain(self, assignment, var):
        if self.lcv:
            ret = []
            to_be_sorted = []

            for val in self.domains[var]:
                count = 0
                for variable in range(len(self.variables)):
                    if variable not in assignment.keys():
                        for x in self.constraints[(var, variable)]:
                            if val == x[0]:
                                count += 1
                        # count += len(self.constraints[(var, variable)])
                to_be_sorted.append((val, count))

            to_be_sorted.sort(key=lambda tup: tup[1], reverse=True)

            # Reinitialize the domain
            for entry in to_be_sorted:
                ret.append(entry[0])

            return ret
        return list(self.domains[var])

    # Loop through the constraints dictionary, and see if value assignment is legal or not.
    def is_consistent(self, assignment, var, val):
        for key in assignment.keys():
            if key != var and (val, assignment[key]) not in self.constraints[(var, key)]:
                return False
        return True

    # If MAC flag is on, loop through the queue, and determine whether the domain has been modified to enforce arc
    # consistency.
    def test_inference(self, assignment, var, domains_reserve):
        if self.mac:
            queue = self.build_arc_queue(assignment, var)

            while len(queue) > 0:
                x = queue.pop()

                if self.revise(assignment, x[0], x[1], domains_reserve):
                    if len(self.domains[x[0]]) == 0:
                        return False

                    for var_2 in range(len(self.variables)):
                        if len(self.constraints[(var, var_2)]) > 0 and var_2 not in x:
                            queue.add((var_2, x[0]))

        return True

    def build_arc_queue(self, assignment, var):
        queue = set()

        for var_2 in range(len(self.variables)):
            if var_2 == var or not (len(self.constraints[(var, var_2)]) > 0 and var_2 not in assignment):
                continue
            queue.add((var, var_2))

        return queue

    def revise(self, assignment, var_1, var_2, domains_reserve):
        revised = False
        to_be_removed = []

        for d_1 in self.domains[var_1]:
            constrained = False
            for d_2 in self.domains[var_2]:
                if (d_1, d_2) in self.constraints[(var_1, var_2)]:
                    constrained = True
            if not constrained:
                to_be_removed.append(d_1)
                revised = True

        for d_1 in to_be_removed:
            self.domains[var_1].remove(d_1)

            if var_1 not in domains_reserve.keys():
                domains_reserve[var_1] = []

            domains_reserve[var_1].add(d_1)

        return revised
