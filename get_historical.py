import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

mydb = mysql.connector.connect(
    host = os.getenv('DATABASE_HOST'),
    user = os.getenv('DATABASE_USER'),
    passwd = os.getenv('DATABASE_PASSWORD'),
    database = "ArbSportsBetting"
)

cursor = mydb.cursor()

cursor.execute("SELECT AVG(profitPercentage) FROM Historical")
for x in cursor:
    print(x)