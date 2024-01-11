import requests as req
import time
from bs4 import BeautifulSoup as bs
import pandas as pd

res = req.get("https://search.daum.net/search?nil_suggest=btn&w=news&DA=STC&cluster=y&q=속보&p=1&sort=recency")
soup = bs(res.text, "lxml")

publication = bs.select(soup, "strong.tit_item > span.txt_info")
title = bs.select(soup, "strong.tit-g.clamp-g")

url = bs.select(soup, "strong.tit-g.clamp-g > a")

publicationList = []
urlList = []
titleList = []
bylineList = []
timeList = []
articleList = []

for i in range(len(url)) :
    newsreq = req.get(url[i]["href"])
    newssoup = bs(newsreq.text, "lxml")
    byline = bs.select(newssoup, "div.info_view > span:nth-child(1)") 
    time = bs.select(newssoup, "div.info_view > span > span")
    temp = bs.select(newssoup, "div.article_view > section > p") 
    article = ""
    
    for j in range(len(temp)) :
        article += temp[j].text
        
    publicationList.append(publication[i].text)
    urlList.append(url[i]["href"])
    titleList.append(title[i].text)
    bylineList.append(byline[0].text)
    timeList.append(time[0].text)
    articleList.append(article)

#len(titleList), len(publicationList), len(bylineList), len(timeList), len(articleList), len(urlList)

data = {"뉴스제목" : titleList, "신문사" : publicationList, "기자" : bylineList, "입력시간" : timeList, "뉴스기사" : articleList, "url" : urlList}
breaking = pd.DataFrame(data)
breaking.to_csv("data.csv", encoding = "euc-kr")
