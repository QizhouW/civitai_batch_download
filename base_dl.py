import os
import requests
from bs4 import BeautifulSoup
import re
import shutil
import requests
import json
import time
import sys
import argparse


def mkdir(path, rm=False):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        if rm:
            shutil.rmtree(path)
            os.mkdir(path)


cookies = {
    '__stripe_mid': '1fe09fa5-502c-48ee-b58a-99a2b731d757f97286',
    'f_period': 'Day',
    'f_sort': 'Most%20Liked',
    '__Secure-next-auth.callback-url': 'https%3A%2F%2Fcivitai.com',
    '__Host-next-auth.csrf-token': 'd2074cb6dac098eaf78897c2a7db2035f4540a307eabb2cd9edc4355925245fc%7C2f3f0646877a1c71195f9756581e8035b714d5508a0bc0f077fc61e1b6e99c2f',
    '__stripe_sid': '9f102a67-cfb3-4943-92b1-c80a81b58c618985fa',
    '__Secure-civitai-token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..HSXwP625QH7flO7Y.4JIVR6cB437_gFapCmEN0EsJqafFpnlEjNrhymhsqeTUyH1asR2D_aaWLhv-Giba7s2KtVWGo32H54YaKPqe0bfJAgifwI5coGzIJIqJnZhG8zjS-U5N63ZepEKjVPzJQzs2gNXZb3M0jkqvdsjM3CvIWXFBG9F83opn3PYkFV9Nb-BD-IVhOdSfLk9UvjhytCKcRnRT_l22lBLYYVpqGmmF8xP3XlQ-lmQfOa7gsIRnoriCu4rh4rOAB8cxDeSVZ81RE4zPzr5bSgA6aHQo7FL9cZUMqBvFAdWbgR2JKZbLkk3R7U8XeGmLni6BuYEjX2fge5cXEqHzux9pV67wXk6Yqr95qtxsQXhb7RRuSZXbrrYrghDajLAXN52J5P-xXTUrQ3UiS_I1kuJQSHffoj5t4uClr6T_0oMxsVnir0RXgIKVWz450RhlnxU2arUVkcUzrjNXPIoUlXsdngzOx_jUIjxmIskOfKESXlDAYfS6_XoBea_hi9ZWixdib65C3XqnGqcuV8G0Wv1kWJpz-ymfcks4c2hRMwpn7bhl_GBCM7H-sBdeDM2X4Bhv6yM0vO0Csbd59rgDf4IQZZb5Oqd6BjdoXOLNlqbUDgFIL8oK3xaVeqrrSgN90qqDixYk8GgQgCrPalHAQmmVBL1Etuhfa91W3zcs_ft0r9LKAfw8XgcS6GDZQgIR3PjHFIrh0OypInWbtGVc3sY1_kEK0jIAnXwzuin5_4bp4ggbRqVwx5k24gQReDjrk4Hc7s_mBsDq7FgmAwqoXqXkkbgwH1UsDQdXac1pKmf1DqHYg021wJfzwNSW5jTkZPNs4B_FTedFsEDrLaepnSlRzK0fjvnt8s-1JXjmsXGtZeWdqprl8_lCXHZvQJ_XZCQN-3GesN4hEF-Ktk1tK4As7CkJrmSVaoQfNkJd20hp-ONCZ6wpZhc-cWSdey73EXzi1t4xbDGIiE7N6j_cEKvuteZLXj3d-Nh4LzjMGW7XNQ.Uqzcg1x3Eu08qMlrSc5hxg',
}

headers = {
    'authority': 'civitai.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': '__stripe_mid=1fe09fa5-502c-48ee-b58a-99a2b731d757f97286; f_period=Day; f_sort=Most%20Liked; __Secure-next-auth.callback-url=https%3A%2F%2Fcivitai.com; __Host-next-auth.csrf-token=d2074cb6dac098eaf78897c2a7db2035f4540a307eabb2cd9edc4355925245fc%7C2f3f0646877a1c71195f9756581e8035b714d5508a0bc0f077fc61e1b6e99c2f; __stripe_sid=9f102a67-cfb3-4943-92b1-c80a81b58c618985fa; __Secure-civitai-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..HSXwP625QH7flO7Y.4JIVR6cB437_gFapCmEN0EsJqafFpnlEjNrhymhsqeTUyH1asR2D_aaWLhv-Giba7s2KtVWGo32H54YaKPqe0bfJAgifwI5coGzIJIqJnZhG8zjS-U5N63ZepEKjVPzJQzs2gNXZb3M0jkqvdsjM3CvIWXFBG9F83opn3PYkFV9Nb-BD-IVhOdSfLk9UvjhytCKcRnRT_l22lBLYYVpqGmmF8xP3XlQ-lmQfOa7gsIRnoriCu4rh4rOAB8cxDeSVZ81RE4zPzr5bSgA6aHQo7FL9cZUMqBvFAdWbgR2JKZbLkk3R7U8XeGmLni6BuYEjX2fge5cXEqHzux9pV67wXk6Yqr95qtxsQXhb7RRuSZXbrrYrghDajLAXN52J5P-xXTUrQ3UiS_I1kuJQSHffoj5t4uClr6T_0oMxsVnir0RXgIKVWz450RhlnxU2arUVkcUzrjNXPIoUlXsdngzOx_jUIjxmIskOfKESXlDAYfS6_XoBea_hi9ZWixdib65C3XqnGqcuV8G0Wv1kWJpz-ymfcks4c2hRMwpn7bhl_GBCM7H-sBdeDM2X4Bhv6yM0vO0Csbd59rgDf4IQZZb5Oqd6BjdoXOLNlqbUDgFIL8oK3xaVeqrrSgN90qqDixYk8GgQgCrPalHAQmmVBL1Etuhfa91W3zcs_ft0r9LKAfw8XgcS6GDZQgIR3PjHFIrh0OypInWbtGVc3sY1_kEK0jIAnXwzuin5_4bp4ggbRqVwx5k24gQReDjrk4Hc7s_mBsDq7FgmAwqoXqXkkbgwH1UsDQdXac1pKmf1DqHYg021wJfzwNSW5jTkZPNs4B_FTedFsEDrLaepnSlRzK0fjvnt8s-1JXjmsXGtZeWdqprl8_lCXHZvQJ_XZCQN-3GesN4hEF-Ktk1tK4As7CkJrmSVaoQfNkJd20hp-ONCZ6wpZhc-cWSdey73EXzi1t4xbDGIiE7N6j_cEKvuteZLXj3d-Nh4LzjMGW7XNQ.Uqzcg1x3Eu08qMlrSc5hxg',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}


def single_dl(url, savedir, authorname=None,dry_run=False):
    response = requests.get(
        url,
        cookies=cookies,
        headers=headers,
    )
    soup = BeautifulSoup(response.content, 'html.parser')

    name = soup.select('.mantine-1296y2v')[0].get_text()

    illegal_str = [r'\/', r'\:', r'\*', r'\?', r'\"', r'\<', r'\>', r'\|', ' ', '_{2,}']
    for ill_s in illegal_str:
        # re.compile()
        name = re.sub(ill_s, '_', name)

    if authorname:
        creator = authorname
    else:
        creator = soup.select('.mantine-1a4mp7o')[0].get('href')
        creator = re.findall('(?<=/user/).*', creator)[0]

    size = soup.select('.mantine-1pe3xtm')[0].get_text()
    size = re.findall('\(.*\)', size)[0]
    size = size[1:-1]

    description = soup.select('.mantine-c8tr4i')[0].get_text()

    md = soup.select('.mantine-1avyp1d')

    md_str = []
    for i in md:
        msg = i.get_text().strip()
        if msg.startswith('Hash'):
            md_str.append(msg[8:])
            break
        else:
            md_str.append(i.get_text().strip())

    if len(md_str) > 14:
        trigger = md_str[14]
    else:
        trigger = 'None'

    model_type = md_str[2]
    # print(name)
    ref_anchor = soup.select('.mantine-1exkstv')

    id_list = ['1exkstv', 'jqoeeu']
    unfind_flag= True
    for id in id_list:
        if unfind_flag:
            ref_anchor = soup.select(f'.mantine-{id}')
            if len(ref_anchor) != 0:
                link = ref_anchor[0].get('href')
                link= 'https://civitai.com/' + link
                unfind_flag = False
    if unfind_flag:
        print(f'Unsupported model link for {name}, please download manually')
        print(f'Link: {url}')
        return


    # print(link)
    dl_dir = os.path.join(savedir, 'Authors',creator, md_str[2].strip(), name)
    mkdir(dl_dir)

    if dry_run:
        return

    with open(os.path.join(dl_dir, 'html_data.html'), 'w', encoding='utf-8') as f:
        f.write(str(soup))

    start_time = time.time()

    with requests.get(link, stream=True) as r:
        dl_head = r.headers
        filename = os.path.join(dl_dir, dl_head['Content-Disposition'].split('"')[1])
        metadata = {
            "Name": name,
            "Creator": creator,
            'Type': model_type,
            'Downloaded': md_str[4],
            'Last Update': md_str[6],
            'Version': md_str[8],
            'Base Model': md_str[10],
            'Trigger Words': trigger,
            "Size": size,
            "Link": link,
            "Description": description,
            "URL": url,
            "Model":filename,
            "Hash":md_str[-1]
        }
        with open(os.path.join(dl_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        if os.path.exists(filename):
            print(f"File exists, skip {name}")
            return
        r.raise_for_status()
        print(f"{name}, {size}")

        with open(filename, 'wb') as f:
            # for chunk in r.iter_content(chunk_size=8192):
            # f.write(chunk)
            shutil.copyfileobj(r.raw, f)
    print(f"Download Success, ETA: {time.time() - start_time:.2f}s")
    return


def author_dl(author_file, savedir,dry_run=False):
    with open(f'./src/{author_file}.html', 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    item_ls = soup.select('.mantine-cf0b3j')
    author_name = soup.select('.mantine-rk7s3e')[0].get_text()

    info = soup.select('.mantine-2qa0ve')
    author_info = {
        'Name': author_name,
        'Rank': info[0].get_text(),
        'Uploads': info[2].get_text(),
        'Followers': info[3].get_text(),
        'Likes': info[4].get_text(),
        'Downloads': info[5].get_text(),
    }
    print('-----------------------------------------------')
    print(f'Author: {author_name}')
    print(f'All {info[2].get_text()} models, available {len(item_ls)-2} models')


    author_dir = os.path.join(savedir, 'Authors', author_name)
    mkdir(author_dir)
    with open(os.path.join(author_dir, 'author.json'), 'w', encoding='utf-8') as f:
        json.dump(author_info, f, indent=4,ensure_ascii=False)

    for item in item_ls:
        anchor = item.find('a')
        if anchor:
            try:
                url = anchor.get('href')
                single_dl(url, savedir, author_name,dry_run=dry_run)
            except Exception as e:
                print(e)
                print(f'Error on downloading {url}')
                continue


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    debug_url = 'https://civitai.com/models/20644/eula-or-realistic-genshin-lora'
    debug_author = '1'
    args.add_argument('-url', type=str, default=debug_url)
    args.add_argument('-author', type=str, default=debug_author)
    args.add_argument('-savedir', type=str, default='./dl')
    args.add_argument('--dryrun', action='store_true')
    args = args.parse_args()
    if args.author:
        author_dl(args.author, args.savedir,args.dryrun)
    elif args.url:
        single_dl(args.url, args.savedir,args.dryrun)

    # url = 'https://civitai.com/models/23440/panty-pull-or-test-sex-act-lora-117'
    # single_dl(url,'./dl')
    # url='https://civitai.com/user/Rerorerorero'
    # batch_dl('./src/cy1zu.html', savedir='./dl')
