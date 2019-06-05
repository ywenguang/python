import datetime
from shutil import copyfile

cur_time=datetime.datetime.now()
copyfile('/home/ywg/vscode/video/temp/_default.jpg', '/home/ywg/vscode/video/temp/' + str(cur_time) + '.jpg')
