import requests
import re
import threadpool
import os


def mkdir(path):
    # function：新建文件夹
    # path：str-从程序文件夹要要创建的目录路径（包含新建文件夹名）
    # 去除首尾空格

    path = path.strip()  # strip方法只要含有该字符就会去除
    # 去除首尾\符号
    path = path.rstrip('\\')
    # 判断路径是否存在
    isExists = os.path.exists(path)

    # 根据需要是否显示当前程序运行文件夹
    # print("当前程序所在位置为："+os.getcwd())

    if not isExists:
        os.makedirs(path)
        print(path + '创建成功')
        return True
    else:
        print(path + '目录已存在')
        return False


class novelSpider:
    def __init__(self, domian_url, url):
        """
        :param url:小说大全url
        """
        self.domian_url = domian_url  # 网站域名
        self.url = url  # 小说大全url
        # 获取每部小说的信息
        self.NovelInfoList = self.getEveryNovelUrl()

    # 请求网页源码
    def getnovelRequestText(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        response = requests.get(url, headers=headers)  # 带消息头请求防止网站反爬虫
        return response.text

    # 获取每个小说的url
    def getEveryNovelUrl(self):
        """
        :return: 返回所有小说的url和小说名
        """
        allNovelHtml = self.getnovelRequestText(self.url)
        # print('所有网页url\n',allNovelHtml)
        if len(allNovelHtml) > 0:
            # 获取maindiv
            maindiv = re.findall(r'<div id="main">(.*?)</div>', allNovelHtml, re.S)
            # print(maindiv)
            if len(maindiv) > 0:
                NovelInfoList = re.findall(r'<a href="(.*?)">(.*?)<', maindiv[0], re.S)
                # print(NovelInfoList)
                return NovelInfoList
        return None

    # 分析小说url获取每章节的url和章节名
    def getEveryChapterUrl(self, novelUrl):
        """
        :param novelUrl: 小说的url
        :return: 每个章节的url和章节名
        """
        novelUrl = self.domian_url + novelUrl
        # 获取小说页面
        chapterInfoHtml = self.getnovelRequestText(novelUrl)
        div = re.findall(r'<div id="list">(.*?)</div>', chapterInfoHtml, re.S)
        if len(div) > 0:
            Allchapter = re.findall(r'<dt><b>.*?</dt>.*?</dt>(.*?)</dl>', div[0], re.S)
            if len(Allchapter) > 0:
                chapter_info_list = re.findall(r'href=\'(.*?)\'>(.*?)<', Allchapter[0], re.S)
                return chapter_info_list
        return None

    # 获取正文内容
    def getchapterContentAndWrite(self, f, chapter_info_list):
        for chapter_info in chapter_info_list:
            chapter_url = self.domian_url + chapter_info[0]
            chapter_title = chapter_info[1]
            # print(chapter_url, chapter_title)
            chapterHtml = self.getnovelRequestText(chapter_url)
            context = re.findall(r'<div id="content">.*?</p>.*?<br/>(.*?)<p>.*?</div>', chapterHtml, re.S)
            if len(context) > 0:
                afterTransContent = self.tranStr(context[0])
                self.writeFile(f, chapter_title, afterTransContent)

    def tranStr(self, context):
        context = context.replace('<br/>', '\n')
        context = context.replace('<br />', '\n')
        context = context.replace('&nbsp;', ' ')
        return context

    # 数据清理

    # 打开文件
    def openFile(self, novelName):
        # 打开文件
        return open(novelName, 'w', encoding='utf-8')

    def writeFile(self, f, chapter_title, context):
        f.write(chapter_title)
        f.write(context)

    def run(self):
        func_args = []
        # 遍历说有小说
        for index, value in enumerate(self.NovelInfoList):
            # if index < 3:  # 这里先爬5部
            if index < 1500 and len(value) == 2:
                func_args.append(([self, value[0], value[1]], None))

        # func_args = [([],None)]
        # 使用线程池进行多线程进行爬虫
        pool = threadpool.ThreadPool(50)
        requests = threadpool.makeRequests(novelSpider.threadFun, func_args)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    def threadFun(self, novelUrl, novelName):
        """
        一部小说一个线程
        :param novelUrl: 小说的url
        :param novelName: 小说名
        :return:
        """
        # 小说路径
        nvoelPath = os.path.join(os.getcwd(), "novelDir")

        if not os.path.exists(nvoelPath):
            mkdir(nvoelPath)

        # 通过小说名创建一个文件
        f = self.openFile(os.path.join(nvoelPath, novelName + ".txt"))  # 返回一个文件对象

        # 获取一部小说的所有章节的url和名字
        chapter_info_list = self.getEveryChapterUrl(novelUrl)

        # 获取正文写入文件
        if len(chapter_info_list) > 0:
            self.getchapterContentAndWrite(f, chapter_info_list)


if __name__ == '__main__':
    domian_url = 'http://www.yuetutu.com/'
    url = 'http://www.yuetutu.com/cbook_all.html'
    novelcollect = novelSpider(domian_url, url)
    novelcollect.run()
