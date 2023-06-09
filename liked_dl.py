import os, sys
import time
import requests
from single_model import dl_model
import argparse
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import shutil
import requests
import json
from fake_useragent import UserAgent
from utils import mkdir, get_file_sha256, dl_file, init_driver, purge_dirname
from list_dl import list_dl

ID_MODEL='mantine-l4k5uh'


def parse_from_soup(soup):
    anchors = soup.select('.' + ID_MODEL)
    links = []
    for l in anchors:
        try:
            model_id = l.get('href').split('/')[2]
            links.append(model_id)
        except:
            continue
    print('Found {} favorite models'.format(len(links)))
    return links


def get_liked_ls(driver):
    driver.get('https://civitai.com/?favorites=true')
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return parse_from_soup(soup)

def write_liked_ls(links, filename='liked_ls.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('## Model IDs in my favorite list:\n')
        for l in links:
            f.write(l+'\n')
    return


if __name__ =='__main__':
    from utils import get_base_opt, Logger
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    sys.stdout = Logger(f'./logs/liked_dl_{timestamp}.txt')
    args = get_base_opt()
    args.add_argument('-file', type=str, default='./liked_list.txt')
    args.add_argument('-old_list', type=str, default='./liked_list_latest.txt')
    args.add_argument('-cookie', type=str, default='./src/cookies.json')
    opt = args.parse_args()
    driver = init_driver(opt.cookie)
    time.sleep(3)
    links1 = get_liked_ls(driver)
    #driver.quit()
    #write_liked_ls(links, filename=opt.file)

    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links2 = parse_from_soup(soup)
    links=links1+links2
    links=np.unique(links)
    #write_liked_ls(links, filename=opt.file)

    #list_dl(opt)
    #os.remove(f'./liked_list_latest.txt')
    #os.rename(opt.file, f'./liked_list_latest.txt')


    #list_dl(opt)


