from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement as web_element, WebElement as WElement
from selenium.webdriver.remote.webdriver import WebDriver as web_driver, WebDriver as WDriver
from typing import List

import logging

LINUX_CHROMEDRIVER_PATH = "/usr/src/app/chromedriver"
FIGSHARE_ARTICLE_JS_QUERY_ARTICLES = "return document.querySelectorAll('div[role=article]')"
DEFAULT_SCROLL_DOWN_KEY_PRESSES = 60

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# TODO: remove unused constant
# DEFAULT_IMPLICIT_WAIT_TIME = 30

class BrowserAutomator(object):
    def __init__(self):
        self.web_driver = None
        self.wait = None

    def load_webdriver(self):
        self.web_driver = self.create_webdriver()

    def go_to_page(self, page: str):
        self.web_driver.get(page)

    def find_tag_and_return(self, tag: str):
        self.web_driver.find_element_by_tag_name(tag).send_keys(Keys.RETURN)

    def wait_for_article_by_selector(self, selector: str):
        self.wait = WebDriverWait(self.web_driver, 5)
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def scroll_down_by_tag_name(self, tag_name: str):
        self.web_driver.find_element_by_tag_name(tag_name).send_keys(Keys.ARROW_DOWN)

    def close_webdriver(self):
        print("closing webdriver")
        self.web_driver.quit()

    def get_webdriver(self):
        return self.web_driver

    def create_webdriver(self) -> web_driver:
        import os
        if os.path.isfile(LINUX_CHROMEDRIVER_PATH):
            print("starting chrome driver")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            return webdriver.Chrome(LINUX_CHROMEDRIVER_PATH, chrome_options=chrome_options)
        print("starting firefox driver")
        firefox_options = webdriver.FirefoxOptions()
        # firefox_options.add_argument('--headless')
        return webdriver.Firefox(firefox_options=firefox_options)


class FigshareBrowserAutomator(BrowserAutomator):
    def __init__(self):
        super().__init__()

    def agree_to_cookies(self) -> None:
        self.web_driver.find_element_by_tag_name('button').send_keys(Keys.RETURN)

    def wait_for_article_div(self) -> None:
        wait = WebDriverWait(self.web_driver, 5)
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role=article]")))
        self.web_driver.implicitly_wait(3)

    def wait_for_child_article_link(self) -> None:
        wait = WebDriverWait(self.web_driver, 3)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[class*=linkback-url]")))

    def fetch_all_current_article_elements(self) -> List[web_element]:
        return self.web_driver.execute_script(FIGSHARE_ARTICLE_JS_QUERY_ARTICLES)

    def execute_manual_scroll_down(self) -> None:
        for _ in range(0, DEFAULT_SCROLL_DOWN_KEY_PRESSES):
            self.web_driver.find_element_by_tag_name('a').send_keys(Keys.ARROW_DOWN)

    def build_page_article_element_list(self) -> List[WElement]:
        self.wait_for_article_div()
        return self.fetch_all_current_article_elements()


def wait_for_article_div(driver) -> None:
    wait = WebDriverWait(driver, 5)
    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role=article]")))
    driver.implicitly_wait(3)


def wait_for_child_article_link(driver) -> None:
    wait = WebDriverWait(driver, 3)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[class*=linkback-url]")))

# def fetch_all_current_article_elements(driver) -> List[web_element]:
#    return driver.execute_script(FIGSHARE_ARTICLE_JS_QUERY_ARTICLES)
#
#
# def execute_manual_scroll_down(driver) -> None:
#    for _ in range(0, DEFAULT_SCROLL_DOWN_KEY_PRESSES):
#        driver.find_element_by_tag_name('a').send_keys(Keys.ARROW_DOWN)
#
#
# def build_page_article_element_list(driver: WDriver) -> List[WElement]:
#    wait_for_article_div(driver)
#    return fetch_all_current_article_elements(driver)
#
