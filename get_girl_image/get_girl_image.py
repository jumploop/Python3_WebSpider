#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from helium import start_chrome, write, press, ENTER, click

"""
百度图片获取小姐姐图片

需要安装helium库

pip install Helium
"""

def get_girl_image(number):
    driver = start_chrome('https://image.baidu.com')
    write('小姐姐')
    press(ENTER)
    time.sleep(3)
    for i in range(number):
        image = driver.find_element_by_name('pn{}'.format(i))
        click(image)
        time.sleep(2)
        click('下载')
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)


if __name__ == '__main__':
    get_girl_image(10)
