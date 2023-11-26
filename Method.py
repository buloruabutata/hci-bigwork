
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

def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1

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
    
    def text_change(self):
        return self.original_text[4:-4]
    
    def set_original_text(self, text):
        self.original_text = text
        self.setText(self.original_text)

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
        self.vlayout = QVBoxLayout()

        # Create buttons and add them to the layout
        self.buttons = []
        for text in self.button_texts:
            button = ScrollingButton(text, self)
            # button.setStyleSheet('QPushButton {min-height: 50px; border: none;}')
            button.clicked.connect(self.start_stop_scrolling)  # Connect the button's clicked signal to a new slot
            self.vlayout.addWidget(button)
            self.buttons.append(button)
            spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
            self.vlayout.addItem(spacer)

        # Add a stretch at the end of the layout
        self.vlayout.addStretch(1)
        
        # Create a scroll area and set the layout
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        widget = QWidget()
        widget.setLayout(self.vlayout)
        self.scroll_area.setWidget(widget)

        # Add the scroll area to the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)
        
        self.cur = None
        
    def change_new_song_position(self, index): 
        self.scrolling_by_outside(index)
        temp = self.buttons[0].original_text
        self.buttons[0].set_original_text(self.buttons[index].original_text)
        self.buttons[index].set_original_text(temp)
        self.scroll_area.verticalScrollBar().setValue(0)
        self.scrolling_by_outside(0)
    
    def add_button(self, text):
        # Remove the stretch
        self.vlayout.takeAt(self.vlayout.count() - 1)
        button = ScrollingButton(text, self)
        # temp = self.buttons[0]
        button.clicked.connect(self.start_stop_scrolling)  # Connect the button's clicked signal to a new slot
        self.vlayout.addWidget(button)
        self.buttons.append(button)
        
        self.change_new_song_position(len(self.buttons) - 1)
        
        # Add the stretch back
        self.vlayout.addStretch(1)
        # print(self.scroll_area.verticalScrollBar().maximum())
        # self.scroll_area.verticalScrollBar().setValue(0)
        # self.ensure_button_visible(-1)
        
    # def ensure_button_visible(self, buttonIndex):
    #     if buttonIndex == -1:
    #         buttonIndex = len(self.buttons) - 1
        # self.scroll_area.ensureWidgetVisible(self.buttons[buttonIndex])
        # self.scroll_area.verticalScrollBar().maximum()
        # self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
        
    def start_stop_scrolling(self):
        button = self.sender()
        self.parent.jump(button.text_change())
        # if self.current_scrolling_button is not None and self.current_scrolling_button != button:
        if self.current_scrolling_button is not None:
            self.current_scrolling_button.start_stop_scrolling()
        # self.current_scrolling_button = button if self.current_scrolling_button != button else None
        self.current_scrolling_button = button
    
    def scrolling_by_outside(self, index):
        button = self.buttons[index]
        if self.current_scrolling_button is not None and self.current_scrolling_button != button:
            self.current_scrolling_button.start_stop_scrolling()
        self.current_scrolling_button = button
        self.current_scrolling_button.start_stop_scrolling()
        
    # def scrolling_by_outside_click(self, index):
    #     button = self.buttons[index]
    #     if self.current_scrolling_button is not None and self.current_scrolling_button != button:
    #         self.current_scrolling_button.start_stop_scrolling()
    #     self.current_scrolling_button = button


if __name__ == "__main__":
    print(search_song_in_file("./list/mp3.txt", "Jack Stauber - buttercup.mp3"))
