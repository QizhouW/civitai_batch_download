import os, sys
import requests
from single_model import dl_model
import argparse
from author_dl import dl_author
import numpy as np
if __name__ == '__main__':
    from utils import get_base_opt
    args = get_base_opt()
    args.add_argument('-file', type=str, default='./author_data.txt')
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
    author_list=np.array(author_list)
    author_list=np.unique(author_list)
    print('Download from listed authors')

    for username in author_list:
        dl_author(username, opt.savedir, versions=opt.versions, update_tag=opt.update_tag,
                         random_tag=opt.random_tag, skip_model=opt.skip_model,only_new=opt.only_new)