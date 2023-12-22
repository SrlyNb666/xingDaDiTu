import numpy as np
file2='map_maintain\map_backups\edge_point+verts.txt'
# with open(file2, 'r',encoding='utf-8') as f:
#         line_edge = f.readlines()
file = 'map_maintain\map_backups\edge_end.txt'
def way_search(file):
    with open(file2, 'r',encoding='utf-8') as f:
        line_edge = f.readlines()
    n = len(line_edge)
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
    with open(file2, 'r',encoding='utf-8') as f:
        line_edge2 = f.readlines()
    for line in line_edge2:
        row = line.strip().split('  ')
        if row[1] == location:
            
            return row[0]
    
def dijkstra(start_txt, end_txt):
    with open(file2, 'r',encoding='utf-8') as f:
        line_edge = f.readlines()
    start = int(find_index(start_txt))
    end = int(find_index(end_txt))
    
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
        #print(min_node)
        for i in range(n):
            if matrix[min_node][i] > 0 and distances[i] > distances[min_node] + matrix[min_node][i]:
                distances[i] = distances[min_node] + matrix[min_node][i]
                previous_nodes[i] = min_node

    path = []
    path_jw = []
    i = end
    while i != -1:
        _ ,spot ,jw = line_edge[i].strip().split('  ', 2)
        path.append(str(spot))
        i = previous_nodes[i]
        jw_1 = jw.split(',')[0].strip()
        jw_2 = jw.split(',')[1].strip()
        path_jw.append(str(f'{jw_1},{jw_2}'))
    
    path.reverse()
    if distances[end]!= np.inf:
        path_all = f'从 {start_txt} 到 {end_txt} 的最短路径是：{path}'
        distances = f'距离是：{distances[1]} km'
        return path_all, distances, path, distances[1],path_jw,line_edge
    else:
        return None, None, path, distances[1],path_jw,line_edge

#哈希表法
def way_search_hash(file):
    with open(file2, 'r',encoding='utf-8') as f:
        line_edge = f.readlines()
    n = len(line_edge)
    with open(file, 'r',encoding='utf-8') as f:
        lines = f.readlines()
    graph = dict()
    for line in lines:
        _ ,link ,_ ,_ ,distance = line.split(' ', 4)
        link1 = int(link.split(',',1)[0].strip())
        link2 = int(link.split(',',1)[1].strip())
        distance = float(distance)
        # 如果 link1 不在图中，添加它
        if link1 not in graph:
            graph[link1] = []
        # 添加一条从 link1 到 link2 的边
        graph[link1].append((link2, distance))
    return graph
#哈希表法的dijkstra
def dijkstra_hash(start_txt, end_txt):
    with open(file2, 'r',encoding='utf-8') as f:
        line_edge = f.readlines()
    start = int(find_index(start_txt))
    end = int(find_index(end_txt))
    graph = way_search_hash(file)
    max_node = max(max(pair[0] for pair in graph[node]) for node in graph)
    n = max_node + 1
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
        if min_node not in graph:  # 如果 min_node 不在 graph 的键中，跳过当前的迭代
            continue
        for neighbor, weight in graph[min_node]:  # 遍历 min_node 的所有邻接节点
            if distances[neighbor] > distances[min_node] + weight:
                distances[neighbor] = distances[min_node] + weight
                previous_nodes[neighbor] = min_node
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
    distances = f'距离是：{distances[1]} km'
    if distances[0]!= np.inf:
        return path_all, distances, path, distances[1],path_jw,line_edge
    else:
        return None, None, path, distances[1],path_jw,line_edge




#全部节点

def node_index_to_name(node_index):
    with open(file2, 'r',encoding='utf-8') as f:
        line_edge = f.readlines()
    _, spot, jw = line_edge[node_index].split('  ', 2)
    return str(spot)
# def find_all_paths_BFS(start, end, max_nodes, max_paths):
#     start = int(find_index(start))
#     end = int(find_index(end))
#     queue = [(start, [start])]
#     graph = way_search_hash(file)
#     found_paths = 0
#     # 创建一个空列表来存储路径的字符串描述
#     path_descriptions = []
#     while queue and found_paths < max_paths:
#         (node, path) = queue.pop(0)
#         for neighbor in graph[node]:
#             if neighbor[0] not in path:
#                 new_path = path + [neighbor[0]]
#                 if neighbor[0] == end and len(new_path) <= max_nodes:
#                     # 将节点序号转换为名称
#                     path_names = [node_index_to_name(node_index) for node_index in new_path]
#                     # 创建路径的字符串描述
#                     path_description = f"路径：{' -> '.join(path_names)}"
#                     # 将路径的字符串描述添加到列表中
#                     path_descriptions.append(path_description)
#                     found_paths += 1
#                     if found_paths == max_paths:
#                         return path_descriptions  # 返回一个空列表，表示找到足够数量的路径
#                 # 将下一层的节点添加到队列
#                 queue.append((neighbor[0], new_path))
#     # 执行到这里，搜索结束但未找到足够数量的路径
#     print("未找到足够数量的路径")
#     return path_descriptions
#以下是新增 包括对文件的解析、路径的合并计算、修改后的find_all_path
def parse_distance_file(file_path):
    distance_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split()
            # 假设每行格式为: index start_node,end_node edge_id1 edge_id2 distance
            nodes = parts[1].split(',')
            key = tuple(sorted([int(nodes[0]), int(nodes[1])]))  # 创建一个节点对作为键
            distance = float(parts[4])
            distance_dict[key] = distance
    return distance_dict

edge_distances = parse_distance_file('map_maintain\\map_backups\\edge_end.txt')


def calculate_total_distance(path, edge_distances):
    total_distance = 0
    for i in range(len(path) - 1):
        node_pair = tuple(sorted([path[i], path[i + 1]]))
        total_distance += edge_distances.get(node_pair, 0)  # 如果找不到距离，默认为 0
    return total_distance


def find_all_paths_BFS(start_txt, end_txt, max_nodes, max_paths=5):
    # 将位置转换为索引
    start = int(find_index(start_txt))
    end = int(find_index(end_txt))
    queue = [(start, [start])]
    graph = way_search_hash(file)
    found_paths = 0
    paths = []
    # 创建一个空列表来存储路径的字符串描述
    while queue and found_paths < max_paths:
        (current_node, path) = queue.pop(0)
        for neighbor, _ in graph[current_node]:
            if neighbor not in path:
                new_path = path + [neighbor]
                if neighbor == end and len(new_path) <= max_nodes:
                    # 如果达到目标节点，记录路径
                    paths.append(new_path)
                    found_paths += 1
                elif len(new_path) < max_nodes:
                    # 如果没有到达目标节点且路径长度小于最大节点数，将其加入队列
                    queue.append((neighbor, new_path))

    # 检查找到的路径数量是否满足要求
    if not paths:
        return "未找到路径或节点数过少"
    
    # 将路径按长度排序，获取最短的路径
    paths.sort(key=len)
    shortest_paths = paths[:max_paths]

    # 转换路径索引为名称，并创建描述字符串
    path_descriptions = []
    for path in shortest_paths:
        total_distance = calculate_total_distance(path, edge_distances)
        path_names = [node_index_to_name(node_index) for node_index in path]
        path_description = f"路径：{' -> '.join(path_names)}，距离：{total_distance}千米"
        path_descriptions.append(path_description)

    return path_descriptions


#测试效果的，不在程序中使用，主程序使用的是其他函数
def main():
    start = '南京信息工程大学明德楼'
    end = '南京信息工程大学揽江楼'
    path_print, distances_print,path,distances,path_jw,line_edge = dijkstra(start, end)
    print(path_print)
    print(distances_print)
    print(path_jw)
    # path_hash, distances_hash,path,distances,path_jw_hash,line_edge = dijkstra_hash(start, end)
    # print(path_hash)
    # print(distances_hash)
    # print(path_jw_hash)

    all_paths = find_all_paths_BFS(start, end,10000, 5)
    print("所有路径：")
    print(all_paths)
    # if all_paths:
    #     for path, coordinates in all_paths:
    #         print(f"路径：{path}")
    #         print(f"地理坐标：{coordinates}")
    #         print("\n")
    # else:
    #     pass



    # if all_paths:
        
    #     for path, coordinates in (item[:2] for item in all_paths):
    # # 处理 path, coordinates
    #         print(f"路径：{path}")
    #         print(f"地理坐标：{coordinates}")
    #         print("\n")
    # else:
    #     pass


if __name__ == '__main__':
    main()
