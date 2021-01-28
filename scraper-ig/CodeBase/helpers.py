from datetime import datetime
import os.path as osp
import argparse
# Create a file name that can be reused without having to make a new string for every file
# and avoid it creating a new name and not being capable to read from the older file


def create_filename(id):
    if id == "ig":
        timestr = datetime.now().strftime("%Y-%m-%d")
        return timestr
    else:
        # Create a filename based on the curren date and time in YYYY-MM-DD - HH
        timestr = datetime.now().strftime("%Y-%m-%d--%H")

        return timestr


# Check the given input file to see whether in exists
def get_searchterms(scraper_name):
    list_of_terms = []
    # Check whether the searchterms file exitst, else abort the scraper
    if not osp.exists(f'../search_terms_{scraper_name}.txt'):
        print("Not found, exiting...")
        exit(-1)
    else:
        input_file = open(f'../search_terms_{scraper_name}.txt', 'r')
        read_lines = input_file.readlines()

        for lines in read_lines:
            list_of_terms_dirty = lines.strip()
            list_of_terms.append(list_of_terms_dirty)

    return list_of_terms
