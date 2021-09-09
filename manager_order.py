import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from dataclasses import dataclass
import os

form_class = uic.loadUiType("./manager.ui")[0]

class WindowClass(QMainWindow, form_class):
    checkBoxList = []
    checkBoxList_Flag = []
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # opening window in maximized size
        self.showMaximized()
        
        self.pushButton_add.clicked.connect(self.pushButtonClicked)
        self.pushButton_remove.clicked.connect(self.pushButtonClicked_r)
        # 테이블 간격 조정
        self.tableWidget.setColumnWidth(0, self.width() * 1 / 10)
        self.tableWidget.setColumnWidth(1, self.width() * 1 / 5)
        self.tableWidget.setColumnWidth(2, self.width() * 1 / 5)
        self.tableWidget.setColumnWidth(3, self.width() * 1 / 5)
        self.tableWidget.setColumnWidth(4, self.width() * 1 / 5)
        # txt 폴더 내의 메뉴들을 백업해온다
        path_dir = './menu/txt'
        for file in os.listdir(path_dir):
            r = open(path_dir + '/{}'.format(file), mode='r', encoding='utf-8')
            lines = r.readlines()
            list=[]
            for i in range(4):
                txt = lines[i]
                list.append(txt.split(':')[1][0:-1])
            self.insert_item(list[0], list[1], list[2], file.split('.')[0])
        print(self.tableWidget.rowCount() - 1)
        for i in range(self.tableWidget.rowCount()):
            self.make_checkbox(i)
        for i in range(self.tableWidget.rowCount()):
            self.checkBoxList[i].stateChanged.connect(self.checkBoxState)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

    # '제품 추가하기' 버튼 누르면
    def pushButtonClicked(self):
        dlg = LogInDialog()
        dlg.exec_()
        if dlg.name and dlg.price and dlg.kinds and dlg.file_path is not None:
        #dlg에서 입력된 변수 저장
            self.name = dlg.name
            self.price = dlg.price
            self.kinds = dlg.kinds
            self.file_path = dlg.file_path
            self.name_eng = self.file_path.split('/')[-1].split('.')[0]
            #dlg에서 입력된 변수 table에 나타냄
            self.insert_item(self.name,self.price,self.kinds,self.name_eng)
            #check box 생성
            self.make_checkbox(self.tableWidget.rowCount()-1)
            f = open('./menu/txt/{}.txt'.format(self.name_eng), mode='wt', encoding='utf-8')
            f.write('name:{0}\nprice:{1}\nkinds:{2}\neng_name:{3}\nfile_path:{4}'.format(self.name,self.price,self.kinds,self.name_eng.split('_')[1],self.file_path))
            f.close()
            for i in range(self.tableWidget.rowCount()):
                self.checkBoxList[i].stateChanged.connect(self.checkBoxState)

    #table에 메뉴명을 나타냄
    def insert_item(self, name, price, kinds, name_eng):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        #self.label.setText("%s" %(file_path))
        self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(name))
        self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(price))
        self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(kinds))
        self.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(name_eng))
        #self.label.setText("이름: %s 가격: %s 종류: %s" % (name, price, kinds))

    def make_checkbox(self, num):
        ckbox = QCheckBox()
        self.checkBoxList.append(ckbox)
        self.checkBoxList_Flag.append(False)
        self.tableWidget.setCellWidget(num, 0, self.checkBoxList[num])

    def checkBoxState(self):
        for i in range(self.tableWidget.rowCount()):
            if self.checkBoxList[i].isChecked() == True:
               self.checkBoxList_Flag[i] = True
            elif self.checkBoxList[i].isChecked() == False:
                self.checkBoxList_Flag[i] = False
            #print(self.checkBoxList)

    # '제품 삭제하기' 버튼 누르면
    def pushButtonClicked_r(self):
        for i in range(self.tableWidget.rowCount()):
            if self.checkBoxList_Flag[i] == True:
                it = self.tableWidget.item(i, 4)
                name_en = it.text() if it is not None else ""
                print(it)
                print(name_en)
                os.remove('./menu/txt/{}.txt'.format(name_en))
                self.tableWidget.removeRow(i)
                del self.checkBoxList[i]
                self.checkBoxState()

#메뉴 추가하기 버튼 누르면 뜨는 dialog
class LogInDialog(QDialog):
    #items = {'콜드 브루', '브루드', '에스프레소'}
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.name = None
        self.price = None
        self.kinds = None
        self.file_path = None
        self.fname = None

    def setupUI(self):
        self.setGeometry(1100, 200, 500, 300)
        self.setWindowTitle("등록하기")

        label_name = QLabel("메뉴명: ")
        label_price = QLabel("가격: ")
        label_kinds = QLabel("종류: ")

        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.combo = QComboBox(self)
        self.combo.addItem(' ')
        self.combo.addItem('콜드 브루')
        self.combo.addItem('브루드')
        self.combo.addItem('에스프레소')

        #item, ok = QInputDialog.getItem(self, items)
        self.pushButton1= QPushButton("Sign In")
        self.pushButton1.clicked.connect(self.pushButtonClicked)
        self.pushButton2 = QPushButton("이미지 파일 불러오기")
        self.pushButton2.clicked.connect(self.pushButtonClicked_file)
        layout = QGridLayout()
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(self.pushButton1, 0, 2)
        layout.addWidget(label_price, 1, 0)
        layout.addWidget(self.lineEdit2, 1, 1)
        layout.addWidget(label_kinds, 2, 0)
        layout.addWidget(self.combo, 2, 1)
        layout.addWidget(self.pushButton2, 3, 1)

        self.setLayout(layout)

    def pushButtonClicked(self):
        msg = QMessageBox()
        self.name = self.lineEdit1.text()
        self.price = self.lineEdit2.text()
        self.kinds = self.combo.currentText()
        if self.fname:
            self.file_path = self.fname[0]
        #elif self.fname:
        #file = open("{}.txt".format(name),mode = 'w')
        if self.name is None or self.price is None or self.kinds is None or self.fname is None:
            msg.setWindowTitle("경고")
            msg.setText("입력되지 않은 항목이 있습니다.")
            x = msg.exec_()
        else :
            self.close()


    def pushButtonClicked_file(self):
        self.fname=QFileDialog.getOpenFileName(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
