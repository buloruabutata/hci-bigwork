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
import time


class PdfWindow(QMainWindow):
    def __init__(self, pdffilepath=r"D:\2023yan\课程\人机交互\大作业说明\大作业说明\人机交互_大作业_20231102a_print.pdf"):
        super().__init__()
        self.pdffilepath = pdffilepath
        self.main_UI()
        self.pdf_UI()
        self.camera_UI()
        self.last_time = 0
        # 0休眠 1默认 2鼠标
        self.cur_status = 2
        self.camera_input.move = True
        # self.initUI()
        
        
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
        self.camera_label.setPixmap(pixmap)
        
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
        self.update_gesture_label()
        time_rate = 0.5
        if self.zoom == 1:
            time_rate = 2
        if self.cur_status == 1 and curtime - self.last_time > time_rate:
            if self.camera_input.gesture_result == "up":
                self.zoom_up()
                self.last_time = curtime
                return 
            if self.camera_input.gesture_result == "down":
                self.zoom_down()
                self.last_time = curtime
                return

        if self.cur_status == 1 and curtime - self.last_time > 3:
            if self.camera_input.gesture_result == "left":
                self.go_prev_page()
                self.last_time = curtime
                return
            if self.camera_input.gesture_result == "right":
                self.go_next_page()
                self.last_time = curtime
                return
            # if self.camera_input.gesture_result == "stone":
            #     self.play_or_pause()
            #     self.last_time = curtime
            if self.camera_input.gesture_result == "ok":
                self.refresh_pdf()
                self.last_time = curtime
                return
        

    
    def update_gesture_label(self):
        if self.cur_status == 1:
            if self.camera_input.gesture_result == "up":
                self.gesture_usage.setText("放大")
                return 
            if self.camera_input.gesture_result == "down":
                self.gesture_usage.setText("缩小")
                return

        if self.cur_status == 1:
            if self.camera_input.gesture_result == "left":
                self.gesture_usage.setText("上一页")
                return
            if self.camera_input.gesture_result == "right":
                self.gesture_usage.setText("下一页")
                return
            # if self.camera_input.gesture_result == "stone":
            #     self.play_or_pause()
            #     self.last_time = curtime
            if self.camera_input.gesture_result == "ok":
                self.gesture_usage.setText("保持/适配纵横比")
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
        self.setFixedSize(1920, 1000)
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
                self.main_layout.addWidget(QLabel(f""), i, j) # 不显示坐标，只添加空的QLabel
                if i == 0:
                    self.main_layout.setColumnMinimumWidth(j, 100)
        # 将窗口加入布局
        self.main_wight.setLayout(self.main_layout)
        # 将这个主窗口设置成窗口主部件
        self.setCentralWidget(self.main_wight)
        # 创建
        self.help_btn = new_button('./images/help.svg', 100, 100, '帮助')
        self.main_btn = new_button('./images/home.svg', 100, 100, '首页')
        self.exit_btn = new_button('./images/exit.svg', 100, 100, '退出')
        self.exit_btn.clicked.connect(self.close_self)
        self.status_label = StatusQLabel(400, 100, self)
        # 定位
        self.main_layout.addWidget(self.main_btn, 0, 24, 4, 4)
        self.main_layout.addWidget(self.help_btn, 0, 27, 4, 4)
        self.main_layout.addWidget(self.exit_btn, 0, 30, 4, 4)
        self.main_layout.addWidget(self.status_label, 5, 25, 8, 8)
        # 链接到方法
        self.help_btn.clicked.connect(lambda: open_help("https://www.bing.com"))
        self.main_btn.clicked.connect(self.toMain)
        self.exit_btn.clicked.connect(self.close_self)
        
        self.gesture_label = new_text_label("当前手势功能：", 200, 50)
        self.main_layout.addWidget(self.gesture_label, 3, 25, 8, 8)
        self.gesture_usage = new_text_label("无", 200, 50)
        self.main_layout.addWidget(self.gesture_usage, 3, 29, 8, 8)
        
    def refresh_pdf(self):
        # 设置媒体播放器的播放位置为0
        self.keep = not self.keep
        self.clearLayout()
        self.renderPage()
        
    def close_self(self):
        self.close()
        
    def toMain(self):
        self.camera_input.stop()
        self.main_window = Main.App()
        self.main_window.show()
        self.close()
        
    def pdf_UI(self):
        self.next_page_btn = new_button('./images/next.svg', 100, 100, '下一页(👍right)')
        self.prev_page_btn = new_button('./images/prev.svg', 100, 100, '上一页(👍left)')
        # 定位
        self.main_layout.addWidget(self.prev_page_btn, 16, 1, 4, 2)
        self.main_layout.addWidget(self.next_page_btn, 16, 5, 4, 2)
        # 链接到方法
        self.next_page_btn.clicked.connect(self.go_next_page)
        self.prev_page_btn.clicked.connect(self.go_prev_page)

        self.zoom_down_btn = new_button('./images/small.svg', 100, 100, '缩小(👇)')
        self.zoom_up_btn = new_button('./images/big.svg', 100, 100, '放大(👆)')
        self.refresh_btn = new_button('images/return.svg', 100, 100, '保持/适配纵横比(👌ok)')
        self.uppdf_btn = new_button('images/upload.svg', 100, 100, '上传')
        # 定位
        self.main_layout.addWidget(self.zoom_up_btn, 16, 9, 4, 2)
        self.main_layout.addWidget(self.zoom_down_btn, 16, 13, 4, 2)
        self.main_layout.addWidget(self.refresh_btn, 16, 17, 4, 2)
        self.main_layout.addWidget(self.uppdf_btn, 16, 21, 4, 2)
        self.uppdf_btn.clicked.connect(self.uploadFile)
        # 链接到方法
        self.zoom_up_btn.clicked.connect(self.zoom_up)
        self.zoom_down_btn.clicked.connect(self.zoom_down)
        self.refresh_btn.clicked.connect(self.refresh_pdf)
        self.set_qss()

        self.title = Path(self.pdffilepath).stem # get name of the file, preferred because metadata['title'] is not often available
        self.doc = fitz.open(self.pdffilepath) # open the given file
        self.metadata = self.doc.metadata
        self.current_page = 0
        self.zoom = 1
        self.xpdf = 1400
        self.ypdf = 860
        self.keep = True
        self.renderPage()
    
    def set_qss(self):
        #B0E0E6
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.main_wight.setStyleSheet("""QWidget {background-color: #d3e6ef;}""")
        
    def uploadFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, f'选择pdf文件', '', f'pdf文件 (*.pdf)')
        if fname:
            self.pdffilepath = os.path.abspath(fname)
            self.doc = fitz.open(self.pdffilepath) # open the given file
            self.current_page = 0
            self.clearLayout()
            self.renderPage()


    def clearLayout(self):
        self.main_layout.removeWidget(self.label)
        self.update()


    def renderPage(self):
        page = self.doc[self.current_page]
        zoom_x = self.xpdf / page.rect.width  # horizontal zoom
        zoom_y = self.ypdf / page.rect.height  # vertical zoom
        if self.keep:
            zoom_x = min(zoom_x, zoom_y)  # choose the smaller zoom factor
            zoom_y = min(zoom_x, zoom_y)  # choose the smaller zoom factor
        mat = fitz.Matrix(zoom_x * self.zoom, zoom_y * self.zoom)  # zoom factor in each dimension
        pix = page.get_pixmap(matrix=mat)
        fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
        pixmap = QPixmap.fromImage(img)

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.setFixedSize(self.xpdf, self.ypdf)
        self.label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label, 0, 0, 15, 24)

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


    def go_next_page(self):
        if self.current_page < self.doc.page_count - 1:
            self.current_page += 1
            self.clearLayout()
            self.renderPage()


    def go_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.clearLayout()
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
        self.current_page = number
        self.renderPage()


    def quit(self):
        '''Store current page number and quit.'''

        self.saveToFile("current_page", self.current_page)
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