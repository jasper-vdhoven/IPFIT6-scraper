# Import external files and assign them names
import marktplaats as mp
import google_maps as gm
import helpers as h
from google_maps_modules.settings import SETTINGS
import argparse


# main
def main():
    print("Starting program...")
    print("\nCapturing date for filename...")
    file_name = h.create_filename("default")
    print(f"The current date and time is: {file_name}")
    print("Done!")

    print("\nStarting Marktplaats scraper with given search terms...")
    mp.main(file_name)
    print("Done!")

    print("\nStarting Google Maps scraper with given search terms...")
    gm.main(file_name)
    print("Done!")

    print("\nAll scrapers have completed!")
    print(f"Results can be found under Output/marktplaats_{file_name}.csv and .xlsx")
    print(f"Results can be found under Output/google_maps_{file_name}.xlsx")
    print("Exiting...")


if __name__ == "__main__":
    main()
