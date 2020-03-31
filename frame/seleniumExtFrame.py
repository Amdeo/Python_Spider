from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ChromeDriver():
    def __init__(self, executable_path, display):
        self.executable_path = executable_path
        self.chrome_options = Options()
        self.browser = self.getbrower(display)

    def getbrower(self, display):
        if not display:
            self.chrome_options.add_argument('--headless')
            self.chrome_options.add_argument('--disable-gpu')
        return webdriver.Chrome(executable_path=self.executable_path, chrome_options=self.chrome_options)


class WebSpider():
    def __init__(self, driver_Path, display, url):
        self.url = url
        self.browser = ChromeDriver(driver_Path, display).browser
        self.browser.get(self.url)
        self.run()

    def run(self):
        pass
