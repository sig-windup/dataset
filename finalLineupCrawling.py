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
    def __init__(self, date, name, team, position, order):
        self.order = order
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

    def getOrder(self):
        return self.order

    def __str__(self):
        return self.name

#크롤링
def games(today):
    URL = 'https://sports.news.naver.com/kbaseball/schedule/index?date='+ str(today)
    print(URL)
    driver.get(URL)
    time.sleep(3)
    gameList = driver.find_elements_by_class_name('end')
    #gameList=driver.find_elements_by_class_name('before_game')
    myTeam = []
    oppositeTeam = []
    for e in gameList:
        teams=e.find_elements_by_class_name('vs_team')
        for i in range(2):
            teaminfo=teams[i].text
            if teaminfo.find('패')==-1:
                infoList = teaminfo.split("승")
            else:
                infoList=teaminfo.split("패")
            remove="\n"
            for r in range(len(remove)):
                infoList[0]=infoList[0].replace(remove[r], "")
            myTeam.append(infoList[0])

    for i in range(len(myTeam)):
        if(i%2==0):
            oppositeTeam.append(myTeam[i+1])
        else:
            oppositeTeam.append(myTeam[i-1])

    return myTeam, oppositeTeam

def crawling(URL, today):
    print(URL)
    driver.get(URL)
    time.sleep(3)
    teams=driver.find_elements_by_class_name('Lineup_lineup_title__1WigY')
    playerList = driver.find_elements_by_class_name('Lineup_lineup_list__1_CNQ')
    lineups=[]
    for t in range(0, len(teams)):
        for i in range(10):
            teamPlayer = playerList[t].find_elements_by_tag_name('li')[i]
            date=today
            print(date)
            name=teamPlayer.find_element_by_class_name('Lineup_name__jV19m').text
            print(name)
            team=teams[t].text
            team = team.split("선발")[0]
            print(team)
            position=teamPlayer.find_element_by_class_name('Lineup_position__265hb').text
            position=position.split(',')[0]
            print(position)
            order=i
            print()
            lineups.append(Data(date, name, team, position, order))
    return lineups


def startCrawling(today):
    lineup=[]
    team1, team2=games(today)
    print(team1)
    print(team2)
    print(len(team1))
    for i in range(len(team1)):
        if i%2==0:
            print(i)
            awayTeamCode = TEAM_CODE[team1[i]]
            print(awayTeamCode)
            homeTeamCode = TEAM_CODE[team2[i]]
            print(homeTeamCode)
            lineupUrl='https://m.sports.naver.com/game/'+str(today)+ awayTeamCode + homeTeamCode+'02021/lineup'
            lineup += crawling(lineupUrl,today)

    return lineup

def saveArticle(csvName, today):
    lineupList=startCrawling(today)
    print("csv 제작 시작")
    date=[]
    name =[]
    team =[]
    position=[]
    order =[]

    for a in lineupList:
        date.append(a.getDate())
        name.append(a.getName())
        team.append(a.getTeam())
        position.append(a.getPosition())
        order.append(a.getOrder())

    df={
        'date' : date,
        'name' : name,
        'team' : team,
        'position' : position,
        'order' : order
    }

    dataFrame=DataFrame(df)

    #csv 이름 설정
    dataFrame.to_csv(csvName, sep=',', na_rep='NaN', mode='a')
    print("끝~~")

#크롤링
saveArticle('finalLineup_20211026.csv', 20211026)
