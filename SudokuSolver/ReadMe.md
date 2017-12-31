## Sudoku
### Introduction
Using a propositional logic allows us to search for solution to variety of problems. One of the most exemplary local search algorithm that uses propositional logic throughout is GSAT and WalkSAT. And for this lab, we will be looking mainly at how to solve sudoku with GSAT and WalkSAT implementations.

**Extra credits** are placed at the end of the document.

### Design Overview
SAT.py is designed so that it can search for solutions to not only sudoku problems but to other relevant problems like map coloring, mine sweeping, etc.

SAT.py has 3 core instance variables: 1) **self.variables**, 2) **self.clauses**, and 3) **self.model**.

1. **self.variables** is a set of variables with which we will construct our model with.
    ```
    e.g.

    111, 112, ..., 999

    in sudoku problem
    ```
2. **self.clauses** is a list of logical clauses that define the problem. A consistent solution will satisfy all of these clauses.
    ```
    e.g.

    111 112 113 114 115 116 117 118 119
    -111 -112
    -111 -113
    -111 -114
    -111 -115
    -111 -116
    .
    .
    .
    in our sudoku cnf files
    ```
3. **self.model** is a dictionary that holds a boolean value in correspondence to each variable. **self.model** will be used for flipping boolean values within our gsat or walksat function and will be used to determine if our model satisfy the clauses or not. I chose dictionary instead of an array because dictionary gives you more flexibility in what name the variable has in expense of a little bit more memory usage.

    ```
    e.g.

    {[111 : True], [112 : False] ...}

    in sudoku problem
    ```
### Codes Revisited

#### def generate_clause(self):
```
def generate_clause(self):
    for clause in self.cnf_buffer:
        variable_list = []
        for variable in clause.split():
            variable_list.append(variable)
            if variable not in self.variables: self.variables.add(variable.strip().strip('-'))
        self.clauses.append(tuple(sorted(variable_list)))
```

The following method turns a line of the provided cnf file into a line of clause, and appends the clause to our list. Moreover, it adds the variable within the clause to our pre-initialized set of variables if it has not been already.

#### def clause_satisfied(self):
```
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
```
The following method determines whether the clauses are satisfied or not with our current model assignment. The basic mechanism of the method is as follows:
1) Loop through each clause
2) Determine whether our model satisfies the clause
3) Accordingly update our list of satisfied clauses and of unsatisfied clauses
4) Update our boolean variable of whether every clause has been satisfied using an **AND operator**
5) Once out of loop, return a boolean for whether every clause has been satisfied or not.

This method is called at the beginning of every iteration of gsat or walksat to determine whether we have found a solution or not, and is called within our get_highest_score() method to determine flipping the value of which variable will satisfy the most number of clauses.

#### def gsat(self):
```
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
```
The following method loops until every clause has been satisfied. And within each iteration, it flips a value of a variable either of the highest compositional score or of a random choice depending on our random seed value.

#### def walksat(self):

```
def walksat(self):
    self.generate_model()

    while not self.clause_satisfied():
        self.iteration += 1

        rand = random.uniform(0, 1)
        clause = random.choice(list(self.unsatisfied_clauses))
        var = None

        if rand > self.threshold:
            var = (random.choice(list(clause))).strip('-')

        else:
            var = self.get_highest_score(list(clause))

        self.model[var] = not self.model[var]

    return True

```
The following method, in contrast to `gsat()`, first chooses an unsatisfied clause, and flips a variable within that clause, thereby reducing the list of variables to iterate through before flipping for a more efficient search.

#### def get_highest_score(self, variables : list):

```
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
```
The following method is probably what completes our GSAT and WalkSAT. Without this method, we cannot be certain of when the search will ever come to an end. This method, in short, takes a list of variables, iterate through each one of them, computes a compositional score (how many clauses are satisfied along with flipping the value of the specified variable), and returns the variable with the highest score.

This method is the most significant yet most computation heavy keystone of our program. It computes a compositional score, which inevitably involves iterating through the entire clauses (in case of puzzle1.cnf, there are 3250 clauses). Going through 3250 clauses for 729 variables does not sound pleasant, and that is why it is important to scale down the list of variables to compute the scores for in order to make the search run faster. And that is why WalkSAT is significantly faster than GSAT.
### GSAT vs WalkSAT

GSAT and WalkSAT are fundamentally the same local search algorithms, yet WalkSAT has a significantly better performance along with a slight optimization. In the section below, we will discuss how WalkSAT optimizes GSAT to enhance its runtime, and see how much stronger the performance is with WalkSAT compared to GSAT.

#### GSAT
```
__all_cells.cnf__

Iteration : 500 times.
Time Elapsed : 1137.23 seconds
4 4 6 | 4 1 2 | 5 2 8
4 8 8 | 5 8 2 | 3 5 4
2 6 7 | 5 5 2 | 9 4 3
---------------------
2 9 3 | 2 8 7 | 7 2 5
4 9 5 | 2 9 2 | 9 7 5
3 3 1 | 2 1 7 | 1 8 3
---------------------
5 7 3 | 4 2 8 | 8 5 6
2 9 2 | 9 8 1 | 8 5 3
1 6 9 | 6 9 2 | 5 6 9
```

GSAT is a very inefficient way of reaching a solution as made apparent above. The inefficiency comes mainly from making unnecessary searches. **GSAT iterates through the entire variables**, computes a composition score for each one of them before deciding which one to flip the value of. Computing composition score is a very costly computation, for it has to loop through the entire list of constraint clauses in order to determine how many clauses are satisfied and how many are not. And GSAT computes composition score for every variable within the model, and goes through these costly computations **729 times** (in case of 9 x 9 Sudoku) for each iteration of GSAT. Hence, it can be said that the overall performance of GSAT largely depends on the number of logical clauses and the number of variables provided.

#### WalkSAT
```
__all_cells.cnf__

Iteration : 292 times.
Time Elapsed : 2.93 seconds
4 1 2 | 4 1 3 | 2 7 1
5 6 8 | 1 3 3 | 4 7 4
4 2 2 | 6 7 2 | 9 1 6
---------------------
1 9 6 | 6 8 9 | 4 8 8
4 6 8 | 3 9 2 | 2 6 4
3 3 2 | 8 1 6 | 5 4 5
---------------------
4 9 8 | 4 2 1 | 6 9 9
2 8 6 | 2 8 9 | 9 5 9
7 2 3 | 7 6 1 | 2 3 1
```
Not only does implementing WalkSAT finds a solution within a smaller number of iteration compared to implementing GSAT, it also finds solution in a much shorter time. There was a 99.7% drop in the amount of time elapsed to find the solution for the case of all_cells.cnf. And this performance gap gets even bigger for complex problems with more clauses.

The main reason behind WalkSAT's stronger performance is as follows:

WalkSAT only **iterates through variables within one of unsatisfied clauses** in contrast to GSAT, which iterates through the entire set of variables in finding the next variable to flip the value of. This may seem trivial, but it indeed is not; a clause usually contains a much smaller number of variables compared to the total number of variables within the model (in case of our sudoku problem, the difference is as large as `729 to 2`). And given how costly computing compositional score for a variable is, starting with a smaller list of variables to compute scores for improves the performance by an enormous amount.

And below are the solutions to the provided puzzles solved using WalkSAT:

```
__puzzle1__

Iteration : 23224 times.
Time Elapsed : 467.14 seconds
5 1 2 | 7 4 6 | 8 9 3
6 7 8 | 1 9 3 | 5 2 4
4 3 9 | 5 8 2 | 1 6 7
---------------------
8 5 1 | 2 6 4 | 3 7 9
9 6 3 | 8 7 1 | 4 5 2
7 2 4 | 3 5 9 | 6 1 8
---------------------
1 9 7 | 4 3 5 | 2 8 6
2 4 6 | 9 1 8 | 7 3 5
3 8 5 | 6 2 7 | 9 4 1
```
```
__puzzle2__

Iteration : 13080 times.
Time Elapsed : 329.08 seconds
5 3 6 | 7 2 4 | 8 9 1
2 7 8 | 1 9 3 | 5 6 4
1 9 4 | 6 5 8 | 3 2 7
---------------------
8 1 2 | 9 6 7 | 4 5 3
4 6 3 | 8 1 5 | 9 7 2
7 5 9 | 4 3 2 | 1 8 6
---------------------
3 8 7 | 5 4 6 | 2 1 9
6 2 1 | 3 8 9 | 7 4 5
9 4 5 | 2 7 1 | 6 3 8
```

### Extra credit


#### Map coloring
As previously discussed, I have designed my SAT.py so that it can operate as a generic problem solver to variety of problems. And as a rather simple proof of that, I have designed a **solve_map.py** that takes in a _mapname_.cnf file and calls **display_map_solution** from display.py. And below is a demonstration of map solving:

```
python solve_map.py australian_map.cnf

WA is B

SA is R

V is B

Q is B

NSW is G

T is G

NT is G

```

#### Redundant Constraints and Its Effect on runtime
According to Ivor Spence, solving a simple cnf problem with no redundancy takes a longer time to compute compared to solving a more complex cnf problem with redundancies. In order to test whether his argument is sound or not, I have edited the **Sudoku.py** so that it adds the redundant clauses specified in cnf description page(http://www.cs.qub.ac.uk/~I.Spence/SuDoku/SuDoku.html). The edited version of Sudoku.py can be found in Sudoku_EC. And below is the computed result:

```
__puzzle1__

Iteration : 10904 times.
Time Elapsed : 487.34 seconds
5 1 4 | 3 8 6 | 7 2 9
2 7 6 | 1 9 4 | 8 5 3
3 9 8 | 7 2 5 | 4 6 1
---------------------
8 4 2 | 5 6 9 | 3 1 7
9 3 5 | 8 7 1 | 6 4 2
7 6 1 | 2 4 3 | 5 9 8
---------------------
1 5 9 | 6 3 7 | 2 8 4
6 8 3 | 4 1 2 | 9 7 5
4 2 7 | 9 5 8 | 1 3 6
```

As made apparent above, having redundant clauses did decrease the number of iterations the search had to go through before reaching a solution  by a pretty significant amount (because it enhances the accuracy of **get_highest_score** method) but as mentioned earlier, computing the score for each variable is a very costly operation, and elongating the clauses would make each operating take a longer time, which in sum causes a huge slow down. And overall, the amount of time elapsed in solving puzzle 1 actually increased from 467.14 seconds to 487.34 seconds despite the number of iteration being cut down by more than half. It can, thus, be concluded that each iteration of the search is much more costly for having redundant clauses in comparison to having non-redundant clauses.
