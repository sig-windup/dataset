import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

path = "C:\\Users\\iris8\\OneDrive\\바탕 화면\\chromedriver.exe"
f = open("schedule.csv", "w")
driver = webdriver.Chrome(path)
driver.get("https://www.naver.com/")

element = driver.find_element_by_name("query")
element.send_keys("2021년 4월 3일 야구 경기일정")
element.submit()



for _ in range(145) :
    html = driver.page_source
    soup = bs(html, "html.parser")
    date = soup.select('div.nv_date > strong')
    team_lft = soup.select('table > tbody > tr > td.l_team > span > a')
    team_rgt = soup.select('table > tbody > tr > td.r_team > span > a')

    dates = []
    team_lfts = []
    team_rgts = []
    result = []

    for i in date:
        a = i.text.strip()
        dates.append(a)

    for i in team_lft:
        a = i.text.strip()
        team_lfts.append(a)

    for i in team_rgt:
        a = i.text.strip()
        team_rgts.append(a)


    for i in range(len(team_lfts)):
        f.write(dates[0] + "," + team_lfts[i] + "," + team_rgts[i] + '\n')

    driver.find_element_by_xpath('//*[@id="main_pack"]/section[1]/div/div[2]/div[2]/div[1]/a[2]').send_keys(Keys.ENTER)