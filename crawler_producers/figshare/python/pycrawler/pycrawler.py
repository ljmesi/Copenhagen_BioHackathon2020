#!/usr/bin/env python3
from typing import List

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement as WElement
from selenium.webdriver.remote.webdriver import WebDriver as WDriver
from selenium.common.exceptions import TimeoutException

import logging

from crawler_lib.webparser import FigshareWebParser

FETCH_LIMIT = 10
BUILD_ATTEMPT_LIMIT = 5

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

FIGSHARE_SEARCH_TERM_URL = "https://figshare.com/search?q=xtc%E2%80%8B%2C%20%E2%80%8Bdcd%2C%E2%80%8B%20%E2%80%8Bntraj%2C%20netcdf%2C%20trr%2C%20lammpstrj%2C%20xyz%2C%20binpos%2C%20hdf5%2C%20dtr%2C%20arc%2C%20tng%2C%20mdcrd%2C%20crd%2C%20dms%2C%20trj%2C%20ent%2C%20ncdf"

from crawler_lib.article import Article
from crawler_lib.browser_automation import FigshareBrowserAutomator
from crawler_lib.article_producer import FigshareArticleProducer

def is_same_element_list(existing_list: List[WElement], new_list: List[WElement]):
    return len(existing_list) == len(new_list) and [a for a in existing_list] == [b for b in new_list]

def fetch_new_articles(browser_automator: FigshareBrowserAutomator, existing_element_list: List[WElement]):
    new_article_list = list()
    is_same_list = True
    figshare_parser = FigshareWebParser()
    while is_same_list != False:
        element_list = browser_automator.build_page_article_element_list()
        is_same_list = is_same_element_list(existing_element_list,
                                            element_list)
        browser_automator.execute_manual_scroll_down()
    browser_automator.web_driver.implicitly_wait(5)
    log.info("building new element list")
    new_list = browser_automator.build_page_article_element_list()
    for element in new_list:
        article = figshare_parser.build_article_from_element(element)
        if article is not None:
            new_article_list.append(article)
    return new_article_list


def build_articles(browser_automator: FigshareBrowserAutomator, article_list, build_attempts: int) -> List[Article]:
    limit = FETCH_LIMIT
    current_element_list = browser_automator.build_page_article_element_list()
    articles = fetch_new_articles(browser_automator,
                                  current_element_list)
    missing_articles = len([x for x in articles if x not in article_list])
    log.info('missing: ' + str(missing_articles))
    if missing_articles == 0:
        browser_automator.web_driver.implicitly_wait(30)
        log.info("no new articles found, incrementing build attempts")
        build_attempts += 1
        if build_attempts > BUILD_ATTEMPT_LIMIT:
            log.info("assuming end of query and continuing")
            return article_list
    if len(article_list) >= limit:
        log.info("article list exeeds " + str(limit) + " continuing")
        return article_list
    for article in articles:
        article_list.append(article)
    log.info("current article count: " + str(len(article_list)))
    return build_articles(browser_automator, article_list, build_attempts)


def fetch_articles_and_scroll(browser_automator: FigshareBrowserAutomator) -> List[Article]:
    article_list = list()
    ##
    browser_automator.wait_for_article_div()
    browser_automator.agree_to_cookies()
    return build_articles(browser_automator, article_list, 0)


def enrich_article(driver: WDriver, original_article_url: str) -> Article:
    log.info("starting enrich article")
    try:
        figshare_parser = FigshareWebParser()
        # TODO: parse pre formatted text
        # print(driver.execute_script("return document.querySelectorAll('.fs-display > div:nth-child(1)')"))
        child_article = figshare_parser.parse_parent_article(driver)
        if child_article != None:
          log.info("child article built: " + str(child_article.to_json()))
          file_obj_list = figshare_parser.parse_file_obj(driver)
          log.info("file_obj list size: " + str(len(file_obj_list)))
          if file_obj_list:
              log.info("files found in article")
              for file_obj in file_obj_list:
                  file_obj.refering_url = original_article_url
                  child_article.add_file(file_obj)
                  for kw in figshare_parser.parse_keywords(driver):
                      child_article.add_keyword(kw)
                  for fkw in file_obj._keywords:
                      child_article.add_keyword(fkw)
          return child_article
    except TimeoutException:
        log.info("timeout exception reached")
    except Exception as e:
        log.info("could not enrich article", exc_info=True)
    log.info("endinging enrich article")


def enrich_and_send_article(article: Article,
                            processed_articles: List[Article]):
    browser_automator = FigshareBrowserAutomator()
    browser_automator.load_webdriver()
    log.info("parsing secondary page")
    browser_automator.go_to_page(article.source_url)
    wait = WebDriverWait(browser_automator.web_driver, 5)
    producer = FigshareArticleProducer()
    try:
        log.info("wating for css selector")
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-doi]")))
        enriched_article = enrich_article(browser_automator.web_driver, article.source_url)
        log.info("enriched article: " + enriched_article.to_json())
        send(article if enriched_article == None else enriched_article,
             processed_articles, producer)
    except TimeoutException as er:
        log.info("timeout exception reached")
    except Exception as e:
        log.info("could not enrich article", exc_info=True)
    producer.close_client()
    browser_automator.close_webdriver()

def send(article, processed_articles: List[Article],
         producer: FigshareArticleProducer):
    article.parent_request_url = FIGSHARE_SEARCH_TERM_URL
    processed_articles.append(article)
    response = producer.send_article(article)
    log.info("response message id: " + response['MessageId'])

def fetch_articles() -> None:
    browser_automator = FigshareBrowserAutomator()
    browser_automator.load_webdriver()
    browser_automator.go_to_page(FIGSHARE_SEARCH_TERM_URL)
    article_list = fetch_articles_and_scroll(browser_automator)
    browser_automator.web_driver.implicitly_wait(3)
    log.info("closing main browser")
    browser_automator.close_webdriver()

    article_set = set(article_list)
    log.info("article set to enrich: " + str(len(article_set)))
    enriched_articles = []
    articles_sent = 0
    for article in article_set:
        enrich_and_send_article(article, enriched_articles)
        articles_sent += 1
        log.info("finished parsing secondary page, articles sent: " + str(articles_sent))

if __name__ == "__main__":
    fetch_articles()
