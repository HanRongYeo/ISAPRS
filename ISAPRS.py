# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 15:09:56 2021

@author: SheepCurry
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 17:09:26 2020

@author: SheepCurry
"""

import requests, sys, os, threading, ast, pickle
import tkinter as tk
from tkinter import messagebox as msgbox
from uuid import getnode as get_mac
#from tendo import singleton

import antivirusCheck as ac
import firewallCheck as fc
import local_user_password_check as lupc
import passwordCheck as pc
import SNS_Check as sc
import tk_dynamic as tkd
import version_check as vc
import ids, admin

sys.path.append('../')
api_key = "replace with your api key"
score = 0.3005
avList = {}
data = {"id":hex(get_mac())}
current_version = 0.2
d = os.path.dirname(os.path.abspath(__file__))
path = d +"\\Snort\\etc\\snort.conf"
path_log = d + "\\Snort\log"
t0 = threading.Thread(target=ids.snort_start)
t1 = threading.Thread(target=ids.snort_kill,kwargs={"time":60})
s = requests.Session()
flag_cookies = False
name_cookies="csars.cookies"

def enter_record(score):
    global t0, t1
    try:
        data["email"] = entryEmail.get()
        data["sns_acc"] = entryFB.get()
        
        if len(entryPassword.get()) > 99:
            msgbox.showerror("Password too long (Limited to 99 char)")
            entryPassword.delete(0, tk.END)
        else:       
            print("Checking password...")
            score = pc.run(data, entryPassword.get(), score)       
            print("Done password check.")
            
            print("Checking SNS")
            score = sc.snsCheck(entryFB.get(),data,score)
            print("Done SNS checking")
            
            print("Checking Local password account")
            score = lupc.run(data,score)
            print("Done checking Local password account")
            
            print("Checking firewall setting")
            score = fc.run(data,score)
            print("Done Firewall check")
            
            print("Checking Anti-virus")
            score = ac.run(data,score)
            print("Done Anti-virus check")
            
            print("Checking network traffic...it may takes a few minutes")
            ids.print_time()
            t1.join()
            if not (os.stat(path_log+"\\alert.ids").st_size == 0):
                data["ids"]=1
            else:
                data["ids"]=0
                score += 0.016 + 0.001 + 0.23/3
            data["phishing"]="0-0-0-0-0"
            print("Done")
            print("data=",data,"\n")
            print("Inserting record...")
            insertDatabase(data,score)
            print("Inserted")
            
            #t_email = threading.Thread(target=ep.run,args=(data["email"],))
            #t_email.start()

            print("Getting recommendations")
            window.destroy()
            getRecom(data)
                
    except ConnectionError as e:
        msgbox.showerror(e)


def checkExist(data):
    try:
        respond = s.post("url to your database",data)
        if respond.text == "False":
            return False
        else:
            data = ast.literal_eval(respond.text)
            return data
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def insertDatabase(data,score):
    data["score"] = score
    s.post("url to your database",data)

def updateExist(data):
    print("Updating current status")
    sc.snsCheck_exist(data)
    lupc.run_exist(data)
    fc.run_exist(data)
    ac.run_exist(data)
    print("Waiting for ids...")
    ids.print_time()
    t1.join()
    ids.run(data)
    try:
        s.post("url to your database",data)
        print("Updated")
    except requests.exceptions.RequestException as e:
        with open("log.txt","wb") as f:
            f.write(e)
        raise SystemExit(e)
    
def on_closing(root,sqlRecomArr):
    flag = False
    for i in sqlRecomArr:
        if not (i==""):
            flag=True
    if flag:
        sql = "UPDATE user_recom SET "
        for i in sqlRecomArr:
            sql += i
        sql = sql[:-1] + " WHERE uid='%s';"%data["id"]
        content={"sql":sql}
        try:
            s.post("url to your database",content)
            print("Rating recorded")
            root.destroy()
        except:
            root.destroy()
    root.destroy()
    
def getRecom(data):
    recomArr=[]
    recomIDArr=[]
    recomCateArr=[]
    level="1"

    if(data["score"]>=0.6 and data["score"]<0.8):
        level="2"
    elif(data["score"]>=0.8):
        level="3"

    sql="SELECT * FROM recommend WHERE (flag=0 AND level="+level+")"
        
    if data["sns"]:
        sql+=" OR (category=3 AND flag=1)"
   
    if not data["enable"]:
        sql+=" OR (category=2 AND flag=1)"
    
    if not data["firewall"]:
        sql+=" OR (category=1 AND flag=1)"
        
    if data["ids"]:
        sql+=" OR (category=5 AND flag=1)"
        
    if (pc.getPasswordRecomFlag(data)):
        sql+=" OR (category=6 AND flag=1)"
        
    sql += ";"
    
    content={"sql":sql}
    try:
        respond = s.post("url to your database",content)
        if respond.text == "False":
            print("False")
        else:
            result = respond.text.split("SPLIT")
            sqlRecomArr = []
            for i in result[:-1]:
                j = ast.literal_eval(i)
                recom = j["content"].replace("\\n", "\n")
                recomIDArr.append(j["id"])
                recomCateArr.append(j["category"])
                recomArr.append(recom)
            root,sqlRecomArr = tkd.run(data,sqlRecomArr,recomArr,recomIDArr, recomCateArr)
            root.protocol("WM_DELETE_WINDOW", lambda root=root:on_closing(root,sqlRecomArr))
            root.mainloop()
            
    except requests.exceptions.RequestException as e:
        with open("log.txt","wb") as f:
            f.write(e)# This is the correct syntax
        raise SystemExit(e)

#///////////////////////////    Main    //////////////////////////////////
#***************************    Window    ******************************
# try:
#     me = singleton.SingleInstance()
# except:
#     import ctypes  # An included library with Python install.   
#     ctypes.windll.user32.MessageBoxW(0, "Program Already Running", "", 1)
#     sys.exit(-1)
if __name__ == "__main__":
    # if True:
    #     if False:
    #         print()
    try:
        rc = admin.run()
        if not rc:
            sys.exit(0)
        else:               
            if(vc.version_check(current_version)):
                t1.start()
                if t1.isAlive():
                    t0.start()
                try:
                    with open(name_cookies,"rb") as f:
                        s.cookies.update(pickle.load(f))
                        flag_cookies = True
                        f.close()
                        
                except Exception:
                    print("Cookies not found")
                    
                test = checkExist(data)
                print(test)
                
                if isinstance(test,dict):
                    data = test
                    updateExist(data)
                    getRecom(data)
                    sys.exit(0)
                    
                else:
                    print("Welcome New User...")
                    sql_Create_Users_Recom="INSERT INTO user_recom (uid) VALUES ('%s');"%data["id"]
                    content_CUR={"sql":sql_Create_Users_Recom}
                    try:
                        respond = s.post("url to your database",content_CUR)
                        
                        window = tk.Tk()
                        window.title("Sign up")
                        window.iconbitmap("sheep.ico")
                        window.focus_set()
                        window.bind("<Return>",(lambda event:enter_record(score)))
                        window.configure(bg="#080a13")
                        frame1 = tk.Frame(window)
                        frame1.configure(bg="#080a13")
                        frame2 = tk.Frame(window)
                        frame2.configure(bg="#1d1e28")
                        frame1.grid(row=0, sticky="nsew")
                        frame2.grid(row=1, sticky="nsew")
                        
                        #***************************    Label    ***********************
                        announce = """This sign up page is to create an account in this recommendation system
                        STEPS:
                        1) Enter the email address which you use usually
                        2) Create a new password for this account.
                        3) Enter your Facebook account (Optional)
                                  For example: facebook.com/somebody
                                  Just enter 'somebody' in the field
                        4) Submit
                           
                        *****************************************************************************************************************************
                        After sign up, you will get some recommendations according to information we collect from you computer
                        
                        Please rate the recommendations 5 if you find that it is suitable for you. **In terms of operation and difficulty.
                        Please rate the recommendations 1 if you find that it is NOT suitable for you. **In terms of operation and difficulty.
                        
                        
                        """
                        labelAnnouce = tk.Label(frame1, justify="left", text=announce)
                        labelAnnouce.configure(bg="#080a13",fg="#fff2df")
                        labelAnnouce.grid(row=0, sticky="nsew")
                        labelEmail = tk.Label(frame2, width=50, anchor="e", justify="right", text="Email address*")
                        labelEmail.configure(bg="#1d1e28",fg="#fff2df")
                        labelEmail.grid(row=0,sticky="nsew")
                        labelPassword = tk.Label(frame2, width=22, anchor="e", justify="right", text="Password*")
                        labelPassword.configure(bg="#1d1e28",fg="#fff2df")
                        labelPassword.grid(row=1,sticky="nsew")
                        labelFB = tk.Label(frame2, width=22, anchor="e", justify="right", text="(Optional) Facebook ID: facebook.com/")
                        labelFB.configure(bg="#1d1e28",fg="#fff2df")
                        labelFB.grid(row=2,sticky="nsew")
                        
                        #***************************    Input    ************************
                        entryEmail = tk.Entry(frame2, width=50)
                        entryEmail.configure(bg="#1d1e28",fg="#fff2df")
                        entryEmail.grid(row=0, column=1, padx=3, pady=3)
                        
                        entryPassword = tk.Entry(frame2, width=50)
                        entryPassword.configure(bg="#1d1e28",fg="#fff2df")
                        entryPassword.grid(row=1, column=1, padx=3, pady=3)
                        
                        entryFB = tk.Entry(frame2, width=50)
                        entryFB.configure(bg="#1d1e28",fg="#fff2df")
                        entryFB.grid(row=2,column=1, padx=3, pady=3)
                    
                        #***************************   Button    ***************************   
                        btn = tk.Button(window, text="Submit", command=lambda:enter_record(score))
                        btn.configure(bg="#29754D",fg="#fff2df")
                        btn.grid(row=2, sticky="nsew", pady=4)
                        window.mainloop()
                        ids.print_time()
                        
                    except requests.exceptions.RequestException as e:
                        input("Cannot connect to database...\nPlease check your internet connection and try it later.\n\nPress ENTER to exit.")
                        ids.snort_kill()
                        sys.exit(e)
                        
            else:
                sys.exit(0)
    except Exception as e:
        print(e)
        with open("log.txt","a") as f:
            f.write(str(e))
            f.close()
        sys.exit(0)