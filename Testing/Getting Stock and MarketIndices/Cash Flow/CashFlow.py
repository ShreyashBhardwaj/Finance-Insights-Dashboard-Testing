import yfinance as yf
import json

def get_Cash_Flow(symbol):
    try:
        stock = yf.Ticker(symbol)
        cash_flow = stock.cash_flow
        if not cash_flow.empty:
            # Convert DataFrame to dictionary and ensure all keys are strings
           cash_flow_dict = cash_flow.to_dict()
           cash_flow_converted = {
               str(key): {str(inner_key): inner_value for inner_key, inner_value in value.items()}
               for key, value in cash_flow_dict.items()
           }
           return cash_flow_converted
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

nifty_50_symbols = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HDFC.NS",
    "ICICIBANK.NS", "KOTAKBANK.NS", "HINDUNILVR.NS", "SBIN.NS", "BAJFINANCE.NS",
    "BHARTIARTL.NS", "ASIANPAINT.NS", "ITC.NS", "AXISBANK.NS", "LT.NS",
    "DMART.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "TITAN.NS", "NESTLEIND.NS",
    "WIPRO.NS", "MARUTI.NS", "M&M.NS", "HCLTECH.NS", "NTPC.NS",
    "TECHM.NS", "POWERGRID.NS", "TATAMOTORS.NS", "INDUSINDBK.NS", "SBILIFE.NS",
    "TATASTEEL.NS", "GRASIM.NS", "BAJAJFINSV.NS", "ADANIGREEN.NS", "CIPLA.NS",
    "ONGC.NS", "HDFCLIFE.NS", "BPCL.NS", "JSWSTEEL.NS", "COALINDIA.NS",
    "BRITANNIA.NS", "HEROMOTOCO.NS", "SHREECEM.NS", "DABUR.NS", "ADANIPORTS.NS",
    "EICHERMOT.NS", "DIVISLAB.NS", "HINDALCO.NS", "UPL.NS", "APOLLOHOSP.NS"
]
for symbol in nifty_50_symbols:
    cash_flow_data = get_Cash_Flow(symbol)
    if cash_flow_data is not None:
        save_to_file(cash_flow_data, f"{symbol}_cash_flow_data.json")
    else:
        print(f"No data to save for {symbol}")
