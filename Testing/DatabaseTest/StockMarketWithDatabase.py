import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine


# Function to fetch stock data
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)

        # Get historical data
        historical_data = stock.history(period="1mo")

        # Get current data
        current_data = stock.info

        if not historical_data.empty:
            # Add 'symbol' column to historical data
            historical_data['symbol'] = symbol

            # Reset index and rename 'Date' column to match MySQL table schema
            historical_data.reset_index(inplace=True)
            historical_data.rename(columns={'Date': 'date_time'}, inplace=True)

            # Reorder columns to match MySQL table schema
            historical_data = historical_data[['date_time', 'symbol', 'Open', 'High', 'Low', 'Close', 'Volume']]

            # Convert current data to a DataFrame
            current_data_df = pd.DataFrame({
                'symbol': symbol,
                'marketCap': [current_data.get('marketCap', None)],
                'forwardPE': [current_data.get('forwardPE', None)],
                'trailingPE': [current_data.get('trailingPE', None)],
                'dayHigh': [current_data.get('dayHigh', None)],
                'dayLow': [current_data.get('dayLow', None)],
                'fiftyTwoWeekHigh': [current_data.get('fiftyTwoWeekHigh', None)],
                'fiftyTwoWeekLow': [current_data.get('fiftyTwoWeekLow', None)],
                'dividendYield': [current_data.get('dividendYield', None)],
                'beta': [current_data.get('beta', None)],
                'primaryExchange': [current_data.get('primaryExchange', None)],
                'currency': [current_data.get('currency', None)]
            })

            return historical_data, current_data_df
        else:
            print(f"No historical data available for {symbol}")
            return None, None
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None


# MySQL database connection details
db_user = 'root'
db_password = 'sanat123'
db_host = 'localhost'  # or your MySQL server IP/hostname
db_name = 'test_schema'

# Creating database connection
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

stock_symbols = ["RELIANCE.BO", "TCS.BO", "HDFCBANK.BO", "INFY.BO", "SBIN.BO"]

for symbol in stock_symbols:
    historical_data, current_data = get_stock_data(symbol)
    if historical_data is not None and current_data is not None:
        try:
            # Save historical data to MySQL table
            historical_data.to_sql(name='HistoricalStockData', con=engine, if_exists='append', index=False)
            print(f"Historical stock data saved in MySQL for {symbol}")

            # Save current data to MySQL table
            current_data.to_sql(name='CurrentStockData', con=engine, if_exists='append', index=False)
            print(f"Current stock data saved in MySQL for {symbol}")
        except Exception as e:
            print(f"Error saving data to MySQL for {symbol}: {e}")
    else:
        print(f"Failed to retrieve stock data for {symbol}")
