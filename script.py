import csv
import os
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import time
from datetime import date
from properti import Properti

zip_code = input("Input a zip code: ")

zip_code = zip_code.strip()

properties = []

with webdriver.Chrome("env/bin/chromedriver") as driver:

    print("Starting browser...")
    driver.start_client()
    driver.get("https://www.realtor.com")
    driver.maximize_window()

    search_bar = driver.find_element_by_id("rdc-main-search-nav-hero-label")
    search_bar.send_keys(zip_code)

    search_button = driver.find_element_by_class_name("search-btn").click()
    time.sleep(3)

    footer_listing = driver.find_element_by_id("srp-footer-found-listing").text
    property_count = int(footer_listing.split(" ")[1])
    page_count = (property_count // 42) + 1

    print("Gathering data")

    for i in range(page_count):

        soup = BeautifulSoup(driver.page_source, "html.parser")

        listings = soup.find_all(attrs={'class':'component_property-card'})

        for listing in listings:
            properti = Properti()
            try:
                properti.address = listing.find(attrs={'class':'address'}).text
                properti.second_address = listing.find(attrs={'class':'address-second'}).text
                properti.price = listing.find(attrs={'data-label':'pc-price'}).text

                beds_meta_container = listing.find(attrs={'data-label':'pc-meta-beds'})
                properti.beds = beds_meta_container.find(attrs={'data-label':'meta-value'}).text

                baths_meta_container = listing.find(attrs={'data-label':'pc-meta-baths'})
                properti.baths = baths_meta_container.find(attrs={'data-label':'meta-value'}).text

                sqft_meta = listing.find(attrs={'data-label':'pc-meta-sqft'})
                properti.sqft = sqft_meta.find(attrs={'data-label':'meta-value'}).text

                sqft_lot_meta = listing.find(attrs={'data-label':'pc-meta-sqftlot'})
                properti.sqft_lot = sqft_lot_meta.find(attrs={'data-label':'meta-value'}).text

                property_type_meta = listing.find(attrs={'data-label':'pc-type'})
                properti.property_type = property_type_meta.find('span').text

                properties.append(properti.get_cells())
            except AttributeError:
                continue
        
        if(i < (page_count - 1)):
            next_page_button = driver.find_element(By.CLASS_NAME, "pagination-next")
            next_page_button.click()
            time.sleep(1)


print("Creating file...")

filename = "./" + zip_code + "-" + str(date.today()) + ".csv"

with open(filename, "a") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Address", "Second Address", "Price", "Beds", "Baths", "Sqft", "Lot Sqft", "Type"])

    writer.writerows(properties)

    csvfile = open(filename, 'r')

    wb = openpyxl.Workbook()

    ws = wb.active

    with open(filename, 'r') as f:
        reader = csv.reader(f)

        for r, row in enumerate(reader, start=1):
            for c, val in enumerate(row, start=1):
                ws.cell(row=r, column=c).value = val

    wb.save("./" + zip_code + "-" + str(date.today()) + ".xlsx")
    csvfile.close()
