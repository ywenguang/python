import itchat

# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# 写成了一个通用的函数接口，想直接用的话，把参数的注释去掉就好
def send_email(msg_from, passwd, msg_to, text_content, file_path=None):
    # msg_from = '1095133888@qq.com'  # 发送方邮箱
    # passwd = 'zjvoymwngfhigjss'  # 填入发送方邮箱的授权码（就是刚刚你拿到的那个授权码）
    # msg_to = '1095133998@qq.com'  # 收件人邮箱

    msg = MIMEMultipart()

    subject = "Test My Email"  # 主题
    # text_content = "你好啊，你猜这是谁发的邮件"
    text = MIMEText(text_content)
    msg.attach(text)

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


#send_email('mail@yangwg.com','zaxncosfroowbibg','jiahua.h@outlook.com','hello，how are you?','E:/PycharmProjects/login_1/login/GUI/2.png')


"""
def send_picture(username,jpg_file):#输入jpg文件时需要输入完整的路径
    itchat.auto_login(hotReload=True)
    users=itchat.search_friends(str(username))
    userName= users[0]['UserName']
    itchat.send('有陌生人来了！',toUserName=userName)
    try:
        itchat.send_image(jpg_file,toUserName=userName)  #如果是其他文件可以直接send_file
        print("success")
    except:
        print("fail")
        

if __name__ == '__main__':

    file = "E:/PycharmProjects/login_1/video\8.jpg"  # 图片地址
    user="黄嘉华"
    send_picture(user,file)


"""


