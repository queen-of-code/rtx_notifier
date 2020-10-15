import datetime
import random
import threading
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from product_search_details import ProductSearchDetails

NEWEGG = "newegg"
BESTBUY = "bestbuy"


def restart_selenium(
    driver
):
    if driver is not None:
        driver.close()
    driver = webdriver.Firefox()

    return driver


def start_newegg_checkout(
    driver,
    item
) -> bool:
    btn = item.find_elements_by_class_name("btn-primary")[0]
    btn.click()
    time.sleep(0.5)
    driver.get("https://secure.newegg.com/Shopping/ShoppingCart.aspx")
    time.sleep(0.5)
    driver.get(
        "javascript:attachDelegateEvent((function(){Biz.GlobalShopping.ShoppingCart.checkOut('True')}));")
    time.sleep(3)

    if item.text.lower().find("Your shopping cart is empty") > -1:
        return False

    return True


def scrape_for_product(
    driver: any,
    vendor_name: str,
    vendor_details: ProductSearchDetails,
    delay: float
) -> float:
    no_response_error_text = "site did not respond"
    should_exit = False

    try:
        product_search_url = vendor_details.product_search_url
        driver.get(product_search_url)
        time.sleep(3)
        try:
            element_search = vendor_details.sku_containter_css_class
            items = WebDriverWait(driver, delay).until(
                expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, element_search)))
            for item in items:
                now = datetime.datetime.now()
                print("Time : ")
                print(now.strftime("%Y-%m-%d %H:%M:%S \n"))
                print(f'{vendor_name}\n{item.text}\n')

                if item.text.lower().find(vendor_details.add_to_cart_search) > -1:
                    print(f'item available at {vendor_name}{item.text}')

                    if vendor_name is NEWEGG:
                        should_exit = start_newegg_checkout(driver, item)
                        break
        except TimeoutException:
            print(no_response_error_text)
            delay += 15
    except WebDriverException:
        print(no_response_error_text)
        delay += 15

    return (delay, should_exit)


class ProductScraper(object):
    def __scrape_for_product_loop__(
        self
    ):
        driver_attempt_count = 0
        driver = restart_selenium(None)

        while True:
            if driver_attempt_count > 100:
                driver_attempt_count = 0
            driver_attempt_count += 1

            delay = random.random() * 10 + \
                self.__product_info__.seconds_delay_between_refresh
            print(f'{self.__vendor_name__}\n')

            (delay, should_exit) = scrape_for_product(
                driver,
                self.__vendor_name__,
                self.__product_info__,
                delay)

            if should_exit:
                print("Please finish ordering")

                time.sleep(15 * 60)

            time.sleep(delay)

    def __init__(
        self,
        vendor_name: str,
        vendor_info: ProductSearchDetails
    ) -> None:
        self.__vendor_name__ = vendor_name
        self.__product_info__ = vendor_info
        self.__thread__ = threading.Thread(
            target=self.__scrape_for_product_loop__,
            name=vendor_name)

        self.__thread__.start()
