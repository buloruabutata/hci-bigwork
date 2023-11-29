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
        self.last_time = 0
        # 0休眠 1默认 2鼠标
        self.cur_status = 2
        self.camera_input.move = True
        self.player.error.connect(self.handle_error)
        
    def camera_UI(self):
        self.camera_label = QLabel()
        self.camera_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # (5,12)是左上角坐标 （4，4）是大小
        self.main_layout.addWidget(self.camera_label, 10, 24, 8, 8)
        self.camera_input = CameraInput()
        self.camera_input.stop_flag = False
        self.camera_input.start()
        # 新增一个信号和槽函数，用于显示摄像头捕获的图像
        self.camera_input.frame_ready.connect(self.on_frame_ready)
        
    # 新增一个槽函数，用于显示摄像头捕获的图像
    def on_frame_ready(self, frame):
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        # 获取label的大小
        label_size = self.camera_label.size()
        # 将pixmap缩放到label的大小
        scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio)
        self.camera_label.setPixmap(scaled_pixmap)
        
        self.update_gesture_label()
        curtime = time.time()
        if self.camera_input.gesture_result != "yeah" and self.cur_status == 0:
            return
        if self.camera_input.gesture_result == "yeah" and curtime - self.last_time > 3:
            self.cur_status = self.status_label.switch_mode()
            if self.cur_status == 2:
                self.camera_input.move = True
            else:
                self.camera_input.move = False
            self.last_time = curtime
            return 
        
        if self.cur_status == 1 and curtime - self.last_time > 0.5:
            if self.camera_input.gesture_result == "up":
                self.volume_slider.setVisible(True)
                self.volume_slider.setValue(self.volume_slider.value() + 1)
                return 
            if self.camera_input.gesture_result == "down":
                self.volume_slider.setVisible(True)
                self.volume_slider.setValue(self.volume_slider.value() - 1)
                return
            self.volume_slider.setVisible(False)

        if self.cur_status == 1 and curtime - self.last_time > 3:
            if self.camera_input.gesture_result == "left":
                self.rewind_video()
                self.last_time = curtime
            if self.camera_input.gesture_result == "right":
                self.forward_video()
                self.last_time = curtime
            if self.camera_input.gesture_result == "stone":
                self.play_or_pause()
                self.last_time = curtime
            if self.camera_input.gesture_result == "ok":
                self.refresh_video()
                self.last_time = curtime
        
    def update_gesture_label(self):
        if self.cur_status == 1:
            if self.camera_input.gesture_result == "up":
                self.gesture_usage.setText("增加音量")
                return 
            if self.camera_input.gesture_result == "down":
                self.gesture_usage.setText("缩小音量")
                return

        if self.cur_status == 1:
            if self.camera_input.gesture_result == "left":
                self.gesture_usage.setText("快退30s")
                return
            if self.camera_input.gesture_result == "right":
                self.gesture_usage.setText("快进30s")
                return
            if self.camera_input.gesture_result == "stone":
                self.gesture_usage.setText("播放/暂停")
                return
            if self.camera_input.gesture_result == "ok":
                self.gesture_usage.setText("从头播放")
                return
            self.gesture_usage.setText("无")
        
        if self.cur_status == 2:
            if self.camera_input.gesture_result == "open":
                self.gesture_usage.setText("移动鼠标")
                return
            if self.camera_input.gesture_result == "stone":
                self.gesture_usage.setText("单击鼠标左键")
                return
            self.gesture_usage.setText("固定鼠标")
            return
        
        # if self.camera_input.gesture_result == "None":
        self.gesture_usage.setText("无")
        
    def main_UI(self):
        # 设置窗口大小
        self.setFixedSize(QApplication.desktop().width(), QApplication.desktop().height() - 80)
        # 设置窗口名称
        self.setWindowTitle("基于手势识别的多媒体辅助控制系统")
        # 设置窗口的图片
        # self.setWindowIcon(QIcon("xxx.svg"))
        # 设置一个主窗口
        self.main_wight = QWidget()
        # 设置一个主窗口布局--我比较喜欢网格布局
        self.main_layout = QGridLayout()
        # 创建一个9*16的网格布局(用于定位，后期会删除)
        for i in range(18):
            self.main_layout.setRowMinimumHeight(i, int(QApplication.desktop().height() / 18))
            for j in range(32):
                self.main_layout.addWidget(QLabel(f""), i, j) # 不显示坐标，只添加空的QLabel
                if i == 0:
                    self.main_layout.setColumnMinimumWidth(j, int(QApplication.desktop().width() / 32))
        # 将窗口加入布局
        self.main_wight.setLayout(self.main_layout)
        # 将这个主窗口设置成窗口主部件
        self.setCentralWidget(self.main_wight)
        
        self.gesture_label = new_text_label("当前手势功能：", 150, 50)
        self.main_layout.addWidget(self.gesture_label, 3, 27, 8, 8)
        self.gesture_usage = new_text_label("无", 150, 50)
        self.main_layout.addWidget(self.gesture_usage, 3, 30, 8, 8)
        
    def toMain(self):
        self.camera_input.stop()
        self.player = None
        self.main_window = Main.App()
        self.main_window.show()
        self.close()
        
    def video_UI(self):
        # 创建视频播放器
        self.player = QMediaPlayer()
        self.player.stateChanged.connect(self.update_play_btn)
        # 创建视频显示组件
        self.videoWidget = QVideoWidget()

        # 设置视频显示组件的尺寸策略为可扩展
        self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 将视频显示组件添加到布局中，并调整其占据的行和列数
        # 例如，您可以让它占据从第1行到第8行，从第0列到第15列
        self.main_layout.addWidget(self.videoWidget, 0, 0, 15, 24)

        # 将视频显示组件设置为视频播放器的视频输出
        self.player.setVideoOutput(self.videoWidget)

        # 创建播放按钮并设置图标
        self.play_btn = new_button('images/play.svg', 100, 100, '播放(👊stone)')
        self.prev_btn = new_button('images/prev.svg', 100, 100, '快进30秒(👍left)')
        self.next_btn = new_button('images/next.svg', 100, 100, '快退30秒(👍right)')
        self.refresh_btn = new_button('images/refresh.svg', 100, 100, '刷新(👌ok)')
        self.volume_btn = new_button('images/voice.svg', 100, 100, '音量(👆或者👇)')
        self.upmp4_btn = new_button('images/upload.svg', 100, 100, '上传')
		# 将播放按钮添加到布局中
        self.main_layout.addWidget(self.prev_btn, 16, 1, 4, 2)
        self.main_layout.addWidget(self.play_btn, 16, 5, 4, 2)
        self.main_layout.addWidget(self.next_btn, 16, 9, 4, 2)
        self.main_layout.addWidget(self.refresh_btn, 16, 13, 4, 2)
        self.main_layout.addWidget(self.volume_btn, 16, 17, 4, 2)
        self.main_layout.addWidget(self.upmp4_btn, 16, 21, 4, 2)
        self.upmp4_btn.clicked.connect(self.uploadFile)
        
        self.play_btn.clicked.connect(self.play_or_pause)
        self.prev_btn.clicked.connect(self.rewind_video)
        self.next_btn.clicked.connect(self.forward_video)
        self.refresh_btn.clicked.connect(self.refresh_video)
        self.volume_btn.clicked.connect(self.show_or_hide_volume_slider)
        
        # 创建
        self.exit_btn = new_button('./images/exit.svg', 100, 100, '退出')
        self.exit_btn.clicked.connect(self.close_self)
        self.help_btn = new_button('./images/help.svg', 100, 100, '帮助')
        self.main_btn = new_button('./images/home.svg', 100, 100, '首页')
        self.status_label = StatusQLabel(400, 100, self)
        
        # 定位
        self.main_layout.addWidget(self.main_btn, 0, 24, 4, 4)
        self.main_layout.addWidget(self.help_btn, 0, 27, 4, 4)
        self.main_layout.addWidget(self.exit_btn, 0, 30, 4, 4)
        self.main_layout.addWidget(self.status_label, 5, 27, 8, 8)
        # 链接到方法
        self.help_btn.clicked.connect(lambda: open_help("https://www.cnblogs.com/19373400weileng/p/17864459.html"))
        self.exit_btn.clicked.connect(self.close_self)
        self.main_btn.clicked.connect(self.toMain)
        
        self.slider = QSlider(Qt.Horizontal, self)
        # 设置滑动条的最小值和最大值
        self.slider.setMinimum(0)
        self.slider.setMaximum(600)
        # 设置滑动条的初始值
        self.slider.setValue(0)
        self.main_layout.addWidget(self.slider, 15, 0, 1, 21)
        # 连接进度滑动条的值改变信号和设置播放位置的槽函数
        self.slider.valueChanged.connect(self.set_position)
        self.player.positionChanged.connect(self.update_slider)
        
        # 创建一个滑动条，用于调节音量
        self.volume_slider = QSlider(Qt.Vertical, self)
        # 设置滑动条的最小值和最大值
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        # 设置滑动条的初始值
        self.volume_slider.setValue(50)
        # 设置滑动条的可见性
        self.volume_slider.setVisible(False)
        self.volume_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.volume_slider, 10, 17, 6, 2)
        self.volume_slider.raise_()
        self.volume_slider.valueChanged.connect(self.set_volume)
        
		# 创建一个 QLabel 对象来显示时间
        self.time_label = QLabel(self)
        # 设置初始文本
        self.time_label.setText("00:00 / 00:00")
        # 将标签添加到布局中
        self.main_layout.addWidget(self.time_label, 15, 21, 1, 3)
        
        
        self.set_qss()

        # 如果提供了视频文件路径，则加载视频
        if self.mp4filepath:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.mp4filepath)))
            self.player.play()
        
    def uploadFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, f'选择mp4文件', '', f'mp4文件 (*.mp4)')
        if fname:
            self.mp4filepath = os.path.abspath(fname)
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(fname)))
            self.player.play()
	
	# 显示或隐藏音量滑动条的槽函数
    def show_or_hide_volume_slider(self):
        # 如果音量滑动条是可见的，就隐藏它
        if self.volume_slider.isVisible():
            self.volume_slider.setVisible(False)
        # 否则，就显示它，并把它的位置设置为音量按钮的正上方
        else:
            self.volume_slider.setVisible(True)
    
	# 设置音量的槽函数
    def set_volume(self, value):
        # 设置媒体播放器的音量为滑动条的值
        self.player.setVolume(value)
    
    def mousePressEvent(self, event):
        if (event.x() < self.volume_slider.x() or
            event.y() < self.volume_slider.y() or
            event.x() > self.volume_slider.x() + self.volume_slider.width() or
            event.y() > self.volume_slider.y() + self.volume_slider.height()):
            self.volume_slider.setVisible(False)
            
    def set_position(self, value):
    # 如果进度滑动条被用户释放，就设置媒体播放器的播放位置为滑动条的值乘以媒体播放器的总时长除以100
        if self.slider.isSliderDown():
            self.player.setPosition(value * self.player.duration() / 600)
    
    # 更新进度滑动条的槽函数
    def update_slider(self, position):
        # 如果媒体播放器的总时长不为0，就把进度滑动条的值设置为媒体播放器的播放位置除以媒体播放器的总时长乘以100
        if self.player.duration() != 0:
            self.slider.setValue(position * 600 / self.player.duration())
            # 获取音乐的总时间和当前时间
            total_time = self.player.duration()
            current_time = self.player.position()
            # 将时间从毫秒转换为分钟和秒
            total_min, total_sec = divmod(total_time, 60000)
            current_min, current_sec = divmod(current_time, 60000)
            total_sec = int(total_sec / 1000)
            current_sec = int(current_sec / 1000)
            # 更新标签的文本
            self.time_label.setText(f"{current_min}:{current_sec:02} / {total_min}:{total_sec:02}")
            
    def close_self(self):
        self.close()

    def play_or_pause(self):
        # 如果媒体播放器的状态是播放中，就暂停播放
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        # 否则，就开始播放
        else:
            self.player.play()
    
    def refresh_video(self):
        # 设置媒体播放器的播放位置为0
        self.player.setPosition(0)
        # 开始播放
        self.player.play()
    
	# 更新播放按钮的槽函数
    def update_play_btn(self, state):
        # 如果媒体播放器的状态是播放中，就把播放按钮的图片和提示文本改为暂停
        if state == QMediaPlayer.PlayingState:
            self.play_btn.setIcon(QIcon('images/pause.svg'))
            self.play_btn.setToolTip('暂停')
        # 否则，就把播放按钮的图片和提示文本改为播放
        else:
            self.play_btn.setIcon(QIcon('images/play.svg'))
            self.play_btn.setToolTip('播放')

    def rewind_video(self):
        # 设置快退时间（例如10秒）
        rewindTime = 30000  # 以毫秒为单位
        self.player.setPosition(max(self.player.position() - rewindTime, 0))

    def forward_video(self):
        # 设置快进时间（例如10秒）
        forwardTime = 30000  # 以毫秒为单位
        duration = self.player.duration()
        self.player.setPosition(min(self.player.position() + forwardTime, duration))

    # 定义处理错误的方法
    def handle_error(self):
        print("播放器错误：", self.player.errorString())
    
    def set_qss(self):
        #B0E0E6
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.main_wight.setStyleSheet("""QWidget {background-color: #d3e6ef;}""")
        # self.list_label.setStyleSheet("""QLabel {border-radius: 10px; background-color: #45c1d6;}""")
        self.slider.setStyleSheet("""
            QSlider
            {
                
                padding-left: 15px;  /*左端点离左边的距离*/
                padding-right: 15px;
                border-radius: 5px; /*外边框矩形倒角*/
            }

            QSlider::add-page:horizontal
            {
                background-color: #7A7B79;
                height:5px;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal
            {
                background-color: #8080ff;
                height:5px;
                border-radius: 2px;
            }

            QSlider::groove:horizontal
            {
                background:transparent;
                height:6px;
            }

            QSlider::handle:horizontal   
            {
                width: 14px; 
                height: 14px;
                margin: -4px 0px -4px 0px;
                border-radius: 7px;
                background: white;
            }
        """)
        self.volume_slider.setStyleSheet("""
            QSlider
            {
                background-color: rgba(22, 22, 22, 0.7);
                padding-top: 15px;  /*上面端点离顶部的距离*/
                padding-bottom: 15px;
                border-radius: 5px; /*外边框矩形倒角*/
            }
            
            QSlider::add-page:vertical
            {
                background-color: #8080ff;
                width:5px;
                border-radius: 2px;
            }
            
            QSlider::sub-page:vertical
            {
                background-color: #7A7B79;
                width:5px;
                border-radius: 2px;
            }
            
            QSlider::groove:vertical
            {
                background:transparent;
                width:6px;
            }
            
            QSlider::handle:vertical   
            {
                height: 14px; 
                width: 14px;
                margin: 0px -4px 0px -4px;
                border-radius: 7px;
                background: white;
            }
        """)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VideoWindow()
    gui.show()
    sys.exit(app.exec_())