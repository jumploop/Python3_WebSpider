#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/9/10 21:08
# @Author  : 一叶知秋
# @File    : qidian.py
# @Software: PyCharm
import csv
import requests
from fake_useragent import UserAgent
from lxml import etree
from requests import RequestException
import pandas as pd


class QiDian(object):
    def __init__(self):
        self.url = "https://www.qidian.com/rank/yuepiao?chn=-1&page={}"
        self.ua = UserAgent()
        self.fieldnames = ['排行', '书名', '作者', '类型', '简介', '最新章节', '书的地址链接', '图片链接']

    @property
    def generate_random_ua(self):
        """
        生成随机User-Agent
        :return:
        """
        headers = {
            'User-Agent': self.ua.random
        }
        return headers

    def get_one_page(self, url):
        """
        请求url返回响应结果
        :param url:
        :return:
        """
        print(self.generate_random_ua)
        try:
            response = requests.get(url, headers=self.generate_random_ua)
            if response.status_code == 200:
                return response.content
            return None
        except RequestException:
            return None

    @staticmethod
    def parse_one_page(content):
        """
        解析页面数据，提取数据
        :param content:
        :return:
        """
        html = etree.HTML(content)
        items = html.xpath('//*[@id="rank-view-list"]/div/ul/li')
        for item in items:
            index = item.xpath('.//div[1]/span/text()')  # 排行
            book = item.xpath('.//div[2]/h4/a/text()')  # 书名
            author = item.xpath('.//div[2]/p[1]/a[1]/text()')  # 作者
            type_ = item.xpath('.//div[2]/p[1]/a[2]/text()')  # 类型
            intro = item.xpath('.//div[2]/p[2]/text()')  # 简介
            update = item.xpath('.//div[2]/p[3]/a/text()')  # 最新章节
            book_link = item.xpath('.//div[1]/a/@href')  # 书的地址链接
            image = item.xpath('.//div[1]/a/img/@src')  # 图片链接
            yield [index[0], book[0], author[0], type_[0], intro[0].strip(), update[0], ''.join(('https:', image[0])),
                   ''.join(('https:', book_link[0]))]

    def write_to_file_by_csv(self, content):
        """
        将数据写入文件
        :param content:
        :return:
        """
        with open('result.csv', 'w', newline='', errors='replace') as f:
            writer = csv.writer(f)
            writer.writerow(self.fieldnames)
            writer.writerows(content)

    def write_to_file_by_pandas(self, content):
        """
        通过pandas模块将数据写入文件
        :param content:
        :return:
        """
        # 输入到to按住Tab有很多格式，储存
        df = pd.DataFrame(content, columns=self.fieldnames)
        print(df)
        df.to_excel('result.xlsx',index=False)

    def run(self):
        """
        主方法
        :return:
        """
        results = []
        # 拼接请求的url
        urls = [self.url.format(i) for i in range(1, 6)]
        for url in urls:
            content = self.get_one_page(url)
            for item in self.parse_one_page(content):
                print(item)
                results.append(item)

        self.write_to_file_by_csv(results)
        self.write_to_file_by_pandas(results)


def main():
    qidian = QiDian()
    qidian.run()


if __name__ == '__main__':
    main()
