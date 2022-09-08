import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from app.app import App

PORTAL_URL = 'http://prestashop-automation.qatestlab.com.ua/uk/'


@pytest.fixture(scope="session")
def app():
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    app = App(driver)
    app.driver.get(PORTAL_URL)
    yield app

    driver.close()
