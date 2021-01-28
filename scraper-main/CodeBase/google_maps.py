from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

from google_maps_modules.helpers import *
from google_maps_modules.settings import SETTINGS
from colours import fore

import time
import xlsxwriter

import os.path as osp
import helpers as h


def get_terms():
    id = "gm"
    list_of_terms = h.get_searchterms(id)
    print("returning terms now")
    return list_of_terms


def scrape(filename, search_terms):
    # Determies whether urls should be collected too, takes more time
    scrape_website = True
    # Turning this on makes ever result without an address appear as a duplicate
    skip_duplicate_address = False

    # Created driver and wait
    chrome_options = Options()
    # Run the browser headless to avoid the GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    # Set main box class name
    box_class = "section-result-content"

    # Initialize workbook / worksheet
    workbook = xlsxwriter.Workbook(f"../persistant/GoogleMaps/google_maps_{filename}.xlsx")
    worksheet = workbook.add_worksheet()

    # Headers and data
    data = {
        "name": "",
        "phone": "",
        "address": "",
        "website": ""
    }
    headers = generate_headers(scrape_website, data)
    print_table_headers(worksheet, headers)

    # Start from second row in xlsx, as first one is reserved for headers
    row = 1

    # Remember scraped addresses to skip duplicates
    addresses_scraped = {}

    # List of current terms
    current_term = {
        "name": ""
    }

    for term in search_terms:
        print(term)
        # Go to the index page
        driver.get(SETTINGS["MAPS_INDEX"])

        current_term["name"] = term

        write_data_row(worksheet, current_term, row)
        row += 1

        # Build the query string
        query = "{0} {1}".format(term, SETTINGS["PLACES"])

        # Fill in the input and press enter to search
        q_input = driver.find_element_by_name("q")
        q_input.send_keys(query, Keys.ENTER)

        # Wait for the results page to load. If no results load in 10 seconds, continue to next place
        try:
            w = wait.until(
                ec.presence_of_element_located((By.CLASS_NAME, box_class))
            )
        except:
            continue

        # Loop through pages and results
        for _ in range(0, SETTINGS["PAGE_DEPTH"]):
            # Get all the results boxes
            boxes = driver.find_elements_by_class_name(box_class)

            # Loop through all boxes and get the info from it and store into an excel
            for box in boxes:
                # Just get the values, add only after we determine this is not a duplicate (or duplicates should not be skiped)
                name = box.find_element_by_class_name("section-result-title").find_element_by_xpath(".//span[1]").text

                address = box.find_element_by_class_name("section-result-location").text

                scraped = address in addresses_scraped

                if scraped and skip_duplicate_address is True:
                    print(f"{fore.WARNING}Skipping {name} as duplicate by address{fore.RESET}")
                else:
                    # Initiate the list and add to it only now
                    data["name"] = name
                    data["address"] = address

                    phone = box.find_element_by_class_name("section-result-phone-number").find_element_by_xpath(
                        ".//span[1]").text

                    data["phone"] = phone

                    if scraped:
                        addresses_scraped[address] += 1
                    else:
                        addresses_scraped[address] = 1

                    # Only if user wants to get the URL to, get it
                    try:
                        if scrape_website:
                            url = box.find_element_by_class_name(
                                "section-result-action-icon-container").find_element_by_xpath("./..").get_attribute("href")
                            website = get_website_url(url)
                            data["website"] = website

                        write_data_row(worksheet, data, row)
                        row += 1
                        
                    except:
                        continue

            # Go to next page
            try:
                next_page_link = driver.find_element_by_class_name("n7lv7yjyC35__button-next-icon")
                next_page_link.click()
            except WebDriverException:
                break

            # Wait for the next page to load
            time.sleep(5)

    workbook.close()
    driver.close()


def main(filename):
    list_of_terms = get_terms()
    scrape(filename, list_of_terms)


if __name__ == '__main__':
    main(filename="2020")
