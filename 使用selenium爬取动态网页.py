from selenium import webdriver
import time
webdriverPath = r'E:\code\python\spider\chromedriver.exe'

# 创建浏览器对象
browser = webdriver.Chrome(executable_path = webdriverPath)

# 获取网页数据
browser.get("https://ac.qq.com/ComicView/index/id/629102/cid/15")

# 模拟浏览器向下滚动页面
# js1 = "window.scrollTo(0,document.body.scrollHeight)" #滑动滚动条到底部
js1 = "document.body.scrollTo(0,document.body.scrollHeight)"

js2 = "window.scrollTo(0,0)" #滑动到顶部
js3 = "window.scrollTo(0,200)" #向下移动200像素
js4 = "arguments[0].scrollIntoView();" #滑动滚动条到某个指定的元素

time.sleep(10)

browser.execute_script(js1)