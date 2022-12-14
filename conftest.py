import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from app.app import App

PORTAL_URL = 'http://prestashop-automation.qatestlab.com.ua/uk/'


@pytest.fixture(scope="session")
def app():
    options = Options()
    options.set_capability('browserName', 'firefox')
    options.set_capability('selenoid:options',
                           {"enableVNC": True,
                            "enableVideo": False})

    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        options=options
    )
    app = App(driver)
    app.driver.get(PORTAL_URL)
    yield app

    driver.close()
