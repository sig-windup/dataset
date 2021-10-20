#라인업
#경기 시작 전 크롤링

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
        self.date=date
        self.name=name
        self.team=team
        self.position=position
        self.order=order

    def getDate(self):
        return self.date

    def getName(self):
        return self.name

    def getTeam(self):
        return self.team

    def getPosition(self):
        return  self.position

    def getOrder(self):
        return self.order

    def __str__(self):
        return self.name

#크롤링
def crawling(URL, csvDate):
    print(URL)
    driver.get(URL)
    time.sleep(3)
    teams=driver.find_elements_by_class_name('Lineup_lineup_title__1WigY')
    playerList = driver.find_elements_by_class_name('Lineup_lineup_list__1_CNQ')
    lineups=[]
    for t in range(0, len(teams)):
        for i in range(10):
            teamPlayer = playerList[t].find_elements_by_tag_name('li')[i]
            date=csvDate
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

#변경
def start_crawling():
    # 스탯 저장 리스트
    lineup=[]

    #경기일정 csv 가져오기
    csvFile=pd.read_csv("C:/Users/X-Note/PycharmProjects/WindUp/Schedule.csv", encoding='UTF-8')

    gameDate=[]
    home=[]
    away=[]
    isCancle=[] #취소여부
    for row_index, row in csvFile.iterrows():
        gameDate.append(row[1])
        home.append(row[3])
        away.append(row[7])
        isCancle.append(row[2])

    index=len(gameDate)
    for i in range(index):
        homeTeamCode = TEAM_CODE[home[i]]
        awayTeamCode = TEAM_CODE[away[i]]
        if isCancle[i]!="취소":
            URL = 'https://m.sports.naver.com/game/' + str(gameDate[i]) + awayTeamCode + homeTeamCode + '02021/lineup'
            # 크롤링
            lineup += crawling(URL,gameDate[i])

    return lineup

def saveArticle():
    # 팀, 시즌시작, 종료시즌, R:정규시즌 (P:포스트시즌)
    # 팀: [1:두산, 2:삼성, 3:KIA, 4:키움, 5:LG, 7:NC, 8:한화, 9:롯데, 15:KT, 16:SSG]
    statList=start_crawling()
    print("csv 제작 시작")
    date=[]
    name =[]
    team =[]
    position=[]
    order=[]
    for a in statList:
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
        'order' : order }

    dataFrame=DataFrame(df)

    #csv 이름 설정
    dataFrame.to_csv('lineup_past.csv', sep=',', na_rep='NaN', mode='a')

#크롤링
saveArticle()
print("끝~~")