import csv
from Heuristics import (
    heuristic1,
    heuristic2,
    heuristic3,
    heuristic4,
    custom_heuristic,
    get_best_move
)

from Mancala import Mancala


# ============================================================
# CONFIGURATION
# ============================================================

SAME_WEIGHTS = (10,1,2,5)

DEPTHS = [2,4,6,8]


# ============================================================
# PRINT GAME OPTION
# ============================================================

# True  = print every move of every simulated game
# False = do not print the moves
PRINT_GAME = True


# ============================================================
# HEURISTIC FACTORY
# ============================================================

def make_heuristic(h_num, weights):

    w1, w2, w3, w4 = weights

    if h_num == 1:

        return lambda state: heuristic1(state)

    elif h_num == 2:

        return lambda state: heuristic2(
            state,
            w1,
            w2
        )

    elif h_num == 3:

        return lambda state: heuristic3(
            state,
            w1,
            w2,
            w3
        )

    elif h_num == 4:

        return lambda state: heuristic4(
            state,
            w1,
            w2,
            w3,
            w4
        )
    elif h_num == 5:
        return lambda state: custom_heuristic(state,w1,w2,w3,w4)

    else:

        raise ValueError("Invalid heuristic number")


# ============================================================
# PRINT BOARD
# ============================================================

def print_board(board):

    print()

    print("                 P1 SIDE")

    print("        +----+----+----+----+----+----+")

    print("        |", end="")

    # Player 1 side
    for i in range(12, 6, -1):
        print(f" {board[i]:2d} |", end="")

    print()

    print("        +----+----+----+----+----+----+")

    print(
        f" P1 [{board[13]:2d}]"
        f"                                   "
        f"P0 [{board[6]:2d}]"
    )

    print("        +----+----+----+----+----+----+")

    print("        |", end="")

    # Player 0 side
    for i in range(0, 6):
        print(f" {board[i]:2d} |", end="")

    print()

    print("        +----+----+----+----+----+----+")

    print("                 P0 SIDE")

    print()


# ============================================================
# PLAY ONE GAME
# ============================================================

def play_game(
    h0_num,
    h1_num,
    h0_depth,
    h1_depth,
    h0_weights,
    h1_weights,
    verbose=False
):

    board = [
        4, 4, 4, 4, 4, 4, 0,
        4, 4, 4, 4, 4, 4, 0
    ]

    game = Mancala(
        board,
        player=0,
        root_player=0
    )

    h0 = make_heuristic(
        h0_num,
        h0_weights
    )

    h1 = make_heuristic(
        h1_num,
        h1_weights
    )


    # --------------------------------------------------------
    # Game loop
    # --------------------------------------------------------

    turn_number = 0

    while not game.is_terminal():

        turn_number += 1

        player = game.current_player

        if player == 0:
            heuristic = h0
            depth = h0_depth
            heuristic_num = h0_num
        else:
            heuristic = h1
            depth = h1_depth
            heuristic_num = h1_num

        # --------------------------------------------------------
        # PRINT CURRENT STATE
        # --------------------------------------------------------

        if verbose:

            print()
            print("=" * 80)
            print(f"TURN {turn_number}")
            print("=" * 80)

            print(f"Current Player: Player {player}")
            print(f"Heuristic: H{heuristic_num}")
            print(f"Depth: {depth}")

            print()
            print("Board BEFORE move:")
            print_board(game.board)

            print(
                f"Stores: "
                f"P0 = {game.board[6]}, "
                f"P1 = {game.board[13]}"
            )

        # --------------------------------------------------------
        # SAVE INFORMATION BEFORE MOVE
        # --------------------------------------------------------

        old_player = game.current_player

        # --------------------------------------------------------
        # GET BEST MOVE
        # --------------------------------------------------------

        move = get_best_move(
            game.board,
            player,
            depth,
            heuristic
        )

        if move is None:

            print("No valid move!")

            break

        # --------------------------------------------------------
        # PRINT CHOSEN MOVE
        # --------------------------------------------------------

        if verbose:

            print()
            print(
                f"Player {player} "
                f"(H{heuristic_num}) "
                f"chooses move: {move}"
            )

        # --------------------------------------------------------
        # APPLY MOVE
        # --------------------------------------------------------

        if not game.apply_move(move):

            print(
                f"ERROR: invalid move {move}"
            )

            break

        # --------------------------------------------------------
        # DETERMINE WHAT HAPPENED
        # --------------------------------------------------------

        extra_move = (
            game.current_player == old_player
        )

        # --------------------------------------------------------
        # PRINT RESULT OF MOVE
        # --------------------------------------------------------

        if verbose:

            print()
            print("Board AFTER move:")
            print_board(game.board)

            if extra_move:

                print(
                    f"*** Player {old_player} "
                    f"gets an EXTRA MOVE ***"
                )

            else:

                print(
                    f"Player changes: "
                    f"{old_player} -> "
                    f"{game.current_player}"
                )

            print(
                f"Stores: "
                f"P0 = {game.board[6]}, "
                f"P1 = {game.board[13]}"
            )


    # ========================================================
    # FINAL SWEEP
    # ========================================================

    if verbose:

        print()
        print("=" * 80)
        print("GAME OVER - FINAL SWEEP")
        print("=" * 80)

        print("Board before final sweep:")
        print_board(game.board)


    for i in range(6):

        game.board[6] += game.board[i]
        game.board[i] = 0


    for i in range(7, 13):

        game.board[13] += game.board[i]
        game.board[i] = 0


    # --------------------------------------------------------
    # PRINT FINAL BOARD
    # --------------------------------------------------------

    if verbose:

        print()
        print("Board AFTER final sweep:")
        print_board(game.board)


    # ========================================================
    # RESULT
    # ========================================================

    if game.board[6] > game.board[13]:

        winner = 0

    elif game.board[13] > game.board[6]:

        winner = 1

    else:

        winner = -1


    # --------------------------------------------------------
    # PRINT FINAL RESULT
    # --------------------------------------------------------

    if verbose:

        print()
        print("=" * 80)
        print("FINAL RESULT")
        print("=" * 80)

        print(
            f"Player 0 (H{h0_num}): "
            f"{game.board[6]}"
        )

        print(
            f"Player 1 (H{h1_num}): "
            f"{game.board[13]}"
        )

        if winner == 0:

            print(
                f"WINNER: Player 0 (H{h0_num})"
            )

        elif winner == 1:

            print(
                f"WINNER: Player 1 (H{h1_num})"
            )

        else:

            print("RESULT: DRAW")

        print("=" * 80)


    return (
        winner,
        game.board[6],
        game.board[13]
    )


# ============================================================
# RUN ONE EXPERIMENT
# ============================================================

def run_experiment(
    h0_num,
    h1_num,
    h0_depth,
    h1_depth,
    weights
):

    winner, p0_score, p1_score = play_game(
        h0_num=h0_num,
        h1_num=h1_num,

        h0_depth=h0_depth,
        h1_depth=h1_depth,

        h0_weights=weights,
        h1_weights=weights,

        verbose=False
    )


    if winner == 0:

        winner_text = f"H{h0_num}"

    elif winner == 1:

        winner_text = f"H{h1_num}"

    else:

        winner_text = "DRAW"


    print(
        f"H{h0_num} depth {h0_depth}"
        f" vs "
        f"H{h1_num} depth {h1_depth}"
    )

    print(
        f"Score: H{h0_num} = {p0_score}, "
        f"H{h1_num} = {p1_score}"
    )

    print(
        f"Winner: {winner_text}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 100)
    print("MANCALA HEURISTIC EXPERIMENTS")
    print("=" * 100)

    print(f"Weights: {SAME_WEIGHTS}")
    print(f"Depths: {DEPTHS}")
    print("One game per depth combination")

    if PRINT_GAME:
        print("GAME PRINTING: ON")
    else:
        print("GAME PRINTING: OFF")

    print("=" * 100)


    # --------------------------------------------------------
    # CSV FILES
    # --------------------------------------------------------

    csv_file = "mancala_results.csv"
    summary_file = "summary.csv"


    # --------------------------------------------------------
    # Statistics for each heuristic
    # --------------------------------------------------------

    stats = {
        1: {
            "wins": 0,
            "losses": 0,
            "draws": 0
        },
        2: {
            "wins": 0,
            "losses": 0,
            "draws": 0
        },
        3: {
            "wins": 0,
            "losses": 0,
            "draws": 0
        },
        4: {
            "wins": 0,
            "losses": 0,
            "draws": 0
        },
        5: {
            "wins":0,
            "losses":0,
            "draws":0
        }
    }


    # --------------------------------------------------------
    # Create results CSV
    # --------------------------------------------------------

    with open(csv_file, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "H0",
            "H1",
            "H0_Depth",
            "H1_Depth",
            "H0_Score",
            "H1_Score",
            "Winner"
        ])


        # ----------------------------------------------------
        # All ordered pairs
        # ----------------------------------------------------

        pairs = [

            (1,2),
            (1,3),
            (1,4),
            (2,1),
            (2,3),
            (2,4),
            (3,1),
            (3,2),
            (3,4),
            (4,1),
            (4,2),
            (4,3),
            (1,5),(5,1),(2,5),(5,2),(3,5),(5,3),(4,5),(5,4)

        ]


        # ====================================================
        # RUN EXPERIMENTS
        # ====================================================

        for h0, h1 in pairs:

            print()
            print("=" * 100)
            print(f"H{h0} VS H{h1}")
            print("=" * 100)


            for h0_depth in DEPTHS:

                for h1_depth in DEPTHS:

                    print()

                    # ----------------------------------------
                    # Play one game
                    # ----------------------------------------

                    winner, p0_score, p1_score = play_game(
                        h0_num=h0,
                        h1_num=h1,

                        h0_depth=h0_depth,
                        h1_depth=h1_depth,

                        h0_weights=SAME_WEIGHTS,
                        h1_weights=SAME_WEIGHTS,

                        #verbose=PRINT_GAME
                    )


                    # ----------------------------------------
                    # Determine winner
                    # ----------------------------------------

                    if winner == 0:

                        winner_text = f"H{h0}"

                    elif winner == 1:

                        winner_text = f"H{h1}"

                    else:

                        winner_text = "DRAW"


                    # ----------------------------------------
                    # Update statistics
                    # ----------------------------------------

                    if winner == 0:

                        # H0 wins
                        stats[h0]["wins"] += 1

                        # H1 loses
                        stats[h1]["losses"] += 1

                    elif winner == 1:

                        # H1 wins
                        stats[h1]["wins"] += 1

                        # H0 loses
                        stats[h0]["losses"] += 1

                    else:

                        # Draw
                        stats[h0]["draws"] += 1
                        stats[h1]["draws"] += 1


                    # ----------------------------------------
                    # Print result
                    # ----------------------------------------

                    print(
                        f"H{h0} depth {h0_depth}"
                        f" vs "
                        f"H{h1} depth {h1_depth}"
                    )

                    print(
                        f"Score: H{h0} = {p0_score}, "
                        f"H{h1} = {p1_score}"
                    )

                    print(
                        f"Winner: {winner_text}"
                    )


                    # ----------------------------------------
                    # Write result to CSV
                    # ----------------------------------------

                    writer.writerow([
                        h0,
                        h1,
                        h0_depth,
                        h1_depth,
                        p0_score,
                        p1_score,
                        winner_text
                    ])


    # ========================================================
    # CREATE SUMMARY CSV
    # ========================================================

    with open(summary_file, "w", newline="") as file:

        writer = csv.writer(file)

        # Header
        writer.writerow([
            "Heuristic",
            "Wins",
            "Losses",
            "Draws",
            "Total Games",
            "Win Rate (%)"
        ])


        # ----------------------------------------------------
        # Write statistics for H1-H4
        # ----------------------------------------------------

        for h in range(1, 6):

            wins = stats[h]["wins"]
            losses = stats[h]["losses"]
            draws = stats[h]["draws"]

            total_games = wins + losses + draws

            if total_games > 0:

                win_rate = (wins / total_games) * 100

            else:

                win_rate = 0


            writer.writerow([
                f"H{h}",
                wins,
                losses,
                draws,
                total_games,
                f"{win_rate:.2f}"
            ])


    # ========================================================
    # PRINT SUMMARY
    # ========================================================

    print()
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)

    print(
        f"{'Heuristic':<12}"
        f"{'Wins':<10}"
        f"{'Losses':<10}"
        f"{'Draws':<10}"
        f"{'Games':<12}"
        f"{'Win Rate':<12}"
    )

    print("-" * 100)


    for h in range(1, 6):

        wins = stats[h]["wins"]
        losses = stats[h]["losses"]
        draws = stats[h]["draws"]

        total_games = wins + losses + draws

        if total_games > 0:
            win_rate = (wins / total_games) * 100
        else:
            win_rate = 0

        print(
            f"{'H' + str(h):<12}"
            f"{wins:<10}"
            f"{losses:<10}"
            f"{draws:<10}"
            f"{total_games:<12}"
            f"{win_rate:.2f}%"
        )


    print("=" * 100)

    print(f"Results saved to: {csv_file}")
    print(f"Summary saved to: {summary_file}")

    print("=" * 100)