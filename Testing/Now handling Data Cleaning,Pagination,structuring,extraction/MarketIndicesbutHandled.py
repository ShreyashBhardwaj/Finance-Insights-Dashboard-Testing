import yfinance as yf
import json
import pandas as pd


def get_market_indices(symbol):
    try:
        market_indices = yf.Ticker(symbol)
        data = market_indices.history(period="1mo")
        data.fillna(method='bfill', inplace=True)
        data.dropna(inplace=True)  # Specify axis to drop rows
        data.index = pd.to_datetime(data.index)
        data.drop_duplicates(inplace=True)

        if not data.empty:
            data_dict = data.to_dict()
            data_dict = {key: {str(k): v for k, v in values.items()} for key, values in data_dict.items()}
            return data_dict
        else:
            print(f"No data available for {symbol}")
            return None
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


index_symbols = ['^NSEI', '^BSESN']

for symbol in index_symbols:
    index_data = get_market_indices(symbol)
    if index_data:
        save_to_file(index_data, f'{symbol}_index_data.json')
        print(f"Market Index Data saved in {symbol}_index_data.json")
    else:
        print(f"Failed to retrieve Market Index Data for {symbol}")
