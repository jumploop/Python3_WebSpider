#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time

import pandas as pd
import requests  # 请求网页数据
from tqdm import trange  # 获取爬取速度

"""数据类型
��ೃ��D��
 (���5a44c194:58‘C还是85’C？@���b38701229663584261p���
�������D�� (���423afbdd:	酸梅汤@����b38694783457165315p��
������D�� (���73c69d3a:南昌理工学院@�ݱ�b38692226059468805p΋�
�������D��: (���4846ab8c:哈哈哈哈@�ױ�b38691848491368455p���-
1688不香吗@�ȱ�b38690811250999299p̨��
�������D�� (���b27a18e6:告辞@զ��b38688557065830405p����
����ι�D�� (���6ff7714c:	嘤嘤嘤@����b38687196746088453p����
��������DĒ/ (���937df54b:H茶颜说白就是开分店，背后老板是一个，和加盟不一样@����b38686057055125509p�
�����D��6 (���2d3144aa:说的太好了@����b38685522448089091pۡ�
�������D��6 (���86fb42d5:'蜜雪冰城拉一个人加盟，返70%@����b38685474008072195p���
����馅�D��/ (���86fb42d5:Q蜜雪冰城就是这么干的，现在又搞了一个新品牌，“茶小咖”@����b38685399331110917p���
�������D��' (���98dea343:太真实了@���b38684171157110791p��`
 (���98dea343:别骂了别骂了@���b38683931173715971p��`
 (���9b2245c8:别骂了别骂了@�̰�b38682481037672455pկ�
����ݩ�Dǟ (���2f3a9d0f:古茗好喝！@�Ȱ�b38682252899516419pܳ��
�������D��  (���397218dc:;up主是为了流量告诉你，当然也会有一些加工@꼰�b38681454830419971p����
�������D�� (���96019175:!我也觉得赛百味挺好吃的@ݰ��b38680642231205893p���
��������D�6 (���244e2947:Z这不就是传销吗？不过换了个名字，摆在明面上了，传销的升级版本@����b38680602849837059pߗ��
�������D�� (���e39c7bb1:3块钱@����b38680327296647171p����
�������D֭! (���c4f380b3:专业团队@����b38680193565982725p͟�
�������D�� (���56db374b:真实。。。@����b38679065858146307pޚ�
�������D�� (���21a95d47:	sop嘿嘿@����b38679063747887109p��
�������D� (���21a95d47:对的@����b38678994262949895p��
�������Dα (���6535822d:师傅别练了@����b38678068855832579p���(
�������D�� (���aac52c3e:傻人有傻福，沙比没有@���b38676557763444739p����
�������D�: (���3d02e17b:喵啊@���b38675908077289477pʳ9
�������D�� (���98a6bb6a:!我就吃两个，剩下都给你@���b38675279169716231p�ݫ�
�������D� (���7e269828:	厉害了@�ݯ�b38675039256051717p��� 
�������DԆ (���7fc308da:开彩票店不更香嘛@�ٯ�b38674781778739205pﶆ
�������D��( (���c4e7cf01:开超市吧，稳点@�ï�b38673291120476165p���[
�������D�/ (���9bd4b2e3:但是步行街人流量大@����b38671210936532997p��܇
�������Dڽ- (���b562b432:'刚准备开   现在想想太年轻了@⚯�b38670578963972099p�цl
"""


def get_bilibili_url(start, end):
    url_list = []
    date_list = [i for i in pd.date_range(start, end).strftime('%Y-%m-%d')]
    for date in date_list:
        url = f"https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=141367679&date={date}"
        url_list.append(url)
    return url_list


def get_bilibili_danmu(url_list):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "cookie": "你自己的" # Headers中copy即可
    }

    with open("bilibili_danmu.txt", 'w', encoding='utf-8') as file:
        for i in trange(len(url_list)):
            url = url_list[i]
            response = requests.get(url, headers=headers)
            print(response.headers)
            response.encoding = 'utf-8'
            print(response.text)
            pattern = re.compile(r'.*:\s*(\S*)@')
            danmu = pattern.findall(response.text)
            danmu = [str(d) for d in danmu]
            print(danmu)
            for item in danmu:
                item = re.sub(
                    '[�\x01\x02\x03\\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x1b\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+',
                    '', item)
                file.write(item)
                file.write("\n")
            time.sleep(3)


if __name__ == "__main__":
    start = '9/24/2020'  # 设置爬取弹幕的起始日
    end = '9/26/2020'  # 设置爬取弹幕的终止日
    url_list = get_bilibili_url(start, end)
    print(url_list)
    get_bilibili_danmu(url_list)
    print("弹幕爬取完成")
