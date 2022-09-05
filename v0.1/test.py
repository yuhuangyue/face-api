
import cv2, eel

@eel.expose()
def image_process (im):
    print ((im))
    # im_grey = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    # print (im_grey)
    # return im_grey

eel.init(r'C:\0_YHY\1_WORK\创新大赛\v0.1\web')
eel.start('index.html')


