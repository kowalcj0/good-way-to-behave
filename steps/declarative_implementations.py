# -*- coding: utf-8 -*-
"""Step implementations"""
from types import ModuleType

from behave.runner import Context
from retrying import retry
from selenium.common.exceptions import TimeoutException, WebDriverException

from pages import get_page_object
from pages.common import (
    add_actor,
    get_actor,
    get_last_visited_page,
    unauthenticated_actor,
    update_actor,
)
from steps import has_action


def retry_if_webdriver_error(exception):
    """Return True if we should retry on WebDriverException, False otherwise"""
    return isinstance(exception, (TimeoutException, WebDriverException))


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=3,
    retry_on_exception=retry_if_webdriver_error,
    wrap_exception=False,
)
def visit_page(context: Context, actor_alias: str, page_name: str):
    """Will visit specific page.

    NOTE:
    In order for the retry scheme to work properly you should have
    the webdriver' page load timeout set to value lower than the retry's
    `wait_fixed` timer, e.g `driver.set_page_load_timeout(time_to_wait=30)`
    """
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))

    page = get_page_object(page_name)
    has_action(page, "visit")

    page.visit(context.driver)
    update_actor(context, actor_alias, visited_page=page)


def search_for(
    context: Context, actor_alias: str, term: str, *, category: str = None
) -> ModuleType:
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "search")
    result_page = page.search(context.driver, term, category=category)
    update_actor(context, actor_alias, visited_page=result_page)
    return result_page


def should_see_url(context: Context, actor_alias: str, url: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "should_see_url")
    page.should_see_url(context.driver, url)


def visit_and_search(
        context: Context, actor_alias: str, term: str, search_engine: str):
    visit_page(context, actor_alias, f"{search_engine} - Home")
    result_page = search_for(context, actor_alias, term)
    update_actor(context, actor_alias, visited_page=result_page)
