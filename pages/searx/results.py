# -*- coding: utf-8 -*-

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common import (
    Selector,
    can_see_elements,
    check_url,
    find_and_click,
    find_and_type,
    find_elements,
    take_screenshot,
)
from settings import SEARX_URL
from structures.enums import Services

NAME = "Search Results"
SERVICE = Services.SEARX.value
TYPE = "home"
URL = SEARX_URL

INPUT_BOX = Selector("input field", By.ID, "q")
SEARCH_BUTTON = Selector(
    "search button", By.CSS_SELECTOR, "#search_form button"
)
RESULTS_URLS = Selector(
    "search results urls",
    By.CSS_SELECTOR,
    "#main_results h4.result_header > a",
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
    "search": [
        Selector("search form", By.ID, "search_form"),
        INPUT_BOX,
        SEARCH_BUTTON,
    ],
    "results": [RESULTS_URLS],
    "footer": [Selector("footer", By.CSS_SELECTOR, "body > div.footer")],
}


def is_here(driver: WebDriver):
    check_url(driver, URL, exact_match=True)
    can_see_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def search(driver: WebDriver, term: str, category: str = None):
    if category:
        label = f"checkbox_{category.lower().replace(' ', '_')}"
        category_selector = Selector(
            category, By.CSS_SELECTOR, f"#categories > label[for='{label}']"
        )
        find_and_click(driver, category_selector, wait_for_page_load=False)
    find_and_type(driver, INPUT_BOX, term)
    find_and_click(driver, SEARCH_BUTTON)
    take_screenshot(driver, "After searching")


def should_see_url(driver: WebDriver, url: str):
    url_elements = find_elements(driver, RESULTS_URLS)
    urls = [element.get_property("href") for element in url_elements]
    message = f"Couldn't find {url} among all found URLs: {urls}"
    assert url in urls, message
