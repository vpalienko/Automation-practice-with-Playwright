from playwright.sync_api import expect
from pytest import mark


@mark.smoke
def test_cart_is_empty_by_default(cart_page):
    cart_page.open()
    expect(cart_page.cart_navbar_item).to_have_text("cart (0)")
    expect(cart_page.cart_content).not_to_be_visible()
    expect(cart_page.empty_cart_info_message).to_be_visible()


@mark.smoke
def test_navigation_to_menu_page_from_cart_page(cart_page, menu_page, page):
    cart_page.open()
    cart_page.navigate_to_menu()
    expect(page).to_have_url(menu_page.url)