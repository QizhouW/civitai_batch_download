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


