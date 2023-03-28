import os
import sys
import time
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import re
import shutil
import requests
import json
from pprint import pp
from fake_useragent import UserAgent
import pyperclip
from utils import mkdir, get_file_sha256, dl_file, init_driver, purge_dirname
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np
import random
import shutil
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from single_model import dl_model
import argparse




class OPT (object):
    pass

#opt = OPT()
#opt.update_tag = True
#opt.random_tag = True
#opt.skip_model = True
#opt.versions = 3

def dl_author(username, savedir,opt):
    url = f'https://civitai.com/api/v1/models?username={username}'
    response = requests.get(url, headers={"Content-Type": "application/json"})
    info = response.json()

    dl_count=1
    if len(info['items']) == info['metadata']['totalItems']:
        print(f'All {info["metadata"]["totalItems"]} models found, start downloading')
        for model in info['items']:
            print(f'Model {dl_count}: ', model['name'])
            dl_model(model['id'], savedir=savedir, versions_num=opt.versions, update_tag=opt.update_tag,
                     random_tag=opt.random_tag, skip_model=opt.skip_model)
            dl_count+= 1
    else:
        for page in range(1,info['metadata']['pageSize']+1):
            if page == 1:
                print(f'Found {len(info["items"])} models in page {page}, start downloading')
                for model in info['items']:
                    print(f'Model {dl_count}: ', model['name'])
                    dl_model(model['id'], savedir=savedir, versions_num=opt.versions, update_tag=opt.update_tag,
                             random_tag=opt.random_tag, skip_model=opt.skip_model)
                    dl_count += 1
            else:
                url = f'https://civitai.com/api/v1/models?username={username}&page={page}'
                response = requests.get(url, headers={"Content-Type": "application/json"})
                info = response.json()
                for model in info['items']:
                    print(f'Downloading model {dl_count}: ', model['name'])
                    dl_model(model['id'], savedir=savedir, versions_num=opt.versions, update_tag=opt.update_tag,
                             random_tag=opt.random_tag, skip_model=opt.skip_model)
                    dl_count += 1
    print(f'All {dl_count} models downloaded')


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-username', type=str,default='NONE')
    args.add_argument('-update_tag', action='store_true')
    args.add_argument('-random_tag', action='store_true')
    args.add_argument('-skip_model', action='store_true')
    args.add_argument('-versions', type=int, default=1)
    args.add_argument('-savedir', type=str, default='./dl')
    opt = args.parse_args()
    if opt.username == 'NONE':
        print('Please input the username')
        sys.exit(-1)
    else:
        dl_author(opt.username, opt.savedir, opt)

