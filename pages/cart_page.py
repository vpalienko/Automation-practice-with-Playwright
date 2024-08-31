from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    url = "/cart"

    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_content = page.get_by_role("list").locator(".list-item")
        self.empty_cart_info_message = page.get_by_text("No coffee")

    def get_content_item(self, coffee_type):
        return self.cart_content.get_by_text(coffee_type, exact=True)

    def get_section_with_number_of_units(self, coffee_type):
        return self.cart_content.filter(has=self.page.get_by_text(coffee_type, exact=True)).locator(".unit-desc")