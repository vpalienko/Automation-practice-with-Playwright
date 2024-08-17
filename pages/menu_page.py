from playwright.sync_api import Page
from pages.base_page import BasePage


class MenuPage(BasePage):
    url = "/"

    def __init__(self, page: Page):
        super().__init__(page)

        self.coffee_cups = page.get_by_role("listitem").filter(has=page.locator(".cup"))
        self.cart_preview = page.locator(".pay-container .cart-preview")
        self.cart_preview_content = page.get_by_role("list").filter(has=page.locator(".list-item"))
        self.cart_preview_add_button = self.cart_preview.get_by_role("button", name="add one")
        self.cart_preview_remove_button = self.cart_preview.get_by_role("button", name="remove one")

    def click_on_cup(self, coffee_type, **kwargs):
        self.coffee_cups.get_by_label(coffee_type, exact=True).click(**kwargs)

    def get_cup_title_of_(self, coffee_type):
        return self.coffee_cups.filter(has=self.page.get_by_label(coffee_type, exact=True)).get_by_role("heading")

    def double_click_on_cup_title(self, coffee_type):
        self.get_cup_title_of_(coffee_type).dblclick()

    def hover_over_total_price_button(self):
        self.total_price_button.hover()

    def remove_hover_from_total_price_button(self):
        self.coffee_cups.first.hover()

    def add_one_more_coffee_via_cart_preview(self):
        self.cart_preview_add_button.click()

    def remove_one_coffee_from_cart_preview(self):
        self.cart_preview_remove_button.click()