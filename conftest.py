from playwright.sync_api import Page
from pytest import fixture
from pages.cart_page import CartPage
from pages.menu_page import MenuPage


@fixture
def menu_page(page: Page):
    return MenuPage(page)


@fixture
def cart_page(page: Page):
    return CartPage(page)