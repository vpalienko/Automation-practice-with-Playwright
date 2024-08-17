from playwright.sync_api import expect
from pytest import mark
from data.data_for_tests import coffee_list, coffee_translations, coffee_names


@mark.parametrize("coffee, price", coffee_list)
def test_add_coffee_to_cart(menu_page, cart_page, coffee, price):
    menu_page.open()
    menu_page.click_on_cup(coffee)
    expect(menu_page.cart_navbar_item).to_have_text("cart (1)")
    expect(menu_page.total_price_button).to_have_text(f"Total: {price}")
    menu_page.navigate_to_cart()
    expect(cart_page.get_content_item(coffee)).to_be_visible()
    expect(cart_page.get_content_item(coffee)).to_have_count(1)
    expect(cart_page.get_section_with_number_of_units(coffee)).to_have_text(f"{price} x 1")
    expect(cart_page.total_price_button).to_have_text(f"Total: {price}")


@mark.feature
@mark.parametrize("coffee, chinese_translation", coffee_translations)
def test_double_click_changes_coffee_title_to_chinese(menu_page, coffee, chinese_translation):
    menu_page.open()
    menu_page.double_click_on_cup_title(coffee)
    expect(menu_page.get_cup_title_of_(coffee)).to_contain_text(chinese_translation)


@mark.smoke
def test_navigation_to_cart_page_from_menu_page(menu_page, cart_page, page):
    menu_page.open()
    menu_page.navigate_to_cart()
    expect(page).to_have_url(cart_page.url)


@mark.feature
@mark.parametrize("coffee", coffee_names)
def test_right_click_on_coffee_cup_opens_add_to_cart_dialog(menu_page, add_to_cart_dialog, coffee):
    menu_page.open()
    menu_page.click_on_cup(coffee, button="right")
    expect(add_to_cart_dialog.popup).to_be_visible()
    expect(add_to_cart_dialog.popup_text).to_have_text(f"Add {coffee} to the cart?")
    add_to_cart_dialog.decline()
    expect(add_to_cart_dialog.popup).not_to_be_visible()


@mark.feature
@mark.parametrize("coffee, price", coffee_list)
def test_add_coffee_to_cart_via_add_to_cart_dialog(menu_page, cart_page, add_to_cart_dialog, coffee, price):
    menu_page.open()
    menu_page.click_on_cup(coffee, button="right")
    expect(add_to_cart_dialog.popup).to_be_visible()
    expect(add_to_cart_dialog.popup_text).to_have_text(f"Add {coffee} to the cart?")
    add_to_cart_dialog.accept()
    expect(add_to_cart_dialog.popup).not_to_be_visible()
    expect(menu_page.cart_navbar_item).to_have_text("cart (1)")
    expect(menu_page.total_price_button).to_have_text(f"Total: {price}")
    menu_page.navigate_to_cart()
    expect(cart_page.get_content_item(coffee)).to_be_visible()
    expect(cart_page.get_content_item(coffee)).to_have_count(1)
    expect(cart_page.get_section_with_number_of_units(coffee)).to_have_text(f"{price} x 1")
    expect(cart_page.total_price_button).to_have_text(f"Total: {price}")


@mark.smoke
def test_total_price_is_present_and_is_zero_by_default(menu_page):
    menu_page.open()
    expect(menu_page.total_price_button).to_be_visible()
    expect(menu_page.total_price_button).to_have_text("Total: $0.00")


@mark.feature
@mark.usefixtures("add_one_coffee_to_cart")
def test_hover_over_total_price_to_show_cart_preview(menu_page):
    menu_page.hover_over_total_price_button()
    expect(menu_page.cart_preview).to_be_visible()
    expect(menu_page.cart_preview_content).to_have_count(1)
    menu_page.remove_hover_from_total_price_button()
    expect(menu_page.cart_preview).not_to_be_visible()


@mark.feature
@mark.usefixtures("add_one_coffee_to_cart")
def test_add_and_remove_coffee_via_cart_preview(menu_page):
    menu_page.hover_over_total_price_button()
    menu_page.add_one_more_coffee_via_cart_preview()
    expect(menu_page.cart_preview_content).to_contain_text("x 2")
    menu_page.remove_one_coffee_from_cart_preview()
    expect(menu_page.cart_preview_content).to_contain_text("x 1")


@mark.feature
@mark.usefixtures("add_one_coffee_to_cart")
def test_cart_preview_is_closed_if_last_item_is_removed(menu_page):
    menu_page.hover_over_total_price_button()
    menu_page.remove_one_coffee_from_cart_preview()
    expect(menu_page.cart_preview).not_to_be_visible()