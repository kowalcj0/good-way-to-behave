# -*- coding: utf-8 -*-

import logging
from types import ModuleType
from urllib.parse import urljoin

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
from settings import DUCKDUCKGO_URL
from structures.enums import Services

NAME = "Search Results"
SERVICE = Services.DUCKDUCKGO.value
TYPE = "results"
URL = urljoin(DUCKDUCKGO_URL, "?q=")

INPUT_BOX = Selector("input field", By.ID, "search_form_input")
CLEAR_BUTTON = Selector("search button", By.ID, "search_form_input_clear")
SEARCH_BUTTON = Selector("search button", By.ID, "search_button")
RESULTS_URLS = Selector("search results urls", By.CSS_SELECTOR, "a.result__a",)
VIDEO_RESULTS_URLS = Selector("video search results urls", By.CSS_SELECTOR, "div.tile a")
SELECTORS = {
    "search": [
        Selector("logo", By.CSS_SELECTOR, "a.header__logo-wrap"),
        Selector("search form", By.ID, "search_form_homepage"),
        INPUT_BOX,
        SEARCH_BUTTON,
    ],
    "results": [RESULTS_URLS],
}


def is_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
    can_see_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def search(driver: WebDriver, term: str, category: str = None) -> ModuleType:
    if category:
        link_selector = f"a[data-zci-link='{category.lower()}']"
        selector = Selector(category, By.CSS_SELECTOR, link_selector)
        find_and_click(driver, selector, wait_for_it=False, wait_for_page_load=False)
    find_and_type(driver, INPUT_BOX, term)
    find_and_click(driver, SEARCH_BUTTON)
    take_screenshot(driver, "After searching")
    from . import results
    return results


def should_see_url(driver: WebDriver, url: str):
    page_url_elements = find_elements(driver, RESULTS_URLS)
    video_url_elements = find_elements(driver, VIDEO_RESULTS_URLS)
    url_elements = page_url_elements + video_url_elements
    urls = [element.get_property("href") for element in url_elements]
    message = f"Couldn't find {url} among all found URLs: {urls}"
    assert url in urls, message
