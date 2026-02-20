# src/extract.py
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, text
import config  # This imports your password safely

def fetch_data():
    """
    1. EXTRACT: Get live data from Yahoo Finance
    """
    print(f"--- Fetching data for: {config.ASSETS} ---")
    
    # download() fetches data. 
    # period='1d' means "get today's data"
    # interval='1m' means "give me minute-by-minute data"
    data = yf.download(
        tickers=config.ASSETS, 
        period="1d", 
        interval="1m", 
        group_by='ticker', 
        auto_adjust=True,
        prepost=True, 
        threads=True 
    )
    
    # 2. TRANSFORM: Clean the data to fit our Database
    # Yahoo gives a weird format (MultiIndex), we need to flatten it.
    frames = []
    for ticker in config.ASSETS:
        try:
            # Get the specific dataframe for this ticker
            df_ticker = data[ticker].copy()
            
            # Reset index so 'Datetime' becomes a column, not the index
            df_ticker.reset_index(inplace=True)
            
            # Add a column for the symbol (e.g., 'AAPL')
            df_ticker['symbol'] = ticker
            
            # Standardize column names (Lowercase is better for SQL)
            df_ticker.columns = [c.lower() for c in df_ticker.columns]
            
            # Rename 'date' or 'datetime' to specific 'timestamp'
            if 'date' in df_ticker.columns:
                df_ticker.rename(columns={'date': 'timestamp'}, inplace=True)
            elif 'datetime' in df_ticker.columns:
                df_ticker.rename(columns={'datetime': 'timestamp'}, inplace=True)
            
            # Keep only the columns we need
            df_ticker = df_ticker[['timestamp', 'open', 'high', 'low', 'close', 'volume', 'symbol']]
            
            frames.append(df_ticker)
        except KeyError:
            print(f"Warning: No data found for {ticker}")

    if not frames:
        print("No data fetched!")
        return
        
    # Combine all tickers into one big table
    final_df = pd.concat(frames)
    print(f"--- Extracted {len(final_df)} rows of data ---")
    
    return final_df

def load_to_db(df):
    """
    3. LOAD: Save the data to Supabase
    """
    try:
        print("--- Connecting to Database... ---")
        engine = create_engine(config.DB_URL)
        
        # 'if_exists="append"' means: Add new rows, don't delete old ones!
        # 'index=False' means: Don't save the row numbers (0,1,2...)
        df.to_sql('market_data', engine, if_exists='append', index=False)
        
        print("--- Success! Data loaded to Supabase table 'market_data' ---")
        
    except Exception as e:
        print(f"Error loading to DB: {e}")

if __name__ == "__main__":
    # Run the Pipeline
    df_market = fetch_data()
    if df_market is not None:
        load_to_db(df_market)