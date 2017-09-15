# relister.py
#! /usr/bin/python
from contextlib import closing
from selenium import webdriver
from selenium.webdriver import Safari
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import requests
from helper import supersecretusername, supersecretpassword

import time

# get the browser
browser = webdriver.Safari()
browser.get('https://accounts.craigslist.org/login/home')

try:
    WebDriverWait(browser, timeout=10).until(lambda browser: browser.find_element_by_id('inputPassword'))
except TimeoutException:
    browser.quit()


# log in
username = browser.find_element_by_name('inputEmailHandle')
username.send_keys(supersecretusername)

password = browser.find_element_by_name('inputPassword')
password.send_keys(supersecretpassword)

browser.find_element_by_class_name('accountform-btn').click()


# wait for elements to load
try:
    WebDriverWait(browser, timeout=10).until(lambda browser: browser.find_element_by_id('use_arc_chk'))
except TimeoutException:
    browser.quit()
    print ("COULD NOT FIND MAIN SCREEN")


# all relist elements
relist_elements = browser.find_elements_by_class_name('manage repost')

links = list(map(lambda x: x.get_attribute("action"), relist_elements))


for link in links:
    
    # load the link and wait for manage button
    browser.get(link)
    try:
        WebDriverWait(browser, timeout=10).until(lambda browser: browser.find_element_by_class_name('managebtn'))
    except TimeoutException:
        print ("COULD NOT FIND MANAGE BUTTON")
        print (link)


    # get the manage button and repost and then wait for continue button
    browser.find_element_by_class_name('managebtn').click()
    
    try:
        WebDriverWait(browser, timeout=10).until(lambda browser: browser.find_element_by_class_name('bigbutton'))
    except TimeoutException:
        print ("COULD NOT FIND CONTINUE BUTTON")
        print (link)



    # get the continue button and click and wait for publish button
    browser.find_element_by_class_name('bigbutton').click()

    try:
        WebDriverWait(browser, timeout=10).until(lambda browser: browser.find_element_by_class_name('button'))
    except TimeoutException:
        print ("COULD NOT FIND PUBLISH BUTTON")
        print (link)
    
    
    
    # press the publish button
    browser.find_element_by_class_name('button').click()
    try:
        WebDriverWait(browser, timeout=10).until(lambda browser: browser.find_element_by_link_text('Return to your account page'))
    except TimeoutException:
        print ("DID NOT FINISH PUBLISHING")
        print (link)

    print ("Your item was relisted!")

    time.sleep(120) # wait 2 minutes so Craig can keep up!

