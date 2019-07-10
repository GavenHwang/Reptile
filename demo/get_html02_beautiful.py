# -*- coding:utf-8 -*-
import get_html01
from bs4 import BeautifulSoup


def test02():
    url = "http://www.baidu.com"

    get_html = get_html01.get_index(url)

    # - 将网页信息bs格式化
    soup = BeautifulSoup(get_html, "html.parser")

    # - 获取a标签
    all_a_labels = soup.find_all('a')

    # - 打印
    for line in all_a_labels:
        print(line)


if __name__ == "__main__":
    test02()
