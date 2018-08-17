Feature: Search using SearX

  @wip
  @TICKET-003
  @search
  @<selected_category>
  Scenario Outline: Users should be able search for "<specific_term>" in "<selected_category>" category
    Given you are on the "SearX - Home" page

    When you enter "<specific_term>" in the "search" field
    And you click on "Advanced settings" button
    And you click on "<selected_category>" button
    And you click on "search" button

    Then you should be on the "SearX - Search Results" page
    Then you should see link to "<expected>" page among search results

    Examples:
      | specific_term | selected_category | expected                                               |
      | pyconpl       | General           | https://pl.pycon.org/                                  |
      | pyconpl       | It                | https://github.com/zefciu/pyramid-concepts             |
      | pyconpl       | Music             | https://www.youtube.com/watch?v=wt6LmnKyAUw            |
      | pyconpl       | Social Media      | https://twitter.com/timosiia/status/899205699737190400 |
      | pyconpl       | Videos            | https://www.youtube.com/user/pyconpl                   |
