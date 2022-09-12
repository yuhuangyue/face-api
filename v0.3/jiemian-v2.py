import os.path
from tkinter import *
import cv2
from PIL import Image, ImageTk, ImageFont,ImageDraw
from tkinter.ttk import Separator
import numpy as np
import threading
import time
import sys
sys.path.append(r'E:\AFCtest\Face\Face_Recognition_Algorithm\人脸特征分析\minions_check_quality_v0.1.0\checkAPI\Minions\\')
from minions_api import detect

from deepface import DeepFace
import io
import base64

testIp = 'http://172.16.50.17:9000/'



class MyThread1(threading.Thread):
    def __init__(self,name = None):
        super().__init__(name = name)
    def run(self):
        global age_res
        global gender_res
        while(tasklist[0] is 0):
            time.sleep(1)
        step = 0

        while (tasklist[step] is not -1):
            if (tasklist[step] is 0):
                continue
            demography = DeepFace.analyze(np.array(tasklist[step])[:,:,0:3], actions = ['age', 'gender'],enforce_detection = False,models=models,detector_backend = backends[0])
            age_res = demography["age"]
            gender_res = demography["gender"]
            step = (step+5)%max_len


class MyThread2(threading.Thread):
    def __init__(self,name = None):
        super().__init__(name = name)
    def run(self):
        img_process()


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
    print (result1)
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


def img_process():
    global detect_res
    global saved_flag
    global cur_saved_img

    while(tasklist[0] is 0):
        time.sleep(1)
    print('thread start')
    step = 0

    while(tasklist[step] is not -1):
        if tasklist[step] is 0:
            continue

        result = run_api (image2byte(tasklist[step]))
        detect_res, saved_flag = show_res(result)

        # 绘制不符合的图像
        if saved_flag:
            print (saved_flag)
            cur_saved_img = tasklist[step]

        if detect_res is not "":
            print (detect_res)

        step = (step+5)%max_len





def video_loop():
    global tasklist
    global cur_saved_img
    global saved_flag
    global age_res
    global gender_res
    idx = 0
    while camera.isOpened():
        success, img = camera.read()  # 从摄像头读取照片
        if success:
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            cv2image = cv2.flip(cv2image, 1)  # 摄像头是和人对立的，将图像左右调换回来正常显示。
            # cv2.imwrite('temp.jpg', cv2image)
            current_image = Image.fromarray(cv2image)  # 将图像转换成Image对象
            current_image = current_image.resize((400, 300),Image.NEAREST)

            tasklist[idx] = current_image
            idx = (idx+1)%max_len

            draw = ImageDraw.Draw(current_image)

            draw.text((10, 10), detect_res + str(gender_res) + str(age_res), font=ImageFont.truetype("./simsun.ttc",30), fill=(255, 255, 255))

            imgtk = ImageTk.PhotoImage(image=current_image)
            panel.imgtk = imgtk
            panel.config(image=imgtk)
            panel.update()

            # 保存质量不合格的图像
            if saved_flag and (cur_saved_img is not None):
                cur_saved = ImageTk.PhotoImage(image=cur_saved_img)
                label_img.imgtk = cur_saved
                label_img.config(image=cur_saved)
                label_img.update()







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

    #print(x)
    select_type = x

if __name__ == "__main__":

    select_type = ""
    age_res = 0
    gender_res = ''
    max_len = 500
    saved_flag = False
    cur_saved_img = None
    detect_res = ''
    tasklist = [0] * max_len
    #tasklist = [None] * max_len
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
    root.title("camera")

    # 1. camera
    panel = Label(root)  # initialize image panel
    panel.grid(row=0, column=0, rowspan=9)
    root.config(cursor="arrow")


    sep = Separator(root, orient='vertical')
    sep.grid(row=0, column=1, rowspan=9, ipady=200, padx=8, pady=8)

    # 2. select info

    label_top = Label(root, text="请选择检测的项目", bg="lightyellow", fg="red", width=20).grid(row=0 , column=2)
    items = {0: "遮挡检测", 1: "旋转角度", 2: "模糊检测", 3: "光照检测", 4: "瞳孔间距"}



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
    label_top = Label(root, text="以下照片未通过质量检查", bg="lightyellow", fg="red", width=60).grid(row=0 , column=4)
    photo = PhotoImage(file='1.png')
    label_img = Label(image=photo,  width=300, height=300)
    label_img.image = photo
    label_img.grid(row=0, column=4, columnspan=1, rowspan=9)

    thread_age = MyThread1()
    thread_age.start()

    thread_img = MyThread2()
    thread_img.start()

    video_loop()

    root.mainloop()
    tasklist=[-1]*max_len
    #tasklist = None


    thread_age.join()
    thread_img.join()

    camera.release()
    cv2.destroyAllWindows()

