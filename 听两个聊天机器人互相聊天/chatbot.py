#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib.request
from time import sleep
import requests

"""
https://mp.weixin.qq.com/s/Iu7NSdE09lL36Ms0b-MBmA
"""
def tuling_robot():
    s = input("请主人输入话题：")
    while True:
        resp = requests.post("http://www.tuling123.com/openapi/api",
                             data={"key": "4fede3c4384846b9a7d0456a5e1e2943", "info": s, })
        resp = resp.json()
        sleep(1)
        print('小鱼：', resp['text'])
        s = resp['text']
        resp = requests.get("http://api.qingyunke.com/api.php",
                            {'key': 'free', 'appid': 0, 'msg': s})
        resp.encoding = 'utf8'
        resp = resp.json()
        sleep(1)
        print('菲菲：', resp['content'])


# 网上还有一个据说智商比较高的小i机器人，用爬虫的功能来实现一下：


def xiaoi_rebot():
    while True:
        x = input("主人：")
        x = urllib.parse.quote(x)
        link = urllib.request.urlopen(
            "http://nlp.xiaoi.com/robot/webrobot?&callback=__webrobot_processMsg&data=%7B%22sessionId%22%3A%22ff725c236e5245a3ac825b2dd88a7501%22%2C%22robotId%22%3A%22webbot%22%2C%22userId%22%3A%227cd29df3450745fbbdcf1a462e6c58e6%22%2C%22body%22%3A%7B%22content%22%3A%22" +
            x +
            "%22%7D%2C%22type%22%3A%22txt%22%7D")
        html_doc = link.read().decode()
        reply_list = re.findall(r'\"content\":\"(.+?)\\r\\n\"', html_doc)
        print("小i：" + reply_list[-1])


if __name__ == '__main__':
    xiaoi_rebot()
    # tuling_robot()
