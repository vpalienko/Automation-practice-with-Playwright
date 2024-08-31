from playwright.sync_api import Page
from data.data_for_tests import get_random_coffee_type
from pages.base_page import BasePage


class MenuPage(BasePage):
    url = "/"

    def __init__(self, page: Page):
        super().__init__(page)

        self.menu_content = page.get_by_role("list").filter(has=page.locator(".cup"))
        self.coffee_cups = page.get_by_role("listitem").filter(has=page.locator(".cup"))
        self.coffee_cup_titles = self.coffee_cups.get_by_role("heading")
        self.cart_preview = page.locator(".pay-container .cart-preview")
        self.cart_preview_content = self.cart_preview.get_by_role("listitem")
        self.promo_coffee_banner = page.locator(".promo")
        self.promo_coffee_banner_accept_button = self.promo_coffee_banner.get_by_role("button", name="yes")
        self.promo_coffee_banner_skip_button = self.promo_coffee_banner.get_by_role("button", name="skip")

    def click_on_cup(self, coffee_type):
        self.coffee_cups.get_by_label(coffee_type, exact=True).click()

    def right_button_click_on_cup(self, coffee_type):
        self.coffee_cups.get_by_label(coffee_type, exact=True).click(button="right")

    def click_on_any_coffee_cup(self, number_of_selected_cups=1):
        for _ in range(number_of_selected_cups):
            self.coffee_cups.get_by_label(get_random_coffee_type(), exact=True).click()

    def get_cup_title_of_(self, coffee_type):
        return self.coffee_cups.filter(has=self.page.get_by_label(coffee_type, exact=True)).get_by_role("heading")

    def double_click_on_cup_title(self, coffee_type):
        self.get_cup_title_of_(coffee_type).dblclick()

    def hover_over_total_price_button(self):
        self.total_price_button.hover()

    def remove_hover_from_total_price_button(self):
        self.coffee_cups.first.hover()

    def get_cart_preview_content_item(self, coffee_type):
        return self.cart_preview_content.filter(has=self.page.get_by_text(coffee_type, exact=True))

    def get_cart_preview_number_of_units(self, coffee_type):
        return self.get_cart_preview_content_item(coffee_type).locator("div", has=self.page.locator(".unit-desc"))

    def add_via_cart_preview_one_more_unit_of_(self, coffee_type):
        coffee_item = self.get_cart_preview_content_item(coffee_type)
        coffee_item.get_by_role("button", name="add one").click()

    def remove_via_cart_preview_one_unit_of_(self, coffee_type):
        coffee_item = self.get_cart_preview_content_item(coffee_type)
        coffee_item.get_by_role("button", name="remove one").click()

    def accept_promo_coffee(self):
        self.promo_coffee_banner_accept_button.click()

    def skip_promo_coffee(self):
        self.promo_coffee_banner_skip_button.click()