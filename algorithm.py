INF = float('inf')

def run_floyd_warshall(graph):
    n = len(graph)
    dist = [row[:] for row in graph]
    next_node = [[j if graph[i][j] != INF else None for j in range(n)] for i in range(n)]
    
    k_matrices = [([row[:] for row in dist], "Initial Adjacency Matrix D⁽⁰⁾")]
    next_matrices = [[row[:] for row in next_node]]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != INF and dist[k][j] != INF:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]

        k_matrices.append(([row[:] for row in dist], f"Matrix D⁽{k+1}⁾ (via intermediate Node {k})"))
        next_matrices.append([row[:] for row in next_node])

    has_negative_cycle = any(dist[i][i] < 0 for i in range(n))
    return k_matrices, next_matrices, has_negative_cycle

def reconstruct_path(u, v, dist_matrix, next_matrix):
    if dist_matrix[u][v] == INF:
        return None, INF
    path = [u]
    curr = u
    while curr != v:
        curr = next_matrix[curr][v]
        if curr is None:
            return None, INF
        path.append(curr)
    return path, dist_matrix[u][v]
