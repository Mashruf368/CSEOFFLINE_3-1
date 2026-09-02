from Graph import Graph
import random
def greedy(graph):
    max_edge = None
    max_weight = -1
    for u in range(1,graph.vertices+1):
        for v,w in graph.graph[u]:
            if u<v and w > max_weight:
                max_weight = w
                max_edge = [u,v]

    partition = [-1]*(graph.vertices+1)
    u,v = max_edge
    partition[u] = 0
    partition[v] = 1
    unassigned = [z for z in range(1,graph.vertices+1) if z != u and z != v]

    for z in unassigned:
        wt0 = 0
        wt1 = 0

        for neighbor, weight in graph.graph[z]:
            if partition[neighbor] == 1:      # neighbor already in Y
                wt1 += weight
            elif partition[neighbor] == 0:    # neighbor already in X
                wt0 += weight
        partition[z] = 0 if wt1 > wt0 else 1

    return partition, graph.cut_value(partition)

def semi_greedy(graph, alpha):
    
    max_edge = None
    max_weight = -1
    for u in range(1,graph.vertices+1):
        for v, w in graph.graph[u]:
            if u < v and w > max_weight:
                max_weight = w
                max_edge = [u, v]

    partition = [-1] * (graph.vertices+1)
    u,v = max_edge
    partition[u]=0
    partition[v]=1

    candidates = set(range(1,graph.vertices+1))

    candidates.remove(u)
    candidates.remove(v)
    while candidates:
        sigmaX = {}  
        sigmaY = {} 
        greedy_val = {}

        for z in candidates:
            sx = 0
            sy = 0
            for neighbor,weight in graph.graph[z]:
                if partition[neighbor] == 0:      
                    sx += weight
                elif partition[neighbor] ==  1:
                    sy += weight
            sigmaX[z] = sx
            sigmaY[z] = sy
            greedy_val[z]=max(sx,sy)

        wmin = min(min(sigmaX.values()),min(sigmaY.values()))

        wmax = max(max(sigmaX.values()),max(sigmaY.values()))
        mu = wmin + alpha*(wmax - wmin)

        rcl = [z for z in candidates if greedy_val[z] >= mu]

        chosen = random.choice(rcl)

        
        if sigmaX[chosen] > sigmaY[chosen]:
            partition[chosen] = 1
        else:
            partition[chosen] = 0

        candidates.remove(chosen)

    return partition, graph.cut_value(partition)

def compute_delta(graph, partition, v):
    same = 0
    other = 0
    for neighbor, weight in graph.graph[v]:
        if partition[neighbor] == partition[v]:
            same += weight
        else:
            other += weight
    return same - other


def local_search(graph, partition):
    partition = partition[:]
    improved = True
    iterations = 0

    while improved:
        improved = False
        best_delta = 0
        best_vertex = None

        for v in range(1,graph.vertices+1):
            delta = compute_delta(graph, partition, v)
            if delta > best_delta:
                best_delta = delta
                best_vertex = v

        if best_vertex is not None:
            partition[best_vertex] = 1-partition[best_vertex]
            improved = True
            iterations+=1

    return partition, graph.cut_value(partition),iterations


def grasp(graph,max_iterations,alpha):
    best_partition = None
    best_value = -1

    for i in range(max_iterations):
        constructed_partition, _ = semi_greedy(graph, alpha)

        improved_partition, improved_value,local_iterations = local_search(graph, constructed_partition)

        if improved_value > best_value:
            best_value = improved_value
            best_partition = improved_partition

    return best_partition, best_value,max_iterations


