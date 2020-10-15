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
    # Make sure that we wait for the page
    # to fully and properly load
    driver.implicitly_wait(60)

    return driver


def get_direct_cart_add_link(
    vendor_name: str,
    item_element
) -> str:
    if vendor_name is not NEWEGG:
        return None

    if item_element is None:
        return None

    try:
        link_element = item_element.find_element_by_class_name(
            "item-title")

        link_address: str = link_element.get_property("href")
        sku = link_address.split("/")[-1].split("?")[0]
        # Example: https://secure.newegg.com/Shopping/AddtoCart.aspx?Submit=ADD&ItemList=N82E16814487518
        new_link = f'https://secure.newegg.com/Shopping/AddtoCart.aspx?Submit=ADD&ItemList={sku}'

        return new_link
    except Exception:
        return None


def is_page_loaded(
    driver: any
) -> bool:
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'


def wait_for_page_load(
    driver: any,
    maximum_seconds: float = 30.0
):
    if driver is None:
        return

    start_time: datetime = datetime.datetime.utcnow()

    # Make sure that we wait at least 3 seconds so
    # as not to completely trigger all of the bot
    # detection code.
    time.sleep(3.0)

    while (datetime.datetime.utcnow() - start_time).total_seconds() < maximum_seconds and not is_page_loaded(driver):
        time.sleep(1.0)


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
        wait_for_page_load(driver)
        try:
            element_search = vendor_details.sku_containter_css_class
            items = WebDriverWait(driver, delay).until(
                expected_conditions.presence_of_all_elements_located(
                    (By.CLASS_NAME, element_search)))
            for item in items:
                now = datetime.datetime.now()
                print("Time : ")
                print(now.strftime("%Y-%m-%d %H:%M:%S \n"))
                print(f'{vendor_name}\n{item.text}\n')

                new_link = get_direct_cart_add_link(vendor_name, item)

                if item.is_displayed() and item.text.lower().find(vendor_details.add_to_cart_search) > -1:
                    if new_link is not None:
                        driver.get(new_link)
                        not_added = driver.find_elements_by_xpath(
                            '//*[contains(text(), "No item in your shopping cart")]')
                        if not_added is not None and len(not_added) > 0:
                            continue
                    else:
                        item.click()

                    should_exit = True
                    break
        except TimeoutException:
            print(no_response_error_text)
            delay += 15
    except WebDriverException as ex:
        print(f'{no_response_error_text}:{ex}')
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
