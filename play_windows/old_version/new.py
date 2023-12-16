import requests
from PIL import Image, ImageDraw
import cv2
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage, QPainter
import numpy as np
from io import BytesIO
import os
import tempfile
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QLineEdit, QGridLayout, QPushButton, QWidget
from PyQt5.QtGui import QPixmap
import os
from PyQt5.QtWidgets import QGraphicsPixmapItem
sys.path.append('F:\project\信大地图')  # 添加上一级目录到Python路径
from map_maintain.api_request import Amap
from PyQt5.QtWidgets import QGraphicsItem

# 使用高德或百度地图API获取地图数据
url = 'https://restapi.amap.com/v3/staticmap'

parameters = {
            'key': 'a7323c5e0b28b4753e7e45a0a04e144c',
            'location': '118.715383,32.203407',
            'zoom': '17',
            'size': '1024*1024',
            'scale': '2',
        }
response = requests.get(url, params=parameters)

# 定义圆的中心和半径
center = (100, 100)  # 这只是一个示例值，你需要根据你的需求来设置它
radius = 50  # 这只是一个示例值，你需要根据你的需求来设置它


import os
import tempfile
from PyQt5.QtGui import QPixmapCache
# 创建一个具有特定名称的临时文件
fd, temp_file_name = tempfile.mkstemp(suffix='.png', dir=tempfile.gettempdir(), prefix='my_temp_')

# 使用os.write()函数来写入数据
os.write(fd, response.content)

# 使用os.close()函数来关闭文件描述符
os.close(fd)

# 使用cv2.imread()来读取这个临时文件
img = cv2.imread(temp_file_name)
print(temp_file_name)
import shutil
from PyQt5.QtGui import QImage, QPixmap

def qimage(img):
    # 将NumPy数组转换为QImage
    height, width, channel = img.shape
    bytesPerLine = 3 * width
    qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
    return qImg

class MapViewer(QWidget):
    def __init__(self, parent=None):
        super(MapViewer, self).__init__(parent)
        self.amap = Amap('南京', 17)  # 创建Amap类的实例
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.pixmap_items = []  # 用于存储QGraphicsPixmapItem的引用列表

        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing, True)  # 添加抗锯齿效果
        self.view.setRenderHint(QPainter.SmoothPixmapTransform, True)  # 添加平滑变换效果
       
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        factor = 1.15
        self.view.scale(factor, factor)

        self.lineEdit = QLineEdit()
        self.search_button = QPushButton("搜索")
        self.search_button.setFixedSize(100, 50)
        self.zoom_in_button = QPushButton("放大")
        self.zoom_in_button.setFixedSize(100, 50)
        self.zoom_out_button = QPushButton("缩小")
        self.zoom_out_button.setFixedSize(100, 50)

        layout = QGridLayout()
        layout.addWidget(self.view, 0, 0, 3, 3)
        layout.addWidget(self.lineEdit, 3, 0, 1, 2)
        layout.addWidget(self.search_button, 3, 2)
        layout.addWidget(self.zoom_in_button, 0, 3)
        layout.addWidget(self.zoom_out_button, 1, 3)
        self.setLayout(layout)

        self.search_button.clicked.connect(self.on_button_clicked)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)

        # 加载整个文件夹的图片到场景
        folder_path = 'F:\project\信大地图\map_maintain\map_png'
        self.load_images_to_scene(folder_path)

    def load_images_to_scene(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(folder_path, filename)
                pixmap = QPixmap(img_path)
                pixmap_item = self.scene.addPixmap(pixmap)
                # 保存 QPixmap 和对应的文件名
                self.pixmap_items.append((pixmap_item, filename))

    

    def on_button_clicked(self):
        location = self.lineEdit.text()
        print(location)
        # 文件夹的路径
        folder_path =r'F:\project\信大地图\map_maintain\map_png'
        # 获取文件夹中的所有文件
        files = os.listdir(folder_path)
        # 创建一个字典，键是去掉后缀的文件名，值是文件的路径
        name = {os.path.splitext(file)[0]: os.path.join(folder_path, file) for file in files}
        if  self.lineEdit.text() in name.keys():
            print(name[self.lineEdit.text()])
            self.scene.clear()
            pixmap = QPixmap(name[self.lineEdit.text()])
            pixmap_item = self.scene.addPixmap(pixmap)
            self.view.setScene(self.scene)
            self.view.viewport().update()
            
        else:
            # 清除 QGraphicsScene
            self.scene.clear()
            loc = self.amap.address_to_geocode(address=self.lineEdit.text())
            page = self.amap.map_to_geocode_map(loc)
            pixmap = QPixmap(page)
            if pixmap.isNull():
                print('Failed to load image:', page)
            else:
                pixmap_item = self.scene.addPixmap(pixmap)
                # 保存 QPixmap 和对应的文件名
                self.pixmap_items.append((pixmap_item, self.lineEdit.text()))
                self.view.setScene(self.scene)
                self.view.viewport().update()
    def zoom_in(self):
        self.view.scale(1.2, 1.2)

    def zoom_out(self):
        self.view.scale(1 / 1.2, 1 / 1.2)
if __name__ == "__main__":
    app = QApplication([])
    viewer = MapViewer()
    viewer.show()
    app.exec_()
    # 删除临时文件
    os.remove(temp_file_name)
