import os.path
from tkinter import *
import cv2
from PIL import Image, ImageTk, ImageFont,ImageDraw
from tkinter.ttk import Separator
import numpy as np
import time
import sys
sys.path.append(r'E:\AFCtest\Face\Face_Recognition_Algorithm\人脸特征分析\minions_check_quality_v0.1.0\checkAPI\Minions\\')
from minions_api import detect

from deepface import DeepFace
import io
import dlib


testIp = 'http://172.16.50.17:9000/'
detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor(r"E:\AFCtest\Face\Face_Recognition_Algorithm\model/shape_predictor_68_face_landmarks.dat")

def image2byte(image):
    '''
    图片转byte
    image: 必须是PIL格式
    image_bytes: 二进制
    '''
    # 创建一个字节流管道
    img_bytes = io.BytesIO()
    # 将图片数据存入字节流管道， format可以按照具体文件的格式填写
    image.save(img_bytes, format="png")
    # 从字节流管道中获取二进制
    image_bytes = img_bytes.getvalue()
    return image_bytes


def run_api(img_path):

    result1 = detect(testIp, img_path)
    #print (result1)
    return result1


def show_res (result):
    global select_type

    if select_type is None:
        return ""

    saved = False
    detect_res = ''
    #print (select_type)
    if '遮挡检测' in select_type:
        if result[0] == 'false' and result[1] in ['口罩遮挡','左眼遮挡','右眼遮挡']:
            detect_res = result[1]  # 口罩遮挡  左眼遮挡  右眼遮挡
            saved = True

    if '旋转角度' in select_type:
        if result[0] == 'false' and '头部' in result[1]:
            detect_res = result[1]  # 头部旋转/俯仰/侧倾角度超过规定范围
            saved = True

    if '光照检测' in select_type:
        if result[0] == 'false' and '曝光' in result[1]:
            detect_res = result[1]
            saved = True

    if '模糊检测' in select_type:
        if result[0] == 'false' and '模糊' in result[1]:
            detect_res = result[1]
            saved = True

    return detect_res, saved


def video_feat_show(cv2image):
    gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    for i in range(len(rects)):
        cv2.rectangle(cv2image, (rects[i].left(), rects[i].top()), (rects[i].right(), rects[i].bottom()),
                      (0, 255, 0), 2)
        

        landmarks = np.matrix([[p.x, p.y] for p in predictor(cv2image, rects[i]).parts()])
        for idx, point in enumerate(landmarks):
            pos = (point[0, 0], point[0, 1])
            cv2.circle(cv2image, pos, 1, color=(0, 255, 0))

    return cv2image



def video_loop():

    global detect_res
    global face_feat
    global color

    idx = 0
    video_cnt = 0
    gender_res = ''
    age_res = ''
    show_idx = 0
    saved_flag = False
    while camera.isOpened():
        success, img = camera.read()  # 从摄像头读取照片
        if success:
            cv2image = cv2.flip(img, 1)  # 摄像头是和人对立的，将图像左右调换回来正常显示。

            if face_feat :
                cv2image = video_feat_show(cv2image)

            if not saved_flag:
                color = 'green'

            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            current_image = Image.fromarray(cv2image)  # 将图像转换成Image对象
            current_image = current_image.resize((400, 300),Image.NEAREST)

            draw = ImageDraw.Draw(current_image)
            draw.text((10, 10), detect_res, font=ImageFont.truetype("./simhei.ttf",20), fill=(255, 0, 0))
            draw.rectangle(((317, 244), (380, 270)), fill=None, outline='black', width=18)
            draw.text((320, 250), '女性 25', font=ImageFont.truetype("./simhei.ttf", 15), fill=(255, 255, 255))

            draw.rectangle(((0, 0), (400, 300)), fill=None, outline=color, width=8)
            imgtk = ImageTk.PhotoImage(image=current_image)
            panel.imgtk = imgtk
            panel.config(image=imgtk)
            panel.update()


            # if not face_feat and video_cnt % 117 == 0:
            #     img_send = current_image.resize((200, 200), Image.NEAREST)
            #     start = time.time()
            #     demography = DeepFace.analyze(np.array(img_send)[:, :, 0:3], actions=['age', 'gender'],
            #                                   enforce_detection=False, models=models, detector_backend=backends[0])
            #     age_res = demography["age"]-5
            #     gender_res = demography["gender"]
            #     end = time.time()
            #     #print('deep face time ', end - start)



            if not face_feat and video_cnt % 23 == 0:
                #print ('send data ', video_cnt, idx)

                img_send = current_image.resize((200, 200),Image.NEAREST)

                start = time.time()
                result = run_api(image2byte(img_send))
                detect_res, saved_flag = show_res(result)
                end = time.time()
                # print('run api time ', end - start)
                # print (detect_res)

                if saved_flag:
                    color = 'red'
                    imgtk_resize = ImageTk.PhotoImage(image=current_image.resize((100, 70), Image.NEAREST))
                    label_list[show_idx].imgtk = imgtk_resize
                    label_list[show_idx].config(image=imgtk_resize)
                    label_list[show_idx].update()
                    show_idx = (show_idx+1)%4


                idx = (idx+1)%max_len


            video_cnt = (video_cnt + 1)%1000


def send():
    global select_type
    x = ""
    for j in cheakboxs:
        # 这里实际上是cheakboxs[j].get() == True
        # 如果被勾选的话传回来的值为True
        # 如果没有被勾选的话传回来的值为False
        if cheakboxs[j].get():
            x = x +items[j] + "\n"
        select_str.set ('选择的结果是: \n'+x)

    select_type = x

def face_feat_show():
    global face_feat
    print ('click this btn')

    if featVar.get() == 1:
        face_feat = True
    else:
        face_feat = False

if __name__ == "__main__":

    select_type = ""
    max_len = 500
    detect_res = ''
    face_feat = False
    color = 'green'

    models = {}
    models['age'] = DeepFace.build_model('Age')
    models['gender'] = DeepFace.build_model('Gender')
    backends = [
        'opencv',
        'ssd',
        'dlib',
        'mtcnn',
        'retinaface',
        'mediapipe'
    ]
    camera = cv2.VideoCapture(0)  # 摄像头


    root = Tk()
    root.title("人脸质量筛查系统")

    # 1. camera
    panel = Label(root)  # initialize image panel
    panel.grid(row=0, column=0, rowspan=9)
    root.config(cursor="arrow")

    # 1.1 show detector
    featVar = IntVar()
    faceFeatBtn = Checkbutton(root, text='绘制人脸特征', variable=featVar, command=face_feat_show).grid(row=10, column=0)

    sep = Separator(root, orient='vertical')
    sep.grid(row=0, column=1, rowspan=9, ipady=200, padx=8, pady=8)


    # 2. select info
    label_top = Label(root, text="请选择检测的项目", bg="lightyellow", fg="red", width=20).grid(row=0 , column=2)
    items = {0: "遮挡检测", 1: "旋转角度", 2: "模糊检测", 3: "光照检测", 4: "识别距离"}


    # 这里负责给予字典的键一个False或者True的值，用于检测是否被勾选
    cheakboxs = {}
    for i in range(len(items)):
        # 这里相当于是{0: False, 1: False, 2: False, 3: False, 4: False}
        cheakboxs[i] = BooleanVar()
        # 只有被勾选才变为True
        Checkbutton(root, text=items[i], variable=cheakboxs[i]).grid(row=i + 1, column=2)

    buttonOne = Button(root, text="提交", width=20, command=send).grid(row=len(items) + 1, column=2)

    select_str = StringVar()
    label_btn = Label(root , textvariable=select_str, width=20).grid(row=len(items) + 2 , column=2, rowspan=3)
    sep2 = Separator(root, orient='vertical')
    sep2.grid(row=0 , column=3, rowspan=9 , ipady=200, padx=8, pady=8)

    # 3. show img
    label_top = Label(root, text="以下照片未通过质量检查", bg="lightyellow", fg="red", width=30).grid(row=0 , column=4)
    bg_img_path = '1.png'

    label_list = [1] * 4
    for i in range(4):
        photo = PhotoImage(file=bg_img_path)
        label_list[i] = Label(image=photo,  width=100, height=70)
        label_list[i].image = photo
        label_list[i].grid(row=i*2+1,rowspan=2, column=4)

    video_loop()
    root.mainloop()

    camera.release()
    cv2.destroyAllWindows()

