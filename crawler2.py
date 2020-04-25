#!/usr/bin/env python3
import sys
import getopt
from bs4 import BeautifulSoup

url_string = "NA"
output_prefix = "test"
list_file = "NA"
try:
    options, args = getopt.getopt(sys.argv[1:], "ho:u:l:b:l:B:i:f:", [ "outp=", \
                                                                       "url=", \
                                                                       "list=", \
                                                                      ])
except getopt.GetoptError:
    print
    'test.py -o <output_prefix> -u <url> -l <list>'
    sys.exit(2)

for opt, arg in options:
    if opt in ('-o', '--output_prefix'):
        output_prefix = arg
    elif opt in ('-u', '--url'):
        url_string = arg
    elif opt in ('-l', '--list'):
        list_file = arg

outp_string = "NA"
print("Downloading..." + url_string)
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
req = Request(url_string)
try:
    response = urlopen(req)
    html_doc = response.read()
    #print(html_doc)
except HTTPError as e:
    print('The server couldn\'t fulfill the request.')
    print('Error code: ', e.code)
except URLError as e:
    print('We failed to reach a server.')
    print('Reason: ', e.reason)

source = url_string
#domain = urlparse(url_string)

soup = BeautifulSoup(html_doc, "html.parser")
#print(soup)
title = soup.title
text = soup.text

print(title)

links = soup.find_all('a')

for link in links:
    print(link.get('href'))

