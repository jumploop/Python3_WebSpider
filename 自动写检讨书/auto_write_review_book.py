#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import xlrd

ExcelFile = xlrd.open_workbook(r'test.xlsx')
sheet = ExcelFile.sheet_by_name('Sheet1')
i = []
x = input("请输入具体事件：")
y = int(input("老师要求的字数："))
while len(str(i)) < y * 1.2:
    s = random.randint(1, 60)
    rows = sheet.row_values(s)
    i.append(*rows)
print(" " * 8 + "检讨书" + "\n" + "老师：")
print("我不应该" + str(x) + "，", *i)
print("再次请老师原谅！")
'''
以下是样稿：

请输入具体事件：抽烟
老师要求的字数：200
        检讨书
老师：
我不应该抽烟， 学校一开学就三令五申，一再强调校规校纪，提醒学生不要违反校规，可我却没有把学校和老师的话放在心上，没有重视老师说的话，没有重视学校颁布的重要事项，当成了耳旁风，这些都是不应该的。同时也真诚地希望老师能继续关心和支持我，并却对我的问题酌情处理。 无论在学习还是在别的方面我都会用校规来严格要求自己，我会把握这次机会。 但事实证明，仅仅是热情投入、刻苦努力、钻研学业是不够的，还要有清醒的政治头脑、大局意识和纪律观念，否则就会在学习上迷失方向，使国家和学校受损失。
再次请老师原谅！
'''
