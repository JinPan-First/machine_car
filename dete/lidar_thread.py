import math
import numpy as np
import cv2
import threading


class Draw_Lidar_Help(threading.Thread):
    """
    绘画雷达图帮助线程
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.lidar_data_list = [200 for i in range(1536)] # 初始化雷达列表

    def run(self):
        '''
        根据雷达数据,用cv2画出雷达图
        :param lidar_data_list: 输入的雷达数据;lidar_data_list为全局数据,此是为了方便使用线程概念让图像一直在绘制
        '''
        while(True):
            if(self.lidar_data_list == None): # 无雷达数据
                return
            # 建立二维直角坐标系 ，起始角度为 -45°
            # 注意图像的（0,0）在左上角
            graph = np.zeros((500, 500, 3), np.uint8)
            angle = -48.42+90  # +90为将图像顺时针转动90°
            for radius in self.lidar_data_list:  # 遍历半径
                radius = radius*0.1/2  # 换为0.5cm为单位
                Abscissa = int(math.cos(angle*math.pi/180) * radius)  # 横坐标
                Ordinate = int(math.sin(angle*math.pi/180) * radius)  # 纵坐标
                angle -= 0.18
                if(abs(int(Abscissa)) >= 250 or abs(int(Ordinate)) >= 250):  # 超出地图5m
                    continue
                print((Abscissa, Ordinate))
                # 用CV2画线，中心位置在(250,250),和目标点，颜色是(255,0,0),线宽1
                cv2.line(graph, (250, 250), (Abscissa+250,
                                             Ordinate+250), (255, 0, 0), 1)
                # cv2.circle(graph, (300, 300), 2, (255, 255, 0))
                cv2.imshow('graph', graph)
            cv2.waitKey(1)