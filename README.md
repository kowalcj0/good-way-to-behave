Good Way to Behave
------------------

Demo project that uses Python [Behave](https://pythonhosted.org/behave/) and [Selenium](https://selenium-python.readthedocs.io/) to
run functional tests in browsers.


# Requirements

* python 3.6+
* pip
* appropriate [browser driver binaries](https://selenium-python.readthedocs.io/installation.html#drivers) installed in `$PATH`

Then: `pip install -r requirements.txt`


# Worth watching

* Stop writing classes by Jack Diederich (PyCon2012)
    * https://www.youtube.com/watch?v=o9pEzgHorH0
* User Centred Scenarios by Antony Marcano & James Martin (CukeUp2012)
    * https://skillsmatter.com/skillscasts/3141-user-centred-scenarios-describing-capabilities-not-solutions


# Run tests

```shell
make tests
```


# Reproducing a bug (running tests by tag)

```shell
make reproduce ticket={TICKET_NUMBER}
```
