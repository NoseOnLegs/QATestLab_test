import allure
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as exp_cond


PORTAL_URL = 'http://prestashop-automation.qatestlab.com.ua/ru/'


def __transform_price(given_price: str):
    given_price = given_price[:5]
    given_price = given_price.replace(',', '.')
    return float(given_price)


@allure.title("Open portal test")
def test_open_portal(setup):
    with allure.step("Open portal"):
        browser = setup
        browser.get(PORTAL_URL)

    expected_title = 'prestashop-automation'
    actual_title = browser.title

    assert expected_title == actual_title


@allure.title("Check 'popular' tab currency")
def test_popular_tab_currency(setup):
    browser = setup

    with allure.step("Find defined currency"):
        element = browser.find_element(By.CSS_SELECTOR, 'span.expand-more:nth-child(2)')
        text = element.text
        defined_currency = text[-1]

    with allure.step("Find currency of 'popular' tab items"):
        prices = browser.find_elements(By.CLASS_NAME, "price")
        currencies = [price.text[-1] for price in prices]

    assert all([defined_currency == currency for currency in currencies])


@allure.title("Set currency to USD")
def test_set_currency_to_usd(setup):
    browser = setup

    with allure.step("Change currency"):
        currency_list = browser.find_element(By.CLASS_NAME, "currency-selector")
        currency_list.click()

        wait = WebDriverWait(browser, 5)

        usd = wait.until(exp_cond.presence_of_element_located((By.CSS_SELECTOR,
                                                               "ul.dropdown-menu:nth-child(4) > "
                                                               "li:nth-child(3) > "
                                                               "a:nth-child(1)")))
        usd.click()


@allure.title("Search for a dress")
def test_search_dress(setup):
    browser = setup

    with allure.step("Make search"):
        element = browser.find_element(By.CLASS_NAME, 'ui-autocomplete-input')
        element.send_keys("dress", Keys.ENTER)

    with allure.step("Check page is loaded"):
        wait = WebDriverWait(browser, 5)
        element = wait.until(exp_cond.presence_of_element_located((By.CLASS_NAME, "h2")))

        assert element.text == "Результаты поиска".upper()


@allure.title("Check search result number is correct")
def test_result_number(setup):
    browser = setup

    with allure.step("Locate number of results"):
        element = browser.find_element(By.TAG_NAME, "p")
        result_number = int(element.text[-2])

    with allure.step("Count number of products and compare with result number"):
        list_of_products = browser.find_elements(By.CLASS_NAME, "thumbnail-container")

        assert len(list_of_products) == result_number


@allure.title("Check search results prices in USD")
def test_search_result_prices_in_usd(setup):
    browser = setup

    with allure.step("Check currency"):
        prices = browser.find_elements(By.CLASS_NAME, "price")
        currencies = [price.text[-1] for price in prices]

        assert all([currency == '$' for currency in currencies])


@allure.title("Sort from lower to higher")
def test_sort_by_asc(setup):
    browser = setup

    with allure.step("Locate dropdown list"):
        dropdown = browser.find_element(By.CLASS_NAME, "select-title")
        dropdown.click()

    with allure.step("Click on sorting option"):
        options = browser.find_elements(By.CLASS_NAME, "js-search-link")
        for opt in options:
            if "от высокой к низкой" in opt.text:
                opt.click()
                break

    wait = WebDriverWait(browser, 5)
    wait.until(exp_cond.staleness_of(dropdown))


@allure.title("Sorted not by discount price")
def test_sorted_not_by_desc(setup):
    browser = setup

    with allure.step("Locate containers and scrap prices"):
        products = browser.find_elements(By.CLASS_NAME, "thumbnail-container")
        prices_list = []
        for product in products:
            try:
                price = product.find_element(By.CLASS_NAME, "regular-price")
                prices_list.append(__transform_price(price.text))

            except NoSuchElementException:
                price = product.find_element(By.CLASS_NAME, 'price')
                prices_list.append(__transform_price(price.text))

    with allure.step("Compare prices list with sorted list"):
        assert prices_list == sorted(prices_list, reverse=True)


@allure.title("Discounted products contain regular and discounted prices")
def test_discounted_products(setup):
    browser = setup

    with allure.step("Locate products"):
        products_pricing = browser.find_elements(By.CLASS_NAME, "product-price-and-shipping")
        for product in products_pricing:
            children = product.find_elements(By.TAG_NAME, "span")

            assert len(children) == 1 or len(children) == 3


@allure.title("Test is discount correct")
def test_actual_discount(setup):
    browser = setup

    with allure.step("Locate discounted products"):
        price_n_shipping = browser.find_elements(By.CLASS_NAME, "product-price-and-shipping")
        discounts = []
        for product in price_n_shipping:
            children = product.find_elements(By.TAG_NAME, "span")
            if len(children) == 3:
                discounts.append(product)

    with allure.step("Calculate actual discount and compare"):
        regular_price = browser.find_element(By.CLASS_NAME, "regular-price")
        discount = browser.find_element(By.CLASS_NAME, "discount-percentage")
        actual_price = browser.find_element(By.CLASS_NAME, "price")

        regular_price = __transform_price(regular_price.text)
        actual_price = __transform_price(actual_price.text)
        discount = int(discount.text[1])

        calculated_price = regular_price * (100-discount) / 100

        assert actual_price == round(calculated_price, 2)
