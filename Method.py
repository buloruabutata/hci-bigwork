
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def new_button(path, width, height, tip):
    btn = QPushButton()
    btn.setIcon(QIcon(path))
    btn.setIconSize(QSize(width / 2, height / 2))
    btn.setFixedSize(width, height)
    btn.setToolTip(tip)
    return btn

def open_help(url):
    # 使用QDesktopServices.openUrl方法打开网址
    QDesktopServices.openUrl(QUrl(url))


def getMaxMp3Num():
    # 读取文件内容
    with open('./list/mp3num.txt', 'r') as f:
        return int(f.read().strip())

def addMaxMp3Num():
    with open('./list/mp3num.txt', 'r') as f:
        num = int(f.read().strip())
    # 将数字加1
    num += 1
    # 将新数字写回文件
    with open('./list/mp3num.txt', 'w') as f:
        f.write(str(num))
        
def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]
    lines = [int(line) if line.isdigit() else line for line in lines]
    return dict(zip(lines[::2], lines[1::2]))

def append_to_txt_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(content)
        
def search_song_in_file(file_path, song_name):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for i in range(0, len(lines), 2):
        if song_name in lines[i+1]:
            return True, lines[i]
    return False, None

class ScrollingButton(QPushButton):
    def __init__(self, text, parent=None):
        super(ScrollingButton, self).__init__(text, parent)
        self.original_text = text
        self.setStyleSheet('QPushButton {min-height: 50px; border: none;}')
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.clicked.connect(self.start_stop_scrolling)
        self.installEventFilter(self)

    def start_stop_scrolling(self):
        if self.timer.isActive():
            self.timer.stop()
            self.setText(self.original_text)
            self.setStyleSheet('QPushButton {min-height: 50px; border: none;}')
        else:
            self.timer.start(200)
            self.setStyleSheet('QPushButton {background-color: blue; color: white; border: none; min-height: 50px;}')

    def update_text(self):
        current_text = self.text()
        self.setText(current_text[1:] + current_text[0])
        
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            self.setStyleSheet('QPushButton {background-color: blue; color: white; border: none; min-height: 50px;}')
        elif event.type() == QEvent.Leave:
            if not self.timer.isActive():
                self.setStyleSheet('QPushButton {min-height: 50px; border: none;}')
        return super().eventFilter(obj, event)

class ButtonScroll(QWidget):
    def __init__(self, button_texts, parent):
        super().__init__()
        self.button_texts = button_texts
        self.parent = parent
        self.current_scrolling_button = None  # Add a variable to track the current scrolling button
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Button Scroll')
        self.setGeometry(100, 100, 300, 400)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create buttons and add them to the layout
        self.buttons = []
        for text in self.button_texts:
            button = ScrollingButton(text, self)
            # button.setStyleSheet('QPushButton {min-height: 50px; border: none;}')
            button.clicked.connect(self.start_stop_scrolling)  # Connect the button's clicked signal to a new slot
            layout.addWidget(button)
            self.buttons.append(button)

        # Create a scroll area and set the layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        widget = QWidget()
        widget.setLayout(layout)
        scroll_area.setWidget(widget)

        # Add the scroll area to the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        
        self.cur = None
        
    def start_stop_scrolling(self):
        button = self.sender()
        self.parent.jump()
        if self.current_scrolling_button is not None and self.current_scrolling_button != button:
            self.current_scrolling_button.start_stop_scrolling()
        self.current_scrolling_button = button if self.current_scrolling_button != button else None


if __name__ == "__main__":
    print(search_song_in_file("./list/mp3.txt", "Jack Stauber - buttercup.mp3"))
