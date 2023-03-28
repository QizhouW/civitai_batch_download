import os, sys
import requests
from single_model import dl_model
import argparse
from author_dl import dl_author

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-file', type=str, default='author_data.txt')
    args.add_argument('-update_tag', action='store_true')
    args.add_argument('-random_tag', action='store_true')
    args.add_argument('-skip_model', action='store_true')
    args.add_argument('-versions', type=int, default=1)
    args.add_argument('-savedir', type=str, default='./dl')
    opt = args.parse_args()
    author_list=[]
    with open(opt.file, 'r', encoding='utf-8') as f:
        tmp=f.readlines()
        for line in tmp:
            username = line.strip()
            if username.startswith('#') or username == '':
                continue
            else:
                username = username.split('/')[-1]
                author_list.append(username)
    print('Download from authors',author_list)

    for username in author_list:
        dl_author(username, opt.savedir, versions=opt.versions, update_tag=opt.update_tag,
                         random_tag=opt.random_tag, skip_model=opt.skip_model)