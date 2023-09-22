import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication,QMainWindow
from Ui_untitled import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QCursor

class MainWindows(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWindows,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #按钮
        self.close_pushButton.clicked.connect(self.close)
        self.hidden_pushButton.clicked.connect(self.showMinimized)

    #窗口拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

if __name__=="__main__":
    app=QApplication(sys.argv)
    mywin=MainWindows()
    mywin.show()
    sys.exit(app.exec_())