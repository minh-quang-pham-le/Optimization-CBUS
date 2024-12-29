import random
import math

def calculate_cost(route, distance_matrix):
    # Tính tổng chi phí, bao gồm từ điểm 0 đến điểm đầu tiên và từ điểm cuối cùng về điểm 0
    cost = distance_matrix[0][route[0]]  # Từ điểm 0 đến điểm đầu tiên
    for i in range(len(route) - 1):
        cost += distance_matrix[route[i]][route[i + 1]]
    cost += distance_matrix[route[-1]][0]  # Từ điểm cuối cùng quay về điểm 0
    return cost

def generate_neighbor(route):
        # Chọn hai điểm ngẫu nhiên để xác định đoạn con
        i, j = sorted(random.sample(range(len(route)), 2))
        # Đảo ngược đoạn giữa i và j
        neighbor = route[:]
        neighbor[i:j+1] = reversed(neighbor[i:j+1])
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

def tabu_search(n, k, distance_matrix, initial_route, max_iterations, tabu_size):

    # Khởi tạo
    current_route = initial_route
    best_route = initial_route
    best_cost = calculate_cost(initial_route, distance_matrix)
    tabu_list = []
    no_improvement = 0

    for iteration in range(max_iterations):
        # Tạo nhiều lân cận hợp lệ
        neighbors = [
            neighbor for neighbor in (generate_neighbor(current_route) for _ in range(100))
            if is_valid_route(neighbor, n, k)
        ]

        # Nếu không có lân cận hợp lệ, dừng tìm kiếm
        if not neighbors:
            break

        # Tính toán chi phí cho từng lân cận
        neighbor_cost = [
            (neighbor, calculate_cost(neighbor, distance_matrix)) 
            for neighbor in neighbors
        ]

        # Chọn lân cận tốt nhất không thuộc tabu hoặc tốt hơn best_cost
        next_route = None
        next_cost = float('inf')
        for neighbor, cost in neighbor_cost:
            if neighbor not in tabu_list or cost < best_cost:
                if cost < next_cost:
                    next_route = neighbor
                    next_cost = cost

        # Nếu không tìm thấy lân cận hợp lệ, dừng
        if next_route is None:
            break

        # Cập nhật giải pháp hiện tại
        current_route = next_route

        # Nếu tìm được giải pháp tốt hơn, cập nhật giải pháp tốt nhất
        if next_cost < best_cost:
            best_route = next_route
            best_cost = next_cost
            no_improvement = 0  # Reset bộ đếm nếu có cải thiện
        else:
            no_improvement += 1  # Tăng bộ đếm nếu không cải thiện

        # Thêm giải pháp hiện tại vào tabu list
        tabu_list.append(current_route)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        # Dừng sớm nếu không có cải thiện trong nhiều vòng lặp
        if no_improvement >= 2000:
            break

    return best_route, best_cost

def simulated_annealing(n, k, distance_matrix, initial_route, initial_temperature, cooling_rate, max_iterations):
    def calculate_cost(route, distance_matrix):
        cost = distance_matrix[0][route[0]]  # Từ điểm 0 đến điểm đầu tiên
        for i in range(len(route) - 1):
            cost += distance_matrix[route[i]][route[i + 1]]
        cost += distance_matrix[route[-1]][0]  # Từ điểm cuối cùng quay về điểm 0
        return cost

    # Khởi tạo
    current_route = initial_route
    current_cost = calculate_cost(initial_route, distance_matrix)
    best_route = current_route
    best_cost = current_cost
    temperature = initial_temperature
    no_improvement = 0
    max_no_improvement = 5000 # Số vòng lặp tối đa không có cải thiện

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
            no_improvement = 0
        else:
            no_improvement += 1
            
        if no_improvement > max_no_improvement:
            break

        # Giảm nhiệt độ
        temperature *= cooling_rate

        # Dừng sớm nếu nhiệt độ quá thấp
        if temperature < 1e-5:
            break

    return best_route, best_cost

def hybrid_greedy_tabu_sa(n, k, distance_matrix, tabu_iterations, tabu_size, sa_temperature, sa_cooling_rate, sa_iterations):
    initial_route = cbus_greedy(n, k, distance_matrix)
    
    initial_cost = calculate_cost(initial_route, distance_matrix)

    tabu_route, tabu_cost = tabu_search(n, k, distance_matrix, initial_route, tabu_iterations, tabu_size)

    best_route, best_cost = simulated_annealing(n, k, distance_matrix, tabu_route, sa_temperature, sa_cooling_rate, sa_iterations)
    
    return best_route, best_cost

# Input
n, k = map(int, input().split())

# Read distance matrix
distance_matrix = []
for _ in range(2 * n + 1):
    row = list(map(int, input().split()))
    distance_matrix.append(row)
    
# Tham số Hybrid
tabu_iterations = 10000
tabu_size = 100
sa_temperature = 1000000
sa_cooling_rate = 0.995
sa_iterations = 50000

# Chạy Hybrid Optimization
best_route, best_cost = hybrid_greedy_tabu_sa(
    n, k, distance_matrix,
    tabu_iterations, tabu_size,
    sa_temperature, sa_cooling_rate, sa_iterations
)

print(n)
print(*best_route)