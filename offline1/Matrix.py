import math

class Matrix:
    def __init__(self,matrix,zero,g,h,parent):
        self.matrix = matrix
        self.zero = zero
        self.g = g
        self.h = h
        self.parent = parent
    def __lt__(self, other):
        return self.g+self.h < other.g+other.h

    def give_position(self):
        size = int(math.sqrt(len(self.matrix)))
        return size,self.zero // size,self.zero % size

    def move_up(self):
        size,row,col = self.give_position()
        if(row == 0):
            #print("cant move up")
            return False
        else:
            zero1 = self.zero - size
            self.matrix[zero1],self.matrix[self.zero] = (self.matrix[self.zero],self.matrix[zero1])
            self.zero = zero1
            return True
    def move_down(self):
        size,row,col = self.give_position()
        if(row == (size-1)):
            #print("cant move down")
            return False
        else:
            zero1 = self.zero + size
            self.matrix[zero1],self.matrix[self.zero] = (self.matrix[self.zero],self.matrix[zero1])
            self.zero = zero1
            return True
        
    def move_right(self):
        size,row,col = self.give_position()
        if(col == size-1):
            #print("cant move right")
            return False
        else:
            zero1 = self.zero + 1
            self.matrix[zero1],self.matrix[self.zero] = (self.matrix[self.zero],self.matrix[zero1])
            self.zero =zero1
            return True
        
    def move_left(self):
        size,row,col = self.give_position()
        if(col == 0):
            #print("cant move left")
            return False
        else:
            zero1 = self.zero - 1
            self.matrix[zero1],self.matrix[self.zero] = (self.matrix[self.zero],self.matrix[zero1])
            self.zero = zero1
            return True




