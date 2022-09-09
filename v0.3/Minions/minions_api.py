#coding=utf-8
#开发团队 ： EBG-FaceID
#开发人员 ： chenjing
#开发时间 ： 2021/09/23
#文件名称 ： minions_api.PY
#开发工具 ： PyCharm
import requests
from random import randint

USER_AGENTS = [
 "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
 "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
 "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
 "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
 "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
 "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
 "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
 "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
 "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
 
random_agent = USER_AGENTS[randint(0, len(USER_AGENTS)-1)]
headers = {'User-Agent':random_agent,}


#版本信息获取
def get_version(testIp):
    url = testIp + "version"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print('here:', response.json())

#阈值设置
min_confidence_value = 0.3
max_blurness_value = 0.5
forehead_occ_value = 1
left_face_occ_value = 1
right_face_occ_value = 1
chin_occ_value = 0.3
left_eyebrow_occ_value = 1
right_eyebrow_occ_value = 1
left_eye_sunglasses_value = 2
left_eye_otherocc_value = 3
right_eye_sunglasses_value = 2
right_eye_otherocc_value = 3
nose_occ_value = 1
mouth_occ_value = 1
left_ear_occ_value = 1
right_ear_occ_value = 1
max_left_eye_open_value = 0.1
max_right_eye_open_value = 0.1
max_roll_value = 30
max_pitch_value = 30
max_yaw_value = 30
max_brightness_value = 400
min_brightness_value = 70

#设定阈值获取
def get_value():
    return '最小人脸置信度：', min_confidence_value, \
           '最大模糊度：', max_blurness_value, \
           '额头遮挡：', forehead_occ_value, \
           '左脸遮挡：', left_face_occ_value, \
           '右脸遮挡：', right_face_occ_value, \
           '下巴遮挡：', chin_occ_value, \
           '左眉遮挡：', left_eyebrow_occ_value, \
           '右眉遮挡：', right_eyebrow_occ_value, \
           '左眼太阳镜遮挡：', left_eye_sunglasses_value, \
           '左眼其他遮挡：', left_eye_otherocc_value, \
           '右眼太阳镜遮挡：', right_eye_sunglasses_value, \
           '右眼其他遮挡：', right_eye_otherocc_value, \
           '鼻子遮挡：', nose_occ_value, \
           '嘴部遮挡：', mouth_occ_value, \
           '左耳遮挡：', left_ear_occ_value, \
           '右耳遮挡：', right_ear_occ_value, \
           '最大左眼睁开值：', max_left_eye_open_value, \
           '最大右眼睁开值：', max_right_eye_open_value, \
           '最大旋转角度：', max_roll_value, \
           '最大俯仰角度：', max_pitch_value, \
           '最大侧倾角度：', max_yaw_value, \
           '最大光照度：', max_brightness_value, \
           '最小光照度：', min_brightness_value


#图片质量检测（输出检测结果及全部属性）
def detect(testIp, image):
    url= testIp + "detect"
    #headers = {"Content-Type": "application/json"}
    files = {'image': open(image, "rb")}
    #files = {'image': image}
    data = {"faceattr": "1"}

    response = requests.post(url, data=data, files=files)
    if response.status_code == 200:

        if len(response.json()['faces']) ==0:
            quality = "false"
            info = '无人脸'
            return quality, info

        #质量相关属性数据获取
        confidence=response.json()['faces'][0]['Confidence']
        blurness = response.json()['faces'][0]['faceattr']['blurness']
        forehead_occlusion = response.json()['faces'][0]['faceattr']['forehead_occlusion_status']
        left_face_occlusion = response.json()['faces'][0]['faceattr']['left_face_occlusion_status']
        right_face_occlusion = response.json()['faces'][0]['faceattr']['right_face_occlusion_status']
        chin_occlusion = response.json()['faces'][0]['faceattr']['chin_occlusion_status']
        left_eyebrow_occlusion = response.json()['faces'][0]['faceattr']['left_eyebrow_occlusion_status']
        right_eyebrow_occlusion = response.json()['faces'][0]['faceattr']['right_eyebrow_occlusion_status']
        left_eye_occlusion = response.json()['faces'][0]['faceattr']['left_eye_occlusion_status']
        right_eye_occlusion = response.json()['faces'][0]['faceattr']['right_eye_occlusion_status']
        nose_occlusion = response.json()['faces'][0]['faceattr']['nose_occlusion_status']
        mouth_occlusion = response.json()['faces'][0]['faceattr']['mouth_occlusion_status']
        left_ear_occlusion = response.json()['faces'][0]['faceattr']['left_ear_occlusion_status']
        right_ear_occlusion = response.json()['faces'][0]['faceattr']['right_ear_occlusion_status']
        left_eye_closed = response.json()['faces'][0]['faceattr']['left_eye_closed_score']
        right_eye_closed = response.json()['faces'][0]['faceattr']['right_eye_closed_score']
        roll = response.json()['faces'][0]['faceattr']['roll']
        pitch = response.json()['faces'][0]['faceattr']['pitch']
        yaw = response.json()['faces'][0]['faceattr']['yaw']
        brightness = response.json()['faces'][0]['faceattr']['brightness']

        #质量判断算法定义  质量不合格时quality为false且输出不合格项结果，
        if confidence < min_confidence_value:
            quality = "false"
            info = '人脸置信度：', str(confidence)
        elif blurness > max_blurness_value:
            quality = "false"
            #info = ' 模糊度：', str(blurness)
            info = '照片过于模糊'
        #不建议限制此项 elif forehead_occlusion == forehead_occ_value:
        #    quality = "false"
        #    info = '额头遮挡：', forehead_occlusion
        elif left_face_occlusion == left_face_occ_value and right_face_occlusion == right_face_occ_value:
            quality = "false"
            #info = '口罩遮挡：', str(left_face_occlusion)
            info = '口罩遮挡'
        # elif right_face_occlusion == right_face_occ_value:
        #     quality = "false"
        #     info = '右脸遮挡：', str(right_face_occlusion)
        elif chin_occlusion == chin_occ_value:
            quality = "false"
            info = '下巴遮挡：', str(chin_occlusion)
        # elif left_eyebrow_occlusion == left_eyebrow_occ_value:
        #     quality = "false"
        #     info = '左眉遮挡：', str(left_eyebrow_occlusion)
        # elif right_eyebrow_occlusion == right_eyebrow_occ_value:
        #     quality = "false"
        #     info = '右眉遮挡：', str(right_eyebrow_occlusion)
        elif (left_eye_occlusion == left_eye_sunglasses_value or left_eye_occlusion == left_eye_otherocc_value) and (right_eye_occlusion == right_eye_sunglasses_value or right_eye_occlusion == right_eye_otherocc_value):
            quality = "false"
            info = '左右眼遮挡：', str(left_eye_occlusion)+str(right_eye_occlusion)
        # elif (right_eye_occlusion == right_eye_sunglasses_value or right_eye_occlusion == right_eye_otherocc_value):
        #     quality = "false"
        #     info = '右眼遮挡：', str(right_eye_occlusion)
        elif nose_occlusion == nose_occ_value:
            quality = "false"
            info = '鼻子遮挡：', str(nose_occlusion)
        elif mouth_occlusion == mouth_occ_value:
            quality = "false"
            info = '嘴部遮挡：', str(mouth_occlusion)
        #不建议限制此项 elif left_ear_occlusion == left_ear_occ_value:
        #    quality = "false"
        #    info = '左眼闭眼分：' + left_eye_closed
        #不建议限制此项 elif right_ear_occlusion == right_ear_occ_value:
        #    quality = "false"
        #    info = '右眼闭眼分：' + right_eye_closed
        elif left_eye_closed > max_left_eye_open_value:
            quality = "false"
            # info = '左眼遮挡：' + str(left_eye_closed)
            info = '左眼遮挡'
        elif right_eye_closed > max_right_eye_open_value:
            quality = "false"
            info = '右眼遮挡：' + str(right_eye_closed)
            info = '右眼遮挡'
        elif abs(roll) > max_roll_value:
            quality = "false"
            #info = '旋转角度：' + str(roll)
            info = '头部旋转角度超过规定范围['+str(int(roll)) +']'
        elif abs(pitch) > max_pitch_value:
            quality = "false"
            #info = '俯仰角度：' + str(pitch)
            info = '头部俯仰角度超过规定范围['+str(int(pitch)) +']'
        elif abs(yaw) > max_yaw_value:
            quality = "false"
            #info = '侧倾角度：' + str(yaw)
            info = '头部侧倾角度超过规定范围['+str(int(yaw)) +']'
        elif brightness > max_brightness_value or brightness < min_brightness_value:
            quality = "false"
            #info = '光照度：' + str(brightness)
            info = '照片曝光过强'
        else:
            quality = "true"
            info = '人脸置信度：', confidence, '模糊度：', blurness, '额头遮挡：', forehead_occlusion, '左脸遮挡：', left_face_occlusion, '右脸遮挡：', right_face_occlusion, '下巴遮挡：',  chin_occlusion, ',  左眉遮挡：',  left_eyebrow_occlusion, '右眉遮挡：', right_eyebrow_occlusion, '左眼遮挡：', left_eye_occlusion, '右眼遮挡：', right_eye_occlusion, '鼻子遮挡：', nose_occlusion, '嘴部遮挡：', mouth_occlusion, '左耳遮挡：', left_ear_occlusion, '右耳遮挡：', right_ear_occlusion, '左眼闭眼分：', left_eye_closed, '左眼闭眼分：', right_eye_closed, '旋转角度：', roll, '俯仰角度：', pitch, '侧倾角度：', yaw, '光照度：', brightness

        # 输出质量判断结果及各属性数据
        return quality, info
    else:
        error = response.json()['error']
        return [error, '-----']




