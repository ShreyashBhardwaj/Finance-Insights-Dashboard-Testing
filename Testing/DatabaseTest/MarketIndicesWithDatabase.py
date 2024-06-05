import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine


# Function to fetch market index data
def get_market_indices(symbol):
    try:
        market_indices = yf.Ticker(symbol)
        data = market_indices.history(period="1mo")
        data.fillna(method='bfill', inplace=True)
        data.dropna(inplace=True)
        data.index = pd.to_datetime(data.index)
        data.drop_duplicates(inplace=True)

        if not data.empty:
            return data
        else:
            print(f"No data available for {symbol}")
            return None
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


# MySQL database connection details
db_user = 'root'
db_password = 'sanat123'
db_host = 'localhost'  # or your MySQL server IP/hostname
db_name = 'test_schema'

# Creating database connection
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

index_symbols = ['^NSEI', '^BSESN']

for symbol in index_symbols:
    index_data = get_market_indices(symbol)
    if index_data is not None:
        try:
            # Rename the columns to match the MySQL table schema
            index_data.rename(columns={
                'Open': 'open_price',
                'High': 'high_price',
                'Low': 'low_price',
                'Close': 'close_price',
                'Volume': 'volume'
            }, inplace=True)

            # Reset index to use the 'Date' column
            index_data.reset_index(inplace=True)
            index_data.rename(columns={'Date': 'date_time'}, inplace=True)

            # Add a 'symbol' column to store the symbol information
            index_data['symbol'] = symbol

            # Reorder columns to match MySQL table schema
            index_data = index_data[
                ['date_time', 'symbol', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']]

            # Save the data to MySQL table
            index_data.to_sql(name='MarketIndexData', con=engine, if_exists='append', index=False)
            print(f"Market Index Data saved in MySQL for {symbol}")
        except Exception as e:
            print(f"Error saving data to MySQL for {symbol}: {e}")
    else:
        print(f"Failed to retrieve Market Index Data for {symbol}")
