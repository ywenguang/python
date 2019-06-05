import os
import threading
import pygame
import datetime
import time
from login.GUI.weather_audio import *


class alarm:
    time_points = []
    lock = threading.Lock()
    flag = False

    def __init__(self):
        read_thread = threading.Thread(target=self.time_ergodic, args=())
        read_thread.start()
        print(read_thread.is_alive())

    def delete_time_point(self, index):
        self.lock.acquire()
        self.time_points.pop(index)
        self.lock.release()

    def add_time_point(self, hour, minute):
        self.lock.acquire()
        last_time = [hour, minute]
        self.time_points.append(last_time)
        self.lock.release()

    def time_ergodic(self):
        flag = True
        while flag:
            curr_time = datetime.datetime.now()
            for t in self.time_points:
                if int(curr_time.hour) == int(t[0]) and int(curr_time.minute) == int(t[1]):  # 如果设置的闹钟时间和当前的闹钟时间是相等的
                    print("起床时间到了！！！！！！")
                    self.play_music("E:/PycharmProjects/login_1/login/GUI/海阔天空.mp3")
                    stop = input()
                    if int(stop) > 0:
                        self.stop_music()
                    time.sleep(60)
                    flag = True
            time.sleep(1)

    def get_mp3_filename(self, mp3file_path):  # 获取某个path下的MP3文件
        mp3_name_list = []
        for dir_path, dir_names, file_names in os.walk(mp3file_path):
            file_names = filter(lambda filename: filename[-4:] == '.mp3', file_names)
            file_names = map(lambda filename: os.path.join(filename), file_names)
            mp3_name_list.extend(file_names)
        return mp3_name_list

    def play_music(self, file_name, loops=0, start=0.0, value=0.5):
        flag = False  # 是否播放过
        pygame.mixer.init()  # 音乐模块初始化
        if flag == 0:
            pygame.mixer.music.load(file_name)
            pygame.mixer.music.play(loops=loops, start=start)
            pygame.mixer.music.set_volume(value)  # 来设置播放的音量，音量value的范围为0.0到1.0。
        if pygame.mixer.music.get_busy() is True:
            flag = True
        else:
            if flag:
                pygame.mixer.music.stop()  # 停止播放

    def stop_music(self):  # 停止播放音乐
        if self.flag is True:
            pygame.mixer.music.stop()  # 停止播放
        else:
            print("当前未播放音乐！")

    def alarm(self, hour, minute, song):
        start = True
        while start:
            curr_time = datetime.datetime.now()
            if int(curr_time.hour) == int(hour) and int(curr_time.minute) == int(minute):  # 如果设置的闹钟时间和当前的闹钟时间是相等的
                print("起床时间到了！！！！！！")
                self.play_music(song)
                self.flag = True
                start = False
            time.sleep(1)


if __name__ == '__main__':
    times = 10
    clocks = alarm()
    clocks.add_time_point(13, 15)
    clocks.add_time_point(13, 19)
    print(clocks.time_points)
    clocks.delete_time_point(1)
    print(clocks.time_points)
