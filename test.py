def find_index(location):
    with open('verts.txt', 'r', encoding='utf-8') as file:
        for line in file:
            row = line.split('  ')
            if row[1] == location:
                return row[0]
    return None

index = find_index('南京信息工程大学体育馆')
print(index)