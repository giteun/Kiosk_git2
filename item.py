# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 15:24:54 2021

@author: eiprw
"""
# 참고 https://www.daleseo.com/python-dataclasses/

from dataclasses import dataclass
import os


@dataclass
class Item:
    tab: str
    name: str
    price: float  # tall 기준
    text: str


tabName = ["cold_", "brewed_", "esp_"]
menutxt = [[0 for j in range(1)] for i in range(3)]
menuName = [[0 for j in range(1)] for i in range(3)]
menuPrice = [[0 for j in range(1)] for i in range(3)]
path_dir = './menu/txt'


def search_txt(fname):
    r = open(path_dir + '/{}'.format(fname), mode='r', encoding='utf-8')
    lines = r.readlines()
    list = []
    for i in range(4):
        if i != 2:  # 종류 내용 list에서 제외(나중에 코드 수정하기)
            txt = lines[i]
            list.append(txt.split(':')[1][0:-1])
    return list  # [메뉴 이름,가격,영어 이름]


def ItemOpen():
    menu = []
    for i in range(3):
        menu.append([])
        for j in range(len(menuName[i])):
            menu[i].append(Item(tab=tabName[i], name=menuName[i][j], price=menuPrice[i][j], text=menutxt[i][j]))
    print(menu)
    return menu

menutxt_cold = []
menuPrice_cold = []
menuName_cold = []
menutxt_brewed = []
menuPrice_brewed = []
menuName_brewed = []
menutxt_esp = []
menuPrice_esp = []
menuName_esp = []

for file in os.listdir(path_dir):
    list = []
    # all the files in your directory
    if 'cold_' in file:
        list = search_txt(file)
        menutxt_cold.append(list[0])  # 메뉴 이름
        menuPrice_cold.append(int(list[1]))  # 가격
        menuName_cold.append(list[2])  # 영어 이름
    elif 'brewed_' in file:
        list = search_txt(file)
        menutxt_brewed.append(list[0])  # 메뉴 이름
        menuPrice_brewed.append(int(list[1]))  # 가격
        menuName_brewed.append(list[2])  # 영어 이름
    elif 'esp_' in file:
        list = search_txt(file)
        menutxt_esp.append(list[0])  # 메뉴 이름
        menuPrice_esp.append(int(list[1]))  # 가격
        menuName_esp.append(list[2])  # 영어 이름

menutxt[0] = menutxt_cold
menuName[0] = menuName_cold
menuPrice[0] = menuPrice_cold
menutxt[1] = menutxt_brewed
menuName[1] = menuName_brewed
menuPrice[1] = menuPrice_brewed
menutxt[2] = menutxt_esp
menuName[2] = menuName_esp
menuPrice[2] = menuPrice_esp

"""

@dataclass
class Item :
    tab : str
    name : str
    price : float #tall 기준
    text : str

    tabName = ["cold_", "brewed_", "esp_"]
    menuName = [["brew", "oat", "vanilla", "jeju", "float", "nightro"],
                    ["ice", "drip"],
                    ["conpanna", "caramel", "vanillabean", "cappu", "mocha", "affogato"]]
    menuPrice = [[4500, 5600, 5500, 6800, 8000, 5800], #제주 : grande
                    [4100, 3800], #오늘의 : short
                    [3800, 6500, 7000, 4600, 5100, 7000]] #콘파나 : solo, 아포카토:사이즈없음 
    menutxt = [["콜드 브루", "콜드 브루 오트 라떼", "바닐라크림 콜드 브루", "제주비자림 콜드 브루", "콜드 브루 플로트", "나이트로 콜드 브루"],
                    ["아이스 커피", "오늘의 커피"],
                    ["에스프레소 콘 파나", "아이스카라멜마키아또", "바닐라 빈 라떼", "카푸치노", "아이스 카페 모카", "클래식 아포가토"]]
    menu = []   
    for i in range(3) :
        menu.append([])
        for j in range(len(menuName[i])) :
            menu[i].append(Item(tab = tabName[i], name = menuName[i][j], price = menuPrice[i][j], text = menutxt[i][j]))
    return menu


"""

