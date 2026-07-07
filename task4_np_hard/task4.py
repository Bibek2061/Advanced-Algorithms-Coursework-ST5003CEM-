import time
import random

# ADVANCED ALGORITHMS
# TASK 4 – NP-HARD PROBLEM AND HEURISTICS
# Graph Colouring – Equitable Colouring


def create_graph():
    return {
        0: [1, 2, 3],
        1: [0, 2, 4],
        2: [0, 1, 3, 5],
        3: [0, 2, 5],
        4: [1, 5],
        5: [2, 3, 4]
    }


def is_valid(graph, colours):
    for vertex in graph:
        for neighbour in graph[vertex]:
            if colours[vertex] == colours[neighbour]:
                return False
    return True


def is_equitable(colours, total_colours):
    count = [0] * total_colours
    for colour in colours.values():
        count[colour] += 1
    return max(count) - min(count) <= 1


def colour_score(graph, colours, total_colours):
    conflicts = 0

    for vertex in graph:
        for neighbour in graph[vertex]:
            if vertex < neighbour and colours[vertex] == colours[neighbour]:
                conflicts += 1

    count = [0] * total_colours
    for colour in colours.values():
        count[colour] += 1

    imbalance = max(count) - min(count)

    return conflicts + imbalance


# GREEDY HEURISTIC

def greedy_colouring(graph, total_colours):
    colours = {}
    colour_count = [0] * total_colours

    for vertex in graph:
        used_colours = set()

        for neighbour in graph[vertex]:
            if neighbour in colours:
                used_colours.add(colours[neighbour])

        possible = [c for c in range(total_colours) if c not in used_colours]

        if possible:
            selected = min(possible, key=lambda c: colour_count[c])
        else:
            selected = min(range(total_colours), key=lambda c: colour_count[c])

        colours[vertex] = selected
        colour_count[selected] += 1

    return colours


# LOCAL SEARCH HEURISTIC

def local_search(graph, colours, total_colours, iterations=200):
    best = colours.copy()
    best_score = colour_score(graph, best, total_colours)

    for _ in range(iterations):
        candidate = best.copy()
        vertex = random.choice(list(graph.keys()))
        candidate[vertex] = random.randint(0, total_colours - 1)

        candidate_score = colour_score(graph, candidate, total_colours)

        if candidate_score < best_score:
            best = candidate
            best_score = candidate_score

    return best


if __name__ == "__main__":
    graph = create_graph()
    total_colours = 3

    print("\n==============================")
    print("GRAPH COLOURING - EQUITABLE COLOURING")
    print("==============================")

    start = time.perf_counter()
    greedy_result = greedy_colouring(graph, total_colours)
    greedy_time = time.perf_counter() - start

    start = time.perf_counter()
    local_result = local_search(graph, greedy_result, total_colours)
    local_time = time.perf_counter() - start

    print("\nGreedy Heuristic Result:")
    print(greedy_result)
    print("Valid Colouring:", is_valid(graph, greedy_result))
    print("Equitable:", is_equitable(greedy_result, total_colours))
    print("Quality Score:", colour_score(graph, greedy_result, total_colours))

    print("\nLocal Search Result:")
    print(local_result)
    print("Valid Colouring:", is_valid(graph, local_result))
    print("Equitable:", is_equitable(local_result, total_colours))
    print("Quality Score:", colour_score(graph, local_result, total_colours))

    print("\nRuntime Comparison")
    print("------------------")
    print(f"Greedy Heuristic : {greedy_time:.8f} seconds")
    print(f"Local Search     : {local_time:.8f} seconds")