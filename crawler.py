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
    r = url_response(messages, url)
    if r == None:
        messages.append("got response of None, exiting")
        return messages
    try:
        soup = BeautifulSoup(r.content, "html.parser")
        links = soup.body.findAll("a")
        hrefs = []
        for link in links:
            hrefs.append(link.attrs["href"])

        hrefs_reg = []
        for item in hrefs:
            searchObj = re.search(r"http.*", item, re.I)
            if searchObj:
                hrefs_reg.append(searchObj.group())

        messages.append({"soup": "parsed", "links": hrefs, "urls": hrefs_reg})
    except:
        soup = {"status": "failed to parse"}
        messages.append({"soup": soup, "exception": traceback.format_exc()})
    return {"messages": messages}


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
