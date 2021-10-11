from datetime import datetime, timedelta
import re
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By

TEAM_NAME = dict(NC='NC', OB='두산', KT='KT', LG='LG', WO='키움', HT='KIA', LT='롯데', SS='삼성', SK='SK', HH='한화')

# selenium에서 사용할 웹 드라이버 절대 경로 정보(변경)
# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver=webdriver.Chrome('C:/Users/X-Note/Desktop/WIND-UP/chromedriver.exe')
#url 접근
URL = 'https://sports.news.naver.com/kbaseball/news/index?isphoto=N&type=team&team='
driver.get(URL)

class Data:
    def __init__(self, url, team, date, time, publisher, journalist, title, content):
        self.url=url
        self.team=team
        self.date=date
        self.time=time
        self.publisher=publisher
        self.journalist=journalist
        self.title=title
        self.content=content

    def getUrl(self):
        return self.url

    def getTeam(self):
        return self.team

    def getDate(self):
        return self.date

    def getTime(self):
        return self.time

    def getPublisher(self):
        return self.publisher

    def getJournalist(self):
        return self.journalist

    def getTitle(self):
        return self.title

    def getContent(self):
        return self.content

    def setUrl(self, url):
        self.url=url

    def setTeam(self, team):
        self.team=team

    def setDate(self,date):
        self.date=date

    def setTime(self, time):
        self.time=time

    def setPublisher(self, publisher):
        self.publisher=publisher

    def setJournalist(self, journalist):
        self.journalist=journalist

    def setTitle(self, title):
        self.title=title

    def setContent(self, content):
        self.content=content

    def __str__(self):
        return 'url: '+self.url+' 구단: '+self.team+' 날짜: '+self.date+' 시간: '+self.time+' 출판: '+self.journalist+\
               ' 기자: '+self.journalist+' 제목: '+self.title+' 내용: '+self.content

#날짜 설정
def dateRange(start, end):
    start=datetime.strptime(start, "%Y%m%d")
    end=datetime.strptime(end, "%Y%m%d")
    dates=[(start+timedelta(days=i)).strftime("%Y%m%d") for i in range((end-start).days+1)]
    return dates

#데이터가져오기
#url
def getUrl():
    urlEle= driver.find_elements_by_class_name('thmb')
    urlList=[]
    for e in urlEle:
        urlList.append(e.get_attribute('href'))
    return urlList

#구단
def getTeam():
    teamEle=driver.find_element_by_xpath()
    teamList=[]
    for e in teamEle:
        teamList.append(e.get_attribute(''))
    return teamList

#날짜 설정
def getDate():
    startDate="20211011"
    endDate="20211011"
    days=[]
    dates=dateRange(startDate, endDate)
    for e in dates:
        days.append(e)
    return days

#크롤링
def crawling(url): #date, time, publisher, journalist, title, content
    driver.get(url)
    #날짜와시간
    dateAndTime=driver.find_element_by_class_name('info')
    dateAndTime=dateAndTime.text
    #날짜
    date=dateAndTime[5:15]
    deleteChar='.'
    date=''.join(x for x in date if x not in deleteChar)
    print("날짜: "+date)
    #시간
    time=dateAndTime[17:25]
    print("시간: "+time)

    #출판
    publisher=driver.find_element_by_class_name('source')
    publisher=publisher.text
    publisher=publisher[5:]
    print("출판: "+publisher)

    #기자
    journalist=driver.find_element_by_class_name('byline')
    journalist=journalist.text
    deleteString = "기자 "
    journalist = ''.join(x for x in journalist if x not in deleteString)
    print("기자: "+journalist)

    #제목
    title=driver.find_element_by_class_name('title')
    title=title.text
    print("기사제목: "+title)

    #내용
    allContent = driver.find_element_by_id('newsEndContents').text
    try:
        #사진 설명 제거
         deleteTag=driver.find_element_by_class_name('img_desc').text(By.CLASS_NAME,'img_desc')
         print("삭제할 태그 문장: " + deleteTag)
         allContent = ''.join(x for x in allContent if x not in deleteTag)

         contentText = str(str(allContent).split('기사')[0]).replace("\n", ' ')
         contentText = re.sub(r'\[[^)]*]', '', contentText)
         contentText = re.sub(r'\[[^)]*\)', '', contentText)
         print("기사내용:")
         print(contentText)
    except:
        contentText = str(str(allContent).split('기사')[0]).replace("\n", ' ')
        contentText = re.sub(r'\[[^)]*]', '', contentText)
        contentText = re.sub(r'\[[^)]*\)', '', contentText)
        print("기사내용:")
        print(contentText)
    return date, time, publisher, journalist, title, contentText

#변경
def start_crawling(teamCode):
    data=[]
    teamName=TEAM_NAME[teamCode]
    print("팀이름: "+teamName)
    days=getDate()
    for date in days:
        print("기사 날짜:"+date)
        try:
            URL='https://sports.news.naver.com/kbaseball/news/index?isphoto=N&type=team&team=' + teamCode + '&date=' + date
            print('url:'+ URL)
            driver.get(URL)
            articleAddress=getUrl()
            for a in articleAddress:
                articleURL=a
                print("기사URL :"+articleURL)
                date, time, publisher, journalist, title, contents=crawling(a)
                print(2)
                article=Data(articleURL, teamName, date, time, publisher, journalist, title, contents)
                print(3)
                data.append(article)
                print("완")
        except:
            print("예외")
        return data

def saveArticle(teamCode):
    articleList=start_crawling(teamCode)
    print("csv 제작 시작")
    url=[]
    team=[]
    date=[]
    time=[]
    publisher=[]
    journalist=[]
    title=[]
    content=[]
    for a in articleList:
        url.append(a.getUrl())
        team.append(a.getTeam())
        date.append(a.getDate())
        time.append(a.getTime())
        publisher.append(a.getPublisher())
        journalist.append(a.getJournalist())
        title.append(a.getTitle())
        content.append(a.getContent())

    df={
        'url': url,
        'team': team,
        'date': date,
        'time': time,
        'publisher': publisher,
        'journalist': journalist,
        'title': title,
        'content': content }

    dataFrame=DataFrame(df)

    #csv 이름 설정
    dataFrame.to_csv('article_KT(2016-2017).csv', sep=',', na_rep='NaN', mode='a')

#크롤링
#할 때마다 팀코드 확인
saveArticle('KT')
print("끝~~")