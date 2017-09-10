#-*-coding:utf-8-*-
import pymongo
import re
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import jieba
import chardet
import wordcloud
from wordcloud import WordCloud
import numpy as np
connection = pymongo.MongoClient("localhost",27017)
db = connection['zhanlang']
collection = db['zhanlang']
num = collection.count()
print(num)
comments = ""
for i in collection.find():
    comments += i["comment"].strip()
print(comments)
find_text = re.compile(r'[\u4e00-\u9fa5]+')
filter_comment = re.findall(find_text, comments)
print(filter_comment)
cleaned_comment = "".join(filter_comment)
segment = jieba.lcut(cleaned_comment)
print(segment)
words_df = pd.DataFrame({'word':segment})
stopwords = pd.read_csv("stopwords.txt", index_col=False, sep="\t",names=["stopword"],encoding="utf-8")
stopwords.head()
words_df=words_df[~words_df.word.isin(stopwords.stopword)]
words_df.head()
words_count = words_df.groupby(by=['word'])['word'].agg({'count':np.size})
words_count = words_count.reset_index().sort_values(by=['count'],ascending=True)
words_count.head()
matplotlib.rcParams['figure.figsize']=(10.0,5.0)
wordcloud = WordCloud( background_color = 'white',    # 设置背景颜色
#                 mask = backgroud_Imag？e,        # 设置背景图片
                max_words = 2000,            # 设置最大现实的字数
#                 stopwords = STOPWORDS,        # 设置停用词
                font_path = 'C:/Windows/Fonts/FZSTK.TTF',# 设置字体格式，如不设置显示不了中文
                max_font_size = 50,            # 设置字体最大值
                random_state = 30,            # 设置有多少种随机生成状态，即有多少种配色方案
                )
word_frequence = {x[0]:x[1] for x in words_count.values}
# font = 'C:/Windows/Fonts/FZSTK.TTF'
# wc = WordCloud(collocations=False, font_path=font, width=1400, height=1400, margin=2).fit_words(word_frequence)
print(word_frequence)
# word_frequence_list = []
# for key in word_frequence:
#     temp = (key, word_frequence[key])
#     word_frequence_list.append(temp)
# print(word_frequence_list)
wordcloud_pic = wordcloud.fit_words(word_frequence)
# test = [('末', 1), ('末了', 1), ('末页', 1), ('本來', 1)]
# print(dict(test))
# wo = WordCloud().fit_words(dict(test))
plt.imshow(wordcloud_pic)
plt.show()
# %matplotlib inline
# plt.imshow(wordcloud)
# plt.show()
