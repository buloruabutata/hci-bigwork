from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys
import Main
from Method import *
import os
import random
from Gesture import CameraInput
import time

class VideoWindow(QMainWindow):
    def __init__(self, mp4filepath=r"D:\视频\我的视频-1.mp4"):
        super().__init__()
        self.mp4filepath = mp4filepath
        self.main_UI()
        self.camera_UI()
        self.video_UI()
        # self.flag = [0,0,0]
        self.time = [0,0,0]
        self.player.error.connect(self.handle_error)
        
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
        
        if self.camera_input.gesture_result == "OK" and (time.time()-self.time[0] > 2 or self.time[0] == 0):
            self.camera_input.gesture_result = ""
            self.play_video()
            self.time[0] = time.time()
            # self.flag[0] = 1
            # self.time = 
    
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
        
    def toMain(self):
        self.camera_input.stop()
        self.main_window = Main.App()
        self.main_window.show()
        self.close()
        
    def video_UI(self):
        # 创建视频播放器
        self.player = QMediaPlayer()
        # 创建视频显示组件
        self.videoWidget = QVideoWidget()

        # 设置视频显示组件的尺寸策略为可扩展
        self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 将视频显示组件添加到布局中，并调整其占据的行和列数
        # 例如，您可以让它占据从第1行到第8行，从第0列到第15列
        self.main_layout.addWidget(self.videoWidget, 0, 0, 9, 12)

        # 将视频显示组件设置为视频播放器的视频输出
        self.player.setVideoOutput(self.videoWidget)

        # 创建播放按钮并设置图标
        self.playButton = QPushButton()
        self.playIcon = QIcon("./images/play.svg")  # 播放图标
        self.pauseIcon = QIcon("./images/pause.svg")  # 暂停图标
        self.playButton.setIcon(self.playIcon)
        self.playButton.setIconSize(QSize(32, 32))  # 设置图标大小

        # 将播放按钮添加到布局中
        self.main_layout.addWidget(self.playButton, 8, 8)
        
        # if self.camera_input.gesture_result == "OK":
        #     self.play_video()
        self.playButton.clicked.connect(self.play_video)

        # 创建快退按钮
        self.rewindButton = QPushButton()
        self.prev_btn = QIcon('./images/prev.svg')
        self.next_btn = QIcon('./images/next.svg')
        self.rewindButton.setIcon(self.prev_btn)
        self.main_layout.addWidget(self.rewindButton, 3, 0)
        self.rewindButton.clicked.connect(self.rewind_video)

        # 创建快进按钮
        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(self.next_btn)
        self.main_layout.addWidget(self.forwardButton, 3, 15)
        self.forwardButton.clicked.connect(self.forward_video)
        
        # 创建
        self.help_btn = new_button('./images/help.svg', 100, 100, '帮助')
        self.main_btn = new_button('./images/home.svg', 100, 100, '首页')
        # 定位
        self.main_layout.addWidget(self.main_btn, 0, 12, 2, 2)
        self.main_layout.addWidget(self.help_btn, 0, 14, 2, 2)
        # 链接到方法
        self.help_btn.clicked.connect(lambda: open_help("https://www.bing.com"))
        self.main_btn.clicked.connect(self.toMain)

        # 如果提供了视频文件路径，则加载视频
        if self.mp4filepath:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.mp4filepath)))

    def play_video(self):
        # 检查当前媒体播放状态
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.playButton.setText("播放")
        else:
            self.player.play()
            self.playButton.setText("暂停")

    def rewind_video(self):
        # 设置快退时间（例如10秒）
        rewindTime = 10000  # 以毫秒为单位
        self.player.setPosition(max(self.player.position() - rewindTime, 0))

    def forward_video(self):
        # 设置快进时间（例如10秒）
        forwardTime = 10000  # 以毫秒为单位
        duration = self.player.duration()
        self.player.setPosition(min(self.player.position() + forwardTime, duration))

    # 定义处理错误的方法
    def handle_error(self):
        print("播放器错误：", self.player.errorString())

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VideoWindow()
    gui.show()
    sys.exit(app.exec_())