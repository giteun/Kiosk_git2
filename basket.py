# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 14:50:25 2021

@author: eiprw
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import uic
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap                               
from gtts import gTTS

from clickable_filter import Clickable                                 
from mythread import MyPlayer_B
from paymethod import PaymethodClass
import pygame
import os
from datetime import datetime

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("Dialog_basket.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class BasketClass(QMainWindow, form_class):
    nowColum = 0
    totalPrice = 0
    def __init__(self, basketList):
        super().__init__()

        self.setupUi(self)
        # opening window in maximized size
        self.showMaximized()
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.basketList_1 = basketList
        self.InitUI() 
        self.InitTable(basketList)
        Clickable(self.btnOrder_step1).connect(self.btnOrder_step1Click)
        Clickable(self.btnBack_step1).connect(self.btnBack_step1Click)

        # 참고:https://stackoverflow.com/questions/53081391/mousepressevent-doesnt-work-on-child-widgets
        # 메인윈도우 내의 childwidget에서도 mouse event 사용 가능하도록
        for w in self.findChildren(QWidget) + [self]:
            w.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.buttons() & Qt.LeftButton:
                self.start_x = event.x()
                self.start_y = event.y()
                self.move_x = 0
                self.move_y = 0
        elif event.type() == QEvent.MouseMove:
            self.mouse_x = event.x()
            self.mouse_y = event.y()
            self.move_x = self.mouse_x - self.start_x
            self.move_y = self.mouse_y - self.start_y
        elif event.type() == QEvent.MouseButtonRelease:
            # 좌우 슬라이드
            if self.move_x >= 100:
                print("Slide to the right")
                self.setColortoRow("Right")
            elif self.move_x <= -100:
                print("Slide to the left")
                self.setColortoRow("Left")
            else:
                pass  # print("x Motionless")
            # 상하 슬라이드
            if self.move_y >= 100:
                print("Slide down")
                if self.nowColum == self.tableWidget.rowCount():
                    self.change_num(self.nowColum, "sub", False)
                else :
                    self.change_num(self.nowColum, "sub", True)
            elif self.move_y <= -100:
                print("Slide up")
                if self.nowColum == self.tableWidget.rowCount():
                    self.change_num(self.nowColum, "add", False)
                else:
                    self.change_num(self.nowColum, "add", True)
        
        elif event.type() == QEvent.MouseButtonDblClick :
            if self.nowColum == self.tableWidget.rowCount() + 1 :
                self.btnOrder_step1Click()
            elif self.nowColum == self.tableWidget.rowCount() + 2 :
                self.btnBack_step1Click()

        return super(BasketClass, self).eventFilter(obj, event)

    def InitUI(self) :
        pix = QPixmap()
        pix.load("image/buttonOrder_step.png")
        self.btnOrder_step1.setPixmap(pix)       

    # tableWidget 초기화
    def InitTable(self, basketList):
        for i in range(len(basketList)):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(basketList[i].text))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(basketList[i].num)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(basketList[i].price) + "원"))

            self.totalPrice += basketList[i].price

        print("total :" + str(self.totalPrice))

        self.tableWidget_total.setItem(0, 1, QTableWidgetItem(str(self.totalPrice) + "원"))
        for j in range(self.tableWidget.columnCount()): # 0번째 행 분홍색
            self.tableWidget.item(0, j).setBackground(QtGui.QColor(255, 0, 127))
        self.MakeSound(basketList[0].text, basketList[0].price, basketList[0].num, " ") # 0번째 행 읽어줌
    
    # 수량 변경
    def change_num(self, Colnumber, Cal, flag):
        if flag == True:
            if Cal == "add":  # 덧셈
                self.basketList_1[Colnumber].num += 1
                self.totalPrice += self.basketList_1[Colnumber].price
                # print(self.basketList_1)
            elif Cal == "sub":  # 뺄셈
                self.basketList_1[Colnumber].num -= 1
                self.totalPrice -= self.basketList_1[Colnumber].price
                # print(self.basketList_1)
                if (self.basketList_1[Colnumber].num < 0):
                    self.basketList_1[Colnumber].num = 0
            self.tableWidget.setItem(Colnumber, 1, QTableWidgetItem(str(self.basketList_1[Colnumber].num)))
            self.tableWidget.setItem(Colnumber, 2, QTableWidgetItem(
                str(self.basketList_1[Colnumber].price * self.basketList_1[Colnumber].num) + "원"))
            self.tableWidget_total.setItem(0, 1, QTableWidgetItem(str(self.totalPrice) + "원"))

            self.tableWidget.item(self.nowColum, 1).setBackground(QtGui.QColor(255, 0, 127))
            self.tableWidget.item(self.nowColum, 2).setBackground(QtGui.QColor(255, 0, 127))
            # self.thPlayer = MyPlayer_B(self.nowColum, "guide_change", parent=self)
            # self.thPlayer.start()
            self.MakeSound(self.basketList_1[self.nowColum].text,
                           self.basketList_1[self.nowColum].price * self.basketList_1[Colnumber].num,
                           self.basketList_1[self.nowColum].num, "수량이 변경되었습니다.")
        else:
            pass
        
    # 행의 색깔 지정
    def setColortoRow(self, Direction):
        if Direction == "Right": #오른쪽 슬라이드
            self.nowColum += 1
            if self.nowColum < self.tableWidget.rowCount():
                for j in range(self.tableWidget.columnCount()):
                    self.tableWidget.item(self.nowColum - 1, j).setBackground(QtGui.QColor(255, 255, 255)) #흰색
                for j in range(self.tableWidget.columnCount()):
                    self.tableWidget.item(self.nowColum, j).setBackground(QtGui.QColor(255, 0, 127)) #분홍색
            elif self.nowColum == self.tableWidget.rowCount():
                self.ButtonStyle_Step1("total", "select")
                
                for j in range(self.tableWidget.columnCount()):
                    self.tableWidget.item(self.tableWidget.rowCount()-1, j).setBackground(QtGui.QColor(255, 255, 255))
            elif self.nowColum == self.tableWidget.rowCount() + 1:
                self.ButtonStyle_Step1("order", "select")
                self.ButtonStyle_Step1("total", "init")
                self.MakeSound("결제", -1, 0, " ")
            else :
                self.nowColum = self.tableWidget.rowCount() + 2 
                self.ButtonStyle_Step1("order", "init")
                self.ButtonStyle_Step1("back", "select")
                self.MakeSound("뒤로가기", -1, 0, " ")

        elif Direction == "Left" :
            self.nowColum -= 1
            if self.nowColum >= 0:
                if self.nowColum < self.tableWidget.rowCount()-1:
                    for j in range(self.tableWidget.columnCount()):
                        self.tableWidget.item(self.nowColum + 1, j).setBackground(QtGui.QColor(255, 255, 255))
                    for j in range(self.tableWidget.columnCount()):
                        self.tableWidget.item(self.nowColum, j).setBackground(QtGui.QColor(255, 0, 127))
                elif self.nowColum == self.tableWidget.rowCount() - 1 :
                    for j in range(self.tableWidget.columnCount()):
                        self.tableWidget.item(self.nowColum, j).setBackground(QtGui.QColor(255, 0, 127))
                    self.ButtonStyle_Step1("total", "init")
                elif self.nowColum == self.tableWidget.rowCount() :
                    self.ButtonStyle_Step1("order", "init")
                    self.ButtonStyle_Step1("total", "select")
                elif self.nowColum == self.tableWidget.rowCount() + 1: 
                    self.ButtonStyle_Step1("back", "init")
                    self.ButtonStyle_Step1("order", "select")
                    self.MakeSound("결제", -1, 0, " ")

            elif (self.nowColum < 0) :
                self.nowColum = 0

        if self.nowColum < self.tableWidget.rowCount() :
            self.MakeSound(self.basketList_1[self.nowColum].text, self.basketList_1[self.nowColum].price,
                           self.basketList_1[self.nowColum].num, " ")
        elif self.nowColum == self.tableWidget.rowCount() :
            self.MakeSound(" ", self.totalPrice, -1, "최종 결제 금액은 ")


    def MakeSound(self, mname, mprice, count, guide):
        if mprice == -1 :
            mtext = guide + mname + "버튼"
        else :
            if (count < 0):
                mtext = guide + str(mprice) + "원" + "입니다."
            else :
                mtext = guide + mname + str(count) + "개" + str(mprice) + "원"
        tts = gTTS(
            text = mtext,
            lang = 'ko', slow=False
        )
        date_string = datetime.now().strftime("%d%m%Y%H%M%S")
        txt = "sound_basket\ex_mn_" + date_string + ".mp3"
        tts.save(txt)
        self.thPlayer = MyPlayer_B(date_string, "normal", parent=self)
        self.thPlayer.start()

    def ButtonStyle_Step1(self, bname, setting) :
        if bname == "order" :
            if setting == "init" :
                self.btnOrder_step1.setStyleSheet("border-style: solid;"
                        "border-width: 4px;"
                        "border-color: white;" #blue
                        "border-radius: 3px")
            else :
                self.btnOrder_step1.setStyleSheet("border-style: solid;"
                        "border-width: 4px;"
                        "border-color: #6799FF;" #blue
                        "border-radius: 3px")
        elif bname == "back" :
            if setting == "init" :
                self.btnBack_step1.setStyleSheet("border-style: solid;"
                        "border-width: 4px;"
                        "border-color: white;" #blue
                        "border-radius: 3px")
            else :
                self.btnBack_step1.setStyleSheet("border-style: solid;"
                        "border-width: 4px;"
                        "border-color: #6799FF;" #blue
                        "border-radius: 3px")
        else : #total
            if setting == "init" :
                for j in range(self.tableWidget_total.columnCount()):
                    self.tableWidget_total.item(0, j).setBackground(QtGui.QColor(255, 255, 255))
            else :
                for j in range(self.tableWidget_total.columnCount()):
                    self.tableWidget_total.item(0, j).setBackground(QtGui.QColor(255, 0, 127))
    
    #결제 버튼 선택시 동작
    def btnOrder_step1Click(self) :
        self.ui = PaymethodClass()
        self.ui.show()

    #뒤로가기 버튼 선택시 동작
    def btnBack_step1Click(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = BasketClass()
    myWindow.show()
    app.exec_()