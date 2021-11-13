# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 17:18:11 2021

@author: SheepCurry
"""

import tkinter as tk
from tkinter import *
import VerticalScrolledFrame as vsf
import passwordCheck as pc
import webbrowser
buttons=[]

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = self.widget.winfo_pointerx()
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
        widget.configure(fg="#96ceb4")
    def leave(event):
        toolTip.hidetip()
        widget.configure(fg="#fff2df")      
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    
def CreateHover(widget):
    ori_bg = widget["background"]
    def enter(event):
        if not widget["state"]=="disabled":
            widget["state"]=widget["state"]
            widget["bg"]="#96ceb4"
            widget["fg"]="#10121b"
            #widget.configure(bg="#96ceb4",fg="#10121b")
    def leave(event):
        widget["state"]=widget["state"]
        if widget["state"]=="active":
            widget["bg"]= "#96ceb4"
            widget["fg"]= ori_bg
        else:
            widget["bg"]=ori_bg
            widget["fg"]="#96ceb4"
            #widget.configure(bg=ori_bg,fg="#96ceb4")
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def createLabel(window, message, row, col, pady, ex):     
    label = tk.Label(window, width=90, wraplength=600, text=message, anchor="sw", justify="left")
    if row%2==0:
        label.configure(bg="#1d1e28",fg="#fff2df")
    else:
        label.configure(bg="#10121b",fg="#fff2df")      
    label.grid(row=row,column=col,pady=pady)
    CreateToolTip(label, "Why I get this recommendation?\nClick me for more info")
    label.bind("<Button-1>", lambda e: callback(ex))
    
def rating(pos,ID,rate,sqlRecomArr):
    if sqlRecomArr[pos]=="":
        sqlRecomArr[pos] = "r_%s=%s,"%(ID,rate)
        for i in range(5):
            buttons[pos][i]["state"]="disabled"
        buttons[pos][rate-1]["state"]="active"
        buttons[pos][rate-1].configure(bg="#96ceb4",fg="#10121b",relief="sunken")
    else:
        sqlRecomArr[pos] = ""
        for i in range(5):
            buttons[pos][i]["state"]="normal"
        if pos%2==0:
             buttons[pos][rate-1].configure(bg="#1d1e28",fg="#96ceb4",relief="raised")
        else:
             buttons[pos][rate-1].configure(bg="#10121b",fg="#96ceb4",relief="raised")
    
def getYesNo(x):
    if isinstance(x,str):
        x = x.replace("1", "Yes")
        x = x.replace("0", "No")
        return x
    
    elif isinstance(x,int):
        if x<0:
            return "No"
        else:
            return "Yes"
    
    else:
        if x:
            return "Yes"
        else:
            return "No"
        
def title_explain(data, cateArr):
    exArr = []
    for i in cateArr:
        temp = {}
        if i==1:
            temp["title"]="Firewall"
            temp["explain"]="""The purpose of firewall is to protect your computer from network attacks by controling network access.
Turn off firewall could expose yourself to network attacks such as intrusion.

The common situation for people turn off thier Firewall is because the software they try to run is blocked by the Firewall.

In that situation, we suggest allow the specific software access to Firewall instead of turning off the entire Firewall."""
            if data["firewall"]=="1-1-1":
                temp["reason"]="Everything is fine with your Firewall. This recommendation is just provide some methods you may try it out."
            else:
                temp["reason"]="Your Firewall is partly or fully OFF."
            exArr.append(temp)
        
        elif i==2:
            temp["title"]="Anti-virus"
            temp["explain"]="""The purpose of Anti-virus is to protect your computer from viruses and malicious codes.

Those viruses or malicious codes are designed to cause damages not only to your computer but also to your privacy and wallet. (eg. Wanna-cry)

The anti-virus will keep updating the lastest virus information. It is also important to keep your anti-virus up-to-date. The anti-virus may not detect the lastest virus if it is out-of-date.

The common situation for someone turn off their anti-virus is because the software they try to run is blocked/deleted by the anti-virus.

In that situation, we suggest exclude the specific software from your anti-virus quarantine instead of turning off the entire anti-virus."""
            if data["enable"]:
                if data["uptodate"]:
                    temp["reason"]="Everything is fine with your anti-virus. This recommendation is just provide some methods you may try it out."
                else:
                    temp["reason"]="Your anti-virus is out-to-date."
            else:
                if data["anti_name"]=="":
                    temp["reason"]="There is no anti-virus software installed."
                elif not data["uptodate"]:
                    temp["reason"]="Your anti-virus is OFF and also out-of-date."
                else:
                    temp["reason"]="Your anti-virus is OFF."
            exArr.append(temp)
            
        elif i==3:
            temp["title"]="Social Networking site (SNS)"
            temp["explain"]="SNS refers to all the social networking site such as Facebook, Instagram, Twitter and so on. If there is personal information especially sentitive information like address or IC number show on the SNS. The attacker could use those information for crimes, including cybercrime like fraud and phishing."
            if data["sns"]:
                temp["reason"]="Personal information found on your SNS account."
            else:
                temp["reason"]="Everything is fine with your SNS. This recommendation is just provide some methods you may try it out"
            exArr.append(temp)
            
        elif i==4:
            temp["title"]="Email Phishing"
            temp["explain"]="'Phishing' is one of the most common cybercrime. Phishing is the fraudulent attempt to obtain sensitive information or data, such as usernames, passwords and credit card details or other sensitive details. The most common method is through a fake link attached in email. The link will redirect victim to a fake website and asked for sensitive information."
            if data["phishing"] == 1:
                temp["reason"]="You clicked the fake phishing we sent to you. This recommendation may provide you some awareness of phihsing and some countermeasures to against it."
            else:
                temp["reason"]="You didn't click the phishing link.\nThis recommendation is just to increase your awareness of phishing and provide some common coutermeasures of phishing for you."        
            exArr.append(temp)
            
        elif i==5:
            temp["title"]="Network Traffic"
            temp["explain"]="Network traffic refers to the transactions of network. Every activity using Internet including browsing website"
            if data["ids"]:
                temp["reason"]="Some bad network traffic detected in your network."
            else:
                temp["reason"]="You network traffic is clean.\nThis recommendation is just provide some methods you may try it out."
            exArr.append(temp)
            
        elif i==6:
            temp["title"]="Password Management"
            temp["explain"]="A good password pratice can provide much more security to you. Typically, the password strength is refers to the difficulty to crack a password (mostly in terms of cracking time). Higher strength means more difficulty to crack. The common method to crack a password is using 'brute force attack', it try out all the character combinations. So, the possibilities of the combinations become the key factor of password strength. A simple password like '123456' need less than 1 second to crack, while a password like 'b3tZf&kL#2cJ8Ui' need days, even years to crack."
            if pc.getPasswordRecomFlag(data):
                temp["reason"]="The password you created for this system is NOT considered as 'good password'."
            else:
                temp["reason"]="You have a good password practice. This recommendation is just provide some methods that you may try it out."
            
            if not data["com_pass"]:
                temp["reason"] += "\n\nThere is no password set for your computer."
            exArr.append(temp)
    return exArr
    
def callback(ex):
    message ="Reason:\n"+ ex["reason"] + "\n\nExplanation:\n" + ex["explain"]
    #tk.messagebox.showinfo(ex["title"],message)
    ans = tk.messagebox.askyesno(ex["title"],message+"\n\n\nFor more information, click Yes to visit our website with more detail explanation!")
    if ans:
        webbrowser.open_new_tab("https://masterprojectsheep.000webhostapp.com/cybercrime.html#"+ex["title"])
    

def run(data,sqlRecomArr,arr,idArr, cateArr):
    pady=1
    bg="#080a13"
    window = tk.Tk()
    window.title("Recommend")
    window.iconbitmap("sheep.ico")
    window.configure(background=bg)
    window.resizable(False, False)
    
    for i in range(len(arr)):
        sqlRecomArr.append("")
    
    if data["score"]<0.6:
        level="1"
    elif data["score"]>=0.8:
        level="3"
    else:
        level="2"
        
    f = tk.Frame(window,background=bg)
    fLevel = tk.Frame(window,background=bg)
    label_level = tk.Label(fLevel,text=level,anchor="center",justify="center",background=bg,fg="#fff2df")
    label_level.configure(font=("Courier", 60),fg="#fff2df")
    label_level.grid()
    fLevel.grid(row=0)
    label_fArr = ["User:","Level:","Antivirus","Antivirus Real-time Protection:","Antivirus Up-to-Date:","Firewall (Domain-Private-Public):","Windows Account Password:","Facebook:"]
    
    if not data["sns"]:
        text_FB = "No personal information found on public."
    else:
        text_FB = "Personal information found on public"
    text_fArr=[data["email"],level,data["anti_name"],getYesNo(data["enable"]),getYesNo(data["uptodate"]),getYesNo(data["firewall"]),getYesNo(data["com_pass"]),text_FB]
    for i in range(len(label_fArr)):
        label_title = tk.Label(f, width=56,wraplength=340, text=label_fArr[i], anchor="sw", justify="left",background=bg,fg="#fff2df")
        label_status = tk.Label(f, width=56,wraplength=340, text=text_fArr[i], anchor="sw", justify="left",background=bg,fg="#fff2df")
        label_title.grid(row=i+1,column=0)
        label_status.grid(row=i+1,column=1)
        
    f.grid(row=1,pady=5)
    window.update()
    v = vsf.VerticalScrolledFrame(window,width=window.winfo_width(), bg="#080a13")  
    exArr = title_explain(data, cateArr)
    for i in range(len(arr)):
        #createLabel(v,exArr[i], i, 0, pady)
        createLabel(v,arr[i],i,0,pady,exArr[i])
        button=[]
        for j in range(5):
            btn = tk.Button(v, width=3, text=str(j+1), activebackground="#96ceb4",activeforeground="#10121b", command=lambda pos=i,ID=idArr[i],rate=j+1 :rating(pos,ID,rate,sqlRecomArr))
            if i%2==0:
                btn.configure(bg="#1d1e28",fg="#96ceb4")
            else:
                btn.configure(bg="#10121b",fg="#96ceb4")
            btn.grid(row=i,column=j+1, sticky="nsew",pady=pady)
            #CreateHover(btn)
            button.append(btn)
        buttons.append(button)
    v.grid(row=2)
    return window,sqlRecomArr

#//////////////  Testing code  //////////////
# arr=[]
# data = {'id': '0x54a050aa3d1b', 'email': 'sheepmasterproject@gmail.com', 'password': '15-3-1-1', 'sns_acc': 'NULL', 'sns': 0, 'phishing': 0, 'com_pass': 1, 'firewall': '1-1-1', 'anti_name': 'Bitdefender Antivirus Free Antimalware', 'enable': 1, 'uptodate': 1, 'ids': 1, 'score': 0.807413}
# sqlRecomArr=[]
# idArr=[]
# cateArr=[]
# for i in range(6):
#     idArr.append(i)
#     cateArr.append(i+1)
#     arr.append("recommendation%s"%(i))
# window,sqlRecomArr = run(data,sqlRecomArr,arr,idArr,cateArr)
# window.mainloop()