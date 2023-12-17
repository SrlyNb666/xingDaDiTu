import numpy as np
file2='map_maintain/verts.txt'
with open(file2, 'r',encoding='utf-8') as f:
        line_edge = f.readlines()


def way_search(file):
    
    
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


def find_index(location):

    for line in line_edge:
        row = line.split('  ')
        if row[1] == location:
            return row[0]
    


def dijkstra(start_txt, end_txt):
    start = int(find_index(start_txt))
    end = int(find_index(end_txt))
    file = 'map_maintain/edges.txt'
    matrix= way_search(file)
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
    path_jw = []
    i = end
    while i != -1:
        _ ,spot ,jw = line_edge[i].split('  ', 2)

        

        path.append(str(spot))
        i = previous_nodes[i]
        jw_1 = jw.split(',')[0].strip()
        jw_2 = jw.split(',')[1].strip()
        path_jw.append(str(f'{jw_1},{jw_2}'))
    
    path.reverse()
    
    path_all = f'从 {start_txt} 到 {end_txt} 的最短路径是：{path}'
    distances = f'距离是：{distances[end]} km'
    print(distances[end])
    if distances[end]!= 'i':
        return path_all, distances, path, distances[end],path_jw,line_edge
    else:
        return None, None, path, distances[end],path_jw,line_edge




def main():
    
    
    start = '南京信息工程大学文德楼'
    end = '南京信息工程大学明德楼'
    path_print, distances_print,path,distances,path_jw = dijkstra(start, end)
    print(path_print)
    print(distances_print)
    print(path_jw)
if __name__ == '__main__':
    main()
