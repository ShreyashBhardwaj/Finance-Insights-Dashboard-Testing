import pandas as pd
from sqlalchemy import create_engine

# MySQL database connection details
db_user = 'root'
db_password = 'sanat123'
db_host = 'localhost'  # or your MySQL server IP/hostname
db_name = 'test_schema'

# Creating database connection
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

# Function to fetch historical stock data for a given symbol
def fetch_historical_data(symbol):
    try:
        query = f"SELECT * FROM HistoricalStockData WHERE symbol = '{symbol}'"
        historical_data = pd.read_sql(query, con=engine)
        return historical_data
    except Exception as e:
        print(f"Error fetching historical data for {symbol}: {e}")
        return None

# Function to fetch current stock data for a given symbol
def fetch_current_data(symbol):
    try:
        query = f"SELECT * FROM CurrentStockData WHERE symbol = '{symbol}'"
        current_data = pd.read_sql(query, con=engine)
        return current_data
    except Exception as e:
        print(f"Error fetching current data for {symbol}: {e}")
        return None

# Example usage
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
    # Fetch and print historical data
    historical_data = fetch_historical_data(symbol)
    if historical_data is not None:
        print(f"Historical data for {symbol}:")
        print(historical_data)
    else:
        print(f"Failed to retrieve historical data for {symbol}")

    # Fetch and print current data
    current_data = fetch_current_data(symbol)
    if current_data is not None:
        print(f"Current data for {symbol}:")
        print(current_data)
    else:
        print(f"Failed to retrieve current data for {symbol}")
