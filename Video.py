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

class VideoWindow(QMainWindow):
    def __init__(self, mp4filepath=None):
        super().__init__()
        self.mp4filepath = mp4filepath
        self.main_UI()
        self.video_UI()
        self.camera_UI()
        
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
        self.main_layout.addWidget(self.main_btn, 0, 12, 2, 2)
        self.main_layout.addWidget(self.help_btn, 0, 14, 2, 2)
        # 链接到方法
        self.help_btn.clicked.connect(lambda: open_help("https://www.bing.com"))
        self.main_btn.clicked.connect(self.toMain)
        
    def toMain(self):
        self.camera_input.stop()
        self.main_window = Main.App()
        self.main_window.show()
        self.close()
        
    def video_UI(self):
        #todo
        pass
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VideoWindow()
    gui.show()
    sys.exit(app.exec_())