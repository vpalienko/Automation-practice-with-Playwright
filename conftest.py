from playwright.sync_api import Page
from pytest import fixture
from data.data_for_tests import coffee_names
from modals.add_to_cart_dialog import AddToCartDialog
from modals.payment_details_dialog import PaymentDetailsDialog
from pages.cart_page import CartPage
from pages.menu_page import MenuPage


@fixture
def menu_page(page: Page):
    return MenuPage(page)


@fixture
def cart_page(page: Page):
    return CartPage(page)


@fixture
def add_to_cart_dialog(page: Page):
    return AddToCartDialog(page)


@fixture
def payment_details_dialog(page: Page):
    return PaymentDetailsDialog(page)


@fixture(params=[coffee_names[0]])
def add_one_coffee_to_cart(menu_page, request):
    menu_page.open()
    coffee = request.param
    menu_page.click_on_cup(coffee)
    return coffee


@fixture
def add_all_coffee_to_cart(menu_page):
    def promo_coffee_banner_handler():
        menu_page.skip_promo_coffee()
    menu_page.page.add_locator_handler(menu_page.promo_coffee_banner, promo_coffee_banner_handler)

    menu_page.open()
    for coffee in coffee_names:
        menu_page.click_on_cup(coffee)