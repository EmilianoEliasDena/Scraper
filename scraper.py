#scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urlencode


class Scraper:
    def __init__(self, url, api_key):
        """
        Initialize the scraper object with the URL of the page to scrape
        and the API key for the Alpha Vantage API.
        """
        self.url = url
        self.api_url = "https://www.alphavantage.co/query"
        self.api_key = api_key
        
        # Fetch the page and parse the table
        self.soup = self.fetch_page()
        self.df = self.parse_table("Symbol")


    def fetch_page(self):
        """
        Fetch the HTML content of the page using the requests library.
        Return the BeautifulSoup object containing the parsed HTML.
        """
        # Use the requests library to fetch the HTML content of the page
        try:
            with requests.get(self.url) as r:
                r.raise_for_status()
                soup = BeautifulSoup(r.content, "html.parser")
        except requests.exceptions.RequestException as e:
            raise Exception("Error: Could not fetch the page") from e

        return soup

    def parse_table(self, index_col):
        """
        Use the `pandas` library to read the table from the HTML.
        Return the parsed table as a DataFrame.
        """
        # Find the table on the page using its attributes
        table = self.soup.find("table", attrs={"class": "wikitable sortable"})

        # Check if the table was found
        if table is None:
            raise Exception("Error: Invalid table number")

        # Parse the table using `pandas`
        df = pd.read_html(str(table), index_col="Symbol", header=0)[0]

        # Return the DataFrame containing the parsed table
        return df

    def get_overview(self, symbol):
        """
        Make a GET request to the Alpha Vantage API to get overview data for
        the given symbol.
        """
        # Set the parameters for the request
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": self.api_key
        }

        # Create the full URL using the base URL and the query string
        url = self.api_url + "?" + urlencode(params)

        # Make a GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()
            response = r.json()
        except requests.exceptions.RequestException as e:
            # Handle any errors that occur when making the request
            raise Exception(f"Error: Could not get overview data for symbol {symbol}") from e
        except ValueError as e:
            # Handle any errors that occur when parsing the response
            raise Exception(f"Error: Could not parse response for symbol {symbol}") from e

        # Return the response from the API
        return response


    def get_data(self):
        """
        Get overview data for each symbol in the `df` DataFrame and append the
        data to a new DataFrame called `data`. Add a delay of 12 seconds
        between each request to ensure that only 5 requests are made per minute.
        """

        # Create an empty DataFrame to store the data
        data = pd.DataFrame()

        # Iterate over the symbols in the dataframe
        for symbol in self.df.index:
            # Get the overview data for the symbol
            response = self.get_overview(symbol)

            # Check if the response contains an error
            if "Error Message" in response:
                raise Exception(f"Error: {response['Error Message']}")

            # Append the overview data to the DataFrame
            data = data.append(response, ignore_index=True)

            # Check if there are more than 5 symbols in the DataFrame
            if len(self.df.index) > 5:
                # Wait 12 seconds before making the next request
                time.sleep(12)

        # Return the DataFrame containing the overview data
        return data


