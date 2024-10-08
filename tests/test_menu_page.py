from playwright.sync_api import expect
from pytest import mark
from data.data_for_tests import (coffee_list, coffee_translations, coffee_names, number_of_available_coffee,
                                 discounted_coffee)


@mark.smoke
def test_navbar_items_are_present_on_menu_page(menu_page):
    menu_page.open()
    expect(menu_page.menu_navbar_item).to_be_visible()
    expect(menu_page.cart_navbar_item).to_be_visible()
    expect(menu_page.cart_navbar_item).to_have_text("cart (0)")


@mark.smoke
def test_all_available_types_of_coffee_are_present_on_menu_page(menu_page):
    menu_page.open()
    expect(menu_page.menu_content).to_be_visible()
    expect(menu_page.coffee_cups).to_have_count(number_of_available_coffee)
    expect(menu_page.coffee_cup_titles).to_contain_text(coffee_names)


@mark.smoke
def test_total_price_is_present_and_is_zero_by_default(menu_page):
    menu_page.open()
    expect(menu_page.total_price_button).to_be_visible()
    expect(menu_page.total_price_button).to_have_text("Total: $0.00")


@mark.smoke
def test_navigation_to_cart_page_from_menu_page(menu_page, cart_page, page):
    menu_page.open()
    menu_page.navigate_to_cart()
    expect(page).to_have_url(cart_page.url)


@mark.smoke
@mark.parametrize("coffee, price", coffee_list)
def test_add_coffee_to_cart(menu_page, cart_page, coffee, price):
    menu_page.open()
    menu_page.click_on_cup(coffee)
    expect(menu_page.cart_navbar_item).to_have_text("cart (1)")
    expect(menu_page.total_price_button).to_have_text(f"Total: {price}")
    menu_page.navigate_to_cart()
    expect(cart_page.cart_navbar_item).to_have_text("cart (1)")
    expect(cart_page.get_content_item(coffee)).to_be_visible()
    expect(cart_page.get_content_item(coffee)).to_have_count(1)
    expect(cart_page.get_section_with_number_of_units(coffee)).to_have_text(f"{price} x 1")
    expect(cart_page.total_price_button).to_have_text(f"Total: {price}")


@mark.smoke
@mark.usefixtures("add_one_coffee_to_cart")
def test_payment_dialog_is_opened_after_click_on_total_price_on_menu_page(menu_page, payment_details_dialog):
    menu_page.click_on_total_price_button()
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
def test_submit_payment_on_menu_page(menu_page, payment_details_dialog, faker):
    menu_page.click_on_total_price_button()
    payment_details_dialog.enter_name(faker.name())
    payment_details_dialog.enter_email(faker.email())
    payment_details_dialog.submit()
    expect(payment_details_dialog.popup).not_to_be_visible()
    expect(menu_page.purchase_message).to_be_visible()
    expect(menu_page.purchase_message).to_have_text("Thanks for your purchase. Please check your email for payment.")
    menu_page.wait_for_the_purchase_message_to_disappear()
    expect(menu_page.purchase_message).not_to_be_visible()
    expect(menu_page.cart_navbar_item).to_have_text("cart (0)")
    expect(menu_page.total_price_button).to_have_text("Total: $0.00")


@mark.smoke
@mark.parametrize("coffee", coffee_names)
def test_place_an_order(menu_page, cart_page, payment_details_dialog, faker, coffee):
    menu_page.open()
    menu_page.click_on_cup(coffee)
    menu_page.navigate_to_cart()
    expect(cart_page.get_content_item(coffee)).to_be_visible()
    cart_page.click_on_total_price_button()
    expect(payment_details_dialog.popup).to_be_visible()
    payment_details_dialog.enter_name(faker.name())
    payment_details_dialog.enter_email(faker.email())
    payment_details_dialog.submit()
    expect(menu_page.purchase_message).to_be_visible()


@mark.feature
class TestChineseTitleTranslation:

    @mark.parametrize("coffee, chinese_translation", coffee_translations)
    def test_double_click_changes_coffee_title_to_chinese(self, menu_page, coffee, chinese_translation):
        menu_page.open()
        menu_page.double_click_on_cup_title(coffee)
        expect(menu_page.get_cup_title_of_(coffee)).to_contain_text(chinese_translation)


@mark.feature
class TestAddToCartDialog:

    @mark.parametrize("coffee", coffee_names)
    def test_right_button_click_on_coffee_cup_opens_add_to_cart_dialog(self, menu_page, add_to_cart_dialog, coffee):
        menu_page.open()
        menu_page.right_button_click_on_cup(coffee)
        expect(add_to_cart_dialog.popup).to_be_visible()
        expect(add_to_cart_dialog.popup_text).to_have_text(f"Add {coffee} to the cart?")
        expect(add_to_cart_dialog.accept_button).to_be_visible()
        expect(add_to_cart_dialog.decline_button).to_be_visible()
        add_to_cart_dialog.decline()
        expect(add_to_cart_dialog.popup).not_to_be_visible()

    @mark.smoke
    @mark.parametrize("coffee, price", coffee_list)
    def test_add_coffee_to_cart_via_add_to_cart_dialog(self, menu_page, cart_page, add_to_cart_dialog, coffee, price):
        menu_page.open()
        menu_page.right_button_click_on_cup(coffee)
        expect(add_to_cart_dialog.popup).to_be_visible()
        add_to_cart_dialog.accept()
        expect(add_to_cart_dialog.popup).not_to_be_visible()
        expect(menu_page.cart_navbar_item).to_have_text("cart (1)")
        expect(menu_page.total_price_button).to_have_text(f"Total: {price}")
        menu_page.navigate_to_cart()
        expect(cart_page.get_content_item(coffee)).to_be_visible()
        expect(cart_page.get_content_item(coffee)).to_have_count(1)
        expect(cart_page.get_section_with_number_of_units(coffee)).to_have_text(f"{price} x 1")
        expect(cart_page.total_price_button).to_have_text(f"Total: {price}")


@mark.feature
class TestCartPreview:

    @mark.usefixtures("add_one_coffee_to_cart")
    def test_hover_over_total_price_button_to_show_cart_preview(self, menu_page):
        menu_page.hover_over_total_price_button()
        expect(menu_page.cart_preview).to_be_visible()
        expect(menu_page.cart_preview_content).to_be_visible()
        menu_page.remove_hover_from_total_price_button()
        expect(menu_page.cart_preview).not_to_be_visible()

    def test_cart_preview_is_not_shown_if_coffee_is_not_added(self, menu_page):
        menu_page.open()
        menu_page.hover_over_total_price_button()
        expect(menu_page.cart_preview).not_to_be_visible()

    @mark.parametrize("add_one_coffee_to_cart", coffee_names, indirect=True)
    def test_added_coffee_is_displayed_in_cart_preview(self, menu_page, add_one_coffee_to_cart):
        coffee = add_one_coffee_to_cart
        menu_page.hover_over_total_price_button()
        expect(menu_page.cart_preview_content).to_have_count(1)
        expect(menu_page.get_cart_preview_number_of_units(coffee)).to_have_text(f"{coffee} x 1")

    @mark.usefixtures("add_all_coffee_to_cart")
    def test_all_added_types_of_coffee_are_displayed_in_cart_preview(self, menu_page):
        menu_page.hover_over_total_price_button()
        expect(menu_page.cart_preview_content).to_have_count(number_of_available_coffee)
        expect(menu_page.cart_preview_content).to_contain_text(sorted(coffee_names))

    def test_add_and_remove_coffee_unit_via_cart_preview(self, menu_page, add_one_coffee_to_cart):
        coffee = add_one_coffee_to_cart
        menu_page.hover_over_total_price_button()
        menu_page.add_via_cart_preview_one_more_unit_of_(coffee)
        expect(menu_page.get_cart_preview_number_of_units(coffee)).to_have_text(f"{coffee} x 2")
        menu_page.remove_via_cart_preview_one_unit_of_(coffee)
        expect(menu_page.get_cart_preview_number_of_units(coffee)).to_have_text(f"{coffee} x 1")

    def test_cart_preview_is_closed_if_last_coffee_unit_is_removed(self, menu_page, add_one_coffee_to_cart):
        coffee = add_one_coffee_to_cart
        menu_page.hover_over_total_price_button()
        menu_page.remove_via_cart_preview_one_unit_of_(coffee)
        expect(menu_page.cart_preview).not_to_be_visible()


@mark.feature
class TestPromoCoffeeBanner:

    @mark.smoke
    def test_promo_coffee_banner_appears_after_adding_third_coffee_to_cart(self, menu_page):
        coffee, price = discounted_coffee
        menu_page.open()
        menu_page.click_on_any_coffee_cup()
        expect(menu_page.promo_coffee_banner).not_to_be_visible()
        menu_page.click_on_any_coffee_cup()
        expect(menu_page.promo_coffee_banner).not_to_be_visible()
        menu_page.click_on_any_coffee_cup()
        expect(menu_page.promo_coffee_banner).to_be_visible()
        expect(menu_page.promo_coffee_banner).to_contain_text(f"Get an extra cup of {coffee} for {price}")
        expect(menu_page.promo_coffee_banner_accept_button).to_be_visible()
        expect(menu_page.promo_coffee_banner_skip_button).to_be_visible()
        menu_page.skip_promo_coffee()
        expect(menu_page.promo_coffee_banner).not_to_be_visible()

    def test_promo_coffee_banner_appears_after_adding_every_third_coffee_to_cart(self, menu_page):
        menu_page.open()
        menu_page.click_on_any_coffee_cup(number_of_selected_cups=3)
        expect(menu_page.promo_coffee_banner).to_be_visible()
        menu_page.skip_promo_coffee()
        expect(menu_page.promo_coffee_banner).not_to_be_visible()
        menu_page.click_on_any_coffee_cup(number_of_selected_cups=3)
        expect(menu_page.promo_coffee_banner).to_be_visible()
        menu_page.skip_promo_coffee()
        expect(menu_page.promo_coffee_banner).not_to_be_visible()
        menu_page.click_on_any_coffee_cup(number_of_selected_cups=3)
        expect(menu_page.promo_coffee_banner).to_be_visible()
        menu_page.skip_promo_coffee()
        expect(menu_page.promo_coffee_banner).not_to_be_visible()

    @mark.smoke
    def test_add_promo_coffee_to_cart_via_promo_coffee_banner(self, menu_page, cart_page):
        coffee, price = discounted_coffee
        menu_page.open()
        menu_page.click_on_any_coffee_cup(number_of_selected_cups=3)
        expect(menu_page.promo_coffee_banner).to_be_visible()
        menu_page.accept_promo_coffee()
        expect(menu_page.promo_coffee_banner).not_to_be_visible()
        expect(menu_page.cart_navbar_item).to_have_text("cart (4)")
        menu_page.navigate_to_cart()
        expect(cart_page.get_content_item(f"(Discounted) {coffee}")).to_be_visible()
        expect(cart_page.get_content_item(f"(Discounted) {coffee}")).to_have_count(1)
        expect(cart_page.get_section_with_number_of_units(f"(Discounted) {coffee}")).to_have_text(f"{price}.00 x 1")