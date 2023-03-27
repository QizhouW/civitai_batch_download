import os
import time
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import re
import shutil
import requests
import json
from fake_useragent import UserAgent
import pyperclip


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

# url1 = 'https://civitai.com/models/23440/panty-pull-or-test-sex-act-lora-117'

# url2='https://civitai.com/models/23885/yuri-cunnilingus'


author_file = 'liked'

with open(f'./src/{author_file}.html', 'r', encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, 'html.parser')

url2 = 'https://civitai.com/user/dpp12'

url2 = 'https://civitai.com/models/24062/lora-or-landmine-girl-fashion-or'
response = requests.get(
    url2,
    cookies=cookies,
    headers=headers,
)
soup = BeautifulSoup(response.content, 'html.parser')

frame = soup.select('.mantine-8od8ev')  # 框架

gallery = soup.select('.mantine-w0udt3')  # 图片

btn = soup.select('.mantine-xickm0')  # 18 按钮

item_ls = soup.select('.mantine-cf0b3j')

print(len(gallery))
print(len(frame))
print(len(btn))
# print(img[0].get('href'))
print(len(item_ls))

from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ua = UserAgent()
userAgent = ua.random
print(userAgent)

# 创建 ChromeOptions 对象，并设置 headless 模式
chrome_options = Options()
chrome_options.add_argument(f'user-agent={userAgent}')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('user-agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"')
driver = webdriver.Chrome(options=chrome_options)
time.sleep((2))
driver.get(url2)
time.sleep((2))
with open(os.path.join('cookies.json'), 'r') as f:
    cookies = json.load(f)
for item in cookies:
    cookie = {'name': item['name'], 'value': item['value']}
    driver.add_cookie(cookie)

time.sleep((2))
driver.get(url2)
c = driver.get_cookies()
print(c)
time.sleep((5))

# total_height = driver.execute_script("return document.body.scrollHeight")
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# time.sleep((2))


##############################################################################################

button_id = '.mantine-1d2keo9'
cp_button_id = '.mantine-192n9t8'

################### -------------------------------------------------------####################

url = 'https://civitai.com/models/24062/lora-or-landmine-girl-fashion-or'
driver.get(url)
html = driver.page_source
soup2 = BeautifulSoup(html, 'html.parser')
# b = soup2.select(button_id)
left_btn_id = '.mantine-oax1he'
cp_gen_btn_id = 'mantine-cbbdk9'
#btn = driver.find_elements(By.CLASS_NAME, 'mantine-1d2keo9')
#img_click = driver.find_elements(By.CLASS_NAME, 'mantine-1d2keo9')
gallery_id = 'mantine-w0udt3'

## selenium method of gallery
gallery_click = driver.find_elements(By.CLASS_NAME, gallery_id)
gallery_ls = []
for g in gallery_click:
    href = g.get_attribute('href')
    if href.startswith('https://civitai.com/gallery/'):
        gallery_ls.append(href)

## soup parse method of gallery
#gallery_ls=soup2.select('.'+gallery_id)
#g_url_ls=[]
#for g in gallery_ls:
#    href = g.get('href')
#    if href.startswith('https://civitai.com/gallery/'):
#        g_url_ls.append(href)


# 打开某一个gallery
driver.get(gallery_ls[0])
soup2 = BeautifulSoup(driver.page_source, 'html.parser')

# img_cache_name=‘mantine-1mslj4c
# img_cache = soup2.select('.'+img_cache_name)
# try:
#    cache_url=img_cache[0].get('src')
# except:
#    print('no cache for this image')


# 打开图片的链接
cache_url = re.findall('https://imagecache.civitai.com+?(?=\")', str(soup2))[0]
with requests.get(cache_url, stream=True) as r:
    filename = '1.png'
    with open(filename, 'wb') as f:
        # for chunk in r.iter_content(chunk_size=8192):
        # f.write(chunk)
        shutil.copyfileobj(r.raw, f)

import pyperclip

## 寻找并点击generate按钮
cp_gen_btn_id = 'mantine-cbbdk9'
cp_gen_btn = driver.find_elements(By.CLASS_NAME, cp_gen_btn_id)[0]
cp_gen_btn.click()

## 生成标签
with open('request_ver/tags1.txt', 'w', encoding='utf-8') as f:
    tag = str(pyperclip.paste())
    tag = tag.replace('\r', '')
    tag = tag.replace('\n', '')
    f.write(tag)



## 获取某一个作者主页下面所有的model
url='https://civitai.com/user/Rerorerorero'


ua = UserAgent()
userAgent = ua.random
print(userAgent)

# 创建 ChromeOptions 对象，并设置 headless 模式
chrome_options = Options()
chrome_options.add_argument(f'user-agent={userAgent}')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('user-agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"')
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
time.sleep((0.5))
driver.get(url)
time.sleep((2))
with open(os.path.join('cookies.json'), 'r') as f:
    cookies = json.load(f)
for item in cookies:
    cookie = {'name': item['name'], 'value': item['value']}
    driver.add_cookie(cookie)

time.sleep((5))


def get_model_count(tt):
    driver.get(url)
    time.sleep((tt))
    html = driver.page_source
    soup2 = BeautifulSoup(html, 'html.parser')
    frame = soup2.select('.mantine-8od8ev')  # 框架
    gallery = soup2.select('.mantine-w0udt3')  # 图片
    btn = soup2.select('.mantine-xickm0')  # 18 按钮
    item_ls2 = soup2.select('.mantine-cf0b3j')
    #print(len(gallery))
    #print(len(frame))
    #print(len(btn))
    print(len(item_ls2))
    # driver.quit()
    info = soup2.select('.mantine-2qa0ve')

    if len(info) > 5:
        author_info = {
            'Rank': info[0].get_text(),
            'Uploads': info[2].get_text(),
            'Followers': info[3].get_text(),
            'Likes': info[4].get_text(),
            'Downloads': info[5].get_text(),
        }
    elif len(info) == 5:
        author_info = {
            'Uploads': info[1].get_text(),
            'Followers': info[2].get_text(),
            'Likes': info[3].get_text(),
            'Downloads': info[4].get_text(),
        }
    else:
        author_info = {}

    c = re.findall('/models/.{15}', str(item_ls2))
    print('model count: ', len(c))
    #print(c)
    if eval(author_info['Uploads']) == len(c):
        print('model count is correct')
    #print(author_info)



