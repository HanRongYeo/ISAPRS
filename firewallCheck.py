# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 13:11:50 2020

@author: SheepCurry
"""
import subprocess

def run(data,score):
    
    result = subprocess.check_output('netsh advfirewall show allprofiles state', shell = True)
    string = ""
    for status in result.split()[5::6]:
        temp = status.decode("utf-8")
        if temp == "ON":
            score += (0.0192 + 0.001)
            string += "1-"
        else:
            string += "0-"
    
    string = string[:-1]
    data['firewall'] = string
    return score

def run_exist(data):
    result = subprocess.check_output('netsh advfirewall show allprofiles state', shell = True)
    count=0
    for status in result.split()[5::6]:
        temp = status.decode("utf-8")
        if temp == "ON":
            if data["firewall"][count*2]=="0":
                data["score"] += (0.0192 + 0.001)
                data["firewall"][count*2] = "1"
        else:
            if data["firewall"][count*2]=="1":
                data["score"] -= (0.0192 + 0.001)
                data["firewall"][count*2] = "0"