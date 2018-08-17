# -*- coding: utf-8 -*-
import logging
from types import ModuleType

import pages
from pages.common import get_modules_with_page_objects
from structures.enums import PageObjects


PAGES = PageObjects("PageObjects", names=get_modules_with_page_objects(pages))


def get_page_object(service_and_page: str) -> ModuleType:
    assert (
        " - " in service_and_page
    ), f"Invalid Service & Page name: {service_and_page}"
    parts = service_and_page.split(" - ")
    sought_service = parts[0]
    sought_page = parts[1]
    result = None
    for page_object in PAGES.__members__.values():
        if sought_service.lower() == page_object.service.lower():
            if hasattr(page_object.value, "NAMES"):
                names = page_object.value.NAMES
                if sought_page.lower() in [name.lower() for name in names]:
                    result = page_object.value
                    break
            else:
                if sought_page.lower() == page_object.name.lower():
                    result = page_object.value
                    break

    if not result:
        service_key = sought_service.replace(" ", "_").upper()
        keys = [
            key
            for key in PAGES.__members__.keys()
            if key.startswith(service_key)
        ]
        raise KeyError(
            f"Could not find Page Object for '{sought_page}' in "
            f"'{sought_service}' package. Here's a list of available Page "
            f"Objects: {keys}"
        )
    logging.debug(f"Found PageObject for: {service_and_page} → {result}")
    return result
