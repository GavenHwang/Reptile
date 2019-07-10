# -*- coding:utf-8 -*-
import urllib.request

def get_index(url, datas=None):
    """获取网页信息"""

    # - 请求url包装(即使我没有啥包装的)
    response = urllib.request.Request(url=url, data=datas)

    # - 返回页面资源
    page_info = urllib.request.urlopen(response)

    # - 读取页面信息(页面可能编码不同出现乱码 - 转码)
    html = page_info.read().decode("utf-8")

    return html

if __name__ == "__main__":

    url = "http://www.baidu.com"

    # - 调用方法
    get_html = get_index(url)

    # - 打印
    print(get_html)
