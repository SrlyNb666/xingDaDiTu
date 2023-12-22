import csv
import geopy.distance
def write_edges(file):
    # 从文件中读取所有的位置
    with open(file, 'r',encoding='utf-8') as f:
        lines = f.readlines()

    # 创建一个空的列表来存储所有的边
    edges = []
    index = 0
    def check_coords(coords):
        lat, lon = coords
        if abs(lat) > 90:
            # 经纬度的顺序可能是反的
            lat, lon = lon, lat
        if abs(lat) > 90 or abs(lon) > 180:
            # 经纬度的值仍然不在有效的范围内，抛出一个错误
            raise ValueError(f'Invalid coordinates: {coords}')
        return lat, lon
    # 遍历所有的位置
    for i in range(len(lines)):
        _, name_1, coords_1 = lines[i].split('  ')
        coords_1 = check_coords(tuple(map(float, coords_1.split(','))))
        for j in range(i+1, len(lines)):
            _, name_2, coords_2 = lines[j].split()
            coords_2 = check_coords(tuple(map(float, coords_2.split(','))))
            distance = geopy.distance.distance(coords_1, coords_2).km
            index += 1
            # 将结果添加到 edges 列表中
            edges.append([index,f'{i},{j}', name_1, name_2, distance])

    # 将 edges 列表写入文件
    output_file = 'map_maintain/edges.txt'
    # 将 edges 列表写入文件
    with open(output_file, 'w',encoding='utf-8', newline='') as f:
        for edge in edges:
            f.write(' '.join(map(str, edge)) + '\n')

if __name__ == '__main__':
    file = 'map_maintain/verts.txt'
    write_edges(file)