#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd

def get_mangguo_danmu(num1, num2, page):
    data={}
    try:
        url = 'https://bullet-ws.hitv.com/bullet/2021/05/6/{}/{}/{}.json'
        print("正在爬取第" + str(page) + "页")
        danmuurl = url.format(num1, num2, page)
        res = requests.get(danmuurl)
        res.encoding = 'utf-8'
        #print(res.text)
        data = json.loads(res.text)
    except:
        print("无法连接")
    print(data)
    details = []
    for i in range(len(data['data']['items'])):  # 弹幕数据在json文件'data'的'items'中
        result = {}
        result['stype'] = num2  # 通过stype可识别期数
        result['id'] = data['data']['items'][i]['id']  # 获取id

        try:  # 尝试获取uname
            result['uname'] = data['data']['items'][i]['uname']
        except:
            result['uname'] = ''

        result['content'] = data['data']['items'][i]['content']  # 获取弹幕内容
        result['time'] = data['data']['items'][i]['time']  # 获取弹幕发布时间

        try:  # 尝试获取弹幕点赞数
            result['v2_up_count'] = data['data']['items'][i]['v2_up_count']
        except:
            result['v2_up_count'] = ''
        details.append(result)

    return details

#输入关键信息
def count_danmu():
    danmu_total = []
    num1 = input('第一个数字')
    num2 = input('第二个数字')
    page = int(input('输入总时长'))
    for i in range(page):
        danmu_total.extend(get_mangguo_danmu(num1, num2, i))

    return danmu_total

def main():
    df = pd.DataFrame(count_danmu())
    df.to_csv('mangguo_danmu.csv',encoding='utf_8_sig')

if __name__ == '__main__':
    main()