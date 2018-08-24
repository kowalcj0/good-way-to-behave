@searx
Feature: Search using SearX

  @TICKET-001
  @search
  Scenario Outline: Users should be able to find something on "<specific term>" using SearX
    Given "Robert" decided to search the Internet using "SearX"

    When "Robert" searches for "<specific term>"

    Then "Robert" should see link to "<expected>" page among search results

    Examples:
      | specific term | expected                                 |
      | pyconpl       | https://pl.pycon.org/                    |
      | python behave | https://behave.readthedocs.io/en/latest/ |


  @TICKET-002
  @search
  Scenario Outline: Users should be able to continue searching for "<new term>" after they searched for "<specific term>" using SearX
    Given "Robert" searched for "<specific term>" using "SearX"

    When "Robert" searches for "<new term>"

    Then "Robert" should see link to "<expected>" page among search results

    Examples:
      | specific term | new term | expected                                                  |
      | pyconpl       | searx    | https://asciimoo.github.io/searx/                         |
      | python behave | bdd      | https://en.wikipedia.org/wiki/Behavior-driven_development |


  @TICKET-003
  @search
  @<selected>
  Scenario Outline: Users should be able search for "<specific term>" in "<selected>" category using SearX
    Given "Robert" decided to search the Internet using "SearX"

    When "Robert" searches for "<specific term>" in "<selected>" category

    Then "Robert" should see link to "<expected>" page among search results

    @bug
    @TICKET-222
    @fixed
    Examples:
      | specific term | selected     | expected                                               |
      | pyconpl       | General      | https://pl.pycon.org/                                  |
      | pyconpl       | It           | https://github.com/zefciu/pyramid-concepts             |
      | pyconpl       | Videos       | https://www.youtube.com/user/pyconpl                   |
      | pyconpl       | Social Media | https://twitter.com/timosiia/status/899205699737190400 |

    @bug
    @TICKET-222
    @fixme
    Examples: no search results or unreliable search in following categories
      | specific term | selected | expected                                    |
      | pyconpl       | Music    | https://www.youtube.com/watch?v=wt6LmnKyAUw |
      | pyconpl       | Files    | https://pl.pycon.org/                       |
      | pyconpl       | Images   | https://pl.pycon.org/                       |
      | pyconpl       | Map      | https://pl.pycon.org/                       |
      | pyconpl       | News     | https://pl.pycon.org/                       |
      | pyconpl       | Science  | https://pl.pycon.org/                       |
