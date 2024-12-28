from ortools.sat.python import cp_model

def cbus_problem(n, k, distance_matrix):
    model = cp_model.CpModel()

    # Decision variables
    x = {}  # Route variables: x[i][j] = 1 if traveling from i to j
    for i in range(2 * n + 1):
        for j in range(2 * n + 1):
            if i != j:
                x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

    y = [model.NewIntVar(0, k, f'y[{i}]') for i in range(2 * n + 1)]  # Load variables

    u = [model.NewIntVar(0, 2 * n, f'u[{i}]') for i in range(2 * n + 1)]  # Sequence variables

    # Constraints
    # 1. Every node is entered and left exactly once
    for i in range(2 * n + 1):
        model.Add(sum(x[j, i] for j in range(2 * n + 1) if j != i) == 1)
        model.Add(sum(x[i, j] for j in range(2 * n + 1) if j != i) == 1)

    # 2. Load constraints: Maintain capacity
    for i in range(1, n + 1):
        for j in range(1, 2 * n + 1):
            if i != j:
                model.Add(y[j] == y[i] + 1).OnlyEnforceIf(x[i, j])
    
    for i in range(n + 1, 2 * n + 1):
        for j in range(1, 2 * n + 1):
            if i != j:
                model.Add(y[j] == y[i] - 1).OnlyEnforceIf(x[i, j])

    # Subtour elimination using sequence variables
    for i in range(1, 2 * n + 1):
        for j in range(1, 2 * n + 1):
            if i != j:
                model.Add(u[i] + 1 <= u[j]).OnlyEnforceIf(x[i, j])

    # Order constraints: Drop-off after pickup
    for i in range(1, n + 1):
        model.Add(u[i] < u[i + n])

    # Objective: Minimize travel distance
    model.Minimize(
        sum(distance_matrix[i][j] * x[i, j] for i in range(2 * n + 1) for j in range(2 * n + 1) if i != j)
    )

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(solver.ObjectiveValue())
        route = []
        current = 0
        while len(route) < 2 * n:
            next_point = None
            for j in range(1, 2 * n + 1):
                if j != current and solver.Value(x[current, j]) == 1:
                    next_point = j
                    break
            if next_point is None:
                break
            route.append(next_point)
            current = next_point
        # print('Optimal route:', ' '.join(map(str, route)))
    else:
        print('No solution found.')

# Example usage
n, k = map(int, input().split())

# Read distance matrix
distance_matrix = []
for _ in range(2 * n + 1):
    row = list(map(int, input().split()))
    distance_matrix.append(row)
    
cbus_problem(n, k, distance_matrix)