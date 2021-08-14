from selenium import webdriver
from datetime import date
from pandas import Series, DataFrame
from datetime import datetime, timedelta
import csv

TEAM_NAME = dict(NC='NC', OB='두산', KT='KT', LG='LG', WO='키움', HT='KIA', LT='롯데', SS='삼성', SK='SSG', HH='한화')
# selenium에서 사용할 웹 드라이버 절대 경로 정보
chromedriver = 'C:/Users/sojun/OneDrive/바탕 화면/SIG/crawling/chromedriver_win32/chromedriver.exe'
# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver = webdriver.Chrome(chromedriver)
# driver로 특정 페이지를 크롤링한다.
URL = 'https://sports.news.naver.com/kbaseball/news/index?isphoto=N&type=team&team='
driver.get(URL)


class Data:
    def __init__(self, team, date, image, content, positive, negative, label):
        self.date = date
        self.team = team
        self.image = image
        self.content = content
        self.positive = positive
        self.negative = negative
        self.label = label

    def getDate(self):
        return self.date

    def getTeam(self):
        return self.team

    def getImage(self):
        return self.image

    def getContent(self):
        return self.content

    def getPositive(self):
        return self.positive

    def getNegative(self):
        return self.negative

    def getLabel(self):
        return self.label

    def setDate(self, date):
        self.date = date

    def setTeam(self, team):
        self.team = team

    def setImage(self, image):
        self.image = image

    def setContent(self, content):
        self.content = content

    def setPositive(self, positive):
        self.positive = positive

    def setNegative(self, negative):
        self.negative = negative

    def setLabel(self, label):
        self.label = label

    def __str__(self):
        return '구단: ' + self.team + ' 날짜: ' + self.date + ' 사진: ' + self.image + ' 내용: ' + self.content + ' positive: ' + self.positive +' negative: ' + self.negative + 'label:' + self.label

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
    dates = date_range("20200505", "20200731")
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

    try:
        title = driver.find_element_by_tag_name('h4')
        content = driver.find_element_by_id('newsEndContents')
        imageElement = driver.find_element_by_xpath('//span[@class=\'end_photo_org\']')
        imageURL = imageElement.find_element_by_tag_name('img').get_attribute('src')

        #좋아요 + 팬이에요
        positive = int(driver.find_elements_by_xpath('//*[@id="content"]/div/div[1]/div/div[4]/div[1]/ul/li[1]/a/span[2]')[0].text) + int(driver.find_elements_by_xpath('//*[@id="content"]/div/div[1]/div/div[4]/div[1]/ul/li[4]/a/span[2]')[0].text)
        # 화나요 + 슬퍼요
        negative = int(driver.find_elements_by_xpath('//*[@id="content"]/div/div[1]/div/div[4]/div[1]/ul/li[3]/a/span[2]')[0].text) + int(driver.find_elements_by_xpath('//*[ @ id = "content"]/div/div[1]/div/div[4]/div[1]/ul/li[2]/a/span[2]')[0].text)

        # 1 = positive 0 = negative
        if(positive > negative):
            label = '1'
        else:
            label = '0'

    except:
        title = driver.find_element_by_tag_name('h3')
        imageURL = '사진 없음'
    return title.text + str(str(content.text).split('기사')[0]).replace("\n", ' '), imageURL, positive, negative, label

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
            content, image, positive, negative, label = getContents(a)
            article = Data(team_name, d, image, content, positive, negative, label)
            data.append(article)
     except:
        print('오류처리')
    return data

def saveYearArticle(team_code):
    objArr = start_crawlingYear(team_code)
    team = []
    date = []
    image = []
    contents = []
    positive= []
    negative = []
    label = []

    for o in objArr:
        team.append(o.getTeam())
        date.append(o.getDate())
        image.append(o.getImage())
        contents.append(o.getContent())
        positive.append(o.getPositive())
        negative.append(o.getNegative())
        label.append(o.getLabel())

    df = {'team': team,
          'date': date,
          'image': image,
          'contents': contents,
          'positive': positive,
          'negative': negative,
          'positive_or_negative': label}

    dataframe = DataFrame(df)
    #구단 변경시 파일명 변경
    dataframe.to_csv('C:/Users/sojun/OneDrive/바탕 화면/SIG/dataset/article_SSG_Labeling.csv', sep=',', na_rep='NaN', mode='a')

# initial-data(팀 코드 하나씩 넣어야 함)
#팀 코드 변경
saveYearArticle('SK')


