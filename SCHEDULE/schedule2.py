from selenium import webdriver
from pandas import Series, DataFrame
from datetime import datetime, timedelta, date
import csv
from selenium.webdriver.common.keys import Keys

# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver = webdriver.Chrome('C:/Users/sojun/OneDrive/바탕 화면/SIG/crawling/chromedriver_win32/chromedriver.exe')
# driver로 특정 페이지를 크롤링한다.
URL = 'https://sports.news.naver.com/kbaseball/schedule/index?date='
driver.get(URL)

class Data:
    def __init__(self, date, state_game, home, home_score, home_result, home_time, away, away_score, away_result, away_time, stadium):
        self.date = date
        self.state_game = state_game
        self.home = home
        self.home_score = home_score
        self.home_result = home_result
        self.home_time = home_time
        self.away = away
        self.away_score = away_score
        self.away_result = away_result
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
    dates = date_range("20210321", "20210718")
    for e in dates:
        days.append(e)
    return days

# li요소의 수를 센다
def getLiCount():
    try:
        li_count1 = driver.find_elements_by_css_selector('#todaySchedule > li.end')
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
            state_game, home, home_score, home_result, away, away_score, away_result, stadium = getSchedule(i)

            try:
                #더블헤더
                DH = state_game = driver.find_elements_by_xpath('//*[@id="todaySchedule"]/li[%d]/div[1]/p' % (i + 1))[0].text
            except:
                DH = '없음'

            if home_result == '투' and away_result == '투':
                    home_result = '서스펜디드'
                    away_result = '서스펜디드'
            elif home_result == '선' and away_result == '선':
                    home_result = '취소'
                    away_result = '취소'

            #경기 시간
            #더블헤더1, 토요일경우
            if(DH == 'DH1' and weekDay == 5):
                home_time = '14:00'
                away_time = '14:00'
            #더블헤더1,(7,8)월, 일요일경우
            elif(DH == 'DH1' and weekDay == 6 and month == 7):
                home_time = '14:00'
                away_time = '14:00'
            elif(DH == 'DH1' and weekDay == 6 and month == 8):
                home_time = '14:00'
                away_time = '14:00'
            #더블헤더2,7,8월 제외, 일요일경우
            elif(DH == 'DH2' and weekDay == 6):
                home_time = '17:00'
                away_time = '17:00'
            #더블 헤더 1일때 일요일의 경우 14:00
            elif (DH == 'DH1' and weekDay == 6):
                home_time = '14:00'
                away_time = '14:00'
            #더블헤더 1일경우
            elif(DH == 'DH1'):
                home_time = '14:00'
                away_time = '14:00'
            #3월일경우 년도에따라 다르게 조정
            # elif(month == 3):
            #     home_time = '13:00'
            #     away_time = '13:00'
            #금요일이고 NC일 경우
            elif(weekDay == 4 and home == 'NC'):
                home_time = '19:00'
                away_time = '19:00'
            #평일일 경우
            elif(weekDay == 0 or weekDay == 1 or weekDay == 2 or weekDay == 3 or weekDay == 4):
                home_time = '18:30'
                away_time = '18:30'
            #7,8월 토요일 경우
            elif((weekDay == 5 and month == 7) or (weekDay == 5 and month == 8)):
                home_time = '18:00'
                away_time = '18:00'
            # 7,8월 일요일경우
            elif((weekDay == 6 and month == 7) or (weekDay == 6 and month == 8)):
                home_time = '17:00'
                away_time = '17:00'
            #토요일경우
            elif(weekDay == 5):
                home_time = '17:00'
                away_time = '17:00'
            #일요일경우
            elif(weekDay == 6):
                home_time = '14:00'
                away_time = '14:00'
            else:
                home_time = '오류'
                away_time = '오류'

            Schedule = Data(d, state_game, home, home_score, home_result, home_time, away, away_score, away_result, away_time, stadium)
            data.append(Schedule)

    return data

def getSchedule(i):
    if(i == 5):
        driver.find_element_by_css_selector("#_daily_schedule_root > button.button_next").send_keys(Keys.ENTER)
    try:
        state_game = driver.find_elements_by_xpath('//*[@id="todaySchedule"]/li[%d]/div[1]/em' % (i + 1))[0].text
    except:
        state_game = '종료'

    away = driver.find_elements_by_xpath('//*[@id="todaySchedule"]/li[%d]/div[2]/p/strong' % (i + 1))[0].text
    home = driver.find_elements_by_xpath('//*[@id="todaySchedule"]/li[%d]/div[3]/p/strong' % (i + 1))[0].text

    try:
            away_score = driver.find_elements_by_xpath('//*[@id="todaySchedule"]/li[%d]/div[2]/strong' % (i + 1))[0].text
            home_score = driver.find_elements_by_xpath('//*[@id="todaySchedule"]/li[%d]/div[3]/strong' % (i + 1))[0].text
    except:
            away_score = '취소'
            home_score = '취소'
    try:
            away_result = driver.find_elements_by_xpath('//*[@id="todaySchedule"]/li[%d]/div[2]/p/span/span' % (i + 1))[0].text
            home_result = driver.find_elements_by_xpath('//*[@id="todaySchedule"]/li[%d]/div[3]/p/span/span' % (i + 1))[0].text
    except:
            away_result = '무승부'
            home_result = '무승부'

    stadium = getStadium(home)

    #왜 넥센을 인지를 못하는 걸까?
    #인지는 하지만 바꾸지를 않는다
    if (home == '넥센'):
        home = '키움'
    elif (away == '넥센'):
        away = '키움'
    elif (home == 'SK'):
        home = 'SSG'
    elif (away == 'SK'):
        away = 'SSG'
    elif (home == '넥센' and away == 'SK'):
        home = '키움'
        away = 'SSG'
    elif (home == 'SK' and away == '넥센'):
        home = 'SSG'
        away = '키움'

    return state_game, home, home_score, home_result, away, away_score, away_result, stadium

#이부분 부터
#데이터 저장
def saveYearArticle():
    objArr = start_crawlingYear()
    date = []
    state_game = []
    home = []
    home_score = []
    home_result = []
    home_time = []
    away = []
    away_score = []
    away_result = []
    away_time = []
    stadium = []

    for o in objArr:
        date.append(o.getDate())
        state_game.append(o.getState_game())
        home.append(o.getHome())
        home_score.append(o.getHome_score())
        home_result.append(o.getHome_result())
        home_time.append(o.getHome_time())
        away.append(o.getAway())
        away_score.append(o.getAway_score())
        away_result.append(o.getAway_result())
        away_time.append(o.getAway_time())
        stadium.append(o.getStadium())

    df = {'date': date,
          'state_game': state_game,
          'home': home,
          'home_score': home_score,
          'home_result': home_result,
          'home_time': home_time,
          'away': away,
          'away_score': away_score,
          'away_result': away_result,
          'away_time': away_time,
          'stadium': stadium}

    dataframe = DataFrame(df)
    #구단 변경시 파일명 변경
    dataframe.to_csv('C:/Users/sojun/OneDrive/바탕 화면/SIG/dataset/Schedule.csv', sep=',', na_rep='NaN', mode='a')

saveYearArticle()

