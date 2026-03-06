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
    # 3. CSV'yi Oku
    df = pd.read_csv("german_credit_data.csv")
    
    # 4. Sütun isimlerini temizle (SQL boşluk sevmez)
    #df.columns = [c.lower().replace(' ', '_') for c in df.columns]

    # 5. SQL'e Gönder
    # 'credit_table' isminde bir tabloyu otomatik oluşturur
    # 'schema' ekleyerek yerini garantiye alıyoruz
    df.to_sql('credit_table', engine, if_exists='replace', index=False, schema='public')
    
    print("✅ CConnection successful and data inserted into SQL!")
except Exception as e:
    print(f"❌ Error occurred: {e}")