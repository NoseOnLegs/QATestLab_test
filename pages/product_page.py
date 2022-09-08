from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.page import Page


class ProductPage(Page):
    product_container = (By.CSS_SELECTOR, ".thumbnail-container")
    price = (By.CSS_SELECTOR, 'span[class="price"]')
    regular_price = (By.CLASS_NAME, "regular-price")
    discount = (By.CLASS_NAME, "discount-percentage")

    @staticmethod
    def __transform_price(price: str):
        price = price[:5].replace(',', '.')
        return float(price)

    def get_all_products(self):
        return self.driver.find_elements(*self.product_container)

    def get_all_products_prices(self, with_discount=False):
        prices = []
        for product in self.get_all_products():
            if with_discount:
                try:
                    price = product.find_element(*self.regular_price).text
                except NoSuchElementException:
                    price = product.find_element(*self.price).text
            else:
                price = product.find_element(*self.price).text
            prices.append(self.__transform_price(price))
        return prices

    def get_all_products_currencies(self):
        currencies = []
        for product in self.get_all_products():
            currency = product.find_element(*self.price).text.split()
            currencies.append(currency[1])

        return currencies

    def get_product_price_and_shipping(self, product: WebElement):
        price_n_shipping = {"actual_price": self.__transform_price(product.find_element(*self.price).text)}
        try:
            price_n_shipping["regular_price"] = self.__transform_price(product.find_element(*self.regular_price).text)
            price_n_shipping["discount"] = int(product.find_element(*self.discount).text[1])

            return price_n_shipping
        except NoSuchElementException:
            return price_n_shipping
