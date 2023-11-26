# https://blog.csdn.net/weixin_41747193/article/details/122117629

import cv2 as cv
import numpy as np
import mediapipe as mp
from numpy import linalg
from PyQt5.QtCore import QThread, pyqtSignal
from pynput.mouse import Controller, Button
import time
 
# 新增一个摄像头输入类，继承自QThread
class CameraInput(QThread):
    DEVICE_NUM = 0
    frame_ready = pyqtSignal(np.ndarray)
    stop_flag = False
    gesture_result = None
    def __init__(self):
        super().__init__()
        self.mouse = Controller()
        self.prev_hand_pos = None  # 上一帧的手的位置
        self.mouse_rate = -5.0
        self.DEVICE_NUM = 0
        self.last_click_time = 0  # 上一次点击的时间
        self.move = True
    # 手指检测
    # point1-手掌0点位置，point2-手指尖点位置，point3手指根部点位置
    def finger_stretch_detect(self, point1, point2, point3):
        result = 0
        #计算向量的L2范数
        dist1 = np.linalg.norm((point2 - point1), ord=2)
        dist2 = np.linalg.norm((point3 - point1), ord=2)
        if dist2 > dist1 or (dist2 > dist1 and point2[1] < point3[1]):
            result = 1
        return result

    def detect_hands_gesture(self, result, landmark):
        if (result[0] == 1) and (result[1] == 0) and (result[2] == 0) and (result[3] == 0) and (result[4] == 0):
            gesture = self.gesture_signal_left_and_right(landmark)
        elif (result[0] == 0) and (result[1] == 1)and (result[2] == 0) and (result[3] == 0) and (result[4] == 0):
            gesture = self.gesture_signal_up_and_down(landmark)
        elif (result[0] == 0) and (result[1] == 0)and (result[2] == 1) and (result[3] == 0) and (result[4] == 0):
            gesture = "please civilization in testing"
        elif (result[0] == 0) and (result[1] == 1)and (result[2] == 1) and (result[3] == 0) and (result[4] == 0):
            gesture = "yeah"
        elif (result[0] == 0) and (result[1] == 1)and (result[2] == 1) and (result[3] == 1) and (result[4] == 0):
            gesture = "three"
        elif (result[0] == 0) and (result[1] == 1)and (result[2] == 1) and (result[3] == 1) and (result[4] == 1):
            gesture = "four"
        elif (result[0] == 1) and (result[1] == 1)and (result[2] == 1) and (result[3] == 1) and (result[4] == 1):
            gesture = "open"
        elif (result[0] == 1) and (result[1] == 0)and (result[2] == 0) and (result[3] == 0) and (result[4] == 1):
            gesture = "six"
        elif (result[0] == 0) and (result[1] == 0)and (result[2] == 1) and (result[3] == 1) and (result[4] == 1):
            gesture = "OK"
        elif(result[0] == 0) and (result[1] == 0) and (result[2] == 0) and (result[3] == 0) and (result[4] == 0):
            gesture = "stone"
        else:
            gesture = "not in detect range..."
        return gesture
    
    
    def run(self):
        # 接入USB摄像头时，注意修改cap设备的编号
        self.cap = cv.VideoCapture(self.DEVICE_NUM) 
        # 加载手部检测函数
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        # 加载绘制函数，并设置手部关键点和连接线的形状、颜色
        mpDraw = mp.solutions.drawing_utils
        handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=int(5))
        handConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=int(10))
        
        figure = np.zeros(5)
        landmark = np.empty((21, 2))
    
        if not self.cap.isOpened():
            print("Can not open camera.")
            exit()
    
        while True:
            if self.stop_flag:
                self.cap.release()
                cv.destroyAllWindows()
                break
            ret, frame = self.cap.read()
            if not ret:
                print("Can not receive frame (stream end?). Exiting...")
                break
    
            #mediaPipe的图像要求是RGB，所以此处需要转换图像的格式
            frame_RGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            result = hands.process(frame_RGB)
            #读取视频图像的高和宽
            frame_height = frame.shape[0]
            frame_width  = frame.shape[1]
            
            #print(result.multi_hand_landmarks)
            #如果检测到手
            if result.multi_hand_landmarks:
                #为每个手绘制关键点和连接线
                for i, handLms in enumerate(result.multi_hand_landmarks):
                    mpDraw.draw_landmarks(frame, 
                                        handLms, 
                                        mpHands.HAND_CONNECTIONS,
                                        landmark_drawing_spec=handLmsStyle,
                                        connection_drawing_spec=handConStyle)
    
                    for j, lm in enumerate(handLms.landmark):
                        xPos = int(lm.x * frame_width)
                        yPos = int(lm.y * frame_height)
                        landmark_ = [xPos, yPos]
                        landmark[j,:] = landmark_
    
                    # 通过判断手指尖与手指根部到0位置点的距离判断手指是否伸开(拇指检测到17点的距离)
                    for k in range (5):
                        if k == 0:
                            figure_ = self.finger_stretch_detect(landmark[17],landmark[4*k+2],landmark[4*k+4])
                        else:    
                            figure_ = self.finger_stretch_detect(landmark[0],landmark[4*k+2],landmark[4*k+4])
                        figure[k] = figure_
                    # print(figure,'\n')
    
                    self.gesture_result = self.detect_hands_gesture(figure, landmark)
                    cv.putText(frame, f"{self.gesture_result}", (30, 45 * i + 90), cv.FONT_HERSHEY_COMPLEX, 1.5, (255 ,255, 0), 5)
                    
                    self.do_move(landmark)
                    self.do_click()

            # cv.imshow('frame', frame)
            # 发出一个信号，传递视频帧，用emit方法
            if not self.stop_flag:
                self.frame_ready.emit(frame)
                
    
    def do_click(self):
        if self.gesture_result == "open" and self.move:
            current_time = time.time()
            if current_time - self.last_click_time >= 1:  # 如果距离上一次点击已经过去了1秒
                self.mouse.click(Button.left, 1)  # 模拟左键点击一次
                self.last_click_time = current_time  # 更新上一次点击的时间
                
    def do_move(self, landmark):
        hand_pos = np.mean(landmark, axis=0)
        if self.prev_hand_pos is not None and self.gesture_result == "stone":
            # 计算手的移动距离和方向
            hand_movement = hand_pos - self.prev_hand_pos
            # 将手的移动应用到鼠标上
            self.mouse.move(self.mouse_rate * hand_movement[0], (-1) * self.mouse_rate * hand_movement[1])
        # 保存这一帧的手的位置，以便在下一帧中使用
        self.prev_hand_pos = hand_pos
    
    def gesture_signal_left_and_right(self, landmarks):
        thumb_tip = landmarks[4]
        thumb_base = landmarks[2]
        
        if thumb_tip[0] < thumb_base[0]:
            return "right"
        else:
            return "left"
        
    def gesture_signal_up_and_down(self, landmarks):
        index_tip = landmarks[8]
        index_base = landmarks[6]
        
        if index_tip[1] < index_base[1]:
            return "up"
        else:
            return "down"
                
    def stop(self):
        self.stop_flag = True
 
# if __name__ == '__main__':
    