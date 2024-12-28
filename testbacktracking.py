class CBUSolver:
    def __init__(self, n, k, distance_matrix):
        self.n = n  # number of passengers
        self.k = k  # bus capacity
        self.c = distance_matrix  # distance matrix
        self.current_path = [0] * (2 * n + 1)  # current route being explored
        self.min_cost = float('inf')  # minimum cost found
        self.visited = [False] * (2 * n + 1)  # track visited points
        self.passengers_on_bus = 0  # current number of passengers
        self.current_cost = 0  # running cost of current path

    def is_valid_next_point(self, point):
        """Check if adding this point to the route is valid."""
        # Already visited this point
        if self.visited[point]:
            return False
            
        if point <= self.n:  # pickup point
            # Check if bus is full
            if self.passengers_on_bus >= self.k:
                return False
        else:  # dropoff point
            # Can't drop off if haven't picked up
            if not self.visited[point - self.n]:
                return False
                
        return True

    def try_next_point(self, pos, last_point):
        """
        Recursive backtracking function to explore possible routes.
        pos: current position in route
        last_point: last point visited
        """
        # Pruning: if current cost exceeds min_cost, no need to continue
        if self.current_cost >= self.min_cost:
            return

        # Base case: all points visited
        if pos == 2 * self.n + 1:
            total_cost = self.current_cost + self.c[last_point][0]  # add cost to return to start
            if total_cost < self.min_cost:
                self.min_cost = total_cost
            return

        # Try all possible next points
        for next_point in range(1, 2 * self.n + 1):
            if self.is_valid_next_point(next_point):
                # Calculate cost to add this point
                additional_cost = self.c[last_point][next_point]
                
                # Update state
                self.current_path[pos] = next_point
                self.visited[next_point] = True
                self.current_cost += additional_cost
                
                # Update passenger count
                if next_point <= self.n:
                    self.passengers_on_bus += 1
                else:
                    self.passengers_on_bus -= 1

                # Recursive call
                self.try_next_point(pos + 1, next_point)

                # Backtrack: restore state
                self.visited[next_point] = False
                self.current_cost -= additional_cost
                if next_point <= self.n:
                    self.passengers_on_bus -= 1
                else:
                    self.passengers_on_bus += 1

    def solve(self):
        """Solve the CBUS problem and return the solution."""
        self.try_next_point(1, 0)  # start from position 1 (after depot)
        return self.min_cost

def solve_cbus():
    # Read input
    n, k = map(int, input().split())
    
    # Read distance matrix
    c = []
    for _ in range(2 * n + 1):
        row = list(map(int, input().split()))
        c.append(row)
    
    # Solve
    solver = CBUSolver(n, k, c)
    min_cost = solver.solve()
    
    # Output
    print(min_cost)

if __name__ == "__main__":
    solve_cbus()