import math

from Matrix import Matrix
from Heuristics import Heuristics
from BFS import BFS
from Report import generate_report


def inversion_count(board):
    arr = [x for x in board if x != 0]
    inv = 0

    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1

    return inv


def is_solvable(board):
    inv = inversion_count(board)
    size = int(math.sqrt(len(board)))

    if size % 2 == 1:
        return inv % 2 == 0

    zero = board.index(0)
    top_row = zero // size
    bottom_row = size - top_row

    if bottom_row % 2 == 0:
        return inv % 2 == 1
    else:
        return inv % 2 == 0


def choose_heuristic():
    print("\nChoose Heuristic")
    print("1. Hamming Distance")
    print("2. Manhattan Distance")
    print("3. Euclidean Distance")
    print("4. Linear Conflict")

    choice = int(input("Choice: "))

    if choice == 1:
        return Heuristics.Hamming_Distance
    elif choice == 2:
        return Heuristics.Manhattan_Distance
    elif choice == 3:
        return Heuristics.Euclidean_Distance
    elif choice == 4:
        return Heuristics.Linear_Conflict
    else:
        print("Invalid choice.")
        exit()


def solve_board(size, board, heuristic):

    print("\n==============================")
    print(f"{size} x {size} Puzzle")

    if not is_solvable(board):
        print("Unsolvable puzzle")
        return None

    results = []

    for w in [1.0, 1.2, 2.0, 5.0]:

        zero = board.index(0)
        initial = Matrix(board.copy(), zero, 0, 0, None)

        solver = BFS(initial, heuristic)

        cost, expanded = solver.solve(w)

        results.append((w, cost, expanded))

    return results


def manual_input(heuristic):

    size = int(input("Enter matrix size: "))
    print("Enter the board row by row:")

    board = []

    for _ in range(size):
        board.extend(map(int, input().split()))

    solve_board(size, board, heuristic)


def file_input(heuristic):

    all_results = []

    with open("input.txt", "r") as f:

        while True:

            line = f.readline()

            if not line:
                break

            line = line.strip()

            if line == "":
                continue

            size = int(line)

            board = []

            for _ in range(size):
                board.extend(map(int, f.readline().split()))

            results = solve_board(size, board, heuristic)

            if results is not None:
                all_results.append(results)

    generate_report(all_results)


def main():

    print("1. Manual Input")
    print("2. Read from input.txt")

    option = int(input("Choice: "))

    heuristic = choose_heuristic()

    if option == 1:
        manual_input(heuristic)

    elif option == 2:
        file_input(heuristic)

    else:
        print("Invalid option")


if __name__ == "__main__":
    main()