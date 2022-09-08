from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from pages.header import Header


class Page:

    def __init__(self, wd: WebDriver):
        self.driver = wd
        self.header = Header(self.driver)
        self.wait = WebDriverWait(wd, 20)
