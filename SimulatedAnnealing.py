import math
import random

def cbus_greedy(n, k, distance_matrix):
    visited = [False] * (2 * n + 1)  # Trạng thái các điểm đã được ghé thăm
    route = []  # Tuyến đường
    capacity = 0  # Số hành khách hiện tại trên xe

    current = 0  # Bắt đầu từ điểm 0
    while len(route) < 2 * n:  # Lặp cho đến khi đi qua tất cả điểm đón/trả
        best_next = None
        best_cost = float('inf')

        # Tìm điểm tiếp theo gần nhất
        for next_point in range(1, 2 * n + 1):
            if not visited[next_point]:
                # Điều kiện hợp lệ
                if next_point > n and not visited[next_point - n]:  # Không trả khách trước khi đón
                    continue
                if next_point <= n and capacity >= k:  # Quá tải
                    continue

                # Cập nhật điểm gần nhất
                if distance_matrix[current][next_point] < best_cost:
                    best_next = next_point
                    best_cost = distance_matrix[current][next_point]

        # Cập nhật route
        if best_next is not None:
            route.append(best_next)
            visited[best_next] = True
            if best_next <= n:  # Điểm đón
                capacity += 1
            else:  # Điểm trả
                capacity -= 1
            current = best_next
        else:
            break

    return route

def simulated_annealing(n, k, distance_matrix, initial_route, initial_temperature, cooling_rate, max_iterations):
    def calculate_cost(route, distance_matrix):
        cost = distance_matrix[0][route[0]]  # Từ điểm 0 đến điểm đầu tiên
        for i in range(len(route) - 1):
            cost += distance_matrix[route[i]][route[i + 1]]
        cost += distance_matrix[route[-1]][0]  # Từ điểm cuối cùng quay về điểm 0
        return cost

    def generate_neighbor(route):
        # Tạo lân cận bằng cách hoán đổi hai điểm
        i, j = random.sample(range(len(route)), 2)
        neighbor = route[:]
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor

    def is_valid_route(route, n, k):
        # Kiểm tra ràng buộc đón trước trả và sức chứa
        current_load = 0
        position = {val: idx for idx, val in enumerate(route)}
        for i in range(1, n + 1):
            if position[i] > position[i + n]:  # Đón sau trả
                return False
        for point in route:
            if point <= n:
                current_load += 1
            else:
                current_load -= 1
            if current_load > k:
                return False
        return True

    # Khởi tạo
    current_route = initial_route
    current_cost = calculate_cost(initial_route, distance_matrix)
    best_route = current_route
    best_cost = current_cost
    temperature = initial_temperature

    for iteration in range(max_iterations):
        # Tạo lân cận
        neighbor = generate_neighbor(current_route)
        if not is_valid_route(neighbor, n, k):
            continue

        neighbor_cost = calculate_cost(neighbor, distance_matrix)

        # Quyết định chấp nhận giải pháp mới
        if neighbor_cost < current_cost:
            current_route = neighbor
            current_cost = neighbor_cost
        else:
            # Chấp nhận với xác suất
            delta = neighbor_cost - current_cost
            probability = math.exp(-delta / temperature)
            if random.random() < probability:
                current_route = neighbor
                current_cost = neighbor_cost

        # Cập nhật giải pháp tốt nhất
        if current_cost < best_cost:
            best_route = current_route
            best_cost = current_cost

        # Giảm nhiệt độ
        temperature *= cooling_rate

        # Dừng sớm nếu nhiệt độ quá thấp
        if temperature < 1e-5:
            break

    return best_route, best_cost

# Example usage
n, k = map(int, input().split())

# Read distance matrix
distance_matrix = []
for _ in range(2 * n + 1):
    row = list(map(int, input().split()))
    distance_matrix.append(row)

# Khởi tạo giải pháp bằng Greedy
initial_route = cbus_greedy(n, k, distance_matrix)

# Tham số Simulated Annealing
initial_temperature = 1000  # Nhiệt độ ban đầu
cooling_rate = 0.99         # Tốc độ giảm nhiệt độ
max_iterations = 1000       # Số vòng lặp tối đa

# Chạy Simulated Annealing
best_route, best_cost = simulated_annealing(n, k, distance_matrix, initial_route, initial_temperature, cooling_rate, max_iterations)

print("Initial Greedy Route:", initial_route)
print("Best Route after Simulated Annealing:", best_route)
print("Best Cost after Simulated Annealing:", best_cost)
