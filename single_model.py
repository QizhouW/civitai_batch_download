import os
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
from utils import mkdir, get_file_sha256, dl_file, init_driver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np
import random
import shutil
# driver=init_driver()
##


def dl_model(model_id, savedir='./dl'):
    #model_id = 12597
    #savedir = './dl'
    response = requests.get(f"https://civitai.com/api/v1/models/{model_id}", headers={"Content-Type": "application/json"})
    info = response.json()
    name = info['name'].strip()
    creator = info['creator']['username'].strip()
    illegal_str = [r'\/', r'\:', r'\*', r'\?', r'\"', r'\<', r'\>', r'\|', ' ']
    for ill_s in illegal_str:
        # re.compile()
        name = re.sub(ill_s, '_', name)

    dl_dir = os.path.join(savedir,info['type'], name + '_' + creator)
    mkdir(dl_dir)
    mkdir(os.path.join(dl_dir, 'tags'))
    model_latest = info['modelVersions'][0]
    metadata = {
        "Name": name,
        "Creator": creator,
        'Type': info['type'],
        'Version': model_latest['name'],
        'Trigger Words': model_latest['trainedWords'],
        "Link": model_latest['files'][0]['downloadUrl'],
        "Description": BeautifulSoup(info['description'], 'html.parser').get_text(),
        'Last Update': model_latest['updatedAt'],
        'Base Model': model_latest['baseModel'],
        "Size": model_latest['files'][0]['sizeKB'] / 1024,
        'Filename': model_latest['files'][0]['name'],
        "Download_url": f'https://civitai.com/models/{model_id}/',
        "SHA256": model_latest['files'][0]['hashes']['SHA256'][:8],
    }

    with open(os.path.join(dl_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    gallery = model_latest['images']
    with_tag_ls = []
    no_tag_ls=[]
    for g in gallery:
        if g['meta'] is not None:
            with_tag_ls.append(g)
        else:
            no_tag_ls.append(g)
    random.shuffle(with_tag_ls)
    random.shuffle(no_tag_ls)
    residual_tag_num= 5-np.min([len(with_tag_ls),5])
    for tag_idx,g in enumerate(with_tag_ls):
        with requests.get(g['url'], stream=True) as r:
            dl_head = r.headers
            filename = os.path.join(dl_dir, 'tags', f'tag{tag_idx}.png')
            r.raise_for_status()
            with open(filename, 'wb') as f:
                # for chunk in r.iter_content(chunk_size=8192):
                # f.write(chunk)
                shutil.copyfileobj(r.raw, f)
            if tag_idx==4:
                break

        with open(os.path.join(dl_dir, 'tags', f'tag{tag_idx}.txt'), 'w', encoding='utf-8') as f:
            msg = ''
            msg += g['meta']['prompt'] + '\n'
            msg += 'Negative prompt: ' + g['meta']['negativePrompt'] + '\n'
            for key in ['Size', 'seed', 'Model', 'steps', 'sampler', 'cfgScale',
                        'Model hash']:
                msg += key + ': ' + str(g['meta'][key]) + ',  '
            f.write(msg)


    for tag_idx in range(residual_tag_num):
        with requests.get(g['url'], stream=True) as r:
            dl_head = r.headers
            filename = os.path.join(dl_dir, 'tags', f'tag{tag_idx+len(with_tag_ls)}.png')
            r.raise_for_status()
            with open(filename, 'wb') as f:
                # for chunk in r.iter_content(chunk_size=8192):
                # f.write(chunk)
                shutil.copyfileobj(r.raw, f)

    shutil.copyfile(os.path.join(dl_dir, 'tags','tag0.png'), os.path.join(dl_dir,'cover.png'))

    with requests.get(metadata['Download_url'], stream=True) as r:
        filename = os.path.join(dl_dir, metadata['Filename'])
        if os.path.exists(filename):
            existing_hash = get_file_sha256(filename)
            if existing_hash == metadata['SHA256']:
                print(f'File {filename} already exists')
                exit()
            else:
                print(f'Update Model {filename}, size {metadata["Size"]} MB')
        else:
            print(f'Download Model {filename}, size {metadata["Size"]} MB')
        r.raise_for_status()
        with open(filename, 'wb') as f:
            # for chunk in r.iter_content(chunk_size=8192):
            # f.write(chunk)
            shutil.copyfileobj(r.raw, f)
        return


if __name__ == '__main__':
    dl_model(12597, savedir='./dl')
