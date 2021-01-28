import subprocess
# from helpers import get_searchterms as gst
import helpers as h
from os import mkdir as osdir
import os.path as osp


# Create the needed directories
def make_dirs(file_name):
    if not osp.exists(f"../persistant/Instagram/{file_name}"):
        path = f"../persistant/Instagram/{file_name}"
        osdir(path)
    else:
        path = f"../persistant/Instagram/{file_name}"


# simple main for the Instagram scraper
def scraper(file_name):
    id = "ig"
    lis_of_terms = h.get_searchterms(id)

    for i in lis_of_terms:
        subprocess.run(f"cd ../persistant/Instagram/{file_name} && instagram-scraper {i} --tag --include-location --latest --maximum 100", shell=True)
    return lis_of_terms


def main():
    id = "ig"
    file_name = h.create_filename(id)
    make_dirs(file_name)
    list = scraper(file_name)
    return list

if __name__ == '__main__':
    main()
