
import time

from product_scraper import BESTBUY, NEWEGG, ProductScraper
from product_search_details import ProductSearchDetails

add_to_cart_button_search = "add to cart"

# Update the search term for each of the vendors. the css class to look for. should be fine for a while. currenly setup for 3080
search_details_by_vendor = {
    NEWEGG: ProductSearchDetails(
        "https://www.newegg.com/p/pl?d=rtx+3080&N=50001315%20601357261%20100007709%204841%2050001402%2050001314&isdeptsrh=1",
        "item-cell",
        add_to_cart_button_search,
        2),
    BESTBUY: ProductSearchDetails(
        "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=brand_facet%3DBrand~ASUS%5Ebrand_facet%3DBrand~EVGA%5Ebrand_facet%3DBrand~NVIDIA&sc=Global&st=rtx%203080&type=page&usc=All%20Categories",
        "sku-item",
        add_to_cart_button_search,
        5)
}

#    "zotac": (0, "https://store.zotac.com/zotac-gaming-geforce-rtx-3080-trinity-zt-a30800d-10p", "product-essential", "add to cart", 20),
#    "amazon": (0, "https://www.amazon.com/stores/GeForce/RTX3080_GEFORCERTX30SERIES/page/6B204EA4-AAAC-4776-82B1-D7C3BD9DDC82", "style__item__3gM_7", "add to cart", 5),
#    "evga": (0, "https://www.evga.com/products/ProductList.aspx?type=0&family=GeForce+30+Series+Family", "list-item", "qty", 3),
#    "bh": (0, "https://www.bhphotovideo.com/c/products/Graphic-Cards/ci/6567/N/3668461602?filters=fct_nvidia-geforce-series_5011%3Ageforce-rtx-3080", "product_19pae40ejOyj6V7StHfjYz", "add to cart", 30)


for vendor_name in search_details_by_vendor.keys():
    ProductScraper(vendor_name, search_details_by_vendor[vendor_name])

while True:
    time.sleep(5)
