from playwright.sync_api import Page
from pytest import fixture
from data.data_for_tests import coffee_names
from modals.add_to_cart_dialog import AddToCartDialog
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


@fixture(params=[coffee_names[0]])
def add_one_coffee_to_cart(menu_page, request):
    menu_page.open()
    menu_page.click_on_cup(request.param)