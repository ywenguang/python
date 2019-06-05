#!/usr/bin/python

import os
import time
import urllib
import ssl
import json
import smtplib
import subprocess
import datetime
from shutil import copyfile
from urllib import request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication



# filename = "/home/jiahua/pics/image" + str(get_rand()) + ".jpg"
def get_rand():
    tm = datetime.datetime.now()
    s = ""
    s += str(tm.year) + str(tm.month) + str(tm.day) + str(tm.hour) + str(tm.minute)
    return s

def run_command(filename):
    task = subprocess.run(['fswebcam', '-d', '/dev/video0', '--no-banner', '640x480', filename])
    return task.returncode

def get_pic_path(b):
    filename = "/home/ywg/vscode/video/temp/"
    if b == True:
        filename += get_rand()
    else:
        filename += "_default.jpg"
    ret = run_command(filename)
    if ret == 0:
        return filename
    else:
        return ""


# 邮件发送模块

def send_email(msg_from, passwd, msg_to,subject,text_content, file_path=None):

    # msg_from = '1095133888@qq.com'  # 发送方邮箱
    # passwd = 'zjvoymwngfhigjss'  # 填入发送方邮箱的授权码（就是刚刚你拿到的那个授权码）
    # msg_to = '1095133998@qq.com'  # 收件人邮箱
    msg = MIMEMultipart()
    # text_content = "你好啊，你猜这是谁发的邮件"
    text = MIMEText(text_content)
    msg.attach(text)

    print("enter send_email")

    # docFile = 'C:/Users/main.py'  如果需要添加附件，就给定路径
    if file_path:  # 最开始的函数参数我默认设置了None ，想添加附件，自行更改一下就好
        docFile = file_path
        docApart = MIMEApplication(open(docFile, 'rb').read())
        docApart.add_header('Content-Disposition', 'attachment', filename=docFile)
        msg.attach(docApart)

    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except (smtplib.SMTPException):
        print("发送失败")
    finally:
        s.quit()


def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    context = ssl._create_unverified_context()
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=oxWSUmCiaxLARzcavNHsh4Sq&client_secret=feMOxxWatn53Gxp2IG8rpv5bR2fIKGry'
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request, context=context)
    # 获取请求结果
    content = response.read()
    # 转换为字符
    content = bytes.decode(content)
    # 转换为字典
    content = eval(content[:-1])
    return content['access_token']


# 转换图片
# 读取文件内容，转换为base64编码
# 二进制方式打开图文件
def imgdata(file1path, file2path):
    import base64
    f = open(r'%s' % file1path, 'rb')
    pic1 = base64.b64encode(f.read())
    f.close()
    f = open(r'%s' % file2path, 'rb')
    pic2 = base64.b64encode(f.read())
    f.close()
    # 将图片信息格式化为可提交信息，这里需要注意str参数设置
    params = json.dumps(
        [{"image": str(pic1, 'utf-8'), "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"},
         {"image": str(pic2, 'utf-8'), "image_type": "BASE64", "face_type": "IDCARD", "quality_control": "LOW"}]
    )
    return params.encode(encoding='UTF8')


# 进行对比获得结果
def img(file1path, file2path):
    token = get_token()
    # 人脸识别API
    # url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token='+token
    # 人脸对比API
    context = ssl._create_unverified_context()
    # url = 'https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=' + token
    params = imgdata(file1path, file2path)

    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
    request_url = request_url + "?access_token=" + token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request, context=context)
    content = response.read()
    print(content)
    str_content=str(content)
    is_str_null=str(str_content[-6:-2])
    if is_str_null == "null":

        return False
    else:
        content = eval(content)
        print(content)
        print("")
    # # 获得分数
        score = content['result']['score']
        return score

def get_jpg_filename(path):#获取某个path下的MP3文件
    jpg_name_list = []
    for dirpath, dirnames, filenames in os.walk(path):
        filenames = filter(lambda filename: filename[-4:] == '.jpg', filenames)
        filenames = map(lambda filename: os.path.join(filename), filenames)
        jpg_name_list.extend(filenames)
    return jpg_name_list

def familiar_people(recognized_path,unrecognized_file):#
    result_list=[]
    jpg_list = get_jpg_filename(recognized_path)
    for i in jpg_list:
        pic=str(recognized_path+'/'+i)
        res = img(pic ,unrecognized_file)
        if res != False:
            result_list.append(res)
        else:
            continue
    return result_list



def camera():
    while True:
        get_pic_path(False)
        recognized_path = "/home/ywg/vscode/video/knownpic"
        unrecognized_file = '/home/ywg/vscode/video/temp/_default.jpg'
        # test_path='E:/PycharmProjects/login_1/video\pic/1.jpg'
        result_list = familiar_people(recognized_path, unrecognized_file)
        print(result_list)
        if result_list.__len__() != 0:
            max_similar_value = max(result_list)
            if max_similar_value < 80:
                send_email('mail@yangwg.com', 'zaxncosfroowbibg', '1974480535@qq.com', '智能猫眼提醒', '家里有陌生人来了！',
                           unrecognized_file)
                cur_time = datetime.datetime.now()
                copyfile('/home/ywg/vscode/video/temp/_default.jpg',
                         '/home/ywg/vscode/video/unknownpic/' + str(cur_time) + '.jpg')
        time.sleep(5)

if __name__ == '__main__':
    camera()
