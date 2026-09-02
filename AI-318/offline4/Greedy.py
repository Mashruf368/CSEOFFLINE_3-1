from typing import List, Tuple


def greedyTSP(
        cost_matrix: List[List[float]]
) -> Tuple[List[int], float]:
    """
    Solves TSP using the Nearest Neighbor Greedy algorithm.
    """

    n = len(cost_matrix)

    visited = [False] * n

    current_city = 0

    tour = [0]

    visited[0] = True

    total_cost = 0

    # Visit remaining cities
    for _ in range(n - 1):

        next_city = -1
        minimum_cost = float("inf")

        # Find nearest unvisited city
        for city in range(n):

            if not visited[city]:

                travel_cost = (
                    cost_matrix[current_city][city]
                )

                if travel_cost < minimum_cost:

                    minimum_cost = travel_cost
                    next_city = city

        # Move to selected city
        tour.append(next_city)

        visited[next_city] = True

        total_cost += minimum_cost

        current_city = next_city

    # Return to City 0
    total_cost += cost_matrix[current_city][0]

    return tour, total_cost