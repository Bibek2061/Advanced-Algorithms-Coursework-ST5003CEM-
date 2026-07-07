
# ADVANCED ALGORITHMS
# TASK 3 – ALGORITHMIC STRATEGIES

# MATRIX CHAIN MULTIPLICATION
# Dynamic Programming (Bottom-Up)


import sys


def matrix_chain_order(dimensions):

    n = len(dimensions)

    dp = [[0 for _ in range(n)] for _ in range(n)]

    for chain_length in range(2, n):

        for i in range(1, n - chain_length + 1):

            j = i + chain_length - 1

            dp[i][j] = sys.maxsize

            for k in range(i, j):

                cost = (
                    dp[i][k]
                    + dp[k + 1][j]
                    + dimensions[i - 1] * dimensions[k] * dimensions[j]
                )

                if cost < dp[i][j]:
                    dp[i][j] = cost

    return dp[1][n - 1]


# TEST MATRIX CHAIN


dimensions = [40, 20, 30, 10, 30]

minimum_cost = matrix_chain_order(dimensions)

print("\n==============================")
print("MATRIX CHAIN MULTIPLICATION")
print("==============================")
print("Matrix Dimensions :", dimensions)
print("Minimum Multiplications :", minimum_cost)

# MINIMUM NUMBER OF PLATFORMS
# Greedy Algorithm


def minimum_platforms(arrival, departure):

    arrival.sort()
    departure.sort()

    platform_needed = 1
    maximum_platforms = 1

    i = 1
    j = 0

    while i < len(arrival) and j < len(departure):

        if arrival[i] <= departure[j]:
            platform_needed += 1
            i += 1

            if platform_needed > maximum_platforms:
                maximum_platforms = platform_needed

        else:
            platform_needed -= 1
            j += 1

    return maximum_platforms

# HAMILTONIAN CYCLE
# Backtracking Algorithm


class HamiltonianGraph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for _ in range(vertices)]
                      for _ in range(vertices)]

    def is_safe(self, vertex, position, path):

        # Vertex should be connected to previous vertex
        if self.graph[path[position - 1]][vertex] == 0:
            return False

        # Vertex should not already exist in path
        if vertex in path:
            return False

        return True

    def hamiltonian_util(self, path, position):

        # All vertices included
        if position == self.V:

            # Last vertex connected to first
            return self.graph[path[position - 1]][path[0]] == 1

        for vertex in range(1, self.V):

            if self.is_safe(vertex, position, path):

                path[position] = vertex

                if self.hamiltonian_util(path, position + 1):
                    return True

                # Backtrack
                path[position] = -1

        return False

    def hamiltonian_cycle(self):

        path = [-1] * self.V

        path[0] = 0

        if not self.hamiltonian_util(path, 1):

            print("\nNo Hamiltonian Cycle Found")
            return

        print("\n==============================")
        print("HAMILTONIAN CYCLE")
        print("==============================")

        for vertex in path:
            print(vertex, end=" -> ")

        print(path[0])



# TEST MINIMUM PLATFORM


arrival = [900, 940, 950, 1100, 1500, 1800]
departure = [910, 1200, 1120, 1130, 1900, 2000]

platforms = minimum_platforms(arrival, departure)

print("\n==============================")
print("MINIMUM NUMBER OF PLATFORMS")
print("==============================")
print("Arrival Times   :", arrival)
print("Departure Times :", departure)
print("Platforms Needed:", platforms)

# TEST HAMILTONIAN CYCLE


graph = HamiltonianGraph(5)

graph.graph = [
    [0,1,1,0,1],
    [1,0,1,1,0],
    [1,1,0,1,1],
    [0,1,1,0,1],
    [1,0,1,1,0]
]

graph.hamiltonian_cycle()