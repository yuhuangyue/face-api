#coding=utf-8
#开发团队 ： EBG-FaceID
#开发人员 ： chenjing
#开发时间 ： 2021/09/23
#文件名称 ： check_quality.PY
#开发工具 ： PyCharm

from minions_api import get_version
from minions_api import get_value
from minions_api import detect
import os
import sys
import shutil



sys.path.append('..\\common\\')
from getLog import Log

log = Log()

if __name__ == '__main__':
    #本地图片路径
    ROOT = "D:\WORK\AFCtest\Face\Face_Recognition_Algorithm\data\\202110\\"
    imgurl_all = ROOT + "faces\\"
    imgurl_true = ROOT + "data\\true\\"
    imgurl_false = ROOT + "data\\false\\"


    if not os.path.exists(imgurl_false):
        os.makedirs(imgurl_false)

    #服务地址及端口
    testIp = 'http://172.16.50.17:9000/'
    #输出版本信息
    # log.info('算法版本信息：' + str(get_version(testIp)))
    #输出当前设定阈值
    log.info('当前阈值：' + str(get_value()))
    #输出检测结果
    log.info('--------------Start Running in ' + testIp + '--------------------------')
    imgs = os.listdir(imgurl_all)
    for img in imgs:
        imgpath_all = imgurl_all + img
        result = detect(testIp, imgpath_all)

        img = img.split('.')[0]+str(result[1])+'.png'

        imgpath_true = imgurl_true + img
        imgpath_false = imgurl_false + img

        str(result) + '.jpg'

        #仅将质量不合格图片名称、不合格项信息写入到日志文件
        if str(result[0]) == "false": 
            print (result)
            log.info(img + '-----'+ str(result))
            shutil.copyfile(imgpath_all, imgpath_false)

        #将全部图片名称、质检结果、属性信息写入到日志文件
        #log.info(img + '-----' + str(result))
        #将质量合格图片复制到“imgurl_true”文件夹，将质量不合格图片复制到“imgurl_false”文件夹
       
            
        # else:
        #     shutil.copyfile(imgpath_all, imgpath_true)
