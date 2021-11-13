# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 15:52:37 2021

@author: SheepCurry
"""
import subprocess

def run(data,score):
    p = subprocess.Popen(["powershell.exe", "Get-LocalUser"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
        
    out,err = p.communicate()
    out_str = out.decode("utf-8")
    outLines = out_str.split("\n")
    user=""
    status=""
    p.terminate()
    for line in outLines:
        if "True" in line:
            user = line.split("True")[0].strip(" ")
    
    if user:
        p2 = subprocess.Popen(["powershell.exe", "Get-LocalUser -Name %s | select *"%user],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out2,err2 = p2.communicate()
        out_str2 = out2.decode("utf-8")
        outLines2 = out_str2.split("\n")
        p2.terminate()
        for line in outLines2:
            if "PasswordLastSet" in line:
                status = line.split(" : ")[1].split(" ")[0]
                
        if status.isspace():
            data["com_pass"]= 0
        
        else:
            data["com_pass"] = 1                    
            score += 0.23/3/4
        return score
    
    else:
        data["com_pass"]= 0
        data["com_days"]= -1
        return score
        #return data
        
def run_exist(data):
    p = subprocess.Popen(["powershell.exe", "Get-LocalUser"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
        
    out,err = p.communicate()
    out_str = out.decode("utf-8")
    outLines = out_str.split("\n")
    user=""
    status=""
    p.terminate()
    for line in outLines:
        if "True" in line:
            user = line.split("True")[0].strip(" ")
    
    if user:
        p2 = subprocess.Popen(["powershell.exe", "Get-LocalUser -Name %s | select *"%user],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out2,err2 = p2.communicate()
        out_str2 = out2.decode("utf-8")
        outLines2 = out_str2.split("\n")
        p2.terminate()
        for line in outLines2:
            if "PasswordLastSet" in line:
                status = line.split(" : ")[1].split(" ")[0]
                
        if status.isspace() and data["com_pass"]==1:
            data["com_pass"]= 0
            data["score"]-= 0.23/3/4
            #return data
        
        elif not status.isspace() and data["com_pass"]==0:
            data["com_pass"] = 1
            data["score"] += 0.23/3/4

    else:
        data["com_pass"]= 0
        
        
data = {}
score = 0
run(data,score)

