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

list_of_formats_with_trayectories = [".xtc",".dcd", ".ntraj", ".netcdf", ".trr", ".lammpstrj", ".xyz", ".binpos", ".hdf5", ".dtr", ".arc", ".tng", "mdcrd", ".crd", ".dms", ".trj", ".ent", ".ncdf"]
#Creating dictionary to store the data
data = {}
data['Title'] = []
data['Authors'] = []
data['Categories'] = []
data['Keywords'] = []
data['Description'] = []
data['Type of (possible) format'] = []


for format in list_of_formats_with_trayectories:
    URL1 = "https://figshare.com/search?q={}&searchMode=1".format(format)

    browser1 = webdriver.Chrome()                                                                    #Connects to chrome principal page
    browser2 = webdriver.Chrome()                                                                    #Connects to each link we visit

    browser1.get(URL1)                                                                               # Opens in chrome the URL
        
    time.sleep(2)

    browser1.find_element_by_xpath("//a[@class = 'simple-pink-button acceptCookies']").click()                      #Accepts cookies (important to be able to continue)

    links = browser1.find_elements_by_xpath("//a[contains(@href,'https://') and @role = 'button' and @class = '']") #Sintax used to find the different links


    for link in links:                     #For each of the links nodes
        print('hola')
        #time.sleep(10)
        is_link = False
        try:
            lnk = link.get_attribute('href')   #We have the individual URL at href class so we select it
            is_link = True
        except:
            print("no link")
        print(lnk)
        URL_to_scrap = lnk
        browser2.get(URL_to_scrap)          #We go to the designated URL. Using a second browser variable so as it doesn't interfere with the page of each format

        try:
            title = browser2.find_element_by_xpath("//h2[@class = 'title']").text 
            time.sleep(1)                                                                                   #Extracting tittle of trayectory 
        except:
            title = "Not title found"

        try:
            list_of_authors = []
            authors = browser2.find_elements_by_xpath("//span[contains(@class,'author')]")                   #EXtracting the author 
            for author in authors:
                author_found = author.text
                list_of_authors.append(author_found)
        except:
            authors = "No authors found"

        time.sleep(2)

        try:
            Categories_list = []
            Categories = browser2.find_elements_by_xpath("//ul[@class = 'normal-list']//a[@class = 'normal-link']")      #Syntax used to identify the different links of categoreis that thee may appear 
            for string in Categories:
                filtered_string = string.text                                                                             #The string we want appears at the text part
                Categories_list.append(filtered_string)
        except:
            Categories_list = "No categories found"
        
        try:
            Keywords_list = []
            Keywords = browser2.find_elements_by_xpath("//div[@class = 'tags section']//a[@class = 'tag-wrap']") #Same that for categories
            for string in Keywords:
                filtered_string = string.get_attribute("title")                                                 #The string we are interested in appears at the tittle part of the node
                Keywords_list.append(filtered_string)
        except:
            Keywords_list = "No keywords found"

        try:
            Description = browser2.find_element_by_xpath("//Div[@class = 'description section']").text
        except:
            Description = "No description found"

        if is_link == True:
            data['Title'].append(title)
            data['Authors'].append(list_of_authors)
            data['Categories'].append(Categories_list)
            data['Keywords'].append(Keywords_list)
            data['Description'].append(Description)
            data['Type of (possible) format'].append(format)

        #print(title, "\n", Author, "\n", Categories_list, "\n", Keywords_list, "\n" ,Description)

        #break

dataframe = pd.DataFrame(data)                # Creating dataframe
dataframe.to_csv("~/Desktop/DAtaframe.csv")   #Change to a personalized location
