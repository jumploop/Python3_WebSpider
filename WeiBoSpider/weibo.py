#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/9/20 17:57
# @Author  : 一叶知秋
# @File    : weibo.py
# @Software: PyCharm
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/9/9 23:41
# @Author  : 一叶知秋
# @File    : weibo.py
# @Software: PyCharm
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
import json


class WeiBo:
    def __init__(self, uid, since_date=None):
        self.base_url = 'https://m.weibo.cn/api/container/getIndex?'
        self.uid = uid
        self.since_date = since_date
        self.ua = UserAgent()

    @property
    def headers(self):
        return {
            'Host': 'm.weibo.cn',
            'Referer': f'https://m.weibo.cn/u/{self.uid}',
            'User-Agent': self.ua.random,
            'X-Requested-With': 'XMLHttpRequest',
        }

    def get_page(self, page):
        params = {
            'type': 'uid',
            'value': self.uid,
            'containerid': f'100505{self.uid}',
            'page': page
        }
        url = self.base_url + urlencode(params)
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
        except requests.ConnectionError as e:
            print('Error', e.args)

    def parse_page(self, json):
        if json:
            items = json.get('data').get('cards')
            for item in items:
                item = item.get('mblog')
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_count')
                yield weibo


def main():
    uid = input('请输入用户uid：').strip()
    weibo = WeiBo(uid)
    for page in range(1, 11):
        data = weibo.get_page(page)
        print(data)
        with open(f'胡歌-{page}.json', 'w', encoding='utf-8')as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # results = weibo.parse_page(json)
        # for result in results:
        #     print(result)


if __name__ == '__main__':
    main()
