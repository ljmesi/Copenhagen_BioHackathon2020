#!/usr/bin/env python3
import argparse
import json
import re
import traceback
import time
import pandas as pd

import requests
from bs4 import BeautifulSoup
from crawler_lib.study_params import Protien, StudyParameters

FIGSHARE_COOKIE_XPATH = "//a[@class = 'simple-pink-button acceptCookies']"

FIGSHARE_ANCHOR_XPATH = "//a[contains(@href,'https://') and @role = 'button' and @class = '']"

DEFAULT_INFINI_SCROLL_TIMEOUT = 5

DEFAULT_IMPLICIT_WAIT_TIME = 30

FIGSHARE_SELENIUM_LINKS = []


def run(url: str) -> dict:
    messages = []

    initial_response = url_response(messages, url)

    if initial_response is None:
        messages.append("got response of None, exiting")
        return {"messages": messages}

    append_bs_parsing(messages, initial_response)
    append_selenium_parsing(messages, url, args)
    # parse_secondary_link(driver)
    # output_pandas_csv()
    return {"messages": messages}


def append_bs_parsing(messages, initial_response):
    try:
        soup = BeautifulSoup(initial_response.content, "html.parser")
        links = soup.body.findAll("a")
        hrefs = []
        for link in links:
            hrefs.append(link.attrs["href"])

        hrefs_reg = []
        for item in hrefs:
            search_obj = re.search(r"http.*", item, re.I)
            if search_obj:
                hrefs_reg.append(search_obj.group())

        messages.append({"soup": "parsed",
                         "links": hrefs,
                         "urls": hrefs_reg})
    except Exception:
        soup = {"status": "failed to parse"}
        messages.append({"soup": soup, "exception": traceback.format_exc()})


def append_selenium_parsing(messages: list, url: str, args: argparse.Namespace):
    try:
        prepare_selenium_response(url, args)
        messages.append({"selenium": "parsed",
                         "links": FIGSHARE_SELENIUM_LINKS,
                         "total": str(len(FIGSHARE_SELENIUM_LINKS))})
    except:
        selenium = {"status": "failed to parse"}
        messages.append({"selenium": selenium, "exception": traceback.format_exc()})


def prepare_selenium_response(url: str, args: argparse.Namespace) -> None:
    driver = build_webdriver(args)
    driver.get(url)
    driver.implicitly_wait(DEFAULT_IMPLICIT_WAIT_TIME)
    accept_cookies(driver)

    scroll_to_bottom_and_get_links(driver)


def accept_cookies(driver) -> None:
    cookie_string = FIGSHARE_COOKIE_XPATH
    element = driver.find_element_by_xpath(cookie_string)
    if element:
        element.click()


def scroll_to_bottom_and_get_links(driver) -> None:
    seed_height = driver.execute_script("return document.body.scrollHeight")
    scroll_down_finding_links(driver, seed_height)


def update_figshare_links(links_found):
    for link in links_found:
        link_string = link.get_attribute('href')
        if link_string not in FIGSHARE_SELENIUM_LINKS:
            FIGSHARE_SELENIUM_LINKS.append(link_string)


def scroll_down_finding_links(driver, height) -> None:
    driver.execute_script("scroll(0, 250);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    get_links_in_browser(driver, 0)
    print("current links ", len(FIGSHARE_SELENIUM_LINKS))
    executed_height = driver.execute_script("return document.body.scrollHeight")
    if executed_height == height:
        return
    print("scrolling to bottom, current height: {}, previous height: {}".format(executed_height, height))
    time.sleep(DEFAULT_INFINI_SCROLL_TIMEOUT)
    scroll_down_finding_links(driver, executed_height)


def get_links_in_browser(driver, current_attempt: int) -> None:
    try:
        if current_attempt > 10:
            print("giving up!")
            return
        links = driver.find_elements_by_xpath(FIGSHARE_ANCHOR_XPATH)
        if links:
            update_figshare_links(links)
    except Exception as e:
        current_attempt += 1
        error_msg = "could not parse element it on attempt: " \
                    + str(current_attempt) \
                    + ", retrying. error:"
        print(error_msg, str(e))
        get_links_in_browser(driver, current_attempt)


def build_webdriver(args: argparse.Namespace):
    from selenium import webdriver
    driver = None
    if args.webdriver == "firefox":
        print("starting firefox driver")
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--headless')
        driver = webdriver.Firefox()
    elif args.webdriver == "chrome":
        print("starting chrome driver")
        if args.webdriver_location is None:
            print("webdriver file location required, please add...")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(args.webdriver_location, chrome_options=chrome_options)
    if driver is None:
        print("could not build webdriver on localhost")
    return driver


def parse_secondary_link(links: list, browser) -> None:
    print("parsing secondary links")
    links = browser.find_elements_by_xpath(FIGSHARE_ANCHOR_XPATH)
    normal_link_string = "//ul//a[@class = 'normal-link']"
    title_xpath = "//h2[@class = 'title']"
    author_xpath = "//a[@class = 'normal-link author']"
    tag_section_xpath = "//div[@class = 'tags section']//a[@class = 'tag-wrap']"
    if links:
        for link in links:
            study = StudyParameters()
            lnk = link.get_attribute('href')
            browser.get(lnk)
            title = browser.find_element_by_xpath(title_xpath).text  # Extracting tittle of trayectory
            author = browser.find_element_by_xpath(author_xpath).text  # EXtracting the author
            study.add_authors(author)
            study.add_title(title)
            categories = browser.find_elements_by_xpath(normal_link_string)
            for string in categories:
                filtered_string = string.text
                study.add_category(filtered_string)

            keywords_list = []
            tag_section = tag_section_xpath
            keywords = browser.find_elements_by_xpath(tag_section)  # Same that for categories
            for string in keywords:
                filtered_string = string.get_attribute("title")
                keywords_list.append(filtered_string)


def url_response(messages: list, url: str) -> requests.Response:
    try:
        response = requests.get(url, )
        messages.append("request to: url produced: {}".format(url, str(response.status_code)))
        return response
    except Exception as e:
        messages.append("initial request failed, error: {}".format(e))


def output_pandas_csv(data: dict, args) -> None:
    if 'output_location' in args:
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(args.output_location)


def main(args: argparse.Namespace) -> None:
    url = args.url
    try:
        json_response = json.dumps(run(url), indent=4)
        print(json_response)
    except Exception as exc:
        print("failed to run crawler", exc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="command line tool to parse web links for bioinfo links")

    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--webdriver', type=str, choices=["chrome", "firefox"], required=True)
    parser.add_argument('--webdriver_location', type=str, required=False)
    parser.add_argument('--output_location', type=str, required=False)
    args = parser.parse_args()
    main(args)
