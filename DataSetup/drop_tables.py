import mysql.connector

mydb = mysql.connector.connect(
    host="arbsportsbettingdatabase.czcyyswyshyy.us-west-1.rds.amazonaws.com",
    user="admin",
    passwd="ArbSportsBettingsasha4",
    database="ArbSportsBetting"
)

cursor = mydb.cursor()

cursor.execute("SET foreign_key_checks = 0")

cursor.execute("SELECT TABLE_NAME \
        FROM INFORMATION_SCHEMA.TABLES \
        WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='ArbSportsBetting' ")
tables = cursor.fetchall()

for table in tables:
    cursor.execute(f"DROP TABLE {table[0]}")

cursor.execute("SHOW TABLES")
for table in cursor: 
    print(table)

cursor.execute("SET foreign_key_checks = 1") 