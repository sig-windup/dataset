from pandas import DataFrame
from selenium import webdriver
import time
from selenium.webdriver.support.select import Select

TEAM_NAME = dict(NC='NC', OB='두산', KT='KT', LG='LG', WO='키움', HT='KIA', LT='롯데', SS='삼성', SK='SSG', HH='한화')

# selenium에서 사용할 웹 드라이버 절대 경로 정보(변경)
# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver=webdriver.Chrome('C:/Users/X-Note/Desktop/WIND-UP/chromedriver.exe')
#url 접근
URL = 'https://www.koreabaseball.com/Player/Search.aspx'
driver.get(URL)

class Data:
    def __init__(self, name, backNum, birth, position):
        self.name=name
        self.backNum=backNum
        self.birth=birth
        self.position=position

    def getName(self):
        return self.name

    def getBackNum(self):
        return self.backNum

    def getBirth(self):
        return self.birth

    def getPosition(self):
        return self.position

    def __str__(self):
        return '이름: '+self.name+' 등번호: '+self.backNum+' 생일: '+self.birth+' 포지션: '+self.position

#데이터가져오기
#페이지수 가져오기
def getPages():
    time.sleep(2)
    pageEle=driver.find_elements_by_xpath('/html/body/form/div[3]/section/div/div/div[2]/div/div[2]/div/a')
    pages=[]
    for e in pageEle:
        pages.append(e.get_attribute('id'))
    pages=pages[1:-1]

    print(pages)

    return pages

#크롤링
def crawling(): #name, backNum, birth, position
    time.sleep(2)
    #테이블 가져오기

    tableList=driver.find_element_by_class_name('tEx')
    tbodyList=tableList.find_element_by_tag_name('tbody')
    trList=tbodyList.find_elements_by_tag_name('tr')
    player=[]

    for r in trList:
        backNum=r.find_elements_by_tag_name('td')[0].text
        name=r.find_elements_by_tag_name('td')[1].text
        position=r.find_elements_by_tag_name('td')[3].text
        birth=r.find_elements_by_tag_name('td')[4].text
        player.append(Data(name, backNum, birth, position))

    return player

#변경
def start_crawling(teamName):
    data=[]
    player=[]
    #구단 선택
    selectTeam=Select(driver.find_element_by_class_name('select02'))
    selectTeam.select_by_visible_text(teamName)

    # page 수 구하기
    pages = getPages()

    for i in pages:
        #페이지 클릭
        driver.find_element_by_id(i).click()

        #크롤링
        crawling()
        player+=crawling()

    return player

def saveArticle(teamCode):
    articleList=start_crawling(teamCode)
    print("csv 제작 시작")
    name=[]
    backNum=[]
    birth=[]
    position=[]

    for a in articleList:
        name.append(a.getName())
        backNum.append(a.getBackNum())
        birth.append(a.getBirth())
        position.append(a.getPosition())

    df={
        'name': name,
        'backNum': backNum,
        'birth': birth,
        'position': position }

    dataFrame=DataFrame(df)

    #csv 이름 설정
    dataFrame.to_csv('player_두산.csv', sep=',', na_rep='NaN', mode='a')

#크롤링
#할 때마다 팀코드 확인
saveArticle('두산')
print("끝~~")