import heapq
import time
import matplotlib.pyplot as plt


# ============================================================
# ADVANCED ALGORITHMS
# TASK 2 – GRAPH ALGORITHMS AND PATHFINDING
# Transportation Network Optimisation
# ============================================================


# ============================================================
# WEIGHTED GRAPH USING ADJACENCY LIST
# ============================================================

class Graph:

    def __init__(self):
        self.adj_list = {}

    def add_city(self, city):
        if city not in self.adj_list:
            self.adj_list[city] = []

    def add_edge(self, source, destination, weight):
        self.add_city(source)
        self.add_city(destination)

        self.adj_list[source].append((destination, weight))

    def get_cities(self):
        return list(self.adj_list.keys())

    def get_edges(self):
        edges = []

        for source in self.adj_list:
            for destination, weight in self.adj_list[source]:
                edges.append((source, destination, weight))

        return edges

    def display_graph(self):
        print("\nTRANSPORTATION NETWORK")
        print("======================")

        for city in self.adj_list:
            print(f"{city} -> {self.adj_list[city]}")





# ============================================================
# DIJKSTRA SHORTEST PATH
# ============================================================

def dijkstra(graph, start):

    distances = {}

    previous = {}

    for city in graph.adj_list:
        distances[city] = float("inf")
        previous[city] = None

    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:

        current_distance, current_city = heapq.heappop(priority_queue)

        if current_distance > distances[current_city]:
            continue

        for neighbour, weight in graph.adj_list[current_city]:

            distance = current_distance + weight

            if distance < distances[neighbour]:

                distances[neighbour] = distance
                previous[neighbour] = current_city

                heapq.heappush(priority_queue,
                               (distance, neighbour))

    return distances, previous


# ============================================================
# PRINT SHORTEST PATH
# ============================================================

def print_shortest_paths(graph, start):

    distances, previous = dijkstra(graph, start)

    print("\n==============================")
    print("DIJKSTRA SHORTEST PATH")
    print("==============================")

    for city in graph.adj_list:

        print(f"{start} -> {city} : {distances[city]} km") 


# ============================================================
# PRIM'S MINIMUM SPANNING TREE
# ============================================================

def prim(graph, start):

    visited = set()

    priority_queue = [(0, start, None)]

    mst = []

    total_cost = 0

    while priority_queue:

        weight, current, parent = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        if parent is not None:
            mst.append((parent, current, weight))
            total_cost += weight

        for neighbour, edge_weight in graph.adj_list[current]:

            if neighbour not in visited:
                heapq.heappush(priority_queue,
                               (edge_weight, neighbour, current))

    return mst, total_cost


# ============================================================
# DISPLAY MST
# ============================================================

def display_mst(graph):

    mst, total = prim(graph, "Kathmandu")

    print("\n==============================")
    print("PRIM'S MINIMUM SPANNING TREE")
    print("==============================")

    for source, destination, weight in mst:
        print(f"{source} --> {destination} ({weight} km)")

    print(f"\nTotal Cost = {total} km")


# ============================================================
# BELLMAN-FORD ALGORITHM
# ============================================================

def bellman_ford(graph, start):

    distance = {}

    for city in graph.adj_list:
        distance[city] = float("inf")

    distance[start] = 0

    vertices = list(graph.adj_list.keys())

    # Relax edges
    for _ in range(len(vertices) - 1):

        for source in graph.adj_list:

            for destination, weight in graph.adj_list[source]:

                if distance[source] != float("inf") and \
                        distance[source] + weight < distance[destination]:

                    distance[destination] = distance[source] + weight

    # Negative cycle detection
    negative_cycle = False

    for source in graph.adj_list:

        for destination, weight in graph.adj_list[source]:

            if distance[source] != float("inf") and \
                    distance[source] + weight < distance[destination]:

                negative_cycle = True

    print("\n==============================")
    print("BELLMAN-FORD ALGORITHM")
    print("==============================")

    if negative_cycle:
        print("Negative Weight Cycle Detected!")
    else:
        print("No Negative Weight Cycle Found.\n")

        for city in distance:
            print(f"{start} -> {city} : {distance[city]} km")


# ============================================================
# RUNTIME COMPARISON
# ============================================================

def compare_runtime():

    sizes = [100, 1000, 10000]

    dijkstra_times = []
    prim_times = []
    bellman_times = []

    for size in sizes:

        graph = Graph()

        for i in range(size):
            graph.add_city(f"City_{i}")

        for i in range(size - 1):
            graph.add_edge(f"City_{i}", f"City_{i+1}", i % 20 + 1)

        # ---------------- Dijkstra ----------------
        start = time.perf_counter()
        dijkstra(graph, "City_0")
        end = time.perf_counter()
        dijkstra_times.append(end - start)

        # ---------------- Prim ----------------
        start = time.perf_counter()
        prim(graph, "City_0")
        end = time.perf_counter()
        prim_times.append(end - start)

        # ---------------- Bellman Ford ----------------
        start = time.perf_counter()
        bellman_ford(graph, "City_0")
        end = time.perf_counter()
        bellman_times.append(end - start)

    print("\n==============================")
    print("RUNTIME COMPARISON")
    print("==============================")

    print("Nodes\tDijkstra\tPrim\tBellman-Ford")

    for i in range(len(sizes)):
        print(
            f"{sizes[i]}\t"
            f"{dijkstra_times[i]:.6f}\t"
            f"{prim_times[i]:.6f}\t"
            f"{bellman_times[i]:.6f}"
        )

    plt.figure(figsize=(8,5))

    plt.plot(sizes, dijkstra_times, marker="o", label="Dijkstra")
    plt.plot(sizes, prim_times, marker="o", label="Prim")
    plt.plot(sizes, bellman_times, marker="o", label="Bellman-Ford")

    plt.title("Task 2 Runtime Comparison")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (seconds)")
    plt.grid(True)
    plt.legend()

    plt.savefig("graphs/task2_runtime_comparison.png")

    plt.show()


# ============================================================
# SAMPLE TRANSPORTATION NETWORK
# ============================================================

def create_transport_network():
    graph = Graph()

    graph.add_edge("Kathmandu", "Bhaktapur", 13)
    graph.add_edge("Kathmandu", "Lalitpur", 7)
    graph.add_edge("Kathmandu", "Pokhara", 200)

    graph.add_edge("Bhaktapur", "Dhulikhel", 25)
    graph.add_edge("Bhaktapur", "Lalitpur", 18)

    graph.add_edge("Lalitpur", "Hetauda", 85)
    graph.add_edge("Lalitpur", "Dhulikhel", 30)

    graph.add_edge("Dhulikhel", "Sindhuli", 95)
    graph.add_edge("Sindhuli", "Itahari", 210)

    graph.add_edge("Hetauda", "Sindhuli", 140)
    graph.add_edge("Hetauda", "Pokhara", 170)

    graph.add_edge("Pokhara", "Butwal", 160)
    graph.add_edge("Butwal", "Itahari", 320)

    return graph


# ============================================================
# BASIC TEST
# ============================================================

if __name__ == "__main__":
    graph = create_transport_network()
    graph.display_graph()


print_shortest_paths(graph, "Kathmandu")
display_mst(graph)
bellman_ford(graph, "Kathmandu")
compare_runtime()