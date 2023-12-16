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
from PyQt5.QtWidgets import QGraphicsItem,QLabel
import shutil
from PyQt5.QtGui import QImage, QPixmap

image_folder = "F:\project\信大地图\map_maintain\map_png"  # 替换为你的图片文件夹路径
image_files = os.listdir(image_folder)
index = 0
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QLabel

class DraggableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.dragging = False
        self.offset = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
from PyQt5.QtWidgets import QScrollArea
class MapViewer(QWidget):
    def __init__(self,):
        super().__init__()
        self.setMinimumSize(1000, 500)  # 设置窗口最小尺寸为500x400
        self.setMaximumSize(1000, 700)  # 设置窗口最大尺寸为500x400
        self.amap = Amap('南京', 17)  # 创建Amap类的实例
        self.images = [QPixmap(os.path.join(image_folder, image_file)) for image_file in image_files if image_file.endswith(('.png', '.jpg', '.jpeg'))]
        print(self.images)
        self.label = DraggableLabel()
        self.label.setAlignment(Qt.AlignCenter)
        #self.label.setScaledContents (True)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.label)
        self.lineEdit = QLineEdit()
        self.search_button = QPushButton("搜索")
        self.search_button.clicked.connect(self.on_button_clicked)
        self.search_button.setFixedSize(100, 50)
        self.zoom_in_button = QPushButton("放大")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        
        self.zoom_in_button.setFixedSize(100, 50)
        self.zoom_out_button = QPushButton("缩小")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_out_button.setFixedSize(100, 50)


        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0, 3, 3)
        layout.addWidget(self.lineEdit, 3, 0, 1, 2)
        layout.addWidget(self.search_button, 3, 2)
        layout.addWidget(self.zoom_in_button, 0, 3)
        layout.addWidget(self.zoom_out_button, 1, 3)
        self.setLayout(layout)
   

    def on_button_clicked(self):
        

        # 文件夹的路径
        folder_path =r'F:\project\信大地图\map_maintain\map_png'
        # 获取文件夹中的所有文件
        files = os.listdir(folder_path)
        # 创建一个字典，键是去掉后缀的文件名，值是文件的路径
        name = {os.path.splitext(file)[0]: os.path.join(folder_path, file) for file in files}
        location = 'F:\project\信大地图\map_maintain\map_png\map_' + str(self.lineEdit.text()) + '.png'
        if  self.lineEdit.text() in name.keys():
            print(name[self.lineEdit.text()])
            self.label.setPixmap(QPixmap(name[self.lineEdit.text()]))
        else:
            print('没有该地点')
            loc = self.amap.address_to_geocode(address=self.lineEdit.text())
            self.amap.map_to_geocode_map(loc)     
            # 获取文件夹中的所有文件
            files = os.listdir(folder_path)
            # 创建一个字典，键是去掉后缀的文件名，值是文件的路径
            name = {os.path.splitext(file)[0]: os.path.join(folder_path, file) for file in files}
            self.label.setPixmap(QPixmap(name[self.lineEdit.text()]))
         

    def changeImg(self,index):
        self.current_index=index 
        print(self.current_index)
        self.label.setPixmap(self.images[self.current_index])
       
    def zoom_in(self):
        # 获取标签中的 QPixmap 对象
        pixmap = self.label.pixmap()
        # 放大 QPixmap 对象
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 1.2), int(pixmap.height() * 1.2), Qt.KeepAspectRatio)
        # 将放大的 QPixmap 对象设置为标签的图片
        self.label.setPixmap(scaled_pixmap)

    def zoom_out(self):
        # 获取标签中的 QPixmap 对象
        pixmap = self.label.pixmap()
        # 缩小 QPixmap 对象
        scaled_pixmap = pixmap.scaled(int(pixmap.width() / 1.2), int(pixmap.height() / 1.2), Qt.KeepAspectRatio)
        # 将缩小的 QPixmap 对象设置为标签的图片
        self.label.setPixmap(scaled_pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MapViewer()
    viewer.show()
    sys.exit(app.exec_())


