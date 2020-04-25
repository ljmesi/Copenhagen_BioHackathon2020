# Copenhagen_BioHackathon2020
This is the home repository of team BioCrawCraw's contributions in Copenhagen BioHackathon 2020.

To run the crawler:
1) create a virtual environment
2) from the name of the virtual environment, run `source ./VENV_NAME/bin/activate` to activate the virtual environment
3) run `pip3 install -r requirements.py`
4) run the app with python3: e.g.: python3 crawler.py --url 'https://figshare.com/search?q=dcd&searchMode=1'

5) It is not required to use the selenium driver, but it will be required on many websites that render the content dynamically. For this I have started to use the gecko webdriver for python. You must install this locally on your environment if you wish to run this. As an example, if you use a mac, you can run brew install geckodriver. More information can be found here: https://github.com/mozilla/geckodriver
