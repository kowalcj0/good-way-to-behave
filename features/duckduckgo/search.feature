@duckduckgo
Feature: Search using DuckDuckGo

  @TICKET-011
  @search
  Scenario Outline: Users should be able to find something on "<specific term>" using DuckDuckGo
    Given "Robert" decided to search the Internet using "DuckDuckGo"

    When "Robert" searches for "<specific term>"

    Then "Robert" should see link to "<expected>" page among search results

    Examples:
      | specific term | expected                                 |
      | pyconpl       | https://pl.pycon.org/2018/               |
      | python behave | https://behave.readthedocs.io/en/latest/ |


  @TICKET-022
  @search
  Scenario Outline: Users should be able to continue searching for "<new term>" after they searched for "<specific term>"
    Given "Robert" searched for "<specific term>" using "DuckDuckGo"

    When "Robert" searches for "<new term>"

    Then "Robert" should see link to "<expected>" page among search results

    Examples:
      | specific term | new term | expected                                                  |
      | pyconpl       | searx    | https://asciimoo.github.io/searx/                         |
      | python behave | bdd      | https://en.wikipedia.org/wiki/Behavior-driven_development |


  @TICKET-033
  @search
  @<selected>
  Scenario Outline: Users should be able search for "<specific term>" in "<selected>" category using "DuckDuckGo"
    Given "Robert" decided to search the Internet using "DuckDuckGo"

    When "Robert" searches for "<specific term>" in "<selected>" category

    Then "Robert" should see link to "<expected>" page among search results

    Examples:
      | specific term | selected | expected                                                                          |
      | pyconpl       | News     | http://www.businessinsider.com/rachel-sklar-on-adria-richards-and-sendgrid-2013-3 |
      | pyconpl       | Videos   | https://www.youtube.com/watch?v=aEj8W_K1IFE                                       |
