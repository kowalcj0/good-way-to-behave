# -*- coding: utf-8 -*-
"""Project Settings."""
import os
from datetime import datetime

import config

SEARX_URL = os.environ.get("SEARX_URL", "https://find.kraal.one/")
DUCKDUCKGO_URL = os.environ.get("DUCKDUCKGO_URL", "https://duckduckgo.com/")

# variables set in Paver configuration file
CONFIG_NAME = os.environ.get("CONFIG", "local")
TASK_ID = int(os.environ.get("TASK_ID", 0))

# optional variables set by user
RESTART_BROWSER = os.environ.get("RESTART_BROWSER", "feature")
assert RESTART_BROWSER in ["feature", "scenario"]
BROWSERS = os.environ.get("BROWSERS", "").split()
BROWSERS_VERSIONS = os.environ.get("VERSIONS", "").split()
HUB_URL = os.environ.get("HUB_URL", None)
CAPABILITIES = os.environ.get("CAPABILITIES", None)
BUILD_ID = os.environ.get("CIRCLE_SHA1", str(datetime.date(datetime.now())))

__take_screenshots = os.environ.get("TAKE_SCREENSHOTS", "false")
TAKE_SCREENSHOTS = (
    True
    if __take_screenshots
    and __take_screenshots.lower() in ["true", "1", "yes"]
    else False
)
__auto_retry = os.environ.get("AUTO_RETRY", "true")
AUTO_RETRY = (
    True
    if __auto_retry and __auto_retry.lower() in ["true", "1", "yes"]
    else False
)

if CAPABILITIES:
    import json

    CAPABILITIES = json.loads(CAPABILITIES)

CONFIG = config.get(
    config_file=CONFIG_NAME,
    hub_url=HUB_URL,
    capabilities=CAPABILITIES,
    browsers=BROWSERS,
    versions=BROWSERS_VERSIONS,
    build_id=BUILD_ID,
)
