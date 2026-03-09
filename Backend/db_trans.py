import pandas as pd
from sqlalchemy import create_engine

# 1. Connection Settings
USER = 'postgres'
PASSWORD = '8U8T5K8U' 
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'German_Credit_Risk'

# 2. Connection Engine
connection_string = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
engine = create_engine(connection_string)

try:
    # 3. Read CSV Data
    df = pd.read_csv("german_credit_data.csv")
    
    # 4. Clean up column names 
    #df.columns = [c.lower().replace(' ', '_') for c in df.columns]

    # 5. Insert data into SQL
    df.to_sql('prediction_logs', engine, if_exists='append', index=False, schema='public')
    
    print("✅ Connection successful and data inserted into SQL!")
except Exception as e:
    print(f"❌ Error occurred: {e}")