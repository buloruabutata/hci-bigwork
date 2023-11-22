from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import Music
import Video
import Pdf
import os
from Method import *

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_UI()
        self.button_UI()
 
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
        # 创建一个9*16的网格布局
        for i in range(9):
            for j in range(16):
                self.main_layout.addWidget(QLabel(f"({i},{j})"), i, j) # 不显示坐标，只添加空的QLabel
        # 将窗口加入布局
        self.main_wight.setLayout(self.main_layout)
        # 将这个主窗口设置成窗口主部件
        self.setCentralWidget(self.main_wight)
        self.title = QLabel("请上传需要展示的媒体文件")
        self.title.setFont(QFont("微软雅黑", 25, QFont.Bold))
        # self.title.setStyleSheet("color: red")
        self.title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title, 0, 6, 2, 4)
 
    def button_UI(self):
        # 设置几个按钮用做调用其他窗口
        self.music_btn = QPushButton("上传mp3音乐文件")
        self.music_btn.setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.music_btn.setFixedSize(400, 100)
        self.video_btn = QPushButton("上传mp4视频文件")
        self.video_btn.setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.video_btn.setFixedSize(400, 100)
        self.pdf_btn = QPushButton("上传pdf文件")
        self.pdf_btn.setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.pdf_btn.setFixedSize(400, 100)
        self.help_btn = QPushButton()
        
        self.help_btn = new_button('./images/help.svg', 100, 100, '帮助')
        self.help_btn.clicked.connect(lambda: open_help("https://www.bing.com"))
        
        self.pdf_btn = QPushButton("上传pdf文件")
        self.pdf_btn.setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.pdf_btn.setFixedSize(400, 100)
        
        # 将按钮加入布局
        self.main_layout.addWidget(self. music_btn, 2, 6, 2, 4)
        self.main_layout.addWidget(self.video_btn, 4, 6, 2, 4)
        self.main_layout.addWidget(self.pdf_btn, 6, 6, 2, 4)
        self.main_layout.addWidget(self.help_btn, 0, 14, 2, 2)
        
        self.music_btn.clicked.connect(self.toMusic)
        self.video_btn.clicked.connect(self.toVideo)
        self.pdf_btn.clicked.connect(self.toPdf)
 
    def toMusic(self):
        mp3filepath = self.uploadFile("mp3")
        if mp3filepath:
            self.music_window = Music.MusicWindow(mp3filepath)
            self.music_window.show()
            self.close()
    
    def toVideo(self):
        self.video_window = Video.VideoWindow()
        self.video_window.show()
        self.close()
        
    def toPdf(self):
        self.pdf_window = Pdf.PdfWindow()
        self.pdf_window.show()
        self.close()
        
    def uploadFile(self, type="mp3"):
        fname, _ = QFileDialog.getOpenFileName(self, f'选择{type}文件', '', f'{type}文件 (*.{type})')
        if fname:
            # 获取文件名
            filename = os.path.basename(fname)
            if not os.path.exists(f'{type}'):
                os.makedirs(f'{type}')
            # 将文件移动到musics文件夹下
            filepath = os.path.join(f'{type}', filename)
            if os.path.exists(filepath):
                os.remove(filepath)
            os.rename(fname, filepath)
            return filepath
        return None
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = App()
    gui.show()
    sys.exit(app.exec_())