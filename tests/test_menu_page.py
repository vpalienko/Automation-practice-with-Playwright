from playwright.sync_api import expect
from pytest import mark
from data.data_for_tests import coffee_list, coffee_translations


@mark.data_driven
@mark.parametrize("coffee_type, coffee_price", coffee_list)
def test_add_coffee_to_cart(menu_page, cart_page, coffee_type, coffee_price):
    menu_page.open()
    menu_page.click_on_coffee_cup(coffee_type)
    expect(menu_page.cart_navbar_item).to_have_text("cart (1)")
    expect(menu_page.total_price).to_contain_text(coffee_price)
    menu_page.navigate_to_cart()
    expect(cart_page.total_price).to_contain_text(coffee_price)
    expect(cart_page.cart_content_item(coffee_type)).to_be_visible()
    expect(cart_page.cart_content_item(coffee_type)).to_have_count(1)


@mark.feature
@mark.data_driven
@mark.parametrize("coffee_type, chinese_title", coffee_translations)
def test_double_click_changes_coffee_title_to_chinese(menu_page, coffee_type, chinese_title):
    menu_page.open()
    menu_page.double_click_on_coffee_cup_title(coffee_type)
    expect(menu_page.coffee_cup_title(coffee_type)).to_contain_text(chinese_title)