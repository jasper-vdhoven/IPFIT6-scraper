import csv
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime
import os.path as osp
import helpers as h
from helpers import get_searchterms as gst


# Class for the item for writing to CSV/Excel
class Item:
    title = ""
    price = ""
    summary = ""
    seller = ""
    date = ""
    location = ""
    seller_url = ""
    seller_website = ""


# Create the URL to use for the scraper
def create_url(item_query, item_postalcode, item_distance):
    url = 'https://www.marktplaats.nl'
    url += '/q/:' + item_query
    url += '/#distanceMeters:' + item_distance
    url += '|postcode:' + item_postalcode

    return url


# Write the results to a external file for storage and analysis
def write_to_csv(items, file_name, query):
    with open(f'../persistant/Marktplaats/marktplaats_{file_name}.csv', 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow([f"The current query is: {query}"])
        csv_writer.writerow(['Title', 'Price', 'Summary', "Seller", "Date", "Location", "Seller url", "Seller website"])
        for item in items:
            csv_writer.writerow([item.title, item.price, item.summary, item.seller, item.date, item.location, item.seller_url, item.seller_website])
        csv_writer.writerow('')
        write_obj.close()


# Convert the CSV file to a Excel file for easier reading
def convert_csv_to_xsl(file_name):
    wb = Workbook()
    ws = wb.active
    with open(f"../persistant/Marktplaats/marktplaats_{file_name}.csv", 'r') as f:
        for row in csv.reader(f):
            ws.append(row)
    wb.save(f'../persistant/Marktplaats/marktplaats-{file_name}.xlsx')


def is_correct_response(response):
    # Check that the response returned 'success'
    return response == 'success'


def is_defined_item(element):
    if element is not None:
        return element
    else:
        return "not Available"


# Collect the listings with help form the entered search terms
def get_listings(url, timestr, query):
    source = requests.get(url)

    marktplaats = BeautifulSoup(source.text, 'lxml')
    # Returns entire page
    body = marktplaats.find('body')
    # Returns website body
    search_result = is_defined_item(body.find('ul', class_='mp-Listings--list-view'))
    list_of_articles = []

    try:
        for article in search_result:
            try:
                # Get all product links
                item_link = article.a['href']

                # Get all product titles
                item_title = is_defined_item(article.find('h3')).text

                # Get items short summary
                item_summary = is_defined_item(article.find('p')).text

                # Get the name of the seller
                item_seller = is_defined_item(article.find('span', class_="mp-Listing-seller-name")).text

                # Get the link to the sellers Marktplaats profile
                gen_item_seller_link = is_defined_item(article.find('a', class_="mp-TextLink"))['href']
                if "/u/" in gen_item_seller_link:
                    item_seller_link = "https://www.marktplaats.nl" + gen_item_seller_link

                # Get the price of the item
                item_price = is_defined_item(article.find('span', class_="mp-Listing-price mp-text-price-label")).text
                item_price = item_price.replace("\xc2\xa0", " ")

                # Get the date the item was posted
                item_date = is_defined_item(article.find('span', class_="mp-Listing-date mp-Listing-date--desktop")).text

                # Get the location from where the seller is selling from
                item_location = is_defined_item(article.find('span', class_="mp-Listing-location")).text

                # Get the external website the seller promotes in the listing
                item_seller_website = is_defined_item(article.find('a', class_="mp-Listing-sellerCoverLink"))['href']

                myObj = Item()
                myObj.title = item_title.strip()
                myObj.price = item_price.strip()
                myObj.summary = item_summary.strip()
                myObj.seller = item_seller.strip()
                myObj.date = item_date.strip()
                myObj.location = item_location.strip()
                myObj.url = item_link.strip()
                myObj.seller_url = item_seller_link.strip()
                myObj.seller_website = item_seller_website.strip()
                list_of_articles.append(myObj)

            except Exception as e:
                summary_ = "None"
                title_ = "None"
                href = "None"
                price = "None"
                print(e)
    except Exception as e:
        print(e)

    write_to_csv(list_of_articles, timestr, query)
    convert_csv_to_xsl(timestr)


def main(file_name_time):
    i = 0
    id = "mp"
    postalcode = '1011ab'
    distance = '25000'
    query_list = gst(id)

    while i < len(query_list):
        current_url = create_url(query_list[i], postalcode, distance)
        print(f"Current URL to search: {current_url}")
        get_listings(current_url, file_name_time, query_list[i])
        i += 1


if __name__ == "__main__":
    fn = "2020"
    main(fn)
