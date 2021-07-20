from selenium import webdriver
from datetime import date
from pandas import Series, DataFrame
from datetime import datetime, timedelta
import re
import csv

TEAM_NAME = dict(NC='NC', OB='두산', KT='KT', LG='LG', WO='키움', HT='KIA', LT='롯데', SS='삼성', SK='SK', HH='한화')
# selenium에서 사용할 웹 드라이버 절대 경로 정보
chromedriver = 'C:\pgm\Python\Windup\chromedriver.exe'
# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver = webdriver.Chrome(chromedriver)
# driver로 특정 페이지를 크롤링한다.
URL = 'https://sports.news.naver.com/kbaseball/news/index?isphoto=N&type=team&team='
driver.get(URL)



class Data:
    def __init__(self, team, date, time, image, content):
        self.date = date
        self.time = time
        self.team = team
        self.image = image
        self.content = content

    def getDate(self):
        return self.date

    def getTime(self):
        return self.time

    def getTeam(self):
        return self.team

    def getImage(self):
        return self.image

    def getContent(self):
        return self.content

    def setDate(self, date):
        self.date = date

    def setTime(self, time):
        self.time = time

    def setTeam(self, team):
        self.team = team

    def setImage(self, image):
        self.image = image

    def setContent(self, content):
        self.content = content

    def __str__(self):
        return '구단: ' + self.team + ' 날짜: ' + self.date + ' 시간: ' + self.time +' 사진: ' + self.image + ' 내용: ' + self.content


def date_range(start, end):
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    dates = [(start + timedelta(days=i)).strftime("%Y%m%d") for i in range((end-start).days+1)]
    return dates

# 데이터 가져오기(getTeams(): 구단, get5Days(): 최근 5일, getArticles(): 기사의 주소)
def getTeams():
    teamele = driver.find_elements_by_xpath('//div[@class=\'news_team\']/ul/li')
    teams = []
    for e in teamele:
        if e.get_attribute('data-id') != 'kbo':
            teams.append(e.get_attribute('data-id'))
    return teams

# 원하는 기간의 기사 크롤링
def getYear():
    days = []
    # 기사 기간 설정
    dates = date_range("20160101", "20210712")
    for e in dates:
        days.append(e)
    return days


def getAddress():
    ele = driver.find_elements_by_xpath('//div[@id=\'_newsList\']/ul/li/div[@class=\'text\']/a[@class=\'title\']')
    address = []
    for e in ele:
        address.append(e.get_attribute('href'))
    return address


# 기사의 제목과 내용 크롤링
def getContents(address):
    driver.get(address)
    title = driver.find_element_by_tag_name('h4')
    content = driver.find_element_by_id('newsEndContents')
    content_text = title.text + ' ' + str(str(content.text).split('기사')[0]).replace("\n", ' ')
    content_text = re.sub(r'\[[^)]*]', '', content_text)
    content_text = re.sub(r'\([^)]*\)', '', content_text)
    print(content_text)
    try:
        imageElement = driver.find_element_by_xpath('//span[@class=\'end_photo_org\']')
        imageURL = imageElement.find_element_by_tag_name('img').get_attribute('src')
        timeArr = driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[1]/div/span[1]').text.split(' ')[2:4]
        timeStr = timeArr[0] + ' ' + timeArr[1]
    except:
        imageURL = '사진 없음'
    return content_text, imageURL, timeStr


# team 코드로 기사 크롤링
def start_crawlingYear(team_code):
    data = []
    team_name = TEAM_NAME[team_code]
    days = getYear()
    for d in days:
     try:
        URL = 'https://sports.news.naver.com/kbaseball/news/index?isphoto=N&type=team&team=' + team_code + '&date=' + d
        driver.get(URL)
        address = getAddress()
        for a in address:
            content, image, time = getContents(a)
            article = Data(team_name, d, time, image, content)
            data.append(article)
     except:
        print('오류처리')
    return data

def saveYearArticle(team_code):
    objArr = start_crawlingYear(team_code)
    team = []
    date = []
    time = []
    image = []
    contents = []
    for o in objArr:
        team.append(o.getTeam())
        date.append(o.getDate())
        time.append(o.getTime())
        image.append(o.getImage())
        contents.append(o.getContent())

    df = {'team': team,
          'date': date,
          'time': time,
          'image': image,
          'contents': contents }

    dataframe = DataFrame(df)
    #구단 변경시 파일명 변경
    dataframe.to_csv('article_NC(2016-2021beforebreak).csv', sep=',', na_rep='NaN', mode='a')

# initial-data(팀 코드 하나씩 넣어야 함)
#팀 코드 변경
saveYearArticle('NC')
