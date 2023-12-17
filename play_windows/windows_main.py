from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QLineEdit, QGridLayout, QPushButton, QWidget, QTextEdit
from PyQt5.QtGui import QPixmap,QTransform,QFont
import os
from PyQt5.QtWidgets import QGraphicsPixmapItem
sys.path.append('F:\project\信大地图')  # 添加上一级目录到Python路径
from map_maintain.api_request import Amap
from map_maintain.way_link_api_request import write_edges
from map_maintain.way_search import dijkstra
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
        self.setWindowTitle("信大游览导航")
        self.amap = Amap('南京', 17)  # 创建Amap类的实例
        self.view1 = QGraphicsView()
        self.view1.setFixedSize(500, 400)
        self.view2 = QGraphicsView()
        self.view2.setFixedSize(500, 400)

        self.view3 = QGraphicsView()
        self.view3.setFixedSize(700, 600)
        self.scene1 = QGraphicsScene()
        self.scene2 = QGraphicsScene()
        self.scene3 = QGraphicsScene()
        self.pixmap_items1 = []  # 用于存储QGraphicsPixmapItem的引用列表
        self.pixmap_items2 = []  # 用于存储第二个QGraphicsPixmapItem的引用列表

        self.view1.setScene(self.scene1)
        self.view2.setScene(self.scene2)
        self.view1.setRenderHint(QPainter.Antialiasing, True)  # 添加抗锯齿效果
        self.view1.setRenderHint(QPainter.SmoothPixmapTransform, True)  # 添加平滑变换效果
        self.view1.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view2.setRenderHint(QPainter.Antialiasing, True)
        self.view2.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.view2.setDragMode(QGraphicsView.ScrollHandDrag)
        
        factor = 1.15
        self.view1.scale(factor, factor)
        self.view2.scale(factor, factor)

        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setFixedSize(250, 50)
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setFixedSize(250, 50)
        self.search_button = QPushButton("搜索")
        self.search_button.setFixedSize(240, 50)
        self.zoom_in_button = QPushButton("放大")
        self.zoom_in_button.setFixedSize(125, 50)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button = QPushButton("缩小")
        self.zoom_out_button.setFixedSize(125, 50)
        self.zoom_out_button.clicked.connect(self.zoom_out)

        # 重新创建布局，调整按键的位置
        layout = QGridLayout()
        
        layout.addWidget(self.view1, 0, 0,2,2 ) 
        layout.setAlignment(self.view1, Qt.AlignTop)
        layout.addWidget(self.view2, 2, 0,2,2)  
        layout.setAlignment(self.view2, Qt.AlignTop)
        layout.addWidget(self.view3, 0, 2,0,3)  
        layout.setAlignment(self.view3, Qt.AlignTop)
        layout.addWidget(self.lineEdit1, 4, 0,)
        layout.addWidget(self.lineEdit2, 4, 1,)
        layout.addWidget(self.search_button, 4, 2,1,1 )
        layout.setAlignment(self.search_button, Qt.AlignLeft)
        layout.addWidget(self.zoom_in_button, 4, 3,)
        layout.setAlignment(self.zoom_in_button, Qt.AlignLeft)
        layout.addWidget(self.zoom_out_button, 4, 4, )
        layout.setAlignment(self.zoom_out_button, Qt.AlignLeft)
        self.setLayout(layout)
        

        #路径推荐显示
        self.textEdit = QTextEdit()
        font = QFont()
        font.setPointSize(18) 
        self.textEdit.setFont(font)
        self.textEdit.setFixedSize(700, 200)
        layout.addWidget(self.textEdit, 3, 2,2,1)
        layout.setAlignment(self.textEdit, Qt.AlignTop)


        self.search_button.clicked.connect(self.on_button_clicked)
        # 加载整个文件夹的图片到场景
        folder_path = 'F:\project\信大地图\map_maintain\map_png'
        self.load_images_to_scene(folder_path, self.pixmap_items1)
        self.load_images_to_scene(folder_path, self.pixmap_items2)

    def load_images_to_scene(self, folder_path, pixmap_items):
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(folder_path, filename)
                pixmap = QPixmap(img_path)
                pixmap_item = QGraphicsPixmapItem(pixmap)
                pixmap_items.append(pixmap_item)

    def on_button_clicked(self):
        folder_path =r'F:\project\信大地图\map_maintain\map_png'
        # 获取文件夹中的所有文件
        files = os.listdir(folder_path)
        # 创建一个字典，键是去掉后缀的文件名，值是文件的路径
        name = {os.path.splitext(file)[0]: os.path.join(folder_path, file) for file in files}
        address_exist1 = True
        address_exist2 = True
        if self.lineEdit2.text() == '' and self.lineEdit1.text() !=None:
            location1 = self.lineEdit1.text()
            print(location1)
            if  self.lineEdit1.text() in name.keys():
                print(name[self.lineEdit1.text()])
                self.scene1.clear()
                pixmap = QPixmap(name[self.lineEdit1.text()])
                pixmap_item = self.scene1.addPixmap(pixmap)
                self.view1.setScene(self.scene1)
                self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
            
            else:
                loc1 = self.amap.address_to_geocode(address=self.lineEdit1.text())
                page1 = self.amap.map_to_geocode_map(loc1)
                if page1 == 0 or self.lineEdit2.text() == None or self.lineEdit1.text() == None:
                    self.textEdit.setText('请输入正确的地址或路径')
                    address_exist1 = False
                
                else:
                    pixmap1 = QPixmap(page1)
                    pixmap_item1 = self.scene1.addPixmap(pixmap1)
                    self.pixmap_items1.append(pixmap_item1)
                    self.view1.setScene(self.scene1)
                    self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
                    self.view1.update()
                    address_exist1 = True
        
        if self.lineEdit1.text() == '' and self.lineEdit2.text() !=None:
            location2 = self.lineEdit2.text()
            print(location2)
            if self.lineEdit2.text() in name.keys():
                print(name[self.lineEdit2.text()])
                self.scene2.clear()
                pixmap = QPixmap(name[self.lineEdit2.text()])
                pixmap_item = self.scene2.addPixmap(pixmap)
                self.view2.setScene(self.scene2)
                self.view2.fitInView(self.scene2.sceneRect(), Qt.KeepAspectRatio)
            else:
                loc2 = self.amap.address_to_geocode(address=self.lineEdit2.text())
                page2 = self.amap.map_to_geocode_map(loc2)
                if page2 == 0 or self.lineEdit1.text() == None or self.lineEdit2.text() == None:
                    self.textEdit.setText('请输入正确的地址或路径')
                    address_exist2 = False
                else:
                    pixmap2 = QPixmap(page2)
                    pixmap_item2 = self.scene2.addPixmap(pixmap2)
                    self.pixmap_items2.append(pixmap_item2)
                    self.view2.setScene(self.scene2)
                    self.view2.fitInView(self.scene2.sceneRect(), Qt.KeepAspectRatio)
                    self.view2.update()
                    address_exist2 = True
        else:
            location1 = self.lineEdit1.text()
            location2 = self.lineEdit2.text()
            print(location1)
            print(location2)
            
            if  self.lineEdit1.text() in name.keys():
                print(name[self.lineEdit1.text()])
                self.scene1.clear()
                pixmap = QPixmap(name[self.lineEdit1.text()])
                pixmap_item = self.scene1.addPixmap(pixmap)
                self.view1.setScene(self.scene1)
                self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
            
            else:
                loc1 = self.amap.address_to_geocode(address=self.lineEdit1.text())
                page1 = self.amap.map_to_geocode_map(loc1)
                if page1 == 0 or self.lineEdit2.text() == None or self.lineEdit1.text() == None:
                    self.textEdit.setText('请输入正确的地址或路径')
                    address_exist1 = False
                else:    
                    pixmap1 = QPixmap(page1)
                    pixmap_item1 = self.scene1.addPixmap(pixmap1)
                    self.pixmap_items1.append(pixmap_item1)
                    self.view1.setScene(self.scene1)
                    self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
                    self.view1.update()
                    address_exist1 = True

            if self.lineEdit2.text() in name.keys():
                print(name[self.lineEdit2.text()])
                self.scene2.clear()
                pixmap = QPixmap(name[self.lineEdit2.text()])
                pixmap_item = self.scene2.addPixmap(pixmap)
                self.view2.setScene(self.scene2)
                self.view2.fitInView(self.scene2.sceneRect(), Qt.KeepAspectRatio)
            else:
                loc2 = self.amap.address_to_geocode(address=self.lineEdit2.text())
                page2 = self.amap.map_to_geocode_map(loc2)
                if page2 == 0 or self.lineEdit1.text() == None or self.lineEdit2.text() == None:
                    self.textEdit.setText('请输入正确的地址或路径')
                    address_exist2 = False
                else:
                    pixmap2 = QPixmap(page2)
                    pixmap_item2 = self.scene2.addPixmap(pixmap2)
                    self.pixmap_items2.append(pixmap_item2)
                    self.view2.setScene(self.scene2)
                    self.view2.fitInView(self.scene2.sceneRect(), Qt.KeepAspectRatio)
                    self.view2.update()
                    address_exist2 = True
            print(address_exist1)
            print(address_exist2)
            if address_exist1 is False or address_exist2 is False :
                self.textEdit.setText('请输入正确的路径')
            else:
                path_print, distances_print,path,distances,path_jw,line_edge=dijkstra(location1,location2)
                if path_print == None:
                    self.textEdit.setText('请输入正确的地址或路径')
                else:
                    path_lable_map = self.amap.path_lable(path_jw, line_edge)
                    pixmap3 = QPixmap(path_lable_map)
                    pixmap_item3 = self.scene3.addPixmap(pixmap3)
                    self.view3.setScene(self.scene3)
                    self.view3.update()


                    
                    self.textEdit.setText(path_print+'    '+distances_print)
                    print(path_print)





        # file = 'map_maintain/verts.txt'
        # write_edges(file)

    def zoom_in(self):
        self.view1.scale(1.2, 1.2)
        self.view2.scale(1.2, 1.2)

    def zoom_out(self):
        self.view1.scale(1 / 1.2, 1 / 1.2)
        self.view2.scale(1 / 1.2, 1 / 1.2)

if __name__ == "__main__":
    app = QApplication([])
    viewer = MapViewer()
    viewer.show()
    app.exec_()
  