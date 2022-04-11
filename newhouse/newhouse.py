# -*- coding = uft-8 -*-
# @Time : 2020/12/19 9:29 下午
# @Author : 公众号 菜J学Python
# @File : newhouse.py
# https://mp.weixin.qq.com/s?__biz=MzAwMjYxNjcwMw==&mid=2456408997&idx=2&sn=b4ad88eff3614a8cc26d25bedee4e501&scene=19#wechat_redirect

from fake_useragent import UserAgent
import csv
import time
import random
import requests
import traceback
from lxml import etree


def get_href(parse, qy):
    items = parse.xpath('//*[@id="parent-content"]/div/div[6]/div/div[1]/div[2]/div')
    try:
        for item in items:
            href = ''.join(item.xpath('./div[2]/div[1]/div[1]/a/@href')).strip()
            # print("初始href为：",href)
            # print(len(href))
            if len(href) > 25:
                href1 = 'http://newhouse.fz0752.com/project/detail.shtml?num=' + href[52:].replace(
                    ".html", "")
            else:
                href1 = 'http://newhouse.fz0752.com/project/detail.shtml?num=' + href[15:]
            # print("详情href为：",href1)
            try:
                get_detail(href1, qy)
            except:
                pass
    except Exception:
        print(traceback.print_exc())


def get_detail(href1, qy):
    time.sleep(random.uniform(1, 2))
    response = requests.get(href1, headers=headers, timeout=5)
    if response.status_code == 200:
        source = response.text
        html = etree.HTML(source)
        # 项目状态
        try:
            xmzt = html.xpath(
                '//*[@id="parent-content"]/div/div[3]/div[3]/div[1]/div[1]/text()')[0].strip()
        except:
            xmzt = None
        # 项目名称
        try:
            name = html.xpath(
                '//*[@id="parent-content"]/div/div[3]/div[3]/div[1]/h1/text()')[0].strip()
        except:
            name = None
        # 项目简介
        ps = html.xpath('//*[@id="parent-content"]/div/div[3]/div[5]/div[2]/div')
        for p in ps:
            try:
                xmjj = p.xpath('./p[1]/text()')[0].strip()
            except:
                xmjj = None
        infos = html.xpath('//*[@id="parent-content"]/div/div[3]/div[5]/div[1]/div/table/tbody')
        for info in infos:
            # 行政区域
            try:
                xzqy = info.xpath('./tr[1]/td[1]/text()')[0].strip()
            except:
                xzqy = None
            # 物业类型
            try:
                wylx = info.xpath('./tr[2]/td[1]/text()')[0].strip()
            except:
                wylx = None
            # 销售价格
            try:
                xsjg = info.xpath('./tr[3]/td[1]/text()')[0].strip()
            except:
                xsjg = None
            # 开盘时间
            try:
                kpsj = info.xpath('./tr[4]/td[1]/text()')[0].strip()
            except:
                kpsj = None
            # 占地面积
            try:
                zdmj = info.xpath('./tr[5]/td[1]/text()')[0].strip()
            except:
                zdmj = None
            # 户 数
            try:
                hs = info.xpath('./tr[6]/td[1]/text()')[0].strip()
            except:
                hs = None
            # 物业公司
            try:
                wygs = info.xpath('./tr[7]/td[1]/text()')[0].strip()
            except:
                wygs = None
            # 小学学区
            try:
                xxxq = info.xpath('./tr[8]/td[1]/text()')[0].strip()
            except:
                xxxq = None
            # 装修情况
            try:
                zxqq = info.xpath('./tr[9]/td[1]/text()')[0].strip()
            except:
                zxqq = None
            # 容积率
            try:
                qjl = info.xpath('./tr[10]/td[1]/text()')[0].strip()
            except:
                qjl = None
            # 停车位
            try:
                tcw = info.xpath('./tr[11]/td[1]/text()')[0].strip()
            except:
                tcw = None
            # 开工时间
            try:
                cgsj = info.xpath('./tr[12]/td[1]/text()')[0].strip()
            except:
                cgsj = None
            # 代理商
            try:
                dls = info.xpath('./tr[13]/td[1]/text()')[0].strip()
            except:
                dls = None
            # 电梯品牌
            try:
                dtpp = info.xpath('./tr[14]/td[1]/text()')[0].strip()
            except:
                dtpp = None
            # 开发企业
            try:
                kfqy = info.xpath('./tr[15]/td[1]/text()')[0].strip()
            except:
                kfqy = None
            # 建筑设计单位
            try:
                jzsjdw = info.xpath('./tr[16]/td[1]/text()')[0].strip()
            except:
                jzsjdw = None

            # 所属板块
            try:
                ssbk = info.xpath('./tr[1]/td[2]/text()')[0].strip()
            except:
                ssbk = None
            # 建筑类别
            try:
                jzlb = info.xpath('./tr[2]/td[2]/text()')[0].strip()
            except:
                jzlb = None
            # 主力户型
            try:
                zlhx = info.xpath('./tr[3]/td[2]/text()')[0].strip()
            except:
                zlhx = None
            # 交楼时间
            try:
                jlsj = info.xpath('./tr[4]/td[2]/text()')[0].strip()
            except:
                jlsj = None
            # 建筑面积
            try:
                jzmj = info.xpath('./tr[5]/td[2]/text()')[0].strip()
            except:
                jzmj = None
            # 楼 栋 数
            try:
                lds = info.xpath('./tr[6]/td[2]/text()')[0].strip()
            except:
                lds = None
            # 物业管理费
            try:
                wyglf = info.xpath('./tr[7]/td[2]/text()')[0].strip()
            except:
                wyglf = None
            # 中学学区
            try:
                zxxq = info.xpath('./tr[8]/td[2]/text()')[0].strip()
            except:
                zxxq = None
            # 产权有效期
            try:
                cqyxq = info.xpath('./tr[9]/td[2]/text()')[0].strip()
            except:
                cqyxq = None
            # 绿化率
            try:
                lul = info.xpath('./tr[10]/td[2]/text()')[0].strip()
            except:
                lul = None
            # 车位配比
            try:
                cwpb = info.xpath('./tr[11]/td[2]/text()')[0].strip()
            except:
                cwpb = None
            # 竣工时间
            try:
                jgsj = info.xpath('./tr[12]/td[2]/text()')[0].strip()
            except:
                jgsj = None
            # 外立面用料
            try:
                wlmyl = info.xpath('./tr[13]/td[2]/text()')[0].strip()
            except:
                wlmyl = None
            # 梯户配比
            try:
                thpb = info.xpath('./tr[14]/td[2]/text()')[0].strip()
            except:
                thpb = None
            # 开发资质
            try:
                kfszz = info.xpath('./tr[15]/td[2]/text()')[0].strip()
            except:
                kfszz = None
            # 园林设计单位
            try:
                ylsjdw = info.xpath('./tr[16]/td[2]/text()')[0].strip()
            except:
                ylsjdw = None

            # 园林风格
            try:
                ylfg = info.xpath('./tr[17]/td/text()')[0].strip()
            except:
                ylfg = None
            # 楼层状况
            try:
                lczc = info.xpath('./tr[18]/td/text()')[0].strip()
            except:
                lczc = None
            # 楼盘特色
            try:
                lcts = info.xpath('./tr[19]/td/text()')[0].strip()
            except:
                lcts = None
            # 项目地址
            try:
                xmdz = info.xpath('./tr[20]/td/text()')[0].strip()
            except:
                xmdz = None

            data = {
                'xmzt': xmzt,
                'name': name,
                'xzqy': xzqy,
                'wylx': wylx,
                'xsjg': xsjg,
                'kpsj': kpsj,
                'zdmj': zdmj,
                'hs': hs,
                'wygs': wygs,
                'xxxq': xxxq,
                'zxqq': zxqq,
                'qjl': qjl,
                'tcw': tcw,
                'cgsj': cgsj,
                'dls': dls,
                'dtpp': dtpp,
                'kfqy': kfqy,
                'jzsjdw': jzsjdw,
                'ssbk': ssbk,
                'jzlb': jzlb,
                'zlhx': zlhx,
                'jlsj': jlsj,
                'jzmj': jzmj,
                'lds': lds,
                'wyglf': wyglf,
                'zxxq': zxxq,
                'cqyxq': cqyxq,
                'lul': lul,
                'cwpb': cwpb,
                'jgsj': jgsj,
                'wlmyl': wlmyl,
                'thpb': thpb,
                'kfszz': kfszz,
                'ylsjdw': ylsjdw,
                'ylfg': ylfg,
                'lczc': lczc,
                'lcts': lcts,
                'xmdz': xmdz,
                'xmjj': xmjj,
                'href': href1,
                'qy': qy
            }
            print(data)
            try:
                with open('hz_newhouse.csv', 'a', encoding='utf_8_sig', newline='') as fp:
                    fieldnames = [
                        'xmzt', 'name', 'xzqy', 'wylx', 'xsjg', 'kpsj', 'zdmj', 'hs', 'wygs',
                        'xxxq', 'zxqq', 'qjl', 'tcw', 'cgsj', 'dls', 'dtpp', 'kfqy', 'jzsjdw',
                        'ssbk', 'jzlb', 'zlhx', 'jlsj', 'jzmj', 'lds', 'wyglf', 'zxxq', 'cqyxq',
                        'lul', 'cwpb', 'jgsj', 'wlmyl', 'thpb', 'kfszz', 'ylsjdw', 'ylfg', 'lczc',
                        'lcts', 'xmdz', 'xmjj', 'href', 'qy'
                    ]
                    writer = csv.DictWriter(fp, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow(data)
            except Exception:
                print(traceback.print_exc())


def main():
    # 46:惠城区，47：仲恺区，171：惠阳区，172：大亚湾，173：博罗县，174：惠东县，175：龙门县
    qy_list = [46, 47, 171, 172, 173, 174, 175]
    for qy in qy_list:  # 遍历区域
        for page in range(1, 50):  # 遍历页数
            url = f'http://www.fz0752.com/project/list.shtml?state=&key=&qy={qy}&area=&danjia=&func=&fea=&type=&kp=&mj=&sort=&pageNO={page}'
            response = requests.request("GET", url, headers=headers, timeout=5)
            print(response.status_code)
            if response.status_code == 200:
                re = response.content.decode('utf-8')
                print(f"正在提取{str(qy)}第{str(page)}页")
                # time.sleep(random.uniform(1, 2))
                print("-" * 80)
                # print(re)
                parse = etree.HTML(re)
                get_href(parse, qy)
                num = ''.join(
                    parse.xpath(
                        '//*[@id="parent-content"]/div/div[6]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/a/@href'
                    ))
                # print(len(num))
                if not num:
                    break


if __name__ == '__main__':
    ua = UserAgent(verify_ssl=False)
    headers = {"User-Agent": ua.random}
    time.sleep(random.uniform(1, 2))
    main()

# @Author : J哥
# 公众号：菜J学Python
# 本公众号专注Ptyhon爬虫、数据分析和可视化等原创输出，欢迎关注！
