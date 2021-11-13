# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 19:45:23 2020

@author: SheepCurry
"""

from selenium import webdriver

def fix_url(target):
    if not target[-1]=="/":
        target += "/"
    
    if target[:8] == "https://":
        return target+"about"
        
    elif target[:12] == "facebook.com":
        return("https://"+target+"about")
    else:
        return("https://facebook.com/"+target+"about")

def snsCheck(target,data,score):
    if target:
        #***************  Load chrome driver  ************************
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        options.add_argument(' --headless')
        options.add_argument(' -no-sandbox')
        options.add_argument(' -disable-dev-shm-usage')
        driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)
        
        #*********************  Open target Facebook page  *****************************
        try:
            fixedTarget = fix_url(target)
            driver.get(fixedTarget)
            divArr = driver.find_elements_by_xpath("//div[@class='_4-u2 _u9q _3xaf _4-u8']//div[@class='_4bl9']")
            driver.quit()
            if not divArr:
                score += (0.2865 + 0.04 + 0.014)
                data["sns"]=0
                return score
            else:
                data["sns"]=1
                return score
        
        except Exception:
            score += (0.2865 + 0.04 + 0.014)
            data["sns"]=0
            return score
    else:
        score += (0.2865 + 0.04 + 0.014)
        data["sns"]=0
        return score
    
def find_xpath(url,xpath):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    #options.add_argument(' --headless')
    options.add_argument(' -no-sandbox')
    options.add_argument(' -disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)  
    
    #*********************  Open target Facebook page  *****************************
    try:
        driver.get(url)
        a = driver.find_element_by_xpath(xpath).get_attribute('href')
        driver.get(a)
        #driver.quit()
        return a
    
    except Exception as e:
        print(e)
    
def snsCheck_exist(data):
    if(data["sns"]):
        #***************  Load chrome driver  ************************
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        options.add_argument(' --headless')
        options.add_argument(' -no-sandbox')
        options.add_argument(' -disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)  
        
        #*********************  Open target Facebook page  *****************************
        try:
            driver.get("https://www.facebook.com/%s"%data['sns_acc'])
            divArr = driver.find_elements_by_xpath("//div[@class='_4-u2 _u9q _3xaf _4-u8']//div[@class='_4bl9']")
            driver.quit()
            if not divArr:
                if data['sns']==1:
                    data['score'] += (0.2865 + 0.04 + 0.014)
                    data["sns"]=0
                    return data
                else:
                    return data
                    
            else:
                if data['sns']==0:
                    data['score'] -= (0.2865 + 0.04 + 0.014)
                    data["sns"] = 1
                    return data
                else:
                    return data
                    
        except Exception:
            return data
     
    else:
        return data
    
def snsCheck2(target):
    filename = "screenshot.jpg"
    #***************  Load chrome driver  ************************
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    options.add_argument(' --headless')
    options.add_argument(' -no-sandbox')
    options.add_argument(' --start-maximized')
    options.add_argument(' -disable-dev-shm-usage')
    options.add_argument(' --lang=de')
    driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)  
    
    #*********************  Open target Facebook page  *****************************
    try:
        driver.get("https://www.facebook.com/%s"%target)
        original_size = driver.get_window_size()
        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        print("width:",required_width)
        print("height",required_height)
        driver.set_window_size(required_width, required_height)
        # driver.save_screenshot(path)  # has scrollbar
        driver.find_element_by_tag_name('body').screenshot(filename)  # avoids scrollbar
        driver.close()
        return filename
    except:
        return False

# data={}
# score=0
# snsCheck("sheepcurry.bug", data, score)
# print(data)
    
#////////////////  Testing code  //////////////////////
# data = {'id': '0x54a050aa3d1b', 'email': 'birdmanyeo2@gmail.com', 'password': '10-1-1-0', 'sns_acc': 'sheepcurry.bug', 'sns': 1, 'phishing': 0, 'com_pass': 1, 'com_days': 1215, 'firewall': '1-1-1', 'anti_name': 'Bitdefender_Antivirus_Free_Antimalware', 'enable': 1, 'uptodate': 1, 'score': 0.44535}
# data2 = snsCheck_exist(data)
# print(data2)
# url = "https://drive.google.com/u/0/uc?id=1guGGuCsOV3074IH5t0obFD--Lsc9dd7g&export=download"
# xpath = "//a[@id='uc-download-link']"
# a = find_xpath(url, xpath)
# print(a)

# filename = snsCheck2("binobama/about")
# r = tt.get_text(filename)
# print(r)

#//////////////  Testing fix_Target_url() /////////////////////////
# from selenium.webdriver.chrome.options import Options
# options = Options()
# #options = webdriver.ChromeOptions()
# options.binary_location = "chromedriver.exe"
# options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
# options.add_argument(' -no-sandbox')
# #options.add_argument(' -disable-dev-shm-usage')
# driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)  

# # #*********************  Open target Facebook page  *****************************
# target="facebook.com/sheepcurry.bug"
# fixedTarget=fix_url(target)
# driver.get(fixedTarget)