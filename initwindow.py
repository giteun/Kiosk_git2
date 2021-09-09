import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *

from mainwindow import WindowClass
from mythread import MyTimer

form_class = uic.loadUiType("initwindow.ui")[0]

class InitialClass(QMainWindow, form_class):
    sec_ = 0
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # opening window in maximized size
        self.showMaximized()
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #F4ECD9;")
        self.setMouseTracking(True)

    def ShowResult(self, sec) :
        print("sec : " + str(sec))
        self.sec_ = sec

    def TimerStop(self) :
        self.thTimer.terminate()
        self.thTimer.working = False

    def mousePressEvent(self, e):  # e ; QMouseEvent
        print('BUTTON PRESS')
        self.thTimer = MyTimer(sec=0, parent=self)
        self.thTimer.thread_timer.connect(self.ShowResult)
        self.thTimer.start()
        
    def mouseReleaseEvent(self, e):  # e ; QMouseEvent
        print('BUTTON RELEASE')
        self.TimerStop()
        if self.sec_ >= 3:
            self.ui = WindowClass()
            self.ui.show()
            #self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = InitialClass()
    myWindow.show()
    app.exec_()