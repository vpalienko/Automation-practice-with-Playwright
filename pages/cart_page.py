from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    url = "/cart"

    def __init__(self, page: Page):
        super().__init__(page)

        self.empty_cart_info_message = page.get_by_text("No coffee")

    def cart_item(self, coffee_type):
        return self.page.get_by_role("listitem").get_by_text(coffee_type, exact=True)