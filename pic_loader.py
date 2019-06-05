import os
import subprocess
import datetime

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
    filename = "/home/ywg/vscode/video/unknownpic/"
    if b == True:
        filename += get_rand()
    else:
        filename += "_default.jpg"
    ret = run_command(filename)
    if ret == 0:
        return filename
    else:
        return ""

if __name__ == '__main__':
    print(get_pic_path(False))