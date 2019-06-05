import datetime
import subprocess
import time
import pygame
import requests
from aip import AipSpeech


class weather:
    def playMusic(file_name, loops=0, start=0.0, value=0.5):  # 语音播放

        flag = False  # 是否播放过
        pygame.mixer.init()  # 音乐模块初始化
        if flag == 0:
            pygame.mixer.music.load(file_name)
            pygame.mixer.music.play(loops=loops, start=start)
            pygame.mixer.music.set_volume(value)  # 来设置播放的音量，音量value的范围为0.0到1.0。
        if pygame.mixer.music.get_busy():
            flag = True
        else:
            if flag:
                pygame.mixer.music.stop()  # 停止播放

    def weather_to_dict(self, city):  # 获取天气字典
        null_dict = {}
        url = "http://apis.juhe.cn/simpleWeather/query?city=" + str(city) + "&key=2474caa0d0c2f1df25909c6a86dfd2c5"
        data = requests.get(url)
        weather = data.json()
        result = weather['result']
        if result is None:
            return null_dict
        else:
            real_time = result['realtime']
            return real_time

    def weather_audio(self, text):  # 获取天气语音
        """ 你的 APP_ID AK SK """
        APP_ID = '16153159'
        API_KEY = 'LGeFlCeR4kTD7zCrT3IKldGP'
        SECRET_KEY = 'EQ0vP14ohVimQCHMBkrwsgGUctfzIPSC'
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        result = client.synthesis(text=text, options={'vol': 5})
        if not isinstance(result, dict):
            with open('weather_audio.mp3', 'wb') as f:
                f.write(result)
        else:
            print(result)

    def play_weather_audio(self, weather_dict):  # 播放当前天气语音
        cur_time = datetime.datetime.now()
        text = "现在是" + str(cur_time.year) + "年" + str(cur_time.month) \
               + "月" + str(cur_time.day) + "日" + "!" + str(cur_time.hour) \
               + "点" + str(cur_time.minute) + "分" + "!" + str(weather_dict['info']) + "!" \
               + str(weather_dict['temperature']) + "度！" + str(weather_dict['direct']) \
               + str(weather_dict['power']) + "!"
        self.weather_audio(text)
        subprocess.Popen(["start", "weather_audio.mp3"], shell=True)
        #self.playMusic('E:/PycharmProjects/login_1/login\GUI/weather_audio.mp3/weather_audio.mp3')

    def full_play(self):  # 整点报时功能
        while True:
            cur_time = datetime.datetime.now()
            time.sleep(1)
            if cur_time.minute == 36:
                weather_dict = self.weather_to_dict("武汉")
                self.play_weather_audio(weather_dict)
                time.sleep(60)


if __name__ == '__main__':
    weather=weather()
    weather.full_play()



#full_play_thread = threading.Thread(target=full_play, args=())  # 创建整点报时线程
# #full_play_thread.start()
