import hashlib
import os
import time
import requests
from bs4 import BeautifulSoup
import re
import shutil
import requests
import json
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def mkdir(path, rm=False):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        if rm:
            shutil.rmtree(path)
            os.mkdir(path)


def get_file_sha256(file_path):
    # 打开文件，以二进制模式读取文件内容
    with open(file_path, 'rb') as f:
        # 创建sha256对象
        sha256 = hashlib.sha256()
        while True:
            # 每次读取4096字节
            data = f.read(4096)
            if not data:
                break
            # 更新sha256对象
            sha256.update(data)
    # 获取sha256哈希值并返回
    return sha256.hexdigest()


def dl_file(url,dl_dir,filepath=None):
    with requests.get(url, stream=True) as r:
        if filepath is None:
            try:
                filepath = os.path.join(dl_dir, r.headers['Content-Disposition'].split('"')[1])
            except:
                print('Can not find the filename on internet, use the last part of url instead')
                filepath = os.path.join(dl_dir, url.split('/')[-1])
        with open(filepath, 'wb') as f:
            # for chunk in r.iter_content(chunk_size=8192):
            # f.write(chunk)
            shutil.copyfileobj(r.raw, f)


def init_driver():
    url='https://civitai.com'
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
    time.sleep((1))
    driver.get(url)
    time.sleep((2))
    with open(os.path.join('src','cookies.json'), 'r') as f:
        cookies = json.load(f)
    for item in cookies:
        cookie = {'name': item['name'], 'value': item['value']}
        driver.add_cookie(cookie)
    time.sleep((2))
    driver.get(url)
    c = driver.get_cookies()
    # uptate cookies for next time
    with open(os.path.join('src','cookies.json'), 'w') as f:
        json.dump(c, f)
    time.sleep((2.2))
    return driver

