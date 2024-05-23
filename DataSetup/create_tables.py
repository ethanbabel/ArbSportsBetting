import mysql.connector

mydb = mysql.connector.connect(
    host="arbsportsbettingdatabase.czcyyswyshyy.us-west-1.rds.amazonaws.com",
    user="admin",
    passwd="ArbSportsBettingsasha4",
    database="ArbSportsBetting"
)

cursor = mydb.cursor()

cursor.execute("CREATE TABLE Events (id VARCHAR(100) NOT NULL, \
        sport VARCHAR(100) NOT NULL, \
        team1 VARCHAR(100) NOT NULL, \
        team2 VARCHAR(100) NOT NULL, \
        dt VARCHAR(20) NOT NULL, \
        PRIMARY KEY(id))")


cursor.execute("CREATE TABLE OverDog (id INT NOT NULL AUTO_INCREMENT, \
    eventID VARCHAR(100) NOT NULL, \
    spread FLOAT NOT NULL, \
    betonlineag FLOAT, \
    betmgm FLOAT, \
    betrivers FLOAT, \
    betus FLOAT, \
    bovada FLOAT, \
    draftkings FLOAT, \
    fanduel FLOAT, \
    lowvig FLOAT, \
    mybookieag FLOAT, \
    pointsbetus FLOAT, \
    superbook FLOAT, \
    unibet_us FLOAT, \
    williamhill_us FLOAT, \
    wynnbet FLOAT, \
    ballybet FLOAT, \
    betparx FLOAT, \
    espnbet FLOAT, \
    fliff FLOAT, \
    hardrockbet FLOAT, \
    sisportsbook FLOAT, \
    tipico_us FLOAT, \
    windcreek FLOAT, \
    PRIMARY KEY (id), \
    FOREIGN KEY (eventID) REFERENCES Events(id))")

cursor.execute("CREATE TABLE UnderDog (id INT NOT NULL AUTO_INCREMENT, \
    eventID VARCHAR(100) NOT NULL, \
    spread FLOAT NOT NULL, \
    betonlineag FLOAT, \
    betmgm FLOAT, \
    betrivers FLOAT, \
    betus FLOAT, \
    bovada FLOAT, \
    draftkings FLOAT, \
    fanduel FLOAT, \
    lowvig FLOAT, \
    mybookieag FLOAT, \
    pointsbetus FLOAT, \
    superbook FLOAT, \
    unibet_us FLOAT, \
    williamhill_us FLOAT, \
    wynnbet FLOAT, \
    ballybet FLOAT, \
    betparx FLOAT, \
    espnbet FLOAT, \
    fliff FLOAT, \
    hardrockbet FLOAT, \
    sisportsbook FLOAT, \
    tipico_us FLOAT, \
    windcreek FLOAT, \
    PRIMARY KEY (id), \
    FOREIGN KEY (eventID) REFERENCES Events(id))")


cursor.execute("DESCRIBE Events")
for x in cursor:
    print(x)

cursor.execute("DESCRIBE OverDog")
for x in cursor:
    print(x)

cursor.execute("DESCRIBE UnderDog")
for x in cursor:
    print(x)

mydb.commit()

