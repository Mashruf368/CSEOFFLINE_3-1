####### board = [4,4,4,4,4,4,0     player 0     ----->
#######          4,4,4,4,4,4,0]    player 1     ----->
from Mancala import Mancala
def first_valid_move(board,player):
    if player == 0:
        pos = 5
        while(pos >= 0):
            if board[pos] != 0:
                return pos
            pos -= 1
        print("No valid move")
        return -1
    if player == 1:
        pos = 12
        while(pos >= 7):
            if board[pos] != 0:
                return pos
            pos -= 1
        print("No valid move")
        return -1
def difference_with_opponent(board,player):
    if player == 0:
        return board[6] - board[13]
    else: return board[13] - board[6]

def distance_to_winning(board,player):
    if player == 0:
        if board[6] >= 24:
            return 0
        else: return 24 - board[6]
    if player == 1:
        if board[13] >= 24:
            return 0
        else: return 24 - board[13]

def distance_to_winning_opponent(board,player):
    return distance_to_winning(board,1-player)

def total_stones_my_side(board,player):
    if player == 0:
        return sum(board[0:6])
    else: return sum(board[7:13])
def total_stones_opp_side(board,player):
    return total_stones_my_side(board,1-player)

def stones_close_my_storage(board,player):
    if player == 0:
        i = 1
        storage = 6
        total = 0
        while(storage - i >= 0):
            if board[storage - i] <= i:
                total += board[storage-i]
            i += 1
        return total
    if player == 1:
        i = 1
        storage = 13
        total = 0
        while(storage - i >= 7):
            if board[storage - i] <= i:
                total += board[storage-i]
            i += 1
        return total
def stones_close_opp_storage(board,player):
    return stones_close_my_storage(board,1-player)
def stones_my_storage(board,player):
    return board[6] if player == 0 else board[13]
def stones_opp_storage(board,player):
    return stones_my_storage(board,1-player)





def get_extra_moves(board,player):
   
    if player == 0:
        moves =  [i for i in range(0,6) if board[i] > 0]
    else:
        moves =  [i for i in range(7,13) if board[i] > 0]

    opp_store = 13 if player == 0 else 6
    for move in moves:
        pieces = board[move]
        pos = move
        for _ in range(pieces):
            pos = (pos+1)%14
            if pos == opp_store:
                pos = (pos+1)%14

        if (player == 0 and pos == 6) or (player == 1 and pos == 13):
            return 1
    return 0
def get_captures(board,player):
    if player == 0:
            moves =  [i for i in range(0,6) if board[i] > 0]
    else:
        moves =  [i for i in range(7,13) if board[i] > 0]
    
    opp_store = 13 if player == 0 else 6
    max_capture = 0
        
    for move in moves:
            temp = board[:]
            pieces = temp[move]
            temp[move] = 0
            pos = move
            for _ in range(pieces):
                pos = (pos+1)%14
                if pos == opp_store:
                    pos = (pos+1)%14
                temp[pos] += 1
            final = pos

            if player == 1 and 7<=final<=12 and temp[pos] == 1:
                opp = 12 - pos
                if temp[opp]>0:
                    max_capture = max(max_capture,temp[opp]+1)

            elif player == 0 and 0<=final<=5 and temp[pos] == 1:
                opp = 12 - pos
                if temp[opp]>0:
                    max_capture = max(max_capture,temp[opp]+1)
    return max_capture



    

############## HEURISTICS ##################### 
def heuristic1(state):
    opp_store = stones_opp_storage(1-state.root_player)
    if opp_store > 19:
        return heuristicinit(state)-15
    else:
        return heuristicinit(state)

def heuristic2(state,w1,w2):
    return w1*heuristic1(state) + w2*(total_stones_my_side(state.board,state.root_player)-total_stones_opp_side(state.board,state.root_player))

def heuristic3(state,w1,w2,w3):
    cur = state.root_player
    opp = 1- cur
    cur_extra_moves = get_extra_moves(state.board,cur)
    opp_extra_moves =   get_extra_moves(state.board,opp)
    return heuristic2(state,w1,w2) + w3*(cur_extra_moves-opp_extra_moves)

def heuristic4(state,w1,w2,w3,w4):
    cur = state.root_player
    opp = 1- cur
    cur_capture = get_captures(state.board,cur)
    opp_captures = get_captures(state.board,opp)
    return heuristic3(state,w1,w2,w3) + w4*(cur_capture - opp_captures)
def heuristicinit(state):
    return stones_my_storage(state.board,state.root_player) - stones_opp_storage(state.board,state.root_player)

# for custom heuristic
def extra_move_quality(board, player):
    if player == 0:
        moves = [i for i in range(6) if board[i] > 0]
        own_store = 6
        opp_store = 13
    else:
        moves = [i for i in range(7, 13) if board[i] > 0]
        own_store = 13
        opp_store = 6

    best_quality = 0

    for move in moves:

        pieces = board[move]
        pos = move

        for _ in range(pieces):
            pos = (pos + 1) % 14

            if pos == opp_store:
                pos = (pos + 1) % 14

        # This move gives an extra turn
        if pos == own_store:

            # Fewer stones = closer/easier move
            quality = 100 - pieces

            best_quality = max(best_quality, quality)

    return best_quality
def opponent_capture_threat(board, player):

    opp = 1 - player

    if opp == 0:
        moves = [i for i in range(6) if board[i] > 0]
        opp_store = 13
    else:
        moves = [i for i in range(7, 13) if board[i] > 0]
        opp_store = 6

    max_capture = 0

    for move in moves:

        temp = board[:]
        pieces = temp[move]
        temp[move] = 0

        pos = move

        for _ in range(pieces):

            pos = (pos + 1) % 14

            if pos == opp_store:
                pos = (pos + 1) % 14

            temp[pos] += 1

        # opponent can capture
        if opp == 0 and 0 <= pos <= 5 and temp[pos] == 1:
            opposite = 12 - pos

            if temp[opposite] > 0:
                max_capture = max(
                    max_capture,
                    temp[opposite] + 1
                )

        elif opp == 1 and 7 <= pos <= 12 and temp[pos] == 1:
            opposite = 12 - pos

            if temp[opposite] > 0:
                max_capture = max(
                    max_capture,
                    temp[opposite] + 1
                )

    return max_capture
def best_store_gain(board, player):

    if player == 0:
        moves = [i for i in range(6) if board[i] > 0]
        store = 6
        opp_store = 13
    else:
        moves = [i for i in range(7,13) if board[i] > 0]
        store = 13
        opp_store = 6

    best = 0

    for move in moves:

        pieces = board[move]
        pos = move
        gain = 0

        for _ in range(pieces):

            pos = (pos + 1) % 14

            if pos == opp_store:
                pos = (pos + 1) % 14

            if pos == store:
                gain += 1

        best = max(best, gain)

    return best
def custom_heuristic(state, w1, w2, w3, w4):

    cur = state.root_player
    opp = 1 - cur

    f1 = heuristic1(state)

    f2 = (
        total_stones_my_side(state.board, cur)
        - total_stones_opp_side(state.board, cur)
    )

    f3 = (
        get_extra_moves(state.board, cur)
        - get_extra_moves(state.board, opp)
    )
    f4 = (
        get_captures(state.board, cur)
        - get_captures(state.board, opp)
    )
    my_extra = extra_move_quality(state.board, cur)
    opp_extra = extra_move_quality(state.board, opp)

    f5 = my_extra - opp_extra

    my_threat = opponent_capture_threat(state.board, cur)
    opp_threat = opponent_capture_threat(state.board, opp)

    f6 = opp_threat - my_threat

    return (
        10 * f1 +
        2 * f2 +
        2 * f3 +
        2 * f4 +
        1 * f5 +
        1 * f6
    )


def minimax(state,depth,heuristic,alpha,beta):

    if state.is_terminal():
        return state.terminal_score(), None

    if depth == 0:
        return heuristic(state), None
    moves = state.get_valid_moves()
    if not moves:
        return state.terminal_score(), None
    best_move = None
    maximizing = (state.current_player == state.root_player)
    if maximizing:
        best_score =  float('-inf')
        for move in moves:
            child = state.copy()
            child.apply_move(move)
            

            

            score,_ = minimax(child,depth-1,heuristic,alpha,beta)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha,best_score)
            if alpha >= beta:
                break
        return best_score,best_move
    else:
        best_score = float('inf')
        for move in moves:
            child = state.copy()
            child.apply_move(move)
                        
            
            score,_ = minimax(child,depth-1,heuristic,alpha,beta)
            if score < best_score:
                best_score = score
                best_move = move

            beta = min(beta,best_score)
            if alpha >= beta:
                break
        return best_score,best_move

def get_best_move(board,player,depth,heuristic):
   state = Mancala(board, player,player)
   _,best_move = minimax(state,depth,heuristic,float("-inf"),float("inf"))
   return best_move
