# -*- coding:utf-8 -*-

import sys
sys.path.append(r'E:\AFCtest\Face\Face_Recognition_Algorithm\人脸特征分析\minions_check_quality_v0.1.0\checkAPI\Minions\\')
from minions_api import detect
import cv2

testIp = 'http://172.16.50.17:9000/'

# Initialize frame size
frame_width = 256
frame_height = 256

def run_api(img_path):

    # step1
    print('\n \n')
    result1 = detect(testIp, img_path)
    print('run api', result1)

    if result1[0] == 'false':
        return 'no face ' + result1[0][1]
    # roll1 = result1[1][33]
    # roll2 = result1[1][35]
    # roll3 = result1[1][37]
    # if abs(roll1)>5 or abs(roll2)>5 or abs(roll3)>5:
    #     return 'roll false'

    return result1


if __name__ == '__main__' :


    capture = cv2.VideoCapture(0)  # 0为电脑内置摄像头


    while (True):
        ret, frame = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。 frame为视频的每一帧图像
        frame = cv2.flip(frame, 1)  # 摄像头是和人对立的，将图像左右调换回来正常显示。
        cv2.imshow("video", frame)
        cv2.imwrite('1.jpg', frame)
        run_api('1.jpg')
        c = cv2.waitKey(50)
        if c == 27:
            break




