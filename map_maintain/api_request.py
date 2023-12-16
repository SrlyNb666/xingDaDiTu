from PIL import Image, ImageDraw, ImageFont
import requests

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
        max_index = 0
        None_dir = True
        with open('./map_maintain/verts.txt', 'r', encoding='utf-8') as f:
                content = f.read()
        with open('./map_maintain/verts.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
        for line in lines:
            parts = line.split()
            if parts:
                index = int(parts[0])  # 取出序号并转换为整数
                if index > max_index:
                    max_index = index  # 更新最大序号
                    None_dir = False
        if None_dir:
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
            with open('./map_maintain/map_png/{}.png'.format(self.address), 'wb') as f:
                f.write(response.content)
            # 打开图片并在中心点添加红点
            img = Image.open('./map_maintain/map_png/{}.png'.format(self.address))
            draw = ImageDraw.Draw(img)
            width, height = img.size
            center = (width // 2, height // 2)
            radius = 10  # 半径
            draw.ellipse((center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius), fill='red')

            # 在红点上方添加标题
            font = ImageFont.truetype('C:/Windows/Fonts/方正粗黑宋简体.ttf', 55)  # 使用Arial字体，字号为15
            text = self.address
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_position = (center[0] - text_width // 2, center[1] - radius - text_height)
            draw.text(text_position, text, fill='black', font=font)

            # 保存标注后的图片
            img.save('./map_maintain/map_png/{}.png'.format(self.address))
            save_path = 'F:\\project\\信大地图\\map_maintain\\map_png\\{}.png'.format(self.address)
            return save_path    
        else:
            print('该记录已经存在。')
            save_path = 'F:\\project\\信大地图\\map_maintain\\map_png\\{}.png'.format(self.address)
            return save_path



        

if __name__ == '__main__':        
    key = 'a7323c5e0b28b4753e7e45a0a04e144c'
    address = '南京信息工程大学西苑食堂'
    city = '南京'
    zoom = 17
    amap = Amap( city, zoom)
    location = amap.address_to_geocode(address)
    PAGe=amap.map_to_geocode_map(location)