from playwright.sync_api import Page


class AddToCartDialog:
    def __init__(self, page: Page):
        self.page = page

        self.popup = page.get_by_role("dialog")
        self.popup_text = self.popup.get_by_role("paragraph")
        self.accept_button = self.popup.get_by_role("button", name="yes")
        self.decline_button = self.popup.get_by_role("button", name="no")

    def accept(self):
        self.accept_button.click()

    def decline(self):
        self.decline_button.click()