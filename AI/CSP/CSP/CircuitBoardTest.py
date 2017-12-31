from CircuitBoardProblem import CircuitBoardProblem

test_vars = [[['a', 'a'] for i in range(3)], [['b', 'b'] for i in range(5)], [['c', 'c', 'c'] for i in range(2)], [['e'] for i in range(7)]]
test_board = [['.' for i in range(3)] for j in range(10)]
test = CircuitBoardProblem(test_vars, test_board)
print(test)

test_vars_2 = [[['a', 'a', 'a'] for i in range(2)], [['b'] for i in range(8)], [['c', 'c'] for i in range(4)], ['d', 'd'], [['e'] for i in range(3)], ['f'], ['g'], ['h'], [['k'] for i in range(8)], [['l'] for i in range(8)]]
test_board_2 = [['.' for i in range(10)] for j in range(15)]
test_2 = CircuitBoardProblem(test_vars_2, test_board_2, False, False, False)
print(test_2)
test_2 = CircuitBoardProblem(test_vars_2, test_board_2, False, True, False)
print(test_2)