from playwright.sync_api import Page
from pages.base_page import BasePage


class MenuPage(BasePage):
    url = "/"

    def __init__(self, page: Page):
        super().__init__(page)

    def click_on_coffee_cup(self, coffee_type):
        self.page.get_by_label(coffee_type, exact=True).click()