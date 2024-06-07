import yfinance as yf
import json

def get_balance_sheet(symbol):
    try:
        stock = yf.Ticker(symbol)
        balance_sheet = stock.balance_sheet
        if not balance_sheet.empty:
            # Convert DataFrame to dictionary and ensure all keys are strings
            balance_sheet_dict = balance_sheet.to_dict()
            balance_sheet_converted = {
                str(key): {str(inner_key): inner_value for inner_key, inner_value in value.items()}
                for key, value in balance_sheet_dict.items()
            }
            return balance_sheet_converted
        else:
            print(f"No balance sheet data available for {symbol}")
            return None
    except Exception as e:
        print(f"Error fetching balance sheet data for {symbol}: {e}")
        return None

def save_to_file(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to file: {e}")

symbol = "RELIANCE.BO"
balance_sheet_data = get_balance_sheet(symbol)
if balance_sheet_data is not None:
    save_to_file(balance_sheet_data, f"{symbol}_balance_sheet_data.json")
else:
    print(f"No data to save for {symbol}")
