# -*- coding:utf-8 -*-

import requests

def get_page_state(url):
    """
    获取网页状态码信息
    :param url:网页
    :return:状态码
    """
    r = requests.get(url, allow_redirects=False)
    print(r.status_code)

def test03():

    url1 = "http://www.baidu.com"
    url2 = "http://www.xdz.gov.cn/topics/gxqzfbzw/gs/gzf/csgs/100.htm"

    get_page_state(url1)
    get_page_state(url2)

if __name__ == "__main__":
    test03()
