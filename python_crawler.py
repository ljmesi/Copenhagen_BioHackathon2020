# import sys
# sys.path.insert(0, 'usr/lib/chromium-browser/chromedriver')
# from selenium import webdriver
# chrome_options = webdriver.Chrome_options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')


#####

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common import keys
import time

URL1 = "https://figshare.com/search?q=.dcd&searchMode=1"

browser1 = webdriver.Chrome()                                                                    #Connects to chrome principal page
browser2 = webdriver.Chrome()                                                                    #Connects to each link we visit

browser1.get(URL1)                                                                               # Opens in chrome the URL
    
time.sleep(2)

browser1.find_element_by_xpath("//a[@class = 'simple-pink-button acceptCookies']").click()                      #Accepts cookies (important to be able to continue)

links = browser1.find_elements_by_xpath("//a[contains(@href,'https://') and @role = 'button' and @class = '']") #Sintax used to find the different links


#Creating dictionary to store the data
data = {}
data['Title'] = []
data['Author'] = []
data['Categories'] = []
data['Keywords'] = []
data['Description'] = []


for link in links:                     #For each of the links nodes
    print('hola')
    #time.sleep(10)
    lnk = link.get_attribute('href')   #We have the individual URL at href class so we select it
    print(lnk)
    URL_to_scrap = lnk
    browser2.get(URL_to_scrap)          #We go to the designated URL


    title = browser2.find_element_by_xpath("//h2[@class = 'title']").text 
    time.sleep(1)                               #Extracting tittle of trayectory 
    Author = browser2.find_element_by_xpath("//a[@class = 'normal-link author']").text                   #EXtracting the author 

    time.sleep(2)

    Categories_list = []
    Categories = browser2.find_elements_by_xpath("//ul[@class = 'normal-list']//a[@class = 'normal-link']")      #Syntax used to identify the different links of categoreis that thee may appear 
    for string in Categories:
        filtered_string = string.text                                                                             #The string we want appears at the text part
        Categories_list.append(filtered_string)
    
    Keywords_list = []
    Keywords = browser2.find_elements_by_xpath("//div[@class = 'tags section']//a[@class = 'tag-wrap']") #Same that for categories
    for string in Keywords:
        filtered_string = string.get_attribute("title")                                                 #The string we are interested in appears at the tittle part of the node
        Keywords_list.append(filtered_string)

    Description = browser2.find_element_by_xpath("//Div[@class = 'description section']").text

    data['Title'].append(title)
    data['Author'].append(Author)
    data['Categories'].append(Categories_list)
    data['Keywords'].append(Keywords_list)
    data['Description'].append(Description)

    #print(title, "\n", Author, "\n", Categories_list, "\n", Keywords_list, "\n" ,Description)

    #break

dataframe = pd.DataFrame(data)                # Creating dataframe
dataframe.to_csv("~/Desktop/DAtaframe.csv")   #Change to a personalized location
