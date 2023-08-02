import json
import urllib.request
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def get_search_result(client_id, client_secret, url):
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
    #print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)

    return response_body.decode('utf-8')

# 크롬드라이버 셋팅
def set_chrome_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    options.binary_location="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def get_contents_from_url(url):
    #크롬 드라이버 초기화
    driver = set_chrome_driver()
    driver.get(url) # 웹사이트 접속
    time.sleep(3)
    driver.switch_to.frame('mainFrame')

    contents = ''
    try:
        a = driver.find_element(By.CSS_SELECTOR,'div.se-main-container').text
        contents = a.replace('\n', " ")
    finally:
        driver.quit()
    
    return contents
 


# Naver Open API application ID, Secret
client_id = "D7LmDEYrMic2YRpskwt1" # 발급받은 id 입력
client_secret = "th6PYwzWnU" # 발급받은 secret 입력 

# 정보입력
quote = input("검색어 입력: ") #검색어 입력받기
encText = urllib.parse.quote(quote)
display_num = input("검색 출력결과 갯수를 적어주세요.(최대100, 숫자만 입력): ") #출력할 갯수 입력받기
url = "https://openapi.naver.com/v1/search/blog?query=" + encText +"&display="+display_num# json 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과

# 검색결과 받아오기
"""
다음과 같은 형식의 결과를 가져옴 
{
    "lastBuildDate": "Wed, 02 Aug 2023 17:24:02 +0900",
    "total": 28221,
    "start": 1,
    "display": 10,
    "items": [
        {
            "title": "ChatGPT (인공지능 챗봇)와 <b>OpenAI</b>에 대해...",
            "link": "https://ystazo.tistory.com/1964",
            "description": "org ChatGPT - Wikipedia From Wikipedia, the free encyclopedia Artificial intelligence chatbot developed by <b>OpenAI</b> ChatGPT (Chat Generative Pre-trained Transformer[2]) is a chatbot developed by <b>OpenAI</b> and launched in November 2022. It is built on... ",
            "bloggername": "TASTORY : 타스토리!",
            "bloggerlink": "https://ystazo.tistory.com/",
            "postdate": "20230220"
        },
        ...
"""
search_result = json.loads(get_search_result(client_id, client_secret, url))


# data의 items를 순환하며 출력하기
for item in search_result['items']:
    print('--------------------------------------')
    print(get_contents_from_url(item['link']))
    print('--------------------------------------')









