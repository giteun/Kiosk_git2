# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from gtts import gTTS

from mythread import MyPlayer, MyTimer
from complet import CompletClass

form_class = uic.loadUiType("Dialog_payment.ui")[0]

class PaymentClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        
        self.setupUi(self)
        # opening window in maximized size
        self.showMaximized()
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.InitUi()
        voice = self.label.text() + self.label2.text() + self.btnCancel_1.text() + self.btnCancel_2.text()
        self.MakeSound(voice, 0)

        #타이머 스레드 시작
        self.thTimer = MyTimer(sec=0, parent=self)
        self.thTimer.thread_timer.connect(self.stopWatch)
        self.thTimer.start()

    def InitUi(self) :
        self.watch_working = True
        self.setStyleSheet("color: white;"
                    "background-color: #1B3C35;")

        #self.btnCancel.setText("취소")

        self.pix = QPixmap()
        self.pix.load("image/pngwing.png")
        self.pix = self.pix.scaled(240,240)
        self.PayImg.setPixmap(self.pix)

    def MakeSound(self, tname, num):
        ttext = tname
        tts = gTTS(
            text=ttext,
            lang='ko', slow=False
        )
        tfile = "payment{0}". format(num)
        tts.save("sound\ex_" + tfile + ".mp3")
        self.thPlayer = MyPlayer(-1, tfile, parent=self)
        self.thPlayer.start()

    def mouseDoubleClickEvent(self, event) :
        print("doubleclick")
        self.thPlayer.terminate()
        self.thTimer.terminate()
        self.btnCancel()
    
    def btnCancel(self) :
        self.watch_working = False
        self.close()

    def stopWatch(self, sec) :
        print(sec)
        if self.watch_working == True :
            if sec == 13 :
                self.thTimer.terminate()
                self.ui = CompletClass()
                self.ui.show()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = PaymentClass() 
    myWindow.show()
    app.exec_()