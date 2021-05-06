#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import time
import pandas as pd

df = pd.DataFrame()
for page in range(15, 12399, 30):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    url = 'https://mfm.video.qq.com/danmu?otype=json&timestamp={}&target_id=5938032297%26vid%3Dx0034hxucmw&count=80'.format(
        page)
    print("正在提取第" + str(page) + "页")
    html = requests.get(url, headers=headers)
    bs = json.loads(html.text, strict=False)  # strict参数解决部分内容json格式解析报错
    print(bs)
    time.sleep(1)
    # 遍历获取目标字段
    for i in bs['comments']:
        content = i['content']  # 弹幕
        upcount = i['upcount']  # 点赞数
        user_degree = i['uservip_degree']  # 会员等级
        timepoint = i['timepoint']  # 发布时间
        comment_id = i['commentid']  # 弹幕id
        cache = pd.DataFrame({
            '弹幕': [content],
            '会员等级': [user_degree],
            '发布时间': [timepoint],
            '弹幕点赞': [upcount],
            '弹幕id': [comment_id]
        })
        df = pd.concat([df, cache])
df.to_csv('tengxun_danmu.csv', encoding='utf_8_sig',index=False)
print(df.shape)
