import pyaudio
import threading
import queue
import numpy as np
import wave 
import os
import time



class record_monitor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.recording = True
        self.door = 800 #录音阈值
        self.record = pyaudio.PyAudio() #录音的初始化
        self.output_path = 'records/'
        self.wav_path_list = queue.Queue()

    
    def run(self):
        self.stream = self.record.open(format=pyaudio.paInt16,
                                    channels = 1,
                                    rate = 16000,
                                    input = True,
                                    frames_per_buffer = 512)
        print('开始声音监控')
        while(True):
            while(not self.recording): time.sleep(0.1)
            if not self.stream.is_active:
                self.stream.start_stream()
            frames = []
            for i in range(0,5):
                data = self.stream.read(512)
                frames.append(data)
            #判断是否有说话声
            frames2 = []
            temp = np.max(np.fromstring(data, dtype = np.short))
            # print(temp)
            if temp > self.door:
                print('检测到有说话声')
                loss = 0 #记录当前出现多少次声音低于阈值

                frames2 = []
                print('录音中')
                while(True):

                    for i in range(0,30):
                        data2 = self.stream.read(512)
                        frames2.append(data2)
                    
                    temp2 = np.max(np.fromstring(data2, dtype = np.short))
                    if temp2 < self.door:
                        loss += 1

                        if loss == 15:
                            break
                    
                    else:
                        loss = 0
                print('当前音量低于阈值,停止录音')
            os.makedirs(self.output_path, exist_ok=True)
            self.wav_path = os.path.join(self.output_path, '%s.wav' % str(int(time.time())))
            if frames2 != []:
                wf = wave.open(self.wav_path,'wb')
                wf.setnchannels(1)
                wf.setsampwidth(self.record.get_sample_size(pyaudio.paInt16))
                wf.setframerate(16000)
                wf.writeframes(b''.join(frames2))
                wf.close()
                self.wav_path_list.put(self.wav_path)

r'''
记得最后在总进程里面统一回收stream的资源'''
