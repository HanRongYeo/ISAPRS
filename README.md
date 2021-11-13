# ISAPRS
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
I'm using Python 3.x, and all the modules except **VerticalScrolledFrame** are built-in module. I'm not sure whether all of them are included in other version of Python.
The VerticalScrolledFrame was created by [novel-yet-trivial](https://gist.github.com/novel-yet-trivial). The module is included in this package so you don't need to download by yourself. However, You can also download the module from his Github page if you want. [Go to VerticalScolledFrame](https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8)

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
- VerticalScrolledFrame

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


