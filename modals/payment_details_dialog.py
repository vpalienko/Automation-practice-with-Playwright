from playwright.sync_api import Page


class PaymentDetailsDialog:
    def __init__(self, page: Page):
        self.page = page

        self.popup = page.locator(".modal-content")
        self.popup_title = self.popup.get_by_role("heading")
        self.name_field = self.popup.get_by_label("name")
        self.email_field = self.popup.get_by_label("email")
        self.submit_button = self.popup.get_by_role("button", name="submit")
        self.close_button = self.popup.get_by_role("button", name="×")