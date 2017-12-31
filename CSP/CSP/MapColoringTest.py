from MapColoringProblem import MapColoringProblem

# Construct Australia CSP object
test_vars = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
test_colors = ["r", "g", "b"]
test_alist = [[True, True, True, False, False, False, False], [True, True, True, True, False, False, False], [True, True, True, True, True, True, False], [False, True, True, True, True, False, False], [False, False, True, True, True, True, False], [False, False, False, False, True, True, False], [False, False, False, False, False, False, True]]
problem_1 = MapColoringProblem(test_vars, test_colors, test_alist)
print(problem_1)


# Construct United States CSP object
test_vars_2 = []
test_colors_2 = ["r", "g", "b", "y"]
test_alist_2 = [[False for i in range(51)] for j in range(51)]

f = open("US.txt")

counter = -1
for line in f:
    counter += 1

    if counter < 3:
        continue
    test_vars_2.append(str(line[0:2]))

f.seek(0)

counter = -1
for line in f:
    counter += 1
    str_flag = False
    cur_var = None
    neighbor_flag = False

    if counter < 3:
        continue

    for i in range(len(line)):
        if not neighbor_flag and line[i] == ',':
            neighbor_flag = True

        if line[i].isalpha():
            if str_flag:
                str_flag = False
                continue

            if neighbor_flag:
                n_count = 0
                for j in test_vars_2:
                    if j == (line[i:i+2]):
                        break
                    n_count += 1

                test_alist_2[counter - 3][n_count] = True

            str_flag = True
f.close()

problem_2 = MapColoringProblem(test_vars_2, test_colors_2, test_alist_2, mrv=True, lcv=True, mac=True)
print(problem_2)
