#!/usr/bin/sh
echo "starting pycralwer"
export URL='https://google.com'
export WEBDRIVER=chrome
export PARSE_SECONDARy=true
python3 pycrawler.py
echo "ending pycrawler"
