import time

from simulated_annealing import (
    simulatedAnnealing,
    SAParameters
)


def compareInitializations(
        cost_matrix,
        params: SAParameters,
        runs: int = 5
):

    results = {}

    # Test both initialization methods
    for initialization in [
        "random",
        "greedy"
    ]:

        costs = []

        times = []

        print()

        print("=" * 60)

        print(
            f"{initialization.upper()} "
            f"INITIALIZATION"
        )

        print("=" * 60)

        for run in range(runs):

            start_time = time.perf_counter()

            result = simulatedAnnealing(
                cost_matrix,
                params,
                initialization
            )

            execution_time = (
                time.perf_counter()
                - start_time
            )

            costs.append(
                result["best_cost"]
            )

            times.append(
                execution_time
            )

            print(
                f"Run {run + 1}: "
                f"Best Cost = "
                f"{result['best_cost']:.2f}, "
                f"Time = "
                f"{execution_time:.6f}s"
            )

        # Store summary
        results[initialization] = {

            "best":
                min(costs),

            "average":
                sum(costs) / len(costs),

            "worst":
                max(costs),

            "average_time":
                sum(times) / len(times)
        }

    # ========================================================
    # SUMMARY
    # ========================================================

    print()

    print("=" * 60)

    print(
        "INITIALIZATION COMPARISON SUMMARY"
    )

    print("=" * 60)

    for initialization, result in results.items():

        print()

        print(
            initialization.upper()
            + " INITIALIZATION"
        )

        print(
            f"Best Result: "
            f"{result['best']:.2f}"
        )

        print(
            f"Average Result: "
            f"{result['average']:.2f}"
        )

        print(
            f"Worst Result: "
            f"{result['worst']:.2f}"
        )

        print(
            f"Average Execution Time: "
            f"{result['average_time']:.6f}s"
        )

    return results