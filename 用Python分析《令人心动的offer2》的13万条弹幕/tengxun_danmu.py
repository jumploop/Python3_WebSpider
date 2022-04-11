#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import requests
import json
import time
import pandas as pd


def danmu(target_id, vid, name, total):
    df = pd.DataFrame()
    for page in range(15, total, 30):  # 视频时长共3214秒
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        url = 'https://mfm.video.qq.com/danmu?otype=json&timestamp={0}&target_id={1}vid{2}&count=80'.format(
            page, target_id, vid)
        print(f"正在提取第{str(page)}页")
        html = requests.get(url, headers=headers)
        bs = json.loads(html.text, strict=False)  # strict参数解决部分内容json格式解析报错
        time.sleep(1)
        # 遍历获取目标字段
        for i in bs['comments']:
            username = i['opername']  # 用户名
            content = i['content']  # 弹幕
            upcount = i['upcount']  # 点赞数
            user_degree = i['uservip_degree']  # 会员等级
            timepoint = i['timepoint']  # 发布时间
            comment_id = i['commentid']  # 弹幕id
            cache = pd.DataFrame({
                '用户名': [username],
                '内容': [content],
                '会员等级': [user_degree],
                '评论时间点': [timepoint],
                '评论点赞': [upcount],
                '评论id': [comment_id],
                '期数':[name]
            })
            df = pd.concat([df, cache])
    df.to_csv(f'./令人心动的offer/{name}.csv', encoding='utf_8_sig')


if __name__ == '__main__':
    target_id = "6130942571%26"  # 面试篇的target_id
    vid = "%3Dt0034o74jpr"  # 面试篇的vid
    ids = [("6130942571%26", "%3Dt0034o74jpr", "面试篇", 3214),
           ('6164313448', 'r00346rvwyq', '第1期', 148 * 60),
           ("6194952391", "d0035rctvoh", "第2期", 131 * 60),
           ("6227063464", "b0035j0tgo0", "第3期", 150 * 60)]
    if not os.path.exists("令人心动的offer"):
        os.makedirs('令人心动的offer')
    for i in ids:
        danmu(*i)
