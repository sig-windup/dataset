#선발투수 크롤링
import schedule
import time
import startingPitcherCrawling
from datetime import datetime

def startingPitcher():
    print("선발 투수")
    year = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day
    today = str(year) + str(month) + str(day)
    print(today)

    #선발투수 크롤링
    startingPitcherCrawling.saveArticle('starting_pitcher_lineup_' + str(today) + '.csv', today)
    print("선발투수 크롤링 성공")

def finalLineupCrawling():
    print("최종 라인업")
    year = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day
    today = str(year) + str(month) + str(day)
    print(today)

    #선발투수 크롤링
    startingPitcherCrawling.saveArticle('final_lineup_' + str(today) + '.csv', today)
    print("라인업 크롤링 성공")


#매일 정해진 시간에 시작

#자정에 선발투수 크롤링
schedule.every().day.at("00:00:15").do(startingPitcher)

#경기 시작 전 크롤링
#화~금 6시 반 경기 시작->6시에 크롤링
schedule.every().tuesday.at("18:00:15").do(finalLineupCrawling)
schedule.every().wednesday.at("18:00:15").do(finalLineupCrawling)
schedule.every().thursday.at("18:00:15").do(finalLineupCrawling)
schedule.every().friday.at("18:00:15").do(finalLineupCrawling)
#토 6시에 경기 시작->5시 반 크롤링
schedule.every().saturday.at("17:30:15").do(finalLineupCrawling)
#일 5시에 경기 시작->4시 반 크롤링
schedule.every().sunday.at("16:30:15").do(finalLineupCrawling)

while True:
    schedule.run_pending()
    time.sleep(1)




#3초마다 job 실행
#schedule.every(3).seconds.do(job)
#3분마다 job 실행
#schedule.every(3).minutes.do(job)
#3시간마다 job 실행
#schedule.every(3).hours.do(job)
#3일마다 job 실행
#schedule.every(3).days.do(job)
#3주마다 job 실행
#schedule.every(3).weeks.do(job)
#매분 일정한 초에 시작
#schedule.every().minute.at(":23").do(job)
#매시간 일정한 분에 시작
#schedule.every().hour.at(":42").do(job)
#일정한 시간 시작
#schedule.every(5).hours.at("20:30").do(job)
#주중 특정일에 시작
#schedule.every().monday.at("12:15").do(job)



