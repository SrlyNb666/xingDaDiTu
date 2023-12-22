from PIL import Image, ImageDraw, ImageFont
import requests
import io
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from map_maintain.find_nearest_point_and_sort_edges import sort_main,get_distance
from map_maintain.per_edge_distance_count import count_main
from geopy.distance import geodesic
class Amap:
    def __init__(self, city,  zoom):
        self.city = city
        self.key = 'a7323c5e0b28b4753e7e45a0a04e144c'
        self.location_url = "https://restapi.amap.com/v3/geocode/geo"
        self.map_url = "https://restapi.amap.com/v3/staticmap"
        self.zoom = zoom
    def address_to_geocode(self,address):
        self.address = address
        parameters = {
            'key': self.key,
            'address': self.address,
            'city': self.city
        }
        max_index = 110#因为有110个路口点，所以从110开始
        None_dir = True
        with open('./map_maintain/verts.txt', 'r', encoding='utf-8') as f:
                content = f.read()
        with open('./map_maintain/verts.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
        for line in lines:
            parts = line.strip().split('  ')
            if parts:
                index = int(parts[0])  # 取出序号并转换为整数
                if index > max_index:
                    max_index = index  # 更新最大序号
                    None_dir = False
        if None_dir ==False:
            max_index += 1
        # 检查记录是否已经在文件中
        if self.address not in content:
            # 如果address不在文件中，就进行请求并写入
            response = requests.get(self.location_url, params=parameters)
            data = response.json()
            if data['status'] == '1' and data['count'] != '0':
                record = "{}  {}  {}\n".format(max_index,self.address, str(data['geocodes'][0]['location']))
                with open('./map_maintain/verts.txt', 'a', encoding='utf-8') as f:
                    f.write(record)
                with open('map_maintain/map_backups/edge_point+verts.txt', 'a', encoding='utf-8') as f2:
                    f2.write(record)
                sort_main()
                count_main()

                return data['geocodes'][0]['location']



            else:
                return '未找到该地点。'
        else:
            lction = None  # 给lction赋一个默认值
            for i, line in enumerate(lines):
                _, address_2, _ = line.split('  ', 2)
                if self.address == address_2:
                    lction = line.split('  ', 2)[2].strip()
                    break
            print('该记录已经存在。')   
            return lction
             
    def map_to_geocode_map(self, location):
        parameters = {
            'key': self.key,
            'location': location,
            'zoom': self.zoom,
            'size': '512*512',
            'scale': '2',
        }
        import os

        # 获取文件夹中的所有文件
        files = os.listdir('./map_maintain/map_png')

        # 构造你想要的文件名
        filename = '{}.png'.format(self.address)

        # 检查文件是否存在
        if filename not in files:
            
            # 如果文件不存在，那么发送请求获取文件
            response = requests.get(self.map_url, params=parameters)
            try:
                Image.open(io.BytesIO(response.content))
            except IOError:
                return 0
            with open('./map_maintain/map_png/{}.png'.format(self.address), 'wb') as f:
                f.write(response.content)
            # 打开图片并在中心点添加红点
            img = Image.open('./map_maintain/map_png/{}.png'.format(self.address))
            draw = ImageDraw.Draw(img)
            width, height = img.size
            center = (width // 2, height // 2)
            radius = 10  # 半径
            draw.ellipse((center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius), fill='red')

            # 在红点上方添加标题，使用Arial字体，字号为55
            font = ImageFont.truetype('字体/方正粗黑宋简体.TTF', 55)  
            text = self.address
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_position = (center[0] - text_width // 2, center[1] - radius - text_height)
            draw.text(text_position, text, fill='black', font=font)

            # 保存标注后的图片
            img.save('./map_maintain/map_png/{}.png'.format(self.address))
            save_path = 'map_maintain\\map_png\\{}.png'.format(self.address)
            return save_path    
        else:
            print('该记录已经存在。')
            save_path = 'map_maintain\\map_png\\{}.png'.format(self.address)
            return save_path

    def path_lable(self, path_jw, line_edge):
        location_dict = {}
        verts_dict = dict()
        for line in line_edge:
            id, address_3, jw3 = line.strip().split('  ', 2)
            location_dict[jw3] = address_3
            if int(id)>=110:
                verts_dict[jw3] = address_3
        # 在每个坐标前添加路径信息
        path_jw_str = "5,0x0000ff,1,,:{}".format(";".join(x for x in path_jw))

        # 创建 markers 参数
        start_location = path_jw[-1]
        end_location = path_jw[0]
        markers_str_list = ["mid,0xFFFF00,起:{}".format(start_location), "mid,0xFFFF00,终:{}".format(end_location)]
        # markers_str = "|".join(markers_str_list)
        
        # 创建 labels 参数
        labels_str_list = []
        for location in path_jw:
            if location in location_dict:
                location_name = location_dict[location]
                #如果name不是e开头，就添加name
                if location_name[0] != 'e':
                    labels_str_list.append("{},1,0,5,0x000000,0xffffff:{}".format(location_name[2:],location))
        
        
        # 计算每个景点应该间隔的节点数量
        interval = len(path_jw) // 8
        # 初始化一个计数器
        counter = 0
        for location in verts_dict.keys():
            for i in range(len(path_jw)):
                # 只在间隔的节点上检查是否有景点
                if i % interval == 0:
                    distance = get_distance(location, path_jw[i])
                    if distance <= 0.1:
                        markers_str_list.append("mid,0xFFFF00,{}:{}".format(verts_dict[location][-3], location))
                        labels_str_list.append("{},1,0,8,0x000000,0xffffff:{}".format(verts_dict[location][2:],location))
                        counter += 1
                        break
            # 如果已经找到了8个景点，就结束循环
            if counter >= 8:
                break
        markers_str = "|".join(markers_str_list)
        labels_str = "|".join(labels_str_list)

        parameters = {
            'key': self.key,
            'paths': path_jw_str,
            'markers': markers_str,
            'labels': labels_str,
            'size': '512*512',
            'scale': '2',
        }
        response = requests.get(self.map_url, params=parameters)
        try:
            Image.open(io.BytesIO(response.content))
        except IOError:
            print(response.content)
            return 0
        save_path = 'map_maintain\\导航\\path.png'
        with open(save_path, 'wb') as f:
                f.write(response.content)
        return save_path

        

if __name__ == '__main__':        
    key = 'a7323c5e0b28b4753e7e45a0a04e144c'
    address = '南京信息工程大学西苑食堂'
    city = '南京'
    zoom = 17
    amap = Amap( city, zoom)
    lable = ['118.717007,32.204857', '118.718599,32.204579', '118.724767,32.205998']

    file2='map_maintain/verts.txt'
    with open(file2, 'r',encoding='utf-8') as f:
            line_edge = f.readlines()
    path = amap.path_lable(lable, line_edge)
    location = amap.address_to_geocode(address)
    location ='118.71235,32.20732'
    PAGe=amap.map_to_geocode_map(location)