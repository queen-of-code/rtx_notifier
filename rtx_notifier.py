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

add_to_cart_button_search = "add to cart"

NEWEGG = "newegg"
BESTBUY = "bestbuy"

# Update the search term for each of the vendors. the css class to look for. should be fine for a while. currenly setup for 3080
search_details_by_vendor = {
    NEWEGG: ProductSearchDetails(
        "https://www.newegg.com/p/pl?d=rtx+3080&N=50001315%20601357261%20100007709%204841%2050001402%2050001314&isdeptsrh=1",
        "item-cell",
        add_to_cart_button_search,
        2),
    #    "nvidia": ProductSearchDetails(
    #        "https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3080/",
    #        "content-table",
    #        add_to_cart_button_search,
    #        5),
    BESTBUY: ProductSearchDetails(
        "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=brand_facet%3DBrand~ASUS%5Ebrand_facet%3DBrand~EVGA%5Ebrand_facet%3DBrand~NVIDIA&sc=Global&st=rtx%203080&type=page&usc=All%20Categories",
        "sku-item",
        add_to_cart_button_search,
        5)  # ,
    #    "asus": ProductSearchDetails(
    #        "https://store.asus.com/us/search?q=3080&s_c=1",
    #        "item",
    #        "buy now",
    #        30)
}

#    "zotac": (0, "https://store.zotac.com/zotac-gaming-geforce-rtx-3080-trinity-zt-a30800d-10p", "product-essential", "add to cart", 20),
#    "amazon": (0, "https://www.amazon.com/stores/GeForce/RTX3080_GEFORCERTX30SERIES/page/6B204EA4-AAAC-4776-82B1-D7C3BD9DDC82", "style__item__3gM_7", "add to cart", 5),
#    "evga": (0, "https://www.evga.com/products/ProductList.aspx?type=0&family=GeForce+30+Series+Family", "list-item", "qty", 3),
#    "bh": (0, "https://www.bhphotovideo.com/c/products/Graphic-Cards/ci/6567/N/3668461602?filters=fct_nvidia-geforce-series_5011%3Ageforce-rtx-3080", "product_19pae40ejOyj6V7StHfjYz", "add to cart", 30)


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


for vendor_name in search_details_by_vendor.keys():
    ProductScraper(vendor_name, search_details_by_vendor[vendor_name])

while True:
    time.sleep(5)
