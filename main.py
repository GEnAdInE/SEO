# list of account :
# 57873murrilniyanna@randomail.io
# evxopwhjqu@email.omshanti.edu.in


import csv
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import numpy as np
from webdriver_manager.chrome import ChromeDriverManager
import time


class DataBaseObject:  # use str for now maybe use a convert to convert 5.5K to 5500 later
    keyword: str
    googleScore: int
    keywordDif: int
    volume: int
    globalVolume: int

    def ToExportFormat(self):
        return [self.keyword, self.googleScore, self.keywordDif, self.volume, self.globalVolume]


# 57873murrilniyanna@randomail.io
def stringConverter(oldStr: str):
    lastCharPos = len(oldStr) - 1
    preparedStr = oldStr.replace(',', '.')
    if oldStr[lastCharPos] == 'B':
        return int(float(preparedStr[0:-1]) * 1000000000)
    if oldStr[lastCharPos] == 'M':
        return int(float(preparedStr[0:-1]) * 1000000)
    if oldStr[lastCharPos] == 'K':
        return int(float(preparedStr[0:-1]) * 1000)
    if oldStr[lastCharPos] == '%':
        return int(preparedStr[0:-1])
    return oldStr


TmpArray = sys.argv
TmpArray.__delitem__(0)
ListOfLogin = TmpArray[:2]
FilePath = TmpArray[2]

KeyWordArray = []

with open(FilePath, 'r', encoding='utf8') as file:
    reader = csv.reader(file, delimiter=';')  # opening the csv file containing all data
    for row in reader:
        if len(row) >= 2:
            TmpEl = DataBaseObject()
            TmpEl.keyword = row[0]
            TmpEl.googleScore = row[1]
            if len(row) == 5:
                TmpEl.keywordDif = row[2]
                TmpEl.volume = row[3]
                TmpEl.globalVolume = row[4]
            else:
                TmpEl.keywordDif = -1
                TmpEl.volume = -1
                TmpEl.globalVolume = -1
            KeyWordArray.append(TmpEl)
    file.close()

IndexArray = []
i = 0
for key in KeyWordArray:
    if key.keywordDif == -1:
        IndexArray.append(i)
    i += 1
    if len(IndexArray) == 10:
        break

driver = webdriver.Chrome()
driver.get('https://www.semrush.com/projects/')

title = ''
title = driver.title
if title.startswith('Dashboard'):  # already Login
    print('we are good')
else:
    print('Login in ...')
    driver.get('https://www.semrush.com/login/')
    loginId = driver.find_element(By.ID, 'email')
    loginId.clear()
    loginId.send_keys(ListOfLogin[0])
    loginPass = driver.find_element(By.ID, 'password')
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

for index in IndexArray:

    driver.get('https://www.semrush.com/analytics/keywordoverview/?q=' + KeyWordArray[index].keyword + '&db=fr')

    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div[4]/div[2]/div/div[1]/div/div/div[1]/span[2]/span')))
    except:
        print('error to get data')
        quit()

    try:
        el = driver.find_element(By.XPATH,
                                 '//*[@id="app"]/div/div/div[4]/div[2]/div/div[1]/div/div/div[1]/span[2]/span')
        KeyWordArray[index].volume = stringConverter(el.text)
    except:
        print("No data for Volume")
        KeyWordArray[index].volume = -2

    try:
        el = driver.find_element(By.XPATH,
                                 '//*[@id="app"]/div/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/span')
        KeyWordArray[index].globalVolume = stringConverter(el.text)
    except:
        print("No data for Global Volume")
        KeyWordArray[index].globalVolume = -2

    try:
        el = driver.find_element(By.XPATH,
                                 '//*[@id="app"]/div/div/div[4]/div[2]/div/div[1]/div/div/div[2]/span[2]/div/div[1]/span[1]')
        KeyWordArray[index].keywordDif = stringConverter(el.text)
    except:
        print("No data for difficulty")
        KeyWordArray[index].keywordDif = -2

    print(KeyWordArray[index].keywordDif)
    print(KeyWordArray[index].volume)
    print(KeyWordArray[index].globalVolume)

# end of program
print("Data have been gathered")

ExportArray = []
for element in KeyWordArray:
    ExportArray.append(element.ToExportFormat())
    print(element.keyword)
    print(element.keywordDif)

print("Updating file")

with open('newDATA.csv', 'w+', newline='') as file:
    mywriter = csv.writer(file, delimiter=';')
    mywriter.writerows(ExportArray)
    file.close()

print('byebye')
quit()


def Quit():
    print('Quitting')
    driver.close()
    exit(1)
