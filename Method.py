
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

