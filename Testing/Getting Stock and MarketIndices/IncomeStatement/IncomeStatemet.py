import yfinance as yf
import json

def get_income_statement(symbol):
    try:
        stock = yf.Ticker(symbol)
        income_stmt = stock.quarterly_income_stmt
        if not income_stmt.empty:
            # Convert DataFrame to dictionary and ensure all keys are strings
           income_stmt_dict = income_stmt.to_dict()
           income_stmt_converted = {
               str(key): {str(inner_key): inner_value for inner_key, inner_value in value.items()}
               for key, value in income_stmt_dict.items()
           }
           return income_stmt_converted
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
income_statement_data = get_income_statement(symbol)
if income_statement_data is not None:
    save_to_file(income_statement_data, f"{symbol}_quaterlyincome_statement_data.json")
else:
    print(f"No data to save for {symbol}")
