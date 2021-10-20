#투수 스탯
from datetime import datetime, timedelta
import re
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

TEAM_NAME = dict(NC='NC', OB='두산', KT='KT', LG='LG', WO='키움', HT='KIA', LT='롯데', SS='삼성', SK='SK', HH='한화')

# selenium에서 사용할 웹 드라이버 절대 경로 정보(변경)
# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver=webdriver.Chrome('C:/Users/X-Note/Desktop/WIND-UP/chromedriver.exe')
#url 접근
URL = 'http://www.kbreport.com/leader/pitcher/main'
driver.get(URL)

class Data:
    #                                            승 패  세  홀드  블론  경기 선발 이닝 삼진/9 볼넷/9 홈런/9 BABIP LOB% ERA RA9-WAR FIP KFIP WAR
    def __init__(self, name, team, oppositeTeam, w, l, 세, hld, 블론, 경기, gs, ip, k, bb, hr, babip, lob, era, ra, fip, kfip, war):
        self.name=name
        self.team=team
        self.oppositeTeam=oppositeTeam
        self.w=w
        self.l=l
        self.세=세
        self.hld=hld
        self.블론=블론
        self.경기=경기
        self.gs=gs
        self.ip=ip
        self.k=k
        self.bb=bb
        self.hr=hr
        self.babip=babip
        self.lob=lob
        self.era=era
        self.ra=ra
        self.fip=fip
        self.kfip=kfip
        self.war=war

    def getName(self):
        return self.name

    def getTeam(self):
        return self.team

    def getOppositeTeam(self):
        return self.oppositeTeam

    def getW(self):
        return self.w

    def getL(self):
        return self.l

    def get세(self):
        return self.세

    def getHld(self):
        return self.hld

    def get블론(self):
        return self.블론

    def get경기(self):
        return self.경기

    def getGs(self):
        return self.gs

    def getIp (self):
        return self.ip

    def getK (self):
        return self.k

    def getBb (self):
        return self.bb

    def getHr (self):
        return self.hr

    def getBabip(self):
        return self.babip

    def getLob(self):
        return self.lob

    def getEra(self):
        return self.era

    def getRa(self):
        return self.ra

    def getFip(self):
        return self.fip

    def getKfip(self):
        return self.kfip

    def getWar(self):
        return self.war

    def __str__(self):
        return self.name

def getPage(URL):
    driver.get(URL)
    time.sleep(2)
    pageEle=driver.find_elements_by_class_name('paging-num-box')
    pageHref=pageEle[0].find_elements_by_tag_name('a')
    pages=[]

    for e in pageHref:
        pages.append(e.get_attribute('page'))
    #None값 제거
    pages=list(filter(None, pages))

    return pages

#크롤링
def crawling(URL):
    driver.get(URL)
    time.sleep(3)

    #테이블 가져오기
    table=driver.find_element_by_xpath('//*[@id="resultListDiv"]/div[2]/div[1]/table')
    tbody=table.find_element_by_tag_name('tbody')
    trList=tbody.find_elements_by_tag_name('tr')
    #목록 제거
    trList=trList[1:]

    #스탯 크롤링
    stats=[]
    for tds in trList:
        name=tds.find_elements_by_tag_name('td')[1].text
        team=tds.find_elements_by_tag_name('td')[2].text
        if team=="Hero":
            team="키움"
        oppositeTeam=tds.find_elements_by_tag_name('td')[3].text
        if oppositeTeam=="Hero":
            oppositeTeam="키움"
        w=tds.find_elements_by_tag_name('td')[4].text
        l=tds.find_elements_by_tag_name('td')[5].text
        세=tds.find_elements_by_tag_name('td')[6].text
        hld=tds.find_elements_by_tag_name('td')[7].text
        블론=tds.find_elements_by_tag_name('td')[8].text
        경기=tds.find_elements_by_tag_name('td')[9].text
        gs=tds.find_elements_by_tag_name('td')[10].text
        ip=tds.find_elements_by_tag_name('td')[11].text
        k=tds.find_elements_by_tag_name('td')[12].text
        bb=tds.find_elements_by_tag_name('td')[13].text
        hr=tds.find_elements_by_tag_name('td')[14].text
        babip=tds.find_elements_by_tag_name('td')[15].text
        lob=tds.find_elements_by_tag_name('td')[16].text
        era=tds.find_elements_by_tag_name('td')[17].text
        ra=tds.find_elements_by_tag_name('td')[18].text
        fip=tds.find_elements_by_tag_name('td')[19].text
        kfip=tds.find_elements_by_tag_name('td')[20].text
        war=tds.find_elements_by_tag_name('td')[21].text
        stats.append(Data(name, team, oppositeTeam, w, l, 세, hld, 블론, 경기, gs, ip, k, bb, hr, babip, lob, era, ra, fip, kfip, war))
    print(stats)
    return stats

#변경
def start_crawling(inputTeamCode, inputStartYear, inputEndYear, inputGameType):
    # 스탯 저장 리스트
    stats=[]
    #설정
    #팀
    teamId=inputTeamCode
    #상대팀
    oppositeTeamList=['1', '2', '3', '4', '5', '7', '8', '9', '15', '16']
    #시즌범위 설정
    startYear=inputStartYear
    endYear=inputEndYear
    gameType=inputGameType

    print(teamId)

    for oppositeTeamId in oppositeTeamList:
        if(teamId!=oppositeTeamId):
            print(oppositeTeamId)
            getPageURL = 'http://www.kbreport.com/leader/pitcher/main?rows=20&order=WAR&orderType=DESC&teamId=' + teamId + '&pitcher_type=&year_from=' + startYear + '&year_to=' + endYear + '&gameType=' + gameType + '&split01=opposite&split02_1=' + oppositeTeamId + '&split02_2=&r_inning_count=&inning_count=0'

            # 페이지 수
            pages = getPage(getPageURL)

            for page in pages:
                # 크롤링할 URL
                URL = 'http://www.kbreport.com/leader/pitcher/main?rows=20&order=WAR&orderType=DESC&teamId=' + teamId + '&pitcher_type=&year_from=' + startYear + '&year_to=' + endYear + '&gameType=' + gameType + '&split01=opposite&split02_1=' + oppositeTeamId \
                      + '&split02_2=&r_inning_count=&inning_count=0#/' + page
                print(URL)

                # 크롤링
                stats += crawling(URL)

    return stats

def saveArticle():
    # 팀, 시즌시작, 종료시즌, R:정규시즌 (P:포스트시즌)
    # 팀: [1:두산, 2:삼성, 3:KIA, 4:키움, 5:LG, 7:NC, 8:한화, 9:롯데, 15:KT, 16:SSG]
    statList=start_crawling('1', '2021', '2021', 'R')
    print("csv 제작 시작")
    name =[]
    team =[]
    oppositeTeam =[]
    w =[]
    l =[]
    세 =[]
    hld =[]
    블론 =[]
    경기 =[]
    gs =[]
    ip =[]
    k =[]
    bb =[]
    hr =[]
    babip =[]
    lob =[]
    era =[]
    ra =[]
    fip =[]
    kfip =[]
    war =[]

    for a in statList:
        name.append(a.getName())
        team.append(a.getTeam())
        oppositeTeam.append(a.getOppositeTeam())
        w.append(a.getW())
        l.append(a.getL())
        세.append(a.get세())
        hld.append(a.getHld())
        블론.append(a.get블론())
        경기.append(a.get경기())
        gs.append(a.getGs())
        ip.append(a.getIp())
        k.append(a.getK())
        bb.append(a.getBb())
        hr.append(a.getHr())
        babip.append(a.getBabip())
        lob.append(a.getLob())
        era.append(a.getEra())
        ra.append(a.getRa())
        fip.append(a.getFip())
        kfip.append(a.getKfip())
        war.append(a.getWar())

    df={
        'name' : name,
        'team' : team,
        'oppositeTeam' : oppositeTeam,
        'w' : w,
        'l' : l,
        '세' : 세,
        'hld' : hld,
        '블론' : 블론,
        '경기' : 경기,
        'gs' : gs,
        'ip' : ip,
        'k' : k,
        'bb' : bb,
        'hr' : hr,
        'babip' : babip,
        'lob' : lob,
        'era' : era,
        'ra' : ra,
        'fip' : fip,
        'kfip' : kfip,
        'war' : war }

    dataFrame=DataFrame(df)

    #csv 이름 설정
    dataFrame.to_csv('pitcher_stat_DS.csv', sep=',', na_rep='NaN', mode='a')

#크롤링
saveArticle()
print("끝~~")