# -*- coding: utf-8 -*-

from collections import namedtuple

ScenarioData = namedtuple("ScenarioData", ["actors"])

Actor = namedtuple("Actor", ["alias", "email", "password", "visited_page"])

Selector = namedtuple(
    "Selector",
    ["name", "by", "value", "in_desktop", "in_mobile", "in_horizontal"],
)

# define default values
ScenarioData.__new__.__defaults__ = ({},)
Actor.__new__.__defaults__ = (None,) * len(Actor._fields)
Selector.__new__.__defaults__ = (None, None, True, True, True)
