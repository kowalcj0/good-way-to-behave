# -*- coding: utf-8 -*-

import logging
from types import ModuleType

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common import (
    Selector,
    can_see_elements,
    check_url,
    find_and_click,
    find_and_type,
    go_to_url,
    take_screenshot,
)
from settings import SEARX_URL
from structures.enums import Services

NAME = "Home"
SERVICE = Services.SEARX.value
TYPE = "home"
URL = SEARX_URL

INPUT_BOX = Selector("input field", By.ID, "q")
SEARCH_BUTTON = Selector(
    "search button", By.CSS_SELECTOR, "#search_form button"
)
ADVANCED_SEARCH = Selector(
    "advanced search", By.CSS_SELECTOR, "label[for='check-advanced']"
)
SELECTORS = {
    "navbar": [
        Selector("home link", By.CSS_SELECTOR, "span.instance.pull-left > a"),
        Selector(
            "about link", By.CSS_SELECTOR, "span.pull-right > a[href='/about']"
        ),
        Selector(
            "preferences link",
            By.CSS_SELECTOR,
            "span.pull-right > a[href='/preferences']",
        ),
    ],
    "search form": [
        Selector("logo", By.CSS_SELECTOR, "#main-logo > img"),
        Selector("search form", By.ID, "search_form"),
        ADVANCED_SEARCH,
        INPUT_BOX,
        SEARCH_BUTTON,
    ],
    "footer": [Selector("footer", By.CSS_SELECTOR, "body > div.footer")],
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def is_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    can_see_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def search(driver: WebDriver, term: str, *, category: str = None) -> ModuleType:
    if category:
        label = f"checkbox_{category.lower().replace(' ', '_')}"
        category_selector = Selector(
            category, By.CSS_SELECTOR, f"#categories > label[for='{label}']"
        )
        find_and_click(driver, ADVANCED_SEARCH, wait_for_page_load=False)
        find_and_click(driver, category_selector, wait_for_page_load=False)
    find_and_type(driver, INPUT_BOX, term)
    find_and_click(driver, SEARCH_BUTTON)
    take_screenshot(driver, "After searching")
    from . import results
    return results
