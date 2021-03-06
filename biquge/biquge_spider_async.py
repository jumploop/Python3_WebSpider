#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/20 20:46
# @Author  : 一叶知秋
# @File    : main.py
# @Software: PyCharm

import os
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
from requests import RequestException
from async_downloader import download


class BookSpider:
    def __init__(self, url):
        self.start_url = url
        self.book_dir = Path.cwd() / 'books'
        self.html_dir = Path.cwd() / 'htmls'
        self.prefix = 'https://www.jupindai.com'
        self.urls = []
        self.headers = {'User-Agent': 'BaiduSpider'}
        self.init_dir()

    def init_dir(self):
        if not os.path.exists(self.book_dir):
            os.makedirs(self.book_dir)
        if not os.path.exists(self.html_dir):
            os.makedirs(self.html_dir)

    def get_one_page(self, url):
        """获取一页内容"""
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.content
            return None
        except RequestException:
            return None

    def get_all_section_url(self, html):
        """获取所有小说章节链接"""
        sections_list = html.xpath('//*[@id="list-chapterAll"]/dl/dd/a/@href')
        self.urls = [self.prefix + url for url in sections_list]

    def get_book_name(self, html):
        """获取小说名字"""
        self.book_name = html.xpath('/html/body/div[2]/div[1]/div/div/div[2]/h1/text()')[0]

    def create_fiction_html_dir(self):
        # 检查小说的html文件目录是否存在，不存在则创建
        path = Path(self.html_dir).joinpath(self.book_name)
        if not path.exists():
            path.mkdir()

    def parse_html_file(self):
        """解析HTML文件"""
        files = [os.path.join(self.book_html, file) for file in os.listdir(self.book_html)]
        print(files)
        for file in sorted(files):
            html = etree.parse(file, etree.HTMLParser())
            yield html

    def write_to_file(self):
        """将小说写入文件"""
        path = Path(self.book_dir) / (self.book_name + '.txt')
        print(path)
        with path.open('w', encoding='utf-8') as book_file:
            for html in self.parse_html_file():
                self.write_title(html, book_file)
                self.write_content(html, book_file)
            print(f'{self.book_name} file is write done!')

    def write_title(self, html, f):
        """写标题"""
        title = html.xpath('//*[@id="content"]/div[1]/h1/text()')[0]
        print(title)
        f.write(title + os.linesep * 2)

    def write_content(self, html, f):
        """写入章节内容"""
        content_list = html.xpath('//*[@id="htmlContent"]/text()')
        for line in content_list:
            f.write(line)

    def run(self):
        content = self.get_one_page(self.start_url)
        html = etree.HTML(content)
        self.get_book_name(html)
        self.get_all_section_url(html)
        self.create_fiction_html_dir()
        # 小说HTML文件所在目录
        self.book_html = Path(self.html_dir).joinpath(self.book_name)
        # 用协程下载html文件
        os.chdir(self.book_html)
        download(self.urls)
        # 将小说内容写入文件
        self.write_to_file()


def main():
    url = input('请输入小说链接：').strip()
    book = BookSpider(url)
    book.run()


if __name__ == '__main__':
    main()
