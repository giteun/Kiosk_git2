# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from gtts import gTTS

from takeout import TakeoutClass
from mythread import MyPlayer

form_class = uic.loadUiType("pay_screen.ui")[0]

class PaymethodClass(QMainWindow, form_class) :
    btnName = ["btnCard", "btnCoupon", "btnBack"]
    btnText = ["신용카드 결제", "모바일 쿠폰", "뒤로가기"]
    btnList = []

    def __init__(self) :
        super().__init__()
        
        self.setupUi(self)
        # opening window in maximized size
        self.showMaximized()
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.InitUi()
        self.MakeSound(self.label.text(), -1)

    def InitUi(self) :
        self.selbtn = -1
        self.prebtn = -1
        self.setStyleSheet("color: white;"
                    "background-color: #1B3C35;")
        #self.centralwidget.setStyleSheet("background-color: white;")
        
        for i in range(len(self.btnName)) :
            self.btnList.append(QLabel())
        self.btnList[0] = self.btnCard
        self.btnList[1] = self.btnCoupon
        self.btnList[2] = self.btnBack
        for i in range(3) :
            self.btnList[i].setText(self.btnText[i])
            fileName = "image/" + self.btnName[i] + ".png"
            self.btnList[i].setPixmap(QPixmap(fileName))
            
    def BtnCardClick(self):
        print("신용카드 결제")
        self.MoveUI()

    def BtnCouponClick(self):
        print("모바일 쿠폰")
        self.MoveUI()

    def MoveUI(self) :
        self.ui = TakeoutClass()
        self.ui.show()

    def BtnBackClick(self) :
        self.close()

#마우스 이벤트
    def mousePressEvent(self, event):
        self.start_pt = event.x()
        self.move_pt = 0

    def mouseMoveEvent(self, event):
        self.mouse_pt = event.x()
        self.move_pt = self.mouse_pt - self.start_pt

    def mouseReleaseEvent(self, event):
        print("release")
        if self.move_pt >= 100:
            print("Slide to the right")
            if self.selbtn != 2 :
                self.prebtn = self.selbtn
                self.selbtn += 1
                self.VoiceOutput()
        elif self.move_pt <= -100:
            print("Slide to the left ")
            if self.selbtn != 0 :
                self.prebtn = self.selbtn
                self.selbtn -= 1
                self.VoiceOutput()
                
        else : print("Motionless")

    def VoiceOutput(self) :
        self.ButtonStyle() 
        self.MakeSound(self.btnText[self.selbtn], self.selbtn)

    def ButtonStyle(self) :
        self.btnList[self.prebtn].setStyleSheet("border-style: solid;"
                            "border-width: 4px;"
                            "border-color: white;"
                            "border-radius: 3px")
        self.btnList[self.selbtn].setStyleSheet("border-style: solid;"
                        "border-width: 4px;"
                        "border-color: #6799FF;" #blue
                        "border-radius: 3px")

    def MakeSound(self, pname, num):
        if num == -1 :
            ptext = pname
        else :
            ptext = pname + "버튼"
        tts = gTTS(
            text=ptext,
            lang='ko', slow=False
        )
        pfile = "pay{0}". format(num)
        tts.save("sound\ex_" + pfile + ".mp3")
        self.thPlayer = MyPlayer(-1, pfile, parent=self)
        self.thPlayer.start()

    def mouseDoubleClickEvent(self, event) :
        print("doubleclick")
        self.thPlayer.terminate()
        if self.selbtn == 0 : self.BtnCardClick()
        elif self.selbtn == 1 : self.BtnCouponClick()
        elif self.selbtn == 2 : self.BtnBackClick()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = PaymethodClass() 
    myWindow.show()
    app.exec_()