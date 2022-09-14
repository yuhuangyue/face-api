import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import Separator
from utils import morph_faces
import cv2 
import imageio

img_width = 500
img_height = 300

imglist = ['','']
def upload_file1():
    filePath1 = tk.filedialog.askopenfilename()
    photo = PhotoImage(file=filePath1)
    imglist[0] = filePath1
    labe_img1.imgtk = photo
    labe_img1.config(image=photo)
    labe_img1.update()

def upload_file2():
    filePath2 = tk.filedialog.askopenfilename()
    photo = PhotoImage(file=filePath2)
    imglist[1] = filePath2
    labe_img2.imgtk = photo
    labe_img2.config(image=photo)
    labe_img2.update()

def merge_model():
    if imglist[0]=='' or imglist[1] =='':
        return
    img_morphed = morph_faces(imglist[0],imglist[1])
    cv2.imwrite('merge.png', img_morphed)
    photo = PhotoImage(file='merge.png')
    labe_img3.imgtk = photo
    labe_img3.config(image=photo)
    labe_img3.update()


# def create_gif(source, name, duration):
#     frames = []
#     for img in source:
#         frames.append(imageio.imread(img))
#     imageio.mimsave(name, frames, 'GIF', duration=duration)
#     print("处理完成")


root = tk.Tk()
root.title("merge")
btn1 = tk.Button(root, text='上传图片1', command=upload_file1).grid(row=0, column=0, ipadx='3', ipady='3', padx='10', pady='20')
btn2 = tk.Button(root, text='上传图片2', command=upload_file2).grid(row=2, column=0, ipadx='3', ipady='3', padx='10', pady='20')
init_photo = PhotoImage(file='../1.png')
labe_img1 = Label(image=init_photo,  width=img_width, height=img_height)
labe_img1.grid(row=1, column=0)
labe_img2 = Label(image=init_photo,  width=img_width, height=img_height)
labe_img2.grid(row=3, column=0)

sep = Separator(root, orient='vertical')
sep.grid(row=0, column=1, rowspan=9, ipady=400, padx=8, pady=8)
btn3 = tk.Button(root, text='合并图片', command=merge_model,width=15).grid(row=0, column=2, ipadx='3', ipady='3',padx='10', pady='20')
labe_img3 = Label(image=init_photo,  width=img_width, height=img_height)
labe_img3.grid(row=1, column=2)

root.mainloop()