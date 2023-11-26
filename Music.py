import shutil
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

class MusicWindow(QMainWindow):
    def __init__(self, mp3filepath=None):
        super().__init__()
        self.mp3filepath = mp3filepath
        self.main_UI()
        self.music_UI()
        self.camera_UI()
        
    def camera_UI(self):
        self.camera_label = QLabel()
        self.camera_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        for i in range(18):
            self.main_layout.setRowMinimumHeight(i, 100)
            for j in range(32):
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
        self.main_layout.addWidget(self.main_btn, 0, 25, 4, 4)
        self.main_layout.addWidget(self.help_btn, 0, 29, 4, 4)
        # 链接到方法
        self.help_btn.clicked.connect(lambda: open_help("https://www.bing.com"))
        self.main_btn.clicked.connect(self.toMain)
        
        
    def music_UI(self):
        # 创建一个媒体播放器对象
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.music_player = QMediaPlayer()
        # 创建一个定时器对象，用于更新唱片旋转角度和进度条
        self.music_timer = QTimer()
        # 创建一个列表，用于存储音乐文件的路径
        self.music_list = []
        # 存放音乐名字
        self.name_list = []
        # 创建一个变量，用于记录当前播放的音乐索引
        self.current_index = 0

        # self.cd = QLabel()
        # self.cd_icon = QPixmap("./images/cd.svg").scaled(QSize(500,500))
        # # 创建一个变换对象，用于旋转唱片
        # transform = QTransform()
        # # 以唱片的中心为原点，顺时针旋转指定的角度
        # transform.translate(100, 100).rotate(360).translate(-100, -100)
        # self.cd.setPixmap(self.cd_icon.transformed(transform))
        # self.cd.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.main_layout.addWidget(self.cd, 1, 1, 7, 7)
        # # 创建一个变量，用于记录唱片的旋转角度
        # self.angle = 0
        
        self.play_btn = new_button('images/pause.svg', 100, 100, '播放')
        self.prev_btn = new_button('images/prev.svg', 100, 100, '上一首')
        self.next_btn = new_button('images/next.svg', 100, 100, '下一首')
        self.volume_btn = new_button('images/voice.svg', 100, 100, '音量')
        self.refresh_btn = new_button('images/refresh.svg', 100, 100, '刷新')
        self.upmp3_btn = new_button('images/upload.svg', 100, 100, '上传')
        
        self.slider = QSlider(Qt.Horizontal, self)
        # 设置滑动条的最小值和最大值
        self.slider.setMinimum(0)
        self.slider.setMaximum(600)
        # 设置滑动条的初始值
        self.slider.setValue(0)
        
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

        # 创建一个QWidget并将self.volume_slider添加到其中
        # self.slider_widget = QWidget()
        # self.slider_layout = QVBoxLayout()
        # self.volume_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout.addWidget(self.volume_slider, 10, 17, 6, 2)
        # self.volume_slider.resize(200, 300)
        # self.slider_layout.setAlignment(Qt.AlignCenter)
        
        # spacer_left = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        # spacer_right = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout.addWidget(self.prev_btn, 16, 1, 4, 2)
        self.main_layout.addWidget(self.play_btn, 16, 5, 4, 2)
        self.main_layout.addWidget(self.next_btn, 16, 9, 4, 2)
        self.main_layout.addWidget(self.refresh_btn, 16, 13, 4, 2)
        self.main_layout.addWidget(self.volume_btn, 16, 17, 4, 2)
        self.main_layout.addWidget(self.upmp3_btn, 16, 21, 4, 2)
        self.main_layout.addWidget(self.slider, 0, 2, 2, 20)
        
        # 调用初始化音乐列表的方法
        self.init_music_list()
        # 调用连接信号和槽的方法
        self.connect_slots()
        self.set_qss()
 
    def toMain(self):
        self.music_player = None
        self.music_timer = None
        self.camera_input.stop()
        self.main_window = Main.App()
        self.main_window.show()
        self.close()
        
    # 初始化音乐列表的方法
    # def init_music_list(self):
    #     self.music_list = read_txt_file("./list/mp3.txt")
    #     self.keys_list = list(self.music_list.keys())
    #     self.value_list = list(self.music_list.values())
    #     self.current_index = 0
    #     if self.music_list:
    #         if self.mp3filepath:
    #             self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.mp3filepath)))
    #         else:
    #             self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile("./mp3/{}.mp3".format(str(self.keys_list[self.current_index])))))
    #     self.list_label = QLabel()
    #     self.main_layout.addWidget(self.list_label, 2, 0, 14, 24)
    #     self.button_scroll = ButtonScroll(self.value_list, self)
    #     self.list_label.setLayout(self.button_scroll.layout())
    #     self.volume_slider.raise_()
        
    # 初始化音乐列表的方法
    def init_music_list(self):
        # 获取music文件夹下的所有文件
        files = os.listdir('./mp3')
        # 遍历所有文件
        for file in files:
            # 如果文件是mp3格式的音乐文件，就把它的路径添加到音乐列表中
            if file.endswith('.mp3'):
                self.name_list.append("    {}    ".format(file))
                self.music_list.append(os.path.join('./mp3', file))
        self.list_label = QLabel()
        self.main_layout.addWidget(self.list_label, 2, 0, 14, 24)
        self.button_scroll = ButtonScroll(self.name_list, self)
        self.list_label.setLayout(self.button_scroll.layout())
        self.volume_slider.raise_()
        
        self.init_music_play()
        if self.music_list:
            self.button_scroll.scrolling_by_outside(self.current_index)
    
    def setMusic(self):
        self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath(self.music_list[self.current_index]))))

    # 如果音乐列表不为空，就随机选择一个音乐文件作为当前播放的音乐
    def init_music_play(self):
        if self.music_list:
            if self.mp3filepath:
                self.current_index = index_of(self.mp3filepath, self.music_list)
            else:
                self.current_index = 0
            # self.button_scroll.scrolling_by_outside(self.current_index)
            self.setMusic()
            self.music_player.play()
    
    # 跳转到指定歌曲
    def jump(self, filename):
        print(os.path.join('./mp3', filename))
        self.mp3filepath = os.path.join('./mp3', filename)
        self.init_music_play()
        
    
    # 连接信号和槽的方法
    def connect_slots(self):
        # 连接播放按钮的点击信号和播放或暂停音乐的槽函数
        self.play_btn.clicked.connect(self.play_or_pause)
        # 连接上一首按钮的点击信号和播放上一首音乐的槽函数
        self.prev_btn.clicked.connect(self.play_prev)
        # 连接下一首按钮的点击信号和播放下一首音乐的槽函数
        self.next_btn.clicked.connect(self.play_next)
        # 连接音量按钮的点击信号和显示或隐藏音量滑动条的槽函数
        self.volume_btn.clicked.connect(self.show_or_hide_volume_slider)
        # 连接音量滑动条的值改变信号和设置音量的槽函数
        self.volume_slider.valueChanged.connect(self.set_volume)
        # 连接进度滑动条的值改变信号和设置播放位置的槽函数
        self.slider.valueChanged.connect(self.set_position)
        # 连接媒体播放器的状态改变信号和更新播放按钮的槽函数
        self.music_player.stateChanged.connect(self.update_play_btn)
        # 连接媒体播放器的播放位置改变信号和更新进度滑动条的槽函数
        self.music_player.positionChanged.connect(self.update_slider)
        # 连接媒体播放器的媒体状态改变信号和检查是否播放完毕的槽函数
        self.music_player.mediaStatusChanged.connect(self.check_end)
        # 连接定时器的超时信号和更新唱片旋转角度的槽函数
        # self.music_timer.timeout.connect(self.update_angle)
        # 连接刷新按钮的点击信号和刷新音乐的槽函数
        self.refresh_btn.clicked.connect(self.refresh_music)
        self.upmp3_btn.clicked.connect(self.uploadMp3File)
        # 连接上传按钮的点击信号和上传背景图片的槽函数
        # self.upload_btn.clicked.connect(self.upload_background)
        # 连接HandDetector对象的timer对象的timeout信号和一个自定义的槽函数，用于在每次获取摄像头的图像时，判断手势并控制音乐播放器的播放
        # self.hand_detector.timer.timeout.connect(self.gesture_control)
    
    # 播放或暂停音乐的槽函数
    def play_or_pause(self):
        # 如果媒体播放器的状态是播放中，就暂停播放
        if self.music_player.state() == QMediaPlayer.PlayingState:
            self.music_player.pause()
        # 否则，就开始播放
        else:
            self.music_player.play()
    
    # 播放上一首音乐的槽函数
    def play_prev(self):
        # 如果音乐列表不为空，就计算上一首音乐的索引
        # self.current_index = (self.current_index + len(self.keys_list) - 1) % len(self.keys_list)
        # self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile("./mp3/{}.mp3".format(str(self.keys_list[self.current_index])))))
        # self.music_player.play()
        if len(self.music_list) > 1:
            self.current_index = (self.current_index - 1) % len(self.music_list)
            # 设置媒体播放器的媒体内容为上一首音乐的路径
            self.setMusic()
            self.button_scroll.scrolling_by_outside(self.current_index)
            # 开始播放
            self.music_player.play()
    
    # 播放下一首音乐的槽函数
    def play_next(self):
        # 如果音乐列表不为空，就计算下一首音乐的索引
        # self.current_index = (self.current_index + 1) % len(self.keys_list)
        # self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile("./mp3/{}.mp3".format(str(self.keys_list[self.current_index])))))
        # self.music_player.play()
        if len(self.music_list) > 1:
            self.current_index = (self.current_index + 1) % len(self.music_list)
            # 设置媒体播放器的媒体内容为下一首音乐的路径
            self.setMusic()
            self.button_scroll.scrolling_by_outside(self.current_index)
            # 开始播放
            self.music_player.play()
    
    # 显示或隐藏音量滑动条的槽函数
    def show_or_hide_volume_slider(self):
        # 如果音量滑动条是可见的，就隐藏它
        if self.volume_slider.isVisible():
            self.volume_slider.setVisible(False)
        # 否则，就显示它，并把它的位置设置为音量按钮的正上方
        else:
            self.volume_slider.setVisible(True)
            # self.volume_slider.move(self.volume_btn.x(), self.volume_btn.y() - self.volume_slider.height())
    
    def mousePressEvent(self, event):
        if (event.x() < self.volume_slider.x() or
            event.y() < self.volume_slider.y() or
            event.x() > self.volume_slider.x() + self.volume_slider.width() or
            event.y() > self.volume_slider.y() + self.volume_slider.height()):
            self.volume_slider.setVisible(False)
    
    # 设置音量的槽函数
    def set_volume(self, value):
        # 设置媒体播放器的音量为滑动条的值
        self.music_player.setVolume(value)
    
    # 设置播放位置的槽函数
    # def set_position(self, value):
    #     # 设置媒体播放器的播放位置为滑动条的值乘以媒体播放器的总时长除以100
    #     self.music_player.setPosition(value * self.music_player.duration() / 100)
    def set_position(self, value):
    # 如果进度滑动条被用户释放，就设置媒体播放器的播放位置为滑动条的值乘以媒体播放器的总时长除以100
        if self.slider.isSliderDown():
            self.music_player.setPosition(value * self.music_player.duration() / 100)
    
    # 更新播放按钮的槽函数
    def update_play_btn(self, state):
        # 如果媒体播放器的状态是播放中，就把播放按钮的图片和提示文本改为暂停
        if state == QMediaPlayer.PlayingState:
            self.play_btn.setIcon(QIcon('images/pause.svg'))
            self.play_btn.setToolTip('暂停')
            # 启动定时器，每隔10毫秒触发一次
            self.music_timer.start(10)
        # 否则，就把播放按钮的图片和提示文本改为播放
        else:
            self.play_btn.setIcon(QIcon('images/play.svg'))
            self.play_btn.setToolTip('播放')
            # 停止定时器
            self.music_timer.stop()
    
    # 更新进度滑动条的槽函数
    def update_slider(self, position):
        # 如果媒体播放器的总时长不为0，就把进度滑动条的值设置为媒体播放器的播放位置除以媒体播放器的总时长乘以100
        if self.music_player.duration() != 0:
            self.slider.setValue(position * 100 / self.music_player.duration())
    
    # 检查是否播放完毕的槽函数
    def check_end(self, status):
        # 如果媒体播放器的媒体状态是已结束，就播放下一首音乐
        if status == QMediaPlayer.EndOfMedia:
            self.play_next()
        # 否则，什么也不做
        else:
            pass
    
    # 更新唱片旋转角度的槽函数
    def update_angle(self):
        # 把唱片的旋转角度增加1度
        self.angle += 1
        # 如果旋转角度大于等于360度，就把它减去360度
        if self.angle >= 360:
            self.angle -= 360
         # 获取cd_icon的中心点
        dx, dy = self.cd_icon.width() / 2, self.cd_icon.height() / 2
        # 创建一个变换对象，用于旋转唱片
        transform = QTransform()
        # 将cd_icon的中心点移动到原点
        transform.translate(-dx, -dy)
        # 旋转
        transform.rotate(self.angle)
        # 将cd_icon的中心点移动回原来的位置
        transform.translate(dx, dy)
        self.cd.setPixmap(self.cd_icon.transformed(transform))
    
    # # 重写关闭事件的方法
    # def closeEvent(self, event):
    #     # 弹出一个消息框，询问用户是否确定退出
    #     reply = QMessageBox.question(self, '退出', '你确定要退出吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     # 如果用户选择是，就接受关闭事件
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     # 否则，就忽略关闭事件
    #     else:
    #         event.ignore()
            
    # 刷新音乐的槽函数
    def refresh_music(self):
        # 设置媒体播放器的播放位置为0
        self.music_player.setPosition(0)
        # 开始播放
        self.music_player.play()
        
    # 上传背景图片的槽函数
    def upload_background(self):
        # 弹出一个文件对话框，让用户选择一个图片文件
        file_name, _ = QFileDialog.getOpenFileName(self, '选择图片', '', '图片文件 (*.svg *.jpg *.bmp)')
        # 如果用户选择了一个文件，就把背景图片的图片设置为用户选择的图片，并且把图片的大小设置为标签的大小
        if file_name:
            self.background.setPixmap(QPixmap(file_name).scaled(self.background.width(), self.background.height()))
            self.background.setWindowOpacity(0.1)
            # 将用户选择的图片保存到images/background文件夹下，文件名为background.svg
            self.background.pixmap().toImage().save('images/background/background.svg')
    
    def change_new_song_position(self, index):
        temp = self.name_list[0]
        self.name_list[0] = self.name_list[index]
        self.name_list[index] = temp
        
        temp = self.music_list[0]
        self.music_list[0] = self.music_list[index]
        self.music_list[index] = temp
            
    def uploadMp3File(self):
        fname, _ = QFileDialog.getOpenFileName(self, f'选择mp3文件', '', f'mp3文件 (*.mp3)')
        # num = str(getMaxMp3Num())
        if fname:
            # 获取文件名
            filename = os.path.basename(fname)
            if not os.path.exists(f'mp3'):
                os.makedirs(f'mp3')
            # 将文件移动到mp3文件夹下
            # filepath = os.path.join(f'mp3', f"{num}.mp3")
            filepath = os.path.join(f'./mp3', f"{filename}")
            # mp3Exist, mp3Index = search_song_in_file("./list/mp3.txt", filename)
            # if mp3Exist:
                # return os.path.join(f'mp3', f"{mp3Index}.mp3")
            if os.path.exists(filepath):
                index = index_of("    {}    ".format(filename), self.name_list)
                self.button_scroll.change_new_song_position(index)
                self.change_new_song_position(index)
                self.mp3filepath = filepath
                self.init_music_play()
                return filepath
            shutil.copy(fname, filepath)
            # append_to_txt_file("./list/mp3.txt", "{}\n{}\n".format(num, filename))
            # addMaxMp3Num()

            self.button_scroll.add_button("    {}    ".format(filename))
            self.name_list.append("    {}    ".format(filename))
            self.music_list.append(filepath)
            self.mp3filepath = filepath
            self.change_new_song_position(len(self.music_list) - 1)
            self.init_music_play()
            
            print(filepath)
            return filepath
        return None
            
    def set_qss(self):
        self.slider.setStyleSheet("""
            QSlider
            {
                background-color: rgba(22, 22, 22, 0.7);
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
                background-color: #FF7826;
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
                background-color: #FF7826;
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
    gui = MusicWindow()
    gui.show()
    sys.exit(app.exec_())