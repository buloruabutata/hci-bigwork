import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import Music
import Video
import Pdf
import time
import os
from Method import *
from Gesture import CameraInput

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_UI()
        self.button_UI()
        self.camera_UI()
        
        self.last_time = 0
        # 0休眠 1默认 2鼠标
        self.cur_status = 0
    
    def camera_UI(self):
        self.status_label = MainStatusQLabel(400, 100, self)
        self.main_layout.addWidget(self.status_label, 5, 27, 8, 8)
        self.gesture_label = new_text_label("当前手势功能：", 150, 50)
        self.main_layout.addWidget(self.gesture_label, 3, 27, 8, 8)
        self.gesture_usage = new_text_label("无", 150, 50)
        self.main_layout.addWidget(self.gesture_usage, 3, 30, 8, 8)
        self.camera_label = QLabel()
        # self.camera_label.setFixedSize(400, 400)
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
            if self.cur_status == 1:
                self.camera_input.move = True
            else:
                self.camera_input.move = False
            self.last_time = curtime
            return 
    
    def update_gesture_label(self):
        if self.cur_status == 1:
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
        # 创建一个9*16的网格布局
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
        self.title = QLabel("请选择展示的媒体文件")
        self.title.setFont(QFont("微软雅黑", 25, QFont.Bold))
        # self.title.setStyleSheet("color: red")
        self.title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title, 0, 12, 4, 7)
        
        self.set_qss()
        
 
    def button_UI(self):
        # 设置几个按钮用做调用其他窗口
        self.music_btn = new_text_button("进入音乐(mp3)播放界面", 400, 100, "上传mp3音乐文件")
        self.video_btn = new_text_button("进入视频(mp4)播放界面", 400, 100, "上传mp4视频文件")
        self.pdf_btn = new_text_button("进入pdf播放界面", 400, 100, "上传pdf文件")
        
        self.help_btn = new_button('./images/help.svg', 100, 100, '帮助')
        self.exit_btn = new_button('./images/exit.svg', 100, 100, '退出')
        self.help_btn.clicked.connect(lambda: open_help("https://www.cnblogs.com/19373400weileng/p/17864459.html"))
        self.exit_btn.clicked.connect(self.close_self)
        
        # 将按钮加入布局
        self.main_layout.addWidget(self. music_btn, 4, 12, 4, 8)
        self.main_layout.addWidget(self.video_btn, 8, 12, 4, 8)
        self.main_layout.addWidget(self.pdf_btn, 12, 12, 4, 8)
        self.main_layout.addWidget(self.help_btn, 0, 24, 4, 4)
        self.main_layout.addWidget(self.exit_btn, 0, 28, 4, 4)
        
        self.music_btn.clicked.connect(self.toMusic)
        self.video_btn.clicked.connect(self.toVideo)
        self.pdf_btn.clicked.connect(self.toPdf)
 
    def toMusic(self):
        if len(os.listdir("./mp3")) == 0:
            mp3filepath = self.uploadMp3File("mp3")
            if mp3filepath:
                self.camera_input.stop()
                self.music_window = Music.MusicWindow(mp3filepath)
                self.music_window.show()
                self.close()
        else:
            self.music_window = Music.MusicWindow()
            self.music_window.show()
            self.close()
    
    def toVideo(self):
        filepath = self.uploadFile("mp4")
        if filepath:
            self.camera_input.stop()
            self.video_window = Video.VideoWindow(filepath)
            self.video_window.show()
            self.close()
        
    def toPdf(self):
        filepath = self.uploadFile("pdf")
        if filepath:
            self.camera_input.stop()
            self.pdf_window = Pdf.PdfWindow(filepath)
            self.pdf_window.show()
            self.close()
        
    def uploadFile(self, type="mp3"):
        fname, _ = QFileDialog.getOpenFileName(self, f'选择{type}文件', '', f'{type}文件 (*.{type})')
        if fname:
            # 获取文件名
            return os.path.abspath(fname)
        return None
    
    def uploadMp3File(self, type="mp3"):
        fname, _ = QFileDialog.getOpenFileName(self, f'选择{type}文件', '', f'{type}文件 (*.{type})')
        # num = str(getMaxMp3Num())
        if fname:
            # 获取文件名
            filename = os.path.basename(fname)
            if not os.path.exists(f'{type}'):
                os.makedirs(f'{type}')
            # 将文件移动到mp3文件夹下
            # filepath = os.path.join(f'{type}', f"{num}.mp3")
            filepath = os.path.join(f'./{type}', f"{filename}")
            # mp3Exist, mp3Index = search_song_in_file("./list/mp3.txt", filename)
            # if mp3Exist:
                # return os.path.join(f'{type}', f"{mp3Index}.mp3")
            if os.path.exists(filepath):
                return filepath
            shutil.copy(fname, filepath)
            # append_to_txt_file("./list/mp3.txt", "{}\n{}\n".format(num, filename))
            # addMaxMp3Num()
            return filepath
        return None

    def close_self(self):
        sys.exit()

    def set_qss(self):
        #B0E0E6
        self.main_wight.setStyleSheet("""QWidget {background-color: #d3e6ef;}""")
        # self.setWindowFlag(Qt.FramelessWindowHint)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = App()
    gui.show()
    sys.exit(app.exec_())