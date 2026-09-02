from typing import List

from TSP import formatTour


def printResults(
        n: int,

        greedy_tour: List[int],

        greedy_cost: float,

        greedy_time: float,

        sa_result: dict,

        sa_time: float
):

    print()

    print("=" * 60)

    print(
        "TRAVELLING SALESMAN PROBLEM"
    )

    print("=" * 60)

    print(
        f"Number of Cities: {n}"
    )

    # ========================================================
    # GREEDY RESULTS
    # ========================================================

    print()

    print(
        "-" * 15
        + " GREEDY METHOD "
        + "-" * 15
    )

    print("Tour:")

    print(
        formatTour(greedy_tour)
    )

    print(
        f"Total Cost: "
        f"{greedy_cost:.2f}"
    )

    print(
        f"Execution Time: "
        f"{greedy_time:.6f} seconds"
    )

    # ========================================================
    # SIMULATED ANNEALING RESULTS
    # ========================================================

    print()

    print(
        "-" * 12
        + " SIMULATED ANNEALING "
        + "-" * 12
    )

    print(
        f"Initialization Method: "
        f"{sa_result['initialization'].capitalize()}"
    )

    print()

    print(
        f"Initial Cost: "
        f"{sa_result['initial_cost']:.2f}"
    )

    print()

    print("Best Tour Found:")

    print(
        formatTour(
            sa_result["best_tour"]
        )
    )

    print(
        f"Best Cost: "
        f"{sa_result['best_cost']:.2f}"
    )

    print()

    print(
        f"Initial Temperature: "
        f"{sa_result['initial_temperature']}"
    )

    print(
        f"Cooling Rate: "
        f"{sa_result['cooling_rate']}"
    )

    print(
        f"Total Iterations: "
        f"{sa_result['iterations']}"
    )

    print(
        f"Accepted Moves: "
        f"{sa_result['accepted_moves']}"
    )

    print(
        f"Worse Moves Accepted: "
        f"{sa_result['worse_moves_accepted']}"
    )

    print(
        f"Execution Time: "
        f"{sa_time:.6f} seconds"
    )

    # ========================================================
    # COMPARISON
    # ========================================================

    print()

    print(
        "-" * 17
        + " COMPARISON "
        + "-" * 17
    )

    print(
        f"Greedy Cost: "
        f"{greedy_cost:.2f}"
    )

    print(
        f"Simulated Annealing Cost: "
        f"{sa_result['best_cost']:.2f}"
    )

    # Calculate improvement
    improvement = (
        (
            greedy_cost
            - sa_result["best_cost"]
        )
        / greedy_cost
    ) * 100

    print(
        f"Improvement Percentage: "
        f"{improvement:.2f}%"
    )

    print()

    if (
        sa_result["best_cost"]
        < greedy_cost
    ):

        print(
            "Best Method for This Run: "
            "Simulated Annealing"
        )

    elif (
        greedy_cost
        < sa_result["best_cost"]
    ):

        print(
            "Best Method for This Run: "
            "Greedy"
        )

    else:

        print(
            "Best Method for This Run: "
            "Both methods produced the same cost."
        )

    print("=" * 60)