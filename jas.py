from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.view = QWebEngineView(self)
        self.view.setFixedSize(1600, 1000)

        dest = "116.470098,39.992838"
        destName = "阜通西"
        url = f"https://m.amap.com/navi/?dest={dest}&destName={destName}&key=a7323c5e0b28b4753e7e45a0a04e144c"

        self.view.load(QUrl(url))
        self.setCentralWidget(self.view)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())