
import time

from product_scraper import BESTBUY, NEWEGG, AMAZON, ProductScraper
from product_search_details import ProductSearchDetails

add_to_cart_button_search = "add to cart"

# Update the search term for each of the vendors. the css class to look for. should be fine for a while. currenly setup for 3080
search_details_by_vendor = {
    NEWEGG: ProductSearchDetails(
        "https://www.newegg.com/amd-ryzen-9-5900x/p/N82E16819113664?Description=ryzen%205900X&cm_re=ryzen_5900X-_-19-113-664-_-Product",
        "item-cell",
        add_to_cart_button_search,
        30),
    BESTBUY: ProductSearchDetails(
        "https://www.bestbuy.com/site/amd-ryzen-9-5900x-4th-gen-12-core-24-threads-unlocked-desktop-processor-without-cooler/6438942.p?skuId=6438942",
        "sku-item",
        add_to_cart_button_search,
        30),
    AMAZON: ProductSearchDetails(
        "https://www.amazon.com/dp/B08164VTWH/?coliid=I3PAZ8LEXLKMYN&colid=325VOIXRKKDHA&psc=0&ref_=lv_ov_lig_dp_it",
        "style__item__3gM_7",
        add_to_cart_button_search,
        30)

}

#    "zotac": (0, "https://store.zotac.com/zotac-gaming-geforce-rtx-3080-trinity-zt-a30800d-10p", "product-essential", "add to cart", 20),
#    "amazon": (0, "https://www.amazon.com/stores/GeForce/RTX3080_GEFORCERTX30SERIES/page/6B204EA4-AAAC-4776-82B1-D7C3BD9DDC82", "style__item__3gM_7", "add to cart", 5),
#    "evga": (0, "https://www.evga.com/products/ProductList.aspx?type=0&family=GeForce+30+Series+Family", "list-item", "qty", 3),
#    "bh": (0, "https://www.bhphotovideo.com/c/products/Graphic-Cards/ci/6567/N/3668461602?filters=fct_nvidia-geforce-series_5011%3Ageforce-rtx-3080", "product_19pae40ejOyj6V7StHfjYz", "add to cart", 30)


for vendor_name in search_details_by_vendor.keys():
    ProductScraper(vendor_name, search_details_by_vendor[vendor_name])

while True:
    time.sleep(5)
