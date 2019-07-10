# -*- coding:utf-8 -*-

import re

def test04():
    # - 操作字符串
    string = """<a href="http://e.baidu.com/?refer=888" onmousedown="return ns_c({'fm':'behs','tab':'tj_tuiguang'})">百度推广</a>"""

    # - 正则规则
    url_rule = re.compile(r'href="(.*?)"')
    url_name = re.compile(u'>([\u4e00-\u9fa5]+)<')

    # - 正则匹配结果
    url_results = re.findall(url_rule,string)
    name_results = re.findall(url_name,string)

    # - 打印Url
    for line in url_results:
        print(line)

    # - 打印Name
    for line in name_results:
        print(line)

if __name__ == "__main__":
    test04()
