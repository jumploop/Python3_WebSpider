#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jieba
from nltk.classify import NaiveBayesClassifier

# 需要提前把李白的诗收集一下，放在libai.txt文本中。
text1 = open(r"libai.txt", "rb").read()
list1 = jieba.cut(text1)
result1 = " ".join(list1)
# 需要提前把杜甫的诗收集一下，放在dufu.txt文本中。
text2 = open(r"dufu.txt", "rb").read()
list2 = jieba.cut(text2)
result2 = " ".join(list2)

# 数据准备
libai = result1
dufu = result2


# 特征提取
def word_feats(words):
    return dict([(word, True) for word in words])


libai_features = [(word_feats(lb), 'lb') for lb in libai]
dufu_features = [(word_feats(df), 'df') for df in dufu]
train_set = libai_features + dufu_features
# 训练决策
classifier = NaiveBayesClassifier.train(train_set)

# 分析测试
sentence = input("请输入一句你喜欢的诗：")
print("\n")
seg_list = jieba.cut(sentence)
result1 = " ".join(seg_list)
words = result1.split(" ")

# 统计结果


lb = 0
df = 0
for word in words:
    classResult = classifier.classify(word_feats(word))
    if classResult == 'lb':
        lb = lb + 1
    if classResult == 'df':
        df = df + 1

# 呈现比例
x = float(str(float(lb) / len(words)))
y = float(str(float(df) / len(words)))
print('李白的可能性：%.2f%%' % (x * 100))
print('杜甫的可能性：%.2f%%' % (y * 100))