import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QWidget, QLineEdit, QPushButton
from PyQt5.QtCore import Qt,QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QLineEdit, QGridLayout, QPushButton, QWidget, QTextEdit,QLabel, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtWidgets import QGraphicsPixmapItem
from map_maintain.api_request import Amap
from map_maintain.way_search import dijkstra,find_all_paths_BFS
from PyQt5.QtGui import QImage, QPixmap
from map_maintain.find_nearest_point_and_sort_edges import sort_main
from map_maintain.per_edge_distance_count import count_main
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
def qimage(img):
    # 将NumPy数组转换为QImage
    height, width, channel = img.shape
    bytesPerLine = 3 * width
    qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
    return qImg

class MyGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(MyGraphicsView, self).__init__(parent)
    def wheelEvent(self, event):
        # 获取滚轮滚动的方向
        angle = event.angleDelta().y()
        # 根据滚轮滚动的方向进行放大或缩小
        if angle > 0:
            self.scale(1.25, 1.25)
        else:
            self.scale(0.8, 0.8)


#透明浏览器
# class MapViewer(QWidget): 
#     def __init__(self, parent=None):
#         super(MapViewer, self).__init__(parent)
#         self.setWindowTitle("信大游览导航")
#         self.amap = Amap('南京', 17)  # 创建Amap类的实例
#         self.view1 = QWebEngineView()
#         self.view1.setFixedSize(800, 500)
#         self.view1.page().setBackgroundColor(Qt.transparent)  # 设置页面背景为透明
#         self.view2 = QWebEngineView()
#         self.view2.setFixedSize(800, 500)
#         self.view2.page().setBackgroundColor(Qt.transparent)  # 设置页面背景为透明
            

class MapViewer(QWidget): 
    def __init__(self, parent=None):
        super(MapViewer, self).__init__(parent)
        self.setWindowTitle("信大游览导航")
        self.amap = Amap('南京', 17)  # 创建Amap类的实例
        self.view1 = QWebEngineView()
        self.view1.setFixedSize(800, 500)
        self.view2 = QWebEngineView()
        self.view2.setFixedSize(800, 500)

        self.view3 = MyGraphicsView()
        self.view3.setFixedSize(1000, 800)
        
        self.scene3 = QGraphicsScene()
        self.pixmap_items1 = []  # 用于存储QGraphicsPixmapItem的引用列表
        self.pixmap_items2 = []  # 用于存储第二个QGraphicsPixmapItem的引用列表

        
        self.view3.setScene(self.scene3)
        # 设置 QGraphicsView 的背景色
        
        self.view3.setStyleSheet("background-color: rgba(255, 255, 255, 128);")  # 设置为半透明的白色


        
     
        self.view3.setRenderHint(QPainter.Antialiasing, True)
        self.view3.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.view3.setDragMode(QGraphicsView.ScrollHandDrag)

        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setFixedSize(250, 50)
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setFixedSize(250, 50)
        self.search_button = QPushButton("搜索/搜索最短路径")
        self.search_button.setFixedSize(240, 50)
        
        self.zoom_in_button_path = QPushButton("路径放大")
        self.zoom_in_button_path.setFixedSize(125, 50)
        self.zoom_in_button_path.clicked.connect(self.zoom_in_path)
        self.zoom_out_button_path = QPushButton("路径缩小")
        self.zoom_out_button_path.setFixedSize(125, 50)
        self.zoom_out_button_path.clicked.connect(self.zoom_out_path)
        

        self.all_paths_button = QPushButton("显示所有路径")  # 新增：添加此按钮
        self.all_paths_button.setFixedSize(125, 50)
        self.all_paths_button.clicked.connect(self.display_all_paths)  # 新增：连接到新方法

        # 重新创建布局，调整按键的位置
        layout = QGridLayout()
        layout.addWidget(self.view1, 0, 0,2,2 ) 
        layout.setAlignment(self.view1, Qt.AlignTop)
        layout.addWidget(self.view2, 2, 0,2,2)  
        layout.setAlignment(self.view2, Qt.AlignTop)
        layout.addWidget(self.view3, 0, 2,0,2)  
        layout.setAlignment(self.view3, Qt.AlignTop)
        layout.addWidget(self.lineEdit1, 4, 0,)
        layout.addWidget(self.lineEdit2, 4, 1,)
        layout.addWidget(self.search_button, 4, 2,1,1 )
        layout.setAlignment(self.search_button, Qt.AlignLeft)
        
        layout.addWidget(self.zoom_in_button_path, 0, 3,)
        layout.setAlignment(self.zoom_in_button_path, Qt.AlignLeft)
        layout.setAlignment(self.zoom_in_button_path, Qt.AlignTop)
        layout.addWidget(self.zoom_out_button_path, 1, 3, )
        layout.setAlignment(self.zoom_out_button_path, Qt.AlignLeft)
        layout.setAlignment(self.zoom_out_button_path, Qt.AlignTop)


        layout.addWidget(self.all_paths_button, 4,3,1,1)  # 新增：将新按钮添加到布局中

        self.setLayout(layout)
        
        #路径推荐显示
        self.textEdit = QTextEdit()
        font = QFont()
        font.setPointSize(18) 
        self.textEdit.setFont(font)
        self.textEdit.setFixedSize(1000, 250)
        layout.addWidget(self.textEdit, 3, 2,2,1)
        layout.setAlignment(self.textEdit, Qt.AlignTop)
        self.search_button.clicked.connect(self.on_button_clicked)
        # 加载整个文件夹的图片到场景
        folder_path = 'map_maintain\map_png'
        self.load_images_to_scene(folder_path, self.pixmap_items1)
        self.load_images_to_scene(folder_path, self.pixmap_items2)






        #开机动画
        # 创建 QLabel，将图片设置为其背景
        self.label = QLabel(self)
        self.pixmap = QPixmap("字体/南信大启动 (20231218104937).png")  # 保存原始图片
        self.updatePixmap()  # 设置裁剪后的图片

        # 创建 QGraphicsOpacityEffect，并将其设置为 QLabel 的效果
        self.effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(self.effect)

        # 创建 QPropertyAnimation，将其设置为改变 QGraphicsOpacityEffect 的透明度
        self.animation = QPropertyAnimation(self.effect, b'opacity')
        self.animation.setDuration(2000)  # 动画持续时间，单位为毫秒
        self.animation.setStartValue(1)  # 开始时的透明度
        self.animation.setEndValue(0.01)  # 结束时的透明度
        self.animation.finished.connect(self.onAnimationFinished)  # 动画结束后调用 onAnimationFinished 方法
        self.animation.start()

    def onAnimationFinished(self):
        # 动画结束后，隐藏 QLabel，并更新窗口的背景
        self.label.hide()
        

    def paintEvent(self, event):
        # 在窗口绘制事件发生时，绘制窗口的背景
        self.updatePixmap()  # 更新裁剪后的图片
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.label.pixmap())
        


    def resizeEvent(self, event):
        # 当窗口大小改变时，改变 label 的大小以覆盖全窗口，并裁剪图片
        self.label.resize(self.size())
        self.updatePixmap()  # 设置裁剪后的图片
        super(MapViewer, self).resizeEvent(event)

    def updatePixmap(self):
        # 计算裁剪区域的位置和大小
        width = self.pixmap.width()
        height = self.pixmap.height()
        new_height = self.height()  # 使用窗口的高度
        new_width = int(height * self.width() / self.height())  # 根据窗口的宽高比计算新的宽度
        x = int((width *( new_width/width))*0.4)  # 计算裁剪区域的水平位置
        y = int((height *( new_height/height)*0.2))  # 计算裁剪区域的垂直位置
        # 裁剪图片并设置为 QLabel 的背景
        cropped_pixmap = self.pixmap.copy(x, y, new_width, new_height)  # 从两边向中心裁剪
        self.label.setPixmap(cropped_pixmap)







    def generate_url(self, dest, destName):
        key = "a7323c5e0b28b4753e7e45a0a04e144c"
        url = f"https://m.amap.com/navi/?dest={dest}&destName={destName}&key={key}"
        return QUrl(url)








    def load_images_to_scene(self, folder_path, pixmap_items):
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(folder_path, filename)
                pixmap = QPixmap(img_path)
                pixmap_item = QGraphicsPixmapItem(pixmap)
                pixmap_items.append(pixmap_item)

    def on_button_clicked(self):
        folder_path =r'map_maintain\map_png'
        # 获取文件夹中的所有文件
        files = os.listdir(folder_path)
        # 创建一个字典，键是去掉后缀的文件名，值是文件的路径
        name = {os.path.splitext(file)[0]: os.path.join(folder_path, file) for file in files}
        with open('./map_maintain/verts.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
        jw=dict()
        for line in lines:
            parts = line.strip().split('  ')
            if parts:
                 jw[parts[1]]=parts[2]
        #一有，二空
        if self.lineEdit2.text() == '' and self.lineEdit1.text() !='':
            self.textEdit.setText('请输入两个地点')
            location1 = self.lineEdit1.text()
            #1找得到
            if  self.lineEdit1.text() in name.keys():
                self.view1.load(self.generate_url(jw[location1], location1))
               
                
            else:
                
                loc1 = self.amap.address_to_geocode(address=self.lineEdit1.text())
                page1 = self.amap.map_to_geocode_map(loc1)
                
                if page1 == 0 :
                    self.textEdit.setText('请输入正确的地址或路径')
                    
                
                else:
                    sort_main()
                    count_main()
                    print('执行1')
                    self.view1.load(self.generate_url(jw[location1], location1))
                    
        #二有一空
        elif self.lineEdit1.text() == '' and self.lineEdit2.text() !='':
            self.textEdit.setText('请输入两个地点')
            location2 = self.lineEdit2.text()
            #2找得到
            if self.lineEdit2.text() in name.keys():
                self.view2.load(self.generate_url(jw[location2], location2))
            else:
                
                loc2 = self.amap.address_to_geocode(address=self.lineEdit2.text())
                page2 = self.amap.map_to_geocode_map(loc2)
                sort_main()
                count_main()
                print('执行2')
                if page2 == 0 :
                    self.textEdit.setText('请输入正确的地址或路径')
                   
                else:
                    self.view2.load(self.generate_url(jw[location2], location2))
            #1找得到
            if self.lineEdit1.text() in name.keys():
               self.view1.load(self.generate_url(jw[location1], location1))
            else:
                loc1 = self.amap.address_to_geocode(address=self.lineEdit1.text())
                page1 = self.amap.map_to_geocode_map(loc1)
                sort_main()
                count_main()
                print('执行3')
                if page1 == 0 :
                    self.textEdit.setText('请输入正确的地址或路径')
                    
                else:
                    self.view1.load(self.generate_url(jw[location1], location1))
        
        
        #二都空
        elif self.lineEdit1.text() == '' and self.lineEdit2.text() =='':
            self.textEdit.setText('请输入正确的地址或路径')
        #都有
        elif self.lineEdit1.text() !='' and self.lineEdit2.text() !='':
            location1 = self.lineEdit1.text()
            location2 = self.lineEdit2.text()
            #都找得到
            if  self.lineEdit1.text() in name.keys() and self.lineEdit2.text() in name.keys():
                self.view1.load(self.generate_url(jw[location1], location1))
            
                self.view2.load(self.generate_url(jw[location2], location2))
                if self.lineEdit1.text() == self.lineEdit2.text():
                    self.textEdit.setText('请输入不同的地址或路径')
                else:
                    path_print, distances_print,path,distances,path_jw,line_edge=dijkstra(location1,location2)
                    if path_print == '':
                        self.textEdit.setText('请输入正确的地址或路径')
                    else:
                        path_lable_map = self.amap.path_lable(path_jw, line_edge)
                        pixmap3 = QPixmap(path_lable_map)
                        pixmap_item3 = self.scene3.addPixmap(pixmap3)
                        self.view3.setScene(self.scene3)
                        self.view3.update()
                        self.textEdit.setText(path_print+'    '+distances_print)

            #有1找不到
            elif self.lineEdit1.text() in name.keys() == False or self.lineEdit2.text() in name.keys() == False:
                loc1 = self.amap.address_to_geocode(address=self.lineEdit1.text())
                page1 = self.amap.map_to_geocode_map(loc1)
                
                loc2 = self.amap.address_to_geocode(address=self.lineEdit2.text())
                page2 = self.amap.map_to_geocode_map(loc2)
                #无图返回
                if  page1 == 0 and page2 == 0:
                    self.textEdit.setText('请输入正确的地址或路径')
                #有一图返回
                elif page1 !=0 or page2 !=0:
                    self.textEdit.setText('请输入的两个地点都是正确的地点')
                    sort_main()
                    count_main()
                elif page1 !=0 and page2 !=0:
                    sort_main()
                    count_main()
                    self.view1.load(self.generate_url(jw[location1], location1))
                   

                    self.view2.load(self.generate_url(jw[location2], location2))
                   

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

        files = os.listdir(folder_path)
        # 创建一个字典，键是去掉后缀的文件名，值是文件的路径
        name = {os.path.splitext(file)[0]: os.path.join(folder_path, file) for file in files}        
            
            
            
            
            
            
            
            
            
            
            # elif self.lineEdit1.text() in name.keys() != False and self.lineEdit2.text() in name.keys() == False:
            #     pixmap2 = QPixmap(page2)
            #     pixmap_item2 = self.scene2.addPixmap(pixmap2)
            #     self.pixmap_items2.append(pixmap_item2)
            #     self.view2.setScene(self.scene2)
            #     self.view2.fitInView(self.scene2.sceneRect(), Qt.KeepAspectRatio)
            #     self.view2.update()
            #     address_exist2 = True







                
            #     print('执行3')
            #     if page1 == 0 or self.lineEdit2.text() == None or self.lineEdit1.text() == None:
            #         self.textEdit.setText('请输入正确的地址或路径')
            #         address_exist1 = False
            #     else:    
            #         pixmap1 = QPixmap(page1)
            #         pixmap_item1 = self.scene1.addPixmap(pixmap1)
            #         self.pixmap_items1.append(pixmap_item1)
            #         self.view1.setScene(self.scene1)
            #         self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
            #         self.view1.update()
            #         address_exist1 = True

            # if self.lineEdit2.text() in name.keys():
                
            #     self.scene2.clear()
            #     pixmap = QPixmap(name[self.lineEdit2.text()])
            #     pixmap_item = self.scene2.addPixmap(pixmap)
            #     self.view2.setScene(self.scene2)
            #     self.view2.fitInView(self.scene2.sceneRect(), Qt.KeepAspectRatio)
            # else:
                
            #     loc2 = self.amap.address_to_geocode(address=self.lineEdit2.text())
            #     page2 = self.amap.map_to_geocode_map(loc2)
            #     sort_main()
            #     count_main()
            #     print('执行4')
            #     if page2 == 0 or self.lineEdit1.text() == None or self.lineEdit2.text() == None:
            #         self.textEdit.setText('请输入正确的地址或路径')
            #         address_exist2 = False
            #     else:
            #         pixmap2 = QPixmap(page2)
            #         pixmap_item2 = self.scene2.addPixmap(pixmap2)
            #         self.pixmap_items2.append(pixmap_item2)
            #         self.view2.setScene(self.scene2)
            #         self.view2.fitInView(self.scene2.sceneRect(), Qt.KeepAspectRatio)
            #         self.view2.update()
            #         address_exist2 = True
            
            # if address_exist1 is False or address_exist2 is False :
            #     self.textEdit.setText('请输入正确的路径')
            # else:
               
                
            #     path_print, distances_print,path,distances,path_jw,line_edge=dijkstra(location1,location2)
            #     if path_print == None:
            #         self.textEdit.setText('请输入正确的地址或路径')
            #     else:
            #         path_lable_map = self.amap.path_lable(path_jw, line_edge)
            #         pixmap3 = QPixmap(path_lable_map)
            #         pixmap_item3 = self.scene3.addPixmap(pixmap3)
            #         self.view3.setScene(self.scene3)
            #         self.view3.update()
            #         self.textEdit.setText(path_print+'    '+distances_print)
                    

        # file = 'map_maintain/verts.txt'
        # write_edges(file)
    def display_all_paths(self): 
        start_location = self.lineEdit1.text()
        end_location = self.lineEdit2.text()
        if start_location and end_location:
            all_paths = find_all_paths_BFS(start_location, end_location, max_nodes=1000,max_paths=5)  # Call the new function
            self.textEdit.clear()
            for path in all_paths:
                self.textEdit.append(f"路径: {path}")  # Display path
                self.textEdit.append("\n")
        else:
            self.textEdit.setText("请输入起始点和终点。")
            
    def zoom_in(self):
        self.view1.scale(1.2, 1.2)
        self.view2.scale(1.2, 1.2)

    def zoom_out(self):
        self.view1.scale(1 / 1.2, 1 / 1.2)
        self.view2.scale(1 / 1.2, 1 / 1.2)
    def zoom_in_path(self):
        self.view3.scale(1.2, 1.2)
    def zoom_out_path(self):
        self.view3.scale(1 / 1.2, 1 / 1.2)
if __name__ == "__main__":
    app = QApplication([])
    viewer = MapViewer()
    viewer.show()
    app.exec_()
  