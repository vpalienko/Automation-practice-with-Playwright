from playwright.sync_api import expect
from pytest import mark
from data.data_for_tests import coffee_list, coffee_translations, coffee_names


@mark.data_driven
@mark.parametrize("coffee_type, coffee_price", coffee_list)
def test_add_coffee_to_cart(menu_page, cart_page, coffee_type, coffee_price):
    menu_page.open()
    menu_page.click_on_coffee_cup(coffee_type)
    expect(menu_page.cart_navbar_item).to_have_text("cart (1)")
    expect(menu_page.total_price_button).to_have_text(f"Total: {coffee_price}")
    menu_page.navigate_to_cart()
    expect(cart_page.cart_content_item(coffee_type)).to_be_visible()
    expect(cart_page.cart_content_item(coffee_type)).to_have_count(1)
    expect(cart_page.cart_content_item_counter(coffee_type)).to_have_text(f"{coffee_price} x 1")
    expect(cart_page.total_price_button).to_have_text(f"Total: {coffee_price}")


@mark.feature
@mark.data_driven
@mark.parametrize("coffee_type, chinese_title", coffee_translations)
def test_double_click_changes_coffee_title_to_chinese(menu_page, coffee_type, chinese_title):
    menu_page.open()
    menu_page.double_click_on_coffee_cup_title(coffee_type)
    expect(menu_page.coffee_cup_title(coffee_type)).to_contain_text(chinese_title)


@mark.smoke
def test_navigation_to_cart_page_from_menu_page(menu_page, cart_page):
    menu_page.open()
    menu_page.navigate_to_cart()
    expect(cart_page.page).to_have_url(cart_page.url)


@mark.feature
@mark.data_driven
@mark.parametrize("coffee_type", coffee_names)
def test_right_click_on_coffee_cup_opens_add_to_cart_dialog(menu_page, add_to_cart_dialog, coffee_type):
    menu_page.open()
    menu_page.click_on_coffee_cup(coffee_type, button="right")
    expect(add_to_cart_dialog.popup).to_be_visible()
    expect(add_to_cart_dialog.popup_text).to_have_text(f"Add {coffee_type} to the cart?")
    add_to_cart_dialog.decline()
    expect(add_to_cart_dialog.popup).not_to_be_visible()


@mark.feature
@mark.data_driven
@mark.parametrize("coffee_type, coffee_price", coffee_list)
def test_add_coffee_to_cart_via_add_to_cart_dialog(menu_page, cart_page, add_to_cart_dialog, coffee_type, coffee_price):
    menu_page.open()
    menu_page.click_on_coffee_cup(coffee_type, button="right")
    expect(add_to_cart_dialog.popup).to_be_visible()
    expect(add_to_cart_dialog.popup_text).to_have_text(f"Add {coffee_type} to the cart?")
    add_to_cart_dialog.accept()
    expect(add_to_cart_dialog.popup).not_to_be_visible()
    expect(menu_page.cart_navbar_item).to_have_text("cart (1)")
    expect(menu_page.total_price_button).to_have_text(f"Total: {coffee_price}")
    menu_page.navigate_to_cart()
    expect(cart_page.cart_content_item(coffee_type)).to_be_visible()
    expect(cart_page.cart_content_item(coffee_type)).to_have_count(1)
    expect(cart_page.cart_content_item_counter(coffee_type)).to_have_text(f"{coffee_price} x 1")
    expect(cart_page.total_price_button).to_have_text(f"Total: {coffee_price}")


@mark.smoke
def test_total_price_is_present_and_is_zero_by_default(menu_page):
    menu_page.open()
    expect(menu_page.total_price_button).to_be_visible()
    expect(menu_page.total_price_button).to_have_text("Total: $0.00")