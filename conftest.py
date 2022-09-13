import pytest
from selenium import webdriver

from app.app import App

PORTAL_URL = 'http://prestashop-automation.qatestlab.com.ua/uk/'
pytest_plugins = 'allure'


@pytest.fixture(scope="session")
def app():
    capabilities = {
        "browserName": "firefox",
        "browserVersion": "",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False
        }
    }

    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        desired_capabilities=capabilities)
    app = App(driver)
    app.driver.get(PORTAL_URL)
    yield app

    driver.close()
