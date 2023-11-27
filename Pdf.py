from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import Main
from Method import *
import os
import random
from Gesture import CameraInput
import fitz
from pathlib import Path


class PdfWindow(QMainWindow):
    def __init__(self, pdffilepath="D:\\file\\2103.14641.pdf"):
        super().__init__()
        self.pdffilepath = pdffilepath
        self.main_UI()
        self.pdf_UI()
        self.camera_UI()
        # self.initUI()
        
        
    def camera_UI(self):
        self.camera_label = QLabel()
        self.camera_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # (5,12)是左上角坐标 （4，4）是大小
        self.main_layout.addWidget(self.camera_label, 5, 12, 4, 4)
        self.camera_input = CameraInput()
        self.camera_input.stop_flag = False
        self.camera_input.start()
        # 新增一个信号和槽函数，用于显示摄像头捕获的图像
        self.camera_input.frame_ready.connect(self.on_frame_ready)
        
    # 新增一个槽函数，用于显示摄像头捕获的图像
    def on_frame_ready(self, frame):
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.camera_label.setPixmap(pixmap)
    
    def main_UI(self):
        # 设置窗口大小
        self.setFixedSize(1600, 900)
        # 设置窗口名称
        self.setWindowTitle("基于AI的多媒体辅助控制系统")
        # 设置窗口的图片
        # self.setWindowIcon(QIcon("xxx.svg"))
        # 设置一个主窗口
        self.main_wight = QWidget()
        # 设置一个主窗口布局--我比较喜欢网格布局
        self.main_layout = QGridLayout()
        # 创建一个9*16的网格布局(用于定位，后期会删除)
        for i in range(9):
            self.main_layout.setRowMinimumHeight(i, 100)
            for j in range(16):
                self.main_layout.addWidget(QLabel(f"({i},{j})"), i, j) # 不显示坐标，只添加空的QLabel
                if i == 0:
                    self.main_layout.setColumnMinimumWidth(j, 100)
        # 将窗口加入布局
        self.main_wight.setLayout(self.main_layout)
        # 将这个主窗口设置成窗口主部件
        self.setCentralWidget(self.main_wight)
        # 创建
        self.help_btn = new_button('./images/help.svg', 100, 100, '帮助')
        self.main_btn = new_button('./images/home.svg', 100, 100, '首页')
        # 定位
        self.main_layout.addWidget(self.main_btn, 0, 13, 1, 1)
        self.main_layout.addWidget(self.help_btn, 0, 15, 1, 1)
        # 链接到方法
        self.help_btn.clicked.connect(lambda: open_help("https://www.bing.com"))
        self.main_btn.clicked.connect(self.toMain)
        
    def toMain(self):
        self.camera_input.stop()
        self.main_window = Main.App()
        self.main_window.show()
        self.close()
        
    def pdf_UI(self):
        self.next_page_btn = new_button('./images/next.svg', 100, 100, '下一页')
        self.prev_page_btn = new_button('./images/prev.svg', 100, 100, '上一页')
        # 定位
        self.main_layout.addWidget(self.prev_page_btn, 1, 13, 1, 1)
        self.main_layout.addWidget(self.next_page_btn, 1, 15, 1, 1)
        # 链接到方法
        self.next_page_btn.clicked.connect(self.next_page)
        self.prev_page_btn.clicked.connect(self.previous_page)

        self.zoom_down_btn = new_button('./images/zoom_down.svg', 100, 100, '缩小')
        self.zoom_up_btn = new_button('./images/zoom_up.svg', 100, 100, '放大')
        # 定位
        self.main_layout.addWidget(self.zoom_up_btn, 2, 13, 1, 1)
        self.main_layout.addWidget(self.zoom_down_btn, 2, 15, 1, 1)
        # 链接到方法
        self.zoom_up_btn.clicked.connect(self.zoom_up)
        self.zoom_down_btn.clicked.connect(self.zoom_down)

        self.title = Path(self.pdffilepath).stem # get name of the file, preferred because metadata['title'] is not often available
        self.doc = fitz.open(self.pdffilepath) # open the given file
        self.metadata = self.doc.metadata
        self.pageNumber = 0
        self.zoom = 1
        self.renderPage()


    def clearLayout(self):
        self.main_layout.removeWidget(self.label)
        self.update()


    def renderPage(self):
        page = self.doc[self.pageNumber]
        zoom_x = self.zoom  # horizontal zoom
        zomm_y = self.zoom  # vertical zoom
        mat = fitz.Matrix(zoom_x, zomm_y)  # zoom factor 2 in each dimension
        pix = page.get_pixmap(matrix=mat)
        fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
        pixmap = QPixmap.fromImage(img)

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.setGeometry(QRect(0,0, pix.width, pix.height))
        self.label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label,0,0,12,12)
        # self.vbox.addWidget(label)
        # self.vbox.setContentsMargins(0, 0, 0, 0)

        self.update()


    def saveToFile(self, key, value):
        storedData = dict()

        if self.fileDataPath.exists():
            oldData = self.fileDataPath.read_text()
            if isinstance(eval(oldData), dict):
                storedData = eval(oldData)

        storedData[key] = value
        self.fileDataPath.write_text(str(storedData))


    def next_page(self):
        self.clearLayout()
        self.pageNumber += 1
        self.renderPage()


    def previous_page(self):
        self.clearLayout()
        self.pageNumber -= 1
        self.renderPage()

    def zoom_up(self):
        self.clearLayout()
        self.zoom += 0.1
        if self.zoom>2:
            self.zoom=2
        self.renderPage()
    
    def zoom_down(self):
        self.clearLayout()
        self.zoom -= 0.1
        if self.zoom<0.5:
            self.zoom=0.5
        self.renderPage()


    def goto(self, number):
        self.pageNumber = number
        self.renderPage()


    def quit(self):
        '''Store current page number and quit.'''

        self.saveToFile("pageNumber", self.pageNumber)
        QApplication.instance().quit()


    def keyPressEvent(self, event):
        '''Call functions associated with a key press, if any.'''

        global commands
        key = event.text()

        if key == 'g' or key.isnumeric():
            commands.append(key)
            return

        if event.key() == Qt.Key_Escape:
            commands = []
            return

        if event.key() == Qt.Key_Return and commands:
            command = commands[0]
            number = int("".join(commands[1:]))
            commands = []
            self.keymaps[command](number)
            return

        if key in self.keymaps.keys():
            self.keymaps[key]()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = PdfWindow()
    gui.show()
    sys.exit(app.exec_())