import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host = os.getenv('DATABASE_HOST'),
    user = os.getenv('DATABASE_USER'),
    passwd= os.getenv('DATABASE_PASSWORD')
)

cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS ArbSportsBetting")



