import time
from hashlib import sha256

from selenium.webdriver.remote.webdriver import WebDriver


class WaitForPageLoadAfterAction(object):
    """Context manager for waiting the page to load.
    Proved to be a more reliable than wait_for_page_load() ^^^
    src:
    http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
    https://www.develves.net/blogs/asd/2017-03-04-selenium-waiting-for-page-load/
    """

    def __init__(self, driver: WebDriver, *, timeout: int = 3):
        self.driver = driver
        self.timeout = timeout

    def __enter__(self):
        self.old_id = self.driver.find_element_by_tag_name("html").id
        self.old_hash = sha256(self.driver.page_source.encode('utf-8')).hexdigest()

    def page_has_loaded(self):
        new_page = self.driver.find_element_by_tag_name("html")
        new_hash = sha256(self.driver.page_source.encode('utf-8')).hexdigest()
        ids_dont_match = new_page.id != self.old_id
        hashes_dont_match = new_hash != self.old_hash
        return ids_dont_match and hashes_dont_match

    def __exit__(self, *_):
        self.wait_for(self.page_has_loaded, timeout=self.timeout)

    @staticmethod
    def wait_for(condition_function, timeout: int = 3):
        start_time = time.time()
        while time.time() < start_time + timeout:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception(
            "Timeout waiting for {}".format(condition_function.__name__)
        )
