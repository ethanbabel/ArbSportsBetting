import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

mydb = mysql.connector.connect(
    host = os.getenv('DATABASE_HOST'),
    user = os.getenv('DATABASE_USER'),
    passwd= os.getenv('DATABASE_PASSWORD'),
    database="ArbSportsBetting"
)

cursor = mydb.cursor()

cursor.execute("SET foreign_key_checks = 0")

cursor.execute("SELECT TABLE_NAME \
        FROM INFORMATION_SCHEMA.TABLES \
        WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='ArbSportsBetting' ")
tables = cursor.fetchall()
for table in tables:
    if not(table[0] == 'Historical'):
        cursor.execute(f"DROP TABLE {table[0]}")

cursor.execute("SHOW TABLES")
for table in cursor: 
    print(table)

cursor.execute("SET foreign_key_checks = 1") 