## Constraint Satisfaction Problem (CSP)

### Overview

Constraint Satisfaction Problem approaches the search through factoring the problem with a set of **keys**, a set of **domains** for each key, and a set of binary **constraints** for the keys and their values. CSP is **capable of solving general problem** unlike our previous search algorithms that are very **problem specific**.


An object `ConstraintedSatisfactionProblem()` will have as its core instance variable


### Codes Revisited
#### def backtrack(self, assignment):
```
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
```

This simple backtracking method implements a **depth first search**, and assigns a value to a variable at every recursive call made to the function. If the assignment turns out to be a failure (no legal value can be assigned to a variable), the function returns None, recurs to its parent node, and tries out a different value assignment.

There are two base cases for this recursive function: 1) when the assignment is complete (that is, when every variable is assigned a consistent value), and 2) when no legal value whatsoever can be assigned to a variable. Hence, the recursion comes to an end when either the search has found a solution, or the search has explored every possible state.

A several heuristics can be applied to this backtracking method (MRV, LCV, MAC3, etc.) so that the search explores the least number of states possible before reaching the solution. And these heuristics shall be discussed further in the later part of this report.

#### def select_unassigned_var(self, assignment):
```
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
```

This method selectively returns a variable that has not been assigned a value yet. By selectively, I mean the method checks whether the MRV (Minimum-Remaining_Value) flag is on or off, and returns simply the first variable it finds that is without an assigned value if the flag is off, or the most constrained variable that is without an assigned value (a variable that is most likely to **fail first**) if the flag is on.

The method

#### def order_domain(self, assignment, var, domains):
```
def order_domain(self, assignment, var):
    if self.lcv:
        to_be_sorted = []

        for val in self.domains[var]:
            count = 0
            for variable in range(len(self.variables)):
                if variable not in assignment.keys():
                    for x in self.constraints[(var, variable)]:
                        if val == x[0]:
                            count += 1
            to_be_sorted.append((val, count))

        to_be_sorted.sort(key=lambda tup: tup[1])

        # Reinitialize the domain
        del self.domains[var]
        self.domains[var] = []

        for entry in to_be_sorted:
            self.domains[var].append(entry[0])
```

This method implements LCV (Least Constraining Value) heuristics so that the search tries assigning a value that will affect its neighboring variables the least first (that is, a value that is most likely to make the search successful, i.e. **fail last**). Very much like `select_unassigned_var()` method, this method checks if the LCV flag is on or off, and sorts the domain according to its entries' heuristic values only if the flag is on.

It searches for a value that has the most constraint with its neighboring


#### def test_inference(self, assignment, var):
```
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
```
This method implements MAC-3 inference algorithm to check if the current assignment of values leads to any arc inconsistency. If arc-inconsistent, the method shall return False, and True else wise.

Of course, like our other heuristics methods, this method checks if the MAC flag is on or off, and returns either True if the flag is off, or whether the assignment is arc-consistent or not if the flag is on.

And this boolean value is passed onto the our `backtrack()` method, and if it turns out that the assignment does lead to an arc inconsistency, the `backtrack()` method does not pursue down the path, and instantly moves onto a different value assignment.

#### def revise(self, assignment, var_1, var_2):
```
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

        domains_reserve[var_1].append(d_1)

    return revised
```
This method is a crucial component of our `test_inference()` method; it checks whether a variable X is arc consistent in respect to another variable Y. If it turns out that it's not arc consistent, it "revises" X's domain to enforce arc-consistency.



### Heuristics

#### Minimum Remaining Variable (MRV)

The main objective of implementing MRV heuristic is to prune unnecessary search down the graph by exploring a variable that is most likely to fail first (i.e. a variable with the least number of available legal states).

MRV brought about an astonishing improvement to the search when the csp was factored with a large number of variable. To prove its efficacy, I solved map coloring problem for the United States instead of Australia. The adjacency list of neighboring states was found in ("https://writeonly.wordpress.com/2009/03/20/adjacency-list-of-states-of-the-united-states-us/"). Unlike Australian map with 7 variables, United States has 51 variables. And with a bigger set like such, it was possible to exhume by how much the heuristic enhances the run-time.

```
MRV = False

Number of nodes visited : 4519750
Number of nodes explored : 18078870
Number of Inconsistencies Encountered : 4519699

MRV = True

Number of nodes visited : 51
Number of nodes explored : 103
Number of Inconsistencies Encountered : 0
```

As such the number of nodes visited has decreased vastly using MRV heuristic. The number of nodes visited decreased by 99% and the number of nodes explored decreased by 99%.

#### Least Constrained Value (LCV)

The main objective of implementing LCV heuristic is to eliminate the least number of legal states for the subsequent variable assignment. Using LCV is expected to guide the search toward the solution with a less number of deviation throughout.

When LCV was applied to my custom circuit board test case, the result was as follows:

```
LCV = False

Number of nodes visited : 10
Number of nodes explored : 104
Number of Inconsistencies Encountered : 0

LCV = True

Number of nodes visited : 10
Number of nodes explored : 85
Number of Inconsistencies Encountered : 0
```

As shown above, the number of nodes explored decreased by 18% (from 104 to 85). The number of nodes visited and the number of inconsistency did not change because it was at its optimum state to start with.

However, LCV is a costly computation, especially when there are a large number of variable and a large domain for each variable. It may abridge the number of nodes visited and explored, but the actual amount of time elapsed to find a solution might not be significantly better.

#### Maintaining Arc Consistency (MAC-3)

The main objective of implementing MAC-3 inference algorithm is to not recurse through a value assignment that will cause an arc inconsistency.

When MAC-3 was applied to the United States coloring, I got a following result:

```
MAC-3 = False

Number of nodes visited : 4519750
Number of nodes explored : 18078870
Number of Inconsistencies Encountered : 4519699

MAC-3 = True

Number of nodes visited : 4088658
Number of nodes explored : 16354543
Number of Inconsistencies Encountered : 4088607
```
As shown above, the number of nodes visited decreased by 10%.

### Problem solving

#### Map Coloring Problem

##### Variables
Variables for the map coloring problem are the **names** of regions portrayed in the map.

##### Domains
The domain for each variable is the **colors** it can be assigned. For Australia, the domain for each region is (red, green, blue). For United States, the domain for each state is (red, green, blue, yellow).

```
def build_domains(self, colors):
    domains = {}

    for var in range(len(self.variables)):
        domains[var] = set()

        for i in range(colors):
            domains[var].add(i)

    return domains
```

##### Constraints
The constraint for each pair of regions is a set of consistent color combinations of the two. If the two regions are adjacent, the set shall exclude the combinations where the colors for two regions are the same (because it would be inconsistent).

```
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
```

#### Circuit Board Problem

##### Variables
Variables for the circuit board problem are the **circuit components**. These components are n x m sized rectangles, which I portrayed as a `2d array of size n x m` filled with a designated alphabet.

##### Domains
The domain for each component would be a set of possible coordinates of the component's bottom-left corner. The coordinate should never be lower than (0, 0). And the `coordinate_x + the width of the component piece` must always be smaller than or equal to the board's width. Moreover, the `coordinate_y + the height of the component piece` must always be smaller than or equal to the board's height.

```
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
```

##### Constraints
The constraint for each pair of component pieces is a set of possible coordinates of the two pieces within each's domain where the two pieces do not overlap.

```
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
```

I ensured that the two pieces do not overlap by computing `upperbound_x`, `upperbound_y`, `lowerbound_x`, and `lowerbound_y`:

```
upperbound_x = max(d_1[0] + len(v_1), d_2[0] + len(v_2))
upperbound_y = max(d_1[1] + len(v_1[0]), d_2[1] + len(v_2[0]))

lowerbound_x = min(d_1[0], d_2[0])
lowerbound_y = min(d_1[1], d_2[1])

if (upperbound_x - lowerbound_x >= len(v_1) + len(v_2)) or (upperbound_y - lowerbound_y >= len(v_1[0]) + len(v_2[0])):

    if upperbound_x <= len(board) and upperbound_y <= len(board[0]):
        constraints[(i, j)].add((d_1, d_2))
```
**i.e.**  
Upperbound_x is the rightmost coordinate, lowerbound_x is the leftmost coordinate. And the **difference between upperbound_x and lowerbound_x** shall never be smaller than **the sum of the width of component piece A and the width of the component piece B.**

And upperbound_y is the topmost coordinate, lowerbound_y i the bottommost coordinate. The **difference between upperbound_y and lowerbound_y** shall never be smaller than **the sum of the height of component piece A and the height of the component piece B.**
### Extra Credit

#### Min_Conflicts()
The function can be found in ConstraintedSatisfactionProblem.py in CSP_EC and the test case can be found in CircuitBoardTest.py.
