from ortools.sat.python import cp_model

def cbus_problem():
    #Data
    data = {}
    firstline = input()
    firstline = firstline.split()
    data['n'] = int(firstline[0])
    data['k'] = int(firstline[1])
    data['distance_matrix'] = []
    for i in range(2 * data['n'] + 1):
        row_i = []
        line_i = input()
        line_i = line_i.split()
        for j in line_i:
            row_i.append(int(j))
        data['distance_matrix'].append(row_i)

    model = cp_model.CpModel()

    # Decision variables
    x = {}  # Route variables: x[i][j] = 1 if traveling from i to j
    for i in range(2 * data['n'] + 1):
        for j in range(2 * data['n'] + 1):
            if i != j:
                x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

    y = [model.NewIntVar(0, data['k'], f'y[{i}]') for i in range(2 * data['n'] + 1)]  # Load variables

    u = [model.NewIntVar(0, 2 * data['n'], f'u[{i}]') for i in range(2 * data['n'] + 1)]  # Sequence variables

    # Constraints
    # 1. Every node is entered and left exactly once
    for i in range(2 * data['n'] + 1):
        model.Add(sum(x[j, i] for j in range(2 * data['n'] + 1) if j != i) == 1)
        model.Add(sum(x[i, j] for j in range(2 * data['n'] + 1) if j != i) == 1)

    # 2. Load constraints: Maintain capacity
    for i in range(1, 2 * data['n'] + 1):
        for j in range(1, 2 * data['n'] + 1):
            if i != j:
                model.Add(y[j] == y[i] + (1 if j <= data['n'] else -1)).OnlyEnforceIf(x[i, j])

    # Subtour elimination using sequence variables
    for i in range(1, 2 * data['n'] + 1):
        for j in range(1, 2 * data['n'] + 1):
            if i != j:
                model.Add(u[i] + 1 <= u[j]).OnlyEnforceIf(x[i, j])
    # Order constraints: Drop-off after pickup
    for i in range(1, data['n'] + 1):
        model.Add(u[i] < u[i + data['n']])

    # Objective: Minimize travel distance
    model.Minimize(
        sum(data['distance_matrix'][i][j] * x[i, j] for i in range(2 * data['n'] + 1) for j in range(2 * data['n'] + 1) if i != j)
    )

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(int(solver.ObjectiveValue()))
    else:
        print('No solution found.')

if __name__ == '__main__':
    cbus_problem()