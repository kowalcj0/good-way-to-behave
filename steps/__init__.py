# -*- coding: utf-8 -*-

from types import ModuleType


def has_action(page: ModuleType, name: str):
    assert hasattr(
        page, name
    ), f"{page.SERVICE} - {page.NAME} has no '{name}' action"
