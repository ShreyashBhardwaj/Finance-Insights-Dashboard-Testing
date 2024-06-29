import yfinance as yf
import pandas as pd
import mysql.connector

# Function to fetch stock data
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)

        # Get historical data
        historical_data = stock.history(period="5y")

        # Get current data
        current_data = stock.info

        if not historical_data.empty:
            # Add 'symbol' column to historical data
            historical_data['symbol'] = symbol

            # Reset index and rename 'Date' column to match MySQL table schema
            historical_data.reset_index(inplace=True)
            historical_data['date_time'] = historical_data['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')

            # Reorder columns to match MySQL table schema
            historical_data = historical_data[['date_time', 'symbol', 'Open', 'High', 'Low', 'Close', 'Volume']]

            # Convert current data to a DataFrame
            current_data_df = pd.DataFrame({
                'symbol': [symbol],
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
try:
    cnx = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_name)
    cursor = cnx.cursor()

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
        historical_data, current_data = get_stock_data(symbol)
        if historical_data is not None and current_data is not None:
            try:
                # Start a transaction
                cursor.execute("START TRANSACTION")

                # Check if historical data exists
                cursor.execute("SELECT COUNT(*) FROM HistoricalStockData WHERE symbol = %s", (symbol,))
                count = cursor.fetchone()[0]
                if count > 0:
                    print("Delete old data and Insert new Data")
                    # Delete existing historical data for the symbol
                    cursor.execute("DELETE FROM HistoricalStockData WHERE symbol = %s", (symbol,))

                # Insert new historical data
                historical_data_columns = ', '.join(historical_data.columns)
                historical_data_values = [tuple(x) for x in historical_data.to_numpy()]
                cursor.executemany(f"INSERT INTO HistoricalStockData ({historical_data_columns}) VALUES (%s, %s, %s, %s, %s, %s, %s)", historical_data_values)
                print(f"Historical stock data saved in MySQL for {symbol}")

                # Check if current data exists
                cursor.execute("SELECT COUNT(*) FROM CurrentStockData WHERE symbol = %s", (symbol,))
                count = cursor.fetchone()[0]
                if count > 0:
                    # Delete existing current data for the symbol
                    cursor.execute("DELETE FROM CurrentStockData WHERE symbol = %s", (symbol,))

                # Insert new current data
                current_data_columns = ', '.join(current_data.columns)
                current_data_values = [tuple(current_data.values.tolist()[0])]
                cursor.executemany(f"INSERT INTO CurrentStockData ({current_data_columns}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", current_data_values)
                print(f"Current stock data saved in MySQL for {symbol}")

                # Commit the transaction
                cnx.commit()

            except Exception as e:
                print(f"Error saving data to MySQL for {symbol}: {e}")
                # Rollback on error
                cnx.rollback()
        else:
            print(f"Failed to retrieve stock data for {symbol}")

    cursor.close()
    cnx.close()

except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
