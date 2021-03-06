# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging
import socket
import time

from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry
from behave.model import Feature, Scenario, Step
from behave.runner import Context
from retrying import retry
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from pages.common import (
    clear_driver_cookies,
    initialize_scenario_data,
    show_snackbar_message,
)
from settings import AUTO_RETRY, CONFIG, RESTART_BROWSER, TASK_ID

try:
    import http.client as httplib
except ImportError:  # above is available in py3+, below is py2.7
    import httplib as httplib


def start_driver_session(context: Context, session_name: str):
    remote_desired_capabilities = context.remote_desired_capabilities
    remote_desired_capabilities["name"] = session_name
    local_desired_capabilities = context.local_desired_capabilities
    if CONFIG["hub_url"]:
        context.driver = webdriver.Remote(
            desired_capabilities=remote_desired_capabilities,
            command_executor=CONFIG["hub_url"],
        )
    else:
        browser_name = CONFIG["environments"][0]["browser"]
        drivers = {
            "chrome": webdriver.Chrome,
            "edge": webdriver.Edge,
            "firefox": webdriver.Firefox,
            "ie": webdriver.Ie,
            "phantomjs": webdriver.PhantomJS,
            "safari": webdriver.Safari,
        }
        print("Starting local instance of {}".format(browser_name))
        if local_desired_capabilities:
            print(
                "Will use following browser capabilities: {}".format(
                    local_desired_capabilities
                )
            )
            if browser_name.lower() in ["firefox", "edge", "ie"]:
                context.driver = drivers[browser_name.lower()](
                    capabilities=local_desired_capabilities
                )
            elif browser_name.lower() in ["chrome", "phantomjs", "safari"]:
                context.driver = drivers[browser_name.lower()](
                    desired_capabilities=local_desired_capabilities
                )
        else:
            print("Will use default browser capabilities")
            context.driver = drivers[browser_name.lower()]()
    context.driver.set_page_load_timeout(time_to_wait=27)
    try:
        context.driver.maximize_window()
        logging.debug("Maximized the window.")
    except WebDriverException:
        logging.debug("Failed to maximize the window.")
        try:
            context.driver.set_window_size(1600, 1200)
            logging.warning("Set window size to 1600x1200")
        except WebDriverException:
            logging.warning("Failed to set window size, will continue as is")
    logging.debug("Browser Capabilities: %s", context.driver.capabilities)


def before_step(context: Context, step: Step):
    logging.debug("Started Step: %s %s", step.step_type, str(repr(step.name)))


def after_step(context: Context, step: Step):
    logging.debug("Finished Step: %s %s", step.step_type, str(repr(step.name)))
    logging.debug("Step Duration: %s %s", str(repr(step.name)), step.duration)
    if RESTART_BROWSER == "scenario":
        if step.status == "failed":
            message = "Step '%s %s' failed. Reason: '%s'" % (
                step.step_type,
                step.name,
                step.exception,
            )
            logging.error(message)
            logging.debug(context.scenario_data)


def before_feature(context: Context, feature: Feature):
    """Use auto-retry feature of upcoming Behave 1.2.6 which automatically
    retries failing scenarios.
    Here PR for it https://github.com/behave/behave/pull/328
    """
    if AUTO_RETRY:
        for scenario in feature.scenarios:
            patch_scenario_with_autoretry(scenario, max_attempts=2)
    if RESTART_BROWSER == "feature":
        start_driver_session(context, feature.name)


def after_feature(context: Context, feature: Feature):
    if RESTART_BROWSER == "feature":
        if hasattr(context, "driver"):
            logging.debug("QUIT DRIVER AFTER FEATURE: %s", feature.name)
            context.driver.quit()


@retry(stop_max_attempt_number=3)
def before_scenario(context: Context, scenario: Scenario):
    logging.debug("Starting scenario: %s", scenario.name)
    message = f"Start: {scenario.name} | {scenario.filename}:{scenario.line}"
    context.scenario_data = initialize_scenario_data()
    if RESTART_BROWSER == "scenario":
        start_driver_session(context, scenario.name)
    if hasattr(context, "driver"):
        show_snackbar_message(context.driver, message)


def after_scenario(context: Context, scenario: Scenario):
    logging.debug("Closing Selenium Driver after scenario: %s", scenario.name)
    logging.debug(context.scenario_data)

    if hasattr(context, "driver"):
        message = f"End: {scenario.name} | {scenario.filename}:{scenario.line}"
        show_snackbar_message(context.driver, message)
        # in order to show the snackbar message after scenario, an explicit
        # wait has to executed
        time.sleep(0.2)

        if RESTART_BROWSER == "scenario":
            context.driver.quit()
        if RESTART_BROWSER == "feature":
            clear_driver_cookies(context.driver)
    else:
        logging.warning(
            "Context does not have Selenium 'driver' object. This might be "
            "happen when it wasn't initialized properly"
        )

    if scenario.status == "failed":
        if hasattr(context, "driver"):
            from selenium.webdriver.remote.command import Command

            try:
                context.driver.execute(Command.STATUS)
            except (socket.error, httplib.CannotSendRequest):
                message = (
                    "Remote driver is unresponsive after scenario: %s. Will"
                    " try to recover selenium session" % scenario.name
                )
                print(message)
                start_driver_session(
                    context, "session-recovered-after-scenario"
                )


def before_all(context: Context):
    remote_desired_capabilities = CONFIG["environments"][TASK_ID]
    local_desired_capabilities = CONFIG["capabilities"]

    for key in CONFIG["capabilities"]:
        if key not in remote_desired_capabilities:
            remote_desired_capabilities[key] = CONFIG["capabilities"][key]

    context.remote_desired_capabilities = remote_desired_capabilities
    context.local_desired_capabilities = local_desired_capabilities
    context.config.setup_logging(configfile=".behave_logging")
