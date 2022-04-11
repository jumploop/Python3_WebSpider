#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time
import urllib.request
from pprint import pprint

from selenium import webdriver

"""
https://mp.weixin.qq.com/s/Iu7NSdE09lL36Ms0b-MBmA
"""
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.maximize_window()
driver.get("https://www.zhihu.com/question/29134042")
i = 0
while i < 10:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    try:
        driver.find_element_by_css_selector('button.QuestionMainAction').click()
        print(f"page{i}")
        time.sleep(3)
    except:
        break
result_raw = driver.page_source
"""
<img src="https://pic4.zhimg.com/07d8d64eaa1d10d2d284569ccdc7554c_r.jpg?source=1940ef5c" class="ImageView-img" alt="preview" style="width: 654px; transform: translate(164px, 164.294px) scale(1.44037); opacity: 1;">
"""
content_list = re.findall(r'img src="(.+?)"', str(result_raw))
content_list=[url for url in content_list if 'jpg?source' in url]
pprint(content_list)
n = 0

while n < len(content_list):
    i = time.time()
    local = f"{i}.jpg"
    urllib.request.urlretrieve(content_list[n], local)
    print(f"编号：{str(i)}")
    n += 1
