# -*- coding: UTF-8 -*-
import json
import re

import os
from hashlib import md5

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from urllib.parse import urlencode
import pymysql
from multiprocessing import Pool
from config import *


# 1.根据关键字获得索引页信息
def get_page_index(offset, keyword):
    data = {
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'format': 'json',
        'keyword': keyword,
        'offset': offset,
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错！')
        return None


# 2.根据索引页信息，拿到文章地址列表
def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


# 3.拿到文章地址后，根据文章地址获得文章详细信息
def get_page_detail(url):
    try:
        if url:
            url = 'https://www.toutiao.com/a' + url[25:]
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            return None
    except RequestException:
        print('请求详情页出错！', url)
        return None

# 4.从文章信息中提取标题和图片信息
def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.select('title')
    if titles:
        title = soup.select('title')[0].get_text()
    else:
        title = ''
    # re.S 换行匹配
    images_pattern = re.compile('http://p5a.pstatp.com/large/([\w]+)&quot;', re.S)
    # result = re.search(images_pattern, html)
    result = re.findall(images_pattern, html)
    # if data and 'sub_images' in data.keys():
    #     sub_images = data.get('sub_images')
    #     images = [item.get('url') for item in sub_images]
    for i in range(len(result)):
        result[i] = 'http://p5a.pstatp.com/large/' + result[i]
    images = result
    for image in images:
        download_image(image)
    return {
        'title': title,
        'url': url,
        'images': images
    }

# 5.保存图片到数据库
def save_to_postgres(result):
    conn = pymysql.connect(database='reptile', user='root', password='root', host='localhost', port=3306)
    cur = conn.cursor()
    if result.get('images') and result.get('images')[0] and result.get('title') and result.get('url'):
        images = ','.join(result.get('images'))
        cur.execute("insert into toutiao (title, url, images) values ('%s', '%s', '%s');" % (result.get('title'), result.get('url'), images))
        # cur.execute("select * from toutiao")
        # rows = cur.fetchall()
        # print(rows)
        conn.commit()
        cur.close()
        conn.close()

# 下载图片
def download_image(url):
    try:
        print('正在下载：', url)
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('下载图片出错！', url)
        return None

# 保存图片到本地
def save_image(content):
    # file_path_name = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    file_path_name = '{0}/{1}.{2}'.format('D:\\Reptile', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path_name):
        with open(file_path_name, 'wb') as f:
            f.write(content)
            f.close()

# 主函数
def main(offset):
    html = get_page_index(offset, KEYWORD)
    if html:
        for url in parse_page_index(html):
            html = get_page_detail(url)
            print(html)
            if html:
                result = parse_page_detail(html, url)
                save_to_postgres(result)


if __name__ == '__main__':
    # main()
    groups = [x*20 for x in range(GROUP_START, GROUP_END+1)]
    pool = Pool(4)
    pool.map(main, groups)