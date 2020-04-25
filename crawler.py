#!/usr/bin/env python3
import argparse
import json
import re
import traceback
import time

import requests
from bs4 import BeautifulSoup

FIGSHARE_COOKIE_XPATH = "//a[@class = 'simple-pink-button acceptCookies']"

FIGSHARE_ANCHOR_XPATH = "//a[contains(@href,'https://') and @role = 'button' and @class = '']"

INFINI_SCROLL_WAIT_TIME = 5

DEFAULT_IMPLICIT_WAIT_TIME = 30


def run(url: str) -> dict:
    messages = []

    initial_response = url_response(messages, url)

    if initial_response is None:
        messages.append("got response of None, exiting")
        return {"messages": messages}

    append_bs_parsing(messages, initial_response)
    append_selenium_parsing(messages, url, args)
    # parse_secondary_link(driver)
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
            searchObj = re.search(r"http.*", item, re.I)
            if searchObj:
                hrefs_reg.append(searchObj.group())

        messages.append({"soup": "parsed",
                         "links": hrefs,
                         "urls": hrefs_reg})
    except:
        soup = {"status": "failed to parse"}
        messages.append({"soup": soup, "exception": traceback.format_exc()})


def append_selenium_parsing(messages, url, args):
    try:
        links = prepare_selenium_response(url, args)
        messages.append({"selenium": "parsed",
                         "links": links})
    except:
        selenium = {"status": "failed to parse"}
        messages.append({"selenium": selenium, "exception": traceback.format_exc()})


def prepare_selenium_response(url: str, args: argparse.Namespace) -> list:
    driver = build_webdriver(args)
    driver.get(url)
    driver.implicitly_wait(DEFAULT_IMPLICIT_WAIT_TIME)
    accept_cookies(driver)

    scroll_to_bottom_and_get_links(driver)
    links = driver.find_elements_by_xpath(FIGSHARE_ANCHOR_XPATH)
    return [x.get_attribute('href') for x in links]


def accept_cookies(driver) -> None:
    cookie_string = FIGSHARE_COOKIE_XPATH
    element = driver.find_element_by_xpath(cookie_string)
    if element:
        element.click()


def scroll_to_bottom_and_get_links(driver) -> list:
    links_found = get_links_in_browser(driver, [])
    seed_height = driver.execute_script("return document.body.scrollHeight")
    links = scroll_down_finding_links(driver, seed_height, links_found)
    if links:
        for link in links: links_found.append(link)
    return links_found


def scroll_down_finding_links(driver, height, links_found) -> list:
    driver.execute_script("scroll(0, 250);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    links_found = get_links_in_browser(driver, links_found)
    driver.implicitly_wait(INFINI_SCROLL_WAIT_TIME)
    executed_height = driver.execute_script("return document.body.scrollHeight")
    if executed_height == height:
        return links_found
    print("scrolling to bottom, current height: {}, previous height: {}".format(executed_height, height))
    time.sleep(INFINI_SCROLL_WAIT_TIME)
    scroll_down_finding_links(driver, executed_height, links_found)


def get_links_in_browser(driver, link_list: list) -> list:
    links = driver.find_elements_by_xpath(FIGSHARE_ANCHOR_XPATH)
    if links:
        for link in links:
            if link not in link_list:
                link_list.append(link)
    return link_list


def build_webdriver(args):
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
            lnk = link.get_attribute('href')
            browser.get(lnk)  # We go to the designated URL
            title = browser.find_element_by_xpath(title_xpath).text  # Extracting tittle of trayectory
            author = browser.find_element_by_xpath(author_xpath).text  # EXtracting the author

            categories_list = []
            categories = browser.find_elements_by_xpath(normal_link_string)
            for string in categories:
                filtered_string = string.text
                categories_list.append(filtered_string)

            keywords_list = []
            tag_secion = tag_section_xpath
            Keywords = browser.find_elements_by_xpath(
                tag_secion)  # Same that for categories
            for string in Keywords:
                filtered_string = string.get_attribute("title")
                keywords_list.append(filtered_string)
            print(title, "\n", author, "\n", categories_list, "\n", keywords_list)


def url_response(messages: list, url: str) -> requests.Response:
    try:
        # TODO: auth, handle exceptions
        response = requests.get(url, )
        messages.append("request to: url produced: {}".format(url, str(response.status_code)))
        return response
    except Exception as e:
        messages.append("initial request failed, error: {}".format(e))


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
    args = parser.parse_args()
    main(args)
