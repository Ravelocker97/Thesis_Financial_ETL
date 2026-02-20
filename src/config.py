# src/config.py

# PASTE YOUR WORKING CONNECTION STRING HERE
# (The one that just worked with Session Pooler)
DB_URL = "postgresql://postgres.szswjvznvllkpihitwqg:Amal3208motia@aws-1-eu-west-1.pooler.supabase.com:5432/postgres"

# List of assets we want to track
# You can add more later (e.g., 'GOOGL', 'EURUSD=X')
ASSETS = ['BTC-USD', 'ETH-USD', 'AAPL', 'MSFT']