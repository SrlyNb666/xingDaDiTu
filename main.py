import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from play_windows.windows_main import QApplication, MapViewer

if __name__ == "__main__":
    app = QApplication([])
    viewer = MapViewer()
    viewer.show()
    app.exec_()