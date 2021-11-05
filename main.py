import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class SEODATA:  # use str for now maybe use a convert to convert 5.5K to 5500 later
    volume: str
    keywordDif: str
    globalVolume: map
    Results: str


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

    # waiting for page to load up
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="srf-searchbar"]/form/div/div[2]/div[1]/input')))
    except:
        print('took too long')
        quit()

keywordMap = dict()
for keyword in ListOfKeyword:
    driver.get('https://www.semrush.com/analytics/keywordoverview/?q=' + keyword + '&db=fr')
    currentSeoData = SEODATA()
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div[4]/div[2]/div/div[1]/div/div/div[1]/span[2]/span')))
    except:
        print('error to get data')
        quit()

    el = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/div[1]/div/div/div[1]/span[2]/span')
    currentSeoData.volume = el.text
    # etc
    # etc
    print(currentSeoData)

    # put data in map
    keywordMap[keyword] = currentSeoData

# end of program
print('byebye')
driver.close()


def Quit():
    print('Quitting')
    driver.close()
    exit(1)
