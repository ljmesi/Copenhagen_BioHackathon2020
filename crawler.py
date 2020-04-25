#!/usr/bin/env python3
import argparse
import json
import re
import traceback
import time

import requests
from bs4 import BeautifulSoup


def run(url: str) -> dict:
    messages = []

    initial_response = url_response(messages, url)

    if initial_response is None:
        messages.append("got response of None, exiting")
        return {"messages": messages}

    append_bs_parsing(messages, initial_response)
    append_selenium_parsing(messages, url, args)
    #parse_secondary_link(driver)
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
        messages.append({"selenium": "parsed",
                     "links": prepare_selenium_response(url, args)})
    except:
        selenium = {"status": "failed to parse"}
        messages.append({"selenium": selenium, "exception": traceback.format_exc()})

def prepare_selenium_response(url:str, args:argparse.Namespace)->list:
    driver = build_webdriver(args)
    driver.get(url)
    driver.implicitly_wait(30)
    cookie_string = "//a[@class = 'simple-pink-button acceptCookies']"
    driver.find_element_by_xpath(cookie_string).click()  # Accepts cookies (important to be able to continue)
    print("accepted cookies")

    #scroll_to_bottom(driver)
    links = driver.find_elements_by_xpath("//a[contains(@href,'https://') and @role = 'button' and @class = '']")  # Sintax used to find the different links

    return [x.get_attribute('href') for x in links]

def scroll_to_bottom(driver):
    seed_height = driver.execute_script("return document.body.scrollHeight")
    scroll_down(driver, seed_height)

def scroll_down(driver, height):
    driver.execute_script("scroll(0, 250);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    driver.implicitly_wait(5)
    executed_height = driver.execute_script("return document.body.scrollHeight")
    print(executed_height, height)
    if (executed_height == height):
        return
    time.sleep(5)
    scroll_down(driver, executed_height)


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


def parse_secondary_link(links:list, browser) -> None:
    print("parsing secondary links")
    links_string = "//a[contains(@href,'https://') and @role = 'button' and @class = '']"
    links = browser.find_elements_by_xpath(links_string)  # Sintax used to find the different links
    if links:
        for link in links:
            lnk = link.get_attribute('href')  # We have the individual URL at href class so we select it
            browser.get(lnk)  # We go to the designated URL
            title = browser.find_element_by_xpath("//h2[@class = 'title']").text  # Extracting tittle of trayectory
            Author = browser.find_element_by_xpath("//a[@class = 'normal-link author']").text  # EXtracting the author

            Categories_list = []
            normal_link_string = "//ul//a[@class = 'normal-link']"
            Categories = browser.find_elements_by_xpath(
                normal_link_string)  # Syntax used to identify the different links of categoreis that thee may appear
            for string in Categories:
                filtered_string = string.text  # THe string we want appears at the text part
                Categories_list.append(filtered_string)

            Keywords_list = []
            tag_secion = "//div[@class = 'tags section']//a[@class = 'tag-wrap']"
            Keywords = browser.find_elements_by_xpath(
                tag_secion)  # Same that for categories
            for string in Keywords:
                filtered_string = string.get_attribute(
                    "title")  # The string we are interested in appears at the tittle part of the node
                Keywords_list.append(filtered_string)
            print(title, "\n", Author, "\n", Categories_list, "\n", Keywords_list)

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
