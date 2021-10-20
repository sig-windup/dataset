from selenium import webdriver
from pandas import Series, DataFrame
from datetime import datetime, timedelta, date
import csv
from selenium.webdriver.common.keys import Keys

# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver=webdriver.Chrome('C:/Users/X-Note/Desktop/WIND-UP/chromedriver.exe')
# driver로 특정 페이지를 크롤링한다.
URL = 'https://sports.news.naver.com/kbaseball/schedule/index?date='
driver.get(URL)

class Data:
    def __init__(self, date,home,home_time, away,away_time, stadium):
        self.date = date
        self.home = home
        self.home_time = home_time
        self.away = away
        self.away_time = away_time
        self.stadium = stadium

    def getDate(self):
        return self.date

    def getState_game(self):
        return self.state_game

    def getHome(self):
        return self.home

    def getHome_score(self):
        return self.home_score

    def getHome_result(self):
        return self.home_result

    def getHome_time(self):
        return self.home_time

    def getAway(self):
        return self.away

    def getAway_score(self):
        return self.away_score

    def getAway_result(self):
        return self.away_result

    def getAway_time(self):
        return self.away_time

    def getStadium(self):
        return self.stadium

    def setDate(self, date):
        self.date = date

    def setState_game(self, state_game):
        self.state_game = state_game

    def setHome(self, home):
        self.home = home

    def setHome_score(self, home_score):
        self.home_score = home_score

    def setHome_result(self, home_result):
        self.home_result = home_result

    def setHome_time(self, home_time):
        self.home_time = home_time

    def setAway(self, away):
        self.away = away

    def setAway_score(self, away_score):
        self.away_score = away_score

    def setAway_result(self, away_result):
        self.away_result = away_result

    def setAway_time(self, away_time):
        self.away_time = away_time

    def setStadium(self, stadium):
        self.stadium = stadium

    def __str__(self):
        return ' 날짜: ' + self.date + ' 경기상태: ' + self.state_game + ' 홈팀: ' + self.home + ' 홈팀 점수: ' + self.home_score + ' 홈팀 결과: ' + self.home_result + '홈팀 시간:' + self.home_time + ' 원정팀: ' + self.away + ' 원정팀 점수: ' + self.away_score + ' 원정팀 결과: ' + self.away_result + '원정팀 시간:' + self.away_time + '구장:' + self.stadium

def date_range(start, end):
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    dates = [(start + timedelta(days=i)).strftime("%Y%m%d") for i in range((end-start).days+1)]

    return dates

# 원하는 기간의 기사 크롤링
def getYear():
    days = []
    # 기사 기간 설정
    dates = date_range("20211021", "20211022")
    for e in dates:
        days.append(e)
    return days

# li요소의 수를 센다
def getLiCount():
    try:
        li_count1 = driver.find_elements_by_css_selector('#todaySchedule > li.before_game ')
        li_count2 = driver.find_elements_by_css_selector('#todaySchedule > li.type_cancel')
    except:
        print("못 찾음")

    count1 = len(li_count1)
    count2 = len(li_count2)
    count = int(count1) + int(count2)

    return count

#구장을 반환
def getStadium(home):

  stadium = {"NC" : "창원", "삼성": "대구", "kt" : "수원", "KT" : "수원", "롯데" : "사직", "두산" : "잠실", "한화" : "대전", "KIA" : "광주", "LG" : "잠실", "키움" : "고척", "SSG" : "인천", "삼성" : "대구", "넥센" : "고척", "SK" : "인천"}.get(home, "오류")

  return stadium

#일정
def start_crawlingYear():
    data = []
    days = getYear()
    for d in days:
        URL = 'https://sports.news.naver.com/kbaseball/schedule/index?date=' + d
        driver.get(URL)
        count = getLiCount()
        weekDay = date(int(d[0:4]), int(d[4:6]), int(d[6:8])).weekday()
        month = int(d[4:6])
        for i in range(count):
            home, away_time , away, home_time, stadium = getSchedule(i)

            Schedule = Data(d, home, home_time, away, away_time, stadium)
            data.append(Schedule)

    return data

def getSchedule(i):
    if(i == 5):
        driver.find_element_by_css_selector("#_daily_schedule_root > button.button_next").send_keys(Keys.ENTER)
    try:
        home_time = driver.find_elements_by_xpath('//*[@id="todaySchedule"]/li[%d]/div[1]/em' % (i + 1))[0].text
        away_time = driver.find_elements_by_xpath('//*[@id="todaySchedule"]/li[%d]/div[1]/em' % (i + 1))[0].text
    except:
        home_time = '오류'

    away = driver.find_elements_by_xpath('//*[@id="todaySchedule"]/li[%d]/div[2]/p/strong' % (i + 1))[0].text
    home = driver.find_elements_by_xpath('//*[@id="todaySchedule"]/li[%d]/div[3]/p/strong' % (i + 1))[0].text

    stadium = getStadium(home)

    return home, away_time , away, home_time, stadium

#이부분 부터
#데이터 저장
def saveYearArticle():
    objArr = start_crawlingYear()
    date = []
    home = []
    home_time = []
    away = []
    away_time = []
    stadium = []

    for o in objArr:
        date.append(o.getDate())
        home.append(o.getHome())
        home_time.append(o.getHome_time())
        away.append(o.getAway())
        away_time.append(o.getAway_time())
        stadium.append(o.getStadium())

    df = {'date': date,
          'home': home,
          'home_time': home_time,
          'away': away,
          'away_time': away_time,
          'stadium': stadium}

    dataframe = DataFrame(df)
    #구단 변경시 파일명 변경
    dataframe.to_csv('Schedule_future(20211021~).csv', sep=',', na_rep='NaN', mode='a')

saveYearArticle()