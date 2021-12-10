import functools
import os
import random
import sys
import time

from faker import Faker
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from constants.elementIds import *
from constants.location import *
from constants.urls import *
from constants.xPaths import *

fake = Faker()
chromedriver_location = "./chromedriver"
print = functools.partial(print, flush=True)


def start_driver(rand_num):
    driver = webdriver.Chrome(chromedriver_location)
    driver.get(URLS[rand_num])
    driver.implicitly_wait(10)
    time.sleep(2)
    driver.find_element_by_xpath(APPLY_NOW_BUTTON_1).click()
    driver.find_element_by_xpath(APPLY_NOW_BUTTON_2).click()
    driver.find_element_by_xpath(CREATE_AN_ACCOUNT_BUTTON).click()
    return driver


def generate_account(driver, rand_num):
    # make fake account info and fill

    email = fake.email()
    password = fake.password()
    for key in XPATHS_2.keys():
        match key:
            case 'email' | 'email-retype':
                info = email
            case 'pass' | 'pass-retype':
                info = password
            case 'first_name' | 'last_name':
                info = fake.first_name()
            case 'pn':
                info = fake.phone_number()

        driver.find_element_by_xpath(XPATHS_2.get(key)).send_keys(info)

    time.sleep(random.randint(0, 2))
    select = Select(driver.find_element_by_id(COUNTRY_REGION_CODE_LABEL))
    select.select_by_value(COUNTRY_CODE_US)
    select = Select(driver.find_element_by_id(COUNTRY_REGION_OF_RESIDENCE_LABEL))
    select.select_by_value(COUNTRY_CODE_US)

    driver.find_element_by_xpath('//*[@id="dataPrivacyId"]').click()
    time.sleep(1.5)
    driver.find_element_by_xpath('//*[@id="dlgButton_20:"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="fbclc_createAccountButton"]').click()

    time.sleep(1.5)

    print(f"successfully made account for fake email {email}")


def fill_out_application_and_submit(driver, rand_num):
    driver.implicitly_wait(10)
    city = list(CITIES_TO_STATES.keys())[rand_num]

    # fill out form parts of app
    driver.find_element_by_xpath('//*[@id="109:topBar"]').click()
    driver.find_element_by_xpath('//*[@id="260:topBar"]').click()

    zip_num = random.randint(0, 4)

    for key in XPATHS_1.keys():

        match key:
            case 'resume':
                driver.find_element_by_xpath('//*[@id="48:_attach"]/div[6]').click()
                info = os.getcwd() + "/src/resume.png"
            case 'addy':
                info = fake.street_address()
            case 'city':
                info = city
            case 'zip':
                zipp = CITIES_TO_ZIP_CODES[city]
                info = zipp[zip_num]
            case 'job':
                info = fake.job()
            case 'salary':
                info = random.randint(15, 35)

        driver.find_element_by_xpath(XPATHS_1.get(key)).send_keys(info)

    print(f"successfully filled out app forms for {city}")

    # fill out dropdowns
    select = Select(driver.find_element_by_id('154:_select'))
    select.select_by_visible_text('Yes')
    select = Select(driver.find_element_by_id('195:_select'))
    select.select_by_visible_text('United States')

    select = Select(driver.find_element_by_id('211:_select'))
    select.select_by_visible_text('Yes')
    select = Select(driver.find_element_by_id('215:_select'))
    select.select_by_visible_text('No')
    select = Select(driver.find_element_by_id('219:_select'))
    select.select_by_visible_text('No')
    select = Select(driver.find_element_by_id('223:_select'))
    select.select_by_visible_text('No')
    select = Select(driver.find_element_by_id('227:_select'))
    select.select_by_visible_text('No')
    select = Select(driver.find_element_by_id('231:_select'))
    select.select_by_visible_text('Yes')
    select = Select(driver.find_element_by_id('223:_select'))
    select.select_by_visible_text('No')

    time.sleep(1)

    select = Select(driver.find_element_by_id('235:_select'))
    gender = random.choice(['Male', 'Female', 'Other'])
    select.select_by_visible_text(gender)

    driver.find_element_by_xpath('//label[text()="350 LBS"]').click()
    driver.find_element_by_xpath('//label[text()="800 LBS"]').click()
    els = driver.find_elements_by_xpath('//label[text()="Yes"]')
    for el in els:
        el.click()

    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="261:_submitBtn"]').click()
    print(f"successfully submitted application")


def main():
    rand_num = random.randint(0, 3)
    i = 1
    while (i < 10000):

        try:
            driver = start_driver(rand_num)
        except Exception as e:
            print(f"failed to start driver: {str(e)}")
            pass

        time.sleep(2)

        try:
            generate_account(driver, rand_num)
        except Exception as e:
            print(f"failed to create account: {str(e)}")
            pass

        try:
            fill_out_application_and_submit(driver, rand_num)
        except Exception as e:
            print(f"failed to fill out app and submit: {str(e)}")
            pass

        driver.close()
        time.sleep(5)


if __name__ == '__main__':
    main()
    sys.exit()
