import random

from matplotlib import lines

class Graph:
    def __init__(self,u):
        self.vertices = u
        self.graph = [[] for _ in range(u+1)]


    def build_graph(self,g):
        self.edges=len(g)
        for u,v,w in g:
            self.graph[u].append([v,w])
            self.graph[v].append([u,w])
            
    def cut_value(self,partition):
        ans = 0
        for u in range(1,self.vertices+1):
            for v,w in self.graph[u]:
                if(u<v and partition[u]!= partition[v]):
                    ans += w
        return ans
    
    def random_partition(self):
        return [-1] + [random.randint(0, 1) for _ in range(self.vertices)]

    def get_random_cut(self):
        return self.cut_value(self.random_partition())
    def randomized(self,iterations):
        total = 0

        for _ in range(iterations):
            total += self.get_random_cut()

        return total / iterations

    @staticmethod
    def load_graph(filename):
        with open(filename) as file:
            lines = file.readlines()
        n,m = map(int, lines[0].split())
        
        edges = []
        for line in lines[1:m+1]:
                

                u,v,w = map(int, line.split())
                edges.append((u,v,w))
        g = Graph(n)
        g.build_graph(edges)
        return g






if __name__ == "__main__":
    g = Graph.load_graph("g1.rud")
    print("Vertices:", g.vertices)
    print("Sample randomized average:", g.randomized(50))
    

