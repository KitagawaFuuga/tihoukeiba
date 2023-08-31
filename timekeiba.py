from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import datetime
from plyer import notification
import schedule
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

hrefcheck = []
times = []
printtime = []
numnum = 0

today = datetime.date.today()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}    
cookie = {'PHPSESSID': '0gdrs90067ph9j2c9fk83f9t25'}
session = requests.session()

url2 = "https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/TodayRaceInfoTop"
custom_path = "C:\yami\python"

driver_Path = EdgeChromiumDriverManager(path=custom_path).install()
driv = webdriver.Edge(driver_Path)
driv.get(url2)

ren = BeautifulSoup(driv.page_source, "html.parser")

for element in ren.find_all('td'):
    hrefcheck.append(element)
    for k in element.find_all('a',class_='raceName'):
        url = k.get('href')
        race_date = url.split('k_raceDate=')[1].split('&')[0].replace('%2f', '')
        result = f'{race_date}'
        print(result)
        for i in k.find_all('span'):
            print(i.text)

for i in hrefcheck[1].find_all('a'):
    print(i.text)
    
print("どのレースを通知しますか？")
ans = input()

for i in hrefcheck[1].find_all('a'):
    if ans in i.text:
        print(i.text)
        url = "https://www.keiba.go.jp" + i.get('href')
        
driv.get(url)

ren2 = BeautifulSoup(driv.page_source, "html.parser")

for element in ren2.find_all('tr'):
    for i in element.find_all('td'):
        times.append(i.text)
        for k in i.find_all('a'):
            if k.text != "オッズ":
                numnum = numnum + 1
 
print(str(numnum/3) + "レースです")
for runrun in range(1,int((numnum / 3)*10 + 1),10):
    if (times[runrun]) != 2:
        print(times[runrun])
        printtime.append(times[runrun])
    


time.sleep(3)
driv.quit()
    
def task():
    notification.notify(
        title = ans,
        message = "出走します",
        timeout=60
    ) 

for i in printtime:
    schedule.every().day.at(i).do(task)

while True:
    schedule.run_pending()
    time.sleep(1)