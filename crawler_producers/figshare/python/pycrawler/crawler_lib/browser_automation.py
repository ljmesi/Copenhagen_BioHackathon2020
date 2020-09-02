from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement as web_element
from selenium.webdriver.remote.webdriver import WebDriver as web_driver
from typing import List


import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

FIGSHARE_ARTICLE_JS_QUERY_ARTICLES = "return document.querySelectorAll('div[role=article]')"
FIGSHARE_ARTICLE_JS_QUERY_PAGE_SIZE = "return document.querySelectorAll('span')"
DEFAULT_SCROLL_DOWN_KEY_PRESSES = 60

class BrowserAutomator(object):
    def __init__(self):
        self.web_driver = None
        self.wait = None

    def load_webdriver(self):
        self.web_driver = create_webdriver()

    def go_to_page(self, page:str):
        self.web_driver.get(page)

    def find_tag_and_return(self, tag:str):
        self.web_driver.find_element_by_tag_name(tag).send_keys(Keys.RETURN)

    def wait_for_article_by_selector(self, selector:str):
        self.wait = WebDriverWait(self.web_driver, 5)
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def scroll_down_by_tag_name(self, tag_name:str):
        self.web_driver.find_element_by_tag_name(tag_name).send_keys(Keys.ARROW_DOWN)

    def close_webdriver(self):
        self.web_driver.quit()

def agree_to_cookies(driver)->None:
    driver.find_element_by_tag_name('button').send_keys(Keys.RETURN)

def wait_for_article_div(driver)->None:
    wait = WebDriverWait(driver, 5)
    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role=article]")))
    driver.implicitly_wait(3)

def wait_for_actual_article_link(driver)->None:
    wait = WebDriverWait(driver, 3)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[class*=linkback-url]")))

def get_total_pages_from_spans(driver)->str:
    wait_for_article_div(driver)
    span_list = driver.execute_script(FIGSHARE_ARTICLE_JS_QUERY_PAGE_SIZE)
    for span in span_list:
        span_text = span.text
        if 'results found' in span_text:
            return str(span_text).split(' ')[0]

def get_primary_page_article_content_text(element:web_element)->List[str]:
    text = element.find_element_by_xpath(".//*").text
    text_list = text.split('\n')
    return text_list

def get_primary_page_article_content_href(element:web_element)->str:
    return element.find_element_by_xpath(".//a").get_attribute("href")

def fetch_all_current_article_elements(driver)->List[web_element]:
    return driver.execute_script(FIGSHARE_ARTICLE_JS_QUERY_ARTICLES)


def execute_manual_scroll_down(driver)->None:
    for _ in range(0, DEFAULT_SCROLL_DOWN_KEY_PRESSES):
        driver.find_element_by_tag_name('a').send_keys(Keys.ARROW_DOWN)

##
def create_webdriver()->web_driver:
    import os
    if os.path.isfile("/usr/src/app/chromedriver"):
         print("starting chrome driver")
         chrome_options = webdriver.ChromeOptions()
         chrome_options.add_argument('--headless')
         chrome_options.add_argument('--no-sandbox')
         chrome_options.add_argument('--disable-dev-shm-usage')
         return webdriver.Chrome("/usr/src/app/chromedriver", chrome_options=chrome_options)
    print("starting firefox driver")
    firefox_options = webdriver.FirefoxOptions()
    #firefox_options.add_argument('--headless')
    return webdriver.Firefox(firefox_options=firefox_options)
