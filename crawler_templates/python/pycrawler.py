#!/usr/bin/env python3
import json
import os
import traceback
import argparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from lib.study import Study


def run(url: str) -> dict:
    data = []
    parse_html(data, url)
    return {"data": data}

def parse_html(messages: list, url: str):
    try:
        driver = prepare_selenium_response(url)
        bs = BeautifulSoup(driver.page_source, "html.parser")
        links = bs.findAll('a', href=True)
        hrefs = []
        for link in links:
            hrefs.append(link.attrs["href"])

        messages.append({"soup": "parsed",
                         "links": hrefs})
        driver.close()
    except:
        selenium = {"status": "failed to parse"}
        messages.append({"selenium": selenium, "exception": traceback.format_exc()})


def prepare_selenium_response(url: str) -> WebDriver:
    driver = build_webdriver()
    driver.get(url)
    driver.implicitly_wait(100)
    return driver


def build_webdriver() -> WebDriver:
    print("starting chrome driver")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options,
                            executable_path="/usr/src/app/chromedriver",
                            desired_capabilities=DesiredCapabilities.CHROME)



def main(args: argparse.Namespace) -> None:
    url = args.url
    try:
        json_response = json.dumps(run(url), indent=4)
        print(json_response)
    except Exception as exc:
        print("failed to run crawler", exc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="command line tool to parse web content")
    parser.add_argument('--url', type=str, default=os.environ.get('URL'))
    args = parser.parse_args()
    main(args)
