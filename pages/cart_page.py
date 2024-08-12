from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    url = "/cart"

    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_content = page.get_by_role("list").filter(has=page.locator(".list-item"))
        self.empty_cart_info_message = page.get_by_text("No coffee")

    def cart_content_item(self, coffee_type):
        return self.cart_content.get_by_text(coffee_type, exact=True)

    def cart_content_item_counter(self, coffee_type):
        return self.cart_content.filter(has=self.page.get_by_text(coffee_type)).locator(".unit-desc")