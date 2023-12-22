import geopy.distance

def get_distance(point1, point2):
    coords_1 = tuple(map(float, point1.split(',')))[::-1]
    coords_2 = tuple(map(float, point2.split(',')))[::-1]
    return geopy.distance.distance(coords_1, coords_2).km

def calculate_distances(file1, file2, output_file):
    # 读取第二个文件，并将每一行的序号和经纬度数据存储在一个字典中
    points = {}
    name = {}
    with open(file2, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('  ')
            if len(parts) < 3:
                continue
            index = int(parts[0])
            jwd = parts[2].strip()
            points[index] = jwd
            name[index] = parts[1].strip()
    i = 0
    # 读取第一个文件，并使用字典中的数据来计算每一行代表的两点之间的距离
    with open(file1, 'r', encoding='utf-8') as f, open(output_file, 'w', encoding='utf-8') as f2:
        for line in f:
            parts = line.strip().split(' ')
            if len(parts) < 2:
                continue
            indexes = list(map(int, parts[1].split(',')))
            if len(indexes) < 2:
                continue
            point1 = points.get(indexes[0])
            point2 = points.get(indexes[1])
            if point1 is None or point2 is None:
                continue
            distance = get_distance(point1, point2)
            f2.write(f"{i} {indexes[0]},{indexes[1]} {name[indexes[0]]} {name[indexes[1]]} {distance}\n")
            i += 1
# 使用方法
def count_main():
    calculate_distances( 'map_maintain\map_backups\edge_link+verts.txt','map_maintain\map_backups\edge_point+verts.txt','map_maintain\map_backups\edge_end.txt')


if __name__ == '__main__':
    count_main()