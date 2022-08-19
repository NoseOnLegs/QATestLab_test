import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture(scope="session")
def setup():
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    yield driver

    driver.close()


@pytest.fixture
def make_search():
    pass


@pytest.fixture
def set_currency():
    pass
