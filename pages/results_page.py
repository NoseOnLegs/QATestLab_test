from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import staleness_of, presence_of_all_elements_located

from components.sorting_options import SortingOptions
from pages.product_page import ProductPage


class ResultPage(ProductPage):
    total_products = (By.CSS_SELECTOR, '.total-products')
    sorting_dropdown = (By.CLASS_NAME, "select-title")
    sorting_options = (By.CSS_SELECTOR, '.select-list')

    def wait_until_page_loaded(self):
        self.wait.until(presence_of_all_elements_located(self.total_products))

    def sort_products(self, sort_by: SortingOptions):
        dropdown = self.driver.find_element(By.CLASS_NAME, "select-title")
        dropdown.click()
        options_list = self.driver.find_elements(*self.sorting_options)
        option_to_select = options_list[sort_by]
        option_to_select.click()
        self.wait.until(staleness_of(dropdown))

    def get_number_of_results(self):
        element = self.driver.find_element(*self.total_products)
        total = element.find_element(By.TAG_NAME, 'p')
        return int(total.text[-2])
