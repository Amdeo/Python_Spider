import requests
import re

url = "http://www.yuetutu.com/cbook_22866/"

response = requests.get(url)
html = response.text
# 获取小说标题
title = re.findall(r'<meta property="og:title" content="(.*?)"/>', html)[0]

# 创建txt文件
fb = open('%s.txt' % title,'w',encoding='utf-8')

# 获取章节名和url
div = re.findall(r'<div id="list">(.*?)</div>', html, re.S)[0]
# print(list1)

Allchapter = re.findall(r'<dt><b>.*?</dt>.*?</dt>(.*?)</dl>', div, re.S)[0]
# print(Allchapter)

chapter_info_list = re.findall(r'href=\'(.*?)\'>(.*?)<', Allchapter, re.S)
# print(chapter_info_list)

# 获取章节url和章节名
for chapter_info in chapter_info_list:
    chapter_url = "http://www.yuetutu.com%s" % chapter_info[0]
    chapter_title = chapter_info[1]
    print(chapter_url, chapter_title)
    # 下载章节内容
    chapter = requests.get(chapter_url)
    chapter.encoding = 'utf-8'
    chapter_html = chapter.text
    # print(chapter_html)

    context = re.findall(r'<div id="content">.*?</p>.*?<br/>(.*?)<p>.*?</div>', chapter_html, re.S)[0]
    # print(context)
    # 格式转换
    context = context.replace('<br/>', '\n')
    context = context.replace('<br />', '\n')
    context = context.replace('&nbsp;', ' ')
    # print(context)
    fb.write(chapter_title)
    fb.write(context)
