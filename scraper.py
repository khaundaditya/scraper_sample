#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import os
from urllib.request import urlopen, Request

# Local class to parse a specific CMS data 
from . import DoctorContentParser

URL_TO_SCRAP = "SOME_URL"

def get_data(url, name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = requests.get(url, headers=headers)
    content = req.text
    # parse Content and Get fields
    parser = ContentParser(content)
    accreditions = parser.get_accreditions()
    name_details = parser.get_name_details()
    practices_at = parser.associated_with()
    address_details = parser.get_address()
    specialities = parser.get_specialities()
    # Store them in CSV.

if __name__ == '__main__':


    options = Options()
    options.headless = True
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
    #driver = webdriver.Chrome()
    driver.get(URL_TO_SCRAP);

    # listing-30258
    timeout = 10
    try:
        #element_present = EC.presence_of_element_located((By.ID, 'listing-30571'))
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'job_listing-clickbox'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    #class_name="job_listing type-job_listing card-style--default style-grid listing-card type-job_listing style-grid"

    #print(driver.current_url)
    elements = driver.find_elements_by_class_name('job_listing-clickbox')

    for ele in elements:
        href = ele.get_attribute('href')
        data = href.split("/")
        print(href + ":" + str(data) )
        get_data(href)
        break
    count = 100
    for i in range(61):
        pagination_element = driver.find_element_by_class_name('job-manager-pagination')
        children = pagination_element.find_element_by_xpath(".//ul")
        lis = children.find_elements_by_tag_name('li')
        for li in lis:
            if li.text == '→' :
                a = li.find_element_by_xpath(".//a")
                # listing-30258
                a.click()
                time.sleep(12)
                elements = driver.find_elements_by_class_name('job_listing-clickbox')
                for ele in elements:
                   href = ele.get_attribute('href')
                   data = href.split("/")
                   count = count + 1
                   print(str(count) + ':' + href + ":" + data[-2] )
                   get_data(href)
           