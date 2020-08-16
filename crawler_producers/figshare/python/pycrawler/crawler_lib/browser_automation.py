from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        self.web_driver.close()

def agree_to_cookies(driver):
    driver.find_element_by_tag_name('button').send_keys(Keys.RETURN)

def wait_for_article_div(driver):
    wait = WebDriverWait(driver, 5)
    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role=article]")))
    driver.implicitly_wait(3)

def wait_for_actual_article_link(driver):
    wait = WebDriverWait(driver, 3)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[class*=linkback-url]")))

def get_total_pages_from_spans(driver):
    wait_for_article_div(driver)
    span_list = driver.execute_script(FIGSHARE_ARTICLE_JS_QUERY_PAGE_SIZE)
    for span in span_list:
        span_text = span.text
        if 'results found' in span_text:
            return str(span_text).split(' ')[0]

def get_primary_page_article_content_text(element):
    text_list = element.find_element_by_xpath(".//*").text
    return text_list

def get_primary_page_article_content_href(element):
    href_list = element.find_element_by_xpath(".//a").get_attribute("href")
    return href_list

def fetch_all_current_articles(driver):
    return driver.execute_script(FIGSHARE_ARTICLE_JS_QUERY_ARTICLES)


def execute_manual_scroll_down(driver):
    for _ in range(0, DEFAULT_SCROLL_DOWN_KEY_PRESSES):
        driver.find_element_by_tag_name('a').send_keys(Keys.ARROW_DOWN)

##
def create_webdriver():
    # if args.webdriver == "firefox":
    print("starting firefox driver")
    firefox_options = webdriver.FirefoxOptions()
    #firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=firefox_options)
    # elif args.webdriver == "chrome":
    #     print("starting chrome driver")
    #     if args.webdriver_location is None:
    #         print("webdriver file location required, please add...")
    #     chrome_options = webdriver.ChromeOptions()
    #     chrome_options.add_argument('--headless')
    #     chrome_options.add_argument('--no-sandbox')
    #     chrome_options.add_argument('--disable-dev-shm-usage')
    #     #driver = webdriver.Chrome()
    #     driver = webdriver.Chrome(chrome_options=chrome_options)
    # if driver is None:
    #     print("could not build webdriver on localhost")
    return driver






