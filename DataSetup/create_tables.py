import mysql.connector

mydb = mysql.connector.connect(
    host="arbsportsbettingdatabase.czcyyswyshyy.us-west-1.rds.amazonaws.com",
    user="admin",
    passwd="ArbSportsBettingsasha4",
    database="ArbSportsBetting"
)

cursor = mydb.cursor()

cursor.execute("CREATE TABLE Events (id VARCHAR(100) NOT NULL, \
        team1 VARCHAR(100) NOT NULL, \
        team2 VARCHAR(100) NOT NULL, \
        dt DATETIME NOT NULL, \
        PRIMARY KEY(id))")

cursor.execute("CREATE TABLE Spreads (id INT NOT NULL AUTO_INCREMENT, \
        eventID VARCHAR(100) NOT NULL, \
        spread SMALLINT NOT NULL, \
        posSpreadID INT NOT NULL, \
        negSpreadID INT NOT NULL, \
        PRIMARY KEY (id), \
        FOREIGN KEY (eventID) REFERENCES Events(id))")

cursor.execute("CREATE TABLE PosOdds (id INT NOT NULL AUTO_INCREMENT, \
    spreadID INT NOT NULL, \
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
    FOREIGN KEY (spreadID) REFERENCES Spreads(id))")

cursor.execute("CREATE TABLE NegOdds (id INT NOT NULL AUTO_INCREMENT, \
    spreadID INT NOT NULL, \
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
    FOREIGN KEY (spreadID) REFERENCES Spreads(id))")


cursor.execute("DESCRIBE Events")
for x in cursor:
    print(x)

cursor.execute("DESCRIBE Spreads")
for x in cursor:
    print(x)

cursor.execute("DESCRIBE PosOdds")
for x in cursor:
    print(x)

cursor.execute("DESCRIBE NegOdds")
for x in cursor:
    print(x)

