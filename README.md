# ISAPRS<br>
Information Security Awareness Profiling &amp; Recommendation System (ISAPRS) is a combination of profiling system and recommendation system that designed to:<br>
- Automate the ISA measurement process without a questionnaire to avoid Hawthorne effect, reduce the time comsume and man-power. 
- Keep the result of ISA measurement up-to-date and reflect the vulnerability on ISA.
- Profile the users according to their ISA result. (The profiles will be utilized for RS later.)
- To provide suitable security recommendations to users to increase their willingness of to apply for security practice.<br>(Ambiguous and complicated security warnings may disuade people from applying security protection.)<br><br>

### Methodology<br>

This section will briefly explain how the system works. You can [Skip this section](#prerequisites) if you're not interested.<br>
The ISA measurement can be divided into 5 focus areas:
- Email Use
- Password Management
- Social Networking Site (SNS) Use
- Internet Use
- Information Handling<br>

The system will check every focus area and then turn it into a score.
| Focus Area | Sub Area |
| ---------- | -------- |
| Email Use | Phishing email test |
| Password Management | Password strength <br>Locking computer|
| SNS Use             | Personal information on SNS (FB only on this stage) |
| Internet Use        | Network sniffing |
| Information Hanling | Antivirus & Firewall |



### Prerequisites<br>
The modules required:
- requests
- sys
- os
- threading
- ast
- pickle
- tkinter
- uuid <br>

The project are breaks into parts and each part handle a process. The parts includes:
- ISAPRS.py (main)
- firewallCheck.py
- local_user_password_check.py
- passwordCheck.py
- SNS_Check.py
- tk_dynamic.py
- version_check.py
- ids.py
- admin.py


