from selenium.webdriver.chrome.webdriver import WebDriver

from pages.header import Header
from pages.main_page import MainPage
from pages.results_page import ResultPage


class App:
    def __init__(self, wd: WebDriver):
        self.driver = wd
        self.header = Header(wd)
        self.main_page = MainPage(wd)
        self.result_page = ResultPage(wd)
