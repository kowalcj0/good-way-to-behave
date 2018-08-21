# -*- coding: utf-8 -*-
"""Common PageObject actions."""
import logging
import os
import random
import string
import sys
import traceback
import uuid
from contextlib import contextmanager
from datetime import datetime
from importlib import import_module
from os import path
from pkgutil import iter_modules
from types import ModuleType
from typing import Dict, List

from behave.runner import Context
from retrying import retry
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

from settings import TAKE_SCREENSHOTS
from structures.classes import WaitForPageLoadAfterAction
from structures.tuples import Actor, ScenarioData, Selector


def go_to_url(driver: WebDriver, url: str, page_name: str):
    """Go to the specified URL and take a screenshot afterwards."""
    driver.get(url)
    take_screenshot(driver, page_name)


def check_url(
    driver: WebDriver, expected_url: str, *, exact_match: bool = True
):
    """Check if current page URL matches the expected one."""
    with assertion_msg(
        "Expected page URL to be: '%s' but got '%s'",
        expected_url,
        driver.current_url,
    ):
        if exact_match:
            assert driver.current_url == expected_url
        else:
            assert (driver.current_url in expected_url) or (
                expected_url in driver.current_url
            )
    logging.debug("Current page URL matches expected '%s'", driver.current_url)


def can_see_elements(
    driver: WebDriver, selectors: Dict, *, wait_for_it: bool = True
):
    """Check if all page elements are visible."""
    for section in selectors:
        for selector in section:
            if not isinstance(selector, Selector):
                raise TypeError(
                    "Expected '{}' to be a Selector, got {}".format(
                        selector, type(selector)
                    )
                )
            element = find_element(driver, selector, wait_for_it=wait_for_it)
            with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                selector.name,
                driver.current_url,
            ):
                assert element.is_displayed()
        logging.debug(
            "All expected elements are visible on '%s'", driver.current_url
        )


def find_and_click(
    driver: WebDriver,
    selector: Selector,
    *,
    wait_for_it: bool = True,
    wait_for_page_load: bool = True,
    timeout: int = 3,
):
    """Find page element in any page section selectors and click on it."""
    web_element = find_element(driver, selector, wait_for_it=wait_for_it)
    check_if_element_is_visible(web_element, selector.name)
    if wait_for_page_load:
        with WaitForPageLoadAfterAction(driver, timeout=timeout):
            web_element.click()
    else:
        web_element.click()


def find_and_type(driver: WebDriver, selector: Selector, term: str):
    """Find page element in any page section selectors and click on it."""
    element = find_element(driver, selector)
    element.clear()
    element.send_keys(term)


def initialize_scenario_data() -> ScenarioData:
    """Will initialize the Scenario Data."""
    return ScenarioData(actors={})


def unauthenticated_actor(
    alias: str, *, self_classification: str = None
) -> Actor:
    """Create an instance of an unauthenticated Actor.

    Will:
     * generate a random password for user, which can be used later on during
        registration or signing-in.
    """
    email = (
        "test+{}{}@example.com".format(alias, str(uuid.uuid4()))
        .replace("-", "")
        .replace(" ", "")
        .lower()
    )
    password_length = 20
    password = "".join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(password_length)
    )
    return Actor(alias=alias, email=email, password=password)


def add_actor(context: Context, actor: Actor):
    """Will add Actor details to Scenario Data."""
    assert isinstance(
        actor, Actor
    ), "Expected Actor named tuple but got '{}'" " instead".format(type(actor))
    context.scenario_data.actors[actor.alias] = actor
    logging.debug("Successfully added actor: %s to Scenario Data", actor.alias)


def get_actor(context: Context, alias: str) -> Actor:
    """Get actor details from context Scenario Data."""
    return context.scenario_data.actors.get(alias)


def get_last_visited_page(context: Context, actor_alias: str) -> ModuleType:
    """Get last visited Page Object context Scenario Data."""
    actor = context.scenario_data.actors.get(actor_alias)
    return actor.visited_page


def update_actor(context: Context, alias: str, **kwargs):
    """Update Actor's details stored in context.scenario_data"""
    actors = context.scenario_data.actors
    for arg in kwargs:
        if arg in Actor._fields:
            logging.debug("Set '%s'='%s' for %s", arg, kwargs[arg], alias)
            actors[alias] = actors[alias]._replace(**{arg: kwargs[arg]})
    logging.debug(
        "Successfully updated %s's details: %s", alias, actors[alias]
    )


@retry(stop_max_attempt_number=3)
def take_screenshot(driver: WebDriver, page_name: str):
    """Will take a screenshot of current page."""
    if TAKE_SCREENSHOTS:
        session_id = driver.session_id
        browser = driver.capabilities.get("browserName", "unknown_browser")
        version = driver.capabilities.get("version", "unknown_version")
        platform = driver.capabilities.get("platform", "unknown_platform")
        stamp = datetime.isoformat(datetime.utcnow())
        filename = "{}-{}-{}-{}-{}-{}.png".format(
            stamp, page_name, browser, version, platform, session_id
        )
        file_path = path.abspath(path.join("screenshots", filename))
        driver.save_screenshot(file_path)
        logging.debug("Screenshot of '%s' saved in: %s", page_name, filename)
    else:
        logging.debug(
            "Taking screenshots is disabled. In order to turn it on please set"
            " n environment variable TAKE_SCREENSHOTS=true"
        )


@contextmanager
def assertion_msg(message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception
    """
    try:
        yield
    except AssertionError as e:
        if args:
            message = message % args
        logging.error(message)
        e.args += (message,)
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        raise


@contextmanager
def selenium_action(driver: WebDriver, message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception

    :raises WebDriverException, NoSuchElementException or TimeoutException
    """
    try:
        yield
    except (WebDriverException, NoSuchElementException, TimeoutException) as e:
        browser = driver.capabilities.get("browserName", "unknown browser")
        version = driver.capabilities.get("version", "unknown version")
        platform = driver.capabilities.get("platform", "unknown platform")
        session_id = driver.session_id
        info = "[{} v:{} os:{} session_id:{}]".format(
            browser, version, platform, session_id
        )
        if args:
            message = message % args
        print("{} - {}".format(info, message))
        logging.debug("%s - %s", info, message)
        e.args += (message,)
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        raise


def wait_for_visibility(
    driver: WebDriver, selector: Selector, *, time_to_wait: int = 5
):
    """Wait until element is visible."""
    by_locator = (selector.by, selector.value)
    with selenium_action(
        driver,
        "Element identified by '{}' was not visible after waiting "
        "for {} seconds".format(selector.value, time_to_wait),
    ):
        WebDriverWait(driver, time_to_wait).until(
            expected_conditions.visibility_of_element_located(by_locator)
        )


def check_if_element_is_visible(web_element: WebElement, element_name: str):
    """Check if provided web element is visible."""
    with assertion_msg(
        "Expected to see '%s' element but it's not visible", element_name
    ):
        assert web_element.is_displayed()


def find_element(
    driver: WebDriver, selector: Selector, *, wait_for_it: bool = True
) -> WebElement:
    """Find element by CSS selector or it's ID."""
    with selenium_action(
        driver,
        "Couldn't find element called '%s' using selector '%s' on" " %s",
        selector.name,
        selector.value,
        driver.current_url,
    ):
        element = driver.find_element(by=selector.by, value=selector.value)
    if wait_for_it:
        wait_for_visibility(driver, selector)
    return element


def find_elements(driver: WebDriver, selector: Selector) -> List[WebElement]:
    """Find elements by specific selector."""
    with selenium_action(driver, f"Can't find elements with {selector.value}"):
        elements = driver.find_elements(by=selector.by, value=selector.value)
    return elements


def clear_driver_cookies(driver: WebDriver):
    try:
        cookies = driver.get_cookies()
        logging.debug("COOKIES: %s", cookies)
        driver.delete_all_cookies()
        logging.debug("Successfully cleared cookies")
        cookies = driver.get_cookies()
        logging.debug("Driver cookies after clearing them: %s", cookies)
    except WebDriverException as ex:
        logging.error("Failed to clear cookies: '%s'", ex.msg)


@contextmanager
def wait_for_page_load(driver: WebDriver, timeout: int = 30):
    """Alternative Context manager for waiting for page to load.
    src:
    http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
    """
    old_page = driver.find_element_by_tag_name("html")
    yield
    logging.debug("WAITING FOR STALENESS OF OLD PAGE %s", driver.current_url)
    WebDriverWait(driver, timeout).until(staleness_of(old_page))


def scroll_to(driver: WebDriver, element: WebElement):
    vertical_position = element.location["y"]
    logging.debug("Moving focus to %s", element.id)
    driver.execute_script("window.scrollTo(0, {});".format(vertical_position))


def show_snackbar_message(driver: WebDriver, message: str):
    script = """
    function removeElement(id) {{
        var existing = document.getElementById(id);
        if(existing) {{
            existing.parentNode.removeChild(existing);
        }};
    }};

    function addElement(tag, innerHTML, id) {{
        removeElement(id);
        var node = document.createElement(tag);
        node.innerHTML = innerHTML;
        node.id = id;
        document.body.appendChild(node);
    }};

    function showSnackBar() {{
        var x = document.getElementById("snackbar");
        x.className = "show";
        setTimeout(function(){{ x.className = x.className.replace("show", ""); }}, 3000);
    }};

    function createSnackBarElements(message) {{
        var snackbar_css = `
        #snackbar {{
            visibility: hidden;
            min-width: 250px;
            margin-left: -125px;
            background-color: #333;
            color: #00FF00;
            text-align: center;
            border-radius: 2px;
            padding: 16px;
            position: fixed;
            z-index: 1;
            left: 10%;
            top: 30px;
        }}

        #snackbar.show {{
            visibility: visible;
            -webkit-animation: fadein 0.1s, fadeout 0.1s 1s;
            animation: fadein 0.1s, fadeout 0.1s 1s;
        }}
        
        @-webkit-keyframes fadein {{
            from {{top: 0; opacity: 0;}}
            to {{top: 30px; opacity: 1;}}
        }}
        
        @keyframes fadein {{
            from {{top: 0; opacity: 0;}}
            to {{top: 30px; opacity: 1;}}
        }}
        
        @-webkit-keyframes fadeout {{
            from {{top: 30px; opacity: 1;}}
            to {{top: 0; opacity: 0;}}
        }}
        
        @keyframes fadeout {{
            from {{top: 30px; opacity: 1;}}
            to {{top: 0; opacity: 0;}}
        }}`;

        addElement('style', snackbar_css, 'snackbar_css');
        addElement('div', message, 'snackbar');
    }};

    function deleteSnackBarElements() {{
        removeElement('snackbar');
        removeElement('snackbar_css');
    }};

    function showMessage(message) {{
        deleteSnackBarElements();
        createSnackBarElements(message);
        showSnackBar();
        setTimeout(deleteSnackBarElements, 1000);  
    }};
    
    showMessage(`{message}`);
    """
    message = message.replace("`", "")
    driver.execute_script(script.format(message=message))


def is_page_object(module: ModuleType):
    required_properties = ["SERVICE", "NAME", "TYPE", "URL", "SELECTORS"]
    return all([hasattr(module, prop) for prop in required_properties])


def get_enum_key(module: ModuleType) -> str:
    return (
        f"{module.SERVICE}_{module.NAME}".upper()
        .replace(" ", "_")
        .replace("-", "_")
    )


def get_subpackages_names(package: ModuleType) -> List[str]:
    pkg_path = package.__path__
    return [name for _, name, is_pkg in iter_modules(pkg_path) if is_pkg]


def get_modules_with_page_objects(
    package: ModuleType
) -> Dict[str, ModuleType]:
    subpackages_names = get_subpackages_names(package)
    result = {}
    root_prefix = f"{package.__name__}."
    root_path = package.__path__[0]
    for subpackage_name in subpackages_names:
        subpackage_path = os.path.join(root_path, subpackage_name)
        for _, module_name, is_pkg in iter_modules([subpackage_path]):
            module_path = f"{root_prefix}{subpackage_name}.{module_name}"
            if not is_pkg:
                module = import_module(module_path)
                if is_page_object(module):
                    enum_key = get_enum_key(module)
                    result[enum_key] = module
    return result
