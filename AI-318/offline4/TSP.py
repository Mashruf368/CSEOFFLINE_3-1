from typing import List


def readInput(filename: str) -> List[List[float]]:
    """
    Reads the TSP cost matrix from an input file.
    """

    with open(filename, "r") as file:
        lines = file.readlines()

    # Remove empty lines
    lines = [line.strip() for line in lines if line.strip()]

    n = int(lines[0])

    if len(lines) - 1 < n:
        raise ValueError("Not enough rows in the input file.")

    cost_matrix = []

    for i in range(n):

        row = list(map(float, lines[i + 1].split()))

        if len(row) != n:
            raise ValueError(
                f"Row {i} has {len(row)} values. Expected {n}."
            )

        cost_matrix.append(row)

    return cost_matrix


def calculateTourCost(
        tour: List[int],
        cost_matrix: List[List[float]]
) -> float:
    """
    Calculates the total cost of a TSP tour.

    Example:
    [0, 1, 4, 3, 2]

    Cost includes:
    0 -> 1 -> 4 -> 3 -> 2 -> 0
    """

    total_cost = 0
    n = len(tour)

    for i in range(n - 1):

        current_city = tour[i]
        next_city = tour[i + 1]

        total_cost += cost_matrix[current_city][next_city]

    # Return to starting city
    total_cost += cost_matrix[tour[-1]][tour[0]]

    return total_cost


def generateRandomTour(n: int) -> List[int]:
    """
    Generates a random tour while keeping City 0 fixed.
    """

    import random

    cities = list(range(1, n))

    random.shuffle(cities)

    return [0] + cities


def validateTour(tour: List[int], n: int) -> bool:
    """
    Checks whether a tour is valid.
    """

    # Must contain N cities
    if len(tour) != n:
        return False

    # Must start from City 0
    if tour[0] != 0:
        return False

    # Must contain exactly cities 0 to N-1
    if set(tour) != set(range(n)):
        return False

    # No duplicates
    if len(set(tour)) != n:
        return False

    return True


def formatTour(tour: List[int]) -> str:
    """
    Converts:

    [0, 1, 4, 3, 2]

    into:

    0 -> 1 -> 4 -> 3 -> 2 -> 0
    """

    complete_tour = tour + [tour[0]]

    return " -> ".join(map(str, complete_tour))