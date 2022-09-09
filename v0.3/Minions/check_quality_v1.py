#coding=utf-8
#开发团队 ： EBG-FaceID
#优化: zhaojialiang
#开发时间 ： 2021/09/23
#文件名称 ： check_quality.PY
#开发工具 ： PyCharm

from minions_api import get_version
from minions_api import get_value
from minions_api import detect
import os
import sys
import shutil
import threadpool
import glob
import cv2 as cv

sys.path.append('..\\common\\')
from getLog import Log

log = Log()

# 服务地址及端口
# testIp = 'http://10.122.48.94:9000/'
testIp = 'http://172.16.50.17:9000/'

# 本地图片路径
ROOT = "D:\Sensetime-50w\data\images\\"
imgurl_all = ROOT + "A\\"
imgurl_true = ROOT + "true\\"
imgurl_false = ROOT + "false\\"

# if not os.path.exists(imgurl_true):
#     os.makedirs(imgurl_true)
#
# if not os.path.exists(imgurl_false):
#     os.makedirs(imgurl_false)

def classify_img(img):

    img_path = img
    
    result = detect(testIp, img_path)
    img = img.split('.')[0]+ '_' + str(result[1])+ '.jpg'
    imgpath_true = imgurl_true + img
    imgpath_false = imgurl_false + img

    #if str(result[0]) == "false" : log.info( img + '----' + str(result))
    if str(result[0]) == "false" :
        print (img_path)
        # shutil.copyfile(img_path, imgpath_false)
        # cv.imshow('test',cv.imread(img_path))
        # cv.waitKey(0)
        os.remove(img_path)



    # else:
    #     shutil.copyfile(img_path, imgpath_true)


if __name__ == '__main__':


    #输出版本信息
    #log.info('算法版本信息：' + str(get_version(testIp)))
    #输出当前设定阈值
    log.info('当前阈值：' + str(get_value()))
    #输出检测结果
    log.info('--------------Start Running in ' + testIp + '--------------------------')
    imgs = glob.glob(r"D:\Sensetime-50w\data\images\msra\*\*.jpg")
    #imgs = os.listdir(imgurl_all)
    pool = threadpool.ThreadPool(30)
    request = threadpool.makeRequests(classify_img, imgs)
    [pool.putRequest(req) for req in request]
    pool.wait()
