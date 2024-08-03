from playwright.sync_api import Page
from pages.base_page import BasePage


class MenuPage(BasePage):
    url = "/"

    def __init__(self, page: Page):
        super().__init__(page)

        self.coffee_cups = page.get_by_role("listitem").filter(has=page.locator(".cup"))

    def click_on_coffee_cup(self, coffee_type, **kwargs):
        self.page.get_by_label(coffee_type, exact=True).click(**kwargs)

    def coffee_cup_title(self, coffee_type):
        return self.coffee_cups.filter(has=self.page.get_by_label(coffee_type, exact=True)).get_by_role("heading")

    def double_click_on_coffee_cup_title(self, coffee_type):
        self.coffee_cup_title(coffee_type).dblclick()