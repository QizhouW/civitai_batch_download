import hashlib
import os,sys
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
import argparse
import io



class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)

    def flush(self):
        pass




def mkdir(path, rm=False):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        if rm:
            shutil.rmtree(path)
            os.mkdir(path)


def get_base_opt():
    args = argparse.ArgumentParser()
    args.add_argument('-update_tag', action='store_true')
    args.add_argument('-random_tag', action='store_true')
    args.add_argument('-skip_model', action='store_true')
    args.add_argument('-versions', type=int, default=1)
    args.add_argument('-savedir', type=str, default='../dl')
    return args


def purge_dirname(name):
    name=name.strip()
    illegal_str = [r'\/', r'\:', r'\*', r'\?', r'\"', r'\<', r'\>', r'\|', ' ']
    for ill_s in illegal_str:
        # re.compile()
        name = re.sub(ill_s, '_', name)
    return name

def read_chunks(file, size=io.DEFAULT_BUFFER_SIZE):
    """Yield pieces of data from a file-like object until EOF."""
    while True:
        chunk = file.read(size)
        if not chunk:
            break
        yield chunk
def get_file_sha256(filname):
    #("Use Memory Optimized SHA256")
    blocksize=1 << 20
    h = hashlib.sha256()
    length = 0
    with open(os.path.realpath(filname), 'rb') as f:
        for block in read_chunks(f, size=blocksize):
            length += len(block)
            h.update(block)
    hash_value =  h.hexdigest()
    return hash_value


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


def init_driver(cookie_path='./src/cookies.json'):
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
    with open(cookie_path, 'r') as f:
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