import math


class Heuristics:
    def __init__(self):
        pass

    def find_final_position(num,size):
        num -= 1
        x = num // size
        y = num % size
        return x,y

    def Hamming_Distance(a):  #takes the list and computes hamming distance
        cost =0
        size = len(a)
        b = []
        for i in range(size-1):
            b.append(i+1)
        b.append(0)

        for i in range(size):
            if(a[i]!=0):
                if(a[i]!=b[i]):
                    cost +=1

        return cost

    def Manhattan_Distance(a):
        cost = 0
        size = int (math.sqrt(len(a)))
        for i in range(len(a)):
            num = a[i]
            if(num!=0):                         ## x1 y1 position in final matrix
                num -=1                         ## x2 y2 position in current matrix
                x1 = num // size
                y1 = num % size
                x2 = i // size
                y2 = i % size
                cost += abs(x1-x2) + abs(y1-y2)
        return cost
    
    def Euclidean_Distance(a):
        cost = 0
        size = int (math.sqrt(len(a)))
        for i in range(len(a)):
            num = a[i]
            if(num!=0):                         ## x1 y1 position in final matrix
                num -=1                         ## x2 y2 position in current matrix
                x1 = num // size
                y1 = num % size
                x2 = i // size
                y2 = i % size
                cost += math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        return cost
    
    def Linear_Conflict(a):
        cost = 0
        size = int (math.sqrt(len(a)))
        #check pairs in same row
        for i in range(len(a)):
                row = i // size
                last_col = ((i // size)+1)*size     
                for j in range(i+1, last_col):
                    v1 = a[i]                #left value
                    v2 = a[j]                #right value
                    if(v1 == 0 or v2 == 0):
                        continue
                    x1,y1 = Heuristics.find_final_position(v1,size)
                    x2,y2 = Heuristics.find_final_position(v2,size)
                    if(x1 == row and x2 ==  row and y2<y1):
                        cost += 1
        #check pairs in same column
        for i in range(len(a)):
                col = i % size
                for j in range(i+size, size*size, size):
                    v1 = a[i]                #upper value
                    v2 = a[j]             #lower value
                    if(v1 == 0 or v2 == 0):
                        continue
                    x1,y1 = Heuristics.find_final_position(v1,size)
                    x2,y2 = Heuristics.find_final_position(v2,size)
                    if(y1 == col and y2 == col and x2<x1):
                        cost += 1

        return Heuristics.Manhattan_Distance(a) + 2*cost
    

    def Custom_Heuristic(a):
        size = int(math.sqrt(len(a)))

        #linear
        cost = Heuristics.Linear_Conflict(a)

        penalty=0

        # top left
        if (a[0]==1):
            if (size>1 and a[1]!=2 and a[size]!=size + 1):
                penalty +=2

        # top right
        tr= size-1
        if (a[tr] == size):
            if (a[tr-1]!=size-1 and a[tr+size]!=2*size):
                penalty +=2

        # bottom left
        bl=size*(size - 1)
        if (a[bl]==size*(size - 1) + 1):
            if (a[bl +1] != size*(size - 1) + 2 and a[bl-size]!=size*(size - 2) + 1):
                penalty +=2

        # bottom right
        br = size * size - 1
        if (a[br] == 0):
            if (a[br - 1] != size * size - 1 and a[br - size] != size * (size - 1)):
                penalty += 2

        return cost + penalty

            
        
    
            

    