class Mancala:
    def __init__(self,board,player,root_player):
        self.board = board[:]
        self.current_player = player                    
        self.root_player = root_player
        
        

####### board = [4,4,4,4,4,4,0     player 0     ----->
#######          4,4,4,4,4,4,0]    player 1     ----->

    def copy(self):
        return Mancala(self.board,
                       self.current_player,
                       self.root_player)

    def get_valid_moves(self):
        if self.current_player == 0:
            return [i for i in range(0,6) if self.board[i] > 0]
        else:
            return [i for i in range(7,13) if self.board[i] > 0]
    def is_terminal(self):
        return sum(self.board[0:6]) == 0 or sum(self.board[7:13]) == 0
    
    def terminal_score(self):
        p0 = self.board[6] + sum(self.board[0:6])
        p1 = self.board[13] + sum(self.board[7:13])

        if self.root_player == 0:
            return p0-p1
        else:
            return p1-p0
    
    def apply_move(self,move):

        if self.current_player == 0 and not (0<=move <= 5):
            return False
        if self.current_player == 1 and not (7<=move <= 12):
            return False
        if self.board[move] == 0:
            return False
        


        pieces = self.board[move]
        self.board[move] = 0
        pos = move
        own_store = 6 if self.current_player == 0 else 13
        opp_store = 13 if self.current_player == 0 else 6
        own_side_start = 0 if self.current_player==0 else 7
        own_side_end = 5 if self.current_player == 0 else 12
        for _ in range(pieces):
            pos = (pos+1)%14
            if pos == opp_store:
                pos = (pos+1)%14
            self.board[pos] += 1
        final = pos
        captured = 0
        

        if own_side_start <= final <= own_side_end and self.board[final] == 1:      #ends on own side and final square has 1 stone 
            opposite = 12-final
            opposite_stones = self.board[opposite]

            if opposite_stones > 0:
                captured = 1 + opposite_stones
                self.board[own_store] += captured
                self.board[opposite] = 0
                self.board[final] = 0

        if final != own_store:
            self.current_player = 1 - self.current_player
        return True
                

    
        