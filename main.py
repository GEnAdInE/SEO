# list of account :
# 57873murrilniyanna@randomail.io
# evxopwhjqu@email.omshanti.edu.in


import csv
import sys

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver


# our class for each keword
# -1 value means that we don't have search data for this word yet
# -2 value means that semrush don't have any data about it
class DataBaseObject:
    keyword: str
    googleScore: int
    keywordDif: int
    volume: int
    globalVolume: int

    def ToExportFormat(self):  # function to return an array of item , used for export to CSV
        return [self.keyword, self.googleScore, self.keywordDif, self.volume, self.globalVolume]


def Quit():
    print('Quitting')
    driver.close()
    exit(0)


# function to check if an element exist on the page
def check_exists_by_xpath(xpath: str):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


# function to convert string from semrush , 15K -> 15 000 etc
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
    if oldStr == 'n/a':
        return -2
    return oldStr


# here we gather the parameter passed when running the app
TmpArray = sys.argv
if len(TmpArray) < 4:
    print("Missing some arguments please refer to the doc.")
    Quit()


TmpArray.__delitem__(0)
ListOfLogin = TmpArray[:2]
FilePath = TmpArray[2]

KeyWordArray = []  # the array that will contain all of our DataBaseObject

with open(FilePath, 'r', encoding='utf8') as file:
    reader = csv.reader(file, delimiter=';')  # opening the csv file containing all data
    for row in reader:
        # gathering the data and putting it the Array
        print(row)
        if len(row) >= 2:
            TmpEl = DataBaseObject()
            TmpEl.keyword = row[0]
            TmpEl.googleScore = int(row[1])
            if len(row) == 5:
                TmpEl.keywordDif = int(row[2])
                TmpEl.volume = int(row[3])
                TmpEl.globalVolume = int(row[4])
            else:
                TmpEl.keywordDif = -1
                TmpEl.volume = -1
                TmpEl.globalVolume = -1
            KeyWordArray.append(TmpEl)
    file.close()

IndexArray = []  # array of the 10 first item where we want to find data
i = 0
for key in KeyWordArray:
    if key.keywordDif == -1:
        IndexArray.append(i)
    i += 1
    if len(IndexArray) == 10:
        break

# openning chrome and going to semrush.com
driver = webdriver.Chrome()
driver.get('https://www.semrush.com/projects/')

title = driver.title
if title.startswith('Dashboard'):  # already Login
    print('we are good')
else:
    print('Login in ...') # logging in with the email and password passed when executing programs
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
        Quit()

# main part to gather the data
for index in IndexArray:

    # searching for the word
    driver.get('https://www.semrush.com/analytics/keywordoverview/?q=' + KeyWordArray[index].keyword + '&db=fr')

    # waiting for page to load
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div[4]/div[2]/div/div[1]/div/div/div[1]/span[2]/span')))
    except:
        print('error to get data')

    # check if we already used our 10 word per day
    if check_exists_by_xpath('/html/body/div[3]/div/div/div/div/div/div[1]'):
        print("Trial period pop up")
        break;

    # gathering data
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

# end of program
print("Data have been gathered")

# to export back to CSV we need an array of array
ExportArray = []
for element in KeyWordArray:
    ExportArray.append(element.ToExportFormat())

print("Updating file")

# exporting to csv
with open(FilePath, 'w+', newline='', encoding='utf8') as file:
    mywriter = csv.writer(file, delimiter=';')
    mywriter.writerows(ExportArray)
    file.close()

print('byebye')
Quit()
