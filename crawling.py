from selenium import webdriver
from datetime import date
import csv

TEAM_NAME = dict(NC='NC', OB='두산', KT='KT', LG='LG', WO='키움', HT='KIA', LT='롯데', SS='삼성', SK='SSG', HH='한화')
# selenium에서 사용할 웹 드라이버 절대 경로 정보
chromedriver = 'C:\pgm\Python\Windup\chromedriver.exe'
# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver = webdriver.Chrome(chromedriver)
# driver로 특정 페이지를 크롤링한다.
URL = 'https://sports.news.naver.com/kbaseball/news/index?isphoto=N&type=team&team='
driver.get(URL)


class Data:
    def __init__(self, team, date, image, content):
        self.date = date
        self.team = team
        self.image = image
        self.content = content

    def getDate(self):
        return self.date

    def getTeam(self):
        return self.team

    def getImage(self):
        return self.image

    def getContent(self):
        return self.content

    def setDate(self, date):
        self.date = date

    def setTeam(self, team):
        self.team = team

    def setImage(self, image):
        self.image = image

    def setContent(self, content):
        self.content = content

    def __str__(self):
        return '구단: ' + self.team + ' 날짜: ' + self.date + ' 사진: ' + self.image + ' 내용: ' + self.content


# 데이터 가져오기(getTeams(): 구단, get5Days(): 최근 5일, getArticles(): 기사의 주소)
def getTeams():
    teamele = driver.find_elements_by_xpath('//div[@class=\'news_team\']/ul/li')
    teams = []
    for e in teamele:
        if e.get_attribute('data-id') != 'kbo':
            teams.append(e.get_attribute('data-id'))
    return teams


def get5Days():
    dayele = driver.find_elements_by_xpath('//div[@id=\'_bottomDateList\']/div[@class=\'inner\']/a')
    days = []
    for e in dayele:
        days.append(e.get_attribute('data-id'))
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
    imageElement = driver.find_element_by_xpath('//span[@class=\'end_photo_org\']')
    imageURL = imageElement.find_element_by_tag_name('img').get_attribute('src')
    return title.text + str(str(content.text).split('기사')[0]), imageURL


# team 코드로 최근 5일 기사 크롤링
def start_crawling(team_code):
    data = []
    team_name = TEAM_NAME[team_code]
    days = get5Days()
    for d in days:
        URL = 'https://sports.news.naver.com/kbaseball/news/index?isphoto=N&type=team&team=' + team_code + '&date=' + d
        driver.get(URL)
        address = getAddress()
        for a in address:
            content, image = getContents(a)
            article = Data(team_name, d, image, content)
            data.append(article)
    return data


# 전 구단 오늘 기사 크롤링
def today_crawling(URL):
    data = []
    teams = getTeams()
    for t in teams:
        URL += t
        driver.get(URL)
        address = getAddress()
        for a in address:
            content, image = getContents(a)
            article = Data(TEAM_NAME[t], date.today().strftime('%Y%m%d'), image, content)
            data.append(article)
        URL = 'https://sports.news.naver.com/kbaseball/news/index?isphoto=N&type=team&team='
    return data


# start_crawling(teams[6])
# today_crawling(URL)
