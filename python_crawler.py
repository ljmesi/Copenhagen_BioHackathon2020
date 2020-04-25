from selenium import webdriver
from selenium.webdriver.common import keys
import time

URL1 = "https://figshare.com/search?q=.dcd&searchMode=1"

browser = webdriver.Chrome()
browser.get(URL1)
    
time.sleep(2)

browser.find_element_by_xpath("//a[@class = 'simple-pink-button acceptCookies']").click()

links = browser.find_elements_by_xpath("//a[contains(@href,'https://') and @role = 'button']")

for link in links:
    lnk = link.get_attribute('href')
    print(lnk)




#<a class="" href="https://figshare.com/articles/GTT-1-protein-006_dcd/12162405" rel="noopener noreferrer" role="button" target="" title=""><div class="card-item-thumbnail withIcon"><div class="it-preview-placeholder"><div class="it-icon-wrapper"><div class="it-icon dataset"></div></div><div class="it-placeholder-name">dataset</div></div></div><div class="itc-title"><span class="line-clamp last-line line-clamp-defaults">GTT-1-protein-006.dcd</span></div></a>
#<a class="simple-pink-button acceptCookies" href="#" rel="noopener noreferrer" role="button" target="" title="">Accept cookies</a>