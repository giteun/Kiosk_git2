# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 14:50:25 2021

@author: eiprw
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic
import pygame
from gtts import gTTS

from mythread import MyTimer, MyPlayer

form_class = uic.loadUiType("message.ui")[0]

class MessageClass(QMainWindow, form_class) :
    msgSignal = pyqtSignal() #사용자 정의 시그널
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet('QMainWindow{background-color: white; border: 1px solid darkgray;}')
        
        self.MakeSound(self.label_message.text())

        self.btnClose.clicked.connect(self.CloseClick)

        self.thTimer = MyTimer(sec=0, parent=self)
        self.thTimer.thread_timer.connect(self.Timer3sec)
        self.thTimer.start()
        
    def CloseClick(self) :
        self.thTimer.working = False
        self.thPlayer.working = False
        self.msgSignal.emit() #사용자 정의 시그널 발생
        self.close()

    def Timer3sec(self, sec) :
        if sec == 3 :
            self.thTimer.terminate()
            self.CloseClick()

    def MakeSound(self, mtext):
        tts = gTTS(
            text=mtext,
            lang='ko', slow=False
        )
        tts.save("sound\ex_message.mp3")
        self.thPlayer = MyPlayer(-1, "message", parent=self)
        self.thPlayer.start()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = basketClass() 
    myWindow.show()
    app.exec_()

