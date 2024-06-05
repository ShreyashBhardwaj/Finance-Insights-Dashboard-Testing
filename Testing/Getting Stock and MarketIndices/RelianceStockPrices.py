import yfinance as yf
import json


def get_stock_price(symbol):
    stock = yf.Ticker(symbol)

    # Get historical data
    historical_data = stock.history(period="1d")

    # Get current data
    current_data = stock.info

    if not historical_data.empty:
        # Convert Timestamp keys to string format for historical data
        historical_data_dict = historical_data.to_dict()
        converted_historical_data_dict = {key: {str(k): v for k, v in value.items()} for key, value in
                                          historical_data_dict.items()}

        # Combine historical and current data
        combined_data = {
            'historical_data': converted_historical_data_dict,
            'current_data': current_data
        }

        return combined_data
    else:
        return None


def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


# Example usage
symbol = ["RELIANCE.BO","TCS.BO","HDFCBANK.BO","INFY.BO", "SBIN.BO"]  # Yahoo Finance symbol for Reliance Industries Limited on BSE
for sym in symbol:
    stock_data = get_stock_price(sym)
    if stock_data:
        save_to_file(stock_data, f'{sym}_stock_data.json')
        print(f"Stock data for {sym} saved to {sym}_stock_data.json")
    else:
        print(f"Failed to retrieve stock price data for {sym}")

