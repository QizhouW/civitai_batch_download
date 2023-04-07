import os, sys
import time

import requests
from single_model import dl_model
import argparse


### Debug Only
# opt = OPT()
# opt.update_tag = True
# opt.random_tag = True
# opt.skip_model = True
# opt.versions = 3

def dl_author(username, savedir, versions=1, update_tag=True, random_tag=True, skip_model=True,only_new=False):
    print('Download from author: ', username)
    url = f'https://civitai.com/api/v1/models?username={username}'
    time.sleep(0.3)
    response = requests.get(url, headers={"Content-Type": "application/json"})
    info = response.json()
    dl_count = 1
    print(f'All {info["metadata"]["totalItems"]} models found, start downloading')
    if len(info['items']) == info['metadata']['totalItems']:
        for model in info['items']:
            print(f'Model No.{dl_count}: ')
            dl_model(model['id'], savedir=savedir, versions=versions, update_tag=update_tag,
                     random_tag=random_tag, skip_model=skip_model,only_new=only_new)
            dl_count += 1
    else:
        for page in range(1, info['metadata']['pageSize'] + 1):
            if page == 1:
                for model in info['items']:
                    print(f'Model No. {dl_count}:')
                    dl_model(model['id'], savedir=savedir, versions=versions, update_tag=update_tag,
                             random_tag=random_tag, skip_model=skip_model,only_new=only_new)
                    dl_count += 1
            else:
                url = f'https://civitai.com/api/v1/models?username={username}&page={page}'
                time.sleep(0.3)
                response = requests.get(url, headers={"Content-Type": "application/json"})
                info = response.json()
                for model in info['items']:
                    print(f'Model No.{dl_count}: ')
                    dl_model(model['id'], savedir=savedir, versions=versions, update_tag=update_tag,
                             random_tag=random_tag, skip_model=skip_model,only_new=only_new)
                    dl_count += 1
    print(f'All {dl_count - 1} models downloaded')


if __name__ == '__main__':
    from utils import get_base_opt, Logger
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    sys.stdout = Logger(f'./logs/author_dl_{timestamp}.txt')

    args = get_base_opt()
    args.add_argument('-username', type=str, default='NONE')
    opt = args.parse_args()
    if opt.username == 'NONE':
        print('Please input the username')
        sys.exit(-1)
    else:
        dl_author(opt.username, opt.savedir, versions=opt.versions, update_tag=opt.update_tag,
                  random_tag=opt.random_tag, skip_model=opt.skip_model)
