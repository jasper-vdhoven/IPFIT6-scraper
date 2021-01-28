# Import external files and assign them names
import helpers as h
import instagram as ig
import argparse


def main():
    print("Starting program...")
    print("\nCapturing date for filename...")
    file_name = h.create_filename("default")
    print(f"The current date and time is: {file_name}")
    print("Done!")

    print("\nStarting Instagram scraper with given search terms...")
    query_list = ig.main()
    print("Done!")

    print("\nThe scraper have completed succesfully!")
    print(f"Results can be found under Output/Instagram/{query_list}.json and the additional downloaded media")
    print("Exiting...")


if __name__ == "__main__":
    main()
