import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host = os.getenv('DATABASE_HOST'),
    user = os.getenv('DATABASE_USER'),
    passwd= os.getenv('DATABASE_PASSWORD'),
    database="ArbSportsBetting"
)

cursor = mydb.cursor()

cursor.execute("CREATE TABLE Events (id VARCHAR(100) NOT NULL, \
        sport VARCHAR(100) NOT NULL, \
        team1 VARCHAR(100) NOT NULL, \
        team2 VARCHAR(100) NOT NULL, \
        dt VARCHAR(20) NOT NULL, \
        PRIMARY KEY(id))")


cursor.execute("CREATE TABLE team1odds (id INT NOT NULL AUTO_INCREMENT, \
    eventID VARCHAR(100) NOT NULL, \
    team VARCHAR(100) NOT NULL, \
    spread FLOAT NOT NULL, \
    odds VARCHAR(500), \
    books VARCHAR(500), \
    PRIMARY KEY (id), \
    FOREIGN KEY (eventID) REFERENCES Events(id))")

cursor.execute("CREATE TABLE team2odds (id INT NOT NULL AUTO_INCREMENT, \
    eventID VARCHAR(100) NOT NULL, \
    team VARCHAR(100) NOT NULL, \
    spread FLOAT NOT NULL, \
    odds VARCHAR(500) , \
    books VARCHAR(500), \
    PRIMARY KEY (id), \
    FOREIGN KEY (eventID) REFERENCES Events(id))")

cursor.execute("CREATE TABLE Arbs (id INT NOT NULL AUTO_INCREMENT, \
    sport VARCHAR(100) Not Null, \
    eventID VARCHAR(100) NOT NULL, \
    spread FLOAT NOT NULL, \
    teamFavorite VARCHAR(100) NOT NULL, \
    oddFavorite FLOAT NOT NULL, \
    bookFavorite VARCHAR(100) NOT NULL, \
    teamUnderdog VARCHAR(100) NOT NULL, \
    oddUnderdog FLOAT NOT NULL, \
    bookUnderdog VARCHAR(100) NOT NULL, \
    profitPercentage FLOAT NOT NULL, \
    UNIQUE(sport, eventID, spread, bookFavorite, bookUnderdog), \
    PRIMARY KEY (id), \
    FOREIGN KEY (eventID) REFERENCES Events(id))")

# cursor.execute("CREATE TABLE Historical (id INT NOT NULL AUTO_INCREMENT, \
#     profitPercentage FLOAT NOT NULL, \
#     dt VARCHAR(20) NOT NULL, \
#     PRIMARY KEY (id))")

cursor.execute("DESCRIBE Events")
for x in cursor:
    print(x)

cursor.execute("DESCRIBE team1odds")
for x in cursor:
    print(x)

cursor.execute("DESCRIBE team2odds")
for x in cursor:
    print(x)

cursor.execute("DESCRIBE Arbs")
for x in cursor:
    print(x)

cursor.execute("DESCRIBE Historical")
for x in cursor:
    print(x)

mydb.commit()