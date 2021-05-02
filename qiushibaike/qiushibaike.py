#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 21:12
# @Author  : 一叶知秋
# @File    : qiushibaike.py
# @Software: PyCharm
import csv
import random
import time

import requests
from fake_useragent import UserAgent
from lxml import etree
import pandas as pd


class QSBK(object):
    def __init__(self):
        self.url = "https://www.qiushibaike.com/hot/page/{}"
        self.ua = UserAgent()
        self.fieldnames = ['作者', '年龄', '内容', '好笑数', '评论数']

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
        try:
            response = requests.get(url, headers=self.generate_random_ua)
            if response.status_code == 200:
                return response.text
        except Exception  as e:
            print("连接糗事百科失败,错误原因", e)
            return None

    @staticmethod
    def parse_one_page(contents):
        """
        解析页面数据，提取数据
        :param content:
        :return:
        """
        html = etree.HTML(contents)
        items = html.xpath('//div[contains(@id,"qiushi_tag")]')
        # 用来存储每页的段子们
        pageStories = []
        for item in items:
            # 作者
            author = item.xpath('.//div[@class="author clearfix"]/a[2]/h2/text()')[0].strip()
            # print(author)
            # 年龄
            age = item.xpath('.//div[@class="author clearfix"]/div/text()')[0]
            # print(age)
            # 内容
            content = item.xpath('.//a[1]/div[@class="content"]/span[1]/text()')
            content = '\n'.join([n.strip() for n in content])
            # print(content)
            # 好笑数
            funny_number = item.xpath('.//div[@class="stats"]/span[1]/i/text()')[0]
            # print(funny_number)
            # 评论数
            comments_number = item.xpath('.//div[@class="stats"]/span[2]/a/i/text()')[0]
            # print(comments_number)
            pageStories.append([author, age, content, funny_number, comments_number])
        return pageStories

    def write_to_file_by_csv(self, content):
        """
        将数据写入文件
        :param content:
        :return:
        """
        with open('result.csv', 'w', newline='', encoding='utf-8') as f:
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
        content = [line for line in content]
        df = pd.DataFrame(content, columns=self.fieldnames)
        df.to_excel('results.xlsx', index=False)

    def run(self):
        """
        主方法
        :return:
        """
        results = []
        # 拼接请求的url,总共13页
        urls = [self.url.format(i) for i in range(1, 14)]
        for url in urls:
            # 防止速度过快被禁
            time.sleep(random.randint(1, 3))
            content = self.get_one_page(url)
            item = self.parse_one_page(content)
            print(item)
            results.extend(item)
        self.write_to_file_by_csv(results)
        self.write_to_file_by_pandas(results)


def main():
    qsbk = QSBK()
    qsbk.run()


if __name__ == '__main__':
    main()
