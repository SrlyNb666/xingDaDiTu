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


# class MapViewer(QWidget):
#     def __init__(self, parent=None):
#         super(MapViewer, self).__init__(parent)
#         self.amap = Amap('南京',17)  # 创建Amap类的实例
#         self.view = QGraphicsView()
#         self.scene = QGraphicsScene()
#         self.pixmap_item = None  # 用于存储QGraphicsPixmapItem的引用
        
#         qImg=qimage(img)
#         pixmap = QPixmap.fromImage(qImg)
#         self.scene.addPixmap(pixmap)
#         self.view.setScene(self.scene)
#         self.view.setDragMode(QGraphicsView.ScrollHandDrag)
#         factor = 1.15
#         self.view.scale(factor, factor)
#         self.lineEdit = QLineEdit()
#         self.search_button = QPushButton("搜索")
#         self.search_button.setFixedSize(100, 50)
#         self.zoom_in_button = QPushButton("放大")
#         self.zoom_in_button.setFixedSize(100, 50)
#         self.zoom_out_button = QPushButton("缩小")
#         self.zoom_out_button.setFixedSize(100, 50)
#         layout = QGridLayout()
#         layout.addWidget(self.view, 0, 0, 3, 3)
#         layout.addWidget(self.lineEdit, 3, 0, 1, 2)
#         layout.addWidget(self.search_button, 3, 2)
#         layout.addWidget(self.zoom_in_button, 0, 3)
#         layout.addWidget(self.zoom_out_button, 1, 3)
#         self.setLayout(layout)
#         self.search_button.clicked.connect(self.on_button_clicked)
#         self.zoom_in_button.clicked.connect(self.zoom_in)
#         self.zoom_out_button.clicked.connect(self.zoom_out)
        
#     def on_button_clicked(self):
#         QPixmapCache.clear()
#         location = self.lineEdit.text()
#         print (location)
#         filename = 'F:/project/信大地图/map_maintain/map_png/map_'+location+'.png'
#         filename_temp ='F:/project/信大地图/map_maintain/map_png/tem.png'
#         if os.path.exists(filename):
#             print('找到了同名的png文件。')
#             print(filename)
#             shutil.copyfile(filename, filename_temp)
#             shutil.copyfile(filename_temp,filename)
#             pixmap2 = QPixmap(filename)
#             # 检查场景中是否已经存在这个图像
#             # for item in self.scene.items():
#             #     if isinstance(item, QGraphicsPixmapItem) and item.pixmap().cacheKey() == pixmap.cacheKey():
#             #         # 如果存在，将这个图像移动到最上层
#             #         item.setZValue(1)
#             #         self.view.update()
#             #         QApplication.processEvents()
#             #         break
#             # 如果不存在，添加新的图像到场景
#             self.scene.addPixmap(pixmap2)
            
    #     else:
    #         loc = self.amap.address_to_geocode(address=location)#坐标
    #         page=self.amap.map_to_geocode_map(loc)
    #         pixmap = QPixmap(page)
    #         self.scene.addPixmap(pixmap)
    #         self.view.update()

            
    # def zoom_in(self):
    #     self.view.scale(1.2, 1.2)
    # def zoom_out(self):
    #     self.view.scale(1 / 1.2, 1 / 1.2)
class MapViewer(QWidget):
    def __init__(self, parent=None):
        super(MapViewer, self).__init__(parent)
        self.amap = Amap('南京', 17)  # 创建Amap类的实例
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.pixmap_item = None  # 用于存储QGraphicsPixmapItem的引用

        qImg = qimage(img)
        pixmap = QPixmap.fromImage(qImg)
        self.pixmap_item = self.scene.addPixmap(pixmap)  # 保存引用

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

    def on_button_clicked(self):
        location = self.lineEdit.text()
        print(location)
        filename = 'F:/project/信大地图/map_maintain/map_png/map_'+location+'.png'
        filename_temp ='F:/project/信大地图/map_maintain/map_png/tem.png'

        if os.path.exists(filename):
            print('找到了同名的png文件。')
            print(filename)
            shutil.copyfile(filename, filename_temp)
            shutil.copyfile(filename_temp, filename)
            pixmap2 = QPixmap(filename)
            self.pixmap_item.setPixmap(pixmap2.copy()) # 更新已有的Pixmap内容
            self.scene.clear()  # 清空场景  
            print(filename)
            shutil.copyfile(filename, filename_temp)
            shutil.copyfile(filename_temp, filename)
            pixmap2 = QPixmap(filename)
            self.pixmap_item.setPixmap(pixmap2.copy()) # 更新已有的Pixmap内容
        else:
            loc = self.amap.address_to_geocode(address=location)
            page = self.amap.map_to_geocode_map(loc)
            pixmap2 = QPixmap(page)
            self.scene.clear()  # 清空场景
            self.pixmap_item = self.scene.addPixmap(pixmap2.copy())  # 添加新的Pixmap
            self.view.setScene(self.scene)
            self.view.update()

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



