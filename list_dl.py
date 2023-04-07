import os, sys
import time

import numpy as np
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
import re
import shutil
import requests
import json
from fake_useragent import UserAgent
from utils import mkdir, get_file_sha256, dl_file, init_driver, purge_dirname


def list_dl(opt):
    filename=opt.file
    old_filename=opt.old_list
    old_list=[]
    if old_filename != '':
        with open(old_filename, 'r', encoding='utf-8') as f:
            tmp = f.readlines()
            for line in tmp:
                model_id = line.strip()
                if model_id.startswith('#') or model_id == '':
                    continue
                else:
                    if model_id.startswith('https') or model_id.startswith('http') or model_id.startswith('civitai'):
                        model_id = model_id.split('/')[-2]
                    old_list.append(model_id)
        print(f'Found old list with {len(old_list)} models, will only update new models')
    id_list=[]
    with open(filename, 'r', encoding='utf-8') as f:
        tmp=f.readlines()
        for line in tmp:
            model_id = line.strip()
            if model_id.startswith('#') or model_id == '':
                continue
            else:
                if model_id.startswith('https') or model_id.startswith('http') or model_id.startswith('civitai'):
                    model_id = model_id.split('/')[-2]
                if model_id not in old_list:
                    id_list.append(model_id)
    print(f'Download from {len(id_list)} listed models')
    id_list=np.array(id_list)
    id_list=np.unique(id_list)
    for i,model_id in enumerate(id_list):
        print(f'Model No.{i+1}, {model_id}')
        dl_model(model_id, opt.savedir, versions=opt.versions, update_tag=opt.update_tag,
                         random_tag=opt.random_tag, skip_model=opt.skip_model,only_new=opt.only_new)
    return


if __name__=='__main__':
    from utils import get_base_opt, Logger
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    sys.stdout = Logger(f'./logs/list_dl_{timestamp}.txt')
    args = get_base_opt()
    args.add_argument('-file', type=str, default='./models_list.txt')
    args.add_argument('-old_list', type=str, default='')
    opt = args.parse_args()
    list_dl(opt)

