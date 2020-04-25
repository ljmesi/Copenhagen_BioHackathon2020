# import sys
# sys.path.insert(0, 'usr/lib/chromium-browser/chromedriver')
# from selenium import webdriver
# chrome_options = webdriver.Chrome_options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')


#####


from selenium import webdriver
from selenium.webdriver.common import keys
import time

URL1 = "https://figshare.com/search?q=.dcd&searchMode=1"

browser = webdriver.Chrome()                                                                    #Connects to chrome
browser.get(URL1)                                                                               # Opens in chrome the URL
    
time.sleep(2)

browser.find_element_by_xpath("//a[@class = 'simple-pink-button acceptCookies']").click()                      #Accepts cookies (important to be able to continue)

links = browser.find_elements_by_xpath("//a[contains(@href,'https://') and @role = 'button' and @class = '']") #Sintax used to find the different links

for link in links:                     #For each of the links nodes
    lnk = link.get_attribute('href')   #We have the individual URL at href class so we select it
    print(lnk)
    URL_to_scrap = lnk
    browser.get(URL_to_scrap)          #We go to the designated URL

    title = browser.find_element_by_xpath("//h2[@class = 'title']").text                                #Extracting tittle of trayectory 
    Author = browser.find_element_by_xpath("//a[@class = 'normal-link author']").text                   #EXtracting the author 

    Categories_list = []
    Categories = browser.find_elements_by_xpath("//ul//a[@class = 'normal-link']")                      #Syntax used to identify the different links of categoreis that thee may appear 
    for string in Categories:
        filtered_string = string.text #THe string we want appears at the text part
        Categories_list.append(filtered_string)
    
    Keywords_list = []
    Keywords = browser.find_elements_by_xpath("//div[@class = 'tags section']//a[@class = 'tag-wrap']") #Same that for categories
    for string in Keywords:
        filtered_string = string.get_attribute("title")                                                 #The string we are interested in appears at the tittle part of the node
        Keywords_list.append(filtered_string)

    Description = browser.find_element_by_xpath("//Div[@class = 'description section']").text

    print(title, "\n", Author, "\n", Categories_list, "\n", Keywords_list, Description)

    #Now it is left to improve some kind of dataframe or whatever
    break









#<a class="" href="https://figshare.com/articles/GTT-1-protein-006_dcd/12162405" rel="noopener noreferrer" role="button" target="" title=""><div class="card-item-thumbnail withIcon"><div class="it-preview-placeholder"><div class="it-icon-wrapper"><div class="it-icon dataset"></div></div><div class="it-placeholder-name">dataset</div></div></div><div class="itc-title"><span class="line-clamp last-line line-clamp-defaults">GTT-1-protein-006.dcd</span></div></a>
#<a class="simple-pink-button acceptCookies" href="#" rel="noopener noreferrer" role="button" target="" title="">Accept cookies</a>
