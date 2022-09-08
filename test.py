import time

import allure
from selenium.common import TimeoutException

from components.currencies import Currency
from components.sorting_options import SortingOptions


# class TestScript1:
@allure.title("Open portal test")
def test_open_portal(app):
    assert app.driver.title == 'prestashop-automation'


@allure.title("Check 'popular' tab currency")
def test_popular_tab_currency(app):
    with allure.step("Find defined currency"):
        selected_currency = app.header.get_currency()

    with allure.step("Find currency of 'popular' tab items"):
        currencies = app.main_page.get_all_products_currencies()

    assert all([currency in selected_currency for currency in currencies])


@allure.title("Search for a dress")
def test_search_dress(app):
    with allure.step("Make search"):
        app.header.make_search("dress")

    with allure.step("Check page is loaded"):
        app.result_page.wait_until_page_loaded()


@allure.title("Check search result number is correct")
def test_result_number(app):
    with allure.step("Locate number of results"):
        result_number = app.result_page.get_number_of_results()

    with allure.step("Count number of products and compare with result number"):
        list_of_products = app.result_page.get_all_products()

        assert len(list_of_products) == result_number


@allure.title("Check search results prices in USD")
def test_search_result_prices_in_usd(app):
    with allure.step("Check currency"):
        app.header.set_currency(Currency.USD)
        selected_currency = app.header.get_currency()
        currencies = app.result_page.get_all_products_currencies()

        assert all([currency in selected_currency for currency in currencies])


@allure.title("Sorted not by discount price")
def test_sorted_not_by_desc(app):
    app.result_page.sort_products(SortingOptions.PRICE_DESC)
    with allure.step("Locate containers and scrap prices"):
        prices_list = app.result_page.get_all_products_prices(with_discount=True)

    with allure.step("Compare prices list with sorted list"):
        assert prices_list == sorted(prices_list, reverse=True)


@allure.title("Discounted products contain regular and discounted prices")
def test_discounted_products(app):
    with allure.step("Locate products"):
        products_pricing = app.result_page.get_all_products()
        for product in products_pricing:
            price_n_shipping = app.result_page.get_product_price_and_shipping(product)

            assert len(price_n_shipping) == 1 or len(price_n_shipping) == 3


@allure.title("Test discount is correct")
def test_actual_discount(app):
    with allure.step("Locate discounted products"):
        products = app.result_page.get_all_products()
        discounts = []
        for product in products:
            price_n_shipping = app.result_page.get_product_price_and_shipping(product)
            if len(price_n_shipping) == 3:
                discounts.append(price_n_shipping)

    with allure.step("Calculate actual discount and compare"):
        for item in discounts:
            calculated_price = item["regular_price"] * (100 - item["discount"]) / 100

        assert item["actual_price"] == round(calculated_price, 2)
