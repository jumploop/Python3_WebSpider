#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests  # 发送get/post请求，获取网站内容
import wechatsogou  # 微信公众号文章爬虫框架
import datetime  # 日期数据处理模块
import pdfkit  # 可以将文本字符串/链接/文本文件转换成为pdf
import os  # 系统文件管理
import re  # 正则匹配模块
import sys  # 项目进程管理
from lxml import etree  # 把html的文本内容解析成html对象
import time  # 时间模块
from PyPDF2 import PdfFileReader, PdfFileWriter  # pdf读取、写入操作模块
from config import cookie

'''
1、从二十次幂获取公众号所有的推文链接和标题
'''


# 自动获取公众号文章总页数
def get_page_num():
    # bid=EOdxnBO4 表示公众号 简说Python，每个公众号都有对应的bid，可以直接搜索查看
    url1 = 'https://www.ershicimi.com/a/EOdxnBO4'
    r = requests.get(url1)
    # 把html的文本内容解析成html对象
    html = etree.HTML(r.text)
    # xpath 根据标签路径提取数据
    page_num = html.xpath('//*[@id="wrapper"]/div/div[2]/div[1]/div[2]/div/div[2]/a/text()')
    return int(page_num[-2])  # 放回倒数第二个元素，就是总页数


# 将title,publish_time,content_url数据格式化成我们想要的形式
def merge_data(title, publish_time, content_url):
    data = []
    for i in range(len(title)):
        html_data = {}
        html_data['title'] = title[i]
        html_data['publish_time'] = publish_time[i]
        html_data['content_url'] = 'https://www.ershicimi.com' + content_url[i]
        data.append(html_data)
    return data


# 获取数据
def get_data():
    # 手动获取登录后的Cookie 保持登录状态
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        # "Cookie": "登录后自己获取下，第一篇教程有详细说明"
        "Cookie": cookie
    }
    # bid=EOdxnBO4 表示公众号 简说Python，每个公众号都有对应的bid，可以直接搜索查看
    # 循环获取所有数据
    page_num = get_page_num()
    print('total page is {}'.format(page_num))
    html_data = []
    for i in range(page_num):
        url1 = 'https://www.ershicimi.com/a/EOdxnBO4?page=%d' % (i + 1)
        print(url1)
        r = requests.get(url1, headers=headers)
        # 把html的文本内容解析成html对象
        html = etree.HTML(r.text)
        # xpath 根据标签路径提取数据
        title = html.xpath('//*[@id="wrapper"]/div/div[2]/div[1]/div[2]/div/div[1]/div/div/h4/a/text()')  # 标题
        publish_time = html.xpath('//*[@id="wrapper"]/div/div[2]/div[1]/div[2]/div/div[1]/div/div/p[2]/@title')  # 发布时间
        content_url = html.xpath('//*[@id="wrapper"]/div/div[2]/div[1]/div[2]/div/div[1]/div/div/h4/a/@href')  # 文章链接
        html_data = html_data + merge_data(title, publish_time, content_url)
        print("第%d页数据获取完成" % (i + 1))
        time.sleep(1)  # 每隔1s 发送一次请求

    return html_data


'''
2、for循环遍历，将每篇文章转化为pdf
'''
# 转化url为pdf时，调用wechatsogou中的get_article_content函数，将url中的代码提取出来转换为html字符串
# 这里先初始化一个WechatSogouAPI对象
ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)


def url_to_pdf(url, title, targetPath, publish_date):
    '''
    使用pdfkit生成pdf文件
    :param url: 文章url
    :param title: 文章标题
    :param targetPath: 存储pdf文件的路径
    :param publish_date: 文章发布日期，作为pdf文件名开头（标识）
    '''
    try:
        content_info = ws_api.get_article_content(url)
    except:
        return False
    # 处理后的html
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
    </head>
    <body>
    <h2 style="text-align: center;font-weight: 400;">{title}</h2>
    {content_info['content_html']}
    </body>
    </html>
    '''
    # html字符串转换为pdf
    filename = publish_date + '-' + ''.join(title.split())
    # 部分文章标题含特殊字符，不能作为文件名
    # 去除标题中的特殊字符 win / \ : * " < > | ？mac :
    # 先用正则去除基本的特殊字符，python中反斜线很烦，最后用replace函数去除
    filename = re.sub('[/:*"<>|？]', '', filename).replace('\\', '')
    print('filename:',filename)
    config_pdf = pdfkit.configuration(wkhtmltopdf=r'D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(html, targetPath + os.path.sep + filename + '.pdf',configuration=config_pdf)
    return filename  # 返回存储路径，后面邮件发送附件需要


'''
3、合并所有的pdf
'''


# 使用os模块的walk函数，搜索出指定目录下的全部PDF文件
# 获取同一目录下的所有PDF文件的绝对路径
def getFileName(filedir):
    file_list = [os.path.join(root, filespath) \
                 for root, dirs, files in os.walk(filedir) \
                 for filespath in files \
                 if str(filespath).endswith('pdf')
                 ]
    file_list.sort()  # 排序
    return file_list if file_list else []


# 合并同一目录下的所有PDF文件
def MergePDF(filepath, outfile):
    output = PdfFileWriter()
    outputPages = 0
    pdf_fileName = getFileName(filepath)

    if pdf_fileName:
        for pdf_file in pdf_fileName:
            #             print("路径：%s"%pdf_file)

            # 读取源PDF文件
            input = PdfFileReader(open(pdf_file, "rb"))

            # 获得源PDF文件中页面总数
            pageCount = input.getNumPages()
            outputPages += pageCount
            #             print("页数：%d"%pageCount)

            # 分别将page添加到输出output中
            for iPage in range(pageCount):
                output.addPage(input.getPage(iPage))

        print("合并后的总页数:%d." % outputPages)
        # 写入到目标PDF文件
        outputStream = open(os.path.join(filepath, outfile), "wb")
        output.write(outputStream)
        outputStream.close()
        print("PDF文件合并完成！")

    else:
        print("没有可以合并的PDF文件！")


if __name__ == '__main__':
    # 0、为爬取内容创建一个单独的存放目录
    gzh_name = '简说Python'  # 爬取公众号名称
    targetPath = os.getcwd() + os.path.sep + gzh_name
    # 如果不存在目标文件夹就进行创建
    if not os.path.exists(targetPath):
        os.makedirs(targetPath)
    print('------pdf存储目录创建成功！')
    datas = get_data()
    print(datas)
    for item in datas:
        print(item)
        try:
            url_to_pdf(item.get('content_url'), item.get('title'), targetPath, item.get('publish_time'))
        except Exception as error:
            print(error)
    MergePDF(targetPath, gzh_name + '.pdf')
