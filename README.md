# civitai_batch_download
Download civitai models in one line. / C站模型批量下载工具

注意，C站服务器最近不稳定，因此我手动添加了延时以防止请求频率过高被拒绝/服务器负载过高     
如果发现网络不稳定，建议继续降低请求频率以保护网站，show some respect。


## 使用例：

1. 单个模型下载：
```python
python single_model.py -id 8505 -update_tag -random_tag -versions=1
```

2. 批量下载同一作者所有作品
```python
python author_dl.py -update_tag -random_tag -username=Cy1zu_
```
3. 批量下载一批作者所有作品
首先把作者的链接集合在author_data.txt 中，格式如示例文件
```python
python author_list_dl.py -update_tag -random_tag -file=author_data.txt
```
4. 批量下载一批保存的模型ID
格式如示例文件 models_list.txt
```python
python list_dl.py -update_tag -random_tag -file=models_list.txt
```
5. 批量下载自己收藏的所有模型

首先你需要用你的账号登陆CIVITAI, 并手动保存cookie，否则脚本无法获取你的账户收藏夹，使用 -cookie 参数指定cookie文件位置
```python
python liked_dl.py -update_tag -random_tag -file=liked_list.txt -cookie=cookie.json
```
**参数解释：**
- update_tag ：更新tag，建议仅在初次下载时使用，有些作者有些时候会撤掉自己的tag，防止更新丢失，默认=False
- random_tag ：随机选取tag图，默认=False 
- skip_model ：跳过模型检查和下载，仅更新tag， 默认=False
- versions ：需要下载的版本数量，从新到旧，默认=1
- savedir ：保存文件夹，默认=./dl/
- id, username，file ：分别对应于上述三种下载方式，详见示例命令。
- cookie ：保存的cookie文件位置，用于下载自己收藏的模型 
