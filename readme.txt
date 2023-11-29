系统使用指南：https://www.cnblogs.com/19373400weileng/p/17864459.html


1、通过main跳转到其他窗口，如music、video、pdf
2、手势识别目前只能传递图像，需要先实现基本功能，后续通过手势检测结果调用基本功能
3、上传文件必须是英文路径
4、图标库参考https://www.iconfont.cn/collections/detail?spm=a313x.user_detail.i1.dc64b3430.545b3a81pe21aV&cid=35162

Gesture.py、Main.py是公有的

Main.py中，定义了toVideo、toPdf的页面跳转办法，只需要修改这两个方法，相应界面可以在这个里面调用上传文件的办法，参考toMusic函数的写法，不过toMusic的逻辑是复制上传的音乐到项目的mp3文件夹下，video和pdf可以考虑不做复制，直接按照路径打开用户选择的文件，注意处理中文路径的问题

Method.py是与界面关系不大的方法，可以提取出来，为了减少冲突，你们的此类方法可以新建VideoMethod.py和PdfMethod.py存放

创建图标按钮时，可以参考Method.py的new_button的方法，保持ui的一致性

pyinstaller Main.py --add-data="D:\python\anaconda\envs\HCI_env\Lib\site-packages\mediapipe\modules;mediapipe/modules" -F -w

python3.8.18
(HCI_env) PS D:\2023yan\课程\人机交互\大作业\ui> conda list
# packages in environment at D:\python\anaconda\envs\HCI_env:
#
# Name                    Version                   Build  Channel
absl-py                   2.0.0                    pypi_0    pypi
attrs                     23.1.0                   pypi_0    pypi
ca-certificates           2023.08.22           haa95532_0    defaults
certifi                   2023.11.17               pypi_0    pypi
cffi                      1.16.0                   pypi_0    pypi
charset-normalizer        3.3.2                    pypi_0    pypi
contourpy                 1.1.1                    pypi_0    pypi
cycler                    0.12.1                   pypi_0    pypi
flatbuffers               23.5.26                  pypi_0    pypi
fonttools                 4.44.3                   pypi_0    pypi
idna                      3.4                      pypi_0    pypi
importlib-resources       6.1.1                    pypi_0    pypi
kiwisolver                1.4.5                    pypi_0    pypi
libffi                    3.4.4                hd77b12b_0    defaults
matplotlib                3.7.4                    pypi_0    pypi
mediapipe                 0.10.8                   pypi_0    pypi
numpy                     1.24.4                   pypi_0    pypi
opencv-contrib-python     4.8.1.78                 pypi_0    pypi
opencv-python             4.8.1.78                 pypi_0    pypi
openssl                   3.0.12               h2bbff1b_0    defaults
packaging                 23.2                     pypi_0    pypi
pillow                    10.1.0                   pypi_0    pypi
pip                       23.3.1                   pypi_0    pypi
protobuf                  3.20.3                   pypi_0    pypi
pyaudio                   0.2.14                   pypi_0    pypi
pycparser                 2.21                     pypi_0    pypi
pyparsing                 3.1.1                    pypi_0    pypi
pyqt5                     5.15.10                  pypi_0    pypi
pyqt5-qt5                 5.15.2                   pypi_0    pypi
pyqt5-sip                 12.13.0                  pypi_0    pypi
python                    3.8.18               h1aa4202_0    defaults
python-dateutil           2.8.2                    pypi_0    pypi
requests                  2.31.0                   pypi_0    pypi
setuptools                68.0.0           py38haa95532_0    defaults
six                       1.16.0                   pypi_0    pypi
sounddevice               0.4.6                    pypi_0    pypi
speechrecognition         3.10.0                   pypi_0    pypi
sqlite                    3.41.2               h2bbff1b_0    defaults
urllib3                   2.1.0                    pypi_0    pypi
vc                        14.2                 h21ff451_1    defaults
vs2015_runtime            14.27.29016          h5e58377_2    defaults
wheel                     0.41.2           py38haa95532_0    defaults
zipp                      3.17.0                   pypi_0    pypi