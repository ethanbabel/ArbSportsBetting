import mysql.connector

mydb = mysql.connector.connect(
    host="arbsportsbettingdatabase.czcyyswyshyy.us-west-1.rds.amazonaws.com",
    user="admin",
    passwd="ArbSportsBettingsasha4"
)

cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS ArbSportsBetting")



