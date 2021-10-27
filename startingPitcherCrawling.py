#선발투수 라인업 크롤링
#밤 12시마다 크롤링

from datetime import datetime, timedelta
import re
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

TEAM_CODE= dict(NC='NC', 두산='OB', KT='KT', LG='LG', 키움='WO', KIA='HT', 롯데='LT', 삼성='SS', SSG='SK', 한화='HH')

# selenium에서 사용할 웹 드라이버 절대 경로 정보(변경)
# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver=webdriver.Chrome('C:/Users/X-Note/Desktop/WIND-UP/chromedriver.exe')
#url 접근
URL = 'https://sports.news.naver.com/kbaseball/schedule/index'
driver.get(URL)

class Data:
    def __init__(self, date, name, team, position, oppositeTeam):
        self.oppositeTeam = oppositeTeam
        self.date=date
        self.name=name
        self.team=team
        self.position=position

    def getDate(self):
        return self.date

    def getName(self):
        return self.name

    def getTeam(self):
        return self.team

    def getPosition(self):
        return self.position

    def getOppositeTeam(self):
        return self.oppositeTeam

    def __str__(self):
        return self.name

#크롤링
def crawling(today):
    lineups = []
    position='선발투수'
    URL = 'https://sports.news.naver.com/kbaseball/schedule/index?date='+ str(today)
    driver.get(URL)
    time.sleep(3)
    gameList=driver.find_elements_by_class_name('before_game')
    for e in gameList:
        names=[]
        myTeam=[]
        oppositeTeam=[]
        teams=e.find_elements_by_class_name('vs_team')
        for i in range(2):
            teaminfo=teams[i].text
            infoList=teaminfo.split("선")
            remove="\n"
            for r in range(len(remove)):
                infoList[0]=infoList[0].replace(remove[r], "")
            myTeam.append(infoList[0])
            names.append(infoList[1])

        for i in reversed(range(2)):
            oppositeTeam.append(myTeam[i])

        for i in range(2):
            print(names[i])
            print(myTeam[i])
            print(oppositeTeam[i])
            print()
            lineups.append(Data(today, names[i], myTeam[i], position, oppositeTeam[i]))

    return lineups

def saveArticle(csvName, today):
    statList=crawling(today)
    print("csv 제작 시작")
    date=[]
    name =[]
    team =[]
    position=[]
    oppositeTeam =[]

    for a in statList:
        date.append(a.getDate())
        name.append(a.getName())
        team.append(a.getTeam())
        position.append(a.getPosition())
        oppositeTeam.append(a.getOppositeTeam())

    df={
        'date' : date,
        'name' : name,
        'team' : team,
        'position' : position,
        'oppositeTeam' : oppositeTeam
    }

    dataFrame=DataFrame(df)

    #csv 이름 설정
    dataFrame.to_csv(csvName, sep=',', na_rep='NaN', mode='a')
    print("끝~~")

#크롤링
saveArticle('startingLineup_20211027.csv', 20211027)
