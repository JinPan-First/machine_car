import logging
import time
import threading
import time
import queue


from rapid_paraformer import RapidParaformer


class ASRService(threading.Thread):
    def __init__(self, config_path, record_thread):
        threading.Thread.__init__(self)
        logging.info('Initializing ASR Service...')
        self.paraformer = RapidParaformer(config_path)
        logging.info('Initialize ASR Service finish')
        self.result = None
        self.result_list = queue.Queue()
        self.record_thread = record_thread
        self.wav_path = self.record_thread.wav_path_list
        self.open_s = False
        self.open_d = False

    def infer(self):

        stime = time.time()
        wav_path = self.wav_path.get(block =True)
        print(wav_path)
        result = self.paraformer(wav_path)
        logging.info('ASR Result: %s. time used %.2f.' % (result, time.time() - stime))
        self.result = result[0]
        if self.result == '开始识别':
            self.open_s = True
        elif self.result == '打开导航功能':
            self.open_d = True
        else:
            self.result_list.put(self.result,block = True)
    
    def run(self):
        while(True):
            if self.record_thread.recording and not self.wav_path.empty():
                self.infer()
                print(self.result)
