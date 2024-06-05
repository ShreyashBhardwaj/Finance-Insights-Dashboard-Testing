import yfinance as yf
import json


def get_market_index(symbol):
    index = yf.Ticker(symbol)
    data = index.history(period="1d")
    if not data.empty:
        data = data.to_dict()
        data_dict = {key: {str(k): v for k, v in value.items()} for key, value in
                                          data.items()}
        return data_dict
    else:
        return None


def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


# Example usage
index_symbol = '^BSESN'  # Yahoo Finance symbol for BSE SENSEX
index_data = get_market_index(index_symbol)
if index_data:
    save_to_file(index_data, f'{index_symbol}_index_data.json')
    print(f"Market index data saved to {index_symbol}_index_data.json")
else:
    print("Failed to retrieve market index data")
