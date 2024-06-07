import yfinance as yf
import json


def get_asset_profile(symbol):
    try:
        stock = yf.Ticker(symbol)
        asset_profile = stock.info

        if asset_profile:
            return asset_profile
        else:
            print(f"No asset profile data available for {symbol}")
            return None
    except Exception as e:
        print(f"Error fetching asset profile data for {symbol}: {e}")
        return None


def save_to_file(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to file: {e}")


symbol = "RELIANCE.BO"
asset_profile_data = get_asset_profile(symbol)
if asset_profile_data is not None:
    save_to_file(asset_profile_data, f"{symbol}_asset_profile_data.json")
else:
    print(f"No data to save for {symbol}")
