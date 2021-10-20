#타자 스탯
from datetime import datetime, timedelta
import re
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# selenium에서 사용할 웹 드라이버 절대 경로 정보(변경)
# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver=webdriver.Chrome('C:/Users/X-Note/Desktop/WIND-UP/chromedriver.exe')
#url 접근
URL = 'http://www.kbreport.com/leader/main'
driver.get(URL)

class Data:
    #                                            경기 타석 타수 안타 홈런 득점 타점 볼넷 삼진 도루 BABIP 타율 출루율 장타율 OPS wOBA WAR
    def __init__(self, name, team, oppositeTeam, 경기, pa, ab, h, hr, r, rbi, bb, k, sb, babip, avg, obp, slg, ops, woba, war):
        self.name=name
        self.team=team
        self.oppositeTeam=oppositeTeam
        self.경기=경기
        self.pa=pa
        self.ab=ab
        self.h=h
        self.hr=hr
        self.r=r
        self.rbi=rbi
        self.bb = bb
        self.k=k
        self.sb=sb
        self.babip=babip
        self.avg=avg
        self.obp=obp
        self.slg=slg
        self.ops=ops
        self.woba=woba
        self.war=war

    def getName(self):
        return self.name

    def getTeam(self):
        return self.team

    def getOppositeTeam(self):
        return self.oppositeTeam

    def get경기(self):
        return self.경기

    def getPa(self):
        return self.pa

    def getAb(self):
        return self.ab

    def getH(self):
        return self.h

    def getHr (self):
        return self.hr

    def getR(self):
        return self.r

    def getRbi(self):
        return self.rbi

    def getBb (self):
        return self.bb

    def getK (self):
        return self.k

    def getSb(self):
        return self.sb

    def getBabip(self):
        return self.babip

    def getAvg(self):
        return self.avg

    def getObp(self):
        return self.obp

    def getSlg(self):
        return self.slg

    def getOps(self):
        return self.ops

    def getWoba(self):
        return self.woba

    def getWar(self):
        return self.war

    def __str__(self):
        return self.name

def getPage(URL):
    driver.get(URL)
    time.sleep(3)
    pageEle=driver.find_elements_by_class_name('paging-num-box')
    time.sleep(2)
    print("pageEle")
    print(len(pageEle))
    pageHref=pageEle[0].find_elements_by_tag_name('a')
    pages=[]

    for e in pageHref:
        pages.append(e.get_attribute('page'))
    #None값 제거
    pages=list(filter(None, pages))

    print(pages)
    return pages

#크롤링
def crawling(URL):
    print(URL)
    driver.get(URL)
    time.sleep(3)
    #테이블 가져오기
    table = driver.find_element_by_xpath('//*[@id="resultListDiv"]/div[2]/div[1]/table')
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
        경기=tds.find_elements_by_tag_name('td')[4].text
        pa=tds.find_elements_by_tag_name('td')[5].text
        ab=tds.find_elements_by_tag_name('td')[6].text
        h=tds.find_elements_by_tag_name('td')[7].text
        hr=tds.find_elements_by_tag_name('td')[8].text
        r=tds.find_elements_by_tag_name('td')[9].text
        rbi=tds.find_elements_by_tag_name('td')[10].text
        bb=tds.find_elements_by_tag_name('td')[11].text
        k=tds.find_elements_by_tag_name('td')[12].text
        sb=tds.find_elements_by_tag_name('td')[13].text
        babip=tds.find_elements_by_tag_name('td')[14].text
        avg=tds.find_elements_by_tag_name('td')[15].text
        obp=tds.find_elements_by_tag_name('td')[16].text
        slg=tds.find_elements_by_tag_name('td')[17].text
        ops=tds.find_elements_by_tag_name('td')[18].text
        woba=tds.find_elements_by_tag_name('td')[19].text
        war=tds.find_elements_by_tag_name('td')[20].text
        stats.append(Data(name, team, oppositeTeam, 경기, pa, ab, h, hr, r, rbi, bb, k, sb, babip, avg, obp, slg, ops, woba, war))
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
            getPageURL= 'http://www.kbreport.com/leader/main?rows=20&order=oWAR&orderType=DESC&teamId='+teamId+'&defense_no=&year_from='+startYear+'&year_to='+endYear+'&gameType='+gameType+'&split01=opposite&split02_1=' + oppositeTeamId + '&split02_2=&r_tpa_count=&tpa_count=0'
            # 페이지 수
            pages = getPage(getPageURL)

            for page in pages:
                # 크롤링할 URL
                URL = 'http://www.kbreport.com/leader/main?rows=20&order=oWAR&orderType=DESC&teamId='+teamId+'&defense_no=&year_from='+startYear+'&year_to='+endYear+'&gameType='+gameType+'&split01=opposite&split02_1=' + oppositeTeamId +\
                      '&split02_2=&r_tpa_count=&tpa_count=0#/'+ page

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
    경기=[]
    pa=[]
    ab=[]
    h=[]
    hr=[]
    r=[]
    rbi=[]
    bb=[]
    k=[]
    sb=[]
    babip=[]
    avg=[]
    obp=[]
    slg=[]
    ops=[]
    woba=[]
    war =[]

    for a in statList:
        name.append(a.getName())
        team.append(a.getTeam())
        oppositeTeam.append(a.getOppositeTeam())
        경기.append(a.get경기())
        pa.append(a.getPa())
        ab.append(a.getAb())
        h.append(a.getH())
        hr.append(a.getHr())
        r.append(a.getR())
        rbi.append((a.getRbi()))
        bb.append(a.getBb())
        k.append(a.getK())
        sb.append(a.getSb())
        babip.append(a.getBabip())
        avg.append(a.getAvg())
        obp.append(a.getObp())
        slg.append(a.getSlg())
        ops.append(a.getOps())
        woba.append(a.getWoba())
        war.append(a.getWar())

    df={
        'name' : name,
        'team' : team,
        'oppositeTeam' : oppositeTeam,
        '경기' : 경기,
        'pa' : pa,
        'ab' : ab,
        'h' : h,
        'hr' : hr,
        'r' : r,
        'rbi' : rbi,
        'bb' : bb,
        'k' : k,
        'sb' : sb,
        'babip': babip,
        'avg' : avg,
        'obp' : obp,
        'slg' : slg,
        'ops' : ops,
        'woba' : woba,
        'war' : war }

    dataFrame=DataFrame(df)

    #csv 이름 설정
    dataFrame.to_csv('hitter_stat_DS.csv', sep=',', na_rep='NaN', mode='a')

#크롤링
saveArticle()
print("끝~~")