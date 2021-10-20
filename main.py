import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

TmpArray = sys.argv
TmpArray.__delitem__(0)
ListOfLogin = TmpArray[:2]
TmpArray.__delitem__(0)
TmpArray.__delitem__(0)
ListOfKeyword = TmpArray

driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.semrush.com/projects/')

title = ''
title = driver.title
if title.startswith('Dashboard'):  # already Login
    print('we are good')
else:
    print('need to login')
    driver.get('https://www.semrush.com/login/')
    loginId = driver.find_element_by_id('email')
    loginId.clear()
    loginId.send_keys(ListOfLogin[0])
    loginPass = driver.find_element_by_id('password')
    loginPass.clear()
    loginPass.send_keys(ListOfLogin[1])
    loginPass.send_keys(Keys.ENTER)

    # check we got login

for keyword in ListOfKeyword:
    driver.get('https://www.semrush.com/analytics/keywordoverview/?q=' + keyword + '&db=fr')
    # LOGIC FOR getting the data

driver.close()
