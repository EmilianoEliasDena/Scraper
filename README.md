# Scraper
'scraper.py' is a Python module that defines my own personal 'Scraper class'. The objective is to scrape the Dow Jones Stocks and get an overview of each stock through Alpha Vantage API.
This class has the following methods:

'init': This is the constructor method that is called when an instance of the Scraper class is created. It takes the URL of the page to scrape (SOURCE: Wikipedia) and the API key for the Alpha Vantage API as arguments, and initializes the following instance variables:

'self.url': The URL of the page to scrape
'self.api_key': The API key for the Alpha Vantage API
'self.base_url': The base URL for the Alpha Vantage API

'parse_page': This method fetches the HTML content of the page at the URL specified in the 'self.url' instance variable, and parses it using the 'BeautifulSoup' library. It returns the 'BeautifulSoup' object representing the parsed HTML.

'parse_table': This method takes the 'BeautifulSoup' object returned by 'parse_page' as an argument, and uses it to find the table on the page that you want to scrape. It then uses the pandas library to read the table data into a DataFrame and return it.

'get_overview': This method makes a GET request to the Alpha Vantage API to get overview data for a given symbol. It takes the symbol as an argument, constructs the URL for the request using the 'self.base_url' and 'self.api_key' instance variables, and makes the request using the 'requests' library. It returns the response from the API as a dictionary.

'get_data': This method iterates over the symbols in the 'self.df' DataFrame and calls 'get_overview' for each symbol to get the overview data. It appends the overview data to a new DataFrame called data and returns it.
