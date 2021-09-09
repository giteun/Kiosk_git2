# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from gtts import gTTS

from mythread import MyPlayer

form_class = uic.loadUiType("Dialog_complet.ui")[0]

class CompletClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        
        self.setupUi(self)
        # opening window in maximized size
        self.showMaximized()
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.InitUi()
        voice = self.label.text() + self.orderNum_1.text() + "는 " + self.orderNum_2.text() + " 입니다."
        self.MakeSound(voice, 0)

    def InitUi(self) :
        self.setStyleSheet("color: white;"
                    "background-color: #1B3C35;")

        self.pix = QPixmap()
        self.pix.load("image\\receipt_green.png")
        self.pix = self.pix.scaled(300,300)
        self.PayImg.setPixmap(self.pix)

    def MakeSound(self, tname, num):
        ttext = tname
        tts = gTTS(
            text=ttext,
            lang='ko', slow=False
        )
        tfile = "complet{0}". format(num)
        tts.save("sound\ex_" + tfile + ".mp3")
        self.thPlayer = MyPlayer(-1, tfile, parent=self)
        self.thPlayer.start()

    def mouseDoubleClickEvent(self, event) :
        print("doubleclick")
        self.thPlayer.terminate()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = CompletClass() 
    myWindow.show()
    app.exec_()