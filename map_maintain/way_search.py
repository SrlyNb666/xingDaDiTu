import numpy as np
def way_search(file):
    file2='map_maintain/verts.txt'
    with open(file2, 'r',encoding='utf-8') as f:
        line_edge = f.readlines()
    n = len(line_edge)
    print(n)
    with open(file, 'r',encoding='utf-8') as f:
        lines = f.readlines()
    # 设置全0邻接矩阵
    matrix = np.zeros((n, n))
    for line in (lines):
        _ ,link ,_ ,_ ,distence = line.split(' ', 4)
        link1 = link.split(',',1)[0].strip()
        link2 = link.split(',',1)[1].strip()
        matrix[int(link1)][int(link2)] = distence
    return matrix



def dijkstra(matrix, start, end):
    n = len(matrix)
    visited = [False] * n
    distances = [np.inf] * n
    previous_nodes = [-1] * n
    distances[start] = 0

    while True:
        min_distance = np.inf
        min_node = -1
        for i in range(n):
            if not visited[i] and distances[i] < min_distance:
                min_distance = distances[i]
                min_node = i

        if min_node == -1:
            break

        visited[min_node] = True

        for i in range(n):
            if matrix[min_node][i] > 0 and distances[i] > distances[min_node] + matrix[min_node][i]:
                distances[i] = distances[min_node] + matrix[min_node][i]
                previous_nodes[i] = min_node

    path = []
    i = end
    while i != -1:
        path.append(i)
        i = previous_nodes[i]
    path.reverse()

    return path, distances[end]


def main():
    file = 'map_maintain/edges.txt'
    matrix = way_search(file)
    print(matrix.shape)
    start = 5
    end = 8
    path, distance = dijkstra(matrix, start, end)

    print(f'从 {start} 到 {end} 的最短路径是：{path}')

if __name__ == '__main__':
    main()
