from playwright.sync_api import Page


class BasePage:
    url = None

    def __init__(self, page: Page):
        self.page = page

        self.menu_navbar_item = page.get_by_role("link", name="menu page")
        self.cart_navbar_item = page.get_by_role("link", name="cart page")
        self.total_price = page.get_by_role("button", name="checkout")

    def open(self):
        self.page.goto(self.url)

    def navigate_to_cart(self):
        self.cart_navbar_item.click()

    def navigate_to_menu(self):
        self.menu_navbar_item.click()