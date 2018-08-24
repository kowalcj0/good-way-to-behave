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
    wait_for_visibility
)
from settings import DUCKDUCKGO_URL
from structures.enums import Services

NAME = "Home"
SERVICE = Services.DUCKDUCKGO.value
TYPE = "home"
URL = DUCKDUCKGO_URL

INPUT_BOX = Selector("input field", By.ID, "search_form_input_homepage")
SEARCH_BUTTON = Selector("search button", By.ID, "search_button_homepage")
SELECTORS = {
    "search form": [
        Selector("logo", By.ID, "logo_homepage_link"),
        Selector("search form", By.ID, "search_form_homepage"),
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
    find_and_type(driver, INPUT_BOX, term)
    find_and_click(driver, SEARCH_BUTTON, wait_for_page_load=True)
    if category:
        link_selector = f"a[data-zci-link='{category.lower()}']"
        selector = Selector(category, By.CSS_SELECTOR, link_selector)
        find_and_click(driver, selector, wait_for_page_load=False)
        if category.lower() == "news":
            news_results = Selector(
                "news results", By.CSS_SELECTOR, "div.result.result--news")
            wait_for_visibility(driver, news_results)
        if category.lower() == "videos":
            videos_results = Selector(
                "videos results", By.CSS_SELECTOR, "div.tile--vid")
            wait_for_visibility(driver, videos_results)
    take_screenshot(driver, "After searching")
    from . import results
    return results
