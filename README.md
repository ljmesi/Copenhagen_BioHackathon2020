# Copenhagen BioHackathon2020 - Team BioCrawCraw
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ljmesi/Copenhagen_BioHackathon2020/master?filepath=Select_Covid-19_data.ipynb)

This is the home repository of team BioCrawCraw's contributions in [Copenhagen BioHackathon 2020](https://biohackathon.dk/).

To run the crawler:
1) create a virtual environment
2) from the name of the virtual environment, run `source ./VENV_NAME/bin/activate` to activate the virtual environment
3) run `pip3 install -r requirements.py`

5) It is not required to use the selenium driver, but it will be required on many websites that render the content dynamically. For this I have started to use the gecko webdriver for python. You must install this locally on your environment if you wish to run this. As an example, if you use a mac, you can run brew install geckodriver. More information can be found here: https://github.com/mozilla/geckodriver
 or here: https://chromedriver.chromium.org/

4) run the app with python3: 

examples:
 - `python3 crawler.py --url 'https://covid.bioexcel.eu/simulations/' --webdriver firefox`
 -  `python3 crawler.py --url 'https://figshare.com/search?q=dcd&searchMode=1' --webdriver chrome --webdriver_location /opt/Downloads/chrome_driver/chromedriver --use_selenium --parse_secondary`

 -  `python3 crawler.py --url 'https://figshare.com/search?q=dcd&searchMode=1' --webdriver chrome --webdriver_location /opt/Downloads/chrome_driver/chromedriver --use_selenium --parse_secondary --output_location .data/01_raw/Scraped/dcd_trayectories_figshare_data_1.csv`

