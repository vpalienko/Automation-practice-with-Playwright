from playwright.sync_api import expect
from pytest import mark

coffee_list = [('Espresso', '$10.00'),
               ('Espresso Macchiato', '$12.00'),
               ('Cappuccino', '$19.00'),
               ('Mocha', '$8.00'),
               ('Flat White', '$18.00'),
               ('Americano', '$7.00'),
               ('Cafe Latte', '$16.00'),
               ('Espresso Con Panna', '$14.00'),
               ('Cafe Breve', '$15.00')]


@mark.smoke
@mark.parametrize("coffee_type, coffee_price", coffee_list)
def test_add_coffee_to_cart(menu_page, cart_page, coffee_type, coffee_price):
    menu_page.open()
    menu_page.click_on_coffee_cup(coffee_type)
    expect(menu_page.cart_navbar_item).to_have_text("cart (1)")
    expect(menu_page.total_price).to_contain_text(coffee_price)
    menu_page.navigate_to_cart()
    expect(cart_page.total_price).to_contain_text(coffee_price)
    expect(cart_page.cart_item(coffee_type)).to_be_visible()