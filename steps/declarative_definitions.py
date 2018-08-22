# -*- coding: utf-8 -*-
"""Step definitions."""
from behave import given, then, when
from behave.runner import Context

from steps.declarative_implementations import (
    go_to_search_engine,
    search_for,
    should_see_url,
    visit_and_search,
    visit_page,
)


@given('"{actor_alias}" is on the "{page_name}" page')
def given_actor_visits_page(
    context: Context, actor_alias: str, page_name: str
):
    visit_page(context, actor_alias, page_name)


@given('"{actor_alias}" decided to search the Internet using "{search_engine}"')
def given_actor_chose_search_engine(
        context: Context, actor_alias: str, search_engine: str):
    go_to_search_engine(context, actor_alias, search_engine)


@when('"{actor_alias}" searches for "{term}" in "{category}" category')
def step_impl(context: Context, actor_alias: str, term: str, category: str):
    search_for(context, actor_alias, term, category=category)


@when('"{actor_alias}" searches for "{term}"')
def when_actor_searches_for(context: Context, actor_alias: str, term: str):
    search_for(context, actor_alias, term)


@then('"{actor_alias}" should see link to "{url}" page among search results')
def then_should_see_url(context: Context, actor_alias: str, url: str):
    should_see_url(context, actor_alias, url)


@given('"{actor_alias}" searched for "{term}" using "{search_engine}"')
def given_actor_searched_for(
        context: Context, actor_alias: str, term: str, search_engine: str):
    visit_and_search(context, actor_alias, term, search_engine)
