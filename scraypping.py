# -*- coding:utf-8 -*-
import traceback
import csv
from urllib.request import urlopen
import urllib.request as req
from bs4 import BeautifulSoup
import cx_Oracle
conn = cx_Oracle.connect('spring/1234@localhost:1521/xe')
print('conn.version==',conn.version)
cursor = conn.cursor()
item=()
items=[]
file = open("C:/inst/Data/s_num/_1.csv", "r", encoding="UTF-8")
rd = csv.reader(file)
print("시작")
for l in file:
#     print(line)
#   인코딩
#     u = l.replace('\n','')
    k = l.replace('\n','')
#     k = urllib.parse.quote(u,encoding='utf-8')
#     print(k)
#   데이터 전처리
    t = k.strip()
#   데이터 스크레이핑 url 연결
#     https://finance.naver.com/item/news.nhn?code=009180
#     url = "https://finance.naver.com/item/news.nhn?code={0}".format(t)
#     url = "https://finance.naver.com/news/news_search.nhn?q={0}&x=0&y=0".format(t)
    url="https://finance.naver.com/news/news_search.nhn?rcdate=&q={0}&x=10&y=17&sm=all.basic&pd=1&stDateStart=1997-01-01&stDateEnd=2019-08-29".format(t)
    res = req.urlopen(url)
#     soup1 = BeautifulSoup(res,"html.parser") # 현재가용
#     soup2 = BeautifulSoup(res,"html.parser") # 종목이름용
    soup3 = BeautifulSoup(res,"html.parser") #기사수집용

#chart_area > div.rate_info > div > p.no_today 현재가 

# #middle > div.h_company > div.wrap_company > h2 > a   주식이름 
#contentarea_left > div.newsSchResult > dl > dt:nth-child(1) > a 기사제목
# https://finance.naver.com/news/news_search.nhn?q=098660&x=0&y 기사주소
# 기사주소
#contentarea_left > div.newsSchResult > dl > dd:nth-child(2) 기사 
#기사제목
# https://finance.naver.com/news/news_search.nhn?rcdate=&q=098660&x=10&y=17&sm=all.basic&pd=1&stDateStart=1997-01-01&stDateEnd=2019-08-29


#     a_list = soup1.select("tr > td > td") # 현재가 
#     a_list = soup1.find_all("chart_area > div.rate_info > div > p.no_today") # 현재가
#     b_list = soup2.select("div > div > div > h2 > a") #종목이름
#     c_list = soup3.select("div > dl > dd > a ") # 기사
    c_2list = soup3.select("div > dl > dt > a")
#     c_3list = soup3.res.body.a
    for a in c_2list:
        href = a.attrs['href']
        text = a.string
        print(t,'기사제목')
        print('제목==',text)
        # a 에 값이 있다면 진행
        if len(a) !='0':
            if text != None:
                
#             m = urllib.parse.unquote(t,encoding='utf-8')
        # 값에 공백을 제거합니다.
                n = t.strip()
                for a1 in a:
                    text = a.string
                    item=(n,text)
                    items.append(item)
                print('items==',items)
for row in items:
    sql ="insert into a_title values(s_seq.nextval, :1, :2)"
    try:
        cursor.execute(sql,row)
#         print('cursor',cursor)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        if error.code == 955:
            print('Table already exxits')
        if error.code == 1031:
            print("Insufficient privileges - are you sure you'r using the owner account?")
        print("error번호:",error.code)
        print("메세지:",error.message)
        print("error내용:",error.context)
    else:
        sql = "select count(*) from a_title"
        cursor.execute(sql)
        count= cursor.fetchone()
        print("갯수:",count[0])
    conn.commit()
conn.close()

file.close()
