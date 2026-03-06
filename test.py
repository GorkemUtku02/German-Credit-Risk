import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="German_Credit_Risk",
    user="postgres",
    password="8U8T5K8U",
    port="5432"
)

print("Connection successful!")