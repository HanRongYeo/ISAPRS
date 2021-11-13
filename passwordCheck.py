# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 14:28:18 2020

@author: SheepCurry
"""

import re

def run(data, password, score):
    
    upper=False
    lower=False
    result = ""
    
    result = str(len(password))+"-"
     
    if re.search("[A-Z]",password):
        upper=True
    if re.search("[a-z]",password):
        lower=True       
    if upper==True and lower == True:
        result = result + "3-"
        score += 0.23/3/4
    elif upper == True and lower == False:
        result = result + "2-"
        score += 0.23/3/4/2
    elif upper == False and lower == True:
        result = result + "1-"
        score += 0.23/3/4/2
    else:
        result = result + "0-"      
    if re.search("[0-9]",password):
        result = result + "1-"
        score += 0.23/3/4
    else:
        result = result + "0-"      
    if re.search("[ !#$%&'()*+,-./:;<=>?@[\]^_`{|}~]",password):
        result = result + "1"
        score += 0.23/3/4
    else:
        result = result + "0"
        
    data['password']=result
    return score

def getPasswordRecomFlag(data):
    passArr = data["password"].split("-")
    flag = False
    if int(passArr[0])<8:
        flag=True
    if int(passArr[1])<3:
        flag=True
    if not (int(passArr[2]) and int(passArr[3])):
        flag=True
        
    return flag
        