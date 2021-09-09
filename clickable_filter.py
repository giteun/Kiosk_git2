# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 15:01:49 2021

@author: eiprw
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QObject, QEvent, pyqtSignal

#라벨을 클릭하면 동작하는 함수(아래 링크 참고)
#https://developer-mistive.tistory.com/55
#https://jung-max.github.io/2020/06/16/Python-pyqt5-%EC%9D%B4%EB%AF%B8%EC%A7%80%ED%81%B4%EB%A6%AD/
def Clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()	#pyside2 사용자는 pyqtSignal() -> Signal()로 변경
        
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        print("label release")
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True
            
            return False
    
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked
