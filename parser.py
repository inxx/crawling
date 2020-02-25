import requests
from bs4 import BeautifulSoup
import json
import os

## python 파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

## HTTP GET Request
req = requests.get('https://www.ssgdfm.com/shop/dqDisplay/productCategoryMain?dispCtgrId=00010101&cateDepth=3&dispCtgrName=%EC%8A%A4%ED%82%A8%C2%B7%ED%86%A0%EB%84%88')


## HTML 소스 가져오기
html = req.text

## BeautifulSoup으로 html > python변환
## 첫 인자는 html 소스, 두 번째 인자는 어떤 parser를 이용할지 명시.
## 이 글에서는 python 내장 html.parser 이용
soup = BeautifulSoup(html, 'html.parser')

## css selector로 html 요소 찾기
my_titles = soup.select(
    '#productResultArea > li > div > a'
)

## my_titles는 bs의 list 객체
data = {}

for title in my_titles:
    ##태그 안에 텍스트 가져오기
    #print(title.get('title'))
    ## tag의 속성을 가져오기(ex: href속성)
    price_usd = title.find_all('span', class_='us-currency')
    price_krw = title.find_all('span', class_='nation-currency')
    #print(price_usd[0].text + price_krw[0].text)
    data[title.get('title')] = price_usd[0].text + price_krw[0].text

with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    json.dump(data, json_file)

## HTTP Header 가져오기
header = req.headers

## HTTP Status 가져오기 (200: 정상)
status = req.status_code

## HTTP가 정상적으로 되었는지 (True/False)
is_ok = req.ok
