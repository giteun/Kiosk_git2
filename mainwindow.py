# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 00:01:08 2021

@author: eiprw
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import pygame
from gtts import gTTS

from clickable_filter import Clickable
import item
from basketitem import BasketItem
from basket import BasketClass
from message import MessageClass
from mythread import MyTimer, MyPlayer

form_class = uic.loadUiType("mainwindow.ui")[0]

class WindowClass(QMainWindow, form_class) :
    menuList = item.ItemOpen()
    menuImg = [] 
    menuName = []
    menuPrice = []

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # opening window in maximized size
        self.showMaximized()
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)

        #변수 초기화
        self.InitVariable()

        #UI 초기화
        self.InitUI()

        #버튼에 기능을 연결
        self.ConnectClick()
        
        #상태바 사용
        #self.status_bar = self.statusBar()

    def InitVariable(self) :
        self.selmenu = 0 #현재 선택한 메뉴
        self.premenu = 0 #이전에 선택한 메뉴
        self.dblmenu = 0 #더블클릭한 메뉴
        self.doulbeclick_working = False #True : 이전 메뉴 스타일 초기화
        self.row = -1
        self.col = -1
        self.start_xpt = 0
        self.start_ypt = 0
        self.mouse_xpt = 0
        self.mouse_ypt = 0
        self.move_xpt = 0
        self.move_ypt = 0
        self.basketList = []
        self.windowEnable = True
        
        #메뉴 개수 카운트
        self.cntTab = len(self.menuList) #탭 개수
        self.menuTotal = 0 #전체 메뉴 개수
        self.cntMenu = [] #각 탭의 메뉴 개수
        sumIndex = 0
        self.minMenuIndex = [] #각 탭의 최소 selmenu값
        self.maxMenuIndex = [] #각 탭의 최대 selmenu값
        self.basketIndex = []
        for i in range(self.cntTab) :
            self.menuTotal += len(self.menuList[i])
            self.cntMenu.append(len(self.menuList[i]))
            
            self.minMenuIndex.append(sumIndex)
            sumIndex += self.cntMenu[i]
            self.maxMenuIndex.append(sumIndex-1)

            bsklist = [False for _ in range(self.cntMenu[i])] #리스트를 False으로 초기화. True : 장바구니에 담김
            self.basketIndex.append(bsklist)

    def InitUI(self) :
        self.windowEnable = True
        self.setEnabled(self.windowEnable)

        #라벨 스타일 초기화
        self.InitLabelMain()
        self.InitLabelMenu()
        self.InitButton()

        self.centralwidget.setStyleSheet("background-color: white;")
        
        self.groupBox1.setStyleSheet('QGroupBox{background-color: white;}')
        self.groupBox2.setStyleSheet('QGroupBox{background-color: white;}')
        self.groupBox3.setStyleSheet('QGroupBox{background-color: white;}')
        #self.tabWidget.setStyleSheet("color: white;" "background-color: #1B3C35;")

#라벨 변경에 사용되는 함수
    #라벨 이미지 초기화
    def InitLabelMain(self) :
        self.labelMain.setPixmap(QPixmap("image/starbucksBar_resize2.png"))
        self.labelMain.setText("")
        self.labelMain.setStyleSheet("")
    
    #selmenu를 menu배열의 인덱스로 변환
    def SelmenuToMenu(self, index) :
        for i in range(self.cntTab) :
            if index > self.cntMenu[i]-1 :
                index -= self.cntMenu[i]
            else :
                break
        self.row = i
        self.col = index
    
    #배열 menu의 인덱스를 selmenu로 변환
    def MenuToSelmenu(self, r, c) :
        index = 0
        if r == 0 :
            index += c
        else :
            for i in range(r) :
                index += self.cntMenu[i]
            index += c

        return index

    #라벨 초기화(다른 파일로 빼야 할 듯)
    def InitLabelMenu(self) :
        #새 QLabel을 생성해서 labelMenu라는 배열에 하나씩 추가
        for i in range(self.menuTotal + 2) : # 주문버튼과 뒤로가기 버튼 포함
            self.menuImg.append(QLabel())
            self.menuName.append(QLabel())
            self.menuPrice.append(QLabel())
        
        groupBox = []
        for i in range(self.cntTab) :
            gLayout = QGridLayout()

            for j in range(self.cntMenu[i]) :
                index = self.MenuToSelmenu(i, j)
                
                vBox = QVBoxLayout()
                vBox.setContentsMargins(0,0,0,0)
                vBox.setSpacing(0)
                vBox.addWidget(self.menuImg[index], alignment=Qt.AlignCenter)
                vBox.addWidget(self.menuName[index], alignment=Qt.AlignCenter)
                vBox.addWidget(self.menuPrice[index], alignment=Qt.AlignCenter)

                groupBox.append(QGroupBox())
                groupBox[index].setLayout(vBox)

                quotient = j // 2
                remainder = j % 2
                gLayout.addWidget(groupBox[index], quotient, remainder)

            vSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            gLayout.addItem(vSpacer)

            if i == 0 : self.groupBox1.setLayout(gLayout)
            elif i == 1 : 
                
                self.groupBox2.setLayout(gLayout)
            elif i == 2 : self.groupBox3.setLayout(gLayout)

        #라벨에 이미지 출력
        self.pix = QPixmap()
        z = 0
        for i in range(self.cntTab) :
            for j in range(self.cntMenu[i]) :
                fileName = "image/" + self.menuList[i][j].tab + self.menuList[i][j].name + ".png"
                self.pix.load(fileName)
                self.pix = self.pix.scaled(150,150)
                self.menuImg[z].setPixmap(self.pix)
                z += 1

        #라벨에 메뉴이름 출력
        for i in range(self.menuTotal) :
            self.SelmenuToMenu(i)
            self.menuName[i].setText(self.menuList[self.row][self.col].text)
            self.menuPrice[i].setText(str(self.menuList[self.row][self.col].price))
        
        #주문버튼과 뒤로가기버튼 설정
        self.menuImg[self.menuTotal] = self.btnOrder #주문버튼
        self.menuImg[self.menuTotal+1] = self.btnBack #뒤로가기버튼
        self.menuName[self.menuTotal] = "주문" #주문버튼
        self.menuName[self.menuTotal+1] = "뒤로가기" #뒤로가기버튼
        self.menuPrice[self.menuTotal] = 0
        self.menuPrice[self.menuTotal+1] = 0
        self.pix.load("image/buttonOrder_text.png")
        self.menuImg[z].setPixmap(self.pix) 
    
#버튼 작동에 사용되는 함수
    #버튼 스타일 초기화
    def InitButton(self) : 
        self.InitLabelMain()

        self.menuImg[0].setStyleSheet("border-style: solid;" #
                        "border-width: 4px;"
                        "border-color: #6799FF;" #blue
                        "border-radius: 3px")
        self.MakeSound(self.menuList[0][0].text, self.menuList[0][0].price, 0)
        for i in range(1, self.menuTotal + 2) :
            self.menuImg[i].setStyleSheet("border-style: solid;"
                        "border-width: 4px;"
                        "border-color: white;"
                        "border-radius: 3px")
        #self.groupBox1_1.setStyleSheet("QGroupBox#groupBox1_1 { border: 5px solid white;}")
            
    #버튼 스타일 지정
    def ButtonStyle(self) :
        self.SelmenuToMenu(self.premenu)
        if self.doulbeclick_working == False and self.premenu != -1 :
            if self.basketIndex[self.row][self.col] :
                self.menuImg[self.premenu].setStyleSheet("border-style: solid;"
                            "border-width: 4px;"
                            "border-color: #FF5A5A;" #red
                            "border-radius: 3px")
            else :
                self.menuImg[self.premenu].setStyleSheet("border-style: solid;"
                            "border-width: 4px;"
                            "border-color: white;"
                            "border-radius: 3px")
        
        self.SelmenuToMenu(self.selmenu)
        if self.basketIndex[self.row][self.col] :
            self.menuImg[self.selmenu].setStyleSheet("border-style: solid;"
                        "border-width: 4px;"
                        "border-color: #FF5A5A #6799FF;" #FF5A5A : red, 6799FF : blue
                        "border-radius: 3px")
        else :
            self.menuImg[self.selmenu].setStyleSheet("border-style: solid;"
                        "border-width: 4px;"
                        "border-color: #6799FF;" #blue
                        "border-radius: 3px")

        self.doulbeclick_working = False
        self.ChangeLabelMain()
        self.TimerStop()

    #버튼 선택에 따른 메인라벨 변경
    def ChangeLabelMain(self) :
        #현재 탭 위치 변경
        for i in range(self.cntTab):
            if self.selmenu >= self.minMenuIndex[i] and self.selmenu <= self.maxMenuIndex[i] :
                self.tabWidget.setCurrentIndex(i)
        
        #현재 스크롤 위치 변경
        if self.selmenu < self.menuTotal :
            scroll = []
            scroll.append(self.scrollArea1.verticalScrollBar())
            scroll.append(self.scrollArea2.verticalScrollBar())
            scroll.append(self.scrollArea3.verticalScrollBar())
            vScrollBar = scroll[self.row]
            if self.col//2 == 0 :
                vScrollBar.setValue(0)
            elif self.col//2 > 1 :
                #scrollValue = (vScrollBar.maximum() // 3) * (self.col//2)
                vScrollBar.setValue(vScrollBar.maximum())
            
    #버튼 클릭시 함수 연결
    def ConnectClick(self) :
        Clickable(self.btnOrder).connect(self.OrderClick)
        Clickable(self.btnBack).connect(self.BackClick)
    

    #주문 버튼 클릭시 동작하는 함수
    def OrderClick(self) :
        self.premenu = self.selmenu
        self.selmenu = self.maxMenuIndex[self.cntTab-1] + 1
        self.basketList.clear() #리스트 초기화
        for i in range(self.cntTab) :
            for j in range(self.cntMenu[i]) :
                if self.basketIndex[i][j] == True:
                    self.basketList.append(BasketItem(tab = self.menuList[i][j].tab, 
                                        name = self.menuList[i][j].name, 
                                        price = self.menuList[i][j].price, 
                                        text = self.menuList[i][j].text,
                                        num = 1))
        
        if len(self.basketList) == 0 :
            self.windowEnable = False
            self.setEnabled(self.windowEnable)
            self.ui = MessageClass()
            self.ui.msgSignal.connect(self.WindowEnabled)
        else :
            self.ui = BasketClass(self.basketList)

        self.ButtonStyle()
        self.ui.show()

    #message.ui의 btnClose을 누르면 동작(msgSignal.emit()되면 동작)
    @pyqtSlot()
    def WindowEnabled(self) :
        self.windowEnable = True
        self.setEnabled(self.windowEnable)

    def BackClick(self) :
        print("close")
        self.selmenu = self.maxMenuIndex[self.cntTab-1] + 2
        self.close()

    #마우스 클릭할 때
    def mousePressEvent(self, event):
        #스타트 좌표 저장
        self.start_xpt = event.x()
        self.move_xpt = 0
        self.start_ypt = event.y()
        self.move_ypt = 0

        #더블 클릭할 메뉴 저장
        self.dblmenu = self.selmenu

        #타이머 스레드 시작
        self.thTimer = MyTimer(sec=0, parent=self)
        self.thTimer.thread_timer.connect(self.ShowLabelMain)
        self.thTimer.start()
        
        #print("Mouse Start Point : x={0}".format(self.start_xpt))

    @pyqtSlot(int)
    def ShowLabelMain(self, sec) :
        print("press mouse : " + str(sec))
        if sec == 2 :
            #상단에 라벨 출력
            label = self.menuList[self.row][self.col].text + " " + str(self.menuList[self.row][self.col].price)
            self.labelMain.setText(label)
            self.labelMain.setStyleSheet("background-color: black;"
                        "color: white;"
                        "font: bold 30px;"
                        "text-align: center;")

    #마우스를 클릭한 채로 움직일 때 좌표 출력
    def mouseMoveEvent(self, event):
        self.mouse_xpt = event.x()
        #self.status_bar.showMessage("Mouse Point : x={0}".format(self.mouse_xpt))
        self.move_xpt = self.mouse_xpt - self.start_xpt

        if self.selmenu < self.menuTotal :
            self.mouse_ypt = event.y()
            self.move_ypt = self.mouse_ypt - self.start_ypt

    #마우스를 놓을 때 좌표 비교
    def mouseReleaseEvent(self, event):
        print("release")
        self.TimerStop()

        #상단 라벨 초기화
        self.InitLabelMain()
        if self.selmenu != -1 :
            if self.move_xpt >= 100:
                print("Slide to the right")
                if self.selmenu != self.maxMenuIndex[self.cntTab-1] + 2 :
                    self.premenu = self.selmenu
                    self.selmenu += 1
                    self.VoiceOutput()
            elif self.move_xpt <= -100:
                print("Slide to the left ")
                if self.selmenu != self.minMenuIndex[0] :
                    self.premenu = self.selmenu
                    self.selmenu -= 1
                    self.VoiceOutput()
            elif self.move_ypt >= 100:
                print("Slide down")
                self.premenu = self.selmenu
                self.selmenu = self.maxMenuIndex[self.cntTab-1] + 1
                self.VoiceOutput()
            else : print("Motionless")

    def TimerStop(self) :
        self.thTimer.terminate()
        self.thTimer.working = False

    def VoiceOutput(self) :
        self.ButtonStyle()
        if self.selmenu <= self.maxMenuIndex[self.cntTab-1] :    
            self.MakeSound(self.menuList[self.row][self.col].text, self.menuList[self.row][self.col].price, self.selmenu)
        else : 
            self.MakeSound(self.menuName[self.selmenu], self.menuPrice[self.selmenu], self.selmenu)

    def MakeSound(self, mname, mprice, num):
        if mprice != 0 :
            mtext = mname + str(mprice) + "원"
        else :
            mtext = mname + "버튼"

        tts = gTTS(
            text=mtext,
            lang='ko', slow=False
        )
        tts.save("sound\ex_mn_{0}.mp3".format(num))
        self.thPlayer = MyPlayer(num, "", parent=self)
        self.thPlayer.start()

#메뉴 주문에 사용되는 함수          
    #위젯에서 더블클릭하면 선택한 메뉴버튼 실행
    def mouseDoubleClickEvent(self, event) :
        print("doubleclick")
        self.doulbeclick_working = True

        if self.dblmenu != -1 :
            #메뉴를 더블클릭했을 때
            if self.selmenu <= self.maxMenuIndex[self.cntTab-1] :
                self.SelmenuToMenu(self.dblmenu)
                if self.basketIndex[self.row][self.col] :
                    self.basketIndex[self.row][self.col] = False
                    self.menuImg[self.dblmenu].setStyleSheet("border-style: solid;"
                                "border-width: 4px;"
                                "border-color: white;")
                    self.menuName[self.dblmenu].setStyleSheet("color: black;")
                    self.menuPrice[self.dblmenu].setStyleSheet("color: black;")
                else :
                    self.basketIndex[self.row][self.col] = True
                    self.menuImg[self.dblmenu].setStyleSheet("border-style: solid;"
                                "border-width: 4px;"
                                "border-color: #FF5A5A;" #FF5A5A : red
                                "border-radius: 3px")
                    self.menuName[self.dblmenu].setStyleSheet("color: #FF5A5A; font-weight: bold;")
                    self.menuPrice[self.dblmenu].setStyleSheet("color: #FF5A5A; font-weight: bold;")
            #버튼을 더블클릭 했을 때
            else :
                if self.selmenu == self.maxMenuIndex[self.cntTab-1] + 1 : #주문버튼
                    self.OrderClick()
                else :
                    self.BackClick()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()