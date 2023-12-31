import logging
from threading import Thread
from ctypes import *

VCI_USBCAN2 = 4  # 设备类型 USBCAN-2A或USBCAN-2C或CANalyst-II
STATUS_OK = 1

# 定义初始化CAN的数据类型
class VCI_INIT_CONFIG(Structure):
    _fields_ = [("AccCode", c_uint),   # 接收滤波验收码
                ("AccMask", c_uint),   # 接收滤波屏蔽码
                ("Reserved", c_uint),
                ("Filter", c_ubyte),   # 滤波方式 0,1接收所有帧。2标准帧滤波，3是扩展帧滤波。
                # 500kbps Timing0=0x00 Timing1=0x1C
                ("Timing0", c_ubyte),  # 波特率参数1，具体配置，请查看二次开发库函数说明书。
                ("Timing1", c_ubyte),  # 波特率参数1
                ("Mode", c_ubyte)      # 模式，0表示正常模式，1表示只听模式,2自测模式
                ]

# 定义CAN信息帧的数据类型
class VCI_CAN_OBJ(Structure):
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),    # 时间标识
                ("TimeFlag", c_ubyte),    # 是否使用时间标识
                ("SendType", c_ubyte),    # 发送标志。保留，未用
                ("RemoteFlag", c_ubyte),  # 是否是远程帧
                ("ExternFlag", c_ubyte),  # 是否是扩展帧
                ("DataLen", c_ubyte),     # 数据长度
                ("Data", c_ubyte*8),      # 数据
                ("Reserved", c_ubyte*3)   # 保留位
                ]

# python3.8.0 64位（python 32位要用32位的DLL）
# Linux系统下使用下面语句，编译命令：python3 python3.8.0.py
# canDLL = cdll.LoadLibrary('./libcontrolcan.so')
CanDLLName = './ControlCAN.dll'  # 把DLL放到对应的目录下
canDLL = windll.LoadLibrary('dll/ControlCAN.dll')

class can_initial(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        """
        Can接口连接scout——mini 底盘
        """
        # 打开设备
        logger = logging.getLogger('logger')
        logger.setLevel(logging.DEBUG)
        formator = logging.Formatter(fmt="%(asctime)s [ %(filename)s ]  %(lineno)d行 | [ %(levelname)s ] | [%(message)s]",
                             datefmt="%Y/%m/%d/%X")
        sh = logging.StreamHandler()
        fh = logging.FileHandler("../log/can_initial.log", encoding="utf-8")
        logger.addHandler(sh)
        sh.setFormatter(formator)
        logger.addHandler(fh)
        fh.setFormatter(formator)

        ret = canDLL.VCI_OpenDevice(VCI_USBCAN2, 0, 0)
        if ret == STATUS_OK:
            logger.info('调用 VCI_OpenDevice成功\r\n')
        if ret != STATUS_OK:
            logger.error('调用 VCI_OpenDevice出错\r\n')
            raise RuntimeError('调用 VCI_OpenDevice出错\r\n')

        # 初始化CAN 0通道
        vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0,
                                         0, 0x00, 0x1C, 0)  # 波特率500k，正常模式
        ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, 0, byref(vci_initconfig))
        if ret == STATUS_OK:
            logger.info('调用 VCI_InitCAN0成功\r\n')
        if ret != STATUS_OK:
            logger.error('调用 VCI_InitCAN0出错\r\n')
            raise RuntimeError('调用 VCI_InitCAN0出错\r\n')

        # 开启CAN 0通道
        ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, 0)
        if ret == STATUS_OK:
            logger.info('调用 VCI_StartCAN0成功\r\n')
        if ret != STATUS_OK:
            logger.error('调用 VCI_StartCAN0出错\r\n')
            raise RuntimeError('调用 VCI_StartCAN0出错\r\n')

        # 设置底盘为指令控制模式
        ret = canDLL.VCI_Transmit(
            VCI_USBCAN2, 0, 0, byref(canDLL.get_start_controller_inst()), 1)
        if ret == STATUS_OK:
            logger.info('CAN0通道发送成功\r\n')
        if ret != STATUS_OK:
            logger.error('CAN0通道发送失败\r\n')
            raise RuntimeError('CAN0通道发送失败\r\n')
        