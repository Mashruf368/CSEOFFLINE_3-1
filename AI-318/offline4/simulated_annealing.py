import random
import math
from dataclasses import dataclass
from typing import List

from TSP import (
    calculateTourCost,
    generateRandomTour,
    validateTour
)

from Greedy import greedyTSP


# ============================================================
# SIMULATED ANNEALING PARAMETERS
# ============================================================

@dataclass
class SAParameters:

    initial_temperature: float = 1000.0

    cooling_rate: float = 0.995

    minimum_temperature: float = 0.001

    iterations_per_temperature: int = 100

    max_iterations: int = 100000

    random_seed: int = None


# ============================================================
# NEIGHBOR GENERATION
# 2-OPT SEGMENT REVERSAL
# ============================================================

def generateNeighbor(tour: List[int]) -> List[int]:
    """
    Generates a neighboring solution using 2-opt.

    City 0 remains fixed.
    """

    n = len(tour)

    if n <= 2:
        return tour.copy()

    # Choose two positions excluding City 0
    i, j = sorted(
        random.sample(range(1, n), 2)
    )

    neighbor = tour.copy()

    # Reverse selected segment
    neighbor[i:j + 1] = reversed(
        neighbor[i:j + 1]
    )

    return neighbor


# ============================================================
# SIMULATED ANNEALING
# ============================================================

def simulatedAnnealing(
        cost_matrix: List[List[float]],
        params: SAParameters,
        initialization: str = "random"
):

    # Set random seed
    if params.random_seed is not None:

        random.seed(params.random_seed)

    n = len(cost_matrix)

    # --------------------------------------------------------
    # INITIAL SOLUTION
    # --------------------------------------------------------

    if initialization.lower() == "random":

        current_tour = generateRandomTour(n)

    elif initialization.lower() == "greedy":

        current_tour, _ = greedyTSP(
            cost_matrix
        )

    else:

        raise ValueError(
            "Initialization must be "
            "'random' or 'greedy'."
        )

    # Validate initial solution
    if not validateTour(current_tour, n):

        raise ValueError(
            "Invalid initial tour."
        )

    current_cost = calculateTourCost(
        current_tour,
        cost_matrix
    )

    # Store initial cost before SA changes anything
    initial_cost = current_cost

    # Best solution found so far
    best_tour = current_tour.copy()

    best_cost = current_cost

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    total_iterations = 0

    accepted_moves = 0

    worse_moves_accepted = 0

    temperature = params.initial_temperature

    # --------------------------------------------------------
    # MAIN SA LOOP
    # --------------------------------------------------------

    while (
        temperature > params.minimum_temperature
        and total_iterations < params.max_iterations
    ):

        for _ in range(
            params.iterations_per_temperature
        ):

            if (
                total_iterations
                >= params.max_iterations
            ):
                break

            # Generate neighbor
            neighbor_tour = generateNeighbor(
                current_tour
            )

            # Validate neighbor
            if not validateTour(
                neighbor_tour,
                n
            ):

                raise ValueError(
                    "Invalid neighbor generated."
                )

            # Calculate neighbor cost
            neighbor_cost = calculateTourCost(
                neighbor_tour,
                cost_matrix
            )

            # Calculate Delta
            delta = (
                neighbor_cost - current_cost
            )

            accept = False

            # ------------------------------------------------
            # CASE 1:
            # NEW SOLUTION IS BETTER
            # ------------------------------------------------

            if delta <= 0:

                accept = True

            # ------------------------------------------------
            # CASE 2:
            # NEW SOLUTION IS WORSE
            # ------------------------------------------------

            else:

                probability = math.exp(
                    -delta / temperature
                )

                random_value = random.random()

                if random_value < probability:

                    accept = True

                    worse_moves_accepted += 1

            # ------------------------------------------------
            # ACCEPT MOVE
            # ------------------------------------------------

            if accept:

                current_tour = neighbor_tour

                current_cost = neighbor_cost

                accepted_moves += 1

                # Update best solution
                if current_cost < best_cost:

                    best_tour = (
                        current_tour.copy()
                    )

                    best_cost = current_cost

            total_iterations += 1

        # ----------------------------------------------------
        # COOLING
        # ----------------------------------------------------

        temperature *= params.cooling_rate

    # --------------------------------------------------------
    # RETURN RESULTS
    # --------------------------------------------------------

    return {

        "initial_cost": initial_cost,

        "best_tour": best_tour,

        "best_cost": best_cost,

        "iterations": total_iterations,

        "accepted_moves": accepted_moves,

        "worse_moves_accepted":
            worse_moves_accepted,

        "initial_temperature":
            params.initial_temperature,

        "cooling_rate":
            params.cooling_rate,

        "initialization":
            initialization
    }