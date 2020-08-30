#!/usr/bin/env python3
import re
import boto3
import os
from typing import List
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement as web_element
from selenium.webdriver.remote.webdriver import WebDriver as web_driver

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from selenium.common.exceptions import StaleElementReferenceException

FIGSHARE_SEARCH_TERM_URL = "https://figshare.com/search?q=xtc%E2%80%8B%2C%20%E2%80%8Bdcd%2C%E2%80%8B%20%E2%80%8Bntraj%2C%20netcdf%2C%20trr%2C%20lammpstrj%2C%20xyz%2C%20binpos%2C%20hdf5%2C%20dtr%2C%20arc%2C%20tng%2C%20mdcrd%2C%20crd%2C%20dms%2C%20trj%2C%20ent%2C%20ncdf"
FIGSHARE_ARTICLE_JS_QUERY_ARTICLES = "return document.querySelectorAll('div[role=article]')"
FIGSHARE_ARTICLE_JS_QUERY_PAGE_SIZE = "return document.querySelectorAll('span')"
FIGSHARE_ALL_XPATH = ".//*"
FIGSHARE_ANCHOR_XPATH = ".//a"
DEFAULT_IMPLICIT_WAIT_TIME = 30
DEFAULT_SCROLL_DOWN_KEY_PRESSES = 60
PRIMARY_EXEC_LIMIT = 5


DATE_REGEX = r'.*([0-9]{2}[.][0-9]{2}[.][0-9]{4}).*'

from crawler_lib.article import Article, File
from crawler_lib.browser_automation import (
wait_for_actual_article_link,
get_primary_page_article_content_href,
get_primary_page_article_content_text,
get_total_pages_from_spans,
wait_for_article_div,
fetch_all_current_article_elements,
execute_manual_scroll_down,
agree_to_cookies,
BrowserAutomator)

REGION_NAME = os.environ.get('REGION_NAME')
SERVER_SECRET_KEY = os.environ.get('AWS_SERVER_SECRET_KEY')
SERVER_PUBLIC_KEY = os.environ.get('AWS_SERVER_PUBLIC_KEY')
SQS_URL = 'https://sqs.eu-central-1.amazonaws.com/397254617684/crawler_queue'
sqs_client = boto3.client('sqs', region_name='eu-central-1')#,
#                          aws_access_key_id=SERVER_PUBLIC_KEY,
#                          aws_secret_access_key=SERVER_SECRET_KEY,
#                          region_name=REGION_NAME)

BUILD_ATTEMPT_LIMIT = 5

def parse_text_list(text_list: str):
    text = text_list.split('\n')
    if (len(text) == 4):
        article_type = text[0]
        title = text[1]
        posted_on_text = text[2]
        date_match = re.match(DATE_REGEX, posted_on_text)
        author = text[3]
        print("author: " + author)
        article = Article(title=title, upload_date=None if date_match is None else date_match.group(1))
        article.add_author(author)
        return article
    if (len(text) == 3):
        author = text[-1]
        posted_on_text = text[-2]
        date_match = re.match(DATE_REGEX, posted_on_text)
        article = Article(title=text[-3], upload_date=None if date_match is None else date_match.group(1))
        #TODO:FIx authors
        print("author: " + author)
        article.add_author(author)
        return article
    logger.info("no length match for text: ", text)

def build_article_from_element(element):
    current_attempt = 0
    while(current_attempt < 3):
        try:
            text_list = get_primary_page_article_content_text(element)
            href = get_primary_page_article_content_href(element)
            article = parse_text_list(text_list)
            if href.startswith("http"):
                article.source_url = href
            else:
                logger.error("could not add source url from hrefs: " + str(href))
            return article
        except StaleElementReferenceException:
            break
        except Exception as e:
            current_attempt += 1
            logger.error("could not build article from element, error:", e)
            if ('text_list' in locals()):
                logger.info("text list: \n", text_list, "\n\n")

def add_articles_from_page(driver, article_list):
    wait_for_article_div(driver)
    current_articles = fetch_all_current_article_elements(driver)
    for element in current_articles:
        current_element = build_article_from_element(element)
        article_list.append(current_element)
    execute_manual_scroll_down(driver)
    return article_list

def is_same_element_list(existing_list:List[web_element], new_list:List[web_element]):
    return len(existing_list) == len(new_list) and [a for a in existing_list] == [b for b in new_list]

def build_page_article_element_list(driver)->List[web_element]:
    wait_for_article_div(driver)
    return fetch_all_current_article_elements(driver)

def fetch_new_articles(driver, existing_element_list:List[web_element]):
    new_article_list = list()
    is_same_list = True
    while(is_same_list != False):
        element_list = build_page_article_element_list(driver)
        is_same_list = is_same_element_list(existing_element_list,
                               element_list)
        execute_manual_scroll_down(driver)
    driver.implicitly_wait(5)
    logger.info("building new element list")
    new_list = build_page_article_element_list(driver)
    for element in new_list:
        article = build_article_from_element(element)
        new_article_list.append(article)
    return new_article_list

def build_articles(driver, article_list, build_attempts:int):
    current_element_list = build_page_article_element_list(driver)
    articles = fetch_new_articles(driver,
                                  current_element_list)
    missing_articles = len([x for x in articles if x not in article_list])
    logger.info('missing: ' + str(missing_articles))
    if (missing_articles == 0):
        driver.implicitly_wait(30)
        time.sleep(5)
        logger.info("no new articles found, incrementing build attempts")
        build_attempts += 1
        if (build_attempts > BUILD_ATTEMPT_LIMIT):
            logger.info("assuming end of query and continuing")
            return article_list
    for article in articles:
            article_list.append(article)
    logger.info("current article count: " + str(len(article_list)))
    return build_articles(driver, article_list, build_attempts)

def fetch_articles_and_scroll(driver):
    article_list = list()
    ##
    wait_for_article_div(driver)
    agree_to_cookies(driver)
    return build_articles(driver, article_list, 0)

def parse_file_obj(driver):
    file_doi_js_query = "return document.querySelectorAll('div[data-doi]')"
    file_url_js_query = "return document.querySelectorAll('a[class*=download]')"
    file_doi_element_list = driver.execute_script(file_doi_js_query)
    file_url_element_list = driver.execute_script(file_url_js_query)
    file_doi_string = file_doi_element_list[0].get_attribute('data-doi')
    file_url = file_url_element_list[0].get_attribute('href')
    file_name =file_url_element_list[0].text
    return File(file_name=file_name, digital_object_id=file_doi_string, url=file_url)


def parse_keywords(driver):
    keywords = list()
    keyword_js_query = "return document.querySelectorAll('a[href*=keyword]')"
    keyword_element_list = driver.execute_script(keyword_js_query)
    for kw_element in keyword_element_list:
        keywords.append(kw_element.get_attribute('title'))
    return keywords

def parse_parent_article(driver):
    wait_for_actual_article_link(driver)
    actual_article_js_query = "return document.querySelectorAll('a[class*=linkback-url]')"
    article_element_list = driver.execute_script(actual_article_js_query)
    actual_article_title = article_element_list[0].get_attribute('innerHTML')
    actual_article_url = article_element_list[0].get_attribute('href')
    actual_article_doi = actual_article_url.strip("https://doi.org/")
    actual_article = Article(title=actual_article_title,
                             source_url=actual_article_url,
                             digital_object_id=actual_article_doi,
                             published=True, enriched=True)
    return actual_article


def enrich_article(driver, original_article_url):
    try:
        print(driver.execute_script("return document.querySelectorAll('.fs-display > div:nth-child(1)')"))
        file_obj = parse_file_obj(driver)
        file_obj.url = original_article_url
        actual_article = parse_parent_article(driver)
        actual_article.add_file(file_obj)
        for kw in parse_keywords(driver):
            actual_article.add_keyword(kw)
        return actual_article
    except Exception as e:
        logger.info("could not enrich article: ", e)
        return

def fetch_articles():
    browser_automator = BrowserAutomator()
    browser_automator.load_webdriver()
    browser_automator.go_to_page(FIGSHARE_SEARCH_TERM_URL)
    article_list = fetch_articles_and_scroll(browser_automator.web_driver)
    browser_automator.web_driver.implicitly_wait(3)
    browser_automator.close_webdriver()

    article_set = set(article_list)
    logger.info("articles found: " + str(len(article_set)))
    enriched_articles = []
    for article in article_set:
        new_automator = BrowserAutomator()
        new_automator.load_webdriver()
        new_automator.go_to_page(article.source_url)
        wait = WebDriverWait(new_automator.web_driver, 5)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-doi]")))

        try:
            enriched_article = enrich_article(new_automator.web_driver, article.source_url)
            if (enriched_article != None):
                enriched_article.parent_request_url = FIGSHARE_SEARCH_TERM_URL
                enriched_articles.append(enriched_article)
                response = sqs_client.send_message(QueueUrl=SQS_URL, DelaySeconds=0,
                                                   MessageBody=enriched_article.to_json())
            else:
                ##need to handle this properly, this error is mostly due to
                ##files that have no parent article
                article.parent_request_url = FIGSHARE_SEARCH_TERM_URL
                enriched_articles.append(article)
                response = sqs_client.send_message(QueueUrl=SQS_URL, DelaySeconds=0, MessageBody=article.to_json())
            logger.info("response message id: " + response['MessageId'])
            new_automator.close_webdriver()
        except Exception as e:
            print("could not enrich article: " + str(e))
            logger.exception(e)


if __name__ == "__main__":
    fetch_articles()

