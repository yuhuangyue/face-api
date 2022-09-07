from tkinter import *
import cv2
from PIL import Image, ImageTk
from tkinter.ttk import Separator

def video_loop():
    success, img = camera.read()  # 从摄像头读取照片
    if success:
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)  # 将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        root.after(1, video_loop)


camera = cv2.VideoCapture(0)  # 摄像头

root = Tk()
root.title("camera")

# 1. camera
panel = Label(root)  # initialize image panel
panel.grid(row=0 , column=0, rowspan=9)
root.config(cursor="arrow")
video_loop()

sep = Separator(root, orient='vertical')
sep.grid(row=0 , column=1, rowspan=9 , ipady=200, padx=8, pady=8)

# 2. select info

def send():
    x = ""
    for j in cheakboxs:
        # 这里实际上是cheakboxs[j].get() == True
        # 如果被勾选的话传回来的值为True
        # 如果没有被勾选的话传回来的值为False
        if cheakboxs[j].get():
            x = x +items[j] + "\n"
        str.set ('选择的结果是: \n'+x)


    print(x)


label_top = Label(root, text="请选择检测的项目", bg="lightyellow", fg="red", width=20).grid(row=0 , column=2)


items = {0: "口罩检测", 1: "旋转角度", 2: "模糊程度", 3: "光照检测", 4: "瞳孔间距"}
# 这里负责给予字典的键一个False或者True的值，用于检测是否被勾选
cheakboxs = {}
for i in range(len(items)):
    # 这里相当于是{0: False, 1: False, 2: False, 3: False, 4: False}
    cheakboxs[i] = BooleanVar()
    # 只有被勾选才变为True
    Checkbutton(root, text=items[i], variable=cheakboxs[i]).grid(row=i + 1, column=2)

buttonOne = Button(root, text="提交", width=20, command=send).grid(row=len(items) + 1, column=2)

str = StringVar()
label_btn = Label(root , textvariable=str, width=20).grid(row=len(items) + 2 , column=2, rowspan=3)


sep2 = Separator(root, orient='vertical')
sep2.grid(row=0 , column=3, rowspan=9 , ipady=200, padx=8, pady=8)

# 3. show img

label_top = Label(root, text="以下照片未通过质量检查", bg="lightyellow", fg="red", width=60).grid(row=0 , column=4)


photo = PhotoImage(file='bg.png')
label_img = Label(image=photo,  width=300, height=300)
label_img.image = photo
label_img.grid(row=0, column=4, columnspan=1, rowspan=9)



root.mainloop()

camera.release()
cv2.destroyAllWindows()
