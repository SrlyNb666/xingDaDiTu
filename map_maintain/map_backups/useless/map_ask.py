import requests
from PIL import Image, ImageDraw, ImageFont
def map_to_geocode_map(location,address):
        map_url = "https://restapi.amap.com/v3/staticmap"
        address = address
        parameters = {
            'key': 'a7323c5e0b28b4753e7e45a0a04e144c',
            'location': location,
            'zoom': 17,
            'size': '512*512',
            'scale': '2',
        }
        import os
        # 如果文件不存在，那么发送请求获取文件
        response = requests.get(map_url, params=parameters)
        
        with open('./map_maintain/map_png/{}.png'.format(address), 'wb') as f:
            f.write(response.content)
        # 打开图片并在中心点添加红点
        img = Image.open('./map_maintain/map_png/{}.png'.format(address))
        draw = ImageDraw.Draw(img)
        width, height = img.size
        center = (width // 2, height // 2)
        radius = 10  # 半径
        draw.ellipse((center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius), fill='red')

        # 在红点上方添加标题
        font = ImageFont.truetype('C:/Windows/Fonts/方正粗黑宋简体.ttf', 55)  # 使用Arial字体，字号为15
        text = address
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = (center[0] - text_width // 2, center[1] - radius - text_height)
        draw.text(text_position, text, fill='black', font=font)

        # 保存标注后的图片
        img.save('./map_maintain/map_png/{}.png'.format(address))
        save_path = 'F:\\project\\信大地图\\map_maintain\\map_png\\{}.png'.format(address)
        return save_path 
if __name__ == '__main__':
    location = '118.716642,32.202518'
    address = '1960街区'
    map_to_geocode_map(location,address)