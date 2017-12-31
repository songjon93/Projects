import random


class SAT:

    def __init__(self, file_name):
        self.cnf_buffer = []
        self.variables = set()
        self.clauses = []
        self.model = dict()
        self.unsatisfied_clauses = []
        self.satisfied_clauses = []
        self.iteration = 0
        self.threshold = 0.8

        self.generate_buffer(file_name)
        self.generate_clause()

    # Instead of looping through the file to generate clauses, just turn them into a list of lines using a buffer
    def generate_buffer(self, file_name):
        cnf_name = file_name[:-4] + ".cnf"

        f = open(cnf_name, "r")
        self.cnf_buffer = f.readlines()
        f.close()

    # Generate a list of clause, every line of cnf buffer should be entailed with an or operator
    # And clauses should be entailed with an and operator. Also, update the variable set in the meanwhile.
    def generate_clause(self):
        for clause in self.cnf_buffer:
            variable_list = []
            for variable in clause.split():
                variable_list.append(variable)
                if variable not in self.variables: self.variables.add(variable.strip().strip('-'))
            self.clauses.append(tuple(sorted(variable_list)))

    # Randomly assign a boolean value to a variable
    def generate_model(self):
        for var in self.variables:
            self.model[var] = bool(random.getrandbits(1))

    # Loop through every clause, and determine if the clauses are satisfied, return True if all of them are.
    # Update the sets of unsatisfied clauses and of satisfied clauses for uses in walksat() and get_highest_score()
    def clause_satisfied(self):
        del self.unsatisfied_clauses[:]
        del self.satisfied_clauses[:]
        satisfied = True

        for key in self.clauses:
            clause_satisfied = False
            for var in key:
                if var[0] == '-':
                    clause_satisfied = clause_satisfied or not self.model[var.strip('-')]
                else:
                    clause_satisfied = clause_satisfied or self.model[var.strip('-')]

            satisfied = satisfied and clause_satisfied
            if not clause_satisfied: self.unsatisfied_clauses.append(key)
            else: self.satisfied_clauses.append(key)

        return satisfied

    # Iterate until every clause has been satisfied, for each iteration, flip a variable either of the highest
    # compositional score or of random choice depending on the random seed.
    def gsat(self):
        self.generate_model()

        while not self.clause_satisfied():
            self.iteration += 1

            rand = random.uniform(0, 1)
            var = None

            if rand > self.threshold:
                var = str(random.choice(list(self.variables)))

            else:
                var = self.get_highest_score(self.variables)

            self.model[var] = not self.model[var]

        return True

    # Iterate util every clause has been satisfied, for each iteration, choose randomly an unsatisfied clause, and
    # and within that clause, either choose a random variable or determine a variable of the highest compositional
    # value, then flip.
    def walksat(self):
        self.generate_model()

        while not self.clause_satisfied():
            self.iteration += 1
            print(len(self.unsatisfied_clauses))

            rand = random.uniform(0, 1)
            clause = random.choice(list(self.unsatisfied_clauses))
            var = None

            if rand > self.threshold:
                var = (random.choice(list(clause))).strip('-')

            else:
                var = self.get_highest_score(list(clause))

            self.model[var] = not self.model[var]

        return True


    # Loop through the provided list of variables, and return the variable with the highest compositional score
    # (that is, the total number of satisfied clauses).
    def get_highest_score(self, variables):
        highest_var = None
        max_score = -1

        for var in variables:
            var = var.strip('-')
            self.model[var] = not self.model[var]
            self.clause_satisfied()
            self.model[var] = not self.model[var]
            score = len(self.satisfied_clauses)

            highest_var = var if score > max_score else highest_var
            highest_var = random.choice([var, highest_var]) if score == max_score else highest_var
            max_score = max(score, max_score)

        return highest_var

    def write_solution(self, file_name):
        f = open(file_name, "w")
        for var in self.model.keys():
            sign = "" if self.model[var] else "-"
            f.write(str(sign + var + "\n"))