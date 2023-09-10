import requests
import pandas as pd
import yfinance as yf

from io import StringIO



def get_dividend_yield(symbol,field='dividendYield'):
  try:
      # Use Yahoo Finance to fetch dividend yield data
      stock = yf.Ticker(symbol)
      dividend_yield = stock.info.get(field, None)
      print("success for "+symbol)
      return dividend_yield
  except Exception as e:
      print(f"Error fetching data for {symbol}: {str(e)}")
      return None


# Replace 'YOUR_API_KEY' with your Alpha Vantage API key
api_key = 'HOG8WJ5U6FDNIBQD'

# Define the API endpoint to retrieve stock symbols in CSV format
endpoint = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}'


dividend_treshhold = 0.03

# Send a GET request to the API
response = requests.get(endpoint)

# Check if the request was successful
if response.status_code == 200:

    # Read the CSV data from the response content
    csv_data = StringIO(response.text)

    # Create a DataFrame from the CSV data
    df = pd.read_csv(csv_data)

    # Filter for rows with 'status' as 'Active' and 'assetType' as 'stock'
    active_stocks = df[(df['status'] == 'Active') & (df['assetType'] == 'Stock')]

    # Extract the 'symbol' column to get stock symbols
    symbols = active_stocks['symbol']

    df = pd.DataFrame({'Symbol': symbols})

    df['Dividend Yield'] = df['Symbol'].apply(get_dividend_yield)
else:
  print("something went wrong")
  
df['Dividend Yield'] = pd.to_numeric(df['Dividend Yield'], errors='coerce')
high_yield_stocks = df[df['Dividend Yield'] > dividend_treshhold]  
high_yield_stocks_sorted = high_yield_stocks.sort_values(by='Dividend Yield', ascending=False)
output_csv_filename = 'high_yield_stocks.csv'
high_yield_stocks_sorted.to_csv(output_csv_filename, index=False)
