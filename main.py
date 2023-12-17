import sys
sys.path.append('F:\project\信大地图')  # 添加上一级目录到Python路径
from play_windows.windows_main import QApplication, MapViewer

if __name__ == "__main__":
    app = QApplication([])
    viewer = MapViewer()
    viewer.show()
    app.exec_()