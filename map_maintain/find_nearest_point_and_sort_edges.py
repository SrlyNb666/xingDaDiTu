import geopy.distance

def get_distance(point1, point2):
    coords_1 = tuple(map(float, point1.split(',')))[::-1]
    coords_2 = tuple(map(float, point2.split(',')))[::-1]
    return geopy.distance.distance(coords_2, coords_1).km

#寻找景点对应的最近的路口
def find_verts_nearest_point(points1,points2):
    result = []
    for i, point2 in enumerate(points2):
        point2_name = point2.split('  ')[1].strip()
        point2_jwd = point2.split('  ')[2].strip()
        point2_index = point2.split('  ')[0].strip()
        min_distance = float('inf')
        closest_point = None
        for point1 in points1:
            point1_name = point1.split('  ')[1].strip()
            point1_jwd = point1.split('  ')[2].strip()
            point1_index = point1.split('  ')[0].strip()
            distance = get_distance(point1_jwd, point2_jwd)
            if distance < min_distance:
                min_distance = distance
                closest_point = point1_name
                closest_point_index = point1_index
        result.append(f"{i+147} {point2_index},{closest_point_index} {point2_name} {closest_point}")
    with open('map_maintain/map_backups/output.txt', 'w', encoding='utf-8') as f:
        for line in result:
            f.write(line + '\n')
    sorts_again('map_maintain\\map_backups\\edge_link.txt', 'map_maintain/map_backups/output.txt','map_maintain\map_backups\edge_link+verts.txt')

def open_txt(path):
    with open(path, 'r',encoding='utf-8') as f:
        points = f.readlines()
    return points

def sorts_again(edge_point, edge_and_verts_point, output_file):
    lines1 = open_txt(edge_point)
    max_edge_index = int(lines1[-1].split(' ')[0].strip())
    lines2 = open_txt(edge_and_verts_point)

    # 合并文件内容
    lines = lines1 + lines2

    # 生成倒序的路径，并将它们添加到 lines 列表的末尾
    reversed_lines = []
    for line in lines:
        parts = line.strip().split(' ')
        name1 = parts[2]
        name2 = parts[3]
        # 倒序路径
        parts[1] = ','.join(reversed(parts[1].split(',')))
        
        # 倒序连接点
        parts[2] = ' '.join(reversed(name2.split(' ')))
        parts[3] = ' '.join(reversed(name1.split(' ')))
        
        reversed_line = ' '.join(parts) + '\n'
        reversed_lines.append(reversed_line)
    lines += reversed_lines

    # 更新序号
    for i, line in enumerate(lines):
        parts = line.split(' ')
        if len(parts) < 2:
            continue
        parts[0] = str(i)
        lines[i] = ' '.join(parts)

    # 写入新的文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)

def sort_main():
    with open('map_maintain\map_backups\edge_point.txt', 'r',encoding='utf-8') as f:
        points1 = f.readlines()
    with open(r'map_maintain\verts.txt', 'r',encoding='utf-8') as f:
        points2 = f.readlines()
    find_verts_nearest_point(points1,points2)

    
if __name__ == '__main__':
    with open('map_maintain\map_backups\edge_point.txt', 'r',encoding='utf-8') as f:
        points1 = f.readlines()
    with open(r'map_maintain\verts.txt', 'r',encoding='utf-8') as f:
        points2 = f.readlines()
    find_verts_nearest_point(points1,points2)
    # sorts_again('F:\\project\\信大地图\\map_maintain\\map_backups\\edge_point.txt', 'F:\project\信大地图\map_maintain\\verts.txt','F:\project\信大地图\map_maintain\map_backups\edge_point+verts.txt')
    # pass
    