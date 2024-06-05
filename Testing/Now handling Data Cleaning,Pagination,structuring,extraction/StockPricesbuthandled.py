import yfinance as yf
import json
import pandas as pd


def get_stock_price(symbol):
    stock = yf.Ticker(symbol)

    # Get historical data
    historical_data = stock.history(period="1mo")  # Fetch monthly data for more comprehensive analysis

    # Handle missing values
    historical_data.fillna(method='bfill', inplace=True)  # Forward fill missing values
    historical_data.dropna(inplace=True)  # Drop rows with remaining missing values

    # Convert data types
    historical_data.index = pd.to_datetime(historical_data.index)  # Convert index to datetime

    # Remove duplicates (if any)
    historical_data.drop_duplicates(inplace=True)

    # Convert to dictionary
    historical_data_dict = historical_data.to_dict()

    # Convert Timestamp keys to string format
    converted_historical_data_dict = {key: {str(k): v for k, v in value.items()} for key, value in
                                      historical_data_dict.items()}

    # Get current data
    current_data = stock.info

    # Combine historical and current data
    combined_data = {
        'historical_data': converted_historical_data_dict,
        'current_data': current_data
    }

    return combined_data


def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


# Example usage
symbols = ["RELIANCE.BO", "TCS.BO", "HDFCBANK.BO", "INFY.BO", "SBIN.BO"]  # Yahoo Finance symbols
for sym in symbols:
    stock_data = get_stock_price(sym)
    if stock_data:
        save_to_file(stock_data, f'{sym}_stock_data.json')
        print(f"Stock data for {sym} saved to {sym}_stock_data.json")
    else:
        print(f"Failed to retrieve stock price data for {sym}")
