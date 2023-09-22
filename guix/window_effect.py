# coding:utf-8

from ctypes import c_bool, cdll
from ctypes.wintypes import DWORD, HWND,LPARAM

from win32 import win32gui
from win32.lib import win32con


class WindowEffect():
    """ 调用windowEffect.dll来设置窗口外观 """
    dll = cdll.LoadLibrary('dll\\windowEffect.dll')

    def setAcrylicEffect(self,
                         hWnd: HWND,
                         gradientColor: str = 'FF000066',
                         accentFlags: bool = False,
                         animationId: int = 0):
        """ 开启亚克力效果,gradientColor对应16进制的rgba四个分量 """

        # 设置阴影
        if accentFlags:
            accentFlags = DWORD(0x20 | 0x40 | 0x80 | 0x100)
        else:
            accentFlags = DWORD(0)

        # 设置和亚克力效果相叠加的背景颜色
        gradientColor = gradientColor[6:] + gradientColor[4:6] + \
            gradientColor[2:4] + gradientColor[:2]
        gradientColor = DWORD(int(gradientColor, base=16))
        animationId = DWORD(animationId)
        self.dll.setAcrylicEffect(hWnd, accentFlags, gradientColor,
                                  animationId)

    def setAeroEffect(self, hWnd: HWND):
        """ 开启Aero效果 """
        self.dll.setAeroEffect(hWnd)

    def setShadowEffect(self,
                        class_amended: c_bool,
                        hWnd: HWND,
                        newShadow=True):
        """ 去除窗口自带阴影并决定是否添加新阴影 """
        class_amended = c_bool(
            self.dll.setShadowEffect(class_amended, hWnd, c_bool(newShadow)))
        return class_amended

    def addShadowEffect(self, shadowEnable: bool, hWnd: HWND):
        """ 直接添加新阴影 """
        self.dll.addShadowEffect(c_bool(shadowEnable), hWnd)

    def setWindowFrame(self, hWnd: HWND, left: int, top, right, buttom):
        """ 设置客户区的边框大小 """
        self.dll.setWindowFrame(hWnd, left, top, right, buttom)

    def setWindowAnimation(self, hWnd):
        """ 打开窗口动画效果 """
        style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            hWnd, win32con.GWL_STYLE, style | win32con.WS_MAXIMIZEBOX
                                            | win32con.WS_CAPTION
                                            | win32con.CS_DBLCLKS
                                            | win32con.WS_THICKFRAME)

    def adjustMaximizedClientRect(self, hWnd: HWND, lParam: int):
        """ 窗口最大化时调整大小 """
        self.dll.adjustMaximizedClientRect(hWnd, LPARAM(lParam))

    def moveWindow(self,hWnd:HWND):
        """ 移动窗口 """
        self.dll.moveWindow(hWnd)
