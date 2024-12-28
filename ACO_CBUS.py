import numpy as np

def read_input():
    # Read from file
    with open('MiniProject/test_case_5.txt', 'r') as file:
        # Read n and k from first line
        n, k = map(int, file.readline().split())
        
        # Read distance matrix
        distances = []
        for _ in range(2*n + 1):
            row = list(map(int, file.readline().split()))
            distances.append(row)
            
    return n, k, distances

def format_output(n, route, best_distance):
    print(n)
    print(' '.join(map(str, route)))
    print(best_distance)

class ACO:
    def __init__(self, distance_matrix, n_passengers, bus_capacity, 
                 n_ants, n_iterations, evaporation_rate=0.1, 
                 alpha=1, beta=2):
        """
        Initialize ACO solver
        distance_matrix: Matrix of distances between points
        n_passengers: Number of passengers
        bus_capacity: Maximum bus capacity
        """
        self.distances = distance_matrix
        self.n_points = len(distance_matrix)
        self.n_passengers = n_passengers
        self.capacity = bus_capacity
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha  # Pheromone importance
        self.beta = beta    # Distance importance
        self.pheromones = self.initialize_pheromones()

    def initialize_pheromones(self):
        """Initialize pheromone matrix with small random values"""
        return np.ones((self.n_points, self.n_points)) * 1/self.n_passengers

    def get_available_points(self, current, passengers_on_board, served_passengers):
        """
        Determine valid next points based on current state
        Returns list of valid points considering capacity and passenger status
        """
        available = []
        
        # Can pickup if capacity allows
        if len(passengers_on_board) < self.capacity:
            for p in range(1, self.n_passengers + 1):
                if p not in passengers_on_board and p not in served_passengers:
                    available.append(p)
                    
        # Can drop off any passenger currently on board
        for p in passengers_on_board:
            available.append(p + self.n_passengers)
            
        # Can return to depot if all passengers served
        if len(served_passengers) == self.n_passengers:
            available.append(0)
            
        return available

    def select_next_point(self, current, available_points, passengers_on_board):
        """
        Select next point using ACO probability formula
        Combines pheromone levels and distance information
        """
        if not available_points:
            return None
            
        # Calculate probabilities using ACO formula
        pheromone = np.array([self.pheromones[current][j] for j in available_points])
        distance = np.array([1.0/(self.distances[current][j] + 1e-10) for j in available_points])
        probabilities = (pheromone ** self.alpha) * (distance ** self.beta)
        probabilities = probabilities / probabilities.sum()
        
        return np.random.choice(available_points, p=probabilities)

    def construct_solution(self):
        """
        Construct a complete solution for one ant
        Returns the route and its total distance
        """
        route = []  # Start at depot
        current = 0
        passengers_on_board = set()
        served_passengers = set()
        total_distance = 0
        
        while True:
            available = self.get_available_points(current, passengers_on_board, served_passengers)
            if not available:
                break
                
            next_point = self.select_next_point(current, available, passengers_on_board)
            
            # Update passenger status
            if next_point > self.n_passengers:  # Drop off
                passenger = next_point - self.n_passengers
                passengers_on_board.remove(passenger)
                served_passengers.add(passenger)
            elif next_point > 0:  # Pick up
                passengers_on_board.add(next_point)
                
            total_distance += self.distances[current][next_point]
            route.append(next_point)
            current = next_point
            
            if current == 0 and len(served_passengers) == self.n_passengers:
                break
                
        return route, total_distance

    def update_pheromones(self, solutions):
        """
        Update pheromone levels based on solution quality
        Includes evaporation and new deposits
        """
        # Evaporation
        self.pheromones *= (1 - self.evaporation_rate)
        
        # Add new pheromones
        for route, distance in solutions:
            deposit = 1.0 / distance
            for i in range(len(route) - 1):
                self.pheromones[route[i]][route[i+1]] += deposit

    def solve(self):
        """
        Main ACO solving loop
        Returns best route found and its distance
        """
        best_route = None
        best_distance = float('inf')
        
        for iteration in range(self.n_iterations):
            # Construct solutions for all ants
            solutions = [self.construct_solution() for _ in range(self.n_ants)]
            
            # Update best solution
            for route, distance in solutions:
                if distance < best_distance:
                    best_distance = distance
                    best_route = route
                    
            # Update pheromones
            self.update_pheromones(solutions)
            
        return best_route, best_distance
    

def main():
    # Read input
    n, k, distances = read_input()
    
    # Create and run solver
    solver = ACO(distances, n, k, n_ants=10, n_iterations=50)
    best_route, best_distance = solver.solve()
    
    # Output result
    format_output(n, best_route, best_distance)

if __name__ == "__main__":
    main()