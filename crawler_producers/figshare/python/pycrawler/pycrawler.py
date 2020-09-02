#!/usr/bin/env python3
import re
import boto3
import os
from typing import List

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement as web_element
from selenium.webdriver.remote.webdriver import WebDriver as web_driver
from selenium.common.exceptions import TimeoutException

import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

from selenium.common.exceptions import StaleElementReferenceException

FIGSHARE_SEARCH_TERM_URL = "https://figshare.com/search?q=xtc%E2%80%8B%2C%20%E2%80%8Bdcd%2C%E2%80%8B%20%E2%80%8Bntraj%2C%20netcdf%2C%20trr%2C%20lammpstrj%2C%20xyz%2C%20binpos%2C%20hdf5%2C%20dtr%2C%20arc%2C%20tng%2C%20mdcrd%2C%20crd%2C%20dms%2C%20trj%2C%20ent%2C%20ncdf"
JS_QUERYSELECTOR = "return document.querySelectorAll('{selector}')"
FIGSHARE_ARTICLE_JS_QUERY_ARTICLES = JS_QUERYSELECTOR.format(selector='div[role=article]')
FIGSHARE_ARTICLE_JS_QUERY_PAGE_SIZE = JS_QUERYSELECTOR.format(selector='span')
FIGSHARE_PARENT_ARTICLE_QUERY = JS_QUERYSELECTOR.format(selector='a[class*=linkback-url]')
FIGSHARE_KEYWORD_QUERY = JS_QUERYSELECTOR.format(selector='a[href*=keyword]')
FIGSHARE_DOCUMENT_QUERY = JS_QUERYSELECTOR.format(selector='a[class*=download]')
FIGSHARE_DOI_QUERY = JS_QUERYSELECTOR.format(selector='div[data-doi]')
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
    wait_for_article_div,
    fetch_all_current_article_elements,
    execute_manual_scroll_down,
    agree_to_cookies,
    BrowserAutomator)

REGION_NAME = os.environ.get('REGION_NAME')
SERVER_SECRET_KEY = os.environ.get('AWS_SERVER_SECRET_KEY')
SERVER_PUBLIC_KEY = os.environ.get('AWS_SERVER_PUBLIC_KEY')
SQS_URL = 'https://sqs.eu-central-1.amazonaws.com/397254617684/crawler_queue'
sqs_client = boto3.client('sqs', region_name='eu-central-1')  # ,
#                          aws_access_key_id=SERVER_PUBLIC_KEY,
#                          aws_secret_access_key=SERVER_SECRET_KEY,
#                          region_name=REGION_NAME)


BUILD_ATTEMPT_LIMIT = 5


def parse_upload_date(date_text: str) -> str:
    date_match = re.match(DATE_REGEX, date_text)
    return None if date_match is None else date_match.group(1)


def parse_text_list(text_list: List[str]):
    if (len(text_list) == 4):
        article_type = text_list[0]
        title = text_list[1]
        posted_on_text = text_list[2]
        author = text_list[3]
        log.info("author from 4 list found: " + author)
        article = Article(title=title,
                          upload_date=parse_upload_date(posted_on_text),
                          authors=[author])
        log.info("current author list: " + str(article.authors))
        return article
    if (len(text_list) == 3):
        author = text_list[-1]
        posted_on_text = text_list[-2]
        log.info("author from 3 list found: " + author)
        article = Article(title=text_list[-3],
                          upload_date=parse_upload_date(posted_on_text),
                          authors=[author])
        log.info("current author list: " + str(article.authors))
        return article
    if (len(text_list) >= 5):
        author = text_list[-1]
        posted_on_text = text_list[-2]
        log.info("author from 3 list found: " + author)
        article = Article(title=text_list[-3],
                          upload_date=parse_upload_date(posted_on_text),
                          authors=[author])
        log.info("current author list: " + str(article.authors))
        return article
    log.info("no length match for text: ", text_list)


def build_article_from_element(element):
    current_attempt = 0
    while (current_attempt < 3):
        try:
            text_list = get_primary_page_article_content_text(element)
            href = get_primary_page_article_content_href(element)
            article = parse_text_list(text_list)
            if article and href and href.startswith("http"):
                article.source_url = href
                return article
            else:
                log.error("could not add source url ")
        except StaleElementReferenceException:
            break
        except Exception as e:
            current_attempt += 1
            log.error("could not build article from element", exc_info=True)
            if ('text_list' in locals()):
                log.info("text list: \n", text_list, "\n\n")


def is_same_element_list(existing_list: List[web_element], new_list: List[web_element]):
    return len(existing_list) == len(new_list) and [a for a in existing_list] == [b for b in new_list]


def build_page_article_element_list(driver: web_driver) -> List[web_element]:
    wait_for_article_div(driver)
    return fetch_all_current_article_elements(driver)


def fetch_new_articles(driver: web_driver, existing_element_list: List[web_element]):
    new_article_list = list()
    is_same_list = True
    while (is_same_list != False):
        element_list = build_page_article_element_list(driver)
        is_same_list = is_same_element_list(existing_element_list,
                                            element_list)
        execute_manual_scroll_down(driver)
    driver.implicitly_wait(5)
    log.info("building new element list")
    new_list = build_page_article_element_list(driver)
    for element in new_list:
        article = build_article_from_element(element)
        if (article is not None):
            new_article_list.append(article)
    return new_article_list


def build_articles(driver: web_driver, article_list, build_attempts: int) -> List[Article]:
    limit = 2000
    current_element_list = build_page_article_element_list(driver)
    articles = fetch_new_articles(driver,
                                  current_element_list)
    missing_articles = len([x for x in articles if x not in article_list])
    log.info('missing: ' + str(missing_articles))
    if (missing_articles == 0):
        driver.implicitly_wait(30)
        log.info("no new articles found, incrementing build attempts")
        build_attempts += 1
        if (build_attempts > BUILD_ATTEMPT_LIMIT):
            log.info("assuming end of query and continuing")
            return article_list
    if (len(article_list) >= limit):
        log.info("article list exeeds " + str(limit) + " continuing")
        return article_list
    for article in articles:
        article_list.append(article)
    log.info("current article count: " + str(len(article_list)))
    return build_articles(driver, article_list, build_attempts)


def fetch_articles_and_scroll(driver: web_driver) -> List[Article]:
    article_list = list()
    ##
    wait_for_article_div(driver)
    agree_to_cookies(driver)
    return build_articles(driver, article_list, 0)


def parse_file_obj(driver: web_driver) -> File:
    try:
        file_doi_js_query = FIGSHARE_DOI_QUERY
        file_url_js_query = FIGSHARE_DOCUMENT_QUERY
        file_doi_element_list = driver.execute_script(file_doi_js_query)
        file_url_element_list = driver.execute_script(file_url_js_query)
        file_doi_string = file_doi_element_list[0].get_attribute('data-doi')
        file_url = file_url_element_list[0].get_attribute('href')
        file_name = file_url_element_list[0].text
        return File(file_name=file_name, digital_object_id=file_doi_string, url=file_url)
    except Exception as e:
        log.info("could not parse file object attribute from element", exc_info=True)


def parse_keywords(driver: web_driver) -> List[str]:
    keywords = list()
    keyword_js_query = FIGSHARE_KEYWORD_QUERY
    keyword_element_list = driver.execute_script(keyword_js_query)
    for kw_element in keyword_element_list:
        keywords.append(kw_element.get_attribute('title'))
    return keywords


def parse_parent_article(driver: web_driver) -> Article:
    wait_for_actual_article_link(driver)
    actual_article_js_query = FIGSHARE_PARENT_ARTICLE_QUERY
    article_element_list = driver.execute_script(actual_article_js_query)
    actual_article_title = article_element_list[0].get_attribute('innerHTML')
    actual_article_url = article_element_list[0].get_attribute('href')
    actual_article_doi = actual_article_url.strip("https://doi.org/")
    actual_article = Article(title=actual_article_title,
                             source_url=actual_article_url,
                             digital_object_id=actual_article_doi,
                             published=True, enriched=True)
    return actual_article


def enrich_article(driver: web_driver, original_article_url: str) -> Article:
    log.info("starting enrich article")
    try:
        # TODO: parse pre formatted text
        # print(driver.execute_script("return document.querySelectorAll('.fs-display > div:nth-child(1)')"))
        file_obj = parse_file_obj(driver)
        if file_obj:
            file_obj.url = original_article_url
            actual_article = parse_parent_article(driver)
            actual_article.add_file(file_obj)
            for kw in parse_keywords(driver):
                actual_article.add_keyword(kw)
            return actual_article
    except TimeoutException as er:
        log.info("timeout exception reached")
    except Exception as e:
        log.info("could not enrich article", exc_info=True)
    log.info("endinging enrich article")


def parse_and_send_page(article: Article, enriched_articles: List[Article]):
    browser_automator = BrowserAutomator()
    browser_automator.load_webdriver()
    log.info("parsing secondary page")
    browser_automator.go_to_page(article.source_url)
    wait = WebDriverWait(browser_automator.web_driver, 3)
    try:
        log.info("wating for css selector")
        wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-doi]")))
        enriched_article = enrich_article(browser_automator.web_driver, article.source_url)
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
        log.info("response message id: " + response['MessageId'])
    except TimeoutException as er:
        log.info("timeout exception reached")
    except Exception as e:
        log.info("could not enrich article", exc_info=True)
    browser_automator.close_webdriver()


def fetch_articles() -> None:
    browser_automator = BrowserAutomator()
    browser_automator.load_webdriver()
    browser_automator.go_to_page(FIGSHARE_SEARCH_TERM_URL)
    article_list = fetch_articles_and_scroll(browser_automator.web_driver)
    browser_automator.web_driver.implicitly_wait(3)
    log.info("closing main browser")
    browser_automator.close_webdriver()

    article_set = set(article_list)
    log.info("article set to enrich: " + str(len(article_set)))
    enriched_articles = []
    articles_sent = 0
    for article in article_set:
        parse_and_send_page(article, enriched_articles)
        articles_sent += 1
        log.info("finished parsing secondary page, articles sent: " +str(articles_sent))



if __name__ == "__main__":
    fetch_articles()
