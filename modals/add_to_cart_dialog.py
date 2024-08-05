from playwright.sync_api import Page


class AddToCartDialog:
    def __init__(self, page: Page):
        self.page = page

        self.popup = page.get_by_role("dialog")
        self.popup_text = self.popup.get_by_role("paragraph")
        self.popup_decline_button = self.popup.get_by_role("button", name="no")

    def decline(self):
        self.popup_decline_button.click()