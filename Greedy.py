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

n, k = map(int, input().split())

# Read distance matrix
distance_matrix = []
for _ in range(2 * n + 1):
    row = list(map(int, input().split()))
    distance_matrix.append(row)
    
route = cbus_greedy(n, k, distance_matrix)

print(n)
print(*route)