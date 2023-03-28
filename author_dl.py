import os, sys
import requests
from single_model import dl_model
import argparse


### Debug Only
# opt = OPT()
# opt.update_tag = True
# opt.random_tag = True
# opt.skip_model = True
# opt.versions = 3

def dl_author(username, savedir, versions=1, update_tag=True, random_tag=True, skip_model=True):
    print('Download from author: ', username)
    url = f'https://civitai.com/api/v1/models?username={username}'
    response = requests.get(url, headers={"Content-Type": "application/json"})
    info = response.json()

    dl_count = 1
    print(f'All {info["metadata"]["totalItems"]} models found, start downloading')
    if len(info['items']) == info['metadata']['totalItems']:
        for model in info['items']:
            print(f'Model {dl_count}: ', model['name'])
            dl_model(model['id'], savedir=savedir, versions_num=versions, update_tag=update_tag,
                     random_tag=random_tag, skip_model=skip_model)
            dl_count += 1
    else:
        for page in range(1, info['metadata']['pageSize'] + 1):
            if page == 1:
                for model in info['items']:
                    print(f'Model {dl_count}: ', model['name'])
                    dl_model(model['id'], savedir=savedir, versions_num=versions, update_tag=update_tag,
                             random_tag=random_tag, skip_model=skip_model)
                    dl_count += 1
            else:
                url = f'https://civitai.com/api/v1/models?username={username}&page={page}'
                response = requests.get(url, headers={"Content-Type": "application/json"})
                info = response.json()
                for model in info['items']:
                    print(f'Model {dl_count}: ', model['name'])
                    dl_model(model['id'], savedir=savedir, versions_num=versions, update_tag=update_tag,
                             random_tag=random_tag, skip_model=skip_model)
                    dl_count += 1
    print(f'All {dl_count - 1} models downloaded')


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-username', type=str, default='NONE')
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
        dl_author(opt.username, opt.savedir, versions=opt.versions, update_tag=opt.update_tag,
                  random_tag=opt.random_tag, skip_model=opt.skip_model)
