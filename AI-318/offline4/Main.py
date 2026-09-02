import time

from TSP import readInput

from Greedy import greedyTSP

from simulated_annealing import (
    simulatedAnnealing,
    SAParameters
)

from utils import printResults

from experiments import (
    compareInitializations
)


def main():

    # ========================================================
    # READ INPUT
    # ========================================================

    filename = "input.txt"

    cost_matrix = readInput(
        filename
    )

    n = len(cost_matrix)

    # ========================================================
    # CONFIGURE SIMULATED ANNEALING
    # ========================================================

    params = SAParameters(

        initial_temperature=1000,

        cooling_rate=0.995,

        minimum_temperature=0.001,

        iterations_per_temperature=100,

        max_iterations=100000,

        random_seed=42
    )

    # ========================================================
    # RUN GREEDY
    # ========================================================

    start_time = time.perf_counter()

    greedy_tour, greedy_cost = greedyTSP(
        cost_matrix
    )

    greedy_time = (
        time.perf_counter()
        - start_time
    )

    # ========================================================
    # RUN SIMULATED ANNEALING
    # ========================================================

    start_time = time.perf_counter()

    sa_result = simulatedAnnealing(
        cost_matrix,
        params,
        initialization="random"
    )

    sa_time = (
        time.perf_counter()
        - start_time
    )

    # ========================================================
    # PRINT RESULTS
    # ========================================================

    printResults(

        n,

        greedy_tour,

        greedy_cost,

        greedy_time,

        sa_result,

        sa_time
    )

    # ========================================================
    # OPTIONAL:
    # EXPERIMENT 4
    # RANDOM VS GREEDY INITIALIZATION
    # ========================================================

    # compareInitializations(
    #     cost_matrix,
    #     params,
    #     runs=5
    # )


if __name__ == "__main__":

    main()