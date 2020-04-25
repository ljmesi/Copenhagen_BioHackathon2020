#!/usr/bin/env python3
import argparse
import json
import re
import sys
import traceback

import requests
from bs4 import BeautifulSoup

SITE_STRING = "https://{base_url}/{query_params}"


def run(url: str) -> dict:
    messages = []

    initial_response = url_response(messages, url)

    if initial_response is None:
        messages.append("got response of None, exiting")
        return {"messages": messages}

    append_bs_parsing(messages, initial_response)
    append_selenium_parsing(messages, url)
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

def append_selenium_parsing(messages, url):
    try:
        messages.append({"selenium": "parsed",
                     "links": prepare_selenium_response(url)})
    except:
        selenium = {"status": "failed to parse"}
        messages.append({"selenium": selenium, "exception": traceback.format_exc()})

def prepare_selenium_response(url:str)->list:
    #TODO:cleanup webdriver methods
    from selenium import webdriver
    driver = webdriver.Firefox()
    driver.get(url)
    driver.implicitly_wait(30)
    elements = driver.find_elements_by_class_name("item-thumb-card")
    # selenium_links = driver.execute_script('var bob = document.getElementsByClassName("item-thumb-card")``V;Object.keys(bob).forEach(function(a){bob[a].childNodes.forEach(function(b){return b.attributes})})')
    # selenium_links = driver.execute_script('var items = {};Object.keys(items).forEach(function(attrs){console.log(item[attrs]);return items[attrs];});', element)
    selenium_links = []
    # for element in elements:
    java_script = 'var items = document.getElementsByClassName("item-thumb-card");var n = [];for (i=0; i < items.length;i++){var temp = items[i].childNodes[0].getAttribute("href");console.log(temp);n.push(temp);};return n;'
    selenium_links.append(driver.execute_script(java_script, None))
    return [x for x in selenium_links]


def url_response(messages: list, url: str) -> requests.Response:
    try:
        # TODO: auth, handle exceptions
        response = requests.get(url, )
        messages.append("request to: url produced: {}".format(url, str(response.status_code)))
        return response
    except Exception as e:
        messages.append("initial request failed, error: {}".format(e))


def main(args: argparse.Namespace) -> None:
    # TODO: check if desired:
    # url = SITE_STRING.format(base_url=args.base_url, query_params=args.query_params)
    url = args.url
    try:
        json_response = json.dumps(run(url), indent=4)
        print(json_response)
    except Exception as exc:
        print("failed to run crawler", exc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="command line tool to parse web links for bioinfo links")

    # TODO: check if desired:
    # parser.add_argument('--query_params', type=str, required=False, help="add your query params here e.g.: ?id=1&name=bob")
    parser.add_argument('--url', type=str, required=True)
    args = parser.parse_args()
    main(args)
