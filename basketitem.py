# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 15:25:44 2021

@author: eiprw
"""

from dataclasses import dataclass 

@dataclass
class BasketItem :
    tab : str
    name : str
    price : float
    text : str
    num : int