import os
import requests
from bs4 import BeautifulSoup
import re
import shutil
import requests
import json

def mkdir(path, rm=False):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        if rm:
            shutil.rmtree(path)
            os.mkdir(path)

cookies = {
    '__stripe_mid': '1fe09fa5-502c-48ee-b58a-99a2b731d757f97286',
    'f_period': 'Day',
    'f_sort': 'Most%20Liked',
    '__Secure-next-auth.callback-url': 'https%3A%2F%2Fcivitai.com',
    '__Host-next-auth.csrf-token': 'd2074cb6dac098eaf78897c2a7db2035f4540a307eabb2cd9edc4355925245fc%7C2f3f0646877a1c71195f9756581e8035b714d5508a0bc0f077fc61e1b6e99c2f',
    '__stripe_sid': '9f102a67-cfb3-4943-92b1-c80a81b58c618985fa',
    '__Secure-civitai-token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..HSXwP625QH7flO7Y.4JIVR6cB437_gFapCmEN0EsJqafFpnlEjNrhymhsqeTUyH1asR2D_aaWLhv-Giba7s2KtVWGo32H54YaKPqe0bfJAgifwI5coGzIJIqJnZhG8zjS-U5N63ZepEKjVPzJQzs2gNXZb3M0jkqvdsjM3CvIWXFBG9F83opn3PYkFV9Nb-BD-IVhOdSfLk9UvjhytCKcRnRT_l22lBLYYVpqGmmF8xP3XlQ-lmQfOa7gsIRnoriCu4rh4rOAB8cxDeSVZ81RE4zPzr5bSgA6aHQo7FL9cZUMqBvFAdWbgR2JKZbLkk3R7U8XeGmLni6BuYEjX2fge5cXEqHzux9pV67wXk6Yqr95qtxsQXhb7RRuSZXbrrYrghDajLAXN52J5P-xXTUrQ3UiS_I1kuJQSHffoj5t4uClr6T_0oMxsVnir0RXgIKVWz450RhlnxU2arUVkcUzrjNXPIoUlXsdngzOx_jUIjxmIskOfKESXlDAYfS6_XoBea_hi9ZWixdib65C3XqnGqcuV8G0Wv1kWJpz-ymfcks4c2hRMwpn7bhl_GBCM7H-sBdeDM2X4Bhv6yM0vO0Csbd59rgDf4IQZZb5Oqd6BjdoXOLNlqbUDgFIL8oK3xaVeqrrSgN90qqDixYk8GgQgCrPalHAQmmVBL1Etuhfa91W3zcs_ft0r9LKAfw8XgcS6GDZQgIR3PjHFIrh0OypInWbtGVc3sY1_kEK0jIAnXwzuin5_4bp4ggbRqVwx5k24gQReDjrk4Hc7s_mBsDq7FgmAwqoXqXkkbgwH1UsDQdXac1pKmf1DqHYg021wJfzwNSW5jTkZPNs4B_FTedFsEDrLaepnSlRzK0fjvnt8s-1JXjmsXGtZeWdqprl8_lCXHZvQJ_XZCQN-3GesN4hEF-Ktk1tK4As7CkJrmSVaoQfNkJd20hp-ONCZ6wpZhc-cWSdey73EXzi1t4xbDGIiE7N6j_cEKvuteZLXj3d-Nh4LzjMGW7XNQ.Uqzcg1x3Eu08qMlrSc5hxg',
}

headers = {
    'authority': 'civitai.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

url1 = 'https://civitai.com/models/23440/panty-pull-or-test-sex-act-lora-117'

url2='https://civitai.com/models/12433/wintermoonmix'


response = requests.get(
    url2,
    cookies=cookies,
    headers=headers,
)

soup = BeautifulSoup(response.content, 'html.parser')

frame=soup.select('.mantine-8od8ev')  # 框架

img=soup.select('.mantine-w0udt3') # 图片

btn=soup.select('.mantine-xickm0') # 18 按钮



print(len(img))

print(len(frame))

print(len(btn))

print(img[0].get('href'))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 创建 ChromeOptions 对象，并设置 headless 模式
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('user-agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"')

driver = webdriver.Chrome(options=chrome_options)

for key, value in cookies.items():
    cookie = {'name': key, 'value': value}
    driver.add_cookie(cookie)
driver.get(url1)

print(driver.get_cookies())