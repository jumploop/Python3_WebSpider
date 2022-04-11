#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from urllib import parse, request
from queue import Queue
import threading
import os
from retry import retry
from fake_useragent import UserAgent

import sys

# 加上下面代码
os.chdir(sys.path[0])
# 然后就可以愉快使用相对路径了
"""
https://mp.weixin.qq.com/s/AYsVRlGXDikrO_uw2ldn_w
"""
# 目标网址
# "https://pvp.qq.com/web201605/wallpaper.shtml"

headers = {'user-agent': UserAgent().random, 'referer': 'https://pvp.qq.com/'}


# 通过编号来获取不同规格的图片 必须把 200 --> 0
# 发现图片的url做了编码了 parse.unquote 进行了一个解码
def extract_images(data):
    image_urls = []
    for x in range(1, 9):
        image_url = parse.unquote(data['sProdImgNo_%d' % x]).replace('/200', '/0')
        image_urls.append(image_url)
    return image_urls


class Producer(threading.Thread):
    def __init__(self, page_queue, image_queue, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)  # 初始化父类的init方法属性,父类也有__init__方法,如果不初始化,会报错.
        self.page_queue = page_queue
        self.image_queue = image_queue

    def run(self) -> None:
        while not self.page_queue.empty():
            page_url = self.page_queue.get()
            res = requests.get(page_url, headers=headers)
            result = res.json()  # response.json() 是requests第三方库提供的 是将json类型的数据转换成python字典的方法

            datas = result['List']
            for data in datas:
                # extract_images()定义的全局函数函数将图片url的200改成0,并且解码图片url(因为8张图片大小不一样,就是由这个字符串控制,因为看到图片url中有特殊字符%13%aab...)
                image_urls = extract_images(data)
                name = parse.unquote(data['sProdName']).replace(
                    ':', '比').strip()  # [WinError 3] 系统找不到指定的路径。: '1:'
                dirpath = os.path.join('image', name)  # 动态的取添加路径 os.path.join()
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                # 把图片的url放到队列当中
                for index, image_url in enumerate(
                        image_urls):  # 为图片命名 enumerate()来解决图片名字的问题 1.jpg 2.jpg 3.jpg
                    self.image_queue.put({
                        'image_url': image_url,
                        'image_path': os.path.join(dirpath, '%d.jpg' % (index + 1))
                    })


class Comsumer(threading.Thread):
    def __init__(self, image_queue, *args, **kwargs):
        super(Comsumer, self).__init__(*args, **kwargs)
        self.image_queue = image_queue

    def run(self) -> None:
        while True:
            try:
                image_obj = self.image_queue.get(timeout=10)
                image_url = image_obj.get('image_url')
                image_path = image_obj.get('image_path')
                self.download_image(image_url, image_path)
            except BaseException:
                break

    @retry(tries=3)
    def download_image(self, image_url, image_path):
        try:
            request.urlretrieve(image_url, image_path)
            # response = requests.get(image_url,headers=headers)
            # with open(image_path, "wb")as file:
            #     file.write(response.content)
            # time.sleep(uniform(0, 2))
            print(f"{image_path}下载成功!")
        except BaseException as err:
            print(f'下载失败, image url:{image_url}, image path:{image_path}, error: {err}')


def main():
    # 创建url队列一
    page_queue = Queue(25)

    image_queue = Queue(30000)

    for i in range(25):
        img_url = f"https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page={i}&iOrder=0&iSortNumClose=1&171003449092155893818_1620870158277&iAMSActivityId=51991&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735&_=1620870158575"


        page_queue.put(img_url)

    # 创建3个生产者线程
    for _ in range(3):
        pt = Producer(page_queue, image_queue)
        pt.start()

    # 创建5个消费者线程
    for _ in range(5):
        ct = Comsumer(image_queue)
        ct.start()


if __name__ == '__main__':
    main()
