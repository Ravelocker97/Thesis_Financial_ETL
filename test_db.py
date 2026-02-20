import sqlalchemy
from sqlalchemy import create_engine, text

# --- CONFIGURATION ---
# PASTE YOUR FULL URI HERE (Make sure to replace [YOUR-PASSWORD] with your real password)
# It should look like: "postgresql://postgres.xxxx:mypassword@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
DATABASE_URL = "postgresql://postgres.szswjvznvllkpihitwqg:Amal3208motia@aws-1-eu-west-1.pooler.supabase.com:5432/postgres"

# Fix for Supabase "Transaction" mode (optional, but good practice)
# If your URL starts with "postgres://", change it to "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def test_connection():
    print("--- 1. Connecting to Supabase... ---")
    
    try:
        # Create the engine
        engine = create_engine(DATABASE_URL)
        
        # Connect
        with engine.connect() as connection:
            print("--- 2. Connection Successful! ---")
            
            # Run a simple SQL query
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"--- 3. Database Version: {version} ---")
            
            # Create a dummy table to prove we have 'Write' access
            print("--- 4. Creating a test table... ---")
            connection.execute(text("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, message TEXT);"))
            connection.commit() # Save changes
            print("--- 5. Table 'test_table' created successfully! ---")
            
    except Exception as e:
        print("\n!!! ERROR !!!")
        print(e)

if __name__ == "__main__":
    test_connection()