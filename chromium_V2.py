import os
import time
import pickle
import keyboard
import pyautogui
from datetime import datetime
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")
options.add_argument("--window-size=800,600")
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 2,  # 1:allow, 2:block
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.notifications": 2})


def join_meet(url_meet):
    browser.get(url_meet)
    time.sleep(4)
    pyautogui.press('esc')
    time.sleep(2)
    element = browser.find_element_by_class_name('CwaK9')
    browser.execute_script("arguments[0].click();", element)
    browser.find_element_by_xpath("//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Ask to join')]").click()
    print('Joined In the Meeting Successfully')


def google_login(usernameStr, passwordStr):
    browser.get(('https://accounts.google.com/ServiceLogin?'
                 'service=mail&continue=https://mail.google'
                 '.com/mail/#identifier'))
    browser.find_element_by_id('identifierId').send_keys(usernameStr)
    browser.find_element_by_id('identifierNext').click()
    time.sleep(5)
    browser.find_element_by_xpath("//input[@class='whsOnd zHQkBf']").send_keys(passwordStr)
    browser.find_element_by_id('passwordNext').click()


# main_function:

print('Google Meet Bot V.2.0 \n')
if 'database.pkl' not in os.listdir():
    print('[WARNING] No Database File Has Been Found')
    print('[ATTENTION] Please Enter the Required Details')
    data_dict = {"un": str(input("<Enter Your Google Username Here>")),
                 "ps": str(input("<Enter Your Password Here>")),
                 "mu": str(input("<Enter Your Meet URL Here>")),
                 "s1st": str(input("<Session_1 Start Time (HH:MM:SS)>")),
                 "s1sp": str(input("<Session_1 Stop Time (HH:MM:SS)>")),
                 "s2st": str(input("<Session_2 Start Time (HH:MM:SS)>")),
                 "s2sp": str(input("<Session_2 Stop Time (HH:MM:SS)>"))
                 }
    with open('database.pkl', 'wb') as pickle_file:
        pickle.dump(data_dict, pickle_file)
else:
    print('[INFO] Database File Found')

print('[INFO] Loading Data into the Program')
pickle_file = open('database.pkl', 'rb')
data_dict = pickle.load(pickle_file)
username, password, meeting_url = data_dict['un'], data_dict['ps'], data_dict['mu']
session_1_start_time, session_1_stop_time = data_dict['s1st'], data_dict['s1sp']
session_2_start_time, session_2_stop_time = data_dict['s2st'], data_dict['s2sp']
print('[INFO] All the required Parameter Has been Loaded into the Program')
time.sleep(2)
print('[INFO] Starting the Program')

while True:
    print('Checking Time')
    now_time = datetime.now().strftime('%H:%M:%S')
    if (now_time == session_1_start_time) or (now_time == session_2_start_time):
        browser = webdriver.Chrome('chromedriver.exe', chrome_options=options)
        google_login(username, password)
        time.sleep(10)
        join_meet(meeting_url)
        time.sleep(5)
        print('[INFO] Meeting Joined Successfully')

    elif (now_time == session_1_stop_time) or (now_time == session_2_stop_time):
        browser.close()
        browser.quit()
    else:
        print('Waiting Till Session Start/Stop Timing, Sleeping for 10S to Conserve Processing Power')
        time.sleep(10)
        print('Sleep Complete')

    if keyboard.is_pressed('q'):
        print('[INFO] Program Stopped By The User')
        print('[HQ] Thank you For Using This Bot')
        break
