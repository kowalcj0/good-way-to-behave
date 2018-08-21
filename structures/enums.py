# -*- coding: utf-8 -*-

from enum import Enum
from types import ModuleType
from typing import Dict


class Services(Enum):
    SEARX = "SearX"
    DUCKDUCKGO = "DuckDuckGo"


class PageObjects(Enum):
    """Page Objects enumeration.

    Values can only be modules with properties required for a Page Object.
    """

    def __new__(cls, value: ModuleType):
        required_attr = ["SERVICE", "NAME", "TYPE", "URL", "SELECTORS"]
        has_attributes = all([hasattr(value, prop) for prop in required_attr])
        if not has_attributes:
            raise TypeError(
                "Expected Page Object module but got: {}".format(value)
            )
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __str__(self):
        return "{}-{} [{} - {}]".format(
            self.value.SERVICE,
            self.value.NAME,
            self.value.TYPE,
            self.value.URL,
        )

    @property
    def name(self) -> str:
        return self.value.NAME

    @property
    def service(self) -> str:
        return self.value.SERVICE

    @property
    def type(self) -> str:
        return self.value.TYPE

    @property
    def url(self) -> str:
        return self.value.URL

    @property
    def selectors(self) -> Dict:
        return self.value.SELECTORS
