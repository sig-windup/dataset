from selenium import webdriver

# selenium에서 사용할 웹 드라이버 절대 경로 정보
chromedriver = 'C:\pgm\Python\Windup\chromedriver.exe'
# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver = webdriver.Chrome(chromedriver)
# driver로 특정 페이지를 크롤링한다.
URL = 'https://sports.news.naver.com/kbaseball/news/index?isphoto=N&type=team&team='
driver.get(URL)

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


def getArticles():
    ele = driver.find_elements_by_xpath('//div[@id=\'_newsList\']/ul/li/div[@class=\'text\']/a[@class=\'title\']')
    address = []
    for e in ele:
        address.append(e.get_attribute('href'))
    return address


# 기사의 제목과 내용 크롤링
def crawling_contents(address):
    for i in range(len(address)):
        driver.get(address[i])
        title = driver.find_element_by_tag_name('h4')
        contents = driver.find_element_by_id('newsEndContents')
        print(title.text, str(contents.text).split('기사제공'))


# 최근 5일의 전 구단 기사 크롤링(부하 걸림 ㅜ)
def start_crawling(URL):
    days = get5Days()
    for d in days:
        print(d)
        URL = URL + '&date=' + d
        driver.get(URL)
        address = getArticles()
        crawling_contents(address)


# team 코드로 최근 5일 기사 크롤링
def start_crawling(team_code):
    days = get5Days()
    for d in days:
        print(d)
        URL = 'https://sports.news.naver.com/kbaseball/news/index?isphoto=N&type=team&team=' + team_code + '&date=' + d
        driver.get(URL)
        address = getArticles()
        crawling_contents(address)


# 전 구단 오늘 기사 크롤링
def today_crawling(URL):
    driver.get(URL)
    address = getArticles()
    crawling_contents(address)



days = get5Days()
# [Index] 0: NC, 1: 두산, 2: KT, 3: LG, 4: 키움, 5: KIA, 6: 롯데, 7: 삼성, 8: SSG, 9: 한화
teams = getTeams()

'''
[전 구단 오늘 기사 크롤링하기]
for t in teams:
    print(t)
    URL += t
    today_crawling(URL)
    URL = 'https://sports.news.naver.com/kbaseball/news/index?isphoto=N&type=team&team='
'''

'''
[특정 구단 5일 크롤링하기]
start_crawling(teams[6])
'''

# TODO: 데이터들을 정제해서 CSV 파일로 만들기(id, 일자, 구단, 전체 내용)
