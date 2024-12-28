from ortools.sat.python import cp_model

def solve_cbus_with_cp(n, k, distance_matrix):
    model = cp_model.CpModel()

    # Số điểm: 0, 1, ..., 2n
    num_locations = 2 * n + 1

    # Biến quyết định: vị trí tiếp theo trong hành trình
    x = [model.NewIntVar(0, num_locations - 1, f'x[{i}]') for i in range(2 * n + 1)]

    # Biến lưu trạng thái: số lượng khách trên xe tại mỗi bước
    q = [model.NewIntVar(0, k, f'q[{i}]') for i in range(2 * n + 1)]

    # Ràng buộc:
    # 1. Xuất phát tại điểm 0
    model.Add(x[0] == 0)

    # 2. Không lặp lại điểm đến
    model.AddAllDifferent(x[1:])

    # 3. Điểm trả khách phải sau điểm đón khách
    for i in range(1, n + 1):
        model.Add(x[i + n] > x[i])

    # 4. Số lượng khách trên xe không vượt quá k
    for i in range(1, 2 * n + 1):
        model.Add(q[i] <= k)

    # Hàm mục tiêu: Tối thiểu hóa tổng chi phí quãng đường
    total_distance = model.NewIntVar(0, 1000000, 'total_distance')
    distances = []
    for i in range(1, 2 * n + 1):
        # Biến lưu giá trị khoảng cách
        distance_var = model.NewIntVar(0, 1000000, f'distance_{i}')
        prev_index = model.NewIntVar(0, num_locations - 1, f'prev_index_{i}')
        next_index = model.NewIntVar(0, num_locations - 1, f'next_index_{i}')

        model.Add(prev_index == x[i - 1])
        model.Add(next_index == x[i])

        for j in range(num_locations):
            model.Add(distance_var == distance_matrix[j][next_index]).OnlyEnforceIf(prev_index == j)

        distances.append(distance_var)

    model.Add(total_distance == sum(distances))
    model.Minimize(total_distance)

    # Tạo solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Tổng chi phí:", solver.ObjectiveValue())
        route = [solver.Value(x[i]) for i in range(2 * n + 1)]
        print("Hành trình:", route)
    else:
        print("Không tìm thấy giải pháp.")

# Ví dụ input
n, k = map(int, input().split())

# Read distance matrix
distance_matrix = []
for _ in range(2 * n + 1):
    row = list(map(int, input().split()))
    distance_matrix.append(row)
        
solve_cbus_with_cp(n, k, distance_matrix)