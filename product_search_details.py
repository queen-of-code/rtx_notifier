class ProductSearchDetails(object):
    def __init__(
        self,
        product_search_url: str,
        sku_containter_css_class: str,
        add_to_cart_search: str,
        seconds_delay_between_refresh: int
    ):
        self.product_search_url = product_search_url
        self.sku_containter_css_class = sku_containter_css_class
        self.add_to_cart_search = add_to_cart_search
        self.seconds_delay_between_refresh = seconds_delay_between_refresh

    def to_list(
        self
    ) -> list:
        return [0, self.product_search_url, self.sku_containter_css_class, self.add_to_cart_search, self.seconds_delay_between_refresh]
