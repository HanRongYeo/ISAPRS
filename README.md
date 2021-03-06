# ISAPRS
Teleport
- [Methodology](#methodology)
- [Prerequisites](#prerequisites)
- [How to run](#how-to-run-the-script)
### Introduction
Information Security Awareness Profiling &amp; Recommendation System (ISAPRS) is a combination of profiling system and recommendation system that designed to:<br>
- Automate the ISA measurement process without a questionnaire to avoid Hawthorne effect, reduce the time comsume and man-power. 
- Keep the result of ISA measurement up-to-date and reflect the vulnerability on ISA.
- Profile the users according to their ISA result. (The profiles will be utilized for RS later.)
- To provide suitable security recommendations to users to increase their willingness of to apply for security practice.<br>(Ambiguous and complicated security warnings may disuade people from applying security protection.)<br><br>

### Methodology

This section will briefly explain how the system works. You can [Skip this section](#prerequisites) if you're not interested.<br>
The ISA measurement can be divided into 5 focus areas:
- Email Use
- Password Management
- Social Networking Site (SNS) Use
- Internet Use
- Information Handling

The system will check every focus area and then turn it into a score. You can view the details of measurement and score calcurating [HERE](https://ieeexplore.ieee.org/document/9574351)
| Focus Area | Sub Area |
| ---------- | -------- |
| Email Use | Phishing email test |
| Password Management | Password strength <br>Locking computer|
| SNS Use             | Personal information on SNS (FB only on this stage) |
| Internet Use        | Network sniffing |
| Information Handling | Antivirus & Firewall |


The figure below shows the overview of the system design.
![overview diagram](https://user-images.githubusercontent.com/94159290/141487002-9d2ebff9-3017-4d76-831b-9a0f0ff73adf.jpg)


### Prerequisites
1. This program can only works on **Windows OS** at this stage.
2. WinPcap need to be installed in order to perform tracffic sniffing. (Included in package)
3. Snort is required in order to perform tracffic sniffing. (Included in package)
4. You need a database and you need to connect the program to your database.

I'm using Python 3.6, and all the modules except **VerticalScrolledFrame** and **selenium** are built-in module. I'm not sure whether all of them are included in other version of Python. The VerticalScrolledFrame is included in this package so you don't need to download by yourself. It was created by [novel-yet-trivial](https://gist.github.com/novel-yet-trivial) and you can also download the module from his Github page if you want.

The required modules:
- requests
- sys
- os
- threading
- ast
- pickle
- tkinter
- uuid
- webbrowser
- [VerticalScrolledFrame](https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8)
- [selenium](https://pypi.org/project/selenium/)
   - ```python -m pip install selenium```

The project are breaks into parts and each part handle a process.
All the parts above are include in the package. Just put all of them in a same folder.
The parts include:
- ISAPRS.py (main)
- firewallCheck.py
- local_user_password_check.py
- passwordCheck.py
- SNS_Check.py
- tk_dynamic.py
- version_check.py
- ids.py
- admin.py


### How to run the script
#### Things to do before run
1. Before you run the program, make sure all of the scripts are put in the same folder.
2. replace with your database api key
```
   api_key = "replace with your api key"
``` 
4. Change the content in 'data' dictionary to fit your database. For example, the 'user' table in your database does not need 'sns_acc" then you can deleted it, or change the format which can fit into your table.
```
   data = {"id":hex(get_mac())}
   data["email"] = entryEmail.get()
   data["sns_acc"] = entryFB.get()
   data["ids"]=0
   data["phishing"]=0-0-0-0-0
```
5. Replace your own php to run the SQL according to your purpose.
```
   respond = s.post("url to your database",data)
```

### Ready to run
After connected to your database, let's start!

1. Run the ISAPRS.py
   - Please allow to run in admin.
   - The program will ask you to install WinPcap if it is not installed on your device.
   - You need to run it again after WinPcap is installed.
   - ![winpcap](https://user-images.githubusercontent.com/94159290/141609223-aca68424-9732-426d-a478-1daee0e52ea7.JPG)

2. Take a break. Let it do the things.
   - ![step2](https://user-images.githubusercontent.com/94159290/141609349-7c480f2c-6523-41d1-8bdc-7cb1e4c5c258.JPG)

3. The profile is recorded in database. Recommendation provided, rate them!
   - ![RS result](https://user-images.githubusercontent.com/94159290/141609376-a366454c-9a1f-4966-ba1c-489b75bbc849.JPG)

4. Just close the recommender after rating is given.





