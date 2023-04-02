import os,sys
import time
from bs4 import BeautifulSoup
import requests
import json
from utils import mkdir, get_file_sha256, dl_file, init_driver, purge_dirname
import numpy as np
import random
import shutil
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import argparse


def retry_wrapper(func):
    def wrapper(*args, **kwargs):
        count = 0
        while count < 5:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                count += 1
                print(f"Error: {e}. Retrying ({count}/10)...")
        print("Max retries exceeded. Exiting.")
    return wrapper

@retry_wrapper
def dl_model(model_id, savedir='./dl', versions=1, update_tag=True, random_tag=False, skip_model=False):
    time.sleep(0.5)
    # respect the api provides, do not request too fast
    response = requests.get(f"https://civitai.com/api/v1/models/{model_id}",
                            headers={"Content-Type": "application/json"})
    info = response.json()
    name = info['name']
    creator = info['creator']['username'].strip()
    name = purge_dirname(name)
    dl_count = 0
    for chosen_model in info['modelVersions']:
        if dl_count == versions and not skip_model:
            break
        dl_dir = os.path.join(savedir, info['type'], creator + '-' + name, purge_dirname(chosen_model['name']))

        mkdir(dl_dir)
        mkdir(os.path.join(dl_dir, 'imgs'))
        mkdir(os.path.join(dl_dir, 'model'))
        metadata = {
            "Name": name,
            "Creator": creator,
            'Type': info['type'],
            'Version': chosen_model['name'],
            'Trigger Words': chosen_model['trainedWords'],
            "Link": f'https://civitai.com/models/{model_id}/',
            "Description": BeautifulSoup(info['description'], 'html.parser').get_text(),
            'Last Update': chosen_model['updatedAt'],
            'Base Model': chosen_model['baseModel'],
            "Size": np.round(chosen_model['files'][0]['sizeKB'] / 1024, 2),
            'Filename': chosen_model['files'][0]['name'],
            "Download_url": chosen_model['files'][0]['downloadUrl'],
        }
        try:
            metadata['SHA256'] = chosen_model['files'][0]['hashes']['SHA256']
        except:
            pass


        if not skip_model:
            time.sleep(0.5)
            with requests.get(metadata['Download_url'], stream=True) as r:
                filename = os.path.join(dl_dir, 'model',metadata['Filename'])
                if 'SHA256' not in metadata.keys():
                    print(f'No SHA256 for {name}, download anyway')
                    flag = True
                elif os.path.exists(filename):
                    existing_hash = get_file_sha256(filename)
                    if existing_hash.capitalize() == metadata['SHA256'].capitalize():
                        print(f'File {metadata["Filename"]} already exists')
                        if not update_tag:
                            dl_count += 1
                            continue
                        else:
                            print(f'Update Tag of {name}: {chosen_model["name"]}')
                            flag = False
                    else:
                        print(f'Update Model {filename}, size {metadata["Size"]} MB')
                        flag = True
                else:
                    print(f'Download Model {filename}, size {metadata["Size"]} MB')
                    flag = True
                if flag:
                    r.raise_for_status()
                    with open(filename, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
        else:
            print(f'Update Tag of {name}: {chosen_model["name"]}')

        with open(os.path.join(dl_dir, 'model', 'intro.json'), 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)

        with open(os.path.join(dl_dir,'model', 'metadata.json'), 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=4, ensure_ascii=False)

        if update_tag:
            gallery = chosen_model['images']
            with_tag_ls = []
            no_tag_ls = []
            for g in gallery:
                if g['meta'] is not None:
                    with_tag_ls.append(g)
                else:
                    no_tag_ls.append(g)

            if random_tag:
                random.shuffle(with_tag_ls)
                random.shuffle(no_tag_ls)

            residual_tag_num = np.min([len(no_tag_ls), 5 - np.min([len(with_tag_ls), 5])])

            for tag_idx, g in enumerate(with_tag_ls):
                time.sleep(0.2)
                with requests.get(g['url'], stream=True) as r:
                    imgname = os.path.join(dl_dir, 'imgs', f'tag{tag_idx}.png')
                    r.raise_for_status()
                    if os.path.exists(imgname):
                        os.remove(imgname)
                    with open(imgname, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                    if tag_idx == 4:
                        break

                msg = ''
                msg += g['meta']['prompt'] + '\n'
                try:
                    msg += 'Negative prompt: ' + g['meta']['negativePrompt'] + '\n'
                except:
                    print('No negative prompt')
                for key in ['Size', 'seed', 'Model', 'steps', 'sampler', 'cfgScale',
                            'Model hash']:
                    try:
                        msg += key + ': ' + str(g['meta'][key]) + ',  '
                    except:
                        # print('this tag is missing:', key)
                        pass
                image = Image.open(imgname)
                png_info = PngInfo()
                png_info.add_text('parameters', msg)
                image.save(imgname, pnginfo=png_info)

            for tag_idx in range(residual_tag_num):
                time.sleep(0.2)
                with requests.get(g['url'], stream=True) as r:
                    filename = os.path.join(dl_dir, 'imgs', f'tag{tag_idx + len(with_tag_ls)}.png')
                    r.raise_for_status()
                    with open(filename, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)

            shutil.copyfile(os.path.join(dl_dir, 'imgs', 'tag0.png'), os.path.join(dl_dir, f'{metadata["Filename"][:-12]}.png'))
            dl_count += 1

    return


if __name__ == '__main__':
    from utils import get_base_opt, Logger

    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    sys.stdout = Logger(f'./logs/single_dl_{timestamp}.txt')
    args = get_base_opt()
    args.add_argument('-id', type=int, default=-1)
    opt = args.parse_args()
    if opt.id == -1:
        print('Please specify the model id')
        exit(-1)
    dl_model(opt.id, savedir=opt.savedir,versions=opt.versions, update_tag=opt.update_tag,
              random_tag=opt.random_tag, skip_model=opt.skip_model)
