from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.support.wait import WebDriverWait

from components.currencies import Currency


class Header:
    currency_tab = (By.CSS_SELECTOR, '.currency-selector')
    active_currency = (By.CLASS_NAME, 'expand-more')
    search_input = (By.CLASS_NAME, 'ui-autocomplete-input')
    sorting_options = (By.XPATH, ".//a")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)

    def set_currency(self, currency: Currency):
        currency_list = self.driver.find_element(*self.currency_tab)
        currency_list.click()
        self.wait.until(presence_of_all_elements_located(self.sorting_options))
        options = currency_list.find_elements(By.TAG_NAME, 'a')
        options[currency].click()

    def get_currency(self):
        currencies = self.driver.find_element(*self.currency_tab)
        return currencies.find_element(*self.active_currency).text

    def make_search(self, query):
        search_field = self.driver.find_element(By.CLASS_NAME, 'ui-autocomplete-input')
        search_field.clear()
        search_field.send_keys(query, Keys.ENTER)
