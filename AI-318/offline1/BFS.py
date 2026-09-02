import heapq
import math
from Matrix import Matrix
from Heuristics import Heuristics

class BFS:
    def __init__(self, initial_state, heuristic):
        self.initial_state = initial_state
        self.heuristic = heuristic
        self.visited = set()
        self.queue = []
        self.path = []
    def print_board(self,board):
        size = int(math.sqrt(len(board)))
        for i in range(size):
            print(*board[i*size:(i+1)*size])
        print()

    

    def solve(self,w):
        print(f"\nWeight = {w}")
        a = self.initial_state
        size  = int(math.sqrt(len(a.matrix)))
        self.goal_state = list(range(1,size*size))
        self.goal_state.append(0)
        pq = []
        expanded = 0

        a.h = self.heuristic(a.matrix)
        heapq.heappush(pq,(a.g + w*a.h,a))

        while pq:

            a = heapq.heappop(pq)[1]
            if tuple(a.matrix) in self.visited:
                continue
            self.visited.add(tuple(a.matrix))

            expanded += 1

            if a.matrix == self.goal_state:

                goal_cost = a.g

                print("Minimum number of moves =", goal_cost)
                print("Goal state reached!")
                print("Path to goal state:")

                self.path = []
                current = a

                while current is not None:
                    self.path.append(current)
                    current = current.parent

                self.path.reverse()

                for state in self.path:
                    self.print_board(state.matrix)

                return goal_cost, expanded

            left= Matrix(a.matrix.copy(),a.zero,a.g+1,a.h,a)
            right = Matrix(a.matrix.copy(),a.zero,a.g+1,a.h,a)
            up = Matrix(a.matrix.copy(),a.zero,a.g+1,a.h,a)
            down =  Matrix(a.matrix.copy(),a.zero,a.g+1,a.h,a)
            left0 = left.move_left()
            if left0 and tuple(left.matrix) not in self.visited:
                left.h = self.heuristic(left.matrix)
                heapq.heappush(pq,(left.g + w*left.h,left))

            right0 = right.move_right()
            if right0 and tuple(right.matrix) not in self.visited:
                right.h = self.heuristic(right.matrix)
                heapq.heappush(pq,(right.g + w*right.h,right))
            up0 = up.move_up()
            if up0 and tuple(up.matrix) not in self.visited:
                up.h = self.heuristic(up.matrix)
                heapq.heappush(pq,(up.g + w*up.h,up))
            down0 = down.move_down()
            if down0 and tuple(down.matrix) not in self.visited:
                down.h = self.heuristic(down.matrix)
                heapq.heappush(pq,(down.g + w*down.h,down))


        return a.g, expanded

            

        