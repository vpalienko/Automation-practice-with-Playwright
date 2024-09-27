from playwright.sync_api import expect
from pytest import mark
from data.data_for_tests import coffee_names, number_of_available_coffee


@mark.smoke
def test_navbar_items_are_present_on_cart_page(cart_page):
    cart_page.open()
    expect(cart_page.menu_navbar_item).to_be_visible()
    expect(cart_page.cart_navbar_item).to_be_visible()
    expect(cart_page.cart_navbar_item).to_have_text("cart (0)")


@mark.smoke
def test_cart_is_empty_by_default(cart_page):
    cart_page.open()
    expect(cart_page.cart_content).not_to_be_visible()
    expect(cart_page.empty_cart_info_message).to_be_visible()


@mark.smoke
def test_navigation_to_menu_page_from_cart_page(cart_page, menu_page, page):
    cart_page.open()
    cart_page.navigate_to_menu()
    expect(page).to_have_url(menu_page.url)


@mark.usefixtures("add_all_coffee_to_cart")
def test_all_added_types_of_coffee_are_displayed_in_cart(menu_page, cart_page):
    menu_page.navigate_to_cart()
    expect(cart_page.cart_navbar_item).to_have_text(f"cart ({number_of_available_coffee})")
    expect(cart_page.cart_content).to_have_count(number_of_available_coffee)
    expect(cart_page.cart_content).to_contain_text(sorted(coffee_names))


@mark.smoke
def test_add_and_remove_coffee_unit_via_cart(menu_page, cart_page, add_one_coffee_to_cart):
    coffee = add_one_coffee_to_cart
    menu_page.navigate_to_cart()
    cart_page.add_one_more_unit_of_(coffee)
    expect(cart_page.get_section_with_number_of_units(coffee)).to_contain_text("x 2")
    cart_page.remove_one_unit_of_(coffee)
    expect(cart_page.get_section_with_number_of_units(coffee)).to_contain_text("x 1")


@mark.smoke
def test_empty_cart_message_appears_if_last_coffee_unit_is_removed(menu_page, cart_page, add_one_coffee_to_cart):
    coffee = add_one_coffee_to_cart
    menu_page.navigate_to_cart()
    cart_page.remove_one_unit_of_(coffee)
    expect(cart_page.cart_content).not_to_be_visible()
    expect(cart_page.empty_cart_info_message).to_be_visible()


@mark.smoke
def test_remove_coffee_from_cart(menu_page, cart_page, add_one_coffee_to_cart):
    coffee = add_one_coffee_to_cart
    menu_page.navigate_to_cart()
    cart_page.remove_cart_item(coffee)
    expect(cart_page.get_content_item(coffee)).not_to_be_visible()


@mark.smoke
def test_empty_cart_message_appears_if_last_item_is_removed(menu_page, cart_page, add_one_coffee_to_cart):
    coffee = add_one_coffee_to_cart
    menu_page.navigate_to_cart()
    cart_page.remove_cart_item(coffee)
    expect(cart_page.cart_content).not_to_be_visible()
    expect(cart_page.empty_cart_info_message).to_be_visible()


@mark.smoke
@mark.usefixtures("add_one_coffee_to_cart")
def test_payment_dialog_is_opened_after_click_on_total_price_on_cart_page(menu_page, cart_page, payment_details_dialog):
    menu_page.navigate_to_cart()
    cart_page.click_on_total_price_button()
    expect(payment_details_dialog.popup).to_be_visible()
    expect(payment_details_dialog.popup_title).to_have_text("Payment details")
    expect(payment_details_dialog.name_field).to_be_visible()
    expect(payment_details_dialog.email_field).to_be_visible()
    expect(payment_details_dialog.submit_button).to_be_visible()
    expect(payment_details_dialog.close_button).to_be_visible()
    payment_details_dialog.close()
    expect(payment_details_dialog.popup).not_to_be_visible()


@mark.smoke
@mark.usefixtures("add_one_coffee_to_cart")
def test_submit_payment_on_cart_page(menu_page, cart_page, payment_details_dialog, page, faker):
    menu_page.navigate_to_cart()
    cart_page.click_on_total_price_button()
    payment_details_dialog.enter_name(faker.name())
    payment_details_dialog.enter_email(faker.email())
    payment_details_dialog.submit()
    expect(payment_details_dialog.popup).not_to_be_visible()
    expect(page).to_have_url(menu_page.url)
    expect(menu_page.purchase_message).to_be_visible()
    expect(menu_page.purchase_message).to_have_text("Thanks for your purchase. Please check your email for payment.")
    menu_page.wait_for_the_purchase_message_to_disappear()
    expect(menu_page.purchase_message).not_to_be_visible()