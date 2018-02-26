# -*- coding: UTF-8 -*-
import json
import re

import os
from hashlib import md5

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from urllib.parse import urlencode
import psycopg2
from multiprocessing import Pool
from config import *


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


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    try:
        url = 'https://www.toutiao.com/a' + url[25:]
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错！', url)
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.select('title')
    if titles:
        title = soup.select('title')[0].get_text()
    else:
        title = ''
    print(title)
    images_pattern = re.compile('http://p3.pstatp.com/large/([\w]+)&quot;', re.S)
    # result = re.search(images_pattern, html)
    result = re.findall(images_pattern, html)
    # if data and 'sub_images' in data.keys():
    #     sub_images = data.get('sub_images')
    #     images = [item.get('url') for item in sub_images]
    for i in range(len(result)):
        result[i] = 'http://p3.pstatp.com/large/' + result[i]
    images = result
    for image in images:
        download_image(image)
    return {
        'title': title,
        'url': url,
        'images': images
    }


def save_to_postgres(result):
    conn = psycopg2.connect(database='Reptile', user='odoo', password='odoo', host='192.168.99.100', port='5432')
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


def save_image(content):
    file_path_name = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    file_path_name = '{0}/{1}.{2}'.format('D:\\Reptile', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path_name):
        with open(file_path_name, 'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            save_to_postgres(result)


if __name__ == '__main__':
    # main()
    groups = [x*20 for x in range(GROUP_START, GROUP_END+1)]
    pool = Pool()
    pool.map(main, groups)