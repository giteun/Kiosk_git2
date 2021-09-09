# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 00:01:08 2021

@author: eiprw
"""
from PyQt5.QtCore import *
import pygame
from gtts import gTTS
import os
import time
import shutil

class MyTimer(QThread):
    thread_timer = pyqtSignal(int) #사용자 정의 시그널
    def __init__(self, sec, parent = None):
        super(MyTimer, self).__init__(parent)
        self.working = True
        self.sec = sec
 
    def run(self): #thread.start()하면 실행
        if self.working :
            while True :
                self.sec += 1
                self.thread_timer.emit(int(self.sec)) #사용자 정의 시그널 발생
                #print(self.sec)
                self.sleep(1)
        else :
            self.terminate()
            self.quit()

class MyPlayer(QThread):
    def __init__(self, num, file, parent = None):
        super(MyPlayer, self).__init__(parent)
        self.working = True
        self.num = num
        self.file = file

    def run(self): #thread.start()하면 실행
        if self.working :
            if self.num == -1 :
                music_file = "sound\ex_" + self.file + ".mp3"
            else :
                music_file = "sound\ex_mn_{0}.mp3".format(self.num)
            pygame.mixer.init()
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()
        else :
            self.terminate()
            self.quit()


class MyPlayer_B(QThread):
    def __init__(self, num, cal, parent=None):
        super(MyPlayer_B, self).__init__(parent)
        self.working = True
        self.num = num
        self.cal = cal

    def run(self):  # thread.start()하면 실행
        if self.working:
            if self.cal == "normal":
                music_file = "sound_basket\ex_mn_{0}.mp3".format(self.num)
                pygame.mixer.init()
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play()

            elif self.cal == "guide_change":
                music_file = "sound_basket\change_num.mp3"
                pygame.mixer.init()
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play()
                time.sleep(5)
                pygame.mixer.music.unload()


        else:
            self.terminate()
            self.quit()
