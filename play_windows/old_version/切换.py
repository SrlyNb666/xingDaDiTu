import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

import os
from PyQt5.QtGui import QPixmap

image_folder = "F:\project\信大地图\map_maintain\map_png"  # 替换为你的图片文件夹路径
image_files = os.listdir(image_folder)

class ImageSwitcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(500, 400)  # 设置窗口最小尺寸为500x400
        self.setMaximumSize(800, 700)  # 设置窗口最大尺寸为500x400
        self.images = [QPixmap(os.path.join(image_folder, image_file)) for image_file in image_files if image_file.endswith(('.png', '.jpg', '.jpeg'))]
        self.current_index = 0
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(self.images[self.current_index])
        self.button = QPushButton("Switch Image")
        self.button.clicked.connect(self.switch_image)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)
    def switch_image(self):
        self.current_index = (self.current_index + 1) % len(self.images)
        self.label.setPixmap(self.images[self.current_index])
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageSwitcher()
    window.show()
    sys.exit(app.exec_())
