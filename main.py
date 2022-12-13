# main.py
import time

# Import the scraper class from the scraper module
from scraper import Scraper

# Set the URL that you want to scrape
url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"

# Set the API key
api_key = "83FRHS4AHOFR3RRT"

# Create a Scraper object
scraper = Scraper(url, api_key)

# Fetch the page
soup = scraper.fetch_page()

# Get the data
try:
    data = scraper.get_data(soup, "Symbol")
except Exception as e:
    print(e)